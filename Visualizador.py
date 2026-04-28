import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class FiltroImagenesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtro Escala de Grises y Blur")
        self.root.geometry("800x600")

        self.imagen_original = None
        self.imagen_tk = None

        self.crear_interfaz()

    def crear_interfaz(self):
        panel = tk.Frame(self.root, height=50)
        panel.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Botones
        self.btn_cargar = tk.Button(panel, text="Cargar", command=self.cargar_imagen)
        self.btn_cargar.pack(side=tk.LEFT, padx=5)

        self.btn_gris = tk.Button(panel, text="Grises", command=self.aplicar_gris)
        self.btn_gris.pack(side=tk.LEFT, padx=5)

        # NUEVO BOTÓN: Blur
        self.btn_blur = tk.Button(panel, text="Blur (Desenfoque)", command=self.aplicar_blur)
        self.btn_blur.pack(side=tk.LEFT, padx=5)

        self.btn_nuevo = tk.Button(panel, text="Restaurar Original", command=self.restaurar_imagen)
        self.btn_nuevo.pack(side=tk.LEFT, padx=5)

        # Visor de Imagen
        self.visor_imagen = tk.Label(self.root, bg="#e0e0e0")
        self.visor_imagen.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Imágenes", "*.jpg *.png *.jpeg *.bmp")]
        )
        if ruta:
            self.imagen_original = Image.open(ruta)
            self.mostrar_imagen(self.imagen_original)

    def aplicar_gris(self):
        if self.imagen_original is None:
            messagebox.showwarning("Aviso", "Carga una imagen primero")
            return

        nueva_imagen = self.imagen_original.copy().convert("RGB")
        pixeles = nueva_imagen.load()
        ancho, alto = nueva_imagen.size

        for x in range(ancho):
            for y in range(alto):
                r, g, b = pixeles[x, y]
                gris = int(0.299 * r + 0.587 * g + 0.114 * b)
                pixeles[x, y] = (gris, gris, gris)

        self.mostrar_imagen(nueva_imagen)

    def aplicar_blur(self):
        if self.imagen_original is None:
            messagebox.showwarning("Aviso", "Carga una imagen primero")
            return

        # Imagen original de donde LEEREMOS (equivale a tu 'imagen')
        img_lectura = self.imagen_original.convert("RGB")
        pixeles_lectura = img_lectura.load()

        ancho, alto = img_lectura.size

        # Imagen nueva donde ESCRIBIREMOS (equivale a tu 'Bitmap resultado')
        nueva_imagen = Image.new("RGB", (ancho, alto))
        pixeles_nuevos = nueva_imagen.load()

        # Recorrido de Blur
        for x in range(ancho):
            for y in range(alto):
                sumaR = 0
                sumaG = 0
                sumaB = 0
                vecinos_validos = 0  # Contador para saber entre cuánto dividir

                # Recorremos la matriz 3x3 alrededor del píxel
                for i in range(-1, 2):  # range(-1, 2) equivale a de -1 a 1
                    for j in range(-1, 2):
                        nx = x + i
                        ny = y + j

                        # Validamos que el vecino no esté fuera de la imagen (evita errores en los bordes)
                        if 0 <= nx < ancho and 0 <= ny < alto:
                            r, g, b = pixeles_lectura[nx, ny]
                            sumaR += r
                            sumaG += g
                            sumaB += b
                            vecinos_validos += 1

                # Dividimos entre la cantidad de vecinos reales (normalmente 9, pero menos en los bordes)
                r_final = sumaR // vecinos_validos
                g_final = sumaG // vecinos_validos
                b_final = sumaB // vecinos_validos

                # Asignamos el nuevo píxel
                pixeles_nuevos[x, y] = (r_final, g_final, b_final)

        self.mostrar_imagen(nueva_imagen)

    def restaurar_imagen(self):
        if self.imagen_original:
            self.mostrar_imagen(self.imagen_original)

    def mostrar_imagen(self, img_pil):
        img_redimensionada = img_pil.copy()
        img_redimensionada.thumbnail((750, 500))

        self.imagen_tk = ImageTk.PhotoImage(img_redimensionada)
        self.visor_imagen.config(image=self.imagen_tk)


if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = FiltroImagenesApp(ventana_principal)
    ventana_principal.mainloop()