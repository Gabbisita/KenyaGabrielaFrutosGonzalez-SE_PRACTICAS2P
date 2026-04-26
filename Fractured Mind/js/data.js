
// ==============================
// CONFIGURACION NARRATIVA DEL JUEGO
// ==============================
//
// Este archivo contiene TODO el contenido editable del caso:
// - Sospechosos
// - Armas
// - Locaciones
// - Musica
// - Historias y pistas
//
// Si quieres crear variantes del juego, normalmente solo necesitas
// modificar este archivo y mantener los IDs coherentes entre secciones.

// Lista de sospechosos disponibles para sorteo y para la pantalla de acusacion.
// Campos clave:
// - id: identificador interno (debe ser unico y estable)
// - expressions: rutas de imagen usadas por distintas pantallas
const SUSPECTS = [
    { id: 'pax', name: 'Pax Vanderbilt', alias: 'El Novio Celoso', color: '#C41E3A', icon: '♦', desc: 'Novio de Dae. Posesivo. Capaz de cualquier cosa. Pax llegó a su vida como una tormenta disfrazada de calma. Pero debajo de esa fachada latía algo oscuro: la incapacidad de amar sin poseer.', expressions: { default: 'assets/characters/pax/neutral.png', clue: 'assets/characters/pax/obsesivo.png', accuse: 'assets/characters/pax/enojado.png', reveal: 'assets/characters/pax/preocupado.png' } },
    { id: 'eth', name: 'Ethan Blackwood', alias: 'El Amigo Cínico', color: '#2d9c8a', icon: '♠', desc: 'Mejor amigo de Dae. Sarcástico. Enamorado en silencio. Construyó su personalidad como una armadura. Nadie podía herirlo si nadie llegaba cerca. Excepto Dae.', expressions: { default: 'assets/characters/ethan/neutral.png', clue: 'assets/characters/ethan/sonriente.png', accuse: 'assets/characters/ethan/pensativo.png', reveal: 'assets/characters/ethan/preocupado.png' } },
    { id: 'dak', name: 'Dakho Belmont', alias: 'El Profesor Prohibido', color: '#9b5de5', icon: '♣', desc: 'Profesor de Dae. Seductor. Padre de Xion. Impartía ética pero cruzó cada línea que juró no cruzar. Su relación con Dae fue el catalizador de todo el desastre.', expressions: { default: 'assets/characters/dakho/neutral.png', clue: 'assets/characters/dakho/sonriente.png', accuse: 'assets/characters/dakho/neutral.png', reveal: 'assets/characters/dakho/preocupado.png' } },
    { id: 'xio', name: 'Xion Kravitz', alias: 'La Chispa del Caos', color: '#c9a84c', icon: '♥', desc: 'Hijo de Dakho. Nuevo en el instituto. Novio final de Dae. Llegó sin saber nada de la historia previa, convirtiéndose en el detonador perfecto del conflicto.', expressions: { default: 'assets/characters/xion/neutral.png', clue: 'assets/characters/xion/sonriente.png', accuse: 'assets/characters/xion/avergonzado.png', reveal: 'assets/characters/xion/preocupado.png' } },
    { id: 'dar', name: 'Darren Sterling', alias: 'Psiquiatra Jefe', color: '#5c9e6e', icon: '★', desc: '¿Busca la verdad o la construye? El hombre que sostiene los fragmentos de la mente de Dae. Sus intenciones son tan profundas como el hospital que dirige.', expressions: { default: 'assets/characters/sterling/neutral.png', clue: 'assets/characters/sterling/analitico.png', accuse: 'assets/characters/sterling/siniestro.png', reveal: 'assets/characters/sterling/preocupado.png' } }
];

// Lista de armas posibles. El id se cruza con CLUES_BY_WEAPON.
const WEAPONS = [
    { id: 'farm', name: 'Fármaco', icon: '⬡', img: 'assets/items/farmaco.png', desc: 'Una dosis letal de sedantes que nublaron los sentidos de Dae.' },
    { id: 'nota', name: 'Nota', icon: '✉', img: 'assets/items/nota.png', desc: 'Un trozo de papel con una confesión que nunca debió leerse.' },
    { id: 'bist', name: 'Bisturí', icon: '◆', img: 'assets/items/bisturi.png', desc: 'Frío, preciso y profesional. Un corte que cambió todo.' },
    { id: 'cuer', name: 'Cuerda', icon: '♩', img: 'assets/items/cuerda.png', desc: 'Tensión metálica. El sonido de un lazo asfixiante.' },
    { id: 'espe', name: 'Espejo', icon: '◇', img: 'assets/items/espejo.png', desc: 'Reflejos rotos. La belleza fragmentada por la violencia.' }
];

