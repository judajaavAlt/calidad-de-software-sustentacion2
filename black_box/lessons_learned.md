# Lecciones Aprendidas — Pruebas Funcionales de Caja Negra
## Ingeniero de Pruebas Funcionales — Módulo Ventas/Informes Odoo 19.0

---

### Lección 1: Las Tablas de Decisión Revelan Lógica Oculta que las Pruebas Ad-Hoc No Perciben

Durante la construcción de la Tabla de Decisión de 3 fases para RHU04 (Guardar Búsquedas Favoritas), el proceso de expansión 2^4 = 16 combinaciones reveló que las condiciones C2 (nombre ingresado) y C3 (longitud ≤ 256) tienen una dependencia lógica que no es obvia en una inspección superficial del código. Específicamente, cuando C2 = N (no hay nombre), la condición C3 no puede evaluarse físicamente, generando 4 combinaciones imposibles (R13-R16). Una estrategia de pruebas ad-hoc podría haber incluido casos redundantes o, peor aún, haber omitido completamente el escenario de nombre vacío, asumiendo incorrectamente que el sistema siempre valida ambos campos de forma independiente. Las TD formales obligan al ingeniero a pensar en todas las combinaciones, incluyendo las imposibles, lo que fuerza una comprensión más profunda del dominio.

**Recomendación:** Incorporar Tablas de Decisión en el proceso de diseño de pruebas para cualquier funcionalidad con 3 o más condiciones booleanas interrelacionadas. El costo de construir la tabla es bajo comparado con el riesgo de omitir una combinación crítica.

---

### Lección 2: Los Límites Reales del Sistema Están en el Código, No en la Documentación

El análisis de Valor Límite para RHU06 reveló una discrepancia crítica entre lo que la documentación de Odoo sugiere y lo que el código realmente implementa. El límite de 16,384 columnas para exportación XLSX no está documentado en la interfaz de usuario ni en la ayuda contextual; solo es visible al leer `pivot_renderer.js:259`. Del mismo modo, el límite de 32,767 caracteres por celda y 1,048,576 filas están definidos en `export.py` pero no son accesibles para el usuario final. Esto significa que un usuario podría configurar una tabla pivote con muchas columnas y recibir un error silencioso (NC-01) sin entender por qué.

**Recomendación:** Como ingeniero de pruebas, leer el código fuente no es opcional — es el único artefacto que contiene la verdad sobre los límites y validaciones del sistema. La documentación funcional y las historias de usuario rara vez especifican estos límites técnicos, y es responsabilidad del QA descubrirlos mediante análisis de código.

---

### Lección 3: Automatizar Flujos Dinámicos (Tablas Pivote y Descargas) Requiere un Enfoque Híbrido

La automatización de la tabla pivote de Odoo presentó desafíos únicos que no se encuentran en formularios o listas estáticas. Específicamente:
- La tabla pivote se renderiza asíncronamente mediante RPC, por lo que los selectores DOM no están disponibles inmediatamente después de la navegación.
- El botón de descarga XLSX dispara una descarga de archivo binario que Cypress no intercepta de forma nativa en modo headless sin plugins adicionales (`cy.readFile` requiere conocer el nombre exacto del archivo).
- Los cambios de filtro disparan re-renderizados completos de la tabla, lo que puede invalidar referencias anteriores a elementos del DOM.

**Recomendación:** Para flujos dinámicos como tablas pivote, adoptar un enfoque híbrido:
1. Usar esperas explícitas basadas en elementos del DOM (no `cy.wait()` fijos) para sincronización
2. Combinar pruebas E2E (Cypress) con pruebas de integración de API (REST) para verificar la capa de datos independientemente del renderizado
3. Para verificación de descargas, usar un plugin de Cypress como `cy-verify-downloads` o validar via HTTP intercept

---

### Lección 4: Las Particiones de Equivalencia Son Poderosas, Pero su Cobertura Real Depende del Contexto de Ejecución

En el diseño de PE para RHU02, identificamos 8 clases de equivalencia para el input de búsqueda. Sin embargo, durante la implementación, descubrimos que:
- La clase "SQL Injection" (CE-I1) no puede ser validada realmente desde Cypress porque el ORM de Odoo sanitiza la entrada antes de que llegue a la base de datos. Una prueba E2E solo puede verificar que la inyección no rompe la UI, no que efectivamente fue prevenida.
- La clase "Unicode" depende de la configuración del charset de la base de datos PostgreSQL, que varía entre instalaciones.
- La clase "Longitud extrema" (>32767 caracteres) no puede ser tipeada en un campo de búsqueda estándar porque el navegador trunca la entrada antes de enviarla al servidor.

**Recomendación:** Las PE deben complementarse con un análisis de "factibilidad de automatización" antes de comprometerse a implementar cada clase. Para aquellas que no son automatizables en E2E, documentar como "verificación manual" o "prueba de integración" en otro nivel de la pirámide de pruebas.

---

### Lección 5: El Valor del Informe de Pruebas No Está en los Números, Sino en las Decisiones que Habilita

Al construir el informe de pruebas, observamos que los indicadores cuantitativos (%CEE = 90%, EDP = 5%) son útiles pero no cuentan la historia completa. El verdadero valor del informe está en:
1. **La priorización:** NC-01 es un solo defecto, pero es crítico porque afecta la confianza del usuario en la exportación de datos — una operación que puede ocurrir semanal o diariamente en un negocio.
2. **La trazabilidad:** La MRP permite rastrear cada caso de prueba hasta un requerimiento de negocio, demostrando que el 100% de los requerimientos funcionales tienen cobertura.
3. **La acción:** La recomendación de corregir NC-01 antes de producción es clara y está respaldada por datos (el error es silencioso, el límite de 16384 columnas es real, el código fuente lo confirma).

**Recomendación:** Un informe de pruebas debe responder tres preguntas para quien toma decisiones: (1) ¿Pasa o falla? (2) ¿Qué tan grave es? (3) ¿Qué hacemos al respecto? Si el informe no habilita una decisión clara, es ruido. Si lo hace, es el artefacto más valioso que produce el equipo de QA.
