import tkinter as tk
CREMA = "#F3EBDD"
GRAFITO = "#2F3B46"
TEAL = "#2A9D8F"
TEAL_OSCURO = "#207A70"
TERRACOTA = "#C96A4A"
TERRACOTA_OSCURO = "#A95439"
GRIS = "#D6D0C4"
GRIS_OSCURO = "#BBB5AB"
FUNCION = "#718096"
FUNCION_OSCURO = "#596879"
BLANCO = "#FFFFFF"
ROJO = "#D1495B"

ventana = tk.Tk()
ventana.title("Calculadora")
ventana.geometry("500x730")
ventana.configure(bg=CREMA)
ventana.resizable(False, False)

numero_actual = ""
numero_anterior = ""
operacion = ""
nueva_operacion = False
modo_error = False
historial_datos = []


def actualizar_pantalla():
    if modo_error:
        return
    texto = numero_actual if numero_actual != "" else "0.00"
    pantalla_valor.config(text=texto, fg=BLANCO)


def agregar_numero(numero):
    global numero_actual, nueva_operacion, modo_error

    if modo_error:
        borrar_todo()

    if nueva_operacion:
        numero_actual = ""
        nueva_operacion = False
        pantalla_operacion.config(text="")

    numero_actual += str(numero)
    actualizar_pantalla()


def agregar_punto():
    global numero_actual, nueva_operacion, modo_error

    if modo_error:
        borrar_todo()

    if nueva_operacion:
        numero_actual = ""
        nueva_operacion = False
        pantalla_operacion.config(text="")
   
    if "." in numero_actual:
        return

    if numero_actual == "":
        numero_actual = "0."
    else:
        numero_actual += "."

    actualizar_pantalla()


def cambiar_signo():
    global numero_actual, modo_error
    if modo_error:
        return
    if numero_actual == "" or numero_actual == "0.00":
        return
    
    if numero_actual.startswith("-"):
        numero_actual = numero_actual[1:]
    else:
        numero_actual = "-" + numero_actual
    actualizar_pantalla()


def calcular_porcentaje():
    global numero_actual, numero_anterior, operacion, modo_error
    if modo_error or numero_actual == "":
        return
    
    try:
        val = float(numero_actual)
       
        if numero_anterior != "" and operacion in ("+", "-"):
            num_ant = float(numero_anterior)
            val = num_ant * (val / 100)
        elif numero_anterior != "" and operacion in ("×", "÷"):
            val = val / 100
        else:
            val = val / 100
            
        numero_actual = f"{val:.2f}"
        actualizar_pantalla()
    except ValueError:
        pass


def seleccionar_operacion(op):
    global numero_actual, numero_anterior, operacion, nueva_operacion, modo_error

    if modo_error:
        return
   
    if numero_actual == "":
        return
    
    if numero_anterior != "" and operacion != "" and not nueva_operacion:
        calcular()
        if modo_error:
            return

    numero_anterior = numero_actual
    operacion = op
    nueva_operacion = True

    pantalla_operacion.config(text=f"{numero_anterior} {operacion}")


def calcular():
    global numero_actual, numero_anterior, operacion, nueva_operacion, modo_error

    if modo_error:
        return

    if numero_anterior == "" or numero_actual == "" or operacion == "":
        return

    try:
        num1 = float(numero_anterior)
        num2 = float(numero_actual)

        if operacion == "+":
            resultado = num1 + num2
        elif operacion == "-":
            resultado = num1 - num2
        elif operacion == "×":
            resultado = num1 * num2
        elif operacion == "÷":
            if num2 == 0:
                modo_error = True
                pantalla_operacion.config(text=f"{numero_anterior} ÷ {numero_actual}")
                pantalla_valor.config(text="⚠ Operación no válida", fg=ROJO)
                return

            resultado = num1 / num2
        else:
            return

        resultado_texto = f"{resultado:.2f}"
        operacion_completa = (
            f"{numero_anterior} {operacion} {numero_actual} = {resultado_texto}"
        )

        historial_datos.append((operacion_completa, resultado_texto))

        pantalla_operacion.config(
            text=f"{numero_anterior} {operacion} {numero_actual} ="
        )
        pantalla_valor.config(text=resultado_texto, fg=TEAL)
    
        numero_actual = resultado_texto
        numero_anterior = ""
        operacion = ""
        nueva_operacion = True

    except ValueError:
        modo_error = True
        pantalla_valor.config(text="⚠ Error", fg=ROJO)


