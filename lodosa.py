import tkinter as tk
from tkinter import ttk, simpledialog

COSTO_CASILLA = 15

# Color de cada tipo de edificio
COLORES = {
    "vivienda": "#d9ead3",
    "gobierno": "#f4cccc",
    "hospital": "#ffffff",
    "escuela": "#fff2cc",
    "servicio": "#cfe2f3",
    "puente": "#c8a36a",
}


class Edificio:
    """Una casa o edificio de la ciudad."""

    def __init__(self, nombre, tipo, x, y):
        self.nombre = nombre
        self.tipo = tipo
        self.x = x
        self.y = y


class Calle:
    """Una calle que une dos edificios. 'casillas' es None si aun no se cuenta."""

    def __init__(self, nombre, origen, destino, casillas=None):
        self.nombre = nombre
        self.origen = origen      # nombre del edificio donde empieza
        self.destino = destino    # nombre del edificio donde termina
        self.casillas = casillas

    def costo(self):
        return self.casillas * COSTO_CASILLA

    def une(self, edificio):
        return edificio in (self.origen, self.destino)

    def otro_extremo(self, edificio):
        return self.destino if edificio == self.origen else self.origen


class Piscina:
    """La piscina del alcalde: esta en el patio de un edificio, no tiene calle propia."""

    def __init__(self, nombre, detras_de, costo=None):
        self.nombre = nombre
        self.detras_de = detras_de   # nombre del edificio donde esta el patio
        self.costo = costo           # None = todavia sin precio


class Ciudad:
    """Guarda los edificios y las calles, y hace los calculos."""

    def __init__(self):
        self.edificios = {}   # nombre -> Edificio
        self.calles = []      # lista de Calle
        self.piscina = None

    def agregar_edificio(self, nombre, tipo, x, y):
        self.edificios[nombre] = Edificio(nombre, tipo, x, y)

    def agregar_calle(self, nombre, origen, destino, casillas=None):
        self.calles.append(Calle(nombre, origen, destino, casillas))

    def kruskal(self):
        """Elige las calles mas baratas que unen todos los edificios sin hacer circulos."""
        grupo = {nombre: nombre for nombre in self.edificios}  # cada edificio empieza solo
        elegidas = []
        conocidas = [c for c in self.calles if c.casillas is not None]
        for calle in sorted(conocidas, key=lambda c: c.casillas):
            g1 = grupo[calle.origen]
            g2 = grupo[calle.destino]
            if g1 != g2:                      # si estan en grupos distintos, no hay circulo
                elegidas.append(calle)
                for nombre in grupo:          # juntamos los dos grupos en uno
                    if grupo[nombre] == g2:
                        grupo[nombre] = g1
        conectado = len(elegidas) == len(self.edificios) - 1
        return elegidas, conectado

    def camino(self, salida, llegada, pavimentadas):
        """Busca la ruta de un edificio a otro usando solo calles pavimentadas."""
        pendientes = [(salida, [])]
        visitados = {salida}
        while pendientes:
            actual, ruta = pendientes.pop()
            if actual == llegada:
                return ruta
            for calle in pavimentadas:
                if calle.une(actual):
                    siguiente = calle.otro_extremo(actual)
                    if siguiente not in visitados:
                        visitados.add(siguiente)
                        pendientes.append((siguiente, ruta + [calle]))
        return None

    def sin_salida(self, pavimentadas):
        """Edificios a los que solo llega una calle (ruta unica)."""
        resultado = []
        for nombre in self.edificios:
            sus_calles = [c for c in pavimentadas if c.une(nombre)]
            if len(sus_calles) == 1:
                resultado.append((nombre, sus_calles[0]))
        return resultado


