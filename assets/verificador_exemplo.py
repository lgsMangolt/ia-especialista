"""Verificador de exemplo: confere se todo número em R$ da resposta existe nos fatos vigentes
(ou é uma soma permitida) antes de enviar. Adapte as regras ao domínio.

Uso como módulo:
    from verificador_exemplo import carregar_fatos, verificar
    fatos = carregar_fatos("planilha-fatos-modelo.csv")
    ok, motivo = verificar("O banho do shih tzu sai R$ 45.", fatos)

Uso direto (teste rápido):
    python verificador_exemplo.py planilha-fatos-modelo.csv "Banho e tosa no labrador: R$ 110"
"""
import csv
import re
import sys
from datetime import date
from itertools import combinations


def carregar_fatos(caminho, hoje=None):
    hoje = (hoje or date.today()).isoformat()
    fatos = []
    with open(caminho, encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            desde = linha.get("vigente_desde") or "0000-00-00"
            ate = linha.get("vigente_ate") or "9999-12-31"
            if desde <= hoje <= ate:
                fatos.append(linha)
    return fatos


def _valores_permitidos(fatos, max_parcelas=2):
    precos = []
    for f in fatos:
        if f.get("unidade") == "R$":
            try:
                precos.append(float(str(f["valor"]).replace(",", ".")))
            except ValueError:
                pass
    permitidos = set(precos)
    for n in range(2, max_parcelas + 1):  # somas simples, ex.: banho + tosa
        for combo in combinations(precos, n):
            permitidos.add(round(sum(combo), 2))
    return permitidos


def verificar(resposta, fatos):
    """Devolve (ok, motivo). Reprova se aparecer valor em R$ que não vem dos fatos."""
    permitidos = _valores_permitidos(fatos)
    achados = re.findall(r"R\$\s*([\d.]+(?:,\d{1,2})?)", resposta)
    for bruto in achados:
        valor = float(bruto.replace(".", "").replace(",", "."))
        if valor not in permitidos:
            return False, f"o valor R$ {bruto} não está na tabela vigente nem é uma soma permitida"
    return True, "ok"


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    if len(sys.argv) < 3:
        sys.exit("uso: python verificador_exemplo.py <fatos.csv> \"<resposta>\"")
    ok, motivo = verificar(sys.argv[2], carregar_fatos(sys.argv[1]))
    print(("APROVADA: " if ok else "REPROVADA: ") + motivo)
