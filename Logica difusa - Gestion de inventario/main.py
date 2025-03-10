import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

def calcular_inventario():
    try:
        valorStock = float(entry_stock.get())
        valorDemanda = float(entry_demanda.get())
        valorTiempoDemanda = float(entry_tiempo.get())

        inventario_sim.input['stock'] = valorStock
        inventario_sim.input['demanda'] = valorDemanda
        inventario_sim.input['tiempo_demanda'] = valorTiempoDemanda

        inventario_sim.compute()
        resultado = inventario_sim.output['accion']
        
        messagebox.showinfo("Resultado", f"Acción recomendada: {resultado:.2f}")
        accion.view(sim=inventario_sim)
        plt.show()
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

# Definición de variables difusas
stock = ctrl.Antecedent(np.arange(0, 101, 1), 'stock')
demanda = ctrl.Antecedent(np.arange(0, 101, 1), 'demanda')
tiempo_demanda = ctrl.Antecedent(np.arange(0, 101, 1), 'tiempo_demanda')
accion = ctrl.Consequent(np.arange(0, 101, 1), 'accion')

# Funciones de membresía
stock['bajo'] = fuzz.trapmf(stock.universe, [0, 0, 20, 40])
stock['medio'] = fuzz.trimf(stock.universe, [30, 50, 70])
stock['alto'] = fuzz.trapmf(stock.universe, [60, 80, 100, 100])

demanda['baja'] = fuzz.trapmf(demanda.universe, [0, 0, 20, 40])
demanda['media'] = fuzz.trimf(demanda.universe, [30, 50, 70])
demanda['alta'] = fuzz.trapmf(demanda.universe, [60, 80, 100, 100])

tiempo_demanda['corto'] = fuzz.trapmf(tiempo_demanda.universe, [0, 0, 30, 50])
tiempo_demanda['prolongado'] = fuzz.trapmf(tiempo_demanda.universe, [40, 70, 100, 100])

accion['no_pedir'] = fuzz.trapmf(accion.universe, [0, 0, 20, 40])
accion['pedido_bajo'] = fuzz.trimf(accion.universe, [30, 50, 70])
accion['pedido_medio'] = fuzz.trapmf(accion.universe, [60, 80, 100, 100])
accion['pedido_alto'] = fuzz.trapmf(accion.universe, [80, 90, 100, 100])

# Definición de reglas difusas
rule1 = ctrl.Rule(stock['bajo'] & demanda['alta'] & tiempo_demanda['corto'], accion['pedido_medio'])
rule2 = ctrl.Rule(stock['bajo'] & demanda['media'] & tiempo_demanda['prolongado'], accion['pedido_medio'])
rule3 = ctrl.Rule(stock['medio'] & demanda['media'], accion['pedido_bajo'])
rule4 = ctrl.Rule(stock['alto'] & demanda['baja'], accion['no_pedir'])
rule5 = ctrl.Rule(stock['bajo'] & demanda['baja'] & tiempo_demanda['prolongado'], accion['pedido_bajo'])
rule6 = ctrl.Rule(stock['medio'] & demanda['alta'] & tiempo_demanda['corto'], accion['pedido_medio'])
rule7 = ctrl.Rule(stock['medio'] & demanda['baja'] & tiempo_demanda['corto'], accion['pedido_bajo'])
rule8 = ctrl.Rule(stock['bajo'] & demanda['alta'] & tiempo_demanda['prolongado'], accion['pedido_alto'])

# Crear sistema de control difuso
inventario_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])
inventario_sim = ctrl.ControlSystemSimulation(inventario_ctrl)

# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Gestión de Inventario")
root.geometry("300x250")

# Etiquetas y entradas
label_stock = tk.Label(root, text="Nivel de Stock:")
label_stock.pack()
entry_stock = tk.Entry(root)
entry_stock.pack()

label_demanda = tk.Label(root, text="Nivel de Demanda:")
label_demanda.pack()
entry_demanda = tk.Entry(root)
entry_demanda.pack()

label_tiempo = tk.Label(root, text="Tiempo de Demanda:")
label_tiempo.pack()
entry_tiempo = tk.Entry(root)
entry_tiempo.pack()

btn_calcular = tk.Button(root, text="Calcular", command=calcular_inventario)
btn_calcular.pack()

root.mainloop()