def crear_ciudad():
    """Aqui se definen los edificios y las calles. Cambia los nombres y casillas a tu gusto."""
    ciudad = Ciudad()
    # nombre, tipo, x, y  (la posicion sale de la foto del mapa)
    ciudad.agregar_edificio("Alcaldia", "gobierno", 420, 165)
    ciudad.agregar_edificio("Hospital Central", "hospital", 600, 255)
    ciudad.agregar_edificio("Escuela Bolivar", "escuela", 795, 150)
    ciudad.agregar_edificio("Casa Perez", "vivienda", 1030, 250)
    ciudad.agregar_edificio("Casa Rojas", "vivienda", 290, 385)
    ciudad.agregar_edificio("Mercado", "servicio", 720, 375)
    ciudad.agregar_edificio("Casa Mendoza", "vivienda", 975, 510)
    ciudad.agregar_edificio("Bomberos", "servicio", 530, 510)
    ciudad.agregar_edificio("Casa Salazar", "vivienda", 270, 600)
    ciudad.agregar_edificio("Casa Torres", "vivienda", 690, 640)
    ciudad.agregar_edificio("Puente", "puente", 510, 600)

    # nombre de la calle, desde, hasta, casillas (None = todavia sin contar)
    # Calles negras (tu ruta)
    ciudad.agregar_calle("Av. Principal", "Alcaldia", "Hospital Central", 3)
    ciudad.agregar_calle("Calle Salud", "Hospital Central", "Mercado", 3)
    ciudad.agregar_calle("Calle Escuela", "Escuela Bolivar", "Mercado", 2)
    ciudad.agregar_calle("Calle Norte", "Escuela Bolivar", "Casa Perez", 3)
    ciudad.agregar_calle("Calle Este", "Casa Perez", "Casa Mendoza", 3)
    ciudad.agregar_calle("Calle Oeste", "Casa Rojas", "Casa Salazar", 2)
    ciudad.agregar_calle("Calle del Rio", "Casa Salazar", "Puente", 2)
    ciudad.agregar_calle("Calle del Puente", "Puente", "Casa Torres", 1)
    ciudad.agregar_calle("Calle Central", "Mercado", "Casa Torres", 2)
    ciudad.agregar_calle("Calle Bomberos", "Bomberos", "Casa Torres", 2)
    # Calles de colores (faltan los numeros)
    ciudad.agregar_calle("Calle 1", "Alcaldia", "Escuela Bolivar")
    ciudad.agregar_calle("Calle 2", "Alcaldia", "Casa Rojas")
    ciudad.agregar_calle("Calle 3", "Hospital Central", "Casa Rojas")
    ciudad.agregar_calle("Calle 4", "Hospital Central", "Escuela Bolivar")
    ciudad.agregar_calle("Calle 5", "Hospital Central", "Bomberos")
    ciudad.agregar_calle("Calle 6", "Escuela Bolivar", "Casa Mendoza")
    ciudad.agregar_calle("Calle 7", "Mercado", "Casa Mendoza")
    ciudad.agregar_calle("Calle 8", "Mercado", "Bomberos")
    ciudad.agregar_calle("Calle 9", "Casa Rojas", "Bomberos")
    ciudad.agregar_calle("Calle 10", "Casa Salazar", "Bomberos")
    ciudad.agregar_calle("Calle 11", "Casa Torres", "Casa Mendoza")

    # Piscina en el patio de la Alcaldia (costo aparte, se suma al total)
    ciudad.piscina = Piscina("Piscina", "Alcaldia", None)
    return ciudad


