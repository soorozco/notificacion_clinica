import streamlit as st
from datetime import datetime
import sqlite3
import os

# Configuración inicial de la página
st.set_page_config(page_title="Registro de Incidentes Clínicos - HCG", layout="wide")
st.title("Sistema de Identificación, Registro, Análisis y Seguimiento de Incidentes Clínicos")

# Fecha actual (fijada al 07/03/2025 según el contexto)
fecha_actual = datetime(2025, 3, 7)

# Función para calcular la edad
def calcular_edad(fecha_nacimiento):
    if fecha_nacimiento:
        fecha_nacimiento_dt = datetime.combine(fecha_nacimiento, datetime.min.time())
        diferencia = fecha_actual - fecha_nacimiento_dt
        edad = diferencia.days // 365
        return str(edad) if edad >= 0 else "0"
    return ""

# Función para inicializar la base de datos y la tabla
def inicializar_base_datos():
    conn = sqlite3.connect("incidentes_clinicos.db")
    c = conn.cursor()
    # Crear tabla si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS incidentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registro TEXT,
        nombre TEXT,
        fecha_nacimiento TEXT,
        edad TEXT,
        servicio TEXT,
        cama TEXT,
        medico_responsable TEXT,
        condicion_clinica TEXT,
        lugar_incidente TEXT,
        fecha_evento TEXT,
        hora_evento TEXT,
        involucrados TEXT,
        turno TEXT,
        presencia_familiar INTEGER,
        tipo_incidente TEXT,
        gravedad TEXT,
        accion_insegura TEXT,
        subcategoria TEXT,
        detalles TEXT,
        factor_incidente TEXT,
        factor_detalles TEXT,
        descripcion_evento TEXT,
        accion_correctiva TEXT,
        informo_medico INTEGER,
        informo_familiar INTEGER,
        analizado_comite INTEGER,
        fecha_registro TEXT
    )''')
    conn.commit()
    conn.close()

# Función para guardar los datos en la base de datos
def guardar_datos(datos):
    conn = sqlite3.connect("incidentes_clinicos.db")
    c = conn.cursor()
    c.execute('''INSERT INTO incidentes (
        registro, nombre, fecha_nacimiento, edad, servicio, cama, medico_responsable, 
        condicion_clinica, lugar_incidente, fecha_evento, hora_evento, involucrados, 
        turno, presencia_familiar, tipo_incidente, gravedad, accion_insegura, 
        subcategoria, detalles, factor_incidente, factor_detalles, descripcion_evento, 
        accion_correctiva, informo_medico, informo_familiar, analizado_comite, fecha_registro
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
    (
        datos["registro"], datos["nombre"], datos["fecha_nacimiento"], datos["edad"], 
        datos["servicio"], datos["cama"], datos["medico_responsable"], datos["condicion_clinica"],
        datos["lugar_incidente"], datos["fecha_evento"], datos["hora_evento"], datos["involucrados"],
        datos["turno"], datos["presencia_familiar"], datos["tipo_incidente"], datos["gravedad"],
        datos["accion_insegura"], datos["subcategoria"], datos["detalles"], datos["factor_incidente"],
        datos["factor_detalles"], datos["descripcion_evento"], datos["accion_correctiva"],
        datos["informo_medico"], datos["informo_familiar"], datos["analizado_comite"],
        datos["fecha_registro"]
    ))
    conn.commit()
    conn.close()

# Inicializar la base de datos al cargar la aplicación
inicializar_base_datos()

# Sección: Datos Relacionados al Evento
st.header("Datos Relacionados al Evento")
registro = st.text_input("Registro *")
nombre = st.text_input("Nombre")
col3, col4 = st.columns(2)
with col3:
    fecha_nacimiento = st.date_input(
        "Fecha de Nacimiento",
        value=None,
        min_value=datetime(1900, 1, 1).date(),
        max_value=fecha_actual.date()
    )
with col4:
    edad = st.text_input("Edad", value=calcular_edad(fecha_nacimiento), disabled=True)

col6, col8 = st.columns(2)
with col6:
    servicio = st.text_input("Servicio")
with col8:
    cama = st.text_input("Cama")

med_resp = st.text_input("Médico Responsable")

condicion_clinica = st.selectbox(
    "Condición clínica del paciente al momento del evento",
    ["", "Estable", "Crítico", "En recuperación"]
)

