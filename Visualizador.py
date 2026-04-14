import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk



def seleccionar_imagen():
    # Abrir el explorador de archivos
    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[
            ("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("Todos los archivos", "*.*")
        ]
    )

    if ruta_archivo:
        try:
            # Abrir la imagen
            img = Image.open(ruta_archivo)

            # Redimensionar la imagen para que quepa en la ventana (mantiene la proporción)
            img.thumbnail((750, 500))

            # Convertir la imagen para que Tkinter la pueda usar
            img_tk = ImageTk.PhotoImage(img)

            # Actualizar la etiqueta (Label) para mostrar la imagen
            visor_imagen.config(image=img_tk)
            visor_imagen.image = img_tk  # ¡Muy importante! Evita que la memoria borre la imagen

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cargar la imagen:\n{e}")


# 1. Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Mi Visualizador de Imágenes")
ventana.geometry("800x600")
ventana.config(bg="#f0f0f0")  # Color de fondo gris claro

# 2. Configuración del Botón
btn_seleccionar = tk.Button(
    ventana,
    text="Seleccionar Archivo...",
    command=seleccionar_imagen,
    font=("Arial", 12, "bold"),
    padx=10,
    pady=5
)
btn_seleccionar.pack(pady=20)  # Lo colocamos arriba con un pequeño margen

# 3. Configuración del visor de imagen (usamos un Label)
visor_imagen = tk.Label(ventana, bg="#f0f0f0")
visor_imagen.pack(expand=True)  # Se expande para ocupar el resto del espacio

# Iniciar la aplicación
ventana.mainloop()