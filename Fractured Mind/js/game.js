function startGame() {
    // Inicializa un caso nuevo: sortea respuesta real, limpia seleccion del jugador
    // y prepara las pantallas de pistas/acusacion.
    playMusic('mystery');
    culprit = SUSPECTS[Math.floor(Math.random() * SUSPECTS.length)];
    weapon = WEAPONS[Math.floor(Math.random() * WEAPONS.length)];
    location_real = LOCATIONS[Math.floor(Math.random() * LOCATIONS.length)];
    
    pCulprit = null; 
    pWeapon = null; 
    pLocation = null;
    
    const caseNum = document.getElementById('nav-case');
    if (caseNum) caseNum.textContent = 'Caso #' + (Math.floor(Math.random() * 900) + 100);
    
    buildClues();
    buildAccusation();
    
    goTo('s-clues');
    setProgress(35);
}

function buildClues() {
    // Genera 3 pistas (culpable, arma, lugar) del caso actual.
    // Actualmente se muestran en orden fijo; si quieres mas dificultad,
    // puedes barajar el arreglo mixedClues antes de renderizar.
    const noteEl = document.getElementById('sterling-note');
    if (noteEl) noteEl.innerHTML = `${STERLING_OPENERS[culprit.id]} <br><br><span style="color:var(--teal)">— Dr. Sterling</span>`;
    
    const mixedClues = [CLUES_BY_LOC[location_real.id], CLUES_BY_WEAPON[weapon.id], CLUES_BY_CULPRIT[culprit.id]];
    const container = document.getElementById('clue-files');
    if (container) {
        container.innerHTML = mixedClues.map((c, i) => `
            <div class="clue-file revealed">
                <div class="clue-num">EVIDENCIA ${i + 1}</div>
                <div class="clue-text">"${c}"</div>
            </div>`).join('');
    }
}

function buildAccusation() {
    // Construye las tarjetas seleccionables para que el jugador acuse.
    document.getElementById('accuse-chars').innerHTML = SUSPECTS.map(s => `
        <div class="mini-card" onclick="pick('char','${s.id}',this)">
            <div class="mini-char-img"><img src="${s.expressions.default}" style="width:100%; height:100%; object-fit:cover; object-position: center 20%;"></div>
            <div class="mini-card-top">${s.name}<br><small style="font-size:0.5rem; opacity:0.7;">${s.alias}</small></div>
        </div>`).join('');

    document.getElementById('accuse-weapons').innerHTML = WEAPONS.map(w => `
        <div class="mini-card" onclick="pick('weapon','${w.id}',this)">
            <div style="height:50px; overflow:hidden;"><img src="${w.img}" style="width:100%; height:100%; object-fit:cover; filter:grayscale(1);"></div>
            <div class="mini-card-top">${w.name}</div>
        </div>`).join('');

    document.getElementById('accuse-locs').innerHTML = LOCATIONS.map(l => `
        <div class="mini-card" onclick="pick('loc','${l.id}',this)">
             <div style="height:50px; overflow:hidden;"><img src="${l.bg}" style="width:100%; height:100%; object-fit:cover;"></div>
            <div class="mini-card-top">${l.name}</div>
        </div>`).join('');
}

function pick(type, id, el) {
    // Marca visualmente una opcion y guarda la seleccion en estado global.
    const parent = el.parentElement;
    parent.querySelectorAll('.mini-card').forEach(c => c.classList.remove('selected'));
    el.classList.add('selected');
    
    if (type === 'char') { 
        pCulprit = SUSPECTS.find(s => s.id === id); 
        showCharacterPortrait(pCulprit, 'accuse', true); 
    }
    else if (type === 'weapon') { pWeapon = WEAPONS.find(w => w.id === id); }
    else { pLocation = LOCATIONS.find(l => l.id === id); }
}

function confirmAccusation() {
    // Exige seleccionar culpable, arma y locacion antes de revelar resultado.
    if (!pCulprit || !pWeapon || !pLocation) {
        alert("Dae, selecciona a los tres sospechosos...");
        return;
    }
    buildReveal();
    goTo('s-reveal');
}

function buildReveal() {
    // Muestra la verdad del caso y compara la eleccion del jugador vs realidad.
    playMusic('reveal');
    const story = STORIES[culprit.id];
    if (!story) {
        console.error('Story not found for culprit:', culprit.id);
        return;
    }
    
    showCharacterPortrait(culprit, 'reveal', true);
    
    const revName = document.getElementById('rev-name');
    if (revName) revName.innerHTML = `${culprit.name}<br><small>${culprit.alias}</small>`;
    
    const chatHTML = story.dialogue.map(d => `<div><strong>${d.s.toUpperCase()}:</strong> <i>${d.t}</i></div>`).join('');
    
    const revStory = document.getElementById('rev-story');
    if (revStory) {
        revStory.innerHTML = `
            <div class="chat-box" style="background:rgba(0,0,0,0.3); padding:15px; border-left:2px solid var(--teal); margin-bottom:20px;">${chatHTML}</div>
            <div class="memory-desc"><strong>LO QUE RECORDÓ DAE:</strong><br>${story.body}</div>
        `;
    }
    
    const isPerfect = (pCulprit.id === culprit.id && pWeapon.id === weapon.id && pLocation.id === location_real.id);
    const banner = document.getElementById('result-banner');
    if (banner) {
        banner.className = "result-banner " + (isPerfect ? "perfect" : "fail");
        banner.textContent = isPerfect ? "HAS RECUPERADO LA MEMORIA." : "EL PASADO SIGUE SIENDO UNA MENTIRA.";
    }

    const scoreRow = document.getElementById('score-row');
    if (scoreRow) {
        scoreRow.innerHTML = `
            <div class="score-card ${pCulprit.id === culprit.id ? 'correct' : 'wrong'}">Culpable: ${pCulprit.name}</div>
            <div class="score-card ${pWeapon.id === weapon.id ? 'correct' : 'wrong'}">Arma: ${pWeapon.name}</div>
            <div class="score-card ${pLocation.id === location_real.id ? 'correct' : 'wrong'}">Lugar: ${pLocation.name}</div>
        `;
    }
}

function resetGame() { 
    // Reinicia a pantalla inicial. Un nuevo startGame vuelve a sortear todo.
    playMusic('menu'); 
    goTo('s-title'); 
}

function registerUser() {
    // Guarda nombre del usuario solo para sesion local (localStorage).
    const input = document.getElementById('user-input');
    if (input && input.value.trim()) {
        localStorage.setItem('username', input.value.trim());
        goTo('s-title');
    } else {
        alert("Ingrese su identificación de Agente.");
    }
}

window.onload = () => {
    // Al recargar, forzamos login para iniciar una partida limpia.
    localStorage.removeItem('username');
    goTo('s-login'); 
};

// Primer click del usuario habilita reproduccion de audio en navegadores modernos.
window.addEventListener('click', () => { if (!currentAudio) playMusic('menu'); }, { once: true });