# Sección: Descripción del Evento
st.header("Descripción del Evento")
lugar_incidente = st.text_area("Lugar donde ocurrió el incidente clínico", max_chars=150)
col11, col12 = st.columns(2)
with col11:
    fecha_evento = st.date_input("Fecha del Evento", value=fecha_actual.date())
with col12:
    hora_evento = st.time_input("Hora del Evento", value=datetime(2025, 3, 7, 12, 16))

col13, col14, col15 = st.columns(3)
with col13:
    involucrados = st.multiselect(
        "Involucrados",
        ["Médico", "Enfermera", "Paciente", "Familiar", "Otro"]
    )
with col14:
    turno = st.selectbox(
        "Turno",
        ["Matutino", "Vespertino", "Nocturno (A) (1)", "Nocturno (B) (2)", "Jornada"]
    )
with col15:
    presencia_familiar = st.checkbox("Presencia Familiar")

col16, col17 = st.columns(2)
with col16:
    tipo_incidente = st.selectbox(
        "Tipo de Incidente",
        ["", "Cuasi Falla", "Evento adverso", "Evento adverso no atribuible al hospital",
         "Evento centinela", "Reacción adversa a Medicamento (RAM)",
         "Sospecha de reacción adversa a medicamento (SRAM)",
         "Evento supuestamente asociado a vacunación (ESAVI)"]
    )
with col17:
    gravedad = st.selectbox(
        "Gravedad",
        ["", "Leve", "Moderada", "Grave", "Fatal"]
    )

# Sección: Acciones Inseguras Relacionadas con
st.subheader("Acciones Inseguras Relacionadas con")
col18, col19, col20 = st.columns(3)

