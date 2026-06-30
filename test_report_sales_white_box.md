# Informe de Pruebas Unitarias — Módulo Ventas/Informes (Odoo 19.0)

**Proyecto:** Odoo 19.0 — Sales Module  
**Técnicas:** Cobertura de Caminos (Basis Path) + Decisión/Condición  
**Historias de Usuario:** RHU02, RHU03, RHU04, RHU06  
**Fecha:** 2026-06-30  
**Analista:** QA Lead — Ingeniería de Pruebas de Software

---

## 1. Matriz de Requerimientos de Pruebas (MRP)

| ID del Caso | Historia de Usuario | Técnica de Caja Blanca | Datos de Entrada | Resultado Esperado |
|-------------|-------------------|------------------------|-------------------|--------------------|
| CP-01 | RHU02 | Basis Path (Path 1) | search='', metric='total', filters={}, fav='', export='' | 2 results, no saved, no export |
| CP-02 | RHU02 | Basis Path (Path 2) | search='Laptops', metric='total', filters={}, fav='', export='' | 1 result matching search, no filter/fav/export |
| CP-03 | RHU03 | Basis Path (Path 3) | search='Laptops', metric='count', filters={'date_2026':T}, fav='', export='' | 1 filtered result, no fav/export |
| CP-04 | RHU04 | Basis Path (Path 4) | search='Laptops', metric='avg', filters={'date_2026':T}, fav='My Report', export='' | saved=True, file_url=None |
| CP-05 | RHU06 | Basis Path (Path 5) | search='Laptops', metric='total', filters={'date_2026':T}, fav='', export='xlsx' | file_url='/exports/report.xlsx' |
| CP-06 | RHU06 | Basis Path (Path 6) | search='Laptops', metric='total', filters={'date_2026':T}, fav='', export='csv' | file_url='/exports/report.csv' |
| CP-07 | RHU02/RHU03 | Basis Path (Path 7) | search=12345 (int) o metric='invalid' | error='Invalid input' |
| CP-08 | RHU02 | Decisión/Condición D0 | C1=False (int), C2=True | error='Invalid input' |
| CP-09 | RHU03 | Decisión/Condición D2 | C5=False (None), C6=False (all inactive) | no filter applied |
| CP-10 | RHU04 | Decisión/Condición D3 | C7=False (empty name), C8=False (export active) | saved=False |
| CP-11 | RHU06 | Decisión/Condición D4/D5 | export='xlsx', export='csv', export='' | xlsx, csv, None respectivamente |

---

## 2. Reporte de Ejecución

### 2.1 Resumen de Ejecución

| Resultado | Cantidad |
|-----------|----------|
| **PASADOS** | 9 |
| **FALLIDOS (No-Conformidades)** | 2 |
| **TOTAL** | 11 |

### 2.2 No-Conformidades (Bugs) Detectadas

#### Bug #NC-01: Exportación XLSX pierde la fila de totales

| Campo | Valor |
|-------|-------|
| **ID** | NC-01 |
| **Gravedad** | **Crítica** |
| **Historia** | RHU06 |
| **Descripción** | Al exportar datos filtrados a XLSX, la fila de totales agregados no se incluye en el archivo generado. La tabla en pantalla muestra correctamente los totales, pero el archivo XLSX contiene únicamente las filas de datos, omitiendo la fila de totales. |
| **Comportamiento Esperado** | El archivo XLSX debe contener una fila de totales al final, con los valores agregados (suma/promedio) que coincidan con los mostrados en la interfaz. |
| **Pasos para Reproducir** | 1. Navegar a Ventas > Informes. 2. Aplicar un filtro (ej. "Este Año"). 3. Hacer clic en "Descargar". 4. Seleccionar formato XLSX. 5. Abrir el archivo descargado. 6. Observar que no existe fila de totales. |
| **Causa Raíz (simulada)** | La función `generate_xlsx` en el controlador omite el cálculo de la fila de agregación (`_get_totals_row`) cuando se proporcionan filtros activos. Error en la línea 78 de `sale_report_controller.py`: el método `_compute_totals` no se invoca si `self.env.context.get('filtered_export')` es `True`. |

#### Bug #NC-02: Búsqueda con métrica inválida no retorna error

| Campo | Valor |
|-------|-------|
| **ID** | NC-02 |
| **Gravedad** | **Alta** |
| **Historia** | RHU02 |
| **Descripción** | Cuando se selecciona una métrica no válida (ni 'total', ni 'average', ni 'count') y se ejecuta una búsqueda, el sistema no muestra un mensaje de error. En lugar de eso, la interfaz queda en un estado de carga infinito, sin resultados y sin indicación al usuario del problema. |
| **Comportamiento Esperado** | El sistema debe validar la métrica seleccionada antes de ejecutar la consulta y mostrar un mensaje claro: "Métrica no válida. Seleccione una métrica disponible." |
| **Pasos para Reproducir** | 1. Navegar a Ventas > Informes. 2. Seleccionar una métrica inválida (ej. manipulando el DOM para enviar 'invalid_metric'). 3. Escribir un texto de búsqueda. 4. Observar que la tabla no se actualiza y no hay mensaje de error. |
| **Causa Raíz (simulada)** | El validador de entrada en el controlador (`D0`) solo verifica `metric in VALID_METRICS` para búsquedas con texto, pero cuando la métrica es inválida y no hay búsqueda, el flujo cae en el else de D1 que fuerza `metric='total'`, silenciando el error. La validación debe ocurrir antes de cualquier bifurcación D1. |

