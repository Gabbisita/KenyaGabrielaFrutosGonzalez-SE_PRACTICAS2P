import json
import os
import shutil
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, 'assets')
JSON_PATH = os.path.join(BASE_DIR, 'asesinos.json')

class SistemaExperto:
    def __init__(self):
        # Carga base de casos y prepara estructuras para inferencia.
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            self.personajes = json.load(f)
        random.shuffle(self.personajes)
        self.posibles = self.personajes[:]
        self.rasgos_preguntados = set()
        self.primera_pregunta = True

    def obtener_siguiente_rasgo(self):
        # Cuenta cuantas veces aparece cada rasgo entre los candidatos actuales.
        conteo = {}
        total_posibles = len(self.posibles)
        
        if total_posibles <= 1: return None

        for p in self.posibles:
            for r in p['rasgos']:
                if r not in self.rasgos_preguntados:
                    conteo[r] = conteo.get(r, 0) + 1
        
        if not conteo: return None

        # La primera pregunta se elige al azar para que cada partida arranque distinta.
        if self.primera_pregunta:
            self.primera_pregunta = False
            return random.choice(list(conteo.keys()))

        # Se elige el rasgo que mejor divide el conjunto en dos mitades.
        mejor_distancia = float('inf')
        
        for _rasgo, cant in conteo.items():
            distancia = abs((total_posibles / 2) - cant)
            if distancia < mejor_distancia:
                mejor_distancia = distancia
        
        # Si hay empate, se selecciona uno aleatorio para variar partidas.
        candidatos = [r for r, c in conteo.items() if abs((total_posibles / 2) - c) == mejor_distancia]
        
        return random.choice(candidatos)

    def procesar_respuesta(self, rasgo, respuesta):
        # Registra rasgo consultado y filtra candidatos segun respuesta.
        self.rasgos_preguntados.add(rasgo)
        if respuesta == 's':
            self.posibles = [p for p in self.posibles if rasgo in p['rasgos']]
        else:
            self.posibles = [p for p in self.posibles if rasgo not in p['rasgos']]

    def aprender_nuevo_caso(self, nombre, rasgo_nuevo, foto_path=None):
        # Agrega nuevo sospechoso minimo y persiste inmediatamente en disco.
        foto_destino = None
        if foto_path and os.path.exists(foto_path):
            nombre_base = "".join(c for c in nombre.lower().replace(" ", "_") if c.isalnum() or c in ("_", "-")) or "nuevo"
            _, extension = os.path.splitext(foto_path)
            extension = extension.lower() if extension else ".png"
            foto_destino_abs = os.path.join(ASSET_DIR, f"{nombre_base}{extension}")
            contador = 1
            while os.path.exists(foto_destino_abs):
                foto_destino_abs = os.path.join(ASSET_DIR, f"{nombre_base}_{contador}{extension}")
                contador += 1
            try:
                shutil.copy2(foto_path, foto_destino_abs)
                foto_destino = os.path.relpath(foto_destino_abs, BASE_DIR)
            except OSError:
                foto_destino = os.path.relpath(os.path.abspath(foto_path), BASE_DIR)

        nuevo = {"nombre": nombre, "rasgos": [rasgo_nuevo], "foto": foto_destino, "bio": "Registro manual."}
        self.personajes.append(nuevo)
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.personajes, f, indent=4)