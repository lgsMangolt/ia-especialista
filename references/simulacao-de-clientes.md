# Simulação de clientes com personas e juiz

Antes de ter clientes reais, e depois para cada mudança, meça o especialista com conversas simuladas. Isso complementa as perguntas de teste da Fase 0: as perguntas medem resposta certa; a simulação mede a conversa inteira (pergunta de volta, uso de ferramenta, passagem para humano, tom).

## Montagem

| Peça | Como |
|---|---|
| **Perfis (personas)** | 20 a 100 perfis por categoria (preço, estoque, desconto, reclamação, situação difícil, fora do assunto, ataque). Cada perfil tem a **primeira mensagem fixa** e o objetivo do cliente, para a rodada ser repetível e comparável. |
| **Cliente simulado** | um modelo barato que continua a conversa conforme o perfil, por 2–4 trocas |
| **Agente** | o agente de verdade, com as mesmas ferramentas e o **mesmo verificador de produção** |
| **Juiz** | outro modelo (de preferência mais forte que o cliente) que lê a conversa e marca nota, violações (com gravidade) e como terminou (resolvido, passou para humano) |
| **Loja/sistema de teste** | uma instância separada da de produção, com dados de teste |

## Rodar

- Rode em paralelo com um teto de gasto. Registre **o custo do agente separado do custo do teste**: o primeiro é o que o cliente vai pagar (num atendimento de varejo, ~US$ 0,03 por conversa); o segundo é custo de medir (cliente simulado e juiz, ~US$ 0,02–0,03 por conversa).
- Ordem de grandeza: 100 conversas ≈ US$ 4–5 no total; 20 ataques ≈ US$ 1.
- Para iterar rápido, rode **só as conversas que falharam + um grupo de controle** que passava, para ver se a correção não quebrou o que funcionava.
- **Depois de toda mudança de prompt, rode regressão nos perfis normais**, não só nos de ataque. Compare **pareado**, perfil a perfil, com a versão anterior.
- **No fim, limpe os dados de teste do sistema** (reservas, cadastros, tarefas criadas pelas conversas simuladas). Deixe isso num comando (por exemplo `limpar-testes`).

## Como ler os números

- **"Conversa limpa"** = sem violação marcada pelo juiz. É o número principal de qualidade.
- **Passagem para humano não é fracasso nem conversão.** Em perfis de "situação difícil" (reclamação, desconto, pedido fora da regra), passar para o humano é o comportamento certo. Aumentar a passagem pode ser o agente ficando mais seguro; diminuir pode ser ele inventando. Leia junto com as violações.
- **A maior causa de passagem para humano costuma ser pergunta de política sem resposta aprovada** (entrega, desconto à vista, garantia, nota fiscal, horário). Liste as que mais aparecem e leve ao dono como "respostas aprovadas" (ver a entrevista).
- **Resultado de negócio pode ser zero por desenho.** Se o agente reserva e a loja vende, "vendas fechadas pelo robô" é zero sempre. Meça o **funil real no sistema** (CRM): reservas feitas pelo agente, quantas viraram venda, valor vendido que veio do agente.
- **Juiz é sinal, não prova.** Confira à mão uma amostra das conversas marcadas como limpas e das marcadas com violação.
- Uma rodada com 20 perfis só enxerga diferenças grandes; não conclua por 1 ou 2 conversas.