def borrar_todo():
    global numero_actual, numero_anterior, operacion, nueva_operacion, modo_error

    numero_actual = ""
    numero_anterior = ""
    operacion = ""
    nueva_operacion = False
    modo_error = False

    pantalla_operacion.config(text="")
    pantalla_valor.config(text="0.00", fg=BLANCO)


def borrar_digito():
    global numero_actual, nueva_operacion

    if modo_error:
        return

    if nueva_operacion:
        numero_actual = ""
        nueva_operacion = False

    if numero_actual:
        numero_actual = numero_actual[:-1]

    actualizar_pantalla()


def reutilizar_resultado(valor, ventana_historial):
    global numero_actual, numero_anterior, operacion, nueva_operacion, modo_error

    numero_actual = valor
    numero_anterior = ""
    operacion = ""
    nueva_operacion = False
    modo_error = False

    pantalla_operacion.config(text="Resultado reutilizado")
    pantalla_valor.config(text=valor, fg=TEAL)
    ventana_historial.destroy()


def limpiar_historial(lista_frame, ventana_historial):
    historial_datos.clear()
    ventana_historial.destroy()


def abrir_historial():
    historial_ventana = tk.Toplevel(ventana)
    historial_ventana.title("Historial")
    historial_ventana.geometry("430x600")
    historial_ventana.configure(bg=CREMA)
    historial_ventana.resizable(False, False)

    tk.Label(
        historial_ventana,
        text="HISTORIAL",
        font=("Arial", 20, "bold"),
        bg=CREMA,
        fg=GRAFITO
    ).pack(pady=18)

    lista_frame = tk.Frame(historial_ventana, bg=CREMA)
    lista_frame.pack(fill="both", expand=True)

    if not historial_datos:
        tk.Label(
            lista_frame,
            text="No hay operaciones todavía",
            font=("Arial", 14),
            bg=CREMA,
            fg=GRAFITO
        ).pack(pady=50)
    else:
        for texto, resultado in reversed(historial_datos):
            tarjeta = tk.Frame(lista_frame, bg=BLANCO, bd=1, relief="solid")
            tarjeta.pack(fill="x", padx=25, pady=6)

            tk.Label(
                tarjeta,
                text=texto,
                font=("Arial", 10),
                bg=BLANCO,
                fg=GRAFITO,
                wraplength=340,
                justify="left"
            ).pack(anchor="w", padx=12, pady=(8, 3))

            tk.Button(
                tarjeta,
                text=f"Usar resultado: {resultado}",
                font=("Arial", 11, "bold"),
                bg=TEAL,
                fg=BLANCO,
                bd=0,
                padx=10,
                pady=5,
                command=lambda v=resultado: reutilizar_resultado(v, historial_ventana)
            ).pack(anchor="e", padx=12, pady=(3, 8))

        tk.Button(
            historial_ventana,
            text="LIMPIAR HISTORIAL",
            font=("Arial", 11, "bold"),
            bg=TERRACOTA,
            fg=BLANCO,
            bd=0,
            padx=12,
            pady=8,
            command=lambda: limpiar_historial(lista_frame, historial_ventana)
        ).pack(pady=12)


def crear_boton_redondo(texto, fila, columna, color, color_hover, comando):
    tam = 78

    canvas = tk.Canvas(
        teclado,
        width=tam,
        height=tam,
        bg=CREMA,
        highlightthickness=0,
        cursor="hand2"
    )

    circulo = canvas.create_oval(
        5, 5, tam - 5, tam - 5,
        fill=color,
        outline=""
    )

    color_texto = GRAFITO if color == GRIS else BLANCO

    canvas.create_text(
        tam // 2,
        tam // 2,
        text=texto,
        font=("Arial", 13, "bold"),
        fill=color_texto
    )

    def ejecutar(event):
        comando()

    def entrar(event):
        canvas.itemconfig(circulo, fill=color_hover)

    def salir(event):
        canvas.itemconfig(circulo, fill=color)

    canvas.bind("<Button-1>", ejecutar)
    canvas.bind("<Enter>", entrar)
    canvas.bind("<Leave>", salir)

    canvas.grid(row=fila, column=columna, padx=7, pady=6)


