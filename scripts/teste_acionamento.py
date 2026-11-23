"""Mede se a skill é acionada pelos pedidos certos, rodando `claude -p` de verdade.

Funciona no Windows (não usa select em pipes). Testa a skill como ela está instalada,
competindo com todas as outras skills do usuário.

Uso:
  python teste_acionamento.py pedidos.json --execucoes 3 --paralelo 4 --saida resultado.json
  python teste_acionamento.py pedidos.json --so 2          # só os 2 primeiros (teste rápido)

pedidos.json: [{"query": "...", "should_trigger": true}, ...]
Conta como acionada quando o Claude chama a ferramenta Skill com esta skill, ou lê o SKILL.md dela,
antes de usar qualquer outra ferramenta de trabalho. Gasta uso da conta: cada execução é uma chamada.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

SKILL = "ia-especialista"
META = {"Skill", "ToolSearch"}  # ferramentas que não encerram a observação


def rodar(query, timeout, cwd, modelo):
    cmd = [shutil.which("claude") or "claude", "-p", query, "--output-format", "stream-json", "--verbose",
           "--include-partial-messages", "--max-turns", "4"]
    if modelo:
        cmd += ["--model", modelo]
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=cwd, env=env)
    timer = threading.Timer(timeout, p.kill)
    timer.start()
    skills_chamadas, atual, acc = [], None, ""
    acionou, motivo = False, "fim sem ferramenta"
    try:
        for raw in p.stdout:
            try:
                ev = json.loads(raw.decode("utf-8", "replace"))
            except json.JSONDecodeError:
                continue
            if ev.get("type") != "stream_event":
                if ev.get("type") == "result":
                    break
                continue
            se = ev.get("event", {})
            t = se.get("type")
            if t == "content_block_start" and se.get("content_block", {}).get("type") == "tool_use":
                atual, acc = se["content_block"].get("name", ""), ""
            elif t == "content_block_delta" and atual and se.get("delta", {}).get("type") == "input_json_delta":
                acc += se["delta"].get("partial_json", "")
            elif t == "content_block_stop" and atual:
                if atual == "Skill":
                    skills_chamadas.append(acc)
                    if SKILL in acc:
                        acionou, motivo = True, "Skill"
                        break
                elif atual == "Read" and SKILL in acc and "SKILL.md" in acc:
                    acionou, motivo = True, "Read SKILL.md"
                    break
                elif atual not in META:
                    motivo = f"usou {atual} antes"
                    break
                atual = None
    finally:
        timer.cancel()
        if p.poll() is None:
            p.kill()
        p.wait()
    outras = [s for s in skills_chamadas if SKILL not in s]
    return acionou, motivo, outras


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("pedidos")
    ap.add_argument("--execucoes", type=int, default=3)
    ap.add_argument("--paralelo", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--modelo")
    ap.add_argument("--cwd", default=os.getcwd(), help="pasta neutra onde rodar o claude")
    ap.add_argument("--so", type=int, help="usar só os N primeiros pedidos")
    ap.add_argument("--saida")
    a = ap.parse_args()
    pedidos = json.load(open(a.pedidos, encoding="utf-8"))
    if a.so:
        pedidos = pedidos[: a.so]
    tarefas = [(i, r) for i in range(len(pedidos)) for r in range(a.execucoes)]
    res = {i: [] for i in range(len(pedidos))}
    with ThreadPoolExecutor(a.paralelo) as ex:
        futs = {ex.submit(rodar, pedidos[i]["query"], a.timeout, a.cwd, a.modelo): i for i, _ in tarefas}
        for f, i in futs.items():
            try:
                res[i].append(f.result())
            except Exception as e:  # registra e segue
                res[i].append((False, f"erro: {e}", []))
    linhas, certos = [], 0
    for i, q in enumerate(pedidos):
        n = sum(1 for ok, _, _ in res[i] if ok)
        taxa = n / len(res[i])
        acerto = (taxa >= 0.5) == q["should_trigger"]
        certos += acerto
        linhas.append({"query": q["query"], "should_trigger": q["should_trigger"], "acionou": n,
                       "execucoes": len(res[i]), "acerto": acerto,
                       "motivos": [m for _, m, _ in res[i]], "outras_skills": [o for _, _, o in res[i] if o]})
        print(f"[{'OK ' if acerto else 'ERR'}] {n}/{len(res[i])} esperado={'sim' if q['should_trigger'] else 'não'}  {q['query'][:70]}")
    pos = [l for l in linhas if l["should_trigger"]]
    neg = [l for l in linhas if not l["should_trigger"]]
    resumo = {"acertos": certos, "total": len(linhas),
              "acionou_quando_devia": sum(l["acerto"] for l in pos), "devia": len(pos),
              "ficou_fora_quando_devia": sum(l["acerto"] for l in neg), "nao_devia": len(neg)}
    print(json.dumps(resumo, ensure_ascii=False))
    if a.saida:
        json.dump({"resumo": resumo, "pedidos": linhas}, open(a.saida, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
