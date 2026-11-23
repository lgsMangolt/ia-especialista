# Esforço na hora de responder e ciclo com verificador

Duas linhas de pesquisa recentes (2025–2026) mudam como montar um especialista. As duas reforçam a regra central da skill: **o modelo propõe, algo exato confere.**

## 1. Gastar mais esforço só onde precisa (test-time compute adaptativo)

Em vez de um modelo maior, deixar o modelo "pensar mais" na hora de responder, e só nas perguntas difíceis.

- Distribuir o esforço por pergunta, e não igual para todas, rendeu mais de 4× de eficiência em matemática, e um modelo menor pensando mais chegou a superar um 14× maior (ICLR 2025, *Scaling LLM Test-Time Compute Optimally*).
- Trabalhos de 2026 usam um **verificador para decidir onde gastar**: alocação adaptativa guiada por verificador superou a alocação uniforme (arXiv 2602.01070); busca por "pensamentos" tratada como problema de distribuir esforço (Gambit, COLM 2026, arXiv 2608.08020).
- Custo: o preço por token caiu muito, mas raciocínio gasta bem mais tokens por pergunta. Meça custo e latência junto com o acerto.

**Como aplicar no especialista:**

| Situação | O que fazer |
|---|---|
| Pergunta simples (consulta, preço, horário) | resposta direta, sem raciocínio longo; o verificador confere |
| Pergunta difícil (cruza fatos, conta em várias etapas) | ligar o modo de raciocínio ou gerar 2–4 respostas e deixar o verificador escolher a que passa |
| Como saber se é difícil | um roteador simples: tipo de pergunta, número de fatos envolvidos, ou a primeira resposta reprovou no verificador |
| Latência apertada | esforço extra só depois de uma reprovação, nunca por padrão |

Trate "pensar mais" como **uma configuração a medir** no conjunto `dev`, com o mesmo modo fixo em todas as comparações. Não ligue por padrão sem medir: muitas vezes só aumenta custo e tempo.

## 2. Ciclo gerar → verificar → corrigir

Na matemática formal, os melhores resultados de 2026 vêm de um modelo comum num ciclo com um verificador exato (o Lean), que devolve o erro para o modelo tentar de novo. Exemplos: LEAP, que segundo os autores resolveu os 12 problemas do Putnam 2025 (arXiv 2606.03303); AlphaProof Nexus, da DeepMind, aplicado a problemas em aberto (arXiv 2605.22763); e uma comparação que concluiu que o ciclo de feedback com o verificador é o que mais pesa (arXiv 2606.05632).

O mesmo padrão vale fora da matemática, sempre que existir um verificador exato:

| Domínio | Verificador |
|---|---|
| Contas e álgebra | SymPy ou cálculo em código |
| Preço, prazo, estoque | tabela consultada e comparação de números |
| Citação de documento | o item existe e está vigente |
| Código e SQL | testes ou execução |
| Formato | esquema JSON |
| Provas matemáticas | Lean |

**Como aplicar:**
1. O modelo responde.
2. O verificador confere e, se reprovar, diz **o motivo concreto** ("o preço R$60 não está na tabela para porte pequeno").
3. O modelo recebe o motivo e tenta de novo, até 2–3 vezes.
4. Se continuar reprovando, a resposta vai para humano ou vira recusa. Nunca envie uma resposta reprovada.

**Meia verdade também reprova.** Em atendimento, o verificador barra frases de suposição sobre política ou fato ("geralmente", "provavelmente", "pelo que sei", "deve ser") e, em vez de pedir para o modelo reescrever, passa direto para o humano. Reescrever costuma trocar uma suposição por outra; o humano responde certo.

Registre quantas tentativas cada pergunta precisou: muitas tentativas no mesmo tipo de pergunta apontam onde mexer no ciclo de melhoria (fato faltando, regra mal explicada no prompt).

## 3. Calcular direto nos pesos

O Weight-Space Programming (MIT CSAIL, novembro de 2026) está em `edicao-de-pesos.md`: experimental, sem revisão por pares, só para defeitos de comportamento.

## Confiança

Os números de LEAP e AlphaProof Nexus são dos próprios autores e não foram verificados por terceiros. Alguns identificadores e datas do arXiv encontrados na busca pareceram incomuns: confira o original antes de citar a um usuário.

Fontes:
- ICLR 2025 — Scaling LLM Test-Time Compute Optimally: https://iclr.cc/virtual/2025/oral/31924
- Alocação adaptativa (arXiv 2602.01070): https://arxiv.org/html/2602.01070v1
- Gambit, COLM 2026 (arXiv 2608.08020): https://arxiv.org/pdf/2608.08020
- Survey de inferência eficiente (arXiv 2503.23077): https://arxiv.org/pdf/2503.23077
- LEAP (arXiv 2606.03303): https://arxiv.org/abs/2606.03303
- AlphaProof Nexus (arXiv 2605.22763): https://arxiv.org/pdf/2605.22763v1
- Avaliação de LLMs em Lean (arXiv 2606.05632): https://arxiv.org/pdf/2606.05632
- From Solvers to Research (arXiv 2607.07779): https://arxiv.org/pdf/2607.07779
