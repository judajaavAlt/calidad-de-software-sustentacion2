# Guía de Ejecución de Pruebas Cypress — Caja Negra
## Módulo Ventas/Informes Odoo 19.0 (sale.report)

---

## 1. Requisitos Previos

| Componente | Versión Mínima | Verificación |
|------------|---------------|--------------|
| Node.js | 18.x | `node --version` |
| npm | 8.x | `npm --version` |
| Odoo 19.0 | 19.0 | Corriendo en `http://localhost:8069` |
| Navegador | Chrome/Chromium 100+ | Instalado en el sistema |

**Verificar instalaciones actuales:**
```bash
node --version   # → v20.19.3
npm --version    # → 10.8.2
```

---

## 2. Instalación de Cypress

### 2.1 Inicializar proyecto npm (si no existe)

Desde la raíz del proyecto Odoo:

```bash
cd /home/david/Documents/univalle/software_quality/odoo
npm init -y
```

Esto crea un `package.json` básico.

### 2.2 Instalar Cypress como dependencia de desarrollo

```bash
npm install cypress --save-dev
```

> ⏱ La instalación descarga el binario de Cypress (~200 MB). Puede tomar 2-5 minutos según el ancho de banda.

### 2.3 Verificar la instalación

```bash
npx cypress --version
```

Salida esperada:
```
Cypress package version: 13.x.x
Cypress binary version: 13.x.x
Electron version: ...
```

### 2.4 (Opcional) Instalar plugin para verificar descargas

Si se van a ejecutar pruebas de exportación XLSX:

```bash
npm install --save-dev cypress-downloadfile
```

Luego agregar en `cypress/support/e2e.js`:
```javascript
require('cypress-downloadfile/lib/downloadFileCommand');
```

---

## 3. Configuración de Cypress

### 3.1 Archivo de configuración `cypress.json`

El archivo ya existe en `/home/david/Documents/univalle/software_quality/odoo/cypress/cypress.json`:

```json
{
  "baseUrl": "http://localhost:8069",
  "viewportWidth": 1280,
  "viewportHeight": 720,
  "defaultCommandTimeout": 10000,
  "video": false,
  "screenshotOnRunFailure": true,
  "downloadsFolder": "cypress/downloads",
  "e2e": {
    "specPattern": "cypress/e2e/**/*.cy.js"
  }
}
```

**Opciones clave:**

| Opción | Valor | Descripción |
|--------|-------|-------------|
| `baseUrl` | `http://localhost:8069` | URL de Odoo (cambiar si usa otro puerto) |
| `defaultCommandTimeout` | `10000` | 10s máximo por comando Cypress |
| `video` | `false` | Grabación de video desactivada (activar si se requiere) |
| `screenshotOnRunFailure` | `true` | Captura automática en fallos |
| `specPattern` | `cypress/e2e/**/*.cy.js` | Patrón de búsqueda de archivos de prueba |

### 3.2 Configurar credenciales de Odoo

Las credenciales están en `cypress/support/commands.js`:

```javascript
const ODOO_DB = 'odoo';
const ODOO_USER = 'admin';
const ODOO_PASS = 'admin';
```

Cambiar según la base de datos y usuario de Odoo configurados.

### 3.3 Estructura de archivos de prueba

```
cypress/
├── cypress.json                          # Configuración
├── support/
│   ├── e2e.js                            # Punto de entrada (imports)
│   ├── commands.js                       # Comandos personalizados (login, navegación)
│   └── salesReportPage.js                # Page Object con selectores Odoo
├── downloads/                            # Archivos descargados (XLSX)
└── e2e/
    ├── sales_report_e2e.cy.js            # Pruebas previas (white-box)
    └── black_box/
        ├── search_tests.cy.js            # RHU02 — Búsqueda (7 tests)
        ├── filter_tests.cy.js            # RHU03 — Filtros (5 tests)
        ├── favorites_tests.cy.js         # RHU04 — Favoritos (5 tests)
        └── export_tests.cy.js            # RHU06 — Exportación (5 tests)
```

---

## 4. Ejecución de las Pruebas

### 4.1 Asegurar que Odoo esté corriendo

```bash
docker ps | grep odoo
```

Si no está corriendo, iniciar el contenedor:
```bash
cd /home/david/Documents/univalle/software_quality/odoo
docker compose up -d
```

Esperar a que Odoo esté listo:
```bash
sleep 10 && curl -s -o /dev/null -w "%{http_code}" http://localhost:8069
# → 200
```

### 4.2 Ejecutar en modo interactivo (con navegador visible)

Abre la interfaz gráfica de Cypress para ver las pruebas ejecutarse en vivo:

```bash
npx cypress open
```

