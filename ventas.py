import tkinter as tk
from tkinter import ttk, messagebox
import conexion
import menu


def abrir_ventas():
    ventas = tk.Tk() 
    ventas.title("Gestión de Ventas")  
    ventas.geometry("900x600")  
    ventas.configure(bg="#FFD700")

    campos = [
        ("id_ventas",  1, 0),
        ("Fecha (YYYY-MM-DD)", 2, 0),
        ("id_Producto", 3, 0),
        ("Cantidad", 4, 0),
        ("id_empleado", 5, 0),
        ("id_sucursal", 0, 0),
        ("Precio_Unitario", 0, 2),
        ("Subtotal", 1, 2),
        ("IVA", 2, 2),
        ("Total", 3, 2)
    ]
    entradas = {}

    for texto, fila, col in campos:
        tk.Label(ventas, text=texto, bg="#FFD700").grid(row=fila, column=col, padx=10, pady=5, sticky="w")
        entrada = tk.Entry(ventas, bg="#000000", fg="#FFD700")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        entrada.grid(row=fila, column=col + 1, padx=10, pady=5)
        entradas[texto] = entrada 

    def ejecutar_sql(sql, params=(), fetch=False):
        try:
            con = conexion.conectar_bd()  
            cursor = con.cursor()
            cursor.execute(sql, params) 
            if fetch:  
                datos = cursor.fetchall()
                con.close()
                return datos
            else:  
                con.commit()
                con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al ejecutar la consulta: {e}")

    def calcular_totales(event=None):
        try:
            cantidad = float(entradas["Cantidad"].get())  
            precio = float(entradas["Precio_Unitario"].get())  
            subtotal = cantidad * precio  
            iva = subtotal * 0.16 
            total = subtotal + iva 
            
            entradas["Subtotal"].delete(0, tk.END)
            entradas["Subtotal"].insert(0, f"{subtotal:.2f}")
            entradas["IVA"].delete(0, tk.END)
            entradas["IVA"].insert(0, f"{iva:.2f}")
            entradas["Total"].delete(0, tk.END)
            entradas["Total"].insert(0, f"{total:.2f}")
        except ValueError:
            for campo in ("Subtotal", "IVA", "Total"):
                entradas[campo].delete(0, tk.END)

    entradas["Cantidad"].bind("<KeyRelease>", calcular_totales)
    entradas["Precio_Unitario"].bind("<KeyRelease>", calcular_totales)

    def insertar():
        if not entradas["id_ventas"].get() or not entradas["Fecha (YYYY-MM-DD)"].get() or not entradas["id_Producto"].get():
            messagebox.showwarning("Campos vacíos", "id_ventas, Fecha y Producto son obligatorios")
            return
        sql = """INSERT INTO ventas 
                 (id_ventas, fecha, id_producto, id_empleado, id_sucursal, cantidad, precio_unitario, 
                 subtotal, iva, total) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = tuple(entradas[c].get() for c in [
            "id_ventas", "Fecha (YYYY-MM-DD)", "id_Producto", "id_empleado", "id_sucursal", 
            "Cantidad", "Precio_Unitario", "Subtotal", "IVA", "Total"])
        ejecutar_sql(sql, params)  
        mostrar_datos()  
        
        messagebox.showinfo("Éxito", "Venta registrada correctamente")

    def actualizar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione una venta para actualizar")
            return
        sql = """UPDATE ventas 
                 SET fecha=%s, id_producto=%s, id_empleado=%s, id_sucursal=%s, cantidad=%s, 
                     precio_unitario=%s, subtotal=%s, iva=%s, total=%s 
                 WHERE id_ventas=%s"""
        params = (
            entradas["Fecha (YYYY-MM-DD)"].get(),
            entradas["id_Producto"].get(),
            entradas["id_empleado"].get(),
            entradas["id_sucursal"].get(),
            entradas["Cantidad"].get(),
            entradas["Precio_Unitario"].get(),
            entradas["Subtotal"].get(),
            entradas["IVA"].get(),
            entradas["Total"].get(),
            entradas["id_ventas"].get()
        )
        ejecutar_sql(sql, params)
        mostrar_datos()
        
        messagebox.showinfo("Éxito", "Venta actualizada correctamente")

    def eliminar():
        if not entradas["id_ventas"].get():
            messagebox.showwarning("Atención", "Seleccione una venta para eliminar")
            return
        ejecutar_sql("DELETE FROM ventas WHERE id_ventas=%s", (entradas["id_ventas"].get(),))
        mostrar_datos()
        
        messagebox.showinfo("Éxito", "Venta eliminada correctamente")

    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)

    def mostrar_datos():
        for row in tabla.get_children():  
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM ventas", fetch=True)  
        for fila in datos:  
            tabla.insert("", tk.END, values=fila)

    def seleccionar(event):
        seleccionado = tabla.selection()
        if seleccionado:
            valores = tabla.item(seleccionado[0], "values")
            for i, campo in enumerate([
                "id_ventas", "Fecha (YYYY-MM-DD)", "id_Producto", "id_empleado", "id_sucursal", 
                "Cantidad", "Precio_Unitario", "Subtotal", "IVA", "Total"]):
                entradas[campo].delete(0, tk.END)
                entradas[campo].insert(0, valores[i])

    # Botones de acción
    botones = [("Agregar", insertar), ("Actualizar", actualizar), ("Eliminar", eliminar), ("Limpiar", limpiar)]
    for i, (texto, cmd) in enumerate(botones):
        tk.Button(ventas, text=texto, width=12, command=cmd, bg="#000000", fg="#FFD700").grid(row=6, column=i, padx=10, pady=10)  

    columnas = ("id_ventas", "Fecha", "id_Producto", "id_empleado", "id_sucursal", "Cantidad", "Precio Unitario", "Subtotal", "IVA", "Total")
    tabla = ttk.Treeview(ventas, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col) 
        tabla.column(col, width=110)  
    tabla.grid(row=7, column=0, columnspan=4, padx=10, pady=20) 
    tabla.bind("<<TreeviewSelect>>", seleccionar) 

    tk.Button(ventas, text="Regresar al Menú", width=20,
              command=lambda: [ventas.destroy(), menu.abrir_menu()], bg="#000000", fg="#FFD700").grid(row=8, column=0, columnspan=4, pady=10)  

    mostrar_datos()  
    ventas.mainloop()  

if __name__ == "__main__":
    abrir_ventas()
