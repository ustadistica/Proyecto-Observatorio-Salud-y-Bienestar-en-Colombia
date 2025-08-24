# Informe de Viabilidad – Datasets BDUA (Afiliación al Sistema de Salud)

## Descripción del Proyecto
Proyecto colaborativo orientado al análisis de datos abiertos en el ámbito de la salud y el bienestar, con énfasis en el régimen de salud en Colombia. Su propósito es identificar, documentar y evaluar información estratégica relacionada con la afiliación al sistema de salud, la prestación de servicios y la vigilancia de eventos de interés en salud pública.

---

## 1. Introducción y Descripción General
El **sistema de salud colombiano** se organiza bajo dos regímenes principales: **contributivo** (personas que cotizan al sistema por su vínculo laboral o capacidad de pago) y **subsidiado** (personas que acceden al sistema a través de subsidios estatales, generalmente por su situación de vulnerabilidad económica y social).  

La **Base de Datos Única de Afiliados (BDUA)** es la fuente oficial que consolida y administra la información de todos los afiliados al sistema, tanto del régimen contributivo como del subsidiado. Esta base permite:  

- Conocer la cobertura poblacional del sistema de salud.  
- Caracterizar a los afiliados según edad, género, territorio y condición socioeconómica.  
- Analizar inequidades en la afiliación y en el acceso a servicios.  

En este informe se revisa la **viabilidad de uso de dos conjuntos de datos oficiales de la BDUA**, identificando sus fortalezas, limitaciones y usos potenciales dentro del **Observatorio de Salud y Bienestar**.  

---

## 2. Detalle de los Datasets

### Dataset 1: BDUA – Régimen Contributivo  
**Descripción:**  
Contiene el listado de afiliados al sistema de salud bajo el régimen contributivo, con variables demográficas y administrativas.  

- **Frecuencia de actualización:** Mensual (según el Ministerio de Salud).  
- **Columnas relevantes:**  
  - Género  
  - Grupo etario  
  - Código de EPS  
  - Nombre de la entidad (EPS)  
  - Régimen (Contributivo, subsidiado)  
  - Tipo de afiliado (Cotizante, Beneficiario, Adicional, Cabeza de Familia)  
  - Estado de afiliado (Activo, Retirado, Fallecido, Suspendido, Protección Laboral)  
  - Condición del beneficiario (Discapacidad, Escolaridad, Vacío)  
  - Zona de afiliación (rural, urbana)  
  - Departamento  
  - Municipio  
  - Cantidad de registros  

- **Calidad de los datos:**  
  - *Fortalezas:* Cobertura nacional, granularidad por municipio, permite análisis detallados por EPS y tipo de afiliado.  
  - *Retos:* Posibles inconsistencias en estados de afiliado (ej. personas fallecidas aún como activas), duplicados por migraciones de EPS y diferencias en codificación de variables.  

- **Vía de acceso:**  
  [Portal de Datos Abiertos – Régimen Contributivo](https://www.datos.gov.co/Salud-y-Protecci-n-Social/Poblaci-n-Base-de-Datos-nica-de-Afiliados-BDUA-del/tq4m-hmg2)  (API y descarga directa)

---

### Dataset 2: BDUA – Régimen Subsidiado  
**Descripción:**  
Contiene el listado de afiliados al régimen subsidiado, con variables similares al contributivo y adicionalmente información socioeconómica del Sisbén.  

- **Frecuencia de actualización:** Mensual.  
- **Columnas relevantes (además de las anteriores):**  
  - Nivel del Sisbén (I, II, III, IV, N).  
  - Grupo poblacional del afiliado (Habitante de la calle, Población Infantil Vulnerable, Programa en protección a testigos, etc).  

- **Calidad de los datos:**  
  - *Fortalezas:* Información clave para la caracterización socioeconómica y la identificación de población en condiciones de vulnerabilidad.  
  - *Retos:* Inconsistencias en asignación de nivel Sisbén, campos vacíos en condición del beneficiario y posibles rezagos en la actualización por municipio.  

- **Vía de acceso:**  
  [Portal de Datos Abiertos – Régimen Subsidiado](https://www.datos.gov.co/Salud-y-Protecci-n-Social/Poblaci-n-Base-de-Datos-nica-de-Afiliados-BDUA-del/d7a5-cnra)  (API y descarga)
---

## 3. Análisis Preliminar
- **Cobertura:** Ambos datasets son de alto valor estratégico, ya que consolidan prácticamente toda la población afiliada al sistema de salud.  
- **Comparabilidad:** La estructura es similar, lo que permite hacer cruces entre contributivo y subsidiado para analizar inequidades y diferencias por régimen.  
- **Potenciales usos en el Observatorio:**  
  - Estimación de la población cubierta por EPS y régimen.  
  - Distribución demográfica (género, edad, rural/urbano).  
  - Caracterización socioeconómica de afiliados subsidiados (Sisbén).  
  - Identificación de brechas territoriales en afiliación y acceso.  
  - Apoyo a la formulación de políticas públicas en salud y equidad social.  

---

## 4. Informe de Viabilidad
- **Factibilidad de uso:** Alta 

- **Justificación:**  
  Los datasets de la BDUA son una fuente oficial, confiable y de acceso abierto que permite construir indicadores robustos sobre cobertura y equidad en el sistema de salud colombiano. Su carácter nacional y actualización mensual los convierten en un insumo estratégico para la toma de decisiones.  

- **Recomendaciones para su uso:**  
  1. **Incluir ambos datasets** como insumo principal del Observatorio de Salud y Bienestar.  
  2. **Documentar un diccionario de variables**, especialmente para valores no estandarizados y codificaciones inconsistentes.  
  3. **Establecer un proceso de limpieza de datos:**  
     - Revisión de datos faltantes y duplicados.  
     - Validación de códigos de departamento y municipio.  
     - Verificación de coherencia en estados de afiliados (ej. fallecidos como activos).  
  4. **Cruzar la información contributivo vs. subsidiado**, con el fin de identificar inequidades y diferencias territoriales.  
  5. **Diseñar visualizaciones y tableros de control** que permitan monitorear la evolución de la afiliación por región, EPS y grupo poblacional.  

En conclusión, la BDUA constituye una **base sólida y viable** para el análisis de la afiliación al sistema de salud en Colombia, con un enorme potencial para fortalecer el Observatorio en términos de evidencia, análisis comparativo y generación de recomendaciones de política pública.  
