# Treino avançado: reforço com verificador (RLVR/GRPO) e destilação on-policy

Os dois métodos de pós-treino que mais avançaram em 2026. Entram **depois** da linha de base e do LoRA, e só quando a medição mostra que o modelo ainda erra algo que um verificador consegue julgar.

## Quando usar cada um

| Situação | Método |
|---|---|
| Existe verificador automático (conta, preço, citação vigente, teste de código, formato) e o modelo ainda erra mesmo com o ciclo gerar→verificar→corrigir | **RLVR com GRPO** |
| Um modelo grande (API) acerta e o pequeno local não, e você precisa que o pequeno rode sozinho (sigilo, custo, offline) | **Destilação on-policy** |
| O erro é de forma (tom, formato) | LoRA comum (Fase 3), não estes |
| O erro é de fato que muda (preço, política) | fonte consultada, nunca treino |
| Não há verificador nem professor confiável | não use; volte à entrevista e defina como medir |

## 1. RLVR com GRPO

**Como funciona:** para cada pergunta, o modelo gera várias respostas (um grupo de 4 a 16). O **verificador dá a nota** de cada uma (1 se passa, 0 se não; ou parcial). O GRPO compara cada resposta com a média do grupo e reforça as melhores. Não precisa de um modelo "crítico" separado, por isso gasta bem menos memória que o PPO.

**Por que encaixa na skill:** o verificador que você já montou (SymPy, tabela, vigência, esquema) vira a função de recompensa. Nada novo para medir.

**Receita inicial (ajuste pelos números):**
- Base: o mesmo modelo pequeno da trilha local, com o LoRA já treinado (ou LoRA novo por cima). Em 12 GB, comece por 1,7–4B em 4 bits com LoRA; ferramentas como TRL (`GRPOTrainer`) e Unsloth suportam isso.
- Perguntas de treino: **só do conjunto de treino**, nunca do `dev` nem do `holdout`. Gere variações a partir das tabelas e regras (por exemplo, 3–4 por regra).
- Recompensa: o verificador, mais um pequeno bônus de formato. Evite recompensas de juiz LLM quando houver verificador exato.
- Grupo de 4–8 respostas por pergunta, poucas centenas de passos, e avaliação no `dev` a cada checkpoint.

**Cuidados:**
- **Enganar a recompensa (reward hacking):** o modelo pode achar atalhos que passam no verificador sem acertar de verdade (por exemplo, repetir um número da pergunta). Leia uma amostra das respostas a cada checkpoint e endureça o verificador quando aparecer um atalho.
- **Esquecer o resto:** rode também perguntas gerais e de recusa; pare se piorarem.
- **Custo:** gerar várias respostas por pergunta é o que mais pesa. Comece pequeno e só aumente com ganho medido.
- Adote só se vencer a versão anterior no `dev`, pela regra do protocolo de avaliação, e confirme no `holdout` uma vez no fim.

## 2. Destilação on-policy

**Como funciona:** o modelo **aluno** (pequeno, local) gera a resposta, e o **professor** (grande) dá nota a cada palavra, mostrando onde o aluno se desviou. O sinal é muito mais rico que a nota única do RLVR. A divisão de trabalho que está se formando: o RLVR cria especialistas e a destilação junta vários num modelo só.

**Quando faz sentido aqui:**
- O professor via API acerta o domínio (meça no `dev`) e o aluno local fica bem abaixo.
- Os dados de treino podem ir para a API do professor (confira com o usuário; em casos de sigilo, não podem).
- Os termos de uso do fornecedor permitem treinar outro modelo com as saídas dele. **Confira antes**: vários proíbem.

**Receita inicial:**
- Perguntas do conjunto de treino, com as evidências e resultados das ferramentas no prompt, iguais às de produção.
- Aluno gera, professor avalia; treine o aluno com LoRA por cima.
- Compare três versões no `dev`: aluno antes, aluno depois e professor. O objetivo é chegar perto do professor gastando bem menos.

## O que fica de fora

Muon no lugar do AdamW, treino em FP4/FP8 e as novas técnicas de mistura de especialistas (MoE) são do **pré-treino** de modelos grandes, com milhares de GPUs. Não se aplicam a montar um especialista sobre um modelo pronto.

## Confiança e fontes

Os resultados de 2026 vêm em boa parte de preprints e blogs técnicos; trate números específicos como provisórios.

- Guia de pós-treino (Baseten): https://www.baseten.co/articles/a-guide-to-llm-post-training/
- Post-Training in 2026 — GRPO, DAPO, RLVR: https://llm-stats.com/blog/research/post-training-techniques-2026
- Eficiência de rollouts em RL (arXiv 2609.25463): https://arxiv.org/pdf/2609.25463
- Predictable GRPO (arXiv 2606.30789): https://arxiv.org/pdf/2606.30789
- Destilação on-policy (VESSL): https://vessl.ai/en/blog/on-policy-distillation-part-1
- Rubricas como recompensa e risco de reward hacking (PaperGym, arXiv 2608.31119): https://arxiv.org/pdf/2608.31119
- Pré-treino nos laboratórios (Jiaxin Zhang): https://jxzhangjhu.github.io/blog/2026/how-frontier-labs-train-llms/
