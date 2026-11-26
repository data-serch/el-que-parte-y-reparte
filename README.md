# El que parte y reparte…

Siglado, coaliciones y sobrerrepresentación en la Cámara de Diputados.

Datos, código y método de la ponencia de Sergio A. Bárcena Juárez (Tecnológico de Monterrey · Buró Parlamentario) en el foro del INE *La representación proporcional en México. Perspectivas y dilemas*, mesa técnico-jurídica, 26 de noviembre de 2026.

- Presentación: [presentacion.html](https://data-serch.github.io/el-que-parte-y-reparte/presentacion.html)
- Resultados: [`resultados_2024.csv`](resultados_2024.csv)

## Propuesta

Para revisar el tope de ocho puntos del artículo 54 constitucional, cada distrito que gana una coalición se le cuenta al partido que puso los votos para ganarlo.

## Método

Hay dos libretas:

- Libreta de asientos. Dónde se sienta cada diputado de distrito. Manda el convenio de coalición (siglado): constancia y bancada. No cambia.
- Libreta del tope. A quién se le cuenta cada triunfo para revisar los ocho puntos. Hoy el INE usa la militancia del candidato (desde 2021). La propuesta usa los votos.

En cada distrito que gana la coalición:

1. Si un partido ganó solo (sus votos superan al segundo lugar), se le cuenta el triunfo entero. Si fueran varios, el de más votos.
2. Si ninguno ganó solo, el triunfo se reparte con el índice de Shapley-Shubik (1954): de los seis órdenes en que pueden "subirse a la báscula" tres partidos, la proporción en que cada uno convierte a la coalición de perdedora en ganadora. Con tres partidos salen cuatro hipótesis:

| Hipótesis | Reparto | Ejemplo 2024 | Distritos 2024 |
|---|---|---|---|
| 1. Un partido ganó solo | 1 · 0 · 0 | Tijuana, Rioverde | 176 |
| 2. Uno gana con cualquiera de los otros dos | 2/3 · 1/6 · 1/6 | Morelia | 18 |
| 3. Solo una pareja gana | 1/2 · 1/2 · 0 | Ciudad Hidalgo | 11 |
| 4. Solo ganan los tres juntos, o cualquier pareja | 1/3 · 1/3 · 1/3 | Salinas Victoria | 14 |

3. Las fracciones se suman en todo el país y se redondean por resto mayor dentro de cada coalición (no hay medio diputado).
4. Se aplica el tope de cada partido, como hoy: los distritos que se le cuentan entran primero; las plurinominales llenan los lugares que quedan.

Se aplica igual a cualquier coalición.

## Resultados con los votos de 2024

| Regla para contar cada distrito | Morena | PVEM | PT | Morena + PVEM + PT |
|---|---|---|---|---|
| Convenio (siglado), regla de 2009 a 2018 | 248 | 75 | 50 | 373 |
| Militancia, regla del INE desde 2021 (reproduce INE/CG2129/2024) | 257 | 60 | 47 | 364 |
| Propuesta: a quien puso los votos | 257 | 45 | 27 | 329 |

Cifras de la libreta del tope. Mayoría calificada: 334 curules. Con la propuesta, la oposición tendría 171.

Bancadas reales con la propuesta (distritos por constancia más plurinominales): Morena 161 + 28 = 189; PVEM 57 + 27 = 84; PT 38 + 18 = 56. Hoy: 236, 77 y 51. El recorte cae en las plurinominales de Morena, que ya estaba en su tope: de 75 a 28. Las 47 que deja de recibir se reparten por votos: 12 al PVEM y al PT, y 35 a la oposición.

Variantes, para comparar: contar todo al partido más votado (voto particular de la magistrada Otálora en SUP-REC-3505/2024) da 313; Shapley-Shubik puro, 336; Banzhaf, 338. Las dos últimas les reconocen a los aliados votos que no hicieron falta en distritos que Morena ganó solo.

## Reproducir

```
pip install pandas
python codigo/reproducir_2024.py
```

El script comprueba que, con la militancia, se obtiene exactamente la asignación del acuerdo INE/CG2129/2024 (Morena 257, PVEM 60, PT 47, PAN 71, PRI 36, MC 27) y después calcula la propuesta y las variantes.

## Datos

| Archivo | Contenido | Fuente |
|---|---|---|
| `datos/distritos_2024.csv` | Votos por partido y combinación en los 300 distritos; columnas `_REPARTIDO` con los votos marcados en varios logos repartidos según la LGIPE (art. 311, párr. 1, inciso c); coalición, siglado y militancia de los 219 distritos que ganó Sigamos Haciendo Historia | Cómputos distritales INE 2024; convenio de coalición; INE/CG2129/2024 |
| `datos/votacion_nacional_emitida_2024.csv` | Votación nacional emitida de los partidos con derecho a plurinominales | INE/CG2129/2024 |
| `datos/integracion_oficial_2024.csv` | Integración por constancia y por militancia | INE/CG2129/2024; SUP-REC-3505/2024, pp. 63-64 |
| `datos/serie_2009_2024.csv` | Votos y curules del partido más grande y de la coalición ganadora, 2009-2024 | Acuerdos de asignación CG426/2009, CG582/2012, INE/CG804/2015, INE/CG1181/2018, INE/CG1443/2021, INE/CG2129/2024 |

Notas:

- Michoacán 9 lo ganó una candidatura independiente (61,980 votos en el cómputo distrital); se incluye en la columna `IND`.
- Para la oposición, en los escenarios de convenio y militancia se usan los triunfos oficiales del INE; en la propuesta y las variantes, la regla se aplica también a la coalición del PAN, el PRI y el PRD.
- En 2018, el voto particular de Otálora reporta 306 curules y 45.42 %; el acuerdo del INE, 308 y 45.70 %.

## Límites

- No cambia constancias ni bancadas: los electos quedan en el grupo que fija el convenio (LGPP, art. 87, párr. 11).
- No impide en todos los escenarios una mayoría calificada.
- No corrige el voto marcado en varios logos ni los cambios de bancada.
- Las bancadas con la propuesta pueden variar en una curul por redondeo.

## Licencia y cita

Código: MIT. Datos, texto y presentación: CC BY 4.0.

Bárcena Juárez, Sergio A. (2026). *El que parte y reparte… Siglado, coaliciones y sobrerrepresentación en la Cámara de Diputados*. Ponencia en el foro del INE "La representación proporcional en México. Perspectivas y dilemas", 26 de noviembre de 2026. https://github.com/data-serch/el-que-parte-y-reparte
