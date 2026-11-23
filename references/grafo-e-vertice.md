# Grafo do domínio e cálculo em vértice

## 0. Antes do grafo: tabela de cobertura e vigência

Para fatos tabeláveis (feriados, preços, planos, regras com data), uma tabela vale mais que um grafo. Modelo em `assets/tabela-cobertura.csv`:

- cada linha tem escopo, período, regra, efeito, **fonte** e **vigência** (`vigente_desde`, `vigente_ate`);
- a coluna `revisado` só é marcada por um responsável nomeado;
- regra do programa: se a pergunta cai num escopo ou período sem linha revisada, **recusa** e diz o que falta, em vez de calcular com dado incompleto;
- quando entra uma regra nova, recalcule o que estava em aberto e registre a data da revisão.

O mesmo vale para documentos (políticas, runbooks): guarde a data de vigência e consulte só a versão vigente na data da pergunta. Em testes reais, ~1 em cada 10 perguntas tinha duas respostas "certas" vindas de versões diferentes do mesmo documento.

Meça antes de construir um grafo: se menos de ~20% das perguntas precisam ligar 2 ou mais fatos, busca vetorial com reranker costuma bastar.

## Por que um grafo e não só busca vetorial

A busca vetorial acha trechos **parecidos** com a pergunta. O grafo acha trechos **ligados** a ela, inclusive a 2–3 saltos. Exemplo: "quanto rende R$ 1.000 a 1% ao mês?" cita *juros*; o grafo puxa *porcentagem* e *potência*, que o aluno precisa saber e que não aparecem na pergunta. Use os dois juntos: vetores para achar os vértices de partida, grafo para expandir.

## 1. Extração com evidência

```
Extraia um grafo de conhecimento do texto abaixo.
Responda SOMENTE em JSON:
{
  "nos":    [{"id": "...", "tipo": "conceito|regra|entidade", "descricao": "..."}],
  "arestas":[{"de": "...", "para": "...", "relacao": "pre_requisito|parte_de|causa|excecao_de",
              "evidencia": "trecho literal"}]
}
Regras:
- Use o mesmo id para a mesma entidade, mesmo com nomes diferentes no texto.
- Toda aresta precisa de "evidencia" copiada do texto. Sem evidência, não crie a aresta.
- Não invente relações que o texto não afirma.
TEXTO:
<<<
...
>>>
```

Escolha um vocabulário fechado de relações para o domínio (4–8 tipos). Relações livres viram ruído.

Depois de extrair:
- **Valide** que cada `evidencia` aparece de fato no texto de origem (busca de substring). Descarte as que não aparecem.
- **Mescle** ids equivalentes (normalizar acentos e caixa; pedir ao LLM uma lista de pares candidatos e revisar).
- **Revise** pelo menos 50 arestas à mão. Uma relação errada vira "fato" com cara de autoridade.

## 2. Armazenamento

Para até ~100 mil arestas, SQLite ou um JSON basta:

```sql
CREATE TABLE no (id TEXT PRIMARY KEY, tipo TEXT, descricao TEXT);
CREATE TABLE aresta (de TEXT, para TEXT, relacao TEXT, evidencia TEXT, fonte TEXT);
CREATE TABLE trecho (no_id TEXT, texto TEXT, fonte TEXT);  -- o que vai para o prompt
```

Guarde a `fonte` (arquivo, página) para o especialista citar de onde veio cada fato.

## 3. PageRank personalizado

```
p_v ← (1−α)·e_v + α · Σ_{u vizinho de v} p_u / grau_u
```

- `e` vale 1 (normalizado) nos vértices citados na pergunta e 0 nos outros.
- `α ≈ 0,85` é a chance de continuar andando; `1−α` é a chance de voltar à pergunta. `α` menor mantém o resultado perto da pergunta; maior espalha.
- Rode 20–50 rodadas ou até a mudança ficar abaixo de 1e-6. Num grafo de 50 mil vértices isso leva milissegundos.
- `scripts/ppr.py` faz isso a partir do JSON da extração. Ele pula as arestas sem evidência e lista quais pulou; mostre essa lista ao usuário, porque é um erro da extração que precisa ser corrigido na fonte.

Como achar os vértices de partida: casar nomes e sinônimos da pergunta com os ids; se nada casar, usar os 3–5 vértices mais próximos por vetor.

## 4. Montar o contexto

`python scripts/ppr.py grafo.json --semente X --top 10 --bloco` imprime o bloco pronto: conceitos com descrição e as relações entre eles com a evidência. Use `--data AAAA-MM-DD` para considerar só vértices e arestas vigentes nessa data (campos opcionais `vigente_desde` e `vigente_ate`).

Na prática, isso é busca: o bloco vira texto no prompt. A diferença para um RAG simples é que o grafo escolhe fatos compactos e ligados, com fonte, e um LoRA pode ser treinado nesse formato exato.

Pegue os 10–20 vértices de maior pontuação e, para cada um, a descrição e 1–2 trechos. Inclua as arestas entre eles com a relação ("A é pré-requisito de B"), porque o modelo raciocina melhor com a relação explícita do que com trechos soltos. Corte por orçamento de tokens, não por número fixo.

## 5. Ajustes que a busca de hiperparâmetros pode calibrar

| Parâmetro | Faixa típica |
|---|---|
| `α` | 0,5–0,9 |
| nº de vértices no contexto | 5–30 |
| trechos por vértice | 1–3 |
| peso de cada tipo de relação | 0,5–2 (multiplica a aresta) |

## 6. Quando usar uma GNN treinada

Raramente, para um especialista de perguntas e respostas. Faz sentido quando há **muitos rótulos por vértice** e uma tarefa de previsão: recomendar produto, prever domínio de um conceito a partir do desempenho nos vizinhos (knowledge tracing com grafos), detectar fraude. Nesse caso use PyTorch Geometric (GraphSAGE para grafos grandes, GAT quando alguns vizinhos importam mais), 2–3 camadas, e calcule os vetores em lote, não por consulta.

## 7. A ponte com o Transformer

A atenção é troca de mensagens num grafo completo de tokens. Isso ajuda a explicar ao usuário por que fornecer as **relações** do grafo no prompt funciona: o modelo já é, por dentro, uma máquina de juntar mensagens entre vértices.
