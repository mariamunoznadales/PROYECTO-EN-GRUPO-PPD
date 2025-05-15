import tkinter as tk
from tkinter import ttk
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
import threading
import datetime

# Configura PubNub con tus claves
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-a2df94ac-367c-4af8-bc59-17fd53873061"
pnconfig.publish_key = "pub-c-d9c60cc2-2dc9-40ef-99d1-bcd402be43d3"
pnconfig.uuid = "interfaz_dashboard"
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

# Crear ventana
ventana = tk.Tk()
ventana.title("Centro de Control de Emergencias")
ventana.geometry("900x500")
ventana.configure(bg="#f4f4f4")


# Título
titulo = tk.Label(
    ventana,
    text="Panel de Emergencias en Tiempo Real",
    font=("Helvetica", 16, "bold"),
    bg="#f4f4f4",
    fg="#000000"  
)
titulo.pack(pady=10)

# Tabla
tabla = ttk.Treeview(ventana, columns=("Hora", "Tipo", "Ciudad", "Gravedad", "Estado"), show="headings")
for col in ("Hora", "Tipo", "Ciudad", "Gravedad", "Estado"):
    tabla.heading(col, text=col)
    tabla.column(col, width=150)
tabla.pack(expand=True, fill="both", padx=20, pady=10)

# Colores
tabla.tag_configure("red", background="#ffcccc", foreground="black")         # Crítica
tabla.tag_configure("orange", background="#ffe0b3", foreground="black")      # Alta
tabla.tag_configure("yellow", background="#ffff99", foreground="black")      # Moderada
tabla.tag_configure("lightgreen", background="#ccffcc", foreground="black")  # Baja



# Agregar emergencias a la tabla
def agregar_emergencia(mensaje):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    gravedad = mensaje.get("gravedad", "Desconocida")
    color = {
    "Crítica": "red",
    "Alta": "orange",
    "Media": "yellow",   
    "Baja": "lightgreen"
}.get(gravedad, "white")


    tabla.insert("", 0, values=(
        timestamp,
        mensaje.get("tipo", "¿?"),
        mensaje.get("ubicacion", {}).get("ciudad", "¿?"),
        gravedad,
        "Pendiente"
    ), tags=(color,))

# Escucha de PubNub
class EmergenciaListener(SubscribeCallback):
    def message(self, pubnub, message):
        ventana.after(0, lambda: agregar_emergencia(message.message))

def iniciar_escucha():
    pubnub.add_listener(EmergenciaListener())
    pubnub.subscribe().channels("emergencias").execute()

# Hilo separado para escuchar
threading.Thread(target=iniciar_escucha, daemon=True).start()

ventana.mainloop()
