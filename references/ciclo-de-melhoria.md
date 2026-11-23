# Ciclo de melhoria (estilo Harness²)

O ciclo melhora o **entorno** do modelo — prompts, busca no grafo, ferramentas, verificadores, memória — com testes comparativos. Não muda pesos; retreinar o LoRA ou editar pesos são passos separados, disparados pelo ciclo quando a falha pede.

Se a skill `harness2` estiver disponível, siga-a; este arquivo adapta os princípios ao especialista.

## Conjuntos

| Conjunto | Uso | Quem vê |
|---|---|---|
| `dev` (70%) | medir cada candidato | o ciclo |
| `holdout` (30%) | conferência final, uma vez | ninguém até o fim |

Se o `dev` for pequeno (< 70 casos), uma melhora de 2–3 acertos pode ser ruído. Rode o candidato 2–3 vezes quando a geração tiver aleatoriedade e compare médias. Para iterar e confirmar sem viciar, divida o `dev` em `dev_busca` e `dev_confirmacao` e fixe a regra de adoção antes; tamanhos e YAML em `protocolo-avaliacao.md`.

## Classificar cada falha

| Categoria | Sinal | Onde mexer |
|---|---|---|
| **Segurança** (bloqueia, vem primeiro) | obedeceu instrução escondida, entregou dado, executou ação indevida, montou link com dado | trava em código (permissão, limite na ferramenta, limpeza de entrada), nunca só o prompt; depois, teste na bateria sem modelo |
| **Fato** | resposta contradiz o material; evidência não estava no contexto | grafo (aresta faltando/errada), parâmetros do PageRank, trechos |
| **Fato ignorado** | evidência estava no contexto e o modelo não usou | prompt (ordem, destaque), LoRA treinado com contexto |
| **Forma** | conteúdo certo, formato/tom errado | prompt com exemplos; depois LoRA |
| **Ferramenta** | conta errada, consulta impossível sem dado externo | adicionar ferramenta (calculadora, consulta) |
| **Comportamento** | loop, recusa indevida, repetição, inventar regra ao recusar, não chamar o humano diante de falsa autoridade | prompt, limites de geração; por último, edição de pesos |
| **Política sem resposta** | passou para o humano porque não havia resposta aprovada | levar a pergunta ao dono como resposta aprovada; não deixar o agente improvisar |
| **Fora do domínio** | respondeu o que devia recusar | roteador |

## Um candidato por vez

Cada candidato é uma mudança pequena e nomeada: "aumentar α do PageRank de 0,7 para 0,85", "colocar evidências antes da pergunta", "adicionar calculadora". Mudanças misturadas impedem saber o que ajudou.

## Teste A/B

```
para cada candidato:
    rodar dev com a configuração atual (linha de base) e com o candidato
    comparar: acerto, acerto por categoria, custo, tempo
    adotar se: melhora clara E não piora nenhuma categoria importante
    senão: registrar como candidato não adotado
```

- **Ordem depois de cada mudança:** bateria de segurança sem modelo (de graça) → se mexeu no prompt, regressão nos perfis normais, pareada com a versão anterior → red team com modelo se mexeu em ferramentas, regras ou prompt. Uma regra nova de segurança no prompt pode aumentar a passagem para humano no atendimento normal; só a regressão mostra.
- Prefira verificação automática (resposta numérica, regex de formato, citação existente no grafo).
- Juiz LLM é um sinal que falha. Se usar, dê a ele o gabarito e peça um veredito curto; confira uma amostra à mão.

## Registro de lições

Uma entrada por mudança, adotada ou não, em `licoes.md` ou JSONL:

```
## 2026-11-21 · α do PageRank 0,7 → 0,85
Contexto: falhas de "fato" em perguntas que dependem de pré-requisitos a 2 saltos.
Mudança: α = 0,85.
Evidência: dev 61% → 67% (3 rodadas, média); categoria fato 12 → 7 falhas; custo igual.
Limite: piorou 2 perguntas de definição direta (contexto mais espalhado).
Revisar quando: o grafo crescer > 2× ou mudar o tipo de pergunta.
```

## Quando parar

- O ganho das duas últimas rodadas ficou dentro do ruído.
- As falhas restantes são de uma categoria que exige outra fase (LoRA, edição de pesos, mais material).
- O custo do ciclo já passa do valor da melhora.

Uma única rodada bem medida pode ser suficiente.

## Conferência final

Rode o `holdout` uma vez com a configuração adotada. Reporte `dev` e `holdout` lado a lado. Se o `holdout` ficar muito abaixo do `dev`, o ciclo se ajustou ao `dev`: volte algumas mudanças específicas demais e prefira as gerais.
