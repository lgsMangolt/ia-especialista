# ia-especialista

Skill para o [Claude Code](https://claude.com/claude-code) que ajuda a **montar e melhorar uma IA especialista** num assunto estreito — um atendente de loja, um corretor de exercícios, um assistente de prazos, um bot de suporte — de um jeito barato, por API ou rodando no seu computador.

Gratuita e de código aberto (licença MIT).

## O que ela faz

- **Começa por uma entrevista** ajustada ao seu nível: iniciante recebe perguntas simples sobre o negócio (sempre com um pequeno resultado junto); avançado recebe poucas perguntas, diretas, com números.
- **O código decide, a IA explica.** Preço, data, prazo, conta e permissão saem de tabela, cálculo ou banco; um verificador confere a resposta antes de enviar.
- **Mede antes de mexer.** Perguntas de teste com 30% guardadas para o teste final, incluindo **casos de ataque** (injeção indireta, autoridade falsa, abuso de ferramentas, extração de dados). Meta: zero brecha de segurança antes de entregar.
- **Segurança é permissão em código**, não instrução no prompt: ferramentas mínimas, limites nas ações, limpeza da entrada, bateria de testes sem modelo validada por teste de mutação.
- **Simulação de clientes** com personas e um juiz, regressão pareada a cada mudança.
- Só acrescenta **grafo de conhecimento, LoRA, treino por reforço ou edição de pesos** quando a medição mostra que precisa.

## Instalar

Copie a pasta para o diretório de skills do Claude Code:

```bash
git clone https://github.com/lgsMangolt/ia-especialista.git
cp -r ia-especialista ~/.claude/skills/ia-especialista
```

No Windows (PowerShell):

```powershell
git clone https://github.com/lgsMangolt/ia-especialista.git
Copy-Item -Recurse ia-especialista "$env:USERPROFILE\.claude\skills\ia-especialista"
```

Depois, no Claude Code, chame com `/ia-especialista` no começo do pedido.

**Dica:** com muitas skills instaladas, o Claude pode responder perguntas de conselho sem consultar a skill. Para ela ser usada sozinha, acrescente ao seu `~/.claude/CLAUDE.md`:

> Quando o pedido for para planejar, montar, treinar, ajustar, avaliar ou melhorar um agente, chatbot, atendente ou IA especialista num domínio, carregue a skill `ia-especialista` antes de responder.

## O que tem dentro

| Pasta | Conteúdo |
|---|---|
| `SKILL.md` | o método: peças, trilhas, entrevista, fases, arquitetura |
| `references/` | entrevista, protocolo de avaliação, segurança e red team, simulação de clientes, venda sem pressionar, ciclo de melhoria, grafo e PageRank, LoRA e busca de hiperparâmetros, treino avançado (RLVR/GRPO, destilação), esforço e verificação, edição de pesos |
| `assets/` | modelos para copiar: planilha de fatos, perguntas de teste, verificador de preços, script de avaliação, tabela de cobertura |
| `scripts/` | `ppr.py` (PageRank personalizado e bloco de evidências), `lora_size.py` (tamanho de um LoRA), `teste_acionamento.py` (mede se a skill é acionada nos pedidos certos) |
| `evals/` | casos de teste da própria skill, no formato do `claude plugin eval` |

Os scripts usam só a biblioteca padrão do Python.

## Limites

- Os números citados na skill (custos, tamanhos, resultados de simulação) são estimativas ou resultados de testes simulados, não garantias.
- Partes marcadas como experimentais (edição de pesos, por exemplo) vêm de trabalhos ainda sem revisão por pares.

## Licença

[MIT](LICENSE)
