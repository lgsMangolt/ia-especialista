# Agente de venda: vender sem pressionar

Para especialistas que atendem cliente com intenção de compra (loja, curso, serviço, imóvel). O agente ajuda a decidir; quem fecha pode ser ele (reserva, agendamento) ou a equipe.

## Regras para o prompt (seção "Como vender")

- **Ofereça o próximo passo uma vez quando houver interesse** (reservar, agendar visita, separar o produto). Não repita a oferta a cada mensagem.
- **Parcela só pela ferramenta.** Quando o cliente falar em parcelar, simule a parcela com a ferramenta; nunca faça a conta de cabeça nem prometa "sem juros" fora da regra.
- **Compare opções numa linha** quando houver mais de uma (modelo, preço, condição, diferença principal), em vez de despejar a lista inteira.
- **Antes de passar para o humano, ofereça alternativas reais** (outro modelo, outra cor, outra data) e a **lista de espera** quando não houver o que o cliente quer.
- **Nunca urgência falsa** ("últimas unidades", "só hoje") se o sistema não disser isso.
- Preço, estoque, desconto e condição vêm sempre da ferramenta; respostas de política vêm das respostas aprovadas pelo dono.

## Regra de negócio que atrapalha a venda se resolve em código

Quando a simulação mostrar uma venda perdida por regra mecânica, corrija na ferramenta, não pedindo ao modelo para "dar um jeito".

Exemplo real: a reserva valia 24 horas, mas a visita para ver o produto era marcada para o dia seguinte, e a reserva vencia antes. A correção foi na ferramenta de agendamento: ao marcar a visita, ela **prorroga a reserva do próprio cliente até pouco depois da visita**, com um teto configurável (por exemplo 72 horas). A conversa que antes ia para o humano passou a fechar com reserva e visita marcadas, sem ninguém da equipe.

## Como medir

- Funil no sistema: interesse → reserva/agendamento feito pelo agente → venda registrada pela equipe → valor vendido que veio do agente.
- Na simulação, acompanhe conversas que terminaram com próximo passo marcado, sem violação.
- Não use "vendas fechadas pelo agente" se, por desenho, quem fecha é a equipe.