// Lista de locaciones posibles. El id se cruza con CLUES_BY_LOC.
const LOCATIONS = [
    { id: 'aula', name: 'El Aula 304', icon: '◻', bg: 'assets/backgrounds/aula.png', desc: 'Donde todo empezó. Las paredes recuerdan lo que nadie vio.' },
    { id: 'psiq', name: 'NCMH', icon: '⊕', bg: 'assets/backgrounds/psiquiatrico.png', desc: '¿Refugio o prisión? Pasillos blancos que absorben el sonido.' },
    { id: 'depa', name: 'Depa Dakho', icon: '⌂', bg: 'assets/backgrounds/departamento.png', desc: 'Sábanas que guardan secretos. Silencios que pesan toneladas.' },
    { id: 'bar', name: 'Bar Sin Nombre', icon: '◉', bg: 'assets/backgrounds/bar.png', desc: 'Donde los borrachos confiesan lo que los sobrios esconden.' },
    { id: 'jard', name: 'El Jardín de la Azotea', icon: '❋', bg: 'assets/backgrounds/azotea.png', desc: 'El cielo más cerca, el suelo más lejos.' }
];

// Musica por etapa del juego. Puedes reemplazar los mp3 respetando rutas.
const TRACKS = { menu: 'assets/music/menu_theme.mp3', mystery: 'assets/music/clues_theme.mp3', reveal: 'assets/music/reveal_theme.mp3' };

// Texto de revelacion final por culpable.
// La clave (pax/eth/dak/xio/dar) debe coincidir con el id del sospechoso.
const STORIES = {
    pax: { dialogue: [{ s: "Sterling", t: "¿Qué viste esa noche, Dae?" }, { s: "Dae", t: "Vi sus ojos... brillaban con rabia." }], body: 'Dae recordó el calor sofocante de la habitación. Pax no aceptaba el final. En un arrebato de posesividad, decidió que si ella no era suya, no sería de nadie.' },
    eth: { dialogue: [{ s: "Sterling", t: "Ethan siempre fue tu apoyo, ¿no?" }, { s: "Dae", t: "Él lo sabía todo y solo miraba desde lejos." }], body: 'Ethan Blackwood decidió que todos serían víctimas de su frialdad. Dae recordó el brillo del acero y la mirada de arrepentimiento en los ojos de su mejor amigo.' },
    dak: { dialogue: [{ s: "Sterling", t: "¿Él te enseñó algo más que libros?" }, { s: "Dae", t: "Me enseñó que el poder es una droga." }], body: 'El profesor Belmont no podía permitir que el escándalo destruyera su prestigio. Dae recordó la frialdad de sus palabras mientras él intentaba borrar su "error".' },
    xio: { dialogue: [{ s: "Sterling", t: "Parecía el más inocente..." }, { s: "Dae", t: "Los ángeles esconden mejor el cuchillo." }], body: 'Xion Kravitz vio una oportunidad de caos y la tomó. El odio hacia su padre se manifestó en la persona que él más quería.' },
    dar: { dialogue: [{ s: "Sterling", t: "Dime la verdad. ¿Quién te rompió?" }, { s: "Dae", t: "Usted, doctor. Usted es el dueño de mi dolor." }], body: 'Sterling manipuló a Dae hasta que ella ya no supo quién era. Él no quería curarla, quería poseer su mente para siempre.' }
};

// Pistas de cada categoria. Importante: cada clave debe existir en su lista base.
const CLUES_BY_WEAPON = { farm: "Dae siente un sabor amargo en la garganta.", nota: "Hay un papel arrugado: 'Lo siento, esto es por tu bien'.", bist: "El corte en el aire fue rápido. Acero negro.", cuer: "Dae recuerda un zumbido metálico asfixiante.", espe: "Suelo cubierto de reflejos rotos." };
const CLUES_BY_LOC = { aula: "Hay marcas de tiza en el suelo que forman una silueta desesperada.", psiq: "Las luces del pasillo B parpadearon justo cuando Dae dejó de gritar.", depa: "El aroma a jazmín sigue impregnado en las cortinas de seda.", bar: "Una cuenta pagada en efectivo quedó olvidada sobre la barra.", jard: "Huellas de zapatos finos sobre el concreto frío de la azotea." };
const CLUES_BY_CULPRIT = { pax: "Dae susurra: 'Él siempre juró que me cuidaría... que nadie más podría tocarme'.", eth: "Se encontró un encendedor con una 'E'. Olía a humo mentolado.", dak: "Quedó una pluma estilográfica de oro. Solo una persona usaba esa tinta púrpura.", xio: "Hay una pequeña llave dorada de un estuche de música. La melodía no para.", dar: "Un informe con la palabra 'IRRECUPERABLE' fue hallado en el centro del caos." };

// Texto introductorio de Sterling segun el culpable real sorteado.
const STERLING_OPENERS = { pax: "Dae está inquieta. Dice que alguien la observa desde las sombras...", eth: "He encontrado notas extrañas en el diario de la paciente.", dak: "Alguien ha estado llamando. Dae grita cada vez que suena el teléfono.", xio: "Un visitante estuvo aquí ayer. Dae no ha dejado de temblar.", dar: "He decidido tomar el control total. Ella ya no sabe qué es real." };

// Estado global compartido entre ui.js y game.js.
// - culprit/weapon/location_real: respuesta correcta del caso actual
// - pCulprit/pWeapon/pLocation: seleccion del jugador
let culprit, weapon, location_real, pCulprit, pWeapon, pLocation;