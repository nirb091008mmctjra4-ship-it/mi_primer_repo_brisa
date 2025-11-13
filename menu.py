import tkinter as tk
import login
import productos
import ventas
import sucursales
import empleados
import proveedores

def abrir_menu():
    menu = tk.Tk()
    menu.title("Menú Principal")
    menu.geometry("400x250") 
    
    menu.configure(bg="#FFD700")  
    
    def regresar_a_login():
        menu.destroy()
        login.mostrar_login()
    
    def abrir_productos():
        menu.withdraw() 
        ventana_productos = productos.abrir_productos()
        ventana_productos.wait_window() 
        menu.deiconify() 

    def abrir_ventas():
        menu.withdraw()
        ventana_ventas = ventas.abrir_ventas()
        ventana_ventas.wait_window()
        menu.deiconify()

    def abrir_sucursales():
        menu.withdraw()
        ventana_sucursales = sucursales.abrir_sucursales()
        ventana_sucursales.wait_window()
        menu.deiconify()

    def abrir_empleados():
        menu.withdraw()
        ventana_empleados = empleados.abrir_empleados()
        ventana_empleados.wait_window()
        menu.deiconify()

    def abrir_proveedores():
        menu.withdraw()
        ventana_proveedores = proveedores.abrir_proveedores()
        ventana_proveedores.wait_window()
        menu.deiconify()

    frame = tk.Frame(menu, bg="#000000", padx=10, pady=10) 
    frame.place(relx=0.5, rely=0.5, anchor="center") 

    tk.Label(frame, text="Starbucks", font=("Algerian", 20, "bold"), bg="#000000", fg="#FFD700").pack(pady=5)

    tk.Label(frame, text="Bienvenido al Menú Principal", font=("Algerian", 16, "bold"), bg="#000000", fg="#FFD700").pack(pady=10)

    botones = [
        ("Productos", abrir_productos),
        ("Ventas", abrir_ventas),
        ("Sucursales", abrir_sucursales),
        ("Empleados", abrir_empleados),
        ("Proveedores", abrir_proveedores),
        ("Cerrar Sesión", regresar_a_login)
    ]

    for texto, comando in botones:
        tk.Button(frame, text=texto, width=25, height=2, bg="#000000", fg="#FFD700", font=("Algerian", 12), command=comando).pack(pady=5)

    menu.mainloop()

if __name__ == "__main__":
    abrir_menu()
