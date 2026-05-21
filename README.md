# 🤖 RAG Multimodal Assistant – Prueba Técnica IA

## Descripción

Este proyecto consiste en la construcción de un sistema RAG (Retrieval-Augmented Generation) multimodal capaz de procesar documentos PDF técnicos que contienen:

* Texto
* Diagramas
* Imágenes
* Esquemas

El sistema permite realizar preguntas en lenguaje natural y generar respuestas contextualizadas utilizando información extraída desde documentos técnicos junto con referencias visuales asociadas.

La solución fue desarrollada utilizando Python, Streamlit, OpenAI, ChromaDB y PyMuPDF.

---

# Arquitectura de la solución

El flujo general del sistema sigue una arquitectura RAG dividida en tres etapas:

## 1. Ingesta y procesamiento

Archivo principal:

`ingest.py`

Funciones implementadas:

* Lectura de documentos PDF
* Extracción de texto usando PyMuPDF (Fitz)
* Extracción automática de imágenes
* Generación de metadatos:

  * documento
  * página
  * imágenes asociadas
* Chunking de texto
* Generación de embeddings
* Indexación en ChromaDB

Proceso:

PDF → extracción → chunks → embeddings → vector DB

---

## 2. Recuperación (Retrieval)

Cuando el usuario realiza una pregunta:

1. Se genera embedding de la consulta
2. Se consulta ChromaDB
3. Se recuperan los fragmentos más cercanos semánticamente
4. Se obtienen metadatos:

   * documento
   * página
   * imágenes relacionadas

---

## 3. Generación

Archivo principal:

`app.py`

Se utiliza OpenAI para:

* interpretar la pregunta
* combinar el contexto recuperado
* responder con lenguaje natural
* usar conocimiento general cuando el documento no sea suficiente

El sistema incluye un prompt diseñado para:

* priorizar información del documento
* responder preguntas básicas
* evitar respuestas vacías
* entregar explicaciones útiles

---

# Tecnologías utilizadas

## Backend

* Python
* Streamlit
* OpenAI API
* ChromaDB

## Procesamiento de documentos

* PyMuPDF (fitz)

## Embeddings

* OpenAIEmbeddings

## Motor RAG

* LangChain

## Base vectorial

* ChromaDB

---

# Decisiones técnicas

Durante el desarrollo se tomaron las siguientes decisiones:

### ChromaDB

Se eligió por:

* implementación simple
* persistencia local
* rápida integración con LangChain

### OpenAI Embeddings

Permiten búsqueda semántica precisa para documentos técnicos.

### Streamlit

Se eligió para construir rápidamente una interfaz tipo chat sin requerir frontend adicional.

### Chunking

Se utilizó:

* chunk_size=500
* chunk_overlap=100

Esto mejora el contexto y reduce pérdida de información entre secciones.

### Selección de imágenes

Las imágenes extraídas se relacionan mediante metadatos por documento y página.

Debido a que algunos PDFs contienen múltiples diagramas por página, el sistema intenta seleccionar la referencia visual más cercana disponible.

---

# Cómo ejecutar el proyecto

## 1. Clonar repositorio

```bash
git clone https://github.com/madronoagularjaaja-sudo/rag-arduino-system.git
```

## 2. Entrar al proyecto

```bash
cd rag-arduino-system
```

## 3. Crear entorno virtual

Recordar tener Python instalado
```bash
python -m venv .venv
```

Activar:

Windows:

```bash
.venv\Scripts\activate
```

---

## 4. Instalar dependencias

Puede tardar unos minutos ya que son varias dependencias.
```bash
pip install -r requirements.txt
```

---

## 5. Crear archivo .env

La api key la paso por privado solo para la prueba
```env
OPENAI_API_KEY=tu_api_key
```

---

## 6. Agregar PDFs

Ubicar documentos dentro de:
Paso el pdf que usé tambien al privado con el fin de llevar un mismo control y prueba
```
Crear las carpetas data/pdfs/
```
Dentro de pdfs colocar el PDF👆
---

## 7. Procesar documentos

```bash
python ingest.py
```

---

## 8. Ejecutar aplicación

```bash
streamlit run app.py
```
Por último cuando se inicia el ambiante se da enter o alguna tecla cuando esté ya montado en la URL.
---

# Ejemplos de preguntas y respuestas

Preguntas utilizadas durante las pruebas funcionales del sistema:

### ¿Qué es Raspberry Pi?

Respuesta esperada:

Explicación general del dispositivo, propósito, arquitectura y usos.

---

### ¿Qué es el navegador web Chromium?

Respuesta esperada:

Descripción del navegador, funcionalidades principales y relación con Raspberry Pi OS.

---

### ¿Qué gestor de archivos utiliza Raspberry Pi?

Respuesta esperada:

Explicación sobre la herramienta utilizada para navegación y administración de archivos.

---

### ¿Cómo puedo apagar correctamente el sistema Raspberry Pi?

Respuesta esperada:

Proceso recomendado para apagar el sistema de forma segura evitando corrupción de datos.

---

### ¿Qué es la interfaz Scratch 3?

Respuesta esperada:

Descripción del entorno visual de programación y sus usos educativos.

---

### ¿Cuál es el entorno Thonny Python IDE?

Respuesta esperada:

Explicación del IDE utilizado para programación en Python dentro de Raspberry Pi.

---

### ¿Qué son los bucles en programación?

Respuesta esperada:

Definición conceptual y ejemplos básicos.

---

### Quiero las especificaciones de Raspberry Pi

Respuesta esperada:

Resumen de características técnicas y componentes principales.

---

# Posibles mejoras futuras

* OCR avanzado
* Layout-aware chunking
* asociación texto-imagen mediante bounding boxes
* soporte múltiples documentos simultáneos
* despliegue cloud
* integración FastAPI

---

# Autor

Sebastián Santos

Prueba Técnica — Departamento de Inteligencia Artificial
