import os
import subprocess
import threading
import customtkinter as ctk
from pytube import YouTube
from PIL import Image, ImageTk

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")  # Modo oscuro

# Función para descargar el video
def descargar_video_youtube(url, nombre_archivo, path_destino, callback):
    try:
        if not os.path.exists(path_destino):
            os.makedirs(path_destino)
            print(f'Carpeta creada: {path_destino}')
        
        yt = YouTube(url)
        video = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        print(f'Descargando: {yt.title}')
        video.download(output_path=path_destino, filename=nombre_archivo)
        print(f'Video descargado en: {os.path.join(path_destino, nombre_archivo)}')
    except Exception as e:
        print(f'Ocurrió un error: {e}')
    finally:
        callback()

# Función para abrir el directorio en el explorador de archivos
def abrir_directorio(path_destino):
    if os.path.exists(path_destino):
        subprocess.Popen(f'explorer "{os.path.abspath(path_destino)}"')

# Callback cuando la descarga termina
def descarga_terminada():
    boton1.configure(state="normal")
    boton2.configure(state="normal")
    entry_url.delete(0, ctk.END)
    entry_nombre.delete(0, ctk.END)
    # gif_label.grid_remove()

# Función para iniciar la descarga en un hilo separado
def iniciar_descarga():
    url = entry_url.get()
    nombre_archivo = entry_nombre.get()

    # Salimos del bucle si no hay URL
    if not url:
        return

    # Si no hay nombre de archivo, usamos el nombre del video en YouTube
    if not nombre_archivo:
        yt = YouTube(url)
        nombre_archivo = yt.title

    nombre_archivo = nombre_archivo + ".mp4" # Se le añade la extensión para evitar problemas de entendimiento para windows
    ruta_destino = './videos'
    
    # Deshabilitar botones
    boton1.configure(state="disabled")
    boton2.configure(state="disabled")
    # gif_label.grid(row=2, column=2, padx=10, pady=10)
    
    hilo = threading.Thread(target=descargar_video_youtube, args=(url, nombre_archivo, ruta_destino, descarga_terminada))
    hilo.start()

# Configuración de la ventana principal
app = ctk.CTk()
app.geometry("500x200")
app.title("YT-Scrapper")

# Establecer icono personalizado
app.iconbitmap("YT-Scrapper_logo.ico")

# Campo de entrada para la URL
entry_url = ctk.CTkEntry(app, width=400, placeholder_text="URL")
entry_url.grid(row=0, column=0, padx=20, pady=10, columnspan=2)

# Campo de entrada para el nombre del archivo
entry_nombre = ctk.CTkEntry(app, width=400, placeholder_text="Nombre con el que se va a guardar")
entry_nombre.grid(row=1, column=0, padx=20, pady=10, columnspan=2)

# Botón para descargar el video
boton1 = ctk.CTkButton(app, text="Guardar", command=iniciar_descarga, fg_color="#ff0000", hover_color="#e60000", width=200)
boton1.grid(row=2, column=0, padx=20, pady=20, columnspan=2)

# Cargar imagen del ícono de carpeta
folder_icon = ctk.CTkImage(Image.open("folder_icon.png"), size=(20, 20))

# Botón para abrir el directorio con ícono de carpeta
def boton_abrir_directorio():
    ruta_destino = './videos'
    abrir_directorio(ruta_destino)

boton2 = ctk.CTkButton(app, image=folder_icon, text="", command=boton_abrir_directorio,fg_color="#ff0000", hover_color="#e60000", width=40, height=40)
boton2.grid(row=0, column=2, padx=10, pady=10)

# # Cargar gif de carga
# gif_frames = [ImageTk.PhotoImage(Image.open("loading.gif").convert("RGBA").resize((100,100)))]
# gif_label = ctk.CTkLabel(app, image=gif_frames[0])

# Ejecutar la aplicación
app.mainloop()
