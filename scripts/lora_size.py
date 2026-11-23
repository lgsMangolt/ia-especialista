"""Estimativa do tamanho de um adaptador LoRA.

Uso:
  python lora_size.py --d 4096 --k 4096 --r 8
  python lora_size.py --d 2560 --k 2560 --r 16 --matrizes 7 --camadas 36

Supõe que todas as matrizes têm formato d×k (aproximação). Para o número exato,
some r*(d+k) de cada matriz usando as dimensões do config.json do modelo.
"""
import argparse
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

ap = argparse.ArgumentParser()
ap.add_argument("--d", type=int, required=True, help="dimensão de saída da matriz")
ap.add_argument("--k", type=int, required=True, help="dimensão de entrada da matriz")
ap.add_argument("--r", type=int, required=True, help="rank do LoRA")
ap.add_argument("--matrizes", type=int, default=1, help="matrizes com LoRA por camada")
ap.add_argument("--camadas", type=int, default=1)
ap.add_argument("--bytes", type=float, default=2.0, help="bytes por parâmetro (fp16/bf16 = 2)")
a = ap.parse_args()

n = a.matrizes * a.camadas
completo = a.d * a.k * n
lora = a.r * (a.d + a.k) * n
mb = lambda x: x * a.bytes / 1024**2
print(f"matrizes cobertas: {n}")
print(f"ajuste completo:   {completo:,} parâmetros  ({mb(completo):,.1f} MB)")
print(f"LoRA:              {lora:,} parâmetros  ({mb(lora):,.2f} MB)")
print(f"fração:            {100 * lora / completo:.3f}%")
if a.r >= min(a.d, a.k):
    print("aviso: r >= min(d, k) não economiza nada")
