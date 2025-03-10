import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def calcular_accion():
    try:
        stock_val = int(entry_stock.get())
        demanda_val = int(entry_demanda.get())
        tiempo_val = int(entry_tiempo.get())

        sistema.input["stock"] = stock_val
        sistema.input["demanda"] = demanda_val
        sistema.input["tiempo_demanda"] = tiempo_val
        sistema.compute()

        resultado = sistema.output["accion"]
        detalles = "Cálculo de reglas:\n"
        
        for i, rule in enumerate(sistema.ctrl.rules):
            activacion = rule.antecedent.membership_value(sistema)
            detalles += f"Regla {i+1}: {rule.label}, Activación: {activacion:.2f}\n"
        
        messagebox.showinfo("Resultado", f"Acción recomendada: {resultado:.2f}\n\n{detalles}")
        mostrar_graficos()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def mostrar_graficos():
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    
    stock.view(sim=sistema, ax=axes[0, 0])
    demanda.view(sim=sistema, ax=axes[0, 1])
    tiempo_demanda.view(sim=sistema, ax=axes[1, 0])
    accion.view(sim=sistema, ax=axes[1, 1])
    
    plt.tight_layout()
    plt.show()

# Definir variables difusas
stock = ctrl.Antecedent(np.arange(0, 101, 1), "stock")
demanda = ctrl.Antecedent(np.arange(0, 101, 1), "demanda")
tiempo_demanda = ctrl.Antecedent(np.arange(0, 101, 1), "tiempo_demanda")
accion = ctrl.Consequent(np.arange(0, 101, 1), "accion")

# Definir funciones de membresía
stock["bajo"] = fuzz.trapmf(stock.universe, [0, 0, 20, 40])
stock["medio"] = fuzz.trimf(stock.universe, [30, 50, 70])
stock["alto"] = fuzz.trapmf(stock.universe, [60, 80, 100, 100])

demanda["baja"] = fuzz.trapmf(demanda.universe, [0, 0, 20, 40])
demanda["media"] = fuzz.trimf(demanda.universe, [30, 50, 70])
demanda["alta"] = fuzz.trapmf(demanda.universe, [60, 80, 100, 100])

tiempo_demanda["corto"] = fuzz.trapmf(tiempo_demanda.universe, [0, 0, 30, 50])
tiempo_demanda["prolongado"] = fuzz.trapmf(tiempo_demanda.universe, [40, 70, 100, 100])

accion["no_pedir"] = fuzz.trapmf(accion.universe, [0, 0, 20, 40])
accion["pedido_bajo"] = fuzz.trimf(accion.universe, [30, 50, 70])
accion["pedido_medio"] = fuzz.trapmf(accion.universe, [60, 80, 100, 100])
accion["pedido_alto"] = fuzz.trapmf(accion.universe, [80, 90, 100, 100])

# Definir reglas difusas
rule1 = ctrl.Rule(stock["bajo"] & demanda["alta"] & tiempo_demanda["corto"], accion["pedido_alto"])
rule2 = ctrl.Rule(stock["bajo"] & demanda["media"] & tiempo_demanda["prolongado"], accion["pedido_medio"])
rule3 = ctrl.Rule(stock["medio"] & demanda["media"], accion["pedido_bajo"])
rule4 = ctrl.Rule(stock["alto"] & demanda["baja"], accion["no_pedir"])
rule5 = ctrl.Rule(stock["bajo"] & demanda["baja"] & tiempo_demanda["prolongado"], accion["pedido_bajo"])
rule6 = ctrl.Rule(stock["medio"] & demanda["alta"] & tiempo_demanda["corto"], accion["pedido_medio"])
rule7 = ctrl.Rule(stock["medio"] & demanda["baja"] & tiempo_demanda["corto"], accion["pedido_bajo"])

# Controlador difuso
controlador = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
sistema = ctrl.ControlSystemSimulation(controlador)

# Interfaz gráfica
root = tk.Tk()
root.title("Gestión de Inventario Difuso")

label_stock = tk.Label(root, text="Stock:")
label_stock.pack()
entry_stock = tk.Entry(root)
entry_stock.pack()

label_demanda = tk.Label(root, text="Demanda:")
label_demanda.pack()
entry_demanda = tk.Entry(root)
entry_demanda.pack()

label_tiempo = tk.Label(root, text="Tiempo Demanda:")
label_tiempo.pack()
entry_tiempo = tk.Entry(root)
entry_tiempo.pack()

boton_calcular = tk.Button(root, text="Calcular Acción", command=calcular_accion)
boton_calcular.pack()

root.mainloop()