acciones_inseguras = {
    "Administración clínica": {
        "subcategorias": ["", "Alta", "Asignación de tareas", "Citas", "Consentimiento", "Entrega de expediente",
                          "Identificación del paciente", "Ingreso", "Interconsultas", "Lista de espera",
                          "Referencia a otra unidad", "Relevo de equipo asistencial", "Respuesta a emergencia", "Otros"],
        "detalles": ["", "Incompleta o inadecuada", "No disponible", "No se realizó cuando se indicó",
                     "Paciente equivocado", "Proceso o servicio equivocado", "Registro equivocado", "Otros"]
    },
    "Caídas": {
        "subcategorias": ["", "De la cama /camilla", "De la silla", "De las escaleras", "En el baño", "En el pasillo",
                          "Cuna", "Otros"],
        "detalles": ["", "Colapso", "Pérdida del equilibrio", "Resbalón", "Tropiezo", "Otros"]
    },
    "Dispositivos, materiales y/o equipos médicos": {
        "subcategorias": ["", "Dispositivo", "Equipo", "Material"],
        "detalles": ["", "Caduco", "No disponible", "Falta de mantenimiento y/o conservación", "Mal funcionamiento",
                     "Presentación o empaque inadecuado o deficiente", "Sucio/No estéril", "Uso inadecuado",
                     "Inadecuado para la tarea", "Otros"]
    },
    "Sangre / Productos Sanguíneos": {
        "subcategorias": ["", "Sangre", "Productos celulares", "Factores de la coagulación",
                          "Albúmina/proteínas plasmáticas", "Inmunoglobulinas"],
        "detalles": ["", "Almacenamiento, preservación o envasado incorrecto", "Consentimiento informado",
                     "Contraindicada", "Dosis incorrecta", "Equipo de infusión incorrecto", "Frecuencia incorrecta",
                     "Sangre / producto sanguíneo caduco", "No disponible", "Paciente incorrecto",
                     "Producto o dosis omitida", "Reacciones adversas", "Registro incorrecto",
                     "Sangre / producto sanguíneo incorrecto", "Velocidad de infusión incorrecta", "Extravasación",
                     "Información/instrucciones de dispensación erróneas", "Prescripción incorrecta",
                     "Error en la preparación/dispensación", "Traslado incorrecto", "Supervisión /Vigilancia incorrecta",
                     "Identificación de la sangre / producto sanguíneo incorrecto y/o ilegible", "Otros"]
    },
    "Registros Clínicos": {
        "subcategorias": ["", "Certificados/formatos", "Consentimiento Informado", "Identificación/etiquetas",
                          "Indicaciones médicas", "Instrucciones/Información/Guías clínicas/procedimientos",
                          "Lista de verificación", "Notas de enfermería", "Órdenes/solicitudes",
                          "Resultados/reportes/Imágenes", "Otros"],
        "detalles": ["", "Documento correcto en paciente incorrecto", "Documento extraviado o no disponible",
                     "Documento incorrecto en paciente correcto", "Información poco clara, confusa, ilegible",
                     "Retraso en el acceso a los documentos", "Registro omitido, incompleto o sin firma", "Otros"]
    },
    "Medicación / Soluciones intravenosas": {
        "subcategorias": ["", "Selección y Adquisición", "Almacenamiento", "Prescripción", "Distribución",
                          "Transcripción", "Preparación", "Administración"],
        "detalles": ["", "Pyxis", "Kardex", "Unidosis", "Mezclas subrogadas", "Otros"]
    },
    "Infecciones Asociadas a la Atención en Salud": {
        "subcategorias": ["", "De vías urinarias", "Del sitio de la prótesis", "Gastrointestinal",
                          "Herida quirúrgica", "Ocular", "Ótica", "Peritoneo", "Pulmonar", "Sanguíneo",
                          "Sitio de inserción del catéter vascular", "Tejidos blandos", "Otros"],
        "detalles": ["", "Bacteria", "Virus", "Hongo", "Parásito", "Protozoario", "Ricketsia", "Prion",
                     "Organismo causal no definido", "Otros"]
    },
    "Líquidos Intravenosos": {
        "subcategorias": [""],
        "detalles": ["", "Contraindicación en la solución", "Dilución incorrecta", "Dosis incorrecta",
                     "Extravasación", "Falta de vigilancia", "Hora o frecuencia incorrecta", "Medicamento caduco",
                     "Omisión de solución o dosis", "Paciente incorrecto", "Reacción adversa a la solución",
                     "Registro incorrecto u omitido", "Solución no disponible", "Solución incorrecta",
                     "Velocidad de administración incorrecta", "Otros"]
    },
    "Nutrición": {
        "subcategorias": [""],
        "detalles": ["", "Almacenamiento / Conservación incorrecta", "Calidad de los alimentos deficiente",
                     "Cantidad incorrecta", "Consistencia incorrecta", "Dieta incorrecta", "Frecuencia incorrecta",
                     "Método de preparación incorrecto", "No se administró la nutrición/dieta", "Paciente incorrecto",
                     "Traslado de la dieta incorrecto", "Vía de administración incorrecta", "Otros"]
    },
    "Patología/Laboratorio": {
        "subcategorias": [""],
        "detalles": ["", "Almacenamiento incorrecto", "Exámenes de laboratorio no disponibles",
                     "Identificación de la muestra incorrecta", "Muestra extraviada", "Paciente incorrecto",
                     "Procesamiento incorrecto", "Resultados no disponibles", "Técnica de extracción incorrecta",
                     "Muestra insuficiente"]
    },
    "Procedimientos Clínicos": {
        "subcategorias": ["", "Cuidados generales / Manejo", "Valoración", "Diagnóstico",
                          "Prevención / Chequeo de rutina / pesquisas", "Análisis / Pruebas"],
        "detalles": ["", "Diferimiento (se suspendió)", "Incompleto / Inadecuado", "No disponible",
                     "No se inició cuando se indicó", "Paciente incorrecto", "Procedimiento o tratamiento incorrecto",
                     "Sitio anatómico incorrecto", "Otros"]
    },
    "Procedimientos de Especialidad": {
        "subcategorias": ["", "Nefrología/Hemodiálisis: Calambres", "Nefrología/Hemodiálisis: Coagulación del sistema",
                          "Nefrología/Hemodiálisis: Embolia gaseosa secundario a: dejar abierto el catéter arterial, avería sistema de detección de aire, etc",
                          "Nefrología/Hemodiálisis: Falla de la osmosis", "Nefrología/Hemodiálisis: Filtro de reúso equivocado",
                          "Nefrología/Hemodiálisis: Hemolisis", "Nefrología/Hemodiálisis: Hipotensión por ultrafiltración excesiva secundario a: error al pesar, peso seco inadecuado",
                          "Nefrología/Hemodiálisis: Inadecuado tratamiento dialítico secundario a: inversión de líneas, tiempo de diálisis erróneo",
                          "Nefrología/Hemodiálisis: Infiltración subcutánea", "Nefrología/Hemodiálisis: Salida del catéter",
                          "Nefrología/Hemodiálisis: Salida de agujas durante la hemodiálisis",
                          "Nefrología/Hemodiálisis: Sangrado excesivo por sitios de punción",
                          "Oncología: Infiltración de quimioterapia", "Oncología: Derrame de quimioterapia",
                          "Premedicación", "Preparación de la quimioterapia",
                          "Quirófanos: Hipotermia", "Quirófanos: Diferimiento quirúrgico",
                          "Quirófanos: Paciente incorrecto", "Quirófanos: Procedimiento incorrecto",
                          "Quirófanos: Sitio quirúrgico incorrecto", "Quirófanos: Cuerpo extraño en cavidad",
                          "Quirófanos: Omisión de llenado de cirugía segura", "Quirófanos: Salida de drenes quirúrgicos",
                          "Quirófanos: Aspiración postanestésica",
                          "Quirófanos: Lesión cutánea secundaria al uso de sensores, fijaciones y placa de electrocauterio",
                          "Quirófanos: Contaminación de instrumental, prótesis e implantes",
                          "Neonatología: Entrega de neonato equivocado", "Neonatología: Identificación equivocada",
                          "Neonatología: Falta de identificadores / información incompleta o incorrecta",
                          "Neonatología: Secuestro / Robo de infante",
                          "Neonatología: Lesión cutánea secundaria al uso de sensores o fijaciones",
                          "Neonatología: Lesión ocular secundaria al uso de oxígeno o fototerapia",
                          "Neonatología: Aspiración",
                          "Obstetricia: Lesión de los nervios faciales secundario a la utilización de fórceps",
                          "Obstetricia: Lesión del plexo braquial", "Obstetricia: Parto fortuito",
                          "Obstetricia: Muerte materna", "Obstetricia: Shock hipovolémico secundario a sangrado",
                          "Obstetricia: Sepsis", "Obstetricia: Rotura uterina",
                          "Obstetricia: Maniobras obstétricas inadecuadas"],
        "detalles": [""]
    },
    "Comunicación escrita y de registros": {
        "subcategorias": ["", "Oficio / correos electrónicos / registros de comunicación",
                          "Certificados / formatos", "Consentimiento Informado",
                          "Etiquetas / adhesivos / pulseras de identificación / fichas de identificación",
                          "Hojas de evolución/historias clínicas/evaluaciones / interconsultas",
                          "Indicaciones médicas",
                          "Instrucciones / Información / Políticas / Guías clínicas / procedimientos",
                          "Lista de verificación", "Notas de enfermería", "Órdenes / solicitudes",
                          "Resultados / reportes / Imágenes"],
        "detalles": ["", "Documento correcto en paciente incorrecto", "Documento extraviado o no disponible",
                     "Documento incorrecto en paciente correcto", "Información incorrecta, poco clara, confusa, ilegible",
                     "Retraso en el acceso a los documentos", "Registro omitido, incompleto o sin firma"]
    },
    "Oxígeno/Gases/Vapores": {
        "subcategorias": ["", "Oxígeno", "Óxido nitroso", "Vacío medicinal", "Aire medicinal",
                          "Dióxido de carbono", "Nitrógeno", "Helio"],
        "detalles": ["", "Paciente incorrecto", "Dispositivo de administración incorrecta",
                     "Gas/vapor incorrecto", "Velocidad/concentración/caudal incorrecto",
                     "Modo de administración incorrecto", "Contraindicado",
                     "Condiciones de conservación inadecuadas", "No disponible", "Contaminación",
                     "Sistema de suministro incorrecto"]
    },
    "Infraestructuras/instalaciones": {
        "subcategorias": ["", "Techos", "Plafones", "Paredes", "Pisos", "Barda", "Puertas",
                          "Ventana", "Instalación eléctrica", "Instalación hidráulica",
                          "Instalación sanitaria", "Instalación informática"],
        "detalles": ["", "Inexistente", "Inadecuado", "Dañado/defectuoso/desgastado"]
    },
    "Lesiones en la piel y tegumentos": {
        "subcategorias": ["", "Acromion", "Boca", "Brazo", "Cabeza", "Cara", "Codo",
                          "Cóndilos", "Costillas", "Cuello", "Dedos", "Genitales",
                          "Maléolos", "Mano", "Ojos", "Omoplato", "Oreja", "Pies",
                          "Sacro", "Talones", "Trocánteres"],
        "detalles": ["", "Ulcera por presión estadio I", "Ulcera por presión estadio II",
                     "Ulcera por presión estadio III", "Ulcera por presión estadio IV",
                     "Contusión", "Escoriación", "Equimosis", "Hematoma", "Herida",
                     "Laceración", "Aplastamiento", "Quemadura", "Necrosis", "Dehiscencia"]
    },
    "Sondas, cánulas, catéteres y/o drenajes": {
        "subcategorias": ["", "Sonda", "Cánula", "Catéter", "Drenaje"],
        "detalles": ["", "Oclusión", "Ruptura", "Retirada accidental", "Técnica de colocación incorrecta",
                     "Técnica de retiro incorrecta", "Localización / Ubicación incorrecta",
                     "Mantenimiento / manejo / cuidados incorrectos", "Disfuncional / inadecuado"]
    },
    "Comportamiento": {
        "subcategorias": ["", "Del paciente", "Del personal"],
        "detalles": ["", "Fuga", "Incumplidor/no colaborador/obstructivo",
                     "Desconsiderado/grosero/hostil/inapropiado", "Arriesgado/imprudente/peligroso",
                     "Problema de uso/abuso de sustancias", "Acoso", "Discriminación/prejuicio",
                     "Autolesión deliberada/suicidio", "Agresión verbal", "Agresión física",
                     "Agresión sexual", "Agresión a objeto inanimado", "Amenaza de muerte"]
    },
    "Robo de infante": {
        "subcategorias": ["", "Con violencia", "Sin violencia"],
        "detalles": ["", "Secuestro", "Sustracción mediante engaño al personal",
                     "Sustracción mediante engaño al familiar", "Sustracción por familiar de primera línea",
                     "Sustracción por familiar de segunda línea", "Por error del personal",
                     "Entrega a familia equivocada", "Otro"]
    },
    "Muerte materna": {
        "subcategorias": ["", "Atribuible a la institución", "No atribuible a la institución"],
        "detalles": ["", "Hemorragia antes del parto", "Hemorragia durante el parto",
                     "Infección/Sepsis", "Preeclampsia", "Eclampsia", "Complicaciones del parto",
                     "Aborto inducido", "Otro"]
    }
}

