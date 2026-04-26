// ==============================
// UTILIDADES DE INTERFAZ (UI)
// ==============================
// Este archivo controla navegacion de pantallas, musica y render de tarjetas.

let currentAudio = null;

function playMusic(trackKey) {
    // Reproduce la pista asociada a la etapa actual (menu, mystery, reveal).
    // Evita recrear audio si ya suena la misma pista.
    const src = TRACKS[trackKey];
    if (!src) return;
    if (currentAudio && currentAudio.src.includes(src)) return;
    if (currentAudio) { currentAudio.pause(); currentAudio.currentTime = 0; }
    currentAudio = new Audio(src);
    currentAudio.loop = true;
    currentAudio.volume = 0.4;
    currentAudio.play().catch(e => console.log("Audio esperando clic inicial."));
}

function hideCharacterPortrait() {
    // Oculta el retrato lateral del personaje en pantallas donde no aplica.
    const wrap = document.getElementById('char-portrait-wrap');
    const label = document.getElementById('char-portrait-label');
    if (wrap) {
        wrap.style.setProperty('display', 'none', 'important');
        wrap.style.opacity = '0';
    }
    if (label) {
        label.innerHTML = ''; 
    }
}

function clearSceneBg() {
    const bg = document.getElementById('scene-bg');
    if (!bg) return;
    bg.style.backgroundImage = 'none';
    bg.style.opacity = '0';
}

function setSceneBg(imagePath) {
    const bg = document.getElementById('scene-bg');
    if (!bg) return;
    bg.style.backgroundImage = imagePath ? `url('${imagePath}')` : 'none';
    bg.style.opacity = imagePath ? '1' : '0';
}

function showCharacterPortrait(char, expressionType, highlight = false) {
    // Solo mostramos retratos en acusacion/revelacion para mantener foco visual.
    const currentScreen = document.querySelector('.screen.active');
    if (currentScreen && currentScreen.id !== 's-accuse' && currentScreen.id !== 's-reveal') {
        return;
    }

    const label = document.getElementById('char-portrait-label');
    const wrap = document.getElementById('char-portrait-wrap');
    
    if (!char) return;

    const portraitPath = char.expressions?.[expressionType] || char.expressions?.default;

    if (label) {
        label.innerHTML = `${char.name}<br><small>${char.alias}</small>`;
        label.style.color = char.color;
        label.style.opacity = highlight ? "1" : "0.5";
    }
    const image = document.getElementById('char-portrait-img');
    if (image && portraitPath) {
        image.src = portraitPath;
        image.alt = char.name;
    }
    if (wrap) {
        wrap.style.setProperty('display', 'block', 'important');
        wrap.style.opacity = '1';
    }
}

function goTo(id) {
    // Navegador simple de pantallas (tipo SPA sin rutas).
    const screens = document.querySelectorAll('.screen');
    screens.forEach(s => s.classList.remove('active'));
    const target = document.getElementById(id);
    if (target) target.classList.add('active');

    if (id === 's-clues' || id === 's-title' || id === 's-login' || id === 's-intro' || id === 's-cast') {
        hideCharacterPortrait(); 
    } else if (id === 's-accuse') {
        if (typeof pCulprit !== 'undefined' && pCulprit !== null) {
            showCharacterPortrait(pCulprit, 'accuse', true);
        } else {
            hideCharacterPortrait();
        }
    }
}

function setProgress(p) {
    // Ajusta barra de progreso principal en porcentaje.
    const fill = document.getElementById('prog-fill');
    if (fill) fill.style.width = p + '%';
}

function setNav(t) {
    // Cambia subtitulo superior contextual.
    const nav = document.getElementById('nav-step');
    if (nav) nav.textContent = t;
}

function showLore() { goTo('s-intro'); setNav('· El Expediente de Dae ·'); }
function showCast() { buildCast(); goTo('s-cast'); setNav('· Sospechosos ·'); }

function buildCast() {
    // Render dinamico de sospechosos, armas y locaciones para la pantalla Informacion.
    // Si agregas elementos en data.js, apareceran automaticamente aqui.
    const grid = document.getElementById('cast-grid');
    if (grid) {
        grid.innerHTML = SUSPECTS.map(s => `
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front" style="border-top: 3px solid ${s.color}">
                        <div class="char-portrait-mini"><img src="${s.expressions.default}" style="width:100%; height:100%; object-fit:cover; object-position: center 20%;"></div>
                        <div class="char-name">${s.name}</div>
                        <div class="char-alias" style="color:${s.color}">${s.alias}</div>
                    </div>
                    <div class="flip-card-back"><p class="back-desc">${s.desc}</p></div>
                </div>
            </div>`).join('');
    }
    const weaponsGrid = document.getElementById('weapons-grid');
    if (weaponsGrid) {
        weaponsGrid.innerHTML = WEAPONS.map(w => `<div class="flip-card"><div class="flip-card-inner"><div class="flip-card-front"><div style="height:120px; overflow:hidden;"><img src="${w.img}" style="width:100%; height:100%; object-fit:cover; filter:grayscale(1);"></div><div class="item-name">${w.icon} ${w.name}</div></div><div class="flip-card-back"><p class="back-desc">${w.desc}</p></div></div></div>`).join('');
    }
    const locationsGrid = document.getElementById('locations-grid');
    if (locationsGrid) {
        locationsGrid.innerHTML = LOCATIONS.map(l => `<div class="flip-card"><div class="flip-card-inner"><div class="flip-card-front"><div style="height:120px; overflow:hidden;"><img src="${l.bg}" style="width:100%; height:100%; object-fit:cover;"></div><div class="item-name">${l.icon} ${l.name}</div></div><div class="flip-card-back"><p class="back-desc">${l.desc}</p></div></div></div>`).join('');
    }
}