class AppLodosa:
    """La ventana del programa."""

    def __init__(self, ventana):
        self.ventana = ventana
        self.ciudad = crear_ciudad()
        self.recorrido = []   # calles del recorrido que se esta mostrando
        ventana.title("La Ciudad Lodosa")
        ventana.geometry("1150x700")

        self.lienzo = tk.Canvas(ventana, bg="#f7f3e8")
        self.lienzo.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        self.lienzo.bind("<Configure>", lambda e: self.dibujar())
        self.lienzo.bind("<Button-1>", self.clic_en_calle)

        panel = tk.Frame(ventana, width=300)
        panel.pack(side="right", fill="y", padx=8, pady=8)
        panel.pack_propagate(False)

        nombres = [n for n in self.ciudad.edificios if n != "Puente"]
        tk.Label(panel, text="Salida:").pack(anchor="w")
        self.salida = ttk.Combobox(panel, values=nombres, state="readonly")
        self.salida.set(nombres[0])
        self.salida.pack(fill="x")
        tk.Label(panel, text="Destino:").pack(anchor="w", pady=(6, 0))
        self.destino = ttk.Combobox(panel, values=nombres, state="readonly")
        self.destino.set(nombres[-1])
        self.destino.pack(fill="x")
        tk.Button(panel, text="Ver recorrido (ida y retorno)",
                  command=self.ver_recorrido).pack(fill="x", pady=8)

        tk.Button(panel, text="Presupuesto final",
                  command=self.mostrar_presupuesto).pack(fill="x")
        tk.Button(panel, text="Clases y objetos",
                  command=self.mostrar_clases).pack(fill="x", pady=(4, 8))

        self.texto = tk.Text(panel, wrap="word", font=("Arial", 10))
        self.texto.pack(fill="both", expand=True)
        self.dibujar()

    # ---------- posicion en pantalla ----------
    def convertir(self, x, y):
        """Ajusta las coordenadas de la foto (1246x864) al tamano de la ventana."""
        ancho = max(self.lienzo.winfo_width(), 300)
        alto = max(self.lienzo.winfo_height(), 200)
        escala = min(ancho / 1246, alto / 864)
        return x * escala + (ancho - 1246 * escala) / 2, y * escala + (alto - 864 * escala) / 2

    def punto(self, nombre):
        e = self.ciudad.edificios[nombre]
        return self.convertir(e.x, e.y)

    # ---------- dibujo ----------
    def dibujar(self):
        self.lienzo.delete("all")
        pavimentadas, _ = self.ciudad.kruskal()

        for calle in self.ciudad.calles:
            x1, y1 = self.punto(calle.origen)
            x2, y2 = self.punto(calle.destino)
            if calle in self.recorrido:
                self.lienzo.create_line(x1, y1, x2, y2, fill="#e69138", width=8)
            elif calle in pavimentadas:
                self.lienzo.create_line(x1, y1, x2, y2, fill="#222", width=6)
            elif calle.casillas is None:
                self.lienzo.create_line(x1, y1, x2, y2, fill="#bbb", width=2, dash=(6, 4))
            else:
                self.lienzo.create_line(x1, y1, x2, y2, fill="#aaa", width=2)
            numero = "?" if calle.casillas is None else str(calle.casillas)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.lienzo.create_text(mx, my, text=f"{calle.nombre}\n{numero}",
                                    font=("Arial", 8, "bold"), fill="#222",
                                    justify="center")

        for e in self.ciudad.edificios.values():
            x, y = self.convertir(e.x, e.y)
            self.lienzo.create_rectangle(x - 45, y - 14, x + 45, y + 14,
                                         fill=COLORES[e.tipo], outline="#444", width=2)
            self.lienzo.create_text(x, y, text=e.nombre, font=("Arial", 9, "bold"))
        self.dibujar_piscina()
        self.mostrar_resumen()

    def dibujar_piscina(self):
        p = self.ciudad.piscina
        e = self.ciudad.edificios[p.detras_de]
        x, y = self.convertir(e.x, e.y - 60)   # detras (arriba) del edificio
        self.lienzo.create_oval(x - 40, y - 14, x + 40, y + 14,
                                fill="#9fd3f0", outline="#2a6f97", width=2)
        precio = "?" if p.costo is None else f"${p.costo}"
        self.lienzo.create_text(x, y, text=f"{p.nombre} {precio}", font=("Arial", 8, "bold"))

    def mostrar_resumen(self):
        pavimentadas, conectado = self.ciudad.kruskal()
        casillas = sum(c.casillas for c in pavimentadas)
        faltan = sum(1 for c in self.ciudad.calles if c.casillas is None)
        t = self.texto
        t.delete("1.0", "end")
        pavimento = casillas * COSTO_CASILLA
        piscina = self.ciudad.piscina.costo or 0
        t.insert("end", f"Calles a pavimentar: {len(pavimentadas)}\n")
        t.insert("end", f"Casillas: {casillas}\n")
        t.insert("end", f"Pavimentacion: ${pavimento}\n")
        t.insert("end", f"Piscina: ${piscina}\n")
        t.insert("end", f"TOTAL: ${pavimento + piscina}\n")
        if faltan:
            t.insert("end", f"\nFaltan {faltan} calles por contar (clic sobre su nombre).\n")
        t.insert("end", "\nEdificios con una sola calle:\n")
        for nombre, calle in self.ciudad.sin_salida(pavimentadas):
            t.insert("end", f"- {nombre} (solo por {calle.nombre})\n")
        if self.recorrido:
            self.escribir_recorrido()

    # ---------- acciones ----------
    def ver_recorrido(self):
        pavimentadas, _ = self.ciudad.kruskal()
        ruta = self.ciudad.camino(self.salida.get(), self.destino.get(), pavimentadas)
        self.recorrido = ruta if ruta else []
        self.dibujar()

    def escribir_recorrido(self):
        salida, destino = self.salida.get(), self.destino.get()
        casillas = sum(c.casillas for c in self.recorrido)
        t = self.texto
        t.insert("end", f"\n--- Recorrido ---\nIDA: {salida} -> {destino}\n")
        actual = salida
        for calle in self.recorrido:
            actual = calle.otro_extremo(actual)
            t.insert("end", f"  por {calle.nombre} hasta {actual}\n")
        t.insert("end", f"Casillas de la ida: {casillas}\n")
        t.insert("end", f"RETORNO: {destino} -> {salida} (mismas calles al reves)\n")
        t.insert("end", f"Casillas del retorno: {casillas}\n")
        t.insert("end", f"Total ida y vuelta: {casillas * 2} casillas\n")
        t.insert("end", "(Es distancia recorrida, no se suma al costo de pavimentar.)\n")

    def abrir_ventana(self, titulo, contenido):
        """Abre una ventana aparte con un texto."""
        v = tk.Toplevel(self.ventana)
        v.title(titulo)
        v.geometry("620x620")
        caja = tk.Text(v, wrap="word", font=("Consolas", 10))
        caja.pack(fill="both", expand=True)
        caja.insert("end", contenido)

    def mostrar_presupuesto(self):
        """Presupuesto de la ciudad y de la piscina, por separado."""
        pavimentadas, _ = self.ciudad.kruskal()
        total_casillas = sum(c.casillas for c in pavimentadas)
        costo_ciudad = total_casillas * COSTO_CASILLA
        p = self.ciudad.piscina
        texto = "PRESUPUESTO DE LA CIUDAD (pavimentacion)\n"
        texto += f"Cada casilla cuesta ${COSTO_CASILLA}\n\n"
        for c in pavimentadas:
            texto += f"{c.nombre} ({c.origen} - {c.destino}): {c.casillas} casillas = ${c.costo()}\n"
        texto += f"\nTotal: {total_casillas} casillas\n"
        texto += f"SUBTOTAL CIUDAD: ${costo_ciudad}\n"
        texto += "\nPRESUPUESTO DE LA PISCINA\n"
        if p.costo is None:
            texto += f"{p.nombre} (detras de {p.detras_de}): sin precio definido\n"
            texto += "SUBTOTAL PISCINA: pendiente\n"
        else:
            texto += f"{p.nombre} (detras de {p.detras_de}): ${p.costo}\n"
            texto += f"SUBTOTAL PISCINA: ${p.costo}\n"
        texto += f"\nTOTAL GENERAL: ${costo_ciudad + (p.costo or 0)}\n"
        if any(c.casillas is None for c in self.ciudad.calles):
            texto += "\nOjo: faltan calles por contar, el total puede bajar si alguna ruta resulta mas barata.\n"
        self.abrir_ventana("Presupuesto final", texto)

    def mostrar_clases(self):
        """Explica las clases y lista los objetos que existen en este momento."""
        c = self.ciudad
        texto = "CLASES\n\n"
        texto += "Edificio - atributos: nombre, tipo, x, y\n"
        texto += "Calle - atributos: nombre, origen, destino, casillas\n"
        texto += "         metodos: costo(), une(), otro_extremo()\n"
        texto += "Piscina - atributos: nombre, detras_de, costo\n"
        texto += "Ciudad - atributos: edificios, calles, piscina\n"
        texto += "         metodos: agregar_edificio(), agregar_calle(), kruskal(),\n"
        texto += "                  camino(), sin_salida()\n"
        texto += "AppLodosa - la ventana: dibujar(), ver_recorrido(), mostrar_presupuesto()...\n"
        texto += f"\nOBJETOS CREADOS\n\nEdificios ({len(c.edificios)}):\n"
        for e in c.edificios.values():
            texto += f"  {e.nombre} - tipo {e.tipo}\n"
        texto += f"\nCalles ({len(c.calles)}):\n"
        for calle in c.calles:
            casillas = "sin contar" if calle.casillas is None else f"{calle.casillas} casillas"
            texto += f"  {calle.nombre}: {calle.origen} - {calle.destino} ({casillas})\n"
        texto += f"\nPiscina (1): {c.piscina.nombre}, detras de {c.piscina.detras_de}\n"
        texto += "\n1 objeto Ciudad y 1 objeto AppLodosa.\n"
        self.abrir_ventana("Clases y objetos", texto)

    def clic_en_calle(self, evento):
        """Clic en una calle: pide sus casillas. Clic en la piscina: pide su costo."""
        p = self.ciudad.piscina
        e = self.ciudad.edificios[p.detras_de]
        px, py = self.convertir(e.x, e.y - 60)
        if abs(evento.x - px) < 40 and abs(evento.y - py) < 14:
            n = simpledialog.askinteger("Piscina", "Costo de la piscina ($):",
                                        parent=self.ventana, minvalue=0)
            if n is not None:
                p.costo = n
                self.dibujar()
            return
        for calle in self.ciudad.calles:
            x1, y1 = self.punto(calle.origen)
            x2, y2 = self.punto(calle.destino)
            if abs(evento.x - (x1 + x2) / 2) < 30 and abs(evento.y - (y1 + y2) / 2) < 15:
                n = simpledialog.askinteger("Casillas", f"Casillas de {calle.nombre}:",
                                            parent=self.ventana, minvalue=1, maxvalue=20)
                if n is not None:
                    calle.casillas = n
                    self.recorrido = []
                    self.dibujar()
                return


if __name__ == "__main__":
    ventana = tk.Tk()
    AppLodosa(ventana)
    ventana.mainloop()
