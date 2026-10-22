# Memoria Continua del Proyecto

## Lecciones Aprendidas (Mejora Continua)
- *2026-10-22*: Inicialización del proyecto de econometría urbana y análisis institucional. Mantener modularidad estricta en `/src`, estándares PEP8, sin dependencias no declaradas y asegurar reproducibilidad estadística.
- Regla de Fuentes Oficiales Más Recientes (Banco de España Informe Anual 2025/2026): El déficit acumulado de vivienda según la última presentación oficial de David López Salido (18 de junio de 2026) asciende exactamente a **750.000 viviendas** (diferencial acumulado 2021-2025 de -3,9% de hogares promedio). Nunca usar estimaciones preliminares obsoletas (450k) cuando existe el dato consolidado oficial de 750k.
- Regla de Gráficos Limpios (Zero-Clutter Visuals): NUNCA colocar cajas de texto flotantes (`bbox`) sobre el área de datos de los gráficos, ya que tapan barras, líneas y etiquetas. Las explicaciones deben residir exclusivamente en el texto del informe. El gráfico debe ser autoexplicativo, diáfano y minimalista (estilo gráfico del Banco de España / Financial Times).
- Regla del Esfuerzo de Compra (BdE Diapositiva 43): El esfuerzo salarial en Málaga, Madrid y Barcelona para hogares en alquiler alcanza los **10 años de renta neta** (frente al promedio nacional de 4 años para propietarios).
- Regla del Parque Público (BdE Diapositiva 48): El parque público en España es de solo el **1,5%** (1 de cada 65 viviendas), frente al 34,1% de Países Bajos o 14,0% de Francia.
- Metodología de Déficit BdE (Slide 29): Suma 2021-2025 de la diferencia acumulada entre viviendas residenciales terminadas y creación neta de hogares.
- Regla Anti-Estilo IA:
  1. No abusar de la negrita (`**`) indiscriminada; mantener tono sobrio, técnico y académico.
  2. Prohibido el uso de em dashes (`—`). Utilizar guiones simples `-` o comas.
  3. No usar `\overline{Texto}` en LaTeX (genera barras flotantes erróneas en KaTeX); definir la variable limpia (ej. $S = 95\text{ m}^2$).
  4. Evitar sombreros anidados en fórmulas inline (`\hat{\epsilon}_s^{PGOU}`); usar notación estándar y limpia (`\epsilon_s = 0.31`).
  5. Tablas de regresión limpias sin backticks (`` ` ` ``) dentro de las celdas de datos.
  6. Mensajes de git commit humanos, profesionales y sintéticos, sin sonar a plantilla de agente.
  7. Hilo narrativo continuo: El informe y README integran las figuras en orden cronológico argumental (Figura 7 -> Mecanismo -> Figuras 1 y 5 -> Figura 2 -> Figuras 3 y 4 -> Figura 6 -> Hoja de ruta).
  8. Coherencia cromática unificada: Todas las figuras (1 a 7) comparten la paleta institucional (`#BE123C` Carmesí statu quo/anomalía, `#0D9488` Teal By-Right/reforma, `#D97706` Ámbar costes/turismo, `#1E3A8A` Azul marino benchmark europeo).

## Actualidad (Estado y Roadmap Activo)
- [x] **Calibración Oficial Banco de España 2025/2026**: Integrado el dato de **750.000 viviendas** de déficit acumulado 2021-2025 (-3,9% de los hogares promedio) y los 10 años de esfuerzo salarial para inquilinos en grandes ciudades (David López Salido, 18 de junio de 2026).
- [x] **Unificación Cromática Total (Figuras 1 a 7)**:
  - Establecido sistema de color institucional en `/src/visualization.py`, `/src/european_benchmark.py` y `/src/monte_carlo_policy.py`.
  - Regeneradas todas las figuras a 300 DPI con estética minimalista de publicación financiera.
- [x] **Reestructuración Narrativa del README y Documentación**:
  - Hilo narrativo académico fluido que guía al lector a través de la investigación.
  - Figuras embebidas progresivamente en su sección correspondiente.
  - Eliminados artefactos tipográficos (`\overline`, `\hat{\epsilon}`, em dashes y backticks en tablas).