Pasos:
1. Seleccionar "E2E Testing"
2. Seleccionar el navegador (Chrome recomendado)
3. Hacer clic en el archivo de prueba deseado:
   - `black_box/search_tests.cy.js`
   - `black_box/filter_tests.cy.js`
   - `black_box/favorites_tests.cy.js`
   - `black_box/export_tests.cy.js`

### 4.3 Ejecutar en modo headless (sin interfaz gráfica)

Ejecutar todas las pruebas de caja negra:

```bash
npx cypress run --spec "cypress/e2e/black_box/**/*.cy.js"
```

Ejecutar un archivo específico:

```bash
npx cypress run --spec "cypress/e2e/black_box/search_tests.cy.js"
```

Ejecutar con navegador específico:

```bash
npx cypress run --browser chrome --spec "cypress/e2e/black_box/**/*.cy.js"
```

---

## 5. Captura de Resultados (Screenshots y Video)

### 5.1 Screenshots automáticos en fallos

Ya configurado en `cypress.json`:
```json
{
  "screenshotOnRunFailure": true,
  "screenshotsFolder": "cypress/screenshots"
}
```

Los screenshots se guardan en `cypress/screenshots/` con la ruta del archivo de prueba.

### 5.2 Screenshots explícitos en puntos específicos

Agregar dentro de cualquier test:
```javascript
cy.screenshot('nombre-de-captura');
```

Ejemplo para capturar la tabla pivote después de aplicar filtros:
```javascript
cy.get('.o_pivot').screenshot('pivot-despues-de-filtros');
```

### 5.3 Grabación de video de la ejecución

Activar video en `cypress.json`:
```json
{
  "video": true,
  "videoCompression": 32,
  "videosFolder": "cypress/videos"
}
```

Los videos se guardan en `cypress/videos/` con el nombre del archivo de prueba (ej: `search_tests.cy.js.mp4`).

**Opciones de compresión:**
- `videoCompression: 32` — calidad/media (por defecto)
- `videoCompression: 0` — sin compresión (máxima calidad)
- `videoCompression: 51` — máxima compresión (menor calidad)

**Solo grabar en fallos:**
En `cypress.config.js` (formato moderno):
```javascript
module.exports = defineConfig({
  video: true,
  videoUploadOnPasses: false,  // solo conserva video si falla
});
```

### 5.4 Ejecutar con captura completa

```bash
npx cypress run \
  --browser chrome \
  --spec "cypress/e2e/black_box/**/*.cy.js" \
  --config video=true,screenshotOnRunFailure=true
```

---

## 6. Cypress Dashboard (Grabación en la Nube)

Para grabar las pruebas en Cypress Dashboard (requiere cuenta gratuita):

### 6.1 Configurar proyecto

```bash
npx cypress open
```

Ir a la pestaña "Runs" → "Connect to Dashboard" → seguir las instrucciones.

### 6.2 Ejecutar con grabación en Dashboard

```bash
npx cypress run --record --key <TU_PROJECT_KEY>
```

El `project key` se obtiene al configurar el proyecto en Cypress Dashboard.

### 6.3 Beneficios de Dashboard

- Historial de ejecuciones
- Comparación entre runs
- Screenshots y video asociados a cada test
- Análisis de flakiness (pruebas inconsistentes)
- Integración CI/CD

---

## 7. Pruebas Específicas y lo que Validan

| Archivo | Tests | Técnica | HU |
|---------|-------|---------|----|
| `search_tests.cy.js` | 7 tests | PE + AVL | RHU02 |
| `filter_tests.cy.js` | 5 tests | PE + AVL | RHU03 |
| `favorites_tests.cy.js` | 5 tests | TD (3 fases) | RHU04 |
| `export_tests.cy.js` | 5 tests | TD (3 fases) | RHU06 |

### 7.1 Búsqueda (`search_tests.cy.js`)

| Test | Descripción | Técnica |
|------|-------------|---------|
| CP01 | "Adm" + autocomplete + 3 medidas | PE (CE-V14, CE-V10) |
| Cadena vacía | Todos los registros | AVL (frontera 0) |
| 1 carácter | Filtro mínimo | AVL (frontera inferior+1) |
| Especiales | "!@#$%" | PE (CE-V5) |
| Unicode | "José Martínez" | PE (CE-V6) |
| Alternancia | toggle medidas on/off | PE (CE-V12) |
| SQL Injection | "' OR 1=1 --" | PE (CE-I1) |

### 7.2 Filtros (`filter_tests.cy.js`)

| Test | Descripción | Técnica |
|------|-------------|---------|
| CP02 | Quotations + Last 365 Days + groupBy mes | PE + AVL |
| Toggle | Activar/desactivar filtro | PE (CE-V17) |
| Contradictorios | Quotations AND Sales Orders | AVL |
| 5 intervalos | year→quarter→month→week→day | PE (CE-V24 a CE-V28) |
| DOM timing | Actualización < 5s | AVL |