encabezado = tk.Frame(ventana, bg=CREMA)
encabezado.pack(fill="x", padx=35, pady=(20, 5))

tk.Label(
    encabezado,
    text="CALCULADORA",
    font=("Arial", 18, "bold"),
    bg=CREMA,
    fg=GRAFITO
).pack(side="left")

tk.Button(
    encabezado,
    text="HISTORIAL",
    font=("Arial", 10, "bold"),
    bg=TEAL,
    fg=BLANCO,
    bd=0,
    padx=10,
    pady=5,
    cursor="hand2",
    command=abrir_historial
).pack(side="right")


display = tk.Frame(ventana, bg=GRAFITO, height=145)
display.pack(fill="x", padx=35, pady=10)
display.pack_propagate(False)

pantalla_operacion = tk.Label(
    display,
    text="",
    font=("Arial", 13),
    bg=GRAFITO,
    fg="#B8C2CC",
    anchor="e"
)
pantalla_operacion.pack(fill="x", padx=20, pady=(18, 0))

pantalla_valor = tk.Label(
    display,
    text="0.00",
    font=("Arial", 30, "bold"),
    bg=GRAFITO,
    fg=BLANCO,
    anchor="e"
)
pantalla_valor.pack(fill="both", padx=20, pady=(4, 12))


teclado = tk.Frame(ventana, bg=CREMA)
teclado.pack(pady=5)

crear_boton_redondo("AC", 0, 0, FUNCION, FUNCION_OSCURO, borrar_todo)
crear_boton_redondo("DEL", 0, 1, FUNCION, FUNCION_OSCURO, borrar_digito)
crear_boton_redondo(".", 0, 2, GRIS, GRIS_OSCURO, agregar_punto)
crear_boton_redondo("÷", 0, 3, TEAL, TEAL_OSCURO, lambda: seleccionar_operacion("÷"))

crear_boton_redondo("7", 1, 0, GRIS, GRIS_OSCURO, lambda: agregar_numero(7))
crear_boton_redondo("8", 1, 1, GRIS, GRIS_OSCURO, lambda: agregar_numero(8))
crear_boton_redondo("9", 1, 2, GRIS, GRIS_OSCURO, lambda: agregar_numero(9))
crear_boton_redondo("×", 1, 3, TEAL, TEAL_OSCURO, lambda: seleccionar_operacion("×"))

crear_boton_redondo("4", 2, 0, GRIS, GRIS_OSCURO, lambda: agregar_numero(4))
crear_boton_redondo("5", 2, 1, GRIS, GRIS_OSCURO, lambda: agregar_numero(5))
crear_boton_redondo("6", 2, 2, GRIS, GRIS_OSCURO, lambda: agregar_numero(6))
crear_boton_redondo("−", 2, 3, TEAL, TEAL_OSCURO, lambda: seleccionar_operacion("-"))

crear_boton_redondo("1", 3, 0, GRIS, GRIS_OSCURO, lambda: agregar_numero(1))
crear_boton_redondo("2", 3, 1, GRIS, GRIS_OSCURO, lambda: agregar_numero(2))
crear_boton_redondo("3", 3, 2, GRIS, GRIS_OSCURO, lambda: agregar_numero(3))
crear_boton_redondo("+", 3, 3, TEAL, TEAL_OSCURO, lambda: seleccionar_operacion("+"))

crear_boton_redondo("±", 4, 0, GRIS, GRIS_OSCURO, cambiar_signo)
crear_boton_redondo("0", 4, 1, GRIS, GRIS_OSCURO, lambda: agregar_numero(0))
crear_boton_redondo("%", 4, 2, GRIS, GRIS_OSCURO, calcular_porcentaje)
crear_boton_redondo("=", 4, 3, TERRACOTA, TERRACOTA_OSCURO, calcular)

ventana.mainloop()