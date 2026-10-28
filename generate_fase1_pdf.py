import os
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class UTSPhase1PDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=False)  # Control manual exacto por páginas temáticas
        self.set_margins(18, 18, 18)
        
        # Cargar fuentes TrueType completas de Windows con soporte Unicode
        self.add_font("ArialUni", "", r"C:\Windows\Fonts\arial.ttf")
        self.add_font("ArialUni", "B", r"C:\Windows\Fonts\arialbd.ttf")
        self.add_font("ArialUni", "I", r"C:\Windows\Fonts\ariali.ttf")
        self.add_font("ArialUni", "BI", r"C:\Windows\Fonts\arialbi.ttf")

    def header(self):
        if self.page_no() > 1:
            self.set_fill_color(245, 248, 252)
            self.rect(0, 0, 210, 14, "F")
            
            self.set_draw_color(0, 174, 157)
            self.set_line_width(0.6)
            self.line(18, 13, 192, 13)

            self.set_xy(18, 3.5)
            self.set_font("ArialUni", "B", 8)
            self.set_text_color(15, 76, 129)
            self.cell(100, 5, "UNIVERSIDAD TECNOLÓGICA DE SALAMANCA • IDGS 10°", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)

            self.set_font("ArialUni", "I", 8)
            self.set_text_color(100, 116, 139)
            self.cell(74, 5, "Fase 1: Plan de Desarrollo Móvil | LabPass QR", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

    def footer(self):
        if self.page_no() > 1:
            self.set_draw_color(226, 232, 240)
            self.set_line_width(0.4)
            self.line(18, 283, 192, 283)

            self.set_xy(18, 284)
            self.set_font("ArialUni", "", 8)
            self.set_text_color(100, 116, 139)
            self.cell(100, 5, "Desarrollo Móvil Integral — Docente: Ericka Nohemí Álvarez Valencia", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
            
            self.set_font("ArialUni", "B", 8)
            self.set_text_color(15, 76, 129)
            self.cell(74, 5, f"Página {self.page_no()}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

def build_pdf(output_pdf_path):
    pdf = UTSPhase1PDF()

    # Helpers
    def render_section_title(num, title):
        pdf.ln(1)
        y = pdf.get_y()
        pdf.set_fill_color(15, 76, 129)
        pdf.rect(18, y, 6.5, 6.5, "F")
        pdf.set_xy(18, y)
        pdf.set_font("ArialUni", "B", 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(6.5, 6.5, str(num), 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")

        pdf.set_x(27)
        pdf.set_font("ArialUni", "B", 11.5)
        pdf.set_text_color(15, 76, 129)
        pdf.cell(165, 6.5, title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_draw_color(203, 213, 225)
        pdf.set_line_width(0.5)
        pdf.line(18, pdf.get_y() + 1, 192, pdf.get_y() + 1)
        pdf.ln(2.5)

    def render_sub_heading(title):
        pdf.set_font("ArialUni", "B", 9.5)
        pdf.set_text_color(14, 116, 144)
        pdf.cell(174, 4.8, f"> {title}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.8)

    def render_p(text, spacing=1.5):
        pdf.set_font("ArialUni", "", 8.5)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(174, 4.1, text)
        pdf.ln(spacing)

    def render_bullet(title, desc, spacing=1.2):
        pdf.set_x(20)
        pdf.set_font("ArialUni", "B", 8.4)
        pdf.set_text_color(15, 76, 129)
        prefix = f"- {title}: "
        pdf.write(4.1, prefix)
        
        pdf.set_font("ArialUni", "", 8.4)
        pdf.set_text_color(51, 65, 85)
        pdf.write(4.1, desc + "\n")
        pdf.ln(spacing)

    def render_info_box(title, text, color="blue", h_fixed=None):
        y = pdf.get_y()
        bg_c = (240, 249, 255) if color == "blue" else (255, 251, 235)
        border_c = (14, 116, 144) if color == "blue" else (245, 158, 11)
        
        pdf.set_font("ArialUni", "", 8.2)
        lines = len(pdf.multi_cell(164, 3.9, f"{title}\n{text}", dry_run=True, output="LINES"))
        box_h = h_fixed if h_fixed else max(14, (lines * 3.9) + 5)

        pdf.set_fill_color(*bg_c)
        pdf.set_draw_color(226, 232, 240)
        pdf.rect(18, y, 174, box_h, "FD")
        pdf.set_fill_color(*border_c)
        pdf.rect(18, y, 3, box_h, "F")

        pdf.set_xy(23, y + 2)
        pdf.set_font("ArialUni", "B", 8.8)
        pdf.set_text_color(*border_c)
        pdf.cell(164, 4.2, title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_x(23)
        pdf.set_font("ArialUni", "", 8.2)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(164, 3.8, text)
        pdf.set_y(y + box_h + 2)

    # ==============================================================
    # PÁGINA 1: PORTADA COLORIDA Y LLAMATIVA
    # ==============================================================
    pdf.add_page()

    # Fondo superior azul marino tecnológico
    pdf.set_fill_color(10, 46, 80)
    pdf.rect(0, 0, 210, 108, "F")

    # Franja turquesa brillante
    pdf.set_fill_color(0, 174, 157)
    pdf.rect(0, 104, 210, 5, "F")

    # Franja naranja de contraste
    pdf.set_fill_color(245, 130, 32)
    pdf.rect(0, 109, 210, 3.5, "F")

    # Header de la Universidad
    pdf.set_xy(15, 14)
    pdf.set_font("ArialUni", "B", 9)
    pdf.set_text_color(167, 243, 208)
    pdf.cell(180, 5, "UTS • DIVISIÓN TIC • 10° CUATRIMESTRE", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.ln(1)
    pdf.set_font("ArialUni", "B", 15)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(180, 7, "UNIVERSIDAD TECNOLÓGICA DE SALAMANCA", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("ArialUni", "", 10)
    pdf.set_text_color(226, 232, 240)
    pdf.cell(180, 5.5, "División de Tecnologías de la Información y Comunicación", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("ArialUni", "B", 11)
    pdf.set_text_color(94, 234, 212)
    pdf.cell(180, 6, "Ingeniería en Desarrollo y Gestión de Software (IDGS)", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # Título del Trabajo
    pdf.ln(5)
    pdf.set_fill_color(245, 130, 32)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("ArialUni", "B", 9.5)
    
    # Badge Fase 1
    badge_text = " FASE 1: PLAN DEL PROCESO DE DESARROLLO MÓVIL "
    bw = pdf.get_string_width(badge_text) + 10
    bx = (210 - bw) / 2
    pdf.set_xy(bx, pdf.get_y())
    pdf.cell(bw, 6.5, badge_text, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C", fill=True)

    pdf.ln(3)
    pdf.set_font("ArialUni", "B", 26)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(180, 11, "LabPass QR", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("ArialUni", "I", 10.5)
    pdf.set_text_color(220, 240, 255)
    pdf.cell(180, 5.5, "Sistema Móvil de Control, Préstamo y Trazabilidad en Laboratorios UTS", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # ==================== TARJETAS DE PORTADA ====================
    card_y = 122
    pdf.set_xy(16, card_y)
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(16, card_y, 86, 76, "FD")

    pdf.set_fill_color(15, 76, 129)
    pdf.rect(16, card_y, 86, 8, "F")
    pdf.set_xy(16, card_y + 1)
    pdf.set_font("ArialUni", "B", 9)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(86, 6, "DATOS DE LA ASIGNATURA", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    meta_y = card_y + 11
    def draw_meta_field(label, val, y_pos):
        pdf.set_xy(20, y_pos)
        pdf.set_font("ArialUni", "B", 8.5)
        pdf.set_text_color(15, 76, 129)
        pdf.cell(26, 4.5, label, 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("ArialUni", "", 8.5)
        pdf.set_text_color(40, 50, 65)
        pdf.cell(52, 4.5, val, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    draw_meta_field("Asignatura:", "Desarrollo Móvil Integral", meta_y)
    draw_meta_field("Carrera:", "IDGS (Ingeniería)", meta_y + 9)
    draw_meta_field("Grado/Grupo:", "10° Cuatrimestre", meta_y + 18)
    draw_meta_field("Docente:", "Ericka N. Álvarez Valencia", meta_y + 27)
    
    # Fecha de Entrega destacada
    pdf.set_xy(20, meta_y + 37)
    pdf.set_fill_color(254, 243, 199)
    pdf.set_draw_color(245, 158, 11)
    pdf.rect(19, meta_y + 36, 80, 11, "FD")
    pdf.set_xy(21, meta_y + 37.5)
    pdf.set_font("ArialUni", "B", 8)
    pdf.set_text_color(146, 64, 14)
    pdf.cell(32, 4.5, "Fecha de Entrega:", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font("ArialUni", "B", 9)
    pdf.set_text_color(180, 83, 9)
    pdf.cell(44, 4.5, "16 de Octubre de 2026", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    draw_meta_field("Entregable:", "Documento Digital Fase 1", meta_y + 51)

    # Tarjeta 2: Equipo de Desarrollo (Derecha)
    pdf.set_xy(108, card_y)
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(108, card_y, 86, 76, "FD")

    pdf.set_fill_color(0, 174, 157)
    pdf.rect(108, card_y, 86, 8, "F")
    pdf.set_xy(108, card_y + 1)
    pdf.set_font("ArialUni", "B", 9)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(86, 6, "INTEGRANTES DEL EQUIPO (IDGS)", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    team = [
        ("Alvaro Jesús Chávez Bazana", "Product Owner (PO)"),
        ("Guillermo Yael Berlín Fomperosa", "Scrum Master (SM)"),
        ("Juan Pablo Vega Uribe", "Lead Mobile Dev (UI/UX)"),
        ("Diego Sebastián Vilegas Enriquez", "Backend & Data Architect")
    ]

    t_y = card_y + 12
    for name, role in team:
        pdf.set_fill_color(15, 76, 129)
        pdf.circle(114, t_y + 3.5, 1.8, "F")
        pdf.set_xy(118, t_y)
        pdf.set_font("ArialUni", "B", 8.8)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(72, 4.5, name, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_xy(118, t_y + 4.5)
        pdf.set_font("ArialUni", "I", 8)
        pdf.set_text_color(14, 116, 144)
        pdf.cell(72, 4, f"Rol: {role}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        t_y += 15

    # Pie de Portada
    pdf.set_xy(18, 260)
    pdf.set_draw_color(226, 232, 240)
    pdf.line(18, 260, 192, 260)

    pdf.set_xy(18, 263)
    pdf.set_font("ArialUni", "B", 8.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(174, 5, "Salamanca, Guanajuato, México — Universidad Tecnológica de Salamanca", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # ==============================================================
    # PÁGINA 2: INTRODUCCIÓN Y DESCRIPCIÓN DEL PROYECTO
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_section_title("2", "INTRODUCCIÓN")

    render_p("El desarrollo de software móvil profesional exige un riguroso balance entre velocidad de entrega, estabilidad técnica y satisfacción de necesidades humanas reales. Iniciar la codificación de una aplicación sin una fase previa de análisis, alcance y planeación representa uno de los factores primordiales de fracaso en la ingeniería de software.")

    render_sub_heading("2.1 ¿Por qué es importante planificar un proyecto antes de programar?")
    render_p("Planificar permite dimensionar las restricciones del sistema antes de escribir código: hardware móvil, batería, permisos del SO, consumo de datos y resiliencia ante pérdida de conectividad en campus escolares.")
    render_p("Una adecuada planificación previene la acumulación de deuda técnica, minimiza los retrabajos que consumen semanas de esfuerzo, evita desacuerdos internos en el equipo y asegura que la arquitectura adoptada soporte el crecimiento proyectado del sistema.")

    render_sub_heading("2.2 ¿Cómo ayudan las metodologías ágiles a los equipos de desarrollo móvil?")
    render_p("En el ecosistema móvil, caracterizado por pantallas táctiles, constante evolución de SO y alta demanda de inmediatez por parte del usuario, las metodologías ágiles aportan ventajas decisivas:")
    render_bullet("Entregas frecuentes e incrementales (Sprints)", "Permiten obtener builds ejecutables (APKs) cada 2 semanas, facilitando que usuarios y la docente interactúen con el producto desde etapas tempranas.")
    render_bullet("Adaptabilidad inmediata ante el cambio", "Si la cámara o una regla en la nube presenta retos, el equipo ajusta el backlog en la siguiente iteración sin comprometer la entrega final.")
    render_bullet("Transparencia y autoorganización", "La sincronización continua en tableros y dailies visibiliza bloqueos y enfoca el esfuerzo en las tareas de mayor valor.")

    render_section_title("3", "DESCRIPCIÓN DEL PROYECTO MÓVIL")
    render_info_box("Nombre Tentativo del Proyecto: LabPass QR",
                    "Sistema Móvil Integral para la Digitalización, Control, Préstamo y Trazabilidad de Materiales, Componentes y Equipamiento en Laboratorios de la Universidad Tecnológica de Salamanca (UTS).", "blue")

    render_sub_heading("3.1 Breve descripción de su propósito")
    render_p("En los laboratorios de cómputo, redes, electrónica y mecatrónica de la UTS, el control de entradas y salidas de material se efectúa mediante bitácoras de firmas en papel o registros aislados en hojas de cálculo. Este método tradicional provoca largas filas en horas pico de cambio de clase (10 a 20 minutos de espera), extravíos recurrentes de componentes y falta de certeza sobre quién tiene asignado cada activo.")
    render_p("LabPass QR resuelve esta problemática integrando códigos QR dinámicos en las credenciales digitales de los alumnos y códigos QR serializados en cada activo físico del laboratorio. Mediante la cámara del smartphone del laboratorista, el sistema concreta préstamos y devoluciones en un tiempo récord de 3 a 5 segundos por transacción, con registro automático en la nube y notificaciones en tiempo real.")

    render_sub_heading("3.2 Público objetivo (Segmentos de usuario)")
    render_bullet("Alumnos de la UTS (Usuarios Finales Solicitantes)", "Estudiantes de ingenierías y TSU que requieren insumos para prácticas. Buscan inmediatez en ventanilla, consulta de stock remoto y comprobante digital de entrega.")
    render_bullet("Encargados y Laboratoristas (Usuarios de Operación)", "Personal técnico responsable del resguardo de equipo. Requieren escaneo continuo ágil, control de préstamos activos, alertas de entrega vencida y toma de evidencia fotográfica de averías.")
    render_bullet("Direcciones de Carrera y Administración Escolar", "Autoridades universitarias interesadas en preservar el patrimonio institucional, reducir compras por mermas y auditar la tasa de uso de infraestructura.")

    # ==============================================================
    # PÁGINA 3: FUNCIONALIDADES Y METODOLOGÍA ÁGIL
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_sub_heading("3.3 Funcionalidades Principales (Características Fijas + Propuesta Adicional)")

    features = [
        ("1. Escaneo y Vinculación Rápida con Cámara QR (Core Fijo 1)",
         "Lectura nativa de alta velocidad con cámara que escanea en un solo paso la credencial QR del alumno y el código del activo físico, registrando matrícula, ID de equipo, fecha, hora y responsable en menos de 5 segundos."),
        
        ("2. Catálogo Dinámico de Inventario en Tiempo Real (Core Fijo 2)",
         "Visualización estructurada de insumos clasificados por laboratorio, indicando en tiempo real si el activo está 'Disponible', 'En Préstamo' (con hora estimada de retorno) o 'En Mantenimiento', accesible remotamente desde el aula."),
        
        ("3. Módulo de Devolución, Finiquito y Registro de Incidencias (Core Fijo 3)",
         "Cierre ágil del préstamo mediante re-escaneo inverso que libera el equipo en la base de datos de inmediato. Incluye captura fotográfica obligatoria si el material se entrega roto, incompleto o con daños para deslindar responsabilidades."),
        
        ("4. Sistema de Alertas y Notificaciones Push Inteligentes (Core Fijo 4)",
         "Disparo automático de recordatorios al smartphone del estudiante 15 minutos antes de la hora límite de entrega de clase y avisos preventivos al laboratorista sobre materiales no devueltos."),
        
        ("5. Soporte y Persistencia Offline-First con Caché Local (Core Fijo 5)",
         "Almacenamiento local (SQLite / Hive) que permite al laboratorista seguir prestando y recibiendo material aun si la red Wi-Fi universitaria presenta caídas temporales, sincronizándose de forma transparente al recuperar conexión.")
    ]

    for title, desc in features:
        render_bullet(title, desc)

    render_info_box("[PROPUESTA ADICIONAL] Comprobante Digital Criptográfico de No-Adeudo",
                    "Generación instantánea de una constancia digital en PDF con código QR y token criptográfico verificable cuando el estudiante devuelve el material en orden. Permite al alumno respaldar la entrega ante sus docentes y agiliza el trámite de finiquito cuatrimestral sin necesidad de cartas físicas ni firmas manuales.", "orange")

    render_section_title("4", "METODOLOGÍA ÁGIL SELECCIONADA")
    render_info_box("Metodología Seleccionada: SCRUM (con Gestión de Flujo Scrumban)",
                    "El equipo adoptó el marco de trabajo Scrum debido a su enfoque en ciclos iterativos cortos, entregas incrementales funcionales y distribución clara de responsabilidades en equipos colaborativos de desarrollo.", "blue")

    render_sub_heading("4.1 Justificación de su elección para este proyecto móvil")
    render_bullet("Adaptación al calendario académico", "Los Sprints de 2 semanas sincronizan de manera natural los entregables funcionales (APKs) con las fechas de evaluación de parciales solicitadas por la docente.")
    render_bullet("Mitigación de riesgos de hardware", "La integración de la cámara móvil y lectura óptica de QR conlleva pruebas con distintas calidades de luz; Scrum permite abordar estas pruebas de concepto en el Sprint 1 y 2.")
    render_bullet("Claridad en roles para 4 desarrolladores", "Permite estructurar las tareas técnicas en historias de usuario bien delimitadas (Frontend Flutter, Backend Firebase, Calidad y Requerimientos), evitando duplicidad de esfuerzos.")

    render_sub_heading("4.2 Explicación de funcionamiento y organización del equipo")
    render_p("El proyecto se organiza bajo los eventos, artefactos y tableros formales de Scrum:")
    render_bullet("Sprint Planning (Planificación)", "Reunión quincenal de 1 hora para seleccionar historias del Product Backlog y fijar el objetivo del Sprint.")
    render_bullet("Daily Standup (Sincronización Diaria)", "Reunión de 10 minutos (vía Discord / presencial en campus): ¿Qué avancé ayer? ¿Qué haré hoy? ¿Qué bloqueos tengo?")
    render_bullet("Sprint Review y Retrospectiva", "Presentación del APK funcional a la docente Ericka Nohemí Álvarez Valencia para validación técnica y sesión de mejora continua.")
    render_bullet("Tablero Digital (Trello / GitHub Projects)", "Flujo visual en 5 columnas con límites WIP: Product Backlog -> To Do -> In Progress -> Code Review / QA -> Done.")
    render_bullet("Estrategia GitFlow", "Control de versiones en GitHub protegiendo la rama main y utilizando develop y feature branches con Pull Requests obligatorios.")

    # ==============================================================
    # PÁGINA 4: TABLA DE SPRINTS Y TABLA DE ROLES
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_sub_heading("4.3 Plan de Trabajo por Sprints (Cronograma del Proyecto)")

    pdf.set_fill_color(15, 76, 129)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("ArialUni", "B", 8)
    pdf.cell(24, 6.5, "Sprint", 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C", fill=True)
    pdf.cell(85, 6.5, "Objetivo del Sprint (Sprint Goal)", 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C", fill=True)
    pdf.cell(65, 6.5, "Entregable Funcional (Incremento)", 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C", fill=True)

    sprints_data = [
        ("Sprint 1\n(Sem 1-2)", "Configurar proyecto en Flutter con Clean Architecture, Firebase Auth con roles y diseño de maquetas UI.", "APK v0.1 con navegación base y autenticación institucional."),
        ("Sprint 2\n(Sem 3-4)", "Integrar lector QR con cámara (Mobile Scanner), credencial digital y catálogo de stock en tiempo real.", "APK v0.2 capaz de leer códigos de material y listar inventario."),
        ("Sprint 3\n(Sem 5-6)", "Lógica transaccional de préstamo, devolución con foto de incidencia y persistencia local offline (Hive).", "APK v0.3 con ciclo de préstamo/retorno y funcionamiento offline."),
        ("Sprint 4\n(Sem 7-8)", "Notificaciones Push (FCM), comprobante digital criptográfico de no-adeudo y empaquetado release.", "Release Final APK v1.0, manual de usuario y documentación.")
    ]

    for sp, goal, inc in sprints_data:
        pdf.set_font("ArialUni", "B", 8)
        pdf.set_text_color(15, 76, 129)
        pdf.cell(24, 11, sp, 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
        
        pdf.set_font("ArialUni", "", 7.8)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(85, 11, goal, 1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(65, 11, inc, 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(3)
    render_section_title("5", "ROLES DENTRO DEL EQUIPO")
    render_p("Conforme a las mejores prácticas de la metodología Scrum, la asignación de responsabilidades para los cuatro estudiantes de IDGS se estructuró de la siguiente manera:")

    pdf.set_fill_color(15, 76, 129)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("ArialUni", "B", 8)
    pdf.cell(45, 6.5, "Integrante (IDGS)", 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C", fill=True)
    pdf.cell(38, 6.5, "Rol Ágil Asignado", 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C", fill=True)
    pdf.cell(91, 6.5, "Responsabilidades Principales", 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C", fill=True)

    roles_data = [
        ("Alvaro Jesús Chávez Bazana", "Product Owner (PO)\nGestor de Requisitos",
         "- Definir la visión y alcance del producto.\n- Crear y priorizar las historias de usuario del Product Backlog.\n- Definir criterios de aceptación (Definition of Done).\n- Validar entregas con la docente y recopilar feedback de laboratoristas."),
        
        ("Guillermo Yael Berlín Fomperosa", "Scrum Master (SM)\nFacilitador & QA",
         "- Guiar al equipo en las ceremonias Scrum (Planning, Daily, Review, Retro).\n- Remover bloqueos e impedimentos técnicos u organizacionales.\n- Administrar el tablero en Trello/GitHub y diseñar pruebas de calidad (QA)."),
        
        ("Juan Pablo Vega Uribe", "Lead Mobile Developer\nFrontend & UI/UX",
         "- Desarrollar las interfaces de usuario en Flutter (Dart) con Material 3.\n- Implementar navegación reactiva y gestión de estado (BLoC).\n- Integrar el controlador de cámara para lectura QR de alta velocidad.\n- Garantizar accesibilidad y rendimiento nativo en Android/iOS."),
        
        ("Diego Sebastián Vilegas Enriquez", "Backend & Data Architect\nCloud BaaS & Offline",
         "- Modelar la base de datos documental en Firebase Cloud Firestore.\n- Configurar autenticación, reglas de seguridad y control por roles (RBAC).\n- Implementar persistencia local Offline-First con Hive/SQLite.\n- Configurar Notificaciones Push (FCM) y Cloud Storage para evidencias.")
    ]

    for member, role_lbl, resp in roles_data:
        pdf.set_font("ArialUni", "B", 8)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(45, 17, member, 1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        
        pdf.set_font("ArialUni", "I", 7.8)
        pdf.set_text_color(14, 116, 144)
        pdf.cell(38, 17, role_lbl, 1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        
        pdf.set_font("ArialUni", "", 7.5)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(91, 4.2, resp, 1)

    pdf.ln(3)
    render_section_title("6", "JUSTIFICACIÓN DE LA ARQUITECTURA PROPUESTA")
    render_info_box("Arquitectura Seleccionada: Clean Architecture + MVVM + Cloud BaaS",
                    "Se diseñó una arquitectura desacoplada en 3 capas fundamentales (Presentación, Dominio y Datos) implementando el Patrón Repositorio y persistencia híbrida Offline-First.", "blue")

    render_sub_heading("6.1 ¿Por qué es la arquitectura más adecuada para LabPass QR?")
    render_bullet("Separación estricta de responsabilidades", "La Capa de Presentación (vistas Flutter y widgets) se encuentra totalmente desacoplada de la base de datos y de la lógica de negocio, lo que permite modificar el diseño sin alterar reglas de validación.")
    render_bullet("Alta testabilidad en la Capa de Dominio", "Los Casos de Uso (ej. RegistrarPrestamoUseCase, DevolverActivoUseCase) son clases de Dart puro libres de dependencias de Flutter o Firebase, permitiendo ejecutar pruebas unitarias automáticas sin emuladores.")
    render_bullet("Estrategia Offline-First con Repository Pattern", "En los talleres de la UTS la señal Wi-Fi suele ser débil; el repositorio decide de forma transparente si obtiene datos de la memoria local (Hive) o de la nube (Firestore), encolando transacciones.")
    render_bullet("Aceleración del desarrollo mediante BaaS", "El uso de Firebase suprime la necesidad de programar servidores backend dedicados, permitiendo al equipo concentrarse en la experiencia de usuario y en la lectura veloz de códigos QR.")

    # ==============================================================
    # PÁGINA 5: DIAGRAMA DE FLUJO DE PANTALLAS
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_section_title("7", "DIAGRAMA DE LA ARQUITECTURA Y FLUJO DE PANTALLAS")

    render_sub_heading("7.1 Diagrama de Navegación y Flujo de Pantallas (Screen Flow)")
    render_p("El siguiente diagrama visual ilustra la jerarquía de pantallas de la aplicación, el proceso de autenticación institucional centralizado y la derivación de vistas según el rol del usuario (Estudiante vs. Laboratorista), detallando las transiciones y eventos de interacción:")

    if os.path.exists("diagram_flujo_pantallas.png"):
        img_y = pdf.get_y()
        pdf.image("diagram_flujo_pantallas.png", x=18, y=img_y, w=174)
        pdf.set_y(img_y + 125)

    render_sub_heading("Descripción de Transiciones y Navegación entre Pantallas:")
    render_bullet("Transición de Splash (1) a Login (2)", "Verificación automática de token de sesión almacenado. Si no existe sesión activa, conduce al formulario de acceso con credenciales universitarias.")
    render_bullet("Derivación por Rol (2 a 3A / 3B)", "Tras validar credenciales en Firebase Auth, el router redirige automáticamente al Dashboard de Alumno (3A) o al Panel de Laboratorista (3B) según los claims de usuario.")
    render_bullet("Flujo de Préstamo Rápido (3B -> 4C -> 5B)", "El laboratorista activa el botón de cámara (4C), escanea el QR de la credencial del alumno y consecutivamente el QR del activo; la app muestra la pantalla de confirmación (5B) con asignación en menos de 3 segundos.")
    render_bullet("Devolución con Evidencia (6B -> 7A)", "Al recibir el material, el laboratorista libera el stock y puede capturar una foto si hay averías. Al confirmarse, se genera y desbloquea el comprobante digital de no-adeudo (7A) en el teléfono del alumno.")

    # ==============================================================
    # PÁGINA 6: DIAGRAMA DE ARQUITECTURA Y CONCLUSIONES
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_sub_heading("7.2 Diagrama de Arquitectura de Software en Capas (Clean Architecture)")
    render_p("Estructura técnica de capas concéntricas que rige la construcción de LabPass QR, garantizando el flujo unidireccional de datos y la persistencia local resiliente:")

    if os.path.exists("diagram_arquitectura_capas.png"):
        img_y2 = pdf.get_y()
        pdf.image("diagram_arquitectura_capas.png", x=18, y=img_y2, w=174)
        pdf.set_y(img_y2 + 112)

    render_sub_heading("Componentes de la Arquitectura en Capas:")
    render_bullet("1. Capa de Presentación (Frontend Flutter)", "Contiene las pantallas, controladores BLoC, visor de enfoque de cámara (Mobile Scanner Overlay) y widgets de navegación.")
    render_bullet("2. Capa de Dominio (Casos de Uso Puros)", "Contiene la lógica de negocio central (RegistrarPrestamo, DevolverActivo, ConsultarStock) y las entidades del modelo de dominio.")
    render_bullet("3. Capa de Datos (Repository Pattern)", "Intermediario inteligente que arbitra entre el Local DataSource (Caché Hive/SQLite) y el Remote DataSource (Firebase Cloud Firestore, Auth, FCM y Storage).")

    pdf.ln(3)
    render_section_title("8", "CONCLUSIÓN DE LA FASE 1")
    render_info_box("Compromiso y Conclusión del Equipo de Desarrollo (IDGS)",
                    "La culminación del Plan del Proceso de Desarrollo Móvil (Fase 1) establece los cimientos estratégicos y técnicos del proyecto LabPass QR. La combinación del marco ágil Scrum, la asignación especializada de roles para sus cuatro integrantes (Alvaro, Guillermo, Juan Pablo y Diego) y una Clean Architecture con enfoque Offline-First aseguran una ejecución ordenada, orientada a la excelencia académica y lista para dar inicio al Sprint 1.", "blue")

    pdf.output(output_pdf_path)
    print(f"PDF generado con éxito: {output_pdf_path}")

if __name__ == "__main__":
    out_pdf = "c:\\Users\\galan\\OneDrive - Universidad Tecnológica de Salamanca\\Aplicación\\Fase1_Plan_Desarrollo_Movil_LabPassQR.pdf"
    build_pdf(out_pdf)
