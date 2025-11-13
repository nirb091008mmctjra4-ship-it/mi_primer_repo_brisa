
import tkinter as tk


window = tk.Tk()

window.title("mi primer formulario abraham velazquez salinas")
window.geometry("400x300")

titulo_etiqueta = tk.Label(window,text="bienvenido abraham velazquez salinas")
titulo_etiqueta.place(x=100, y=10)
nombre_etiqueta = tk.Label(window, text="Nombre:")
nombre_etiqueta.place(x=50, y=50) 


nombre_cajatexto = tk.Entry(window)
nombre_cajatexto.place(x=150, y=50)


email_etiqueta = tk.Label(window, text="Edad:")
email_etiqueta.place(x=50, y=100)


email_cajatexto = tk.Entry(window)
email_cajatexto.place(x=150, y=100)


boton_clic = tk.Button(window, text="Enviar")
boton_clic.pack(pady=10)
boton_clic.place(x=200, y=150)



window.mainloop()