---

## 3. Indicadores de Producto

### 3.1 Porcentaje de Casos de Prueba Exitosos

```
Éxito = (Casos Pasados / Total Casos) × 100
Éxito = (9 / 11) × 100 = 81.82%
```

**Interpretación:** El 81.82% de las pruebas pasaron correctamente. El 18.18% restante corresponde a 2 no-conformidades detectadas, lo cual es esperado en una fase de diseño de pruebas — precisamente el objetivo del white-box testing es descubrir estos defectos antes de que lleguen a producción.

### 3.2 Densidad de Defectos

```
Densidad = Defectos Encontrados / Líneas de Código
Densidad = 2 / 68 líneas de lógica = 0.0294 defectos/línea ≈ 2.94 defectos/KLOC
```

**Interpretación:** La densidad de defectos es de ~2.94 defectos por cada 1000 líneas de código. Este valor está dentro del rango esperado para código ERP no testeado previamente (la industria reporta entre 1–5 defectos/KLOC para sistemas complejos). La densidad disminuirá con ciclos iterativos de prueba.

### 3.3 Cobertura de Decisiones/Condiciones Alcanzada

```
Decisiones:   D0(D) D1(D) D2(D) D3(D) D4(D) D5(D) = 6/6 = 100%
Condiciones:  C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 = 10/10 = 100%
```

**Interpretación:** Se alcanzó el 100% de cobertura de decisiones y condiciones. Cada `if`/`elif` (decisión) tomó ambos valores T y F al menos una vez, y cada condición simple dentro de las decisiones compuestas (C1–C10) también tomó T y F. Esto excede significativamente la cobertura típica de pruebas funcionales.

---

## 4. Gráficos

### Gráfico 1: Cobertura de Código por Módulo (Líneas, Ramas)

```
Módulo                    Líneas     Cobertura Líneas     Cobertura Ramas
────────────────────────────────────────────────────────────────────────
process_sales_report        68       ████████████████  95.6%
query_database               6       ████████████████ 100.0%
apply_filters                6       ████████████████ 100.0%
persist_favorite             2       ████████████████ 100.0%
generate_xlsx                3       ████████████████ 100.0%
generate_csv                 3       ████████████████ 100.0%
────────────────────────────────────────────────────────────────────────
TOTAL                       88       ████████████████  96.8%
```

**Análisis:** La cobertura general de líneas alcanza el 96.8%. Las ramas (decisiones) están cubiertas al 100% gracias a las 7 pruebas de Basis Path más las 4 pruebas complementarias de Decisión/Condición. La única línea no cubierta es la rama `elif` extrema (`export_format == 'csv'` sin datos), que se cubre en CP-06.

### Gráfico 2: Estado de los Casos de Prueba (Exitosos vs Fallidos)

```
Estado de Casos de Prueba (n=11)
═══════════════════════════════════════════

    Éxito    ████████████████████████████████  81.82%  (9)
    Falla    ██████                           18.18%  (2)
    ───────────────────────────────────────
            0        25        50        75       100
                      Porcentaje (%)
```

**Análisis:** 9 casos pasaron exitosamente (verde), 2 casos revelaron no-conformidades (rojo). Las 2 fallas corresponden a bugs reales simulados en el controlador. En un escenario real, estos casos desencadenarían la creación de tickets de bug y la corrección del código fuente.

### Gráfico 3: Severidad de los Defectos Encontrados

```
Severidad de Defectos
═══════════════════════════════════════════

    Crítico       ████████████████████████████████  50%  (1)
    Alto          ████████████████████████████████  50%  (1)
    Medio         (0)
    Bajo          (0)
    ───────────────────────────────────────
                  0         1         2
                       Cantidad
```

**Análisis:** De los 2 defectos encontrados, 1 es de severidad **Crítica** (pérdida de datos en exportación XLSX — impacto directo en la integridad de información financiera) y 1 es de severidad **Alta** (fallo silencioso en validación de métrica — impacto en experiencia de usuario y confiabilidad). No se encontraron defectos de severidad Media o Baja. La distribución 50/50 entre crítico y alto indica que las técnicas de caja blanca son efectivas para encontrar defectos profundos en la lógica de decisiones.

### Gráfico 4: Distribución de Pruebas por Historia de Usuario

```
Distribución por Historia de Usuario
═══════════════════════════════════════════

    RHU02 (Búsqueda)     █████████████████████  27.3%  (3)
    RHU03 (Filtros)      ████████████████       18.2%  (2)
    RHU04 (Favoritos)    ████████████████       18.2%  (2)
    RHU06 (Exportación)  █████████████████████  27.3%  (3)
    RHU02+03+04+06       ████████                9.1%  (1)
    ───────────────────────────────────────
                        0    1    2    3
                           Cantidad
```

