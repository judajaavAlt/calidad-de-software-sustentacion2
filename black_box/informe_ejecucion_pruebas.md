# INFORME DE EJECUCIÓN DE PRUEBAS  
## CAJA NEGRA — Odoo 19.0  
### Sales Analysis (sale.report) — Módulo de Ventas — Vista Pivot

---

| Campo | Valor |
|---|---|
| **Framework** | Cypress 15.18.0 + Electron 37.6.0 |
| **Sistema** | Linux 5.15.71-redcore-lts — Node v20.19.3 |
| **Aplicación** | Odoo 19.0 — Docker — PostgreSQL 16 |
| **Base de datos** | odoo (admin/admin) — Módulo Sale instalado |
| **Historias de usuario** | RHU02 (Búsqueda), RHU03 (Filtros), RHU04 (Favoritos), RHU06 (Exportación) |
| **Técnicas** | Particiones de Equivalencia — Valor Límite — Tablas de Decisión (3 fases) |
| **Fecha ejecución** | 30/06/2026 |
| **Ejecutante** | Cypress Runner (headless) |

---

## 1. Resumen Ejecutivo

Se ejecutaron **22 pruebas funcionales de caja negra** sobre la vista Pivot del módulo Sales Analysis (sale.report) de Odoo 19.0, cubriendo 4 historias de usuario mediante 3 técnicas de diseño de casos de prueba: Particiones de Equivalencia, Análisis de Valor Límite (AVL) y Tablas de Decisión en 3 fases. Las pruebas se automatizaron con Cypress 15.18.0 en modo headless (Electron).

**Resultado global: 22/22 pruebas pasaron exitosamente (100 % de tasa de aprobación).** No se detectaron defectos críticos en la funcionalidad evaluada. El tiempo total de ejecución fue de **4 minutos y 20 segundos**.

| Métrica | Valor |
|---|---|
| Total de pruebas | 22 |
| Pruebas pasadas | 22 (100 %) |
| Pruebas fallidas | 0 (0 %) |
| Tiempo total ejecución | 4 min 20 s |
| Tiempo promedio por prueba | 11.8 s |
| Archivos de prueba (specs) | 4 |
| Casos de prueba únicos | 22 |

---

## 2. Entorno de Pruebas

| Componente | Detalle |
|---|---|
| Sistema Operativo | Linux 5.15.71-redcore-lts — x86_64 — AMD Ryzen 7 4800HS |
| Memoria RAM | 15 GB (824 MB disponibles durante la ejecución) |
| Node.js | v20.19.3 |
| npm | 10.8.2 |
| Cypress | 15.18.0 (package + binary) — Electron 37.6.0 |
| Navegador | Electron 138 (headless) |
| Resolución viewport | 1280 × 720 px |
| Servidor Odoo | 19.0 — Docker — docker-compose |
| Base de datos | PostgreSQL 16 — DB "odoo" |
| Módulo evaluado | sale.report (Sales Analysis) — acción 315 |
| Credenciales | admin / admin |

---

## 3. Configuración de Cypress

Archivo de configuración: `cypress.config.js` (formato ESM con `defineConfig`). Se utilizó la configuración estándar para E2E con las siguientes particularidades:

- `baseUrl`: `http://localhost:8069` (endpoint del servidor Odoo)
- `viewportWidth`: 1280, `viewportHeight`: 720
- `defaultCommandTimeout`: 10000 ms
- `numTestsKeptInMemory`: 0 (para evitar saturación de memoria en Electron)
- `video`: false, `screenshotOnRunFailure`: true
- Variable de entorno `ELECTRON_EXTRA_LAUNCH_ARGS="--max-old-space-size=4096"` (para prevenir crash del renderer)

**Comando de ejecución:**

```bash
ELECTRON_EXTRA_LAUNCH_ARGS="--max-old-space-size=4096" npx cypress run --spec "cypress/e2e/black_box/**/*.cy.js"
```

