# LoRA, QLoRA e busca de hiperparâmetros

## A matemática que você precisa explicar

```
W' = W + (α/r) · B·A
W ∈ ℝ^{d×k} congelada · B ∈ ℝ^{d×r} começa em zero · A ∈ ℝ^{r×k} aleatória · r ≪ min(d,k)
```

- `B = 0` faz o modelo começar idêntico ao original; `A` aleatória garante que `B` receba gradiente.
- Parâmetros treinados por matriz: `r·(d+k)`. Ex.: `d=k=4096`, `r=8` → 65.536, ou 0,39% da matriz.
- Depois do treino, `BA` pode ser somado em `W`; a inferência não fica mais lenta.
- QLoRA: a base fica em 4 bits e o adaptador em 16. Ajustar 7–8B numa GPU de 16–24 GB; 4B em 12–16 GB.

## Quando LoRA é a ferramenta certa

| A falha é… | Use |
|---|---|
| fato errado ou faltando | grafo / RAG, não LoRA |
| formato, tom, estrutura da resposta | **LoRA** (ou primeiro, prompt com exemplos) |
| prompt de sistema enorme repetido em toda chamada | LoRA |
| comportamento isolável (loop) | prompt, depois edição de pesos |

Um few-shot que já funciona é o rascunho do dataset.

## Dataset

Formato de conversa, uma linha JSONL por exemplo:

```json
{"messages":[
  {"role":"system","content":"Você é o especialista em <domínio>."},
  {"role":"user","content":"<pergunta + evidências do grafo, como no uso real>"},
  {"role":"assistant","content":"<resposta no formato desejado>"}
]}
```

- Inclua as evidências do grafo no `user`, do mesmo jeito que o agente monta em produção. Assim o LoRA aprende a **usar** o contexto, não a decorá-lo.
- Varie dificuldade, tipo de erro e tamanho. Inclua recusas para perguntas fora do domínio.
- 500–2.000 exemplos costumam bastar para forma. Revise uma amostra à mão: o LoRA aprende os erros do dataset com a mesma fidelidade que os acertos.
- Nunca use casos do `holdout` como exemplos de treino.

## Configuração inicial razoável

| Item | Valor inicial |
|---|---|
| rank `r` | 16 |
| `α` | 16 ou 32 (com rsLoRA, a escala vira α/√r) |
| matrizes | `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` |
| taxa de aprendizado | 2e-4 |
| épocas | 1–3 |
| dropout do LoRA | 0–0,05 |

Ferramentas: Unsloth (rápido, cabe no Colab), PEFT + TRL (padrão Hugging Face), Axolotl (configuração em YAML). Depois do treino, exportar para GGUF e rodar em llama.cpp/Ollama, ou servir com vLLM (multi-LoRA).

## Busca de hiperparâmetros com Optuna (modelo de código)

Adapte ao projeto; nomes de função do treino variam por ferramenta.

```python
import optuna

def objetivo(trial):
    cfg = {
        "r": trial.suggest_categorical("r", [8, 16, 32]),
        "lr": trial.suggest_float("lr", 5e-5, 5e-4, log=True),
        "epocas": trial.suggest_int("epocas", 1, 3),
        "alvos": trial.suggest_categorical("alvos", ["atencao", "atencao+mlp"]),
    }
    adaptador = treinar_lora(cfg)              # sua função: QLoRA com Unsloth/PEFT
    return avaliar(adaptador, "evals/dev.jsonl")  # acerto no dev, NUNCA no holdout

estudo = optuna.create_study(direction="maximize")
estudo.optimize(objetivo, n_trials=15)
print(estudo.best_params)
```

- Orçamento curto (10–20 rodadas). Ganhos depois disso costumam ser ruído.
- Se cada treino demora, use um subconjunto menor do dataset na busca e treine o vencedor com tudo.
- Registre todas as rodadas, não só a melhor, para o ciclo de melhoria.

## Tamanho do adaptador

`python scripts/lora_size.py --d 2560 --k 2560 --r 16 --matrizes 7 --camadas 36` dá uma estimativa. É aproximada: as matrizes do MLP e de K/V têm dimensões diferentes; para o número exato, some `r·(d+k)` de cada matriz com as dimensões do `config.json` do modelo.

## Variantes que podem ajudar

- **DoRA:** separa magnitude e direção; costuma chegar mais perto do ajuste completo.
- **rsLoRA:** escala α/√r; estável em ranks altos.
- **LoRA+:** taxa maior para `B`.
- **PiSSA:** começa pelos componentes principais (SVD) de `W`.

## SEAL (MIT, 2025): quando o modelo gera os próprios ajustes

O modelo escreve "auto-edições" (exemplos + hiperparâmetros), treina um LoRA, e é reforçado quando melhora. É a versão automática desta fase. Só considere depois que o ciclo manual estiver medindo bem, porque cada atualização pode apagar o que o modelo sabia: rode o `dev` completo a cada passo.