with col18:
    accion_insegura = st.selectbox(
        "Acción Insegura",
        ["", "Administración clínica", "Caídas", "Dispositivos, materiales y/o equipos médicos",
         "Sangre / Productos Sanguíneos", "Registros Clínicos", "Medicación / Soluciones intravenosas",
         "Infecciones Asociadas a la Atención en Salud", "Líquidos Intravenosos", "Nutrición",
         "Patología/Laboratorio", "Procedimientos Clínicos", "Procedimientos de Especialidad",
         "Comunicación escrita y de registros", "Oxígeno/Gases/Vapores", "Infraestructuras/instalaciones",
         "Lesiones en la piel y tegumentos", "Sondas, cánulas, catéteres y/o drenajes", "Comportamiento",
         "Robo de infante", "Muerte materna"],
        key="accion_insegura"
    )

with col19:
    if accion_insegura and accion_insegura in acciones_inseguras:
        subcategoria = st.selectbox(
            "Subcategoría",
            acciones_inseguras[accion_insegura]["subcategorias"],
            key="subcategoria"
        )
    else:
        subcategoria = st.selectbox("Subcategoría", [""], key="subcategoria_default")

with col20:
    if accion_insegura and accion_insegura in acciones_inseguras and subcategoria:
        detalles = st.selectbox(
            "Detalles",
            acciones_inseguras[accion_insegura]["detalles"],
            key="detalles"
        )
    else:
        detalles = st.selectbox("Detalles", [""], key="detalles_default")

