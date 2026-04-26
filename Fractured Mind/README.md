# Fractured Mind

<p align="center">
  <strong>Thriller psicológico interactivo</strong><br>
  Una investigación fragmentada entre recuerdos, pistas y una única acusación.
</p>

<p align="center">
  <img alt="HTML5" src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
  <img alt="CSS3" src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
  <img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-1F2937?style=for-the-badge&logo=javascript&logoColor=F7DF1E">
  <img alt="Estado" src="https://img.shields.io/badge/Estado-Estable-2E7D32?style=for-the-badge">
</p>

---

## Tabla de Contenidos

1. [Qué Es Dae's Fractured Mind](#qué-es-fractured-mind)
2. [Highlights](#highlights)
3. [Demo Local En 60 Segundos](#demo-local-en-60-segundos)
4. [Arquitectura Del Proyecto](#arquitectura-del-proyecto)
5. [Flujo Narrativo y Mecánica](#flujo-narrativo-y-mecánica)
6. [Playbook De Personalización](#playbook-de-personalización)
7. [Guía Para Agregar Un Nuevo Sospechoso](#guía-para-agregar-un-nuevo-sospechoso)
8. [Calidad y Mantenimiento](#calidad-y-mantenimiento)
9. [Troubleshooting](#troubleshooting)
10. [Roadmap](#roadmap)
11. [Créditos y Licencia](#créditos-y-licencia)

---

## Qué Es Dae's Fractured Mind

Dae's Fractured Mind es una experiencia narrativa de misterio psicológico donde el jugador, en rol de agente, reconstruye un caso a través de recuerdos rotos de Dae.

Cada partida sortea de forma aleatoria una combinación real de:
- Culpable
- Arma
- Locación

Con base en pistas y narrativa contextual, el jugador emite una única acusación. El sistema compara su elección contra la verdad del caso y despliega una revelación final.

---

## Highlights

- Arquitectura simple y mantenible con HTML, CSS y JavaScript puro
- Navegación por pantallas sin framework
- Contenido narrativo centralizado y extensible
- Integración de audio por fase narrativa
- Flujo claro de gameplay: Pistas -> Acusación -> Revelación
- Base ideal para prácticas de storytelling interactivo

---

## Demo Local En 60 Segundos

### Opción A: Abrir directamente

1. Abre el proyecto en tu editor.
2. Ejecuta `index.html` en el navegador.

### Opción B: Servidor local (recomendado)

Usa cualquier servidor estático para evitar posibles restricciones del navegador con recursos locales.

Ejemplo con Python:

```bash
python -m http.server 5500
```

Luego abre:

```text
http://localhost:5500
```

---

## Arquitectura Del Proyecto

```text
Fractured Mind/
├─ index.html
├─ README.md
├─ assets/
│  ├─ backgrounds/
│  ├─ characters/
│  │  ├─ dakho/
│  │  ├─ ethan/
│  │  ├─ pax/
│  │  ├─ sterling/
│  │  └─ xion/
│  ├─ items/
│  └─ music/
├─ css/
│  └─ styles.css
└─ js/
   ├─ data.js
   ├─ ui.js
   └─ game.js
```

### Responsabilidad por archivo

#### js/data.js

Fuente única de verdad para datos narrativos y catálogo del juego.

Define:
- Sospechosos, armas y locaciones
- Pistas por categoría
- Historias de revelación
- Openers de Sterling
- Rutas de audio
- Estado global de partida compartido entre módulos

#### js/ui.js

Capa de interfaz y navegación.

Gestiona:
- Cambio de pantallas
- Música por fase
- Retrato lateral de personaje
- Barra de progreso
- Render de tarjetas de información

#### js/game.js

Capa de mecánica y reglas.

Controla:
- Sorteo del caso
- Construcción de pistas
- Selección de acusación
- Validación de resultado
- Construcción de revelación final

#### index.html

Estructura de todas las pantallas y contenedores globales.

Importante: orden de carga de scripts
1. js/data.js
2. js/ui.js
3. js/game.js

---

## Flujo Narrativo y Mecánica

1. Login de agente.
2. Portada con accesos a lore e información.
3. Inicio de caso con sorteo aleatorio.
4. Exposición de evidencias narrativas.
5. Acusación de culpable, arma y locación.
6. Revelación de la verdad y comparación de resultados.

### Regla central

La victoria perfecta ocurre solo si se acierta la triple coincidencia:

$$
acierto = (culpable) \land (arma) \land (locacion)
$$

---

## Playbook De Personalización

### 1) Modificar contenido narrativo

Editar en js/data.js:
- SUSPECTS
- WEAPONS
- LOCATIONS
- STORIES
- CLUES_BY_WEAPON
- CLUES_BY_LOC
- CLUES_BY_CULPRIT
- STERLING_OPENERS

### 2) Cambiar arte y audio

Editar rutas en js/data.js y validar archivos en assets.

### 3) Ajustar dificultad

Editar en js/game.js:
- Estrategia de armado de pistas en `buildClues`
- Orden o ruido de evidencias
- Mensajería de feedback final

### 4) Ajustar UX del flujo

Editar en js/ui.js:
- Reglas de `goTo`
- Mostrar u ocultar retrato por pantalla
- Progreso narrativo y textos de navegación

---

## Guía Para Agregar Un Nuevo Sospechoso

Checklist mínimo para evitar inconsistencias:

1. Agregar objeto en SUSPECTS con `id` único.
2. Agregar retratos en assets/characters/<id>/.
3. Agregar entrada correspondiente en STORIES.
4. Agregar entrada en CLUES_BY_CULPRIT.
5. Agregar entrada en STERLING_OPENERS.
6. Verificar que no haya typo en ids cruzados.

### Ejemplo conceptual

Si creas `id: "nova"`, deben existir:
- STORIES.nova
- CLUES_BY_CULPRIT.nova
- STERLING_OPENERS.nova

---

## Calidad y Mantenimiento

### Convenciones sugeridas

- IDs cortos y estables en minúscula
- Rutas relativas limpias
- Separación estricta entre datos, UI y mecánica
- Comentarios breves en bloques con lógica no evidente

### Criterios de revisión antes de publicar cambios

1. El juego inicia sin errores de consola.
2. Carga de imágenes correcta en todas las pantallas.
3. Audio transiciona entre menú, investigación y revelación.
4. La acusación exige los 3 campos.
5. La revelación refleja con precisión el caso sorteado.

---

## Troubleshooting

### No se reproduce la música

Motivo común: autoplay bloqueado por navegador.

Acción:
- Hacer click en la página para habilitar audio.

### No carga una imagen

Acción:
- Revisar ruta en js/data.js
- Verificar nombre real del archivo y mayúsculas/minúsculas

### Error tras agregar nuevo personaje

Acción:
- Validar mapeo completo del id en STORIES, CLUES_BY_CULPRIT y STERLING_OPENERS

### No cambia de pantalla

Acción:
- Confirmar que el id de pantalla existe en index.html
- Revisar llamadas a goTo con ids correctos

---

## Roadmap

- Sistema de casos curados con narrativa ramificada
- Persistencia de estadísticas por jugador
- Modo difícil con pistas ambiguas
- Panel de configuración de partida
- Internacionalización de textos
- Suite de pruebas para lógica de selección y revelación

---

## Créditos

Proyecto de práctica narrativa interactiva basado en assets locales y lógica vanilla JS.

Historia totalmente original de la creadora de la practica.

Autora: Kenya Gabriela Frutos González.

---

## Anexo: Mapa Rápido De Pantallas

- s-login: acceso inicial
- s-title: portada y menú principal
- s-intro: lore y contexto del caso
- s-cast: catálogo de personajes, armas y locaciones
- s-clues: expediente y evidencias
- s-accuse: selección de culpable/arma/lugar
- s-reveal: veredicto y cierre narrativo
