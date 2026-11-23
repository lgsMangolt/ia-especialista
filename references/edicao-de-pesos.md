# Edição direta de pesos (experimental)

## Origem e status

"Sparks of Weight-Space Programming", post de blog do MIT CSAIL (Takehi, Teoh, Zhang, Khattab), 2 de novembro de 2026. **Sem revisão por pares** até o momento em que esta skill foi escrita; reproduções independentes começaram em novembro de 2026 e relatam números diferentes entre si. Confira o estado atual antes de apresentar resultados como fato.

- Post e código: https://github.com/openwsp/openwsp
- Reprodução com controles: https://github.com/kyle-chalmers/weight-space-programming

No experimento principal, um modelo de ponta numa sandbox de Python analisou os pesos do Qwen3.5-0.8B, que entrava em loops de dúvida, e editou ~0,016% deles (duas matrizes `down_proj`). O MATH-500 relatado foi de 7,9% para 48,1%. O ganho veio de **consertar um defeito**, não de ensinar conteúdo.

## Quando propor

Só se todas forem verdade:
- a falha é de **comportamento** e se repete de forma reconhecível (loop, recusa indevida, um padrão de formato teimoso);
- prompt, limites de geração e LoRA já foram tentados e medidos;
- há um conjunto `dev` confiável e um `holdout` guardado;
- o usuário entende que é experimental.

## A operação

Remover uma direção `v` (comprimento 1) do que alguns neurônios escrevem:

```
para cada neurônio j escolhido:
    W[:, j] ← W[:, j] − v · (vᵀ · W[:, j])
```

`ΔW` tem posto 1: é um LoRA de rank 1 calculado, sem treino. Para guardar basta `v` e os índices (~KB).

## Achar a direção (diferença de médias)

```python
import torch

def media_ativacoes(modelo, prompts, camada):
    acts = []
    def gancho(_m, _i, saida):            # saída do bloco MLP da camada
        acts.append(saida[0].mean(dim=0) if saida.dim() == 3 else saida.mean(dim=0))
    h = modelo.model.layers[camada].mlp.register_forward_hook(gancho)
    with torch.no_grad():
        for p in prompts:
            modelo(**tokenizar(p))
    h.remove()
    return torch.stack(acts).mean(dim=0)

v = media_ativacoes(m, casos_com_defeito, L) - media_ativacoes(m, casos_sem_defeito, L)
v = v / v.norm()
```

Os nomes dos módulos variam por arquitetura; confira com `print(modelo)`. Use dezenas de casos de cada lado, tirados do `dev`, nunca do `holdout`.

## Aplicar com caminho de volta

```python
W = m.model.layers[L].mlp.down_proj.weight      # formato (d_modelo, d_mlp)
backup = W[:, neuronios].clone()
with torch.no_grad():
    cols = W[:, neuronios]
    W[:, neuronios] = cols - torch.outer(v, v @ cols)
# para desfazer: W[:, neuronios] = backup
```

Escolha dos neurônios: os que mais escrevem na direção `v` (maior `|vᵀ W[:, j]|`). Comece com poucos (16–64) e uma camada do meio.

## Controles obrigatórios

1. **Direção aleatória:** repita a edição com um `v` aleatório de mesma norma nos mesmos neurônios. Se o ganho for parecido, a edição não tem efeito específico; descarte.
2. **Sem regressão:** rode o `dev` inteiro, não só os casos do defeito. Uma edição que conserta loops e piora respostas diretas não serve.
3. **Holdout no fim**, uma vez, como em qualquer mudança.

## Teste curto (antes de mexer no especialista)

Valida a técnica num modelo pequeno antes de arriscar o especialista, em uma ou duas noites:

1. Modelo pequeno (0,5–1,7B) que caiba na GPU do usuário, separado do especialista.
2. Um defeito fácil de provocar e medir: repetição, recusa indevida ou um formato teimoso. Monte 30–50 casos com defeito e 30–50 sem.
3. Ache a direção pela diferença de médias numa camada do meio e aplique a projeção em 16–64 neurônios, com backup.
4. Meça três coisas: taxa do defeito antes/depois, a mesma edição com direção **aleatória** e uma bateria curta de perguntas normais para ver se algo piorou.
5. Registre o resultado. Só leve ao especialista se o defeito aparecer lá e o controle aleatório perder.

## Como apresentar ao usuário

Diga que é experimental, que o método vem de um post sem revisão por pares, mostre o resultado contra a linha de base e contra o controle aleatório, e mantenha o backup dos pesos originais.
