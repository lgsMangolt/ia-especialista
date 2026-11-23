# Entrevista para verticalizar o especialista

O objetivo é sair da conversa com uma **ficha do especialista**: o recorte, os fatos, o que o código decide, os riscos e como medir. Com ela, cada fase já nasce desenhada para aquele negócio, e não para um caso genérico.

## Como conduzir

- **Uma pergunta por vez** (para avançados, pode agrupar), curta, com um exemplo do que você espera ouvir. Quando a ferramenta de perguntas com opções estiver disponível, use-a com 2–4 opções prováveis; a pessoa sempre pode escrever outra.
- **Pule o que já foi respondido** no pedido, no código do projeto ou em conversas anteriores. Releia antes de perguntar.
- **Proponha em vez de perguntar no vazio.** "Pelo que você contou, eu começaria só por troca e cancelamento. Serve?" é melhor que "Qual o escopo?".
- **Pare quando der para decidir.** Os blocos 1–4 são obrigatórios; os outros só se a resposta mudar o desenho. O número de perguntas depende do nível da pessoa (bloco 0): 7–10 para iniciante, 5–7 para intermediário, 3–5 para avançado.
- **Sem resposta, assuma e registre.** Se a pessoa não puder responder agora (ou for um teste automático), escreva a suposição na ficha e siga. Suposição marcada é melhor que travar.
- **Dê o primeiro resultado visível logo depois da entrevista**, na mesma sessão.

## Perguntas, em ordem

### 0. Nível da pessoa no assunto (primeiro)

Descubra quanto a pessoa entende de IA e de programação. Isso decide quantas perguntas fazer, que palavras usar e quanto você decide por ela.

- **Infira antes de perguntar.** Se o pedido já mostra o nível ("tenho 2 A100 e uso PEFT", "nunca programei"), não pergunte; diga em uma linha como vai conduzir e siga.
- Se não der para inferir, pergunte com opções:
  - **Iniciante:** usa ChatGPT, não programa ou programa pouco.
  - **Intermediário:** programa e já chamou uma API de IA ou rodou um modelo local.
  - **Avançado:** já treinou ou ajustou modelos, conhece RAG, LoRA e avaliação.

Quem é iniciante não sabe o que especificar, então precisa de **mais perguntas, todas pequenas e sobre o próprio negócio**, para o resultado chegar perto do que quer. Quem é avançado costuma chegar com o pedido já detalhado, então precisa de **poucas perguntas, diretas, só sobre o que falta**.

| Nível | Quantas perguntas | Como conduzir |
|---|---|---|
| Iniciante | 7–10, uma por vez | além dos blocos obrigatórios, pergunte sempre **quem vai cuidar do sistema** (iniciante quase sempre depende de alguém: filho, funcionário, a agência) e **quanto dá para gastar por mês**; só sobre o negócio, nunca sobre técnica; cada pergunta fácil de responder, com exemplo ou opções ("seus clientes perguntam mais de preço, horário ou planos?"); peça exemplos reais de pergunta e de resposta ideal; sem jargão (diga "tabela que o sistema consulta", não "RAG"); as decisões técnicas você toma e explica numa frase; **cada mensagem traz um pequeno resultado junto com a pergunta** (exemplo de resposta com os dados que ele já deu, preço calculado, planilha modelo preenchida) — pergunta sem entrega cansa e faz desistir |
| Intermediário | 5–7 | obrigatórios + restrições e como medir; termos técnicos com uma frase de explicação na primeira vez; ofereça 2 opções nas decisões de arquitetura |
| Avançado | 3–5, podendo agrupar várias numa mensagem | pule tudo que o pedido já trouxe; pergunte só o que falta, inclusive detalhes técnicos abaixo; jargão liberado; mostre números e trade-offs e deixe a pessoa decidir; **na primeira resposta já proponha o conjunto de teste e os casos difíceis previsíveis** (acento, formato de número e preço, versões de documento, perguntas que cruzam fontes) |

Em qualquer nível, se a pessoa pedir resposta curta, responda curto (até ~120 palavras).

**Perguntas técnicas para o nível avançado** (só as que faltarem e mudarem o desenho):
- Qual base já usam ou preferem, e em que precisão vão servir (BF16, FP8, 4 bits)?
- Existe infraestrutura de avaliação? Que diferença de acerto precisam detectar (define o tamanho do teste)?
- O modo de raciocínio do modelo vai ligado ou desligado em produção?
- Há documentos com várias versões (exige partição por grupo e controle de vigência)?

O nível também muda a entrega: para iniciantes, um passo por vez e um resultado visível rápido; para avançados, o protocolo completo de `protocolo-avaliacao.md`.

### 1. Recorte (obrigatório)
- O que o especialista precisa responder ou fazer? Peça **3 a 5 perguntas reais** que ele deve atender e **uma que deve recusar**.
- Se o recorte for amplo ("especialista em Direito", "atende tudo da loja"), proponha 2–3 recortes estreitos e peça para escolher um para começar.

### 2. Quem usa e por onde (obrigatório)
- Quem pergunta (cliente, aluno, equipe interna) e por qual canal (WhatsApp, site, app, sistema interno, terminal)?
- **Sempre pergunte, não decida sozinho:** o especialista responde sozinho ou começa como rascunho que alguém aprova antes de enviar? Ofereça as opções com a sua recomendação (por exemplo: "1. responde sozinha, mais rápido, mas se errar o cliente já recebe o erro; 2. você aprova antes, mais seguro nas primeiras semanas — recomendo a 2"). Se a resposta variar por assunto (informação sai sozinha, agendamento fica para confirmar), diga isso como proposta e peça confirmação. É a pessoa que vai arcar com o erro, então a escolha é dela.
- **Integrações e aprovações, logo aqui:** o que já usam e onde o especialista precisa encaixar (WhatsApp oficial ou não oficial, sistema de pedidos, agenda, ERP, planilha)? Dá para ligar nisso (há API, exportação, alguém com acesso)? Quem precisa aprovar (TI, jurídico, dono)? Descobrir isso no meio do caminho foi a queixa mais comum de intermediários.

