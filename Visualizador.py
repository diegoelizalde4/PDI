import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class FiltroImagenesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtro Escala de Grises")
        self.root.geometry("800x600")

        # Variables para almacenar las imágenes
        self.imagen_original = None
        self.imagen_tk = None  # Para evitar que Python borre la imagen de la memoria

        self.crear_interfaz()

    def crear_interfaz(self):
        panel = tk.Frame(self.root, height=50)
        panel.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        #Botón Cargar
        self.btn_cargar = tk.Button(panel, text="Cargar", command=self.cargar_imagen)
        self.btn_cargar.pack(side=tk.LEFT, padx=5)

        #Botón Grises
        self.btn_gris = tk.Button(panel, text="Grises", command=self.aplicar_gris)
        self.btn_gris.pack(side=tk.LEFT, padx=5)

        #Bton Negativo
        self.btn_negativo = tk.Button(panel, text="Negativo", command=self.aplicar_negativo)
        self.btn_negativo.pack(side=tk.LEFT, padx=5)

        #Restaurar imagen a RGB
        self.btn_nuevo = tk.Button(panel, text="Restaurar Original", command=self.restaurar_imagen)
        self.btn_nuevo.pack(side=tk.LEFT, padx=5)

        #Visor de Imagen
        self.visor_imagen = tk.Label(self.root, bg="#e0e0e0")
        self.visor_imagen.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Imágenes", "*.jpg *.png *.jpeg *.bmp")]
        )
        if ruta:
            # Abrimos la imagen y la guardamos en la variable original
            self.imagen_original = Image.open(ruta)
            self.mostrar_imagen(self.imagen_original)

    def aplicar_gris(self):
        if self.imagen_original is None:
            messagebox.showwarning("Aviso", "Carga una imagen primero")
            return

        # Creamos una copia para no sobreescribir la original y aseguramos modo RGB
        nueva_imagen = self.imagen_original.copy().convert("RGB")

        # Obtenemos los píxeles para manipularlos rápido
        pixeles = nueva_imagen.load()
        ancho, alto = nueva_imagen.size

        # Inicio Escala de grises
        for x in range(ancho):
            for y in range(alto):
                # Extraer canales R, G, B
                r, g, b = pixeles[x, y]

                # Aplicar la fórmula
                gris = int(0.299 * r + 0.587 * g + 0.114 * b)

                # Asignar el nuevo color al píxel
                pixeles[x, y] = (gris, gris, gris)


        self.mostrar_imagen(nueva_imagen)

    def aplicar_negativo(self):
        if self.imagen_original is None:
            messagebox.showwarning("Aviso", "Carga una imagen primero")
            return

        # Creamos una copia para no sobreescribir la original y aseguramos modo RGB
        nueva_imagen = self.imagen_original.copy().convert("RGB")

        # Obtenemos los píxeles para manipularlos rápido
        pixeles = nueva_imagen.load()
        ancho, alto = nueva_imagen.size

        # Inicio Escala de grises
        for x in range(ancho):
            for y in range(alto):
                # Extraer canales R, G, B
                r, g, b = pixeles[x, y]

                # Aplicar la fórmula
                gris = int(255-r + 255-g + 255-b)

                # Asignar el nuevo color al píxel
                pixeles[x, y] = (gris, gris, gris)


        self.mostrar_imagen(nueva_imagen)
    def restaurar_imagen(self):

        if self.imagen_original:
            self.mostrar_imagen(self.imagen_original)

    def mostrar_imagen(self, img_pil):
        # Redimensionamos la imagen para que encaje en la ventana sin deformarse
        img_redimensionada = img_pil.copy()
        img_redimensionada.thumbnail((750, 500))

        # Convertimos para Tkinter y mostramos
        self.imagen_tk = ImageTk.PhotoImage(img_redimensionada)
        self.visor_imagen.config(image=self.imagen_tk)



if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = FiltroImagenesApp(ventana_principal)
    ventana_principal.mainloop()