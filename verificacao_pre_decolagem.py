# -*- coding: utf-8 -*-
"""
Missão Aurora Siger - Verificação de pré-decolagem

Lê a telemetria da nave, compara cada leitura com as faixas seguras
definidas para a missão e decide se o lançamento está liberado ou se
deve ser abortado. Ao final, calcula a autonomia energética inicial.

Execução:  python verificacao_pre_decolagem.py
"""

# ---------------------------------------------------------------
# 1. LEITURA DOS DADOS (telemetria simulada)
# ---------------------------------------------------------------
temperatura_interna = 22.5     # °C - cabine
temperatura_externa = -45.0    # °C - apenas registro, não impede o lançamento
integridade_estrutural = 1     # 1 = casco íntegro / 0 = falha detectada
nivel_energia = 85.0           # % da carga das baterias
pressao_tanques = 42.0         # atm
modulos_criticos = "OK"        # OK = navegação, suporte à vida e comunicação operantes

# ---------------------------------------------------------------
# 2. FAIXAS SEGURAS DEFINIDAS PARA A MISSÃO
# ---------------------------------------------------------------
TEMP_INTERNA_MIN = 18.0
TEMP_INTERNA_MAX = 26.0
ENERGIA_MINIMA = 80.0
PRESSAO_MIN = 30.0
PRESSAO_MAX = 50.0

# ---------------------------------------------------------------
# 3. EXECUÇÃO DAS VERIFICAÇÕES
# ---------------------------------------------------------------
print("--- INICIANDO VERIFICAÇÃO DE TELEMETRIA ---")
print()

checagens = [
    ("Temperatura interna",
     TEMP_INTERNA_MIN <= temperatura_interna <= TEMP_INTERNA_MAX,
     f"{temperatura_interna} °C (faixa: {TEMP_INTERNA_MIN} a {TEMP_INTERNA_MAX} °C)"),

    ("Integridade estrutural",
     integridade_estrutural == 1,
     f"{integridade_estrutural} (esperado: 1)"),

    ("Nível de energia",
     nivel_energia > ENERGIA_MINIMA,
     f"{nivel_energia}% (mínimo: acima de {ENERGIA_MINIMA}%)"),

    ("Pressão dos tanques",
     PRESSAO_MIN <= pressao_tanques <= PRESSAO_MAX,
     f"{pressao_tanques} atm (faixa: {PRESSAO_MIN} a {PRESSAO_MAX} atm)"),

    ("Módulos críticos",
     modulos_criticos == "OK",
     f"{modulos_criticos} (esperado: OK)"),
]

for nome, aprovado, leitura in checagens:
    selo = "APROVADO" if aprovado else "REPROVADO"
    print(f"[{selo}] {nome:<24} -> {leitura}")

print(f"[REGISTRO] {'Temperatura externa':<24} -> {temperatura_externa} °C "
      "(informativo, não bloqueia o lançamento)")
print()

# ---------------------------------------------------------------
# 4. DECISÃO FINAL
# ---------------------------------------------------------------
if (18 <= temperatura_interna <= 26) and \
   (integridade_estrutural == 1) and \
   (nivel_energia > 80) and \
   (30 <= pressao_tanques <= 50) and \
   (modulos_criticos == "OK"):

    print("STATUS FINAL: PRONTO PARA DECOLAR")
else:
    print("STATUS FINAL: DECOLAGEM ABORTADA")

# ---------------------------------------------------------------
# 5. ANÁLISE ENERGÉTICA
# ---------------------------------------------------------------
CAPACIDADE_TOTAL = 100_000.0   # kWh
CONSUMO_DECOLAGEM = 30_000.0   # kWh
TAXA_PERDAS = 0.05             # 5% de dissipação térmica

carga_atual = CAPACIDADE_TOTAL * (nivel_energia / 100)
perdas = carga_atual * TAXA_PERDAS
consumo_total = CONSUMO_DECOLAGEM + perdas
autonomia_inicial = carga_atual - consumo_total

print()
print("--- ANÁLISE ENERGÉTICA ---")
print(f"Capacidade total ............: {CAPACIDADE_TOTAL:,.2f} kWh")
print(f"Carga atual ({nivel_energia}%) .........: {carga_atual:,.2f} kWh")
print(f"Perdas térmicas (5%) ........: {perdas:,.2f} kWh")
print(f"Consumo na decolagem ........: {CONSUMO_DECOLAGEM:,.2f} kWh")
print(f"Consumo total de lançamento .: {consumo_total:,.2f} kWh")
print(f"AUTONOMIA INICIAL ...........: {autonomia_inicial:,.2f} kWh")
print(f"Reserva sobre a carga atual .: {autonomia_inicial / carga_atual * 100:.2f}%")
