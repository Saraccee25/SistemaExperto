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
        
        # Interpretación del resultado
        if resultado < 25:
            descripcion = "No es necesario realizar un pedido."
        elif 25 <= resultado < 50:
            descripcion = "Se recomienda hacer un pedido bajo."
        elif 50 <= resultado < 75:
            descripcion = "Se recomienda hacer un pedido medio."
        else:
            descripcion = "Se recomienda hacer un pedido alto."
        
        # Calcular los grados de pertenencia
        stockBajo = fuzz.interp_membership(stock.universe, stock['bajo'].mf, valorStock)
        stockMedio = fuzz.interp_membership(stock.universe, stock['medio'].mf, valorStock)
        stockAlto = fuzz.interp_membership(stock.universe, stock['alto'].mf, valorStock)
        
        demandaBaja = fuzz.interp_membership(demanda.universe, demanda['baja'].mf, valorDemanda)
        demandaMedia = fuzz.interp_membership(demanda.universe, demanda['media'].mf, valorDemanda)
        demandaAlta = fuzz.interp_membership(demanda.universe, demanda['alta'].mf, valorDemanda)
        
        tiempoCorto = fuzz.interp_membership(tiempo_demanda.universe, tiempo_demanda['corto'].mf, valorTiempoDemanda)
        tiempoProlongado = fuzz.interp_membership(tiempo_demanda.universe, tiempo_demanda['prolongado'].mf, valorTiempoDemanda)
        
        # Calcular la activación de las reglas difusas
        activeRules = {
            "Regla 1": np.fmin(np.fmin(stockBajo, demandaAlta), tiempoCorto),
            "Regla 2": np.fmin(np.fmin(stockBajo, demandaMedia), tiempoProlongado),
            "Regla 3": np.fmin(stockMedio, demandaMedia),
            "Regla 4": np.fmin(stockAlto, demandaBaja),
            "Regla 5": np.fmin(np.fmin(stockBajo, demandaBaja), tiempoProlongado),
            "Regla 6": np.fmin(np.fmin(stockMedio, demandaAlta), tiempoCorto),
            "Regla 7": np.fmin(np.fmin(stockMedio, demandaBaja), tiempoCorto),
            "Regla 8": np.fmin(np.fmin(stockBajo, demandaAlta), tiempoProlongado),
            "Regla 9": np.fmin(np.fmin(stockAlto, demandaAlta), tiempoCorto),
            "Regla 10": np.fmin(np.fmin(stockBajo, demandaBaja), tiempoCorto)
        }
        
        # Mostrar en interfaz
        detalles = f"Acción recomendada: {resultado:.2f}\n{descripcion}\n\n"
        detalles += "Grados de Pertenencia:\n"
        detalles += f"Stock: Bajo={stockBajo:.2f}, Medio={stockMedio:.2f}, Alto={stockAlto:.2f}\n"
        detalles += f"Demanda: Baja={demandaBaja:.2f}, Media={demandaMedia:.2f}, Alta={demandaAlta:.2f}\n"
        detalles += f"Tiempo de Demanda: Corto={tiempoCorto:.2f}, Prolongado={tiempoProlongado:.2f}\n\n"
        detalles += "Activación de Reglas:\n"
        for regla, valor in activeRules.items():
            detalles += f"{regla}: {valor:.2f}\n"
        
        messagebox.showinfo("Resultado", detalles)
        
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
    try:
        valorStock = float(entry_stock.get())
        valorDemanda = float(entry_demanda.get())
        valorTiempoDemanda = float(entry_tiempo.get())

        inventario_sim.input['stock'] = valorStock
        inventario_sim.input['demanda'] = valorDemanda
        inventario_sim.input['tiempo_demanda'] = valorTiempoDemanda

        inventario_sim.compute()
        resultado = inventario_sim.output['accion']
        
        # Interpretación del resultado
        if resultado < 25:
            descripcion = "No es necesario realizar un pedido."
        elif 25 <= resultado < 50:
            descripcion = "Se recomienda hacer un pedido bajo."
        elif 50 <= resultado < 75:
            descripcion = "Se recomienda hacer un pedido medio."
        else:
            descripcion = "Se recomienda hacer un pedido alto."
        
        # Calcular los grados de pertenencia
        stockBajo = fuzz.interp_membership(stock.universe, stock['bajo'].mf, valorStock)
        stockMedio = fuzz.interp_membership(stock.universe, stock['medio'].mf, valorStock)
        stockAlto = fuzz.interp_membership(stock.universe, stock['alto'].mf, valorStock)
        
        demandaBaja = fuzz.interp_membership(demanda.universe, demanda['baja'].mf, valorDemanda)
        demandaMedia = fuzz.interp_membership(demanda.universe, demanda['media'].mf, valorDemanda)
        demandaAlta = fuzz.interp_membership(demanda.universe, demanda['alta'].mf, valorDemanda)
        
        tiempoCorto = fuzz.interp_membership(tiempo_demanda.universe, tiempo_demanda['corto'].mf, valorTiempoDemanda)
        tiempoProlongado = fuzz.interp_membership(tiempo_demanda.universe, tiempo_demanda['prolongado'].mf, valorTiempoDemanda)
        
        # Mostrar en interfaz
        detalles = f"Acción recomendada: {resultado:.2f}\n{descripcion}\n\n"
        detalles += "Grados de Pertenencia:\n"
        detalles += f"Stock: Bajo={stockBajo:.2f}, Medio={stockMedio:.2f}, Alto={stockAlto:.2f}\n"
        detalles += f"Demanda: Baja={demandaBaja:.2f}, Media={demandaMedia:.2f}, Alta={demandaAlta:.2f}\n"
        detalles += f"Tiempo de Demanda: Corto={tiempoCorto:.2f}, Prolongado={tiempoProlongado:.2f}\n"
        
        messagebox.showinfo("Resultado", detalles)
        
        # Limpiar los campos de entrada después de la ejecución
        entry_stock.delete(0, tk.END)
        entry_demanda.delete(0, tk.END)
        entry_tiempo.delete(0, tk.END)
        
        # Mostrar gráficos en orden
        accion.view(sim=inventario_sim)
        plt.show()
        stock.view()
        plt.show()
        demanda.view()
        plt.show()
        tiempo_demanda.view()
        plt.show()
        accion.view()  
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
rule9 = ctrl.Rule(stock['alto'] & demanda['alta'] & tiempo_demanda['corto'], accion['no_pedir'])
rule10 = ctrl.Rule(stock['bajo'] & demanda['baja'] & tiempo_demanda['corto'], accion['pedido_bajo'])

# Crear sistema de control difuso
inventario_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])
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
