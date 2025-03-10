(deftemplate producto
    (slot nombre)
    (slot stock)
    (slot demanda)
    (slot tiempo_demanda))

(defglobal ?resultado-file = "resultado_clips.txt")

(defrule inicializar
    (initial-fact)
    =>
    (open ?resultado-file resultado "w")
    (close resultado))

(defrule retraso-reabastecimiento
    (producto (nombre ?n) (stock bajo) (demanda baja|media))
    =>
    (open ?resultado-file resultado "a")
    (printout resultado "No sugerir reabastecimiento inmediato para " ?n crlf)
    (close resultado))

(defrule incrementar-pedidos
    (producto (nombre ?n) (stock bajo|medio) (demanda alta))
    =>
    (open ?resultado-file resultado "a")
    (printout resultado "Sugerir aumentar futuros pedidos para " ?n crlf)
    (close resultado))

(defrule ignorar-sobrestock
    (producto (nombre ?n) (stock medio|alto) (demanda media|alta))
    =>
    (open ?resultado-file resultado "a")
    (printout resultado "No es necesario tomar acción inmediata para " ?n crlf)
    (close resultado))

(defrule identificar-baja-rotacion
    (producto (nombre ?n) (stock medio|alto) (demanda baja))
    =>
    (open ?resultado-file resultado "a")
    (printout resultado "Reducir compra de " ?n " por baja rotación" crlf)
    (close resultado))

(defrule reducir-stock
    (producto (nombre ?n) (stock alto) (demanda baja|media) (tiempo_demanda prolongado))
    =>
    (open ?resultado-file resultado "a")
    (printout resultado "Reducir stock de " ?n " con descuentos o promociones" crlf)
    (close resultado))

(defrule aumentar-stock
    (producto (nombre ?n) (stock bajo|medio) (demanda alta) (tiempo_demanda corto))
    =>
    (open ?resultado-file resultado "a")
    (printout resultado "Incrementar stock de " ?n " para evitar escasez" crlf)
    (close resultado))