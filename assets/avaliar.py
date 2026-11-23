"""Roda as perguntas de teste e mostra o acerto. Ponto de partida: troque responder() pela
chamada real do seu especialista (API, Ollama, etc.).

Uso:
    python avaliar.py perguntas-teste-modelo.jsonl
    python avaliar.py dev.jsonl --saida resultado.json

Cada linha do JSONL: id, pergunta, resposta_esperada, numeros_esperados, como_verificar, deve_recusar.
como_verificar: "numero" (todos os numeros_esperados aparecem), "contem:<texto>", ou "recusa".
"""
import argparse
import json
import re
import sys
import time

PALAVRAS_RECUSA = ("veterinário", "não posso", "nao posso", "vou passar", "um atendente", "não consigo responder")


def responder(pergunta):
    """TROQUE ISTO pela chamada do seu especialista. Aqui só devolve um texto fixo."""
    return "Ainda não conectado ao especialista."


def numeros(texto):
    return {float(n.replace(".", "").replace(",", ".")) for n in re.findall(r"\d+(?:[.,]\d+)?", texto)}


def corrigir(caso, resposta):
    regra = caso.get("como_verificar", "numero")
    low = resposta.lower()
    if caso.get("deve_recusar") or regra == "recusa":
        return any(p in low for p in PALAVRAS_RECUSA)
    if regra.startswith("contem:"):
        return regra.split(":", 1)[1].strip().lower() in low
    esperados = {float(x) for x in caso.get("numeros_esperados", [])}
    return bool(esperados) and esperados <= numeros(resposta)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("perguntas")
    ap.add_argument("--saida")
    a = ap.parse_args()
    casos = [json.loads(l) for l in open(a.perguntas, encoding="utf-8") if l.strip()]
    resultados, certos = [], 0
    for c in casos:
        t0 = time.time()
        r = responder(c["pergunta"])
        ok = corrigir(c, r)
        certos += ok
        resultados.append({"id": c["id"], "ok": ok, "resposta": r, "segundos": round(time.time() - t0, 2)})
        print(f"[{'OK ' if ok else 'ERR'}] {c['id']}  {c['pergunta'][:60]}")
    print(f"\nAcerto: {certos}/{len(casos)} ({100 * certos / max(1, len(casos)):.0f}%)")
    if len(casos) < 55:
        print("Aviso: com menos de ~55 perguntas, só diferenças grandes (~15 pontos) entre versões são confiáveis.")
    if a.saida:
        json.dump({"acerto": certos, "total": len(casos), "casos": resultados}, open(a.saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
