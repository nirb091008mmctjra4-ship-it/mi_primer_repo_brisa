import tkinter as tk
from tkinter import messagebox
import menu

usuario_correcto = "abraham"
pass_correcto = "1234"

def mostrar_login():
    ventana_login = tk.Tk()
    ventana_login.title("Login")
    ventana_login.geometry("300x200")
    ventana_login.configure(bg="#FFD700")  

    tk.Label(ventana_login, text="Starbucks", font=("Algerian", 24, "bold"), bg="#FFD700", fg="#000000").pack(pady=10)

    def verificar_login():
        usuario = entry_usuario.get()
        contraseña = entry_contraseña.get()
        if not usuario or not contraseña:           
            messagebox.showwarning("Campos vacíos", "Por favor, ingrese usuario y contraseña.")
            return
        if usuario == usuario_correcto and contraseña == pass_correcto:
            messagebox.showinfo("Datos correctos", f"¡Bienvenido, {usuario}!")
            ventana_login.destroy()
            menu.abrir_menu()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.") 
                      
    tk.Label(ventana_login, text="Usuario:", bg="#FFD700").pack(pady=5)
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack()
    entry_usuario.focus()
        
    tk.Label(ventana_login, text="Contraseña:", bg="#FFD700").pack(pady=5)
    entry_contraseña = tk.Entry(ventana_login, show="*")
    entry_contraseña.pack()
    
    tk.Button(ventana_login, text="Iniciar sesión", command=verificar_login, bg="#000000", fg="#FFD700").pack(pady=10)
    tk.Button(ventana_login, text="Salir", command=ventana_login.destroy, bg="#000000", fg="#FFD700").pack(pady=5)
    
    ventana_login.mainloop()
    
if __name__ == "__main__":
    mostrar_login()