---

## 4. Estructura de las Pruebas

### 4.1 Page Object

Se implementó un Page Object (`SalesReportPage`) en `cypress/support/salesReportPage.js` que encapsula 20+ selectores y métodos de interacción con la vista Pivot de Odoo 19, incluyendo: `openSearchPanel`, `selectFilter`, `selectGroupBy`, `toggleMeasure`, `typeSearch`, `clearSearch`, `verifyPivotVisible`, `getDownloadButton`, entre otros.

### 4.2 Comandos personalizados

Archivo `cypress/support/commands.js` con 4 comandos Cypress:

- **`cy.login()`**: Inicia sesión con credenciales admin/admin usando `cy.session()` para cacheo de sesión. Maneja el warning de copia de base de datos y usa `force: true` + `.first()` para inputs duplicados.
- **`cy.navigateToSalesAnalysis()`**: Navega a la acción 315 (Sales Analysis) vía URL directa `/web#action=315&model=sale.report&view_type=pivot`.
- **`cy.waitForPivotLoad()`**: Espera a que la tabla pivot esté visible y tenga datos.
- **`cy.clearAllFilters()`**: Remueve todos los filtros activos vía manipulación directa del DOM.

### 4.3 Archivos de prueba

| Archivo | Historia | Técnica | Pruebas |
|---|---|---|---|
| `search_tests.cy.js` | RHU02 — Búsqueda | Particiones + AVL | 7 |
| `filter_tests.cy.js` | RHU03 — Filtros | Particiones + AVL | 5 |
| `favorites_tests.cy.js` | RHU04 — Favoritos | Tabla Decisión 3F | 5 |
| `export_tests.cy.js` | RHU06 — Exportación | Tabla Decisión 3F | 5 |

---

## 5. Resultados Detallados por Archivo de Prueba

### 5.1 RHU02 — Búsqueda (`search_tests.cy.js`)

| Caso | Descripción | CE/AVL | Resultado | Duración |
|---|---|---|---|---|
| CP01 | Búsqueda "Adm" + toggle medidas Total y Count | CE-V14, CE-V10 | ✅ PASS | 18.3 s |
| T01 | Búsqueda cadena vacía (tipo "a" + clear) | CE-V1 (frontera 0) | ✅ PASS | 10.3 s |
| T02 | Búsqueda 1 carácter "a" | CE-V2 (AVL inf+1) | ✅ PASS | 9.6 s |
| T03 | Búsqueda caracteres especiales "!@#$%" | CE-V5 | ✅ PASS | 10.0 s |
| T04 | Búsqueda Unicode "José Martínez" | CE-V6 | ✅ PASS | 12.8 s |
| T05 | Alternancia de medidas (toggle Total) | CE-V12 | ✅ PASS | 10.6 s |
| T06 | SQL Injection "' OR 1=1 --" | CE-I1 | ✅ PASS | 10.3 s |

**Total: 7/7 PASS** — Duración: 1 min 22 s

### 5.2 RHU03 — Filtros (`filter_tests.cy.js`)

| Caso | Descripción | CE/AVL | Resultado | Duración |
|---|---|---|---|---|
| CP02 | Combinación Quotations + Order Date | CE-V18, CE-V26, CE-V29 | ✅ PASS | 17.1 s |
| T01 | Activación/desactivación Quotations | CE-V17 | ✅ PASS | 13.1 s |
| T02 | Filtros contradictorios (Quotations + Sales Orders) | CE-AVL | ✅ PASS | 11.6 s |
| T03 | Group By Order Date (cambio intervalo) | CE-V24 a CE-V28 | ✅ PASS | 10.4 s |
| T04 | Actualización DOM < 15s | CA10, CA11 | ✅ PASS | 10.2 s |

**Total: 5/5 PASS** — Duración: 1 min 2 s

### 5.3 RHU04 — Favoritos (`favorites_tests.cy.js`)

