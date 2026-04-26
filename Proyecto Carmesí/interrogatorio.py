import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SistemaExperto:
    def __init__(self):
        # Define archivo fuente y carga la base de conocimiento.
        self.archivo_datos = os.path.join(BASE_DIR, 'asesinos.json')
        self.personajes = self.cargar_datos()

    def cargar_datos(self):
        # Si ocurre un error de lectura, devuelve lista vacia para no romper el flujo.
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return []

    def guardar_datos(self):
        # Persistencia local de los cambios aprendidos por el sistema.
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            json.dump(self.personajes, f, indent=4)

    def jugar(self):
        print("--- INTERROGATORIO DE SEGURIDAD NACIONAL ---")
        print("Piensa en un sujeto... voy a extraer la verdad.\n")
        
        posibles = list(self.personajes)
        rasgos_preguntados = []

        while len(posibles) > 1:
            # Extraer un rasgo del primer personaje que no hayamos preguntado
            rasgo_actual = None
            for p in posibles:
                for r in p['rasgos']:
                    if r not in rasgos_preguntados:
                        rasgo_actual = r
                        break
                if rasgo_actual: break
            
            if not rasgo_actual: break

            respuesta = input(f"¿El sujeto tiene el rasgo: [{rasgo_actual.upper()}]? (s/n): ").lower()
            rasgos_preguntados.append(rasgo_actual)

            if respuesta == 's':
                posibles = [p for p in posibles if rasgo_actual in p['rasgos']]
            else:
                posibles = [p for p in posibles if rasgo_actual not in p['rasgos']]

        # Si queda un unico candidato, solicita confirmacion al usuario.
        if len(posibles) == 1:
            confirmar = input(f"El sujeto es: {posibles[0]['nombre'].upper()}. ¿Es correcto? (s/n): ")
            if confirmar == 's':
                print("Expediente cerrado con éxito.")
            else:
                self.aprender(rasgos_preguntados)
        else:
            print("No tengo registro de este individuo.")
            self.aprender(rasgos_preguntados)

    def aprender(self, rasgos_conocidos):
        # Aprendizaje incremental: agrega un nuevo perfil con rasgos ya conocidos + uno distintivo.
        print("\n--- EL SISTEMA DEBE APRENDER ---")
        nombre = input("¿De quién se trata? ")
        nuevo_rasgo = input(f"¿Qué rasgo único tiene {nombre} que no mencionamos? ")
        
        nuevo_personaje = {
            "nombre": nombre,
            "rasgos": rasgos_conocidos + [nuevo_rasgo],
            "victima": False
        }
        
        self.personajes.append(nuevo_personaje)
        self.guardar_datos()
        print("Base de datos actualizada. No volverá a suceder.")

if __name__ == "__main__":
    # Punto de entrada para ejecutar la version de consola.
    game = SistemaExperto()
    game.jugar()