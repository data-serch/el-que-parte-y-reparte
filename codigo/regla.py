"""Regla "cada distrito, a quien puso los votos" y fórmula de asignación del art. 54.

Funciones puras, sin dependencias externas. Ver ../README.md.
"""
import itertools, math


def shapley_shubik(w, q):
    """Índice de Shapley-Shubik de un distrito.

    w: votos de cada partido de la coalición, p. ej. {'Morena': 63165, 'PVEM': 19364, 'PT': 8879}
    q: votos del segundo lugar.
    Devuelve la proporción de los órdenes posibles en que cada partido "inclina la báscula",
    es decir, convierte a la coalición de perdedora en ganadora.
    """
    partidos = list(w)
    piv = {p: 0 for p in partidos}
    ordenes = list(itertools.permutations(partidos))
    for orden in ordenes:
        acum = 0
        for p in orden:
            if acum <= q < acum + w[p]:
                piv[p] += 1
                break
            acum += w[p]
    return {p: piv[p] / len(ordenes) for p in partidos}


def banzhaf(w, q):
    """Índice de Banzhaf normalizado (variante, solo para comparar)."""
    partidos = list(w)
    cnt = {p: 0 for p in partidos}
    for r in range(1, len(partidos) + 1):
        for S in itertools.combinations(partidos, r):
            tot = sum(w[x] for x in S)
            if tot > q:
                for p in S:
                    if tot - w[p] <= q:
                        cnt[p] += 1
    T = sum(cnt.values()) or 1
    return {p: cnt[p] / T for p in partidos}


def regla_propuesta(w, q):
    """Paso 1: si un partido gana solo, el distrito es suyo (si son varios, el de más votos).
    Paso 2: si ninguno gana solo, se reparte con Shapley-Shubik."""
    solos = [p for p in w if w[p] > q]
    if solos:
        m = max(solos, key=lambda x: w[x])
        return {p: (1.0 if p == m else 0.0) for p in w}
    return shapley_shubik(w, q)


def mas_votado(w, q):
    """Variante del voto particular de la magistrada Otálora: todo al más votado."""
    m = max(w, key=lambda x: w[x])
    return {p: (1.0 if p == m else 0.0) for p in w}


def resto_mayor(n, votos):
    """Reparte n curules en proporción a votos por cociente y resto mayor."""
    t = sum(votos.values())
    cuota = {k: n * v / t for k, v in votos.items()}
    base = {k: int(x) for k, x in cuota.items()}
    for k in sorted(cuota, key=lambda k: -(cuota[k] - base[k]))[: n - sum(base.values())]:
        base[k] += 1
    return base


def asignar(mr, vne, rp=200, maximo=300, margen=8):
    """Asignación de las 200 plurinominales con el tope del art. 54, fr. IV y V.

    mr:  triunfos de mayoría que se le cuentan a cada partido (libreta del tope).
    vne: votación nacional emitida de los partidos con derecho a plurinominales.
    El partido que rebasaría su tope recibe solo las plurinominales que le caben;
    el resto se reparte entre los demás por resto mayor (se repite si otro rebasa).
    Devuelve (plurinominales, tope de curules por partido).
    """
    T = sum(vne.values())
    tope = {k: min(maximo, math.floor(5 * (100 * v / T + margen) + 1e-9)) for k, v in vne.items()}
    fijos = {}
    while True:
        libres = {k: v for k, v in vne.items() if k not in fijos}
        a = resto_mayor(rp - sum(fijos.values()), libres)
        rebasa = False
        for k in libres:
            if mr.get(k, 0) + a[k] > tope[k] + 1e-9:
                fijos[k] = max(0, math.floor(tope[k] - mr.get(k, 0) + 1e-9))
                rebasa = True
        if not rebasa:
            a.update(fijos)
            return a, tope
