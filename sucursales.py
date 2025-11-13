import tkinter as Tk 
from tkinter import ttk, messagebox
import conexion 
import menu

def abrir_sucursales():
    sucursales = Tk.Tk()
    sucursales.title("Gestión de Sucursales")
    sucursales.geometry("700x600")
    sucursales.configure(bg="#FFD700")  
    campos = ["id_sucursal", "nombre_sucursal", "direccion"]
    entradas = {}

    for i, texto in enumerate(campos):
        Tk.Label(sucursales, text=texto, bg="#FFD700").grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entradas[texto] = Tk.Entry(sucursales, bg="#000000", fg="#FFD700")  
        entradas[texto].grid(row=i, column=1, padx=10, pady=5)

    def ejecutar_sql(sql, params=(), fetch=False):
        try:
            con = conexion.conectar_bd()
            cursor = con.cursor()
            cursor.execute(sql, params)
            if fetch:
                resultado = cursor.fetchall()
                con.close()
                return resultado
            else:
                con.commit()
                con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al ejecutar la consulta: {e}")

    def insertar():
        if any(not entradas[c].get() for c in campos):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
            return
        sql = "INSERT INTO sucursales (id_sucursal, nombre_sucursal, direccion) VALUES (%s, %s, %s)"
        params = tuple(entradas[c].get() for c in campos)
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Sucursal agregada correctamente")
        
    def actualizar():
        if not entradas["id_sucursal"].get():
            messagebox.showwarning("Atención", "Seleccione una sucursal para actualizar")
            return
        sql = "UPDATE sucursales SET nombre_sucursal=%s, direccion=%s WHERE id_sucursal=%s"
        params = (entradas["nombre_sucursal"].get(), entradas["direccion"].get(), entradas["id_sucursal"].get())
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Sucursal actualizada correctamente")
        
    def eliminar():
        if not entradas["id_sucursal"].get():
            messagebox.showwarning("Atención", "Seleccione una sucursal para eliminar")
            return
        sql = "DELETE FROM sucursales WHERE id_sucursal=%s"
        ejecutar_sql(sql, (entradas["id_sucursal"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Sucursal eliminada correctamente")
        
    def limpiar():
        for e in entradas.values():
            e.delete(0, Tk.END)
            
    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM sucursales", fetch=True)
        for fila in datos:
            tabla.insert("", Tk.END, values=fila)
                
    def seleccionar(event):
        seleccionado = tabla.selection()
        if seleccionado:
            valores = tabla.item(seleccionado[0], "values")
            for i, c in enumerate(campos):
                entradas[c].delete(0, Tk.END)
                entradas[c].insert(0, valores[i])

    botones = [("Agregar", insertar), ("Actualizar", actualizar), ("Eliminar", eliminar), ("Limpiar", limpiar)]
    for i, (texto, cmd) in enumerate(botones):
        Tk.Button(sucursales, text=texto, width=12, command=cmd, bg="#000000", fg="#FFD700").grid(row=4, column=i, padx=10, pady=10)
    
    columnas = ("id_sucursal", "nombre_sucursal", "direccion")
    tabla = ttk.Treeview(sucursales, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=20)
    
    tabla.bind("<<TreeviewSelect>>", seleccionar)
    Tk.Button(sucursales, text="Regresar al Menú", width=20, command=lambda: [sucursales.destroy(), menu.abrir_menu()], bg="#000000", fg="#FFD700").grid(row=7, column=0, columnspan=4, pady=10)
    
    mostrar_datos()
    sucursales.mainloop()

if __name__ == "__main__":
    abrir_sucursales()
