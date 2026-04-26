import customtkinter as ctk
from PIL import Image, ImageOps
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def resolver_ruta_imagen(ruta):
    if not ruta:
        return None
    if os.path.isabs(ruta):
        return ruta
    return os.path.join(BASE_DIR, ruta)

def renderizar_expedientes(app):
    # Reemplaza la vista actual por un listado desplazable de perfiles.
    app.limpiar_pantalla()
    app.poner_fondo()
    
    scroll = ctk.CTkScrollableFrame(app, fg_color="#070707", border_width=1, border_color="#8B0000", label_text="ARCHIVOS CLASIFICADOS", label_font=("Courier New", 18, "bold"))
    scroll.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.7)
    
    # Crea una tarjeta por personaje con foto, nombre y biografia.
    for p in app.motor.personajes:
        card = ctk.CTkFrame(scroll, fg_color="#111", border_width=1, border_color="#333")
        card.pack(pady=10, padx=10, fill="x")
        
        info_f = ctk.CTkFrame(card, fg_color="transparent")
        info_f.pack(fill="x", padx=10, pady=10)
        
        foto = resolver_ruta_imagen(p.get('foto'))
        if foto and os.path.exists(foto):
            img_c = ImageOps.fit(Image.open(foto), (80, 100), centering=(0.5, 0.5))
            img = ctk.CTkImage(img_c, size=(80, 100))
            ctk.CTkLabel(info_f, image=img, text="").pack(side="left", padx=(0, 15))
        
        text_f = ctk.CTkFrame(info_f, fg_color="transparent")
        text_f.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(text_f, text=p['nombre'].upper(), font=("Courier New", 16, "bold"), text_color="#8B0000").pack(anchor="w")
        ctk.CTkLabel(text_f, text=p.get('bio', "Sin datos."), font=("Courier New", 12), text_color="#aaa", wraplength=500, justify="left").pack(anchor="w", pady=(5,0))
        
    # Boton de retorno al menu principal.
    ctk.CTkButton(app, text="VOLVER AL MENÚ", fg_color="#400", command=app.pantalla_menu).place(relx=0.5, rely=0.9, anchor="center")