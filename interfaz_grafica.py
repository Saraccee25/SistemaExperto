import tkinter as tk
from tkinter import messagebox, ttk
from clips import Environment
import os

# Función para validar las entradas
def validar_entradas():
    nombre = nombre_entry.get().strip()
    stock = stock_var.get().strip()
    demanda = demanda_var.get().strip()
    tiempo_demanda = tiempo_demanda_var.get().strip()

    if not nombre:
        messagebox.showerror("Error", "El nombre del producto no puede estar vacío.")
        return False
    
    return True

# Función para limpiar los campos
def limpiar_campos():
    nombre_entry.delete(0, tk.END)
    stock_var.set("")
    demanda_var.set("")
    tiempo_demanda_var.set("")
    nombre_entry.focus()  # Poner el foco en el campo de nombre para facilitar la siguiente entrada

# Función para ejecutar el sistema experto
def ejecutar_sistema():
    if not validar_entradas():
        return

    try:
        # Eliminar archivo de resultados anterior si existe
        resultado_file = "resultado_clips.txt"
        if os.path.exists(resultado_file):
            os.remove(resultado_file)
        
        # Inicializar el entorno CLIPS
        env = Environment()
        
        # Cargar las reglas modificadas
        env.load("reglas_modificadas.clp")
        
        nombre = nombre_entry.get().strip()
        stock = stock_var.get().strip()
        demanda = demanda_var.get().strip()
        tiempo_demanda = tiempo_demanda_var.get().strip()

        # Limpiar resultados anteriores
        resultado_text.config(state=tk.NORMAL)
        resultado_text.delete(1.0, tk.END)
        
        # Insertar los datos del producto
        resultado_text.insert(tk.END, f"Producto: {nombre}\n")
        resultado_text.insert(tk.END, f"Stock: {stock}\n")
        resultado_text.insert(tk.END, f"Demanda: {demanda}\n")
        resultado_text.insert(tk.END, f"Tiempo de demanda: {tiempo_demanda}\n\n")
        resultado_text.insert(tk.END, "Recomendaciones:\n")
        resultado_text.insert(tk.END, "-" * 50 + "\n")
        
        # Asegurar que los valores sean correctos para CLIPS
        fact_string = f'(producto (nombre "{nombre}") (stock {stock}) (demanda {demanda}) (tiempo_demanda {tiempo_demanda}))'
        env.assert_string(fact_string)
        
        # Ejecutar CLIPS
        env.run()
        
        # Leer el archivo de resultados
        if os.path.exists(resultado_file):
            with open(resultado_file, 'r', encoding='utf-8') as f:
                recomendaciones = f.read().strip()
            
            if recomendaciones:
                resultado_text.insert(tk.END, recomendaciones)
            else:
                resultado_text.insert(tk.END, "No se generaron recomendaciones para los criterios seleccionados.")
        else:
            resultado_text.insert(tk.END, "No se generó el archivo de resultados. Verifica las reglas CLIPS.")
        
        resultado_text.config(state=tk.DISABLED)
        
        # Limpiar los campos después de mostrar los resultados
        limpiar_campos()
        
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al ejecutar el sistema experto: {str(e)}")
        import traceback
        traceback.print_exc()

# Crear ventana Tkinter
root = tk.Tk()
root.title("Sistema Experto de Gestión de Stock")
root.geometry("600x500")
root.config(bg="#f0f0f0")

# Crear un frame principal
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Estilo para los widgets
style = ttk.Style()
style.configure("TLabel", font=('Helvetica', 12), padding=5)
style.configure("TButton", font=('Helvetica', 12, 'bold'), padding=10)
style.configure("TEntry", font=('Arial', 12), padding=5)
style.configure("TCombobox", font=('Arial', 12), padding=5)

# Etiquetas y entradas con mejores widgets
ttk.Label(main_frame, text="Nombre del Producto:").grid(row=0, column=0, sticky=tk.W, pady=5)
nombre_entry = ttk.Entry(main_frame, width=30)
nombre_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)

ttk.Label(main_frame, text="Stock:").grid(row=1, column=0, sticky=tk.W, pady=5)
stock_var = tk.StringVar()
stock_combo = ttk.Combobox(main_frame, textvariable=stock_var, width=28, state="readonly")
stock_combo['values'] = ('bajo', 'medio', 'alto')
stock_combo.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)

ttk.Label(main_frame, text="Demanda:").grid(row=2, column=0, sticky=tk.W, pady=5)
demanda_var = tk.StringVar()
demanda_combo = ttk.Combobox(main_frame, textvariable=demanda_var, width=28, state="readonly")
demanda_combo['values'] = ('baja', 'media', 'alta')
demanda_combo.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)

ttk.Label(main_frame, text="Tiempo de Demanda:").grid(row=3, column=0, sticky=tk.W, pady=5)
tiempo_demanda_var = tk.StringVar()
tiempo_demanda_combo = ttk.Combobox(main_frame, textvariable=tiempo_demanda_var, width=28, state="readonly")
tiempo_demanda_combo['values'] = ('corto', 'prolongado')
tiempo_demanda_combo.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)

# Frame para botones
botones_frame = ttk.Frame(main_frame)
botones_frame.grid(row=4, column=0, columnspan=2, pady=20)

# Botón para ejecutar
ejecutar_button = ttk.Button(botones_frame, text="Ejecutar Sistema Experto", command=ejecutar_sistema)
ejecutar_button.pack(side=tk.LEFT, padx=5)

# Botón para limpiar campos
limpiar_button = ttk.Button(botones_frame, text="Limpiar Campos", command=limpiar_campos)
limpiar_button.pack(side=tk.LEFT, padx=5)

# Frame para resultados
resultado_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
resultado_frame.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW, pady=10)
main_frame.grid_rowconfigure(5, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Text widget para mostrar resultados con scroll
resultado_text = tk.Text(resultado_frame, wrap=tk.WORD, width=60, height=10)
resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(resultado_frame, command=resultado_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
resultado_text.config(yscrollcommand=scrollbar.set)

# Configurar el frame para expandirse
resultado_frame.grid_columnconfigure(0, weight=1)
resultado_frame.grid_rowconfigure(0, weight=1)

# Poner el foco en el campo de nombre al iniciar
nombre_entry.focus()

root.mainloop()