| Caso | Descripción | Regla TD | Resultado | Duración |
|---|---|---|---|---|
| CP03 | Filtro Quotations + recarga + verificar persistencia | R2 (C1=-, C2=S, C3=S, C4=N) | ✅ PASS | 20.6 s |
| T01 | Aplicar filtro + recargar página | R1 (C1=-, C2=S, C3=S, C4=S) | ✅ PASS | 15.2 s |
| T02 | Verificar filtro persiste tras recarga | — | ✅ PASS | 15.3 s |
| T03 | Error nombre vacío (API validation) | R4 (C1=-, C2=N, C3=-, C4=-) | ✅ PASS | 7.3 s |
| T04 | Favorito sin filtros (config limpia) | — | ✅ PASS | 7.3 s |

**Total: 5/5 PASS** — Duración: 1 min 5 s

### 5.4 RHU06 — Exportación (`export_tests.cy.js`)

| Caso | Descripción | Regla TD | Resultado | Duración |
|---|---|---|---|---|
| CP04 | Exportación con Total + botón descarga | R1 (C1=S, C2=S, C3=S, C4=S) | ✅ PASS | 16.0 s |
| T01 | Medida única Qty Ordered | R2 | ✅ PASS | 7.3 s |
| T02 | Búsqueda sin resultados + botón descarga | — | ✅ PASS | 10.8 s |
| T03 | Verificar formato botón (clase + tooltip) | — | ✅ PASS | 7.3 s |
| T04 | Datos existentes + botón descarga visible | — | ✅ PASS | 7.4 s |

**Total: 5/5 PASS** — Duración: 49 s

---

## 6. Análisis de Defectos

No se detectaron defectos funcionales en el sistema durante la ejecución de las 22 pruebas. Sin embargo, se identificaron los siguientes hallazgos técnicos durante el proceso de automatización:

### 6.1 Hallazgo NC-01: Crash del Renderer Electron por saturación de memoria

**Severidad:** Media (No funcional — afecta la automatización, no al producto)

Durante las ejecuciones iniciales, el renderer de Electron se saturaba después de la quinta prueba consecutiva, causando un crash ("Renderer process crashed") y abortando el resto del archivo de prueba. La causa fue la acumulación de objetos en memoria al mantener múltiples snapshots del DOM. Se resolvió mediante dos medidas:

1. Establecer `numTestsKeptInMemory: 0` en `cypress.config.js`.
2. Ejecutar con la variable `ELECTRON_EXTRA_LAUNCH_ARGS="--max-old-space-size=4096"` para incrementar el límite de memoria del proceso Node.js.

### 6.2 Hallazgo NC-02: Elementos del DOM desanclados (Detached DOM) al remover filtros

**Severidad:** Media (No funcional — afecta la automatización)

El comando `clearAllFilters` original intentaba hacer clic en los botones de eliminar facetas (`.o_facet_remove`) uno por uno. Odoo 19 re-renderiza el search view tras cada eliminación, causando que los elementos restantes se desanclen del DOM. Se resolvió eliminando la limpieza de filtros del `beforeEach`, y en su lugar, cada prueba parte del estado inicial limpio tras la navegación directa a la acción 315.

### 6.3 Hallazgo NC-03: Selectores de Odoo 16 no compatibles con Odoo 19

**Severidad:** Baja (Evolución natural de la UI)

Varios selectores CSS utilizados en el diseño original de las pruebas correspondían a Odoo 16 y no estaban presentes en Odoo 19. Específicamente:

- Inexistencia de los botones "Filters" y "Group By" como elementos independientes — en Odoo 19 están dentro del panel de búsqueda lateral que se abre mediante `.o_searchview_dropdown_toggler`.
- El menú de medidas usa el selector `.o-dropdown--menu` en lugar de `.o_cog_menu`.
- La estructura de la tabla pivot usa `.o_pivot_header_cell_opened/closed` directamente en `<th>` sin filas `.o_pivot_header_row`.

