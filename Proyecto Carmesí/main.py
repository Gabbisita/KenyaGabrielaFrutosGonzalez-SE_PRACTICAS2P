import customtkinter as ctk
from PIL import Image, ImageOps, UnidentifiedImageError
import pygame
import os
import random
from tkinter import TclError, filedialog
from motor_inferencia import SistemaExperto 
from narrativa import PREGUNTAS 
from expedientes import renderizar_expedientes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")


def resolver_ruta_imagen(ruta):
    if not ruta:
        return None
    if os.path.isabs(ruta):
        return ruta
    return os.path.join(BASE_DIR, ruta)


class CanalNulo:
    def play(self, *args, **kwargs):
        pass

    def stop(self):
        pass

class InterrogatorioDefinitivo(ctk.CTk):
    preview_imagen: ctk.CTkImage | None = None
    preview_panel: ctk.CTkFrame | None = None
    preview_label: ctk.CTkLabel | None = None

    def __init__(self):
        super().__init__()
        # Configuracion general de la ventana principal.
        self.title("PROYECTO: CARPETA CARMESÍ")
        self.geometry("1000x750")
        self.resizable(False, False) 

        self.audio_activo = False
        self.canal_sfx = CanalNulo()
        self.canal_risa = CanalNulo()
        self.sfx_estatica = None
        self.sfx_risa = None
        self.turnos_totales = 15
        self.turnos_actuales = 15
        self.nombre_agente = "DESCONOCIDO"
        self.rasgo_actual = None
        self.panico_activado = False
        self.risa_reproducida = False
        self.narrativa = PREGUNTAS
        self.frame_menu = None
        self.lbl_titulo = None
        self.entry_nombre = None
        self.selector_turnos = None
        self.lbl_intentos = None
        self.frame_exp = None
        self.lbl_foto = None
        self.lbl_preg = None
        self.btn_s = None
        self.btn_n = None
        self.btn_si_final = None
        self.btn_no_final = None
        self.en = None
        self.er = None
        self.ei = None
        self.preview_imagen = None
        self.preview_panel = None
        self.preview_label = None
        self.sujeto_pendiente = None
        
        # Se inicializa audio y estado de juego antes de mostrar la intro.
        self.configurar_audio()
        self.reiniciar_variables()
        self.secuencia_cinematica()

    def configurar_audio(self):
        # Musica ambiental en bucle si existe en la carpeta assets.
        try:
            pygame.mixer.init()
            self.audio_activo = True
            musica_path = os.path.join(ASSET_DIR, "musica.mp3")
            estatica_path = os.path.join(ASSET_DIR, "estatica.mp3")
            risa_path = os.path.join(ASSET_DIR, "risa.mp3")
            if os.path.exists(musica_path):
                pygame.mixer.music.load(musica_path)
                pygame.mixer.music.set_volume(0.15) 
                pygame.mixer.music.play(-1)
            # Canales separados para no mezclar efectos con musica de fondo.
            self.canal_sfx = pygame.mixer.Channel(1)
            self.canal_risa = pygame.mixer.Channel(2)
            self.sfx_estatica = pygame.mixer.Sound(estatica_path) if os.path.exists(estatica_path) else None
            self.sfx_risa = pygame.mixer.Sound(risa_path) if os.path.exists(risa_path) else None
        except (OSError, RuntimeError, LookupError):
            self.audio_activo = False
            self.canal_sfx = CanalNulo()
            self.canal_risa = CanalNulo()
            self.sfx_estatica = None
            self.sfx_risa = None

    def reiniciar_variables(self):
        # Se crea un motor nuevo para iniciar cada partida desde cero.
        self.motor = SistemaExperto()
        self.turnos_totales = 15 
        self.turnos_actuales = 15
        self.nombre_agente = "DESCONOCIDO"
        self.rasgo_actual = None
        self.panico_activado = False
        self.risa_reproducida = False 
        self.narrativa = PREGUNTAS 
        self.canal_sfx.stop()
        self.canal_risa.stop()

    def limpiar_pantalla(self):
        # Elimina todos los widgets activos para cambiar de vista.
        for widget in self.winfo_children(): widget.destroy()

    def poner_fondo(self):
        # Carga una imagen de fondo compartida por varias pantallas.
        fondo_path = os.path.join(ASSET_DIR, "fondo.png")
        if os.path.exists(fondo_path):
            img = ctk.CTkImage(Image.open(fondo_path), size=(1000, 750))
            ctk.CTkLabel(self, image=img, text="").place(x=0, y=0)

    def secuencia_cinematica(self):
        self.limpiar_pantalla()
        self.configure(fg_color="#000")
        
        historia = [
            "24 ASESINOS.\nUN DETECTIVE.",
            "ENCUÉNTRALOS ANTES DE QUE\nELLOS TE ENCUENTREN A TI.",
            "SISTEMA DESARROLLADO POR:\nKENYA FRUTOS",
            "ESTÁS ACCEDIENDO A LA 'CARPETA CARMESÍ'.\nARCHIVOS CLASIFICADOS.",
            "SI EL SISTEMA SE CORROMPE...\nELLOS SABRÁN QUE ESTÁS AQUÍ."
        ]
        
        self.lbl_historia = ctk.CTkLabel(self, text="", font=("Courier New", 22, "bold"), text_color="#8B0000", justify="center")
        self.lbl_historia.place(relx=0.5, rely=0.5, anchor="center")

        def mostrar_texto(indice):
            # Muestra cada bloque con efecto de maquina de escribir.
            if indice < len(historia):
                self.lbl_historia.configure(text="")
                self.efecto_tipeo(historia[indice], 0, lambda: self.after(2000, lambda: mostrar_texto(indice + 1)))
            else:
                self.after(1000, self.pantalla_menu)
        mostrar_texto(0)

    def efecto_tipeo(self, texto, i, callback):
        if i <= len(texto):
            self.lbl_historia.configure(text=texto[:i])
            self.after(40, lambda: self.efecto_tipeo(texto, i + 1, callback))
        else: callback()

    def pantalla_menu(self):
        # El menu reinicia estado para evitar residuos de partidas previas.
        self.reiniciar_variables()
        self.limpiar_pantalla()
        self.poner_fondo()
        if self.audio_activo and not pygame.mixer.music.get_busy(): pygame.mixer.music.play(-1)

        self.frame_menu = ctk.CTkFrame(self, fg_color="#070707", border_width=1, border_color="#300")
        self.frame_menu.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.8)
        
        self.lbl_titulo = ctk.CTkLabel(self.frame_menu, text="PROYECTO: CARMESÍ", font=("Courier New", 45, "bold"), text_color="#8B0000") 
        self.lbl_titulo.pack(pady=(20, 5))
        self.animar_titulo_glitch()
        
        ctk.CTkLabel(self.frame_menu, text="S I S T E M A   E X P E R T O   F O R E N S E", font=("Courier New", 14), text_color="#555").pack()
        ctk.CTkLabel(self.frame_menu, text="DEV BY: KENYA FRUTOS", font=("Courier New", 10), text_color="#333").pack(pady=(0, 10))

        self.entry_nombre = ctk.CTkEntry(self.frame_menu, placeholder_text="Nombre Agente...", fg_color="#000", border_color="#400", justify="center", width=250)
        self.entry_nombre.pack(pady=10)

        self.selector_turnos = ctk.CTkSegmentedButton(self.frame_menu, values=["5", "10", "15", "20"], fg_color="#000", selected_color="#8B0000", command=self.cambiar_turnos)
        self.selector_turnos.set(str(self.turnos_totales))
        self.selector_turnos.pack(pady=10)

        ctk.CTkButton(self.frame_menu, text="► INICIAR PROTOCOLO", font=("Courier New", 18, "bold"), fg_color="#000", border_width=2, border_color="#8B0000", command=self.preparar_juego).pack(pady=(20, 10))
        ctk.CTkButton(self.frame_menu, text="📂 VER EXPEDIENTES", font=("Courier New", 14), fg_color="#111", command=lambda: renderizar_expedientes(self)).pack(pady=5)
        ctk.CTkButton(self.frame_menu, text="X SALIR DEL SISTEMA", font=("Courier New", 12), fg_color="#300", command=self.quit).pack(pady=20)

    def animar_titulo_glitch(self):
        try:
            if self.lbl_titulo.winfo_exists():
                self.lbl_titulo.configure(text_color=random.choice(["#8B0000", "#FF0000", "#400000", "#000000"]))
                self.after(random.randint(50, 500), self.animar_titulo_glitch)
        except TclError:
            pass

    def cambiar_turnos(self, v): 
        self.turnos_totales = int(v)
        self.turnos_actuales = int(v)

    def preparar_juego(self):
        # Si no se escribe nombre, se asigna un alias por defecto.
        self.nombre_agente = self.entry_nombre.get() if self.entry_nombre.get() else "AGENTE_ANÓNIMO"
        self.canal_risa.stop()
        self.transicion_segura()

    def transicion_segura(self):
        self.limpiar_pantalla()
        self.configure(fg_color="#000")
        lbl_estado = ctk.CTkLabel(self, text="", font=("Courier New", 20, "bold"), text_color="#8B0000")
        lbl_estado.place(relx=0.5, rely=0.5, anchor="center")
        if self.sfx_estatica: self.canal_sfx.play(self.sfx_estatica, loops=-1)
        
        pasos = ["ESTABLECIENDO ENLACE SEGURO...", "DESENCRIPTANDO DATOS...", "SISTEMA LISTO.", "INICIANDO PROTOCOLO DE INTERROGATORIO..."]
        def mostrar_paso(i):
            # Secuencia visual de carga antes de entrar al juego.
            if i < len(pasos):
                lbl_estado.configure(text=pasos[i])
                self.after(1000, lambda: mostrar_paso(i + 1))
            else: self.arrancar_interrogatorio()
        mostrar_paso(0)

    def arrancar_interrogatorio(self):
        self.canal_sfx.stop()
        self.canal_risa.stop()
        self.limpiar_pantalla()
        self.montar_interfaz_juego()
        self.siguiente_pregunta()

    def montar_interfaz_juego(self):
        # Construye componentes visuales fijos usados durante el interrogatorio.
        self.poner_fondo()
        self.lbl_intentos = ctk.CTkLabel(self, text=f"INTENTOS: {self.turnos_actuales}", font=("Courier New", 18, "bold"), text_color="#F00", fg_color="#111", padx=15)
        self.lbl_intentos.place(x=20, y=20)
        self.frame_exp = ctk.CTkFrame(self, fg_color="#050505", border_width=1, border_color="#333")
        self.frame_exp.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.5, relheight=0.45)
        self.lbl_foto = ctk.CTkLabel(self.frame_exp, text="[ ESCANEANDO... ]", text_color="#555", font=("Courier New", 14))
        self.lbl_foto.pack(expand=True)
        self.lbl_preg = ctk.CTkLabel(self, text="", font=("Courier New", 16, "bold"), text_color="#ddd", fg_color="#000", padx=20, pady=15, wraplength=700)
        self.lbl_preg.place(relx=0.5, rely=0.75, anchor="center")
        self.btn_s = ctk.CTkButton(self, text="AFIRMATIVO", fg_color="#111", border_width=1, command=lambda: self.procesar_respuesta('s'))
        self.btn_n = ctk.CTkButton(self, text="NEGATIVO", fg_color="#111", border_width=1, command=lambda: self.procesar_respuesta('n'))

    def procesar_respuesta(self, resp):
        # Cada respuesta reduce turnos y filtra candidatos en el motor experto.
        self.turnos_actuales -= 1
        self.lbl_intentos.configure(text=f"INTENTOS: {self.turnos_actuales}")
        self.motor.procesar_respuesta(self.rasgo_actual, resp)
        if self.turnos_actuales <= 4 and not self.risa_reproducida:
            if self.sfx_risa: self.canal_risa.play(self.sfx_risa)
            self.risa_reproducida = True
        # Priorizacion de estados finales: identificado, sin candidatos, sin turnos.
        if len(self.motor.posibles) == 1: self.pedir_confirmacion(self.motor.posibles[0])
        elif len(self.motor.posibles) == 0: self.game_over("burlado")
        elif self.turnos_actuales <= 0: self.game_over("tiempo")
        else: self.siguiente_pregunta()

    def siguiente_pregunta(self):
        # Solicita al motor el rasgo con mayor valor discriminante.
        self.rasgo_actual = self.motor.obtener_siguiente_rasgo()
        if self.rasgo_actual:
            self.btn_s.place_forget(); self.btn_n.place_forget()
            p = self.narrativa.get(self.rasgo_actual, f"¿Rasgo: {self.rasgo_actual}?")
            self.lbl_preg.configure(text=f"> PROCESANDO EVIDENCIA...\n\n{p}")
            self.after(400, lambda: [self.btn_s.place(relx=0.35, rely=0.88, anchor="center"), self.btn_n.place(relx=0.65, rely=0.88, anchor="center")])
        else: self.game_over("burlado")

    def pedir_confirmacion(self, sujeto):
        self.canal_risa.stop()
        self.sujeto_pendiente = sujeto
        self.btn_s.place_forget(); self.btn_n.place_forget()
        self.lbl_preg.configure(text=f"> ¿ES ESTE EL SUJETO?\n\n*** {sujeto['nombre'].upper()} ***", text_color="#F00")
        self.btn_si_final = ctk.CTkButton(self, text="SÍ", fg_color="#111", border_width=1, command=self.confirmar_sujeto)
        self.btn_no_final = ctk.CTkButton(self, text="NO", fg_color="#111", border_width=1, command=self.rechazar_sujeto)
        self.after(300, lambda: [self.btn_si_final.place(relx=0.35, rely=0.88, anchor="center"), self.btn_no_final.place(relx=0.65, rely=0.88, anchor="center")])

    def confirmar_sujeto(self):
        if self.btn_si_final:
            self.btn_si_final.place_forget()
        if self.btn_no_final:
            self.btn_no_final.place_forget()
        if self.sujeto_pendiente:
            self.lbl_preg.configure(text="> IDENTIDAD ENCONTRADA", text_color="#F00")
            self.after(800, lambda: self.mostrar_identidad_final(self.sujeto_pendiente))

    def rechazar_sujeto(self):
        if self.btn_si_final:
            self.btn_si_final.place_forget()
        if self.btn_no_final:
            self.btn_no_final.place_forget()
        self.sujeto_pendiente = None
        self.aprendizaje()

    def mostrar_identidad_final(self, sujeto):
        self.lbl_preg.configure(text=f"*** {sujeto['nombre'].upper()} IDENTIFICADO ***", text_color="#00FF00")
        foto = resolver_ruta_imagen(sujeto.get('foto'))
        if foto and os.path.exists(foto):
            img_c = ImageOps.fit(Image.open(foto), (500, 337), centering=(0.5, 0.5))
            img = ctk.CTkImage(img_c, size=(500, 337))
            def parpadear(c):
                # Parpadeo breve para reforzar el efecto de revelacion.
                if c > 0:
                    self.lbl_foto.configure(image="", fg_color="#F00")
                    self.after(50, lambda: [self.lbl_foto.configure(image=img, fg_color="transparent"), self.after(100, lambda: parpadear(c-1))])
            self.lbl_foto.configure(image=img, text="")
            parpadear(4)
        ctk.CTkButton(self, text="REINTENTAR", fg_color="#111", command=self.arrancar_interrogatorio).place(relx=0.4, rely=0.9, anchor="center")
        ctk.CTkButton(self, text="MENÚ", fg_color="#400", command=self.pantalla_menu).place(relx=0.6, rely=0.9, anchor="center")

    def game_over(self, motivo):
        if self.audio_activo:
            pygame.mixer.music.stop()
        if self.sfx_risa: self.canal_risa.play(self.sfx_risa)
        self.limpiar_pantalla(); self.configure(fg_color="#000")
        t1 = "SISTEMA BURLADO: GAME OVER" if motivo == "burlado" else "TIEMPO AGOTADO"
        col = "#F00" if motivo == "burlado" else "#600"
        ctk.CTkLabel(self, text=t1, font=("Courier New", 35, "bold"), text_color=col).place(relx=0.5, rely=0.3, anchor="center")
        ctk.CTkLabel(self, text=f"{self.nombre_agente.upper()}, ÉL ESTÁ CERCA.", font=("Courier New", 18), text_color="#888").place(relx=0.5, rely=0.45, anchor="center")
        if motivo == "tiempo":
            ctk.CTkButton(self, text="REINTENTAR", fg_color="#111", command=self.arrancar_interrogatorio).place(relx=0.4, rely=0.6, anchor="center")
            ctk.CTkButton(self, text="MENÚ", fg_color="#400", command=self.pantalla_menu).place(relx=0.6, rely=0.6, anchor="center")
        else:
            ctk.CTkButton(self, text="MENÚ PRINCIPAL", fg_color="#400", command=self.pantalla_menu).place(relx=0.5, rely=0.6, anchor="center")
            ctk.CTkButton(self, text="MODO APRENDIZAJE", fg_color="transparent", border_width=1, command=self.aprendizaje).place(relx=0.5, rely=0.75, anchor="center")

    def aprendizaje(self):
        # Modo simple para agregar un nuevo caso al archivo JSON.
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self, fg_color="#050505", border_width=1, border_color="#555")
        f.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.5)
        self.en = ctk.CTkEntry(f, placeholder_text="NOMBRE", width=300); self.en.pack(pady=10)
        self.er = ctk.CTkEntry(f, placeholder_text="RASGO", width=300); self.er.pack(pady=10)
        img_row = ctk.CTkFrame(f, fg_color="transparent")
        img_row.pack(pady=10)
        self.ei = ctk.CTkEntry(img_row, placeholder_text="IMAGEN OPCIONAL", width=240)
        self.ei.pack(side="left", padx=(0, 10))
        ctk.CTkButton(img_row, text="BUSCAR", fg_color="#222", width=90, command=self.elegir_imagen).pack(side="left")
        self.preview_panel = ctk.CTkFrame(f, fg_color="#111", border_width=1, border_color="#333", width=240, height=150)
        self.preview_panel.pack(pady=10)
        self.preview_panel.pack_propagate(False)
        self.preview_label = ctk.CTkLabel(self.preview_panel, text="SIN IMAGEN", text_color="#666")
        self.preview_label.pack(expand=True)
        btn_f = ctk.CTkFrame(f, fg_color="transparent")
        btn_f.pack(pady=20)
        ctk.CTkButton(btn_f, text="GUARDAR", fg_color="#400", command=self.guardar_ap).pack(side="left", padx=10)
        ctk.CTkButton(btn_f, text="CANCELAR", fg_color="#222", command=self.pantalla_menu).pack(side="left", padx=10)

    def elegir_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen del personaje",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.webp *.gif"), ("Todos los archivos", "*.*")],
        )
        if ruta and self.ei:
            self.ei.delete(0, "end")
            self.ei.insert(0, ruta)
            self.actualizar_previsualizacion(ruta)

    def actualizar_previsualizacion(self, ruta):
        if not hasattr(self, "preview_label") or not self.preview_label.winfo_exists():
            return

        if ruta and os.path.exists(ruta):
            try:
                img = ImageOps.fit(Image.open(ruta), (220, 120), centering=(0.5, 0.5))
                self.preview_imagen = ctk.CTkImage(img, size=(220, 120))
                self.preview_label.configure(image=self.preview_imagen, text="")
            except (OSError, ValueError, UnidentifiedImageError):
                self.preview_label.configure(image="", text="IMAGEN INVÁLIDA")
                self.preview_imagen = None
        else:
            self.preview_label.configure(image="", text="SIN IMAGEN")
            self.preview_imagen = None

    def guardar_ap(self):
        # Solo guarda cuando ambos campos tienen contenido.
        if self.en.get() and self.er.get():
            foto = self.ei.get().strip() if self.ei and self.ei.get().strip() else None
            self.motor.aprender_nuevo_caso(self.en.get(), self.er.get(), foto)
            self.pantalla_menu()

if __name__ == "__main__":
    app = InterrogatorioDefinitivo(); app.mainloop()