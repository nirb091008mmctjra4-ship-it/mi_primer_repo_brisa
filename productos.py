import tkinter as Tk
from tkinter import ttk, messagebox
import conexion
import menu

def abrir_productos():
    productos = Tk.Tk()
    productos.title("Gestión de Productos")
    productos.geometry("700x600")
    productos.configure(bg="#FFD700")  

    campos = ["id_productos", "nombre_productos", "precio_uni", "id_proveedor"]
    entradas = {}

    for i, texto in enumerate(campos):
        Tk.Label(productos, text=texto, bg="#FFD700").grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entradas[texto] = Tk.Entry(productos)
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
        sql = "INSERT INTO productos (id_productos, nombre_productos, precio_uni, id_proveedor) VALUES (%s, %s, %s, %s)"
        params = tuple(entradas[c].get() for c in campos)
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Producto agregado correctamente")

    def actualizar():
        if not entradas["id_productos"].get():
            messagebox.showwarning("Atención", "Seleccione un producto para actualizar")
            return
        sql = "UPDATE productos SET nombre_productos=%s, precio_uni=%s, id_proveedor=%s WHERE id_productos=%s"
        params = (entradas["nombre_productos"].get(), entradas["precio_uni"].get(), entradas["id_proveedor"].get(), entradas["id_productos"].get())
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Producto actualizado correctamente")

    def eliminar():
        if not entradas["id_productos"].get():
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar")
            return
        sql = "DELETE FROM productos WHERE id_productos=%s"
        ejecutar_sql(sql, (entradas["id_productos"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")

    def limpiar():
        for e in entradas.values():
            e.delete(0, Tk.END)

    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM productos", fetch=True)
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
        Tk.Button(productos, text=texto, width=12, bg="#000000", fg="#FFD700", command=cmd).grid(row=4, column=i, padx=10, pady=10)

    columnas = ("id_productos", "nombre_productos", "precio_uni", "id_proveedor")
    tabla = ttk.Treeview(productos, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=20)

    tabla.bind("<<TreeviewSelect>>", seleccionar)
    Tk.Button(productos, text="Regresar al Menú", width=20, bg="#000000", fg="#FFD700", command=lambda: [productos.destroy(), menu.abrir_menu()]).grid(row=7, column=0, columnspan=4, pady=10)

    mostrar_datos()
    productos.mainloop()

if __name__ == "__main__":
    abrir_productos()
