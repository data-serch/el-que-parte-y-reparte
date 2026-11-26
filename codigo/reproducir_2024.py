"""Reproduce la asignación de 2024 y calcula la propuesta.

Uso:  python reproducir_2024.py   (requiere pandas)
"""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from regla import regla_propuesta, shapley_shubik, banzhaf, mas_votado, asignar

DATOS = os.path.join(os.path.dirname(__file__), '..', 'datos')
d = pd.read_csv(os.path.join(DATOS, 'distritos_2024.csv'), keep_default_na=False)
vne = pd.read_csv(os.path.join(DATOS, 'votacion_nacional_emitida_2024.csv')).set_index('partido').votacion_nacional_emitida.to_dict()

SHH = ['Morena', 'PVEM', 'PT']
FYCM = ['PAN', 'PRI', 'PRD']
P = SHH + FYCM + ['MC']
COL = {'Morena': 'MORENA_REPARTIDO', 'PVEM': 'PVEM_REPARTIDO', 'PT': 'PT_REPARTIDO',
       'PAN': 'PAN_REPARTIDO', 'PRI': 'PRI_REPARTIDO', 'PRD': 'PRD_REPARTIDO', 'MC': 'MC'}


def triunfos(regla_shh, regla_fycm):
    mr = {p: 0.0 for p in P}
    for _, r in d.iterrows():
        v = {p: float(r[COL[p]]) for p in P}
        cont = []
        cont += [('SHH', sum(v[k] for k in SHH))] if r.COALICION_SHH else [(k, v[k]) for k in SHH]
        cont += [('FYCM', sum(v[k] for k in FYCM))] if r.COALICION_FYCM else [(k, v[k]) for k in FYCM]
        cont += [('MC', v['MC'])]
        if float(r.IND) > 0:
            cont.append(('IND', float(r.IND)))
        cont.sort(key=lambda c: -c[1])
        gana, segundo = cont[0][0], cont[1][1]
        if gana == 'SHH':
            for k, x in regla_shh({k: v[k] for k in SHH}, segundo, r).items():
                mr[k] += x
        elif gana == 'FYCM':
            for k, x in regla_fycm({k: v[k] for k in FYCM}, segundo, r).items():
                mr[k] += x
        elif gana != 'IND':
            mr[gana] += 1
    return mr


def redondear(mr):
    """Resto mayor dentro de cada coalición: no hay medio diputado."""
    for grupo in (SHH, FYCM):
        tot = round(sum(mr[k] for k in grupo))
        base = {k: int(mr[k]) for k in grupo}
        for k in sorted(grupo, key=lambda k: -(mr[k] - base[k]))[: tot - sum(base.values())]:
            base[k] += 1
        mr.update(base)
    return mr


def curules(mr):
    rp, tope = asignar({k: mr[k] for k in vne}, vne)
    s = {k: int(round(mr[k] + rp.get(k, 0))) for k in P}
    s['IND'] = 1
    return s, rp


def por_etiqueta(col):
    return lambda w, q, r: {k: (1.0 if k == r[col] else 0.0) for k in w}


envolver = lambda f: (lambda w, q, r: f(w, q))
OFICIAL_MIL = {'PAN': 31, 'PRI': 10, 'PRD': 1}   # INE/CG2129/2024, transcrito en SUP-REC-3505/2024, p. 64
OFICIAL_SIG = {'PAN': 32, 'PRI': 9, 'PRD': 1}    # constancias

escenarios = {
    'Convenio (siglado), regla 2009-2018': {**redondear(triunfos(por_etiqueta('SIGLADO_SHH'), envolver(mas_votado))), **OFICIAL_SIG},
    'Militancia, regla del INE desde 2021': {**redondear(triunfos(por_etiqueta('MILITANCIA_SHH'), envolver(mas_votado))), **OFICIAL_MIL},
    'Propuesta: a quien puso los votos': redondear(triunfos(envolver(regla_propuesta), envolver(regla_propuesta))),
    'Variante: mas votado (Otalora)': redondear(triunfos(envolver(mas_votado), envolver(regla_propuesta))),
    'Variante: Shapley-Shubik puro': redondear(triunfos(envolver(shapley_shubik), envolver(regla_propuesta))),
    'Variante: Banzhaf': redondear(triunfos(envolver(banzhaf), envolver(regla_propuesta))),
}

filas = []
for nombre, mr in escenarios.items():
    s, rp = curules(mr)
    filas.append(dict(escenario=nombre, **{f'MR_{k}': int(mr[k]) for k in SHH}, **{f'RP_{k}': rp[k] for k in SHH},
                      **s, coalicion=s['Morena'] + s['PVEM'] + s['PT']))
t = pd.DataFrame(filas).set_index('escenario')
pd.set_option('display.width', 200)
print(t.to_string())

mil = t.loc['Militancia, regla del INE desde 2021']
oficial = {'Morena': 257, 'PVEM': 60, 'PT': 47, 'PAN': 71, 'PRI': 36, 'MC': 27}
assert all(mil[k] == v for k, v in oficial.items()), 'No reproduce el acuerdo INE/CG2129/2024'
print('\nOK: con la militancia se reproduce el acuerdo INE/CG2129/2024 (257, 60, 47, 71, 36, 27).')

prop = t.loc['Propuesta: a quien puso los votos']
print(f"Propuesta: Morena, PT y PVEM {prop.coalicion} curules en la cuenta del tope.")
banc = {'Morena': 161 + prop.RP_Morena, 'PVEM': 57 + prop.RP_PVEM, 'PT': 38 + prop.RP_PT}
print('Bancadas reales (distritos por constancia + plurinominales):', banc, '=', sum(banc.values()))
t.to_csv(os.path.join(DATOS, '..', 'resultados_2024.csv'))
