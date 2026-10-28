import os
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from fpdf.fonts import FontFace

class SaveBitePhase1PDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=16)
        self.set_margins(18, 16, 18)
        
        # Cargar fuentes TrueType completas de Windows con soporte Unicode
        self.add_font("ArialUni", "", r"C:\Windows\Fonts\arial.ttf")
        self.add_font("ArialUni", "B", r"C:\Windows\Fonts\arialbd.ttf")
        self.add_font("ArialUni", "I", r"C:\Windows\Fonts\ariali.ttf")
        self.add_font("ArialUni", "BI", r"C:\Windows\Fonts\arialbi.ttf")

    def header(self):
        if self.page_no() > 1:
            self.set_fill_color(245, 248, 252)
            self.rect(0, 0, 210, 13, "F")
            
            self.set_draw_color(0, 174, 157)
            self.set_line_width(0.6)
            self.line(18, 12, 192, 12)

            self.set_xy(18, 3)
            self.set_font("ArialUni", "B", 7.8)
            self.set_text_color(15, 76, 129)
            self.cell(100, 5, "UNIVERSIDAD TECNOLÓGICA DE SALAMANCA • IDGS 10°", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)

            self.set_font("ArialUni", "I", 7.8)
            self.set_text_color(100, 116, 139)
            self.cell(74, 5, "Fase 1: Plan de Desarrollo Móvil | SaveBite", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-13)
            self.set_draw_color(226, 232, 240)
            self.set_line_width(0.4)
            self.line(18, 284, 192, 284)

            self.set_xy(18, 285)
            self.set_font("ArialUni", "", 7.8)
            self.set_text_color(100, 116, 139)
            self.cell(100, 5, "Desarrollo Móvil Integral — Docente: Ericka Nohemí Álvarez Valencia", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
            
            self.set_font("ArialUni", "B", 7.8)
            self.set_text_color(15, 76, 129)
            self.cell(74, 5, f"Página {self.page_no()}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

def build_pdf(output_pdf_path):
    pdf = SaveBitePhase1PDF()

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
        pdf.set_font("ArialUni", "B", 11)
        pdf.set_text_color(15, 76, 129)
        pdf.cell(165, 6.5, title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_draw_color(203, 213, 225)
        pdf.set_line_width(0.5)
        pdf.line(18, pdf.get_y() + 1, 192, pdf.get_y() + 1)
        pdf.ln(2)

    def render_sub_heading(title):
        pdf.set_font("ArialUni", "B", 9.2)
        pdf.set_text_color(14, 116, 144)
        pdf.cell(174, 4.8, f"> {title}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.8)

    def render_p(text, spacing=1.5):
        pdf.set_font("ArialUni", "", 8.4)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(174, 4.1, text)
        pdf.ln(spacing)

    def render_bullet(title, desc, spacing=1.2):
        pdf.set_x(20)
        pdf.set_font("ArialUni", "B", 8.3)
        pdf.set_text_color(15, 76, 129)
        prefix = f"- {title}: "
        pdf.write(4.1, prefix)
        
        pdf.set_font("ArialUni", "", 8.3)
        pdf.set_text_color(51, 65, 85)
        pdf.write(4.1, desc + "\n")
        pdf.ln(spacing)

    def render_info_box(title, text, color="blue", h_fixed=None):
        y = pdf.get_y()
        bg_c = (240, 249, 255) if color == "blue" else (255, 251, 235)
        border_c = (14, 116, 144) if color == "blue" else (245, 158, 11)
        
        pdf.set_font("ArialUni", "", 8.2)
        lines = len(pdf.multi_cell(164, 3.8, f"{title}\n{text}", dry_run=True, output="LINES"))
        box_h = h_fixed if h_fixed else max(13, (lines * 3.8) + 5)

        pdf.set_fill_color(*bg_c)
        pdf.set_draw_color(226, 232, 240)
        pdf.rect(18, y, 174, box_h, "FD")
        pdf.set_fill_color(*border_c)
        pdf.rect(18, y, 3, box_h, "F")

        pdf.set_xy(23, y + 2)
        pdf.set_font("ArialUni", "B", 8.6)
        pdf.set_text_color(*border_c)
        pdf.cell(164, 4, title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_x(23)
        pdf.set_font("ArialUni", "", 8.1)
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
    pdf.cell(180, 11, "SaveBite", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("ArialUni", "I", 10.5)
    pdf.set_text_color(220, 240, 255)
    pdf.cell(180, 5.5, "Rescate de Excedentes de Alimentos Locales a Precio Reducido (ODS 12: Cero Merma)", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

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
    render_p("Planificar permite dimensionar las restricciones del sistema antes de escribir código: consumo de batería por geolocalización continua (GPS), permisos del sistema operativo (cámara y notificaciones push), conectividad variable en calle y diseño de esquemas de datos eficientes.")
    render_p("Una adecuada planificación previene la acumulación de deuda técnica, minimiza los retrabajos que consumen semanas de esfuerzo, evita desacuerdos internos en el equipo y asegura que la arquitectura adoptada soporte el crecimiento proyectado del sistema.")

    render_sub_heading("2.2 ¿Cómo ayudan las metodologías ágiles a los equipos de desarrollo móvil?")
    render_p("En el ecosistema móvil, caracterizado por pantallas táctiles, constante evolución de SO y alta demanda de inmediatez por parte del usuario, las metodologías ágiles aportan ventajas decisivas:")
    render_bullet("Entregas frecuentes e incrementales (Sprints)", "Permiten obtener builds ejecutables (APKs) cada 2 semanas, facilitando que usuarios y la docente interactúen con el producto desde etapas tempranas.")
    render_bullet("Adaptabilidad inmediata ante el cambio", "Si la API de mapas, la cámara o una regla en la nube presenta retos, el equipo ajusta el backlog en la siguiente iteración sin comprometer la entrega final.")
    render_bullet("Transparencia y autoorganización", "La sincronización continua en tableros y dailies visibiliza bloqueos y enfoca el esfuerzo en las tareas de mayor valor.")

    render_section_title("3", "DESCRIPCIÓN DEL PROYECTO MÓVIL")
    render_info_box("Nombre Tentativo del Proyecto: SaveBite (CeroMerma)",
                    "Plataforma móvil colaborativa de economía circular que conecta comercios locales de alimentos (panaderías, cafeterías, fruterías, pizzerías) con la comunidad para rescatar comida del día en perfecto estado mediante 'Paquetes Sorpresa' con 50% a 70% de descuento antes del cierre.", "blue")

    render_sub_heading("3.1 Breve descripción de su propósito")
    render_p("Diariamente, cientos de establecimientos gastronómicos en zonas urbanas y universitarias descartan alimentos frescos en óptimas condiciones por no haberse vendido durante el horario comercial regular. Al mismo tiempo, miles de estudiantes universitarios y familias enfrentan restricciones económicas severas para adquirir alimentos preparados de calidad.")
    render_p("SaveBite resuelve ambos problemas simultáneamente: permite a los comercios publicar a media tarde sus excedentes en forma de 'Paquetes Sorpresa' a precios accesibles, mientras que los usuarios exploran las ofertas en un mapa interactivo con GPS, reservan en la app y recogen su paquete en mostrador antes del cierre escaneando un código QR. El proyecto impacta positivamente en los Objetivos de Desarrollo Sostenible (ODS de la ONU), en particular el ODS 12 (Producción y Consumo Responsables) y ODS 2 (Hambre Cero).")

    render_sub_heading("3.2 Público objetivo (Segmentos de usuario)")
    render_bullet("Estudiantes Universitarios y Jóvenes (Consumidores)", "Alumnos de la UTS y jóvenes con presupuesto limitado que buscan comida nutritiva y variada a costos accesibles (ahorro del 50% al 70%).")
    render_bullet("Comercios Gastronómicos Locales (Aliados)", "Panaderías, cafeterías, pastelerías, fruterías y pizzerías que desean recuperar costos operativos de producción, evitar el desperdicio de merma y atraer nuevos clientes a su establecimiento.")
    render_bullet("Consumidores Eco-Conscientes y Comunidad", "Ciudadanos interesados en hábitos sostenibles, reducción del impacto ambiental urbano y mitigación del desperdicio de comida.")

    # ==============================================================
    # PÁGINA 3: FUNCIONALIDADES Y METODOLOGÍA ÁGIL
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_sub_heading("3.3 Funcionalidades Principales (Características Fijas + Propuesta Adicional)")

    features = [
        ("1. Geolocalización y Mapa Interactivo con GPS (Core Fijo 1)",
         "Exploración en vivo de comercios locales cercanos que disponen de paquetes sorpresa activos, visualizados mediante marcadores dinámicos en un mapa interactivo con cálculo de distancias y rutas de recolección a pie o en auto."),
        
        ("2. Catálogo de Paquetes Sorpresa y Reserva In-App (Core Fijo 2)",
         "Ficha detallada por establecimiento con precio original vs. precio reducido (50% al 70% de descuento), descripción del tipo de comida (dulce, salada, vegetariana), ventana horaria estricta de recogida y reserva instantánea con 1 toque."),
        
        ("3. Validación de Canje por Escaneo de Código QR con Cámara (Core Fijo 3)",
         "Cierre seguro de la transacción en mostrador: la app genera un ticket digital con código QR dinámico en el teléfono del comprador, el cual es escaneado por la cámara del comerciante para validar el canje en menos de 2 segundos."),
        
        ("4. Sistema de Alertas y Notificaciones Push en Tiempo Real (Core Fijo 4)",
         "Avisos automáticos al celular mediante Firebase Cloud Messaging (FCM) cuando los comercios favoritos del usuario publican nuevos paquetes disponibles o recordatorios preventivos cuando restan 30 minutos de la ventana de recogida."),
        
        ("5. Modo Offline-First con Caché Local (Core Fijo 5)",
         "Persistencia local de vouchers de reserva y datos del comercio con SQLite / Hive, permitiendo al usuario presentar su código QR de canje en mostrador aun si pierde conexión a datos móviles en la vía pública.")
    ]

    for title, desc in features:
        render_bullet(title, desc)

    render_info_box("[PROPUESTA ADICIONAL] Calculadora de Impacto Ecológico y Social (Métricas ODS)",
                    "Módulo interactivo en el perfil del usuario que contabiliza en tiempo real los kilogramos de comida rescatados del vertedero, el dinero ahorrado acumulado y la reducción estimada en kilogramos de emisiones de gases de efecto invernadero (CO2 equivalente), con insignias gamificadas que premian la constancia ecológica.", "orange")

    render_section_title("4", "METODOLOGÍA ÁGIL SELECCIONADA")
    render_info_box("Metodología Seleccionada: SCRUM (con Gestión de Flujo Scrumban)",
                    "El equipo adoptó el marco de trabajo Scrum debido a su enfoque en ciclos iterativos cortos, entregas incrementales funcionales y distribución clara de responsabilidades en equipos colaborativos de desarrollo.", "blue")

    render_sub_heading("4.1 Justificación de su elección para este proyecto móvil")
    render_bullet("Adaptación al calendario académico", "Los Sprints de 2 semanas sincronizan de manera natural los entregables funcionales (APKs) con las fechas de evaluación de parciales solicitadas por la docente.")
    render_bullet("Mitigación de riesgos de hardware móvil", "SaveBite integra múltiples sensores físicos (GPS, sensor de cámara para escaneo QR y notificaciones push en segundo plano); Scrum permite probar cada componente de hardware en prototipos tempranos.")
    render_bullet("Claridad en roles para 4 desarrolladores", "Permite estructurar las tareas técnicas en historias de usuario bien delimitadas (Frontend Flutter, Backend Firebase, Calidad y Requerimientos), evitando duplicidad de esfuerzos.")

    render_sub_heading("4.2 Explicación de funcionamiento y organización del equipo")
    render_p("El proyecto se organiza bajo los eventos, artefactos y tableros formales de Scrum:")
    render_bullet("Sprint Planning (Planificación)", "Reunión quincenal de 1 hora para seleccionar historias del Product Backlog y fijar el objetivo del Sprint.")
    render_bullet("Daily Standup (Sincronización Diaria)", "Reunión de 10 minutos (vía Discord / presencial en campus): ¿Qué avancé ayer? ¿Qué haré hoy? ¿Qué bloqueos tengo?")
    render_bullet("Sprint Review y Retrospectiva", "Presentación del APK funcional a la docente Ericka Nohemí Álvarez Valencia para validación técnica y sesión de mejora continua.")
    render_bullet("Tablero Digital (Trello / GitHub Projects)", "Flujo visual en 5 columnas con límites WIP: Product Backlog -> To Do -> In Progress -> Code Review / QA -> Done.")
    render_bullet("Estrategia GitFlow", "Control de versiones en GitHub protegiendo la rama main y utilizando develop y feature branches con Pull Requests obligatorios.")

    # ==============================================================
    # PÁGINA 4: TABLA DE SPRINTS Y TABLA DE ROLES (USANDO PDF.TABLE)
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_sub_heading("4.3 Plan de Trabajo por Sprints (Cronograma del Proyecto)")

    # Encabezado estilizado para tablas nativas
    h_style = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(15, 76, 129))

    sprints_rows = [
        ("Sprint 1\n(Sem 1-2)",
         "Configurar proyecto Flutter con Clean Architecture, Firebase Auth con roles (Usuario/Comercio) y mapas base con Google Maps SDK.",
         "APK v0.1 con autenticación y visualización de mapa con geolocalización."),
        
        ("Sprint 2\n(Sem 3-4)",
         "Módulo de publicación de paquetes sorpresa por comercios y catálogo con filtros de distancia en tiempo real con Firestore.",
         "APK v0.2 capaz de explorar ofertas activas en el mapa y consultar fichas de establecimientos."),
        
        ("Sprint 3\n(Sem 5-6)",
         "Lógica de reserva, generación de voucher QR, módulo de escaneo con cámara para comercios y persistencia offline con Hive.",
         "APK v0.3 con ciclo completo de reserva in-app y validación de canje con QR en mostrador."),
        
        ("Sprint 4\n(Sem 7-8)",
         "Notificaciones Push (FCM), calculadora de impacto ecológico (CO2 y dinero ahorrado), pruebas y release final.",
         "Release Final APK v1.0, manual de usuario y documentación técnica completa.")
    ]

    pdf.set_font("ArialUni", "", 7.8)
    with pdf.table(col_widths=(26, 84, 64), headings_style=h_style, line_height=4.2, text_align=("CENTER", "LEFT", "LEFT")) as table:
        header_row = table.row()
        header_row.cell("Sprint")
        header_row.cell("Objetivo del Sprint (Sprint Goal)")
        header_row.cell("Entregable Funcional (Incremento)")

        for sp, goal, inc in sprints_rows:
            r = table.row()
            r.cell(sp)
            r.cell(goal)
            r.cell(inc)

    pdf.ln(3)
    render_section_title("5", "ROLES DENTRO DEL EQUIPO")
    render_p("Conforme a las mejores prácticas de la metodología Scrum, la asignación de responsabilidades para los cuatro estudiantes de IDGS se estructuró de la siguiente manera:")

    roles_rows = [
        ("Alvaro Jesús Chávez Bazana\n(IDGS - UTS)",
         "Product Owner (PO)\nGestor de Requisitos",
         "• Definir la visión y propuesta de valor de SaveBite (modelo ODS).\n• Crear y priorizar las historias de usuario en el Product Backlog.\n• Definir criterios de aceptación (Definition of Done) para cada función.\n• Validar entregas con la docente y recoger feedback de comercios locales."),
        
        ("Guillermo Yael Berlín Fomperosa\n(IDGS - UTS)",
         "Scrum Master (SM)\nFacilitador & QA",
         "• Guiar al equipo en las ceremonias Scrum (Planning, Daily, Review, Retro).\n• Remover bloqueos e impedimentos técnicos u organizacionales.\n• Administrar el tablero en Trello/GitHub y diseñar pruebas de calidad (QA).\n• Monitorear el cumplimiento de los tiempos de entrega de cada Sprint."),
        
        ("Juan Pablo Vega Uribe\n(IDGS - UTS)",
         "Lead Mobile Developer\nFrontend & UI/UX",
         "• Desarrollar las interfaces de usuario en Flutter (Dart) con Material 3.\n• Implementar mapa interactivo con Google Maps SDK y navegación reactiva BLoC.\n• Integrar visor de cámara para escaneo QR de vouchers con baja latencia.\n• Diseñar flujo fluido e intuitivo para reserva y canje en mostrador."),
        
        ("Diego Sebastián Vilegas Enriquez\n(IDGS - UTS)",
         "Backend & Data Architect\nCloud BaaS & Offline",
         "• Modelar la base de datos documental y consultas geoespaciales con Geohashing.\n• Configurar autenticación, reglas de seguridad y control por roles (RBAC).\n• Implementar persistencia local Offline-First con Hive/SQLite para vouchers.\n• Configurar Notificaciones Push (FCM) y Cloud Functions para vencimientos.")
    ]

    pdf.set_font("ArialUni", "", 7.5)
    with pdf.table(col_widths=(44, 40, 90), headings_style=h_style, line_height=4.0, text_align=("LEFT", "LEFT", "LEFT")) as table:
        header_row = table.row()
        header_row.cell("Integrante (IDGS)")
        header_row.cell("Rol Ágil Asignado")
        header_row.cell("Responsabilidades Principales")

        for member, role_lbl, resp in roles_rows:
            r = table.row()
            r.cell(member)
            r.cell(role_lbl)
            r.cell(resp)

    # ==============================================================
    # PÁGINA 5: ARQUITECTURA Y DIAGRAMA DE NAVEGACIÓN
    # ==============================================================
    pdf.add_page()
    pdf.set_y(16)
    render_section_title("6", "JUSTIFICACIÓN DE LA ARQUITECTURA PROPUESTA")
    render_info_box("Arquitectura Seleccionada: Clean Architecture + MVVM + Cloud BaaS",
                    "Se diseñó una arquitectura desacoplada en 3 capas fundamentales (Presentación, Dominio y Datos) implementando el Patrón Repositorio y persistencia híbrida Offline-First.", "blue")

    render_sub_heading("6.1 ¿Por qué es la arquitectura más adecuada para SaveBite?")
    render_bullet("Separación estricta de responsabilidades", "La Capa de Presentación (vistas Flutter y widgets de mapa) se encuentra totalmente desacoplada de la base de datos y de la lógica de negocio, permitiendo modificar la UI sin alterar reglas de reserva.", spacing=0.8)
    render_bullet("Alta testabilidad en la Capa de Dominio", "Los Casos de Uso (ej. ExplorarCercanosUseCase, ReservarPaqueteUseCase) son clases de Dart puro libres de dependencias de Flutter o Firebase, ejecutables en pruebas unitarias automáticas.", spacing=0.8)
    render_bullet("Estrategia Offline-First con Repository Pattern", "Si el usuario tiene señal débil en la calle al llegar al comercio, el repositorio recupera el voucher de la memoria local (Hive) y permite canjearlo con el código QR sin interrupción.", spacing=0.8)
    render_bullet("Aceleración del desarrollo mediante BaaS", "El uso de Firebase (Firestore + Auth + Cloud Functions) suprime la necesidad de programar servidores dedicados, acelerando el desarrollo hacia el MVP.", spacing=1.2)

    pdf.ln(1)
    render_section_title("7", "DIAGRAMA DE LA ARQUITECTURA Y FLUJO DE PANTALLAS")
    render_sub_heading("7.1 Diagrama de Navegación y Flujo de Pantallas (Screen Flow)")
    render_p("El siguiente diagrama visual ilustra la jerarquía de pantallas de SaveBite, la autenticación centralizada y la derivación de vistas según el perfil del usuario (Consumidor vs. Comercio Aliado):", spacing=1)

    if os.path.exists("diagram_flujo_pantallas_savebite.png"):
        img_y = pdf.get_y()
        pdf.image("diagram_flujo_pantallas_savebite.png", x=20, y=img_y, w=150)
        pdf.set_y(img_y + 108)

    render_sub_heading("Descripción de Transiciones y Navegación entre Pantallas:")
    render_bullet("Transición de Splash (1) a Login (2)", "Verificación automática de token de sesión. Si no existe sesión activa, conduce al acceso con selección de perfil.", spacing=0.8)
    render_bullet("Derivación por Rol (2 a 3A / 3B)", "Redirección automática al Mapa GPS y Feed de Ofertas (3A) para consumidores o al Panel del Establecimiento (3B) para comercios aliados.", spacing=0.8)
    render_bullet("Flujo de Reserva del Consumidor (3A -> 4A -> 5A -> 6A)", "El usuario visualiza un comercio, entra a la Ficha del Paquete (4A), realiza la reserva (5A) y la app genera su Voucher Digital con QR Dinámico (6A).", spacing=0.8)
    render_bullet("Validación de Canje en Mostrador (6A -> 5B -> 6B)", "El consumidor muestra el QR en tienda; el comerciante abre el lector de cámara (5B) y valida el canje en 2 segundos, liberando la entrega (6B) y sumando al impacto ODS (7A).", spacing=1.2)

    # ==============================================================
    # PÁGINA 6: DIAGRAMA DE ARQUITECTURA Y CONCLUSIÓN
    # ==============================================================
    pdf.add_page()
    pdf.set_y(16)
    render_sub_heading("7.2 Diagrama de Arquitectura de Software en Capas (Clean Architecture)")
    render_p("Estructura técnica de capas concéntricas que rige la construcción de SaveBite, garantizando el flujo unidireccional de datos, soporte para geolocalización y persistencia local resiliente:", spacing=1)

    if os.path.exists("diagram_arquitectura_capas_savebite.png"):
        img_y2 = pdf.get_y()
        pdf.image("diagram_arquitectura_capas_savebite.png", x=20, y=img_y2, w=150)
        pdf.set_y(img_y2 + 96)

    render_sub_heading("Componentes de la Arquitectura en Capas:")
    render_bullet("1. Capa de Presentación (Frontend Flutter)", "Contiene las pantallas, controladores BLoC, mapa interactivo (Google Maps SDK), visor de escaneo de cámara (Mobile Scanner) y componentes Material Design 3.", spacing=0.8)
    render_bullet("2. Capa de Dominio (Casos de Uso Puros)", "Contiene la lógica de negocio central (ExplorarCercanos, ReservarPaquete, ValidarEntregaQR, CalcularImpactoODS) y las entidades del modelo de datos.", spacing=0.8)
    render_bullet("3. Capa de Datos (Repository Pattern)", "Intermediario inteligente que arbitra entre el Local DataSource (Caché Hive/SQLite) y el Remote DataSource (Firebase Cloud Firestore con Geohashing, Auth, FCM y Storage).", spacing=1.2)

    pdf.ln(1)
    render_section_title("8", "CONCLUSIÓN DE LA FASE 1")
    render_info_box("Compromiso y Conclusión del Equipo de Desarrollo (IDGS)",
                    "La culminación del Plan del Proceso de Desarrollo Móvil (Fase 1) para SaveBite establece una propuesta sólida, técnica y socialmente relevante. Al alinearse con los Objetivos de Desarrollo Sostenible (ODS 12) y apoyarse en una arquitectura Clean Architecture resiliente y el marco ágil Scrum, el equipo (Alvaro, Guillermo, Juan Pablo y Diego) se encuentra perfectamente preparado para iniciar con éxito el Sprint 1 de implementación móvil.", "blue")

    pdf.output(output_pdf_path)
    print(f"PDF SaveBite corregido y generado con éxito: {output_pdf_path}")

if __name__ == "__main__":
    out_pdf = "c:\\Users\\galan\\OneDrive - Universidad Tecnológica de Salamanca\\Aplicación\\Fase1_Plan_Desarrollo_Movil_SaveBite.pdf"
    build_pdf(out_pdf)