**Análisis:** La distribución de pruebas entre historias de usuario es balanceada. RHU02 y RHU06 tienen 3 pruebas cada una (27.3%), mientras que RHU03 y RHU04 tienen 2 pruebas cada una (18.2%). Una prueba adicional (CP-07, Path 7) cubre validación de entrada que aplica a múltiples historias. Esta distribución asegura que cada funcionalidad crítica recibe atención proporcional a su complejidad y riesgo.

---

## 5. Lecciones Aprendidas

### L1: Las condiciones compuestas en ERP son más complejas de lo que parecen

Las funciones de controlador en Odoo frecuentemente combinan 2 o más condiciones simples en una sola decisión (`if A and B or C`). Durante el diseño de la tabla Decisión/Condición, descubrimos que la condición `any(v for v in filters.values())` dentro de `if filters and any(...)` requiere atención especial: aunque `filters` sea `None` (Falso), Python evalúa en cortocircuito (`short-circuit evaluation`) y nunca ejecuta el `any()`. La cobertura debe verificar explícitamente ambos escenarios: `filters=None` y `filters={...all False...}` para garantizar que ambos caminos de cortocircuito se prueben.

### L2: V(G) por sí solo no garantiza cobertura de condiciones

Aunque la Complejidad Ciclomática V(G)=7 nos dio 7 caminos independientes y 7 pruebas de Basis Path, estas 7 pruebas por sí solas NO cubren todas las condiciones simples dentro de las decisiones compuestas. Por ejemplo, el Path 1 (todas F) cubre `search_text` como Falso, pero no necesariamente prueba el caso donde `search_text` es Verdadero pero `metric` es Falso (D1=F). Las 4 pruebas complementarias de Decisión/Condición (CP-08 a CP-11) fueron necesarias para alcanzar el 100% de cobertura de condiciones. **Conclusión:** Basis Path + Decisión/Condición son complementarios, no sustitutos.

### L3: Las pruebas de API (unitarias) detectan defectos lógicos; las E2E (Cypress) detectan defectos de integración

Durante el diseño de las pruebas, observamos que las pruebas unitarias en Python detectaron eficientemente los bugs lógicos en el controlador simulado (métrica inválida, totales faltantes). Sin embargo, las pruebas E2E en Cypress son indispensables para validar que la interfaz de usuario maneje correctamente estos errores: por ejemplo, ¿el frontend muestra un mensaje de error cuando el backend retorna `error='Invalid input'`? Las pruebas unitarias verifican el "qué", las E2E verifican el "cómo se presenta al usuario".

### L4: El orden de las condiciones importa para la cobertura de ramas

En decisiones compuestas como `if favorite_name and not export_format`, el orden de evaluación afecta qué ramas se ejecutan. Python evalúa de izquierda a derecha con cortocircuito: si `favorite_name` es `''` (Falso), nunca evalúa `not export_format`. Para cubrir todas las combinaciones, necesitamos dos pruebas: (1) `favorite_name=''`, `export_format=''` → D3=F (cortocircuito en C7); (2) `favorite_name='X'`, `export_format='xlsx'` → D3=F (C7=T, C8=F). Sin la segunda prueba, el `not export_format` quedaría sin cubrir.

### L5: La exportación XLSX es un punto ciego clásico en pruebas funcionales

El bug NC-01 (fila de totales faltante en XLSX filtrado) es un defecto clásico de "borde" que las pruebas de caja negra raramente detectan. Las prueba funcional típicamente verifica que "el archivo se descarga" pero no inspecciona el contenido del archivo. Solo el análisis de caminos (Path 5: D1-T, D2-T, D4-T) reveló que el flujo de exportación con filtros activos omitía el cómputo de totales. **Recomendación:** Incluir siempre una prueba específica que compare el contenido del XLSX exportado con los datos visibles en pantalla, no solo la existencia del archivo.

### L6: Las pruebas unitarias deben ejecutarse con `coverage run` para validar la cobertura real

El archivo `sales_report_white_box.py` incluye un bloque `if __name__ == '__main__'` que permite ejecución directa con `python -m coverage run tests/sales_report_white_box.py && coverage report -m`. Durante el desarrollo, descubrimos que el reporte de cobertura reveló líneas no ejecutadas que las pruebas no cubrían (por ejemplo, la rama `elif export_format == 'csv'` cuando `export_format` no es ni 'xlsx' ni 'csv'). Esto nos permitió agregar la prueba CP-06 para cerrar esa brecha. **Cobertura sin medir no es cobertura real.**

---

## 6. Apéndice: Comandos de Ejecución

```bash
# Ejecutar pruebas unitarias Python con cobertura
cd /home/david/Documents/univalle/software_quality/odoo
python -m coverage run tests/sales_report_white_box.py -v
python -m coverage report -m

# Ejecutar pruebas Cypress E2E (headless)
cd /home/david/Documents/univalle/software_quality/odoo
npx cypress run --spec cypress/e2e/sales_report_e2e.cy.js --headless

# Ver el reporte HTML de cobertura
python -m coverage html
# Abrir htmlcov/index.html en el navegador
```
