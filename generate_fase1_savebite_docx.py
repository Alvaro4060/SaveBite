import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_savebite_docx(output_path):
    doc = docx.Document()

    # Configuración de márgenes estándar (2.5 cm)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
        # Header y Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("UNIVERSIDAD TECNOLÓGICA DE SALAMANCA • IDGS | SaveBite Fase 1")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139)

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        frun = fp.add_run("Desarrollo Móvil Integral — Docente: Ericka Nohemí Álvarez Valencia")
        frun.font.name = "Arial"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 116, 139)

    # ==============================================================
    # 1. PORTADA COLORIDA Y FORMAL
    # ==============================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("UNIVERSIDAD TECNOLÓGICA DE SALAMANCA\n")
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(16)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(15, 76, 129)

    r_div = p_inst.add_run("División de Tecnologías de la Información y Comunicación\n")
    r_div.font.name = "Arial"
    r_div.font.size = Pt(11)
    r_div.font.color.rgb = RGBColor(70, 80, 95)

    r_car = p_inst.add_run("Ingeniería en Desarrollo y Gestión de Software (IDGS - 10° Cuatrimestre)\n")
    r_car.font.name = "Arial"
    r_car.font.size = Pt(12)
    r_car.font.bold = True
    r_car.font.color.rgb = RGBColor(0, 174, 157)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Banner Título
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_phase = p_title.add_run("FASE 1: PLAN DEL PROCESO DE DESARROLLO MÓVIL\n")
    r_phase.font.name = "Arial"
    r_phase.font.size = Pt(11)
    r_phase.font.bold = True
    r_phase.font.color.rgb = RGBColor(245, 130, 32)

    r_app = p_title.add_run("SaveBite\n")
    r_app.font.name = "Arial"
    r_app.font.size = Pt(28)
    r_app.font.bold = True
    r_app.font.color.rgb = RGBColor(15, 76, 129)

    r_sub = p_title.add_run("Rescate de Excedentes de Alimentos Locales a Precio Reducido (ODS 12: Cero Merma)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Tabla de Portada (Datos de Asignatura e Integrantes)
    cover_table = doc.add_table(rows=1, cols=2)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_meta = cover_table.cell(0, 0)
    cell_team = cover_table.cell(0, 1)

    set_cell_background(cell_meta, "F8FAFC")
    set_cell_background(cell_team, "F8FAFC")
    set_cell_margins(cell_meta, top=140, bottom=140, left=180, right=180)
    set_cell_margins(cell_team, top=140, bottom=140, left=180, right=180)

    # Contenido celda Asignatura
    p_cm = cell_meta.paragraphs[0]
    r = p_cm.add_run("DATOS DE LA ASIGNATURA\n\n")
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 76, 129)

    p_cm.add_run("Asignatura: ").font.bold = True
    p_cm.add_run("Desarrollo Móvil Integral\n")
    p_cm.add_run("Carrera: ").font.bold = True
    p_cm.add_run("IDGS (10° B)\n")
    p_cm.add_run("Docente: ").font.bold = True
    p_cm.add_run("Ericka Nohemí Álvarez Valencia\n")
    p_cm.add_run("Fecha de Entrega: ").font.bold = True
    r_f = p_cm.add_run("16 de Octubre de 2026\n")
    r_f.font.bold = True
    r_f.font.color.rgb = RGBColor(180, 83, 9)
    p_cm.add_run("Entregable: ").font.bold = True
    p_cm.add_run("Documento Digital Fase 1")

    # Contenido celda Integrantes
    p_ct = cell_team.paragraphs[0]
    r = p_ct.add_run("EQUIPO DE DESARROLLO (INTEGRANTES)\n\n")
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 174, 157)

    team_members = [
        ("Alvaro Jesús Chávez Bazana", "Product Owner (PO)"),
        ("Guillermo Yael Berlín Fomperosa", "Scrum Master (SM)"),
        ("Juan Pablo Vega Uribe", "Lead Mobile Developer (UI/UX)"),
        ("Diego Sebastián Vilegas Enriquez", "Backend & Data Architect")
    ]
    for name, role in team_members:
        p_ct.add_run(f"• {name}\n").font.bold = True
        r_rol = p_ct.add_run(f"   Rol: {role}\n")
        r_rol.font.italic = True
        r_rol.font.color.rgb = RGBColor(14, 116, 144)

    # Pie de Portada
    doc.add_paragraph().paragraph_format.space_after = Pt(24)
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ft = p_foot.add_run("Salamanca, Guanajuato, México — Universidad Tecnológica de Salamanca")
    r_ft.font.size = Pt(9.5)
    r_ft.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # ==============================================================
    # HELPERS DE CONTENIDO
    # ==============================================================
    def add_sec_heading(num_str, title_str):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        r = h.add_run(f"{num_str}. {title_str}")
        r.font.name = "Arial"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 76, 129)

    def add_sub_heading(title_str):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(3)
        r = h.add_run(f"> {title_str}")
        r.font.name = "Arial"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(14, 116, 144)

    def add_p(text_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text_str)
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(51, 65, 85)

    def add_bullet(label_str, desc_str):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r_l = p.add_run(f"{label_str}: ")
        r_l.font.name = "Arial"
        r_l.font.size = Pt(9.5)
        r_l.font.bold = True
        r_l.font.color.rgb = RGBColor(15, 76, 129)

        r_d = p.add_run(desc_str)
        r_d.font.name = "Arial"
        r_d.font.size = Pt(9.5)
        r_d.font.color.rgb = RGBColor(51, 65, 85)

    # ==============================================================
    # 2. INTRODUCCIÓN
    # ==============================================================
    add_sec_heading("2", "INTRODUCCIÓN")
    add_p("El desarrollo de software móvil profesional exige un riguroso balance entre velocidad de entrega, estabilidad técnica y satisfacción de necesidades humanas reales. Iniciar la codificación de una aplicación sin una fase previa de análisis, alcance y planeación representa uno de los factores primordiales de fracaso en la ingeniería de software.")
    
    add_sub_heading("2.1 ¿Por qué es importante planificar un proyecto antes de programar?")
    add_p("Planificar permite dimensionar las restricciones del sistema antes de escribir código: consumo de batería derivado del uso continuo del sensor GPS, permisos del sistema operativo (cámara y notificaciones push), conectividad variable en calle y diseño de esquemas de datos eficientes.")
    add_p("Una adecuada planificación previene la acumulación de deuda técnica, minimiza los retrabajos que consumen semanas de esfuerzo, evita desacuerdos internos en el equipo y asegura que la arquitectura adoptada soporte el crecimiento proyectado del sistema.")

    add_sub_heading("2.2 ¿Cómo ayudan las metodologías ágiles a los equipos de desarrollo móvil?")
    add_p("En el ecosistema móvil, caracterizado por pantallas táctiles, constante evolución de SO y alta demanda de inmediatez por parte del usuario, las metodologías ágiles aportan ventajas decisivas:")
    add_bullet("Entregas frecuentes e incrementales (Sprints)", "Permiten obtener builds ejecutables (APKs) cada 2 semanas, facilitando que usuarios y la docente interactúen con el producto desde etapas tempranas.")
    add_bullet("Adaptabilidad inmediata ante el cambio", "Si la API de mapas, la cámara o una regla en la nube presenta retos, el equipo ajusta el backlog en la siguiente iteración sin comprometer la entrega final.")
    add_bullet("Transparencia y autoorganización", "La sincronización continua en tableros y dailies visibiliza bloqueos y enfoca el esfuerzo en las tareas de mayor valor.")

    # ==============================================================
    # 3. DESCRIPCIÓN DEL PROYECTO MÓVIL
    # ==============================================================
    add_sec_heading("3", "DESCRIPCIÓN DEL PROYECTO MÓVIL")
    add_bullet("Nombre Tentativo de la Aplicación", "SaveBite (CeroMerma) — Excedentes de Alimentos Locales a Precio Reducido.")
    
    add_sub_heading("3.1 Breve descripción de su propósito")
    add_p("Diariamente, cientos de establecimientos gastronómicos en zonas urbanas y universitarias descartan alimentos frescos en óptimas condiciones por no haberse vendido durante el horario comercial regular. Al mismo tiempo, miles de estudiantes universitarios y familias enfrentan restricciones económicas severas para adquirir alimentos preparados de calidad.")
    add_p("SaveBite resuelve ambos problemas simultáneamente: permite a los comercios publicar a media tarde sus excedentes en forma de 'Paquetes Sorpresa' a precios accesibles, mientras que los usuarios exploran las ofertas en un mapa interactivo con GPS, reservan en la app y recogen su paquete en mostrador antes del cierre escaneando un código QR. El proyecto impacta positivamente en los Objetivos de Desarrollo Sostenible (ODS de la ONU), en particular el ODS 12 (Producción y Consumo Responsables) y ODS 2 (Hambre Cero).")

    add_sub_heading("3.2 Público objetivo (Segmentos de usuario)")
    add_bullet("Estudiantes Universitarios y Jóvenes (Consumidores)", "Alumnos de la UTS y jóvenes con presupuesto limitado que buscan comida nutritiva y variada a costos accesibles (ahorro del 50% al 70%).")
    add_bullet("Comercios Gastronómicos Locales (Aliados)", "Panaderías, cafeterías, pastelerías, fruterías y pizzerías que desean recuperar costos operativos de producción, evitar el desperdicio de merma y atraer nuevos clientes a su establecimiento.")
    add_bullet("Consumidores Eco-Conscientes y Comunidad", "Ciudadanos interesados en hábitos sostenibles, reducción del impacto ambiental urbano y mitigación del desperdicio de comida.")

    add_sub_heading("3.3 Funcionalidades Principales (Características Fijas + Propuesta Adicional)")
    add_bullet("1. Geolocalización y Mapa Interactivo con GPS (Core Fijo 1)", "Exploración en vivo de comercios locales cercanos que disponen de paquetes sorpresa activos, visualizados mediante marcadores dinámicos en un mapa interactivo con cálculo de distancias y rutas de recolección a pie o en auto.")
    add_bullet("2. Catálogo de Paquetes Sorpresa y Reserva In-App (Core Fijo 2)", "Ficha detallada por establecimiento con precio original vs. precio reducido (50% al 70% de descuento), descripción del tipo de comida (dulce, salada, vegetariana), ventana horaria estricta de recogida y reserva instantánea con 1 toque.")
    add_bullet("3. Validación de Canje por Escaneo de Código QR con Cámara (Core Fijo 3)", "Cierre seguro de la transacción en mostrador: la app genera un ticket digital con código QR dinámico en el teléfono del comprador, el cual es escaneado por la cámara del comerciante para validar el canje en menos de 2 segundos.")
    add_bullet("4. Sistema de Alertas y Notificaciones Push en Tiempo Real (Core Fijo 4)", "Avisos automáticos al celular mediante Firebase Cloud Messaging (FCM) cuando los comercios favoritos del usuario publican nuevos paquetes disponibles o recordatorios preventivos cuando restan 30 minutos de la ventana de recogida.")
    add_bullet("5. Modo Offline-First con Caché Local (Core Fijo 5)", "Persistencia local de vouchers de reserva y datos del comercio con SQLite / Hive, permitiendo al usuario presentar su código QR de canje en mostrador aun si pierde conexión a datos móviles en la vía pública.")
    add_bullet("★ Propuesta Adicional: Calculadora de Impacto ODS (CO2 y Ahorro)", "Módulo interactivo en el perfil del usuario que contabiliza en tiempo real los kilogramos de comida rescatados del vertedero, el dinero ahorrado acumulado y la reducción estimada en kilogramos de emisiones de gases de efecto invernadero (CO2 equivalente), con insignias gamificadas que premian la constancia ecológica.")

    # ==============================================================
    # 4. METODOLOGÍA ÁGIL SELECCIONADA
    # ==============================================================
    add_sec_heading("4", "METODOLOGÍA ÁGIL SELECCIONADA")
    add_bullet("Metodología Elegida", "SCRUM (con Gestión de Flujo Scrumban).")
    
    add_sub_heading("4.1 Justificación de su elección para este proyecto móvil")
    add_bullet("Adaptación al calendario académico", "Los Sprints de 2 semanas sincronizan de manera natural los entregables funcionales (APKs) con las fechas de evaluación de parciales solicitadas por la docente.")
    add_bullet("Mitigación de riesgos de hardware móvil", "SaveBite integra múltiples sensores físicos (GPS, sensor de cámara para escaneo QR y notificaciones push en segundo plano); Scrum permite probar cada componente de hardware en prototipos tempranos.")
    add_bullet("Claridad en roles para 4 desarrolladores", "Permite estructurar las tareas técnicas en historias de usuario bien delimitadas (Frontend Flutter, Backend Firebase, Calidad y Requerimientos), evitando duplicidad de esfuerzos.")

    add_sub_heading("4.2 Explicación de funcionamiento y organización del equipo")
    add_p("El proyecto se organiza bajo los eventos, artefactos y tableros formales de Scrum:")
    add_bullet("Sprint Planning (Planificación)", "Reunión quincenal de 1 hora para seleccionar historias del Product Backlog y fijar el objetivo del Sprint.")
    add_bullet("Daily Standup (Sincronización Diaria)", "Reunión de 10 minutos (vía Discord / presencial en campus): ¿Qué avancé ayer? ¿Qué haré hoy? ¿Qué bloqueos tengo?")
    add_bullet("Sprint Review y Retrospectiva", "Presentación del APK funcional a la docente Ericka Nohemí Álvarez Valencia para validación técnica y sesión de mejora continua.")
    add_bullet("Tablero Digital (Trello / GitHub Projects)", "Flujo visual en 5 columnas con límites WIP: Product Backlog -> To Do -> In Progress -> Code Review / QA -> Done.")
    add_bullet("Estrategia GitFlow", "Control de versiones en GitHub protegiendo la rama main y utilizando develop y feature branches con Pull Requests obligatorios.")

    add_sub_heading("4.3 Plan de Trabajo por Sprints (Cronograma del Proyecto)")
    
    # Tabla de Sprints en Word
    sprints_data = [
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

    sp_table = doc.add_table(rows=len(sprints_data) + 1, cols=3)
    sp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sp_headers = ["Sprint", "Objetivo del Sprint (Sprint Goal)", "Entregable Funcional (Incremento)"]
    
    hdr_cells = sp_table.rows[0].cells
    for i, title in enumerate(sp_headers):
        hdr_cells[i].text = title
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(hdr_cells[i], "0F4C81")
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)

    for row_idx, (sp, goal, inc) in enumerate(sprints_data, start=1):
        row_cells = sp_table.rows[row_idx].cells
        row_cells[0].text = sp
        row_cells[1].text = goal
        row_cells[2].text = inc
        for c in row_cells:
            c.paragraphs[0].runs[0].font.size = Pt(8.5)
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(51, 65, 85)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            if row_idx % 2 == 0:
                set_cell_background(c, "F8FAFC")

    # ==============================================================
    # 5. ROLES DENTRO DEL EQUIPO
    # ==============================================================
    add_sec_heading("5", "ROLES DENTRO DEL EQUIPO")
    add_p("Conforme a las mejores prácticas de la metodología Scrum, la asignación de responsabilidades para los cuatro estudiantes de IDGS se estructuró de la siguiente manera:")

    roles_data = [
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

    r_table = doc.add_table(rows=len(roles_data) + 1, cols=3)
    r_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_headers = ["Integrante (IDGS)", "Rol Ágil Asignado", "Responsabilidades Principales"]
    
    r_hdr_cells = r_table.rows[0].cells
    for i, title in enumerate(r_headers):
        r_hdr_cells[i].text = title
        r_hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        r_hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(r_hdr_cells[i], "0F4C81")
        set_cell_margins(r_hdr_cells[i], top=80, bottom=80, left=100, right=100)

    for row_idx, (mem, role, resp) in enumerate(roles_data, start=1):
        row_cells = r_table.rows[row_idx].cells
        row_cells[0].text = mem
        row_cells[1].text = role
        row_cells[2].text = resp
        for c in row_cells:
            c.paragraphs[0].runs[0].font.size = Pt(8.5)
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(51, 65, 85)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            if row_idx % 2 == 0:
                set_cell_background(c, "F8FAFC")

    # ==============================================================
    # 6. JUSTIFICACIÓN DE LA ARQUITECTURA PROPUESTA
    # ==============================================================
    add_sec_heading("6", "JUSTIFICACIÓN DE LA ARQUITECTURA PROPUESTA")
    add_bullet("Arquitectura Seleccionada", "Clean Architecture (Arquitectura Limpia) + MVVM / BLoC + Cloud BaaS (Firebase).")
    
    add_sub_heading("6.1 ¿Por qué es la arquitectura más adecuada para SaveBite?")
    add_bullet("Separación estricta de responsabilidades", "La Capa de Presentación (vistas Flutter y widgets de mapa) se encuentra totalmente desacoplada de la base de datos y de la lógica de negocio, permitiendo modificar la UI sin alterar reglas de reserva.")
    add_bullet("Alta testabilidad en la Capa de Dominio", "Los Casos de Uso (ej. ExplorarCercanosUseCase, ReservarPaqueteUseCase) son clases de Dart puro libres de dependencias de Flutter o Firebase, ejecutables en pruebas unitarias automáticas sin emuladores.")
    add_bullet("Estrategia Offline-First con Repository Pattern", "Si el usuario tiene señal débil en la calle al llegar al comercio, el repositorio recupera el voucher de la memoria local (Hive) y permite canjearlo con el código QR sin interrupción.")
    add_bullet("Aceleración del desarrollo mediante BaaS", "El uso de Firebase (Firestore + Auth + Cloud Functions) suprime la necesidad de programar servidores dedicados, acelerando el desarrollo hacia el MVP.")

    # ==============================================================
    # 7. DIAGRAMAS VISUALES
    # ==============================================================
    add_sec_heading("7", "DIAGRAMA DE LA ARQUITECTURA Y FLUJO DE PANTALLAS")
    add_sub_heading("7.1 Diagrama de Navegación y Flujo de Pantallas (Screen Flow)")
    add_p("El siguiente diagrama visual ilustra la jerarquía de pantallas de SaveBite, la autenticación centralizada y la derivación de vistas según el perfil del usuario (Consumidor vs. Comercio Aliado):")

    if os.path.exists("diagram_flujo_pantallas_savebite.png"):
        doc.add_picture("diagram_flujo_pantallas_savebite.png", width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run("Figura 1: Mapa de Navegación y Flujo de Pantallas de SaveBite.")
        r_c.font.size = Pt(8.5)
        r_c.font.italic = True
        r_c.font.color.rgb = RGBColor(100, 116, 139)

    add_sub_heading("Descripción de Transiciones y Navegación entre Pantallas:")
    add_bullet("Transición de Splash (1) a Login (2)", "Verificación automática de token de sesión. Si no existe sesión activa, conduce al acceso con selección de perfil.")
    add_bullet("Derivación por Rol (2 a 3A / 3B)", "Redirección automática al Mapa GPS y Feed de Ofertas (3A) para consumidores o al Panel del Establecimiento (3B) para comercios aliados.")
    add_bullet("Flujo de Reserva del Consumidor (3A -> 4A -> 5A -> 6A)", "El usuario visualiza un comercio, entra a la Ficha del Paquete (4A), realiza la reserva (5A) y la app genera su Voucher Digital con QR Dinámico (6A).")
    add_bullet("Validación de Canje en Mostrador (6A -> 5B -> 6B)", "El consumidor muestra el QR en tienda; el comerciante abre el lector de cámara (5B) y valida el canje en 2 segundos, liberando la entrega (6B) y sumando al impacto ODS (7A).")

    add_sub_heading("7.2 Diagrama de Arquitectura de Software en Capas (Clean Architecture)")
    add_p("Estructura técnica de capas concéntricas que rige la construcción de SaveBite, garantizando el flujo unidireccional de datos, soporte para geolocalización y persistencia local resiliente:")

    if os.path.exists("diagram_arquitectura_capas_savebite.png"):
        doc.add_picture("diagram_arquitectura_capas_savebite.png", width=Inches(6.2))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c2 = p_cap2.add_run("Figura 2: Arquitectura de Software en Capas de SaveBite.")
        r_c2.font.size = Pt(8.5)
        r_c2.font.italic = True
        r_c2.font.color.rgb = RGBColor(100, 116, 139)

    add_sub_heading("Componentes de la Arquitectura en Capas:")
    add_bullet("1. Capa de Presentación (Frontend Flutter)", "Contiene las pantallas, controladores BLoC, mapa interactivo (Google Maps SDK), visor de escaneo de cámara (Mobile Scanner) y componentes Material Design 3.")
    add_bullet("2. Capa de Dominio (Casos de Uso Puros)", "Contiene la lógica de negocio central (ExplorarCercanos, ReservarPaquete, ValidarEntregaQR, CalcularImpactoODS) y las entidades del modelo de datos.")
    add_bullet("3. Capa de Datos (Repository Pattern)", "Intermediario inteligente que arbitra entre el Local DataSource (Caché Hive/SQLite) y el Remote DataSource (Firebase Cloud Firestore con Geohashing, Auth, FCM y Storage).")

    # ==============================================================
    # 8. CONCLUSIÓN
    # ==============================================================
    add_sec_heading("8", "CONCLUSIÓN DE LA FASE 1")
    add_p("La culminación del Plan del Proceso de Desarrollo Móvil (Fase 1) para SaveBite establece una propuesta sólida, técnica y socialmente relevante. Al alinearse con los Objetivos de Desarrollo Sostenible (ODS 12) y apoyarse en una arquitectura Clean Architecture resiliente y el marco ágil Scrum, el equipo (Alvaro, Guillermo, Juan Pablo y Diego) se encuentra perfectamente preparado para iniciar con éxito el Sprint 1 de implementación móvil.")

    doc.save(output_path)
    print(f"Documento Word (.docx) generado con éxito en: {output_path}")

if __name__ == "__main__":
    out_docx = "c:\\Users\\galan\\OneDrive - Universidad Tecnológica de Salamanca\\Aplicación\\Fase1_Plan_Desarrollo_Movil_SaveBite.docx"
    create_savebite_docx(out_docx)