# Sección: Factores que Contribuyeron al Incidente
st.subheader("Factores que Contribuyeron al Incidente")
col21, col22 = st.columns(2)
with col21:
    factor_incidente = st.selectbox(
        "Factor",
        ["", "Paciente", "Organizacionales y Estratégicos", "Equipos y materiales",
         "Ambiente/Entorno", "Individuales/Personal", "Equipo de trabajo",
         "Ligados a la Tarea", "Comunicación", "Formación/Entrenamiento"],
        key="factor_incidente"
    )

subfactores = {
    "Paciente": ["", "Condición clínica", "Factores físicos", "Factores mentales y psicológicos",
                 "Factores sociales", "Relaciones interpersonales no adecuadas", "Otros"],
    "Organizacionales y Estratégicos": ["", "Cultura de seguridad", "Estructura organizativa",
                                        "Prioridades", "Riesgos externos", "Otros"],
    "Equipos y materiales": ["", "Fiabilidad/Funcionamiento", "Diseño", "Disponibilidad",
                             "Mantenimiento / conservación", "Usabilidad y/o utilización",
                             "Almacenamiento", "Otros"],
    "Ambiente/Entorno": ["", "Soporte administrativo y gerencial", "Carga de trabajo/horas",
                         "Clima laboral", "Diseño del entorno físico (luz, espacio, ruido)",
                         "Recursos humanos insuficientes", "Patrón de turnos / Tiempo",
                         "Mezcla de habilidades", "Otros"],
    "Individuales/Personal": ["", "Salud física", "Salud mental", "Aspectos sociales",
                              "Personalidad (actitud negativa)", "Conocimiento, habilidades, competencias",
                              "Descuido, distracción, falta de concentración", "Otros"],
    "Equipo de trabajo": ["", "Liderazgo", "Supervisión", "Disponibilidad de soporte: apoyo entre los integrantes",
                          "Estructura del equipo (consistencia, congruencia, etc.)",
                          "Inadecuado enlace de turno", "Otros"],
    "Ligados a la Tarea": ["", "Falta de medidas de seguridad al realizar la tarea (AESP)",
                           "Disponibilidad y uso de guías, protocolos, y procedimientos",
                           "Ayuda para la toma de decisiones", "Diseño de procedimientos o tareas (claridad de la estructura)",
                           "Disponibilidad y confiabilidad de las pruebas diagnósticas",
                           "Relacionado con las políticas", "Otros"],
    "Comunicación": ["", "Verbal", "No verbal", "Escrita y de registros", "Otros"],
    "Formación/Entrenamiento": ["", "Disponibilidad / accesibilidad de la formación o entrenamiento",
                                "Supervisión de la formación o entrenamiento",
                                "Competencias de la formación o entrenamiento", "Otros"]
}

