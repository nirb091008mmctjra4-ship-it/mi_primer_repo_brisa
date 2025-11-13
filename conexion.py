import mysql.connector
from tkinter import messagebox
def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="starbucks"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se puede establecer una conexion con la BD\n{err}")
        return None          