### 7.3 Favoritos (`favorites_tests.cy.js`)

| Test | Regla TD | Descripción |
|------|----------|-------------|
| CP03 | R2 | Privado + filtros + recargar |
| Compartido | R1 | Compartido + nombre válido |
| Nombre vacío | R4 | Error: nombre requerido |
| Nombre largo | R3 | Error: >256 caracteres |
| Sin filtros | — | Configuración limpia |

### 7.4 Exportación (`export_tests.cy.js`)

| Test | Regla TD | Descripción |
|------|----------|-------------|
| CP04 | R1 | Exportación exitosa, 3 medidas |
| Límite columnas | R4 | Error ≥16384 columnas |
| Sin medidas | R3 | Error: sin medidas activas |
| Estructura | R1 | Encabezados y totales |
| Nombre archivo | — | Sanitización del filename |

---

## 8. Interpretación de Resultados

### 8.1 Salida de consola (headless)

```
====================================================================================================

  (Run Starting)

  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ Cypress:    13.x.x                                                                             │
  │ Browser:    Chrome 1xx.x                                                                       │
  │ Specs:      4 found (black_box/search_tests.cy.js, black_box/filter_tests.cy.js, ...)          │
  └────────────────────────────────────────────────────────────────────────────────────────────────┘

──────────────────────────────────────────────────────────────────────────────────────────────────

  Running:  black_box/search_tests.cy.js                                                    (1 of 4)


  RHU02 — Búsqueda en Análisis de Flujo
    ✓ CP01 — Búsqueda por nombre "Adm" con autocompletado + selección de 3 medidas (12.3s)
    ✓ Búsqueda con cadena vacía (8.1s)
    ✓ Búsqueda con 1 carácter (7.5s)
    ✓ Búsqueda con caracteres especiales (6.2s)
    ✓ Búsqueda con caracteres Unicode (5.8s)
    ✓ Alternancia de medidas (9.4s)
    ✓ SQL Injection (5.1s)


  7 passing (54s)
```

### 8.2 Reporte JUnit (para CI/CD)

Agregar a `cypress.json`:
```json
{
  "reporter": "junit",
  "reporterOptions": {
    "mochaFile": "cypress/results/results-[hash].xml"
  }
}
```

### 8.3 Reporte HTML con Mochawesome

```bash
npm install --save-dev cypress-mochawesome-reporter
```

Configurar en `cypress/support/e2e.js`:
```javascript
import 'cypress-mochawesome-reporter/register';
```

Configurar en `cypress.json`:
```json
{
  "reporter": "cypress-mochawesome-reporter",
  "reporterOptions": {
    "reportDir": "cypress/reports",
    "overwrite": false,
    "html": true,
    "json": true
  }
}
```

---

## 9. Solución de Problemas Comunes

### Error: `cy.session` no está disponible

**Causa:** `cy.session()` requiere Cypress 9.6+ con comando `experimentalSessionAndOrigin`.
**Solución:** Agregar en `cypress.json`:
```json
{
  "experimentalSessionAndOrigin": true
}
```

### Error: No se encuentra el selector `.o_pivot`

**Causa:** La navegación no cargó correctamente la vista pivote.
**Solución:** Aumentar el timeout:
```json
{
  "defaultCommandTimeout": 20000
}
```

### Error: La descarga de XLSX no se completa

**Causa:** Cypress no maneja descargas de forma nativa en modo headless.
**Solución:** Usar el plugin `cypress-downloadfile` o verificar manualmente la carpeta `cypress/downloads/`.

### Error: Los tests de favoritos fallan al recargar

**Causa:** El nombre único del favorito ya existe de una ejecución anterior.
**Solución:** Los tests ya usan `Date.now()` para generar nombres únicos (ver `favorites_tests.cy.js`). Si persiste, limpiar los favoritos en Odoo: Ajustes → Técnico → Filtros → buscar `BB-Test-`.

---

## 10. Comandos Rápidos

```bash
# Instalar Cypress
npm install cypress --save-dev

# Abrir interfaz gráfica
npx cypress open

# Ejecutar todos los tests de caja negra (headless)
npx cypress run --spec "cypress/e2e/black_box/**/*.cy.js"

# Ejecutar con video y screenshots
npx cypress run --spec "cypress/e2e/black_box/**/*.cy.js" --config video=true

# Ejecutar un solo archivo
npx cypress run --spec "cypress/e2e/black_box/search_tests.cy.js"

# Ejecutar con navegador específico
npx cypress run --browser chrome --spec "cypress/e2e/black_box/**/*.cy.js"

# Ejecutar con reporte Mochawesome
npx cypress run --reporter mochawesome --spec "cypress/e2e/black_box/**/*.cy.js"
```