with col22:
    if factor_incidente and factor_incidente in subfactores:
        factor_incidente_d = st.selectbox(
            "Detalles",
            subfactores[factor_incidente],
            key="factor_detalles"
        )
    else:
        factor_incidente_d = st.selectbox("Detalles", [""], key="factor_detalles_default")

descripcion_evento = st.text_area("Descripción del Evento")

# Sección: Acciones Preventivas, Correctivas y/o de Mejora
st.header("Acciones Preventivas, Correctivas y/o de Mejora")
st.subheader("Acciones Correctivas Emprendidas de Forma Inmediata")
accion_correctiva = st.text_area("Acciones Correctivas")

col23, col24, col25 = st.columns(3)
with col23:
    informo_medico = st.checkbox("Se informó al médico")
with col24:
    informo_familiar = st.checkbox("Se informó al familiar")
with col25:
    analizado_comite = st.checkbox("El caso es analizado por el comité")

# Botones finales
col26, col27 = st.columns([3, 1])
with col26:
    evidencia = st.file_uploader("Adjuntar Evidencia", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
with col27:
    if st.button("Guardar Cambios", use_container_width=True):
        # Preparar los datos para guardar
        datos = {
            "registro": registro,
            "nombre": nombre,
            "fecha_nacimiento": str(fecha_nacimiento) if fecha_nacimiento else "",
            "edad": edad,
            "servicio": servicio,
            "cama": cama,
            "medico_responsable": med_resp,
            "condicion_clinica": condicion_clinica,
            "lugar_incidente": lugar_incidente,
            "fecha_evento": str(fecha_evento),
            "hora_evento": str(hora_evento),
            "involucrados": ",".join(involucrados) if involucrados else "",
            "turno": turno,
            "presencia_familiar": 1 if presencia_familiar else 0,
            "tipo_incidente": tipo_incidente,
            "gravedad": gravedad,
            "accion_insegura": accion_insegura,
            "subcategoria": subcategoria,
            "detalles": detalles,
            "factor_incidente": factor_incidente,
            "factor_detalles": factor_incidente_d,
            "descripcion_evento": descripcion_evento,
            "accion_correctiva": accion_correctiva,
            "informo_medico": 1 if informo_medico else 0,
            "informo_familiar": 1 if informo_familiar else 0,
            "analizado_comite": 1 if analizado_comite else 0,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        guardar_datos(datos)
        st.success("Cambios guardados exitosamente en la base de datos!")

# Estilo básico para emular Materialize
st.markdown("""
<style>
    .stButton>button {
        background-color: #0288d1;
        color: white;
        border-radius: 5px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #0277bd;
    }
</style>
""", unsafe_allow_html=True)