### 3. Fatos e de onde vêm (obrigatório)
- Onde estão as informações certas hoje (planilha, PDF, sistema, cabeça de alguém)?
- Com que frequência mudam e quem atualiza? Isso define a vigência e quem mantém a tabela.
- O que **pode ser calculado ou consultado** (preço, data, prazo, conta, estoque)? Isso vira verificador em código, não tarefa do modelo.
- **Respostas aprovadas pelo dono** para as perguntas de política (entrega, frete, desconto à vista, fotos, nota fiscal, conferir antes de pagar, horário e como chegar, cobertura da garantia, outros serviços). Sem resposta aprovada, o agente passa para o humano, e essa é a maior causa de passagem. Não peça todas de uma vez: comece pelas que mais aparecem nas simulações e deixe o resto vazio (vazio = humano). O agente nunca inventa política.
- **Que ações o agente vai poder fazer** (só responder, reservar, agendar, cadastrar)? Cada ação vira uma ferramenta com limite em código; o que não estiver na lista ele não faz.

### 4. Risco do erro (obrigatório)
- O que acontece se ele errar? (perde venda, cliente reclama, prazo perdido, nota errada para o aluno)
- Em que casos deve passar para um humano ou recusar?
- Quanto mais caro o erro, mais o desenho pende para tabela de cobertura com recusa, rascunho aprovado e conferência humana.

### 4b. Quem monta e quanto custa no total (obrigatório)
- Quem vai montar e quem vai manter? (a própria pessoa, alguém da equipe, um filho, um freelancer, uma agência)
- Dê o **custo total em faixa**, separando uso mensal (API, servidor, WhatsApp) e montagem (horas de alguém técnico). Diga que é estimativa.
- **Se não houver ninguém técnico**, ofereça logo um caminho pronto: uma ferramenta sem código que resolva o recorte, ou um prestador/agência, com a lista do que pedir a ele. A ficha do especialista serve de briefing para essa pessoa.

### 5. Restrições
- Os dados podem sair da empresa (API) ou precisam ficar no computador?
- Que máquina existe (GPU e memória, só CPU, servidor) e qual orçamento mensal?
- Qual o prazo para ter algo funcionando?

### 6. Como medir
- Como saber se uma resposta está certa? (número que bate, artigo citado, linha do erro, aprovação de um atendente)
- Quem pode conferir respostas e quantas horas por semana?
- Existe histórico real (tickets, conversas, provas) para virar perguntas de teste? Tem dado pessoal que precisa ser anonimizado?

### 7. Forma da resposta
- Tom e formato: curto ou explicado, campos fixos (modelo, preço, parcelamento), citação de fonte, idioma.
- Mostre um exemplo e pergunte se é isso.

### 8. Quem mantém
- Quem cuida do especialista depois de pronto e quanto tempo tem para isso?

## Como cada resposta muda o desenho

| Se a resposta for… | Então… |
|---|---|
| Dados podem sair, prazo curto | trilha rápida (API) |
| Dados não podem sair, ou volume alto | trilha local, modelo pequeno em 4 bits |
| Tem coisa calculável | verificador em código decide; o modelo só explica |
| Fatos mudam com frequência | tabela ou documento com vigência e responsável |
| Erro caro | tabela de cobertura com recusa, rascunho aprovado, conferência humana |
| Muitas perguntas ligam vários fatos | medir a fatia multi-salto; grafo só se passar de ~20% |
| Formato ou tom errados depois de tudo | LoRA, com exemplos no formato real |
| Pouca gente para conferir | conjunto de teste menor, avisando qual diferença ele detecta |

## Ficha do especialista

Ao terminar, salve no projeto (por exemplo `docs/especialista.md`) e mostre ao usuário para confirmar:

```markdown
# Ficha do especialista: <nome curto>

- Nível de quem vai construir: <iniciante | intermediário | avançado> (<inferido ou respondido>)
- Recorte: <o que faz> | Fora do escopo: <o que recusa ou encaminha>
- Usuários e canal: <quem> via <canal>; modo inicial: <sozinho | rascunho aprovado>
- Fatos: <fonte> — muda <frequência>, mantido por <pessoa>; vigência: <como>
- Verificador em código: <o que é calculado ou consultado>
- Risco do erro: <consequência>; passa para humano quando <regra>
- Trilha: <rápida (API) | local (modelo, máquina)>; orçamento <valor>; prazo <data>
- Quem monta: <pessoa | prestador | ferramenta pronta>; quem mantém: <pessoa>; custo total estimado: uso <R$/mês> + montagem <R$ ou horas>
- Integrações: <o que já usam e como o especialista se liga>; aprovações: <quem>
- Ferramentas e permissões: <cada ação, com o limite em código>; o que o agente NÃO pode: <...>
- Respostas aprovadas: <as já preenchidas>; pendentes (vão para o humano): <as que mais aparecem primeiro>
- Acerto é: <critério>; quem confere: <pessoa, horas/semana>
- Forma: <tom, campos, fonte>
- Perguntas de teste: <origem>, meta de <n>, 30% guardados; detecta diferenças de ~<x> pontos
- Suposições ainda não confirmadas: <lista>
- Primeiro resultado visível: <o que será mostrado nesta sessão>
```
