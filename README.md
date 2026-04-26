<h1 align="center">Practias SE P2</h1>

<p align="center">
  <strong>Portafolio académico con dos proyectos independientes</strong><br>
  una experiencia web narrativa y un sistema experto forense de escritorio.
</p>

<p align="center">
  <img alt="Web" src="https://img.shields.io/badge/Proyecto%201-Fractured%20Mind-111827?style=for-the-badge">
  <img alt="Desktop" src="https://img.shields.io/badge/Proyecto%202-Proyecto%20Carmes%C3%AD-1f6feb?style=for-the-badge">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="JS" src="https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?style=for-the-badge&logo=javascript&logoColor=111">
</p>

---

## Visión General

Este repositorio reúne dos propuestas técnicas distintas, diseñadas para ejecutarse por separado:

- Fractured Mind: videojuego narrativo web de investigación psicológica.
- Proyecto Carmesí: sistema experto en Python con interfaz gráfica y aprendizaje incremental.

No comparten runtime ni dependencias directas. Cada carpeta representa un entregable autónomo.

---

## Navegación Rápida

- Proyecto web: Fractured Mind/index.html
- README interno del webgame: Fractured Mind/README.md
- Proyecto desktop Python: Proyecto Carmesí/main.py

---

## Tabla de Contenidos

1. Arquitectura del repositorio
2. Proyecto 1: Fractured Mind
3. Proyecto 2: Proyecto Carmesí
4. Requisitos y dependencias
5. Puesta en marcha
6. Criterios de calidad para entrega
7. Créditos

---

## Arquitectura del Repositorio

```text
Practias SE P2/
├─ Fractured Mind/
│  ├─ index.html
│  ├─ README.md
│  ├─ assets/
│  ├─ css/
│  └─ js/
└─ Proyecto Carmesí/
   ├─ main.py
   ├─ motor_inferencia.py
   ├─ narrativa.py
   ├─ expedientes.py
   ├─ interrogatorio.py
   ├─ asesinos.json
   └─ assets/
```

---

## Proyecto 1: Fractured Mind

### Concepto

Experiencia interactiva en la que el jugador reconstruye un caso a partir de pistas fragmentadas, elige culpable/arma/lugar y recibe una revelación final.

### Stack técnico

- HTML5
- CSS3
- JavaScript (vanilla)

### Entradas clave

- Inicio del proyecto: Fractured Mind/index.html
- Configuración narrativa: Fractured Mind/js/data.js
- Flujo de juego: Fractured Mind/js/game.js
- Capa de UI: Fractured Mind/js/ui.js

---

## Proyecto 2: Proyecto Carmesí

### Concepto

Aplicación de escritorio que ejecuta un sistema experto forense basado en preguntas por rasgos y filtrado de candidatos, con opción de aprendizaje para registrar nuevos casos.

### Stack técnico

- Python 3.13+
- customtkinter
- pillow
- pygame

### Entradas clave

- Inicio del proyecto: Proyecto Carmesí/main.py
- Motor de inferencia: Proyecto Carmesí/motor_inferencia.py
- Banco narrativo de preguntas: Proyecto Carmesí/narrativa.py
- Módulo de expedientes: Proyecto Carmesí/expedientes.py
- Flujo alternativo de consola: Proyecto Carmesí/interrogatorio.py

---

## Requisitos y Dependencias

### Requisitos generales

- Git
- Navegador moderno (Chrome, Edge o Firefox)
- Python 3.13 o superior

### Dependencias Python (solo Proyecto Carmesí)

```bash
pip install customtkinter pillow pygame
```

---

## Puesta en Marcha

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd "Practias SE P2"
```

### 2. Ejecutar Fractured Mind

Opción rápida:

```text
Abrir Fractured Mind/index.html en el navegador
```

Opción recomendada (servidor local):

```bash
cd "Fractured Mind"
python -m http.server 5500
```

Abrir en navegador:

```text
http://localhost:5500
```

### 3. Ejecutar Proyecto Carmesí

```bash
cd "Proyecto Carmesí"
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install customtkinter pillow pygame
```

Iniciar aplicación:

```bash
python main.py
```


---

## Créditos

Autora: Kenya Gabriela Frutos González.