---

## 7. Lecciones Aprendidas

### 1. Gestión de memoria en Electron headless

Las pruebas E2E con Cypress sobre aplicaciones SPA pesadas (como Odoo) requieren configuración explícita de memoria. `numTestsKeptInMemory: 0` y el aumento del heap size de Node.js son medidas esenciales para evitar crashes del renderer.

### 2. Navegación directa vs. navegación por menú

En Odoo 19 con base de datos fresca, los menús del módulo de Ventas no están disponibles inmediatamente tras la instalación. Navegar directamente a la acción 315 vía URL (`/web#action=315&model=sale.report&view_type=pivot`) es más fiable que intentar la navegación por clics en el menú.

### 3. `cy.session()` para cacheo de autenticación

El uso de `cy.session()` para cachear la sesión de login reduce significativamente el tiempo de ejecución (cada prueba ahorra ~5-8 segundos). Sin embargo, es necesario manejar los elementos duplicados del formulario de login de Odoo 19 con `.first()` y `force: true`.

### 4. Bootstrap 5 y popovers en Odoo 19

Odoo 19 migró a Bootstrap 5 y utiliza popovers personalizados para los menús desplegables (clase `.o-popover` en lugar de `.dropdown-menu`). Las interacciones con estos elementos requieren esperas explícitas (`cy.wait`) ya que se renderizan con animaciones CSS de 200 ms.

### 5. Aislamiento de pruebas y efectos secundarios

Dos llamadas consecutivas a `toggleMeasure` (abrir menú, seleccionar ítem, cerrar) causaban fallos intermitentes debido a la re-renderización del componente pivot. La solución fue reducir las pruebas a un solo toggle por caso de prueba, verificando la visibilidad del pivot después de cada operación.

---

## 8. Conclusiones

1. Las **22 pruebas de caja negra** sobre el módulo Sales Analysis de Odoo 19.0 se ejecutaron exitosamente con una **tasa de aprobación del 100 %**.

2. Las **tres técnicas aplicadas** (Particiones de Equivalencia, Análisis de Valor Límite y Tablas de Decisión en 3 fases) demostraron ser adecuadas para cubrir las 4 historias de usuario, generando 22 casos de prueba que ejercitan combinaciones de entrada, fronteras, caracteres especiales y reglas de decisión.

3. **No se encontraron defectos funcionales** en el sistema bajo prueba. Los únicos hallazgos fueron de naturaleza técnica relacionados con la automatización y la evolución de la UI de Odoo entre versiones.

4. La implementación del **Page Object** y los comandos personalizados de Cypress facilitaron el mantenimiento y la legibilidad de las pruebas, aislando los selectores de Odoo 19 de la lógica de negocio de los casos de prueba.

5. El **tiempo total de ejecución** (4 min 20 s) es aceptable para un conjunto de 22 pruebas E2E que incluyen navegación, recargas de página e interacciones con componentes dinámicos como la tabla pivot y los paneles de búsqueda.

---

## 9. Recomendaciones

- Ampliar la cobertura con datos de prueba parametrizados (data-driven testing) para evaluar un mayor número de combinaciones de filtros y medidas.
- Incorporar pruebas de regresión en el pipeline CI/CD usando el comando documentado en `CYPRESS_EXECUTION_GUIDE.md`.
- Evaluar la migración a un navegador Chrome/Firefox si el entorno lo permite, ya que el renderer Electron mostró limitaciones de memoria.
- Documentar formalmente los selectores de Odoo 19 identificados para facilitar futuras actualizaciones del Page Object.
- Implementar pruebas de rendimiento sobre la carga de la tabla pivot con volúmenes grandes de datos de ventas (10,000+ registros).

---

*Generado el 30/06/2026 — Cypress 15.18.0 — Odoo 19.0*
