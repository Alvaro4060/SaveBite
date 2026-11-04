import os
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from fpdf.fonts import FontFace

class SaveBitePhase2PDF(FPDF):
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
            self.cell(74, 5, "Fase 2: Arquitectura, Planificación y Seguridad | SaveBite", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

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
    pdf = SaveBitePhase2PDF()

    # Helpers de Renderizado
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
        pdf.set_font("ArialUni", "B", 10.5)
        pdf.set_text_color(15, 76, 129)
        pdf.cell(165, 6.5, title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_draw_color(203, 213, 225)
        pdf.set_line_width(0.5)
        pdf.line(18, pdf.get_y() + 1, 192, pdf.get_y() + 1)
        pdf.ln(2.2)

    def render_sub_heading(title):
        pdf.set_font("ArialUni", "B", 8.8)
        pdf.set_text_color(14, 116, 144)
        pdf.cell(174, 4.6, f"> {title}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.8)

    def render_p(text, spacing=1.4):
        pdf.set_font("ArialUni", "", 8.1)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(174, 3.9, text)
        pdf.ln(spacing)

    def render_bullet(title, desc, spacing=1.0):
        pdf.set_x(20)
        pdf.set_font("ArialUni", "B", 8.0)
        pdf.set_text_color(15, 76, 129)
        prefix = f"- {title}: "
        pdf.write(3.9, prefix)
        
        pdf.set_font("ArialUni", "", 8.0)
        pdf.set_text_color(51, 65, 85)
        pdf.write(3.9, desc + "\n")
        pdf.ln(spacing)

    def render_info_box(title, text, color="blue", h_fixed=None):
        y = pdf.get_y()
        bg_c = (240, 249, 255) if color == "blue" else (255, 251, 235)
        border_c = (14, 116, 144) if color == "blue" else (245, 158, 11)
        
        pdf.set_font("ArialUni", "", 8.0)
        lines = len(pdf.multi_cell(164, 3.7, f"{title}\n{text}", dry_run=True, output="LINES"))
        box_h = h_fixed if h_fixed else max(12, (lines * 3.7) + 5)

        pdf.set_fill_color(*bg_c)
        pdf.set_draw_color(226, 232, 240)
        pdf.rect(18, y, 174, box_h, "FD")
        pdf.set_fill_color(*border_c)
        pdf.rect(18, y, 3, box_h, "F")

        pdf.set_xy(23, y + 2)
        pdf.set_font("ArialUni", "B", 8.4)
        pdf.set_text_color(*border_c)
        pdf.cell(164, 3.8, title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_x(23)
        pdf.set_font("ArialUni", "", 7.9)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(164, 3.7, text)
        pdf.set_y(y + box_h + 2)

    # ==============================================================
    # PÁGINA 1: PORTADA OFICIAL UTS
    # ==============================================================
    pdf.add_page()

    # Fondo superior azul marino tecnológico UTS
    pdf.set_fill_color(10, 46, 80)
    pdf.rect(0, 0, 210, 108, "F")

    # Franja turquesa brillante institucional
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
    pdf.set_font("ArialUni", "B", 9.2)
    
    badge_text = " FASE 2: ARQUITECTURA, PLANIFICACIÓN Y SEGURIDAD DEL DESARROLLO MÓVIL "
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
    pdf.cell(180, 5.5, "Plataforma Colaborativa de Rescate de Alimentos Locales a Precio Reducido (ODS 12: Cero Merma)", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # TARJETAS DE PORTADA
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
    pdf.cell(44, 4.5, "04 de Noviembre de 2026", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    draw_meta_field("Entregable:", "Documento Digital Fase 2", meta_y + 51)

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
    # PÁGINA 2: INTRODUCCIÓN Y PATRONES DE DISEÑO
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_section_title("1", "INTRODUCCIÓN A LA FASE 2: ARQUITECTURA, PLANIFICACIÓN Y SEGURIDAD")
    render_p("Habiendo fundamentado el alcance, la metodología ágil Scrum y los requerimientos funcionales en la Fase 1 para la plataforma SaveBite, la presente Fase 2 tiene como objetivo formalizar el diseño arquitectónico profundo, la justificación técnica de frameworks, los esquemas de versionamiento profesional, el blindaje de seguridad móvil y el ecosistema de servicios integrados en la nube.")

    render_sub_heading("1.1 Propósito Técnico y Estratégico de la Fase 2")
    render_p("El desarrollo móvil contemporáneo demanda una ingeniería defensiva que responda con solvencia a las restricciones severas del hardware móvil: fluctuación de red en calle, consumo estricto de batería al operar el sensor GPS, latencia en la decodificación de códigos QR con la cámara y estrictas regulaciones sobre la privacidad de la geolocalización del usuario.")
    render_p("Mediante esta planeación integral se asegura que SaveBite no dependa de implementaciones acopladas o código improvisado, garantizando que cada módulo desarrollado por el equipo (UI en Flutter, BaaS en la nube, sincronización offline y escaneo de vouchers) converja bajo estándares de la industria como Clean Architecture, OWASP Mobile Top 10 y la legislación mexicana LFPDPPP.")

    render_section_title("2", "PROPUESTA Y JUSTIFICACIÓN DE PATRONES DE DISEÑO")
    render_info_box("Patrones de Diseño Seleccionados para SaveBite",
                    "Para responder a los desafíos de persistencia híbrida, reactividad en tiempo real y alta testabilidad, se seleccionaron formalmente cuatro patrones de diseño complementarios: Repository Pattern, BLoC Pattern (Observer), Service Locator (Singleton) y Data Transfer Object (DTO) con Factory Method.", "blue")

    render_sub_heading("2.1 Patrón Repositorio (Repository Pattern) - Fuente Única de Verdad")
    render_bullet("Uso en SaveBite", "Actúa como un intermediario y árbitro inteligente entre la capa de Dominio (Casos de Uso) y las múltiples fuentes de datos (Remote DataSource vía Supabase/Firebase y Local DataSource vía Hive/SQLite). Centraliza la lógica de almacenamiento y recuperación de paquetes sorpresa, comercios y vouchers de reserva.")
    render_bullet("Justificación Técnica", "Garantiza el desacoplamiento total de la lógica de negocio respecto a los mecanismos concretos de persistencia. Si el comensal se encuentra en mostrador sin cobertura celular (3G/4G/5G débil), el repositorio entrega el voucher de reserva desde la caché local sin disparar excepciones ni bloquear la UI, permitiendo un canje 100% resiliente (Offline-First).")

    render_sub_heading("2.2 Patrón BLoC (Business Logic Component) / Observer Pattern")
    render_bullet("Uso en SaveBite", "Rige la gestión reactiva de estado en la Capa de Presentación bajo el paradigma de Flujo Unidireccional de Datos (UDF). La interfaz emite eventos discretos (ej. SolicitarReservaEvent, ActualizarFiltroDistanciaEvent), el BLoC procesa la lógica invocando el Caso de Uso y emite nuevos estados inmutables (ReservaCargando, ReservaExitosa, ErrorState) escuchados por la UI mediante Streams de Dart.")
    render_bullet("Justificación Técnica", "Elimina de raíz el desorden derivado de llamadas dispersas a setState(), reduciendo el consumo de batería y CPU al evitar repintados innecesarios en el árbol de widgets. Facilita la elaboración de pruebas unitarias automatizadas con la suite bloc_test sin requerir emuladores ni mocks complejos de interfaz.")

    # ==============================================================
    # PÁGINA 3: PATRONES COMPLEMENTARIOS Y DIAGRAMA DE ARQUITECTURA
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_sub_heading("2.3 Patrón Service Locator / Singleton (Inyección de Dependencias con GetIt)")
    render_bullet("Uso en SaveBite", "Administra de forma centralizada la instanciación perezosa (Lazy Singleton) de servicios críticos globales, tales como el cliente de red SupabaseClient, el motor de almacenamiento seguro FlutterSecureStorage, los controladores de ubicación satelital y el manejador de notificaciones push.")
    render_bullet("Justificación Técnica", "Previene la creación descontrolada de sockets, conexiones HTTP redundantes o relecturas de llaves de cifrado en memoria, disminuyendo el footprint de RAM en el dispositivo móvil y permitiendo inyectar implementaciones ficticias (Mocks) de forma limpia durante las pruebas unitarias de software.")

    render_sub_heading("2.4 Patrón Factory Method y Data Transfer Object (DTO)")
    render_bullet("Uso en SaveBite", "Encapsula la serialización y deserialización segura de payloads JSON procedentes de la nube hacia entidades inmutables del dominio (FoodPackage, Store, Reservation, EcoImpact) a través de constructores nombrados Factory (ej. FoodPackageModel.fromJson(json)).")
    render_bullet("Justificación Técnica", "Otorga tipado fuerte y validación de esquemas en tiempo de compilación. Resguarda a la aplicación contra anomalías de valores nulos imprevistos (Null Safety en Dart 3) y fallos de parseo en caso de que un registro en la base de datos remota contenga tipos inconsistentes o nulos.")

    render_sub_heading("2.5 Diagrama Técnico de Patrones de Diseño y Arquitectura en Capas")
    render_p("La siguiente figura detalla cómo los patrones descritos interactúan de manera concéntrica bajo los principios de Clean Architecture:", spacing=1)

    if os.path.exists("diagram_fase2_patrones_arquitectura.png"):
        img_y = pdf.get_y()
        pdf.image("diagram_fase2_patrones_arquitectura.png", x=18, y=img_y, w=174)
        pdf.set_y(img_y + 115)

    render_info_box("Alineación Arquitectónica con Clean Architecture",
                    "La integración de BLoC en Presentación, Casos de Uso puros en Dominio y Repository en Datos asegura que la aplicación pueda migrar de proveedor de nube o sustituir librerías de UI sin tocar una sola regla de negocio de SaveBite.", "blue")

    # ==============================================================
    # PÁGINA 4: JUSTIFICACIÓN DE FRAMEWORKS Y HERRAMIENTAS
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_section_title("3", "JUSTIFICACIÓN DE FRAMEWORKS Y HERRAMIENTAS A UTILIZAR")
    render_p("La selección tecnológica de SaveBite responde a una rigurosa evaluación de criterios de ingeniería de software móvil, priorizando rendimiento nativo, reducción de tiempos de desarrollo y soporte a largo plazo.")

    render_sub_heading("3.1 Framework Principal de Desarrollo: Flutter SDK (Dart 3.x)")
    render_bullet("Rendimiento Extremo (Compilación AOT)", "Flutter compila directamente a código máquina nativo C/C++ ARM64 mediante Ahead-Of-Time (AOT), eliminando los puentes de JavaScript (presentes en React Native). Gracias a su nuevo motor gráfico Impeller sobre Vulkan/Metal, renderiza animaciones fluidas a 60 y 120 FPS sin caídas de cuadros ni jitter al mover el mapa interactivo.")
    render_bullet("Soporte Multiplataforma Real", "Un único código fuente (Single Codebase) genera binarios nativos para Android (APK/AAB) e iOS (IPA), maximizando la productividad del equipo y garantizando paridad total de interfaz y lógica entre ambos sistemas operativos.")
    render_bullet("Curva de Aprendizaje y Tipado Fuerte", "Dart 3 implementa Sound Null Safety estricto, pattern matching y records, reduciendo errores en tiempo de ejecución en más del 80%. Su sintaxis orientada a objetos es natural para ingenieros en formación con bases en Java/C#.")
    render_bullet("Comunidad y Ecosistema pub.dev", "Respaldado directamente por Google y con millones de paquetes mantenidos por la comunidad, pub.dev ofrece librerías optimizadas para el control de hardware móvil nativo.")

    render_sub_heading("3.2 Ecosistema de Librerías y Herramientas Especializadas")
    h_style = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(15, 76, 129))

    tools_rows = [
        ("Flutter SDK 3.x", "Framework UI Móvil", "Compilación AOT nativa C++, motor Impeller a 60 FPS, Material 3 reactivo."),
        ("Supabase / Firebase BaaS", "Cloud Backend & DB", "Auth JWT, PostgreSQL con PostGIS / Firestore NoSQL, WebSockets en tiempo real."),
        ("mobile_scanner (CameraX)", "Visor y Decodificador QR", "Escaneo ultrarrápido (<300 ms) integrado directo a los drivers de hardware."),
        ("Hive & Secure Storage", "Persistencia Local", "Caché NoSQL binaria ultraligera para modo offline y cifrado AES-256 en KeyStore."),
        ("flutter_lints & DevTools", "Calidad y Profiling", "Análisis estático de código estricto y perfilado de consumo de memoria y CPU.")
    ]

    pdf.set_font("ArialUni", "", 7.6)
    with pdf.table(col_widths=(38, 42, 94), headings_style=h_style, line_height=4.0, text_align=("LEFT", "LEFT", "LEFT")) as table:
        header_row = table.row()
        header_row.cell("Tecnología / Herramienta")
        header_row.cell("Categoría / Función")
        header_row.cell("Argumentación y Ventaja Técnica")

        for tech, cat, arg in tools_rows:
            r = table.row()
            r.cell(tech)
            r.cell(cat)
            r.cell(arg)

    pdf.ln(3)
    render_section_title("4", "ESTRATEGIAS DE VERSIONAMIENTO")
    render_p("Para salvaguardar la integridad del código fuente, habilitar la integración continua entre los 4 desarrolladores y prevenir regresiones en las entregas quincenales, se definió una estrategia de versionamiento profesional basada en GitFlow, Semantic Versioning y CI/CD.")

    render_sub_heading("4.1 Estructura del Flujo de Ramas (GitFlow Adaptado)")
    render_bullet("main (Producción)", "Rama protegida contra escritura directa. Solo alberga releases estables, etiquetadas y validadas con firmas criptográficas de producción. Requiere Pull Request obligatorio con 2 aprobaciones.")
    render_bullet("develop (Integración)", "Rama principal de trabajo continuo. Centraliza las funcionalidades validadas en cada Sprint. Es la base para pruebas de control de calidad (QA).")
    render_bullet("feature/<nombre>", "Ramas de corta duración nacidas de develop para cada historia de usuario (ej. feature/modulo-mapa-gps, feature/lector-qr-camerax). Se eliminan tras merge.")
    render_bullet("release/vX.Y.Z", "Ramas de estabilización previas a un hito de entrega. Se congelan cambios mayores y solo se admiten parches de pulido de UI y documentación.")
    render_bullet("hotfix/<incidencia>", "Ramas de emergencia que se originan directamente de main para mitigar vulnerabilidades o errores críticos en producción, integrándose a main y develop.")

    # ==============================================================
    # PÁGINA 5: SEMVER, COMMITS Y DIAGRAMA GITFLOW
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_sub_heading("4.2 Versionado Semántico (SemVer 2.0.0 + Build Numbers)")
    render_p("Se adopta la nomenclatura formal MAJOR.MINOR.PATCH+BUILD (ejemplo: v1.0.0+1):")
    render_bullet("MAJOR (1.x.x)", "Incrementa ante rupturas de compatibilidad con la API o cambios estructurales en la arquitectura de base de datos.")
    render_bullet("MINOR (x.1.x)", "Incrementa al incorporar nuevas funcionalidades compatibles hacia atrás (ej. APK v0.2.0 al sumar el módulo de publicación de paquetes).")
    render_bullet("PATCH (x.x.1)", "Incrementa ante correcciones de errores, bugs menores de interfaz o ajustes de rendimiento sin alterar los contratos existentes.")
    render_bullet("BUILD NUMBER (+X)", "Entero secuencial autoincrementable requerido por Android (versionCode) y Play Store para identificar cada compilación física de APK.")

    render_sub_heading("4.3 Convención de Commits Semánticos (Conventional Commits)")
    render_p("Los mensajes de confirmación siguen el estándar obligatorio: tipo(alcance): descripción breve en imperativo:")
    render_bullet("feat(scanner)", "Implementación de decodificador de códigos QR con Mobile Scanner en cámara.")
    render_bullet("fix(auth)", "Resolución de fallo de expiración en refresh tokens JWT de Supabase Auth.")
    render_bullet("perf(map)", "Optimización de marcadores de comercios mediante clustering geoespacial en Haversine.")
    render_bullet("security(voucher)", "Incorporación de firma criptográfica HMAC-SHA256 en payload de códigos QR.")

    render_sub_heading("4.4 Diagrama del Flujo de Trabajo GitFlow y Pipeline CI/CD")
    render_p("Visualización de la convergencia de ramas y la automatización de calidad con GitHub Actions:", spacing=1)

    if os.path.exists("diagram_fase2_versionamiento_gitflow.png"):
        img_y_gf = pdf.get_y()
        pdf.image("diagram_fase2_versionamiento_gitflow.png", x=18, y=img_y_gf, w=174)
        pdf.set_y(img_y_gf + 112)

    render_info_box("Políticas de Branch Protection y CI/CD Automatizado",
                    "Toda Pull Request hacia develop o main ejecuta automáticamente el pipeline de GitHub Actions: 1) flutter analyze --fatal-infos, 2) ejecución de unit tests con cobertura mayor al 80%, y 3) compilación de release APK. Si alguna prueba falla, el merge se bloquea automáticamente.", "blue")

    # ==============================================================
    # PÁGINA 6: SEGURIDAD, PRIVACIDAD Y CUMPLIMIENTO LEGAL (LFPDPPP)
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_section_title("5", "SEGURIDAD, PRIVACIDAD Y CUMPLIMIENTO LEGAL")
    render_p("La confianza de los estudiantes y de los comercios gastronómicos locales es el pilar de SaveBite. La aplicación implementa una estrategia de seguridad por diseño (Security by Design), alineada rigurosamente con el marco jurídico mexicano y con los estándares internacionales de seguridad móvil.")

    render_sub_heading("5.1 Cumplimiento de la Normativa Local Vigente en México (LFPDPPP)")
    render_p("SaveBite opera bajo la jurisdicción de la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP) y las directrices del Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales (INAI), rigiéndose por los siguientes principios rectores:")
    render_bullet("Principio de Licitud", "El tratamiento de los datos personales de estudiantes y dueños de negocios se apega estrictamente a las leyes mexicanas y al orden público.")
    render_bullet("Principio de Consentimiento", "Se recaba el consentimiento expreso y verificable del usuario mediante un opt-in activo durante el registro previo a recopilar cualquier información personal o activar permisos de hardware.")
    render_bullet("Principio de Información (Avisos de Privacidad)", "SaveBite despliega dos modalidades: 1) Aviso de Privacidad Simplificado al solicitar acceso al GPS y cámara, y 2) Aviso de Privacidad Integral accesible permanentemente desde los ajustes de la app y portal web.")
    render_bullet("Principio de Finalidad y Lealtad", "La información recolectada (nombre, correo institucional, geolocalización efímera y registros de compra) se utiliza exclusivamente para la reserva, canje de alimentos y cálculo de métricas ODS. Queda terminantemente prohibida su comercialización o perfilamiento publicitario a terceros.")
    render_bullet("Principio de Proporcionalidad (Minimización)", "Únicamente se solicitan los datos indispensables para ejecutar la transacción. No se solicitan contactos de la agenda, acceso a fotos privadas, identificadores publicitarios ni SMS.")
    render_bullet("Ejercicio de Derechos ARCO", "La aplicación provee una sección directa en el perfil del usuario para ejercer sus derechos de Acceso, Rectificación, Cancelación y Oposición de sus datos, así como la eliminación inmediata de su cuenta.")

    render_sub_heading("5.2 Principios de Codificación Segura Móvil (OWASP Mobile Top 10 & MASVS)")
    render_bullet("M1 - Almacenamiento Seguro (Insecure Data Storage)", "Las llaves de sesión, tokens JWT y credenciales se guardan exclusivamente en el hardware criptográfico nativo: Android KeyStore (AES-256-GCM) y iOS Keychain mediante la librería flutter_secure_storage. Queda vetado almacenar datos sensibles en SharedPreferences o logs de consola.")
    render_bullet("M2 - Criptografía Robusta en Vouchers QR (Broken Cryptography)", "Para impedir la falsificación de vouchers de comida, el código QR no viaja en texto plano; contiene un token firmado con HMAC-SHA256 que incluye el identificador de reserva, un Nonce aleatorio de un solo uso y un Timestamp de caducidad (ventana de recogida de 60 min).")
    render_bullet("M3 - Comunicaciones Cifradas en Tránsito (Insecure Communication)", "Todas las conexiones hacia el BaaS y APIs externas exigen TLS 1.3 / HTTPS forzado. En AndroidManifest.xml se declara android:usesCleartextTraffic='false' para neutralizar cualquier vector de ataque por intermediación (Man-in-the-Middle - MitM).")
    render_bullet("M4 - Autenticación y Autorización Robusta (Insecure Authentication)", "Tokens JWT efímeros firmados por el servidor con expiración de 1 hora y refresh tokens rotativos. Control de acceso granular basado en roles (RBAC): un usuario común jamás puede invocar endpoints o consultar pedidos de otros comercios.")
    render_bullet("M5 - Validación Estricta de Entradas (Input Validation)", "Sanitización exhaustiva tanto en cliente Flutter como en el servidor en la nube para campos de texto, precios y coordenadas, bloqueando inyecciones SQL, NoSQL y ataques XSS.")
    render_bullet("M6 - Protección de Binarios y Ofuscación (Reverse Engineering)", "El código Dart se compila a binario nativo AOT. Para el código nativo de Android se activa ProGuard / R8 con optimización de recursos y ofuscación de nombres de clases y métodos, dificultando el análisis estático y descompilado.")

    # ==============================================================
    # PÁGINA 7: CHECKLIST EXHAUSTIVO DE SEGURIDAD MÓVIL
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_sub_heading("5.3 Checklist de Seguridad para Entornos Móviles (SaveBite Security Checklist)")
    render_p("Matriz de verificación técnica aplicada durante los Sprints de desarrollo, alineada con OWASP MASVS y la legislación vigente:")

    sec_rows = [
        ("Autenticación", "Almacenamiento seguro de tokens JWT sin exposición en logs ni caché.", "Implementado", "FlutterSecureStorage / KeyStore", "Diego Villegas"),
        ("Autenticación", "Sesiones efímeras con refresh tokens rotativos y revocación remota.", "Implementado", "Supabase Auth / RLS", "Diego Villegas"),
        ("Comunicaciones", "Tráfico cifrado mandatorio TLS 1.3 en todas las peticiones de red.", "Implementado", "HTTPS / android:usesCleartextTraffic", "Diego Villegas"),
        ("Comunicaciones", "Bloqueo de certificados autofirmados e inspección de proxys MitM.", "En Proceso", "Network Security Config (Android)", "Guillermo Berlín"),
        ("Criptografía", "Vouchers QR firmados con token HMAC-SHA256 y timestamp de expiración.", "Implementado", "Crypto Dart / CameraX Scanner", "Juan Pablo Vega"),
        ("Criptografía", "Caché de vouchers offline cifrada en base de datos local NoSQL.", "Implementado", "Hive Encrypted Box (AES-256)", "Diego Villegas"),
        ("Almacenamiento", "Prohibición de volcado de datos sensibles en SQLite o SharedPrefs.", "Implementado", "Code Review / Static Lints", "Guillermo Berlín"),
        ("Privacidad", "Aviso de Privacidad Integral y Simplificado conforme a LFPDPPP.", "Implementado", "Pantalla Legal / Dialog Consent", "Alvaro Chávez"),
        ("Privacidad", "Acceso a GPS solo durante el uso activo de la app (Foreground Only).", "Implementado", "geolocator (ACCESS_FINE_LOCATION)", "Juan Pablo Vega"),
        ("Privacidad", "Mecanismo interactivo para ejercicio de Derechos ARCO y borrado de cuenta.", "Implementado", "Endpoint Serverless / Ajustes Perfil", "Alvaro Chávez"),
        ("Plataforma", "Ofuscación de código fuente y eliminación de símbolos en el APK Release.", "Implementado", "ProGuard / R8 / Dart Obfuscation", "Guillermo Berlín"),
        ("Plataforma", "Validación estricta de formato y rango en formularios de publicación.", "Implementado", "Form Validators & RegExp en Dart", "Juan Pablo Vega"),
        ("Resiliencia", "Timeouts de red configurados y manejo elegante de pérdida de señal.", "Implementado", "BLoC Exception Handlers", "Juan Pablo Vega")
    ]

    pdf.set_font("ArialUni", "", 7.2)
    with pdf.table(col_widths=(24, 60, 22, 42, 26), headings_style=h_style, line_height=3.8, text_align=("CENTER", "LEFT", "CENTER", "LEFT", "CENTER")) as table:
        header_row = table.row()
        header_row.cell("Categoría")
        header_row.cell("Control Técnico / Criterio")
        header_row.cell("Estado")
        header_row.cell("Mecanismo / Herramienta")
        header_row.cell("Responsable")

        for cat, crit, st, mech, resp in sec_rows:
            r = table.row()
            r.cell(cat)
            r.cell(crit)
            r.cell(st)
            r.cell(mech)
            r.cell(resp)

    pdf.ln(3)
    render_info_box("Compromiso de Calidad y Cero Brechas",
                    "El checklist es auditado por el Scrum Master (Guillermo Berlín) al cierre de cada Sprint como requisito obligatorio para otorgar la 'Definition of Done' a las historias de usuario de SaveBite.", "blue")

    # ==============================================================
    # PÁGINA 8: ECOSISTEMA DE SERVICIOS E INTEGRACIÓN CLOUD
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_section_title("6", "ECOSISTEMA DE SERVICIOS E INTEGRACIÓN")
    render_p("SaveBite combina de forma sinérgica APIs de terceros de clase mundial con una infraestructura en la nube elástica (Cloud BaaS) para brindar una experiencia inmediata tanto al comensal universitario como al dueño del establecimiento comercial.")

    render_sub_heading("6.1 Consumo de APIs de Terceros")
    render_bullet("Google Maps Platform & Places API", "Provee mapas vectoriales fluidos para Android e iOS. Se utiliza el servicio de geocodificación inversa y cálculo de distancias geodésicas mediante la fórmula de Haversine para listar en tiempo real los comercios con paquetes activos a menos de 3 km del estudiante.")
    render_bullet("Pasarela de Pagos Digitales (Stripe / Mercado Pago SDK)", "Permite cobros seguros in-app mediante tarjetas de débito/crédito y transferencias electrónicas SPEI. Cumple la certificación PCI-DSS Nivel 1 mediante tokenización de tarjetas: la app de SaveBite jamás toca ni almacena datos financieros del comprador.")
    render_bullet("Autenticación Federada (Google Sign-In OAuth 2.0)", "Facilita el registro y login en un solo toque mediante cuentas de Google institucionales (@utsalamanca.edu.mx) o personales, disminuyendo la fricción inicial de adopción.")
    render_bullet("Motor de Cámara y Escaneo (Mobile Scanner / Google ML Kit Vision)", "Procesa el stream de video de la cámara física a 60 FPS mediante los subsistemas nativos CameraX (Android) y AVFoundation (iOS) decodificando códigos QR en menos de 300 ms en el mostrador.")

    render_sub_heading("6.2 Arquitectura Cloud y Servicios Críticos en la Nube")
    render_bullet("Supabase Auth / Firebase Auth", "Gestión centralizada de identidades con tokens criptográficos JWT y hashing seguro de contraseñas con algoritmos Argon2 / bcrypt.")
    render_bullet("Base de Datos en Tiempo Real y Espacial (PostgreSQL PostGIS / Cloud Firestore)", "Almacena el catálogo de paquetes y comercios con soporte geoespacial. Mediante suscripciones por WebSockets / Streams, cuando un comercio publica un paquete o un usuario reserva el último disponible, el marcador del mapa se actualiza instantáneamente en los teléfonos de todos los usuarios.")
    render_bullet("Almacenamiento de Archivos (Cloud Storage)", "Buckets seguros compatibles con S3 para fotos de locales y comida, optimizadas en WebP con CDN para reducir el consumo de megabytes del plan de datos del estudiante.")
    render_bullet("Notificaciones Push en Tiempo Real (Firebase Cloud Messaging - FCM)", "Envío de alertas automáticas al celular cuando un comercio favorito publica ofertas y recordatorios preventivos cuando restan 30 minutos de la ventana de recogida.")
    render_bullet("Lógica Serverless (Edge Functions)", "Microservicios que liberan automáticamente reservas no reclamadas y consolidan los reportes de kg de comida rescatada y CO2 mitigado.")

    render_sub_heading("6.3 Diagrama del Ecosistema de Servicios e Integración")
    if os.path.exists("diagram_fase2_ecosistema_integracion.png"):
        img_y_eco = pdf.get_y()
        pdf.image("diagram_fase2_ecosistema_integracion.png", x=18, y=img_y_eco, w=174)
        pdf.set_y(img_y_eco + 108)

    # ==============================================================
    # PÁGINA 9: CAPTURAS DEL AVANCE DE LA APP REVISADAS EN CLASE
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_section_title("7", "EVIDENCIAS Y CAPTURAS DEL AVANCE DE LA APP REVISADAS EN CLASE")
    render_p("Durante las sesiones prácticas y revisiones de Sprint en clase con la docente Ericka Nohemí Álvarez Valencia, el equipo presentó avances funcionales de los componentes core de SaveBite. A continuación se presentan las evidencias de las pantallas operativas implementadas en Flutter:")

    # Renderizar matriz de 6 mockups (2 filas de 3 pantallas)
    mockups = [
        ("screen_1_auth.png", "1. Splash & Multi-Rol", "Acceso Alumno / Comercio"),
        ("screen_2_explore_map.png", "2. Mapa GPS & Feed", "Comercios y Ofertas -65%"),
        ("screen_3_package_detail.png", "3. Ficha de Paquete", "Reserva In-App con 1 toque"),
        ("screen_4_voucher_qr.png", "4. Voucher QR Dinámico", "Token HMAC y Modo Offline"),
        ("screen_5_scanner.png", "5. Escáner de Comercio", "Lectura Cámara CameraX"),
        ("screen_6_eco_impact.png", "6. Impacto ODS 12", "Métricas CO2 y Ahorro")
    ]

    # Fila 1 (Pantallas 1, 2, 3)
    y_row1 = pdf.get_y()
    for idx in range(3):
        fn, t_lbl, st_lbl = mockups[idx]
        x_pos = 18 + (idx * 59)
        if os.path.exists(fn):
            pdf.image(fn, x=x_pos, y=y_row1, w=55)
        pdf.set_xy(x_pos, y_row1 + 101)
        pdf.set_font("ArialUni", "B", 7.8)
        pdf.set_text_color(15, 76, 129)
        pdf.cell(55, 3.8, t_lbl, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.set_xy(x_pos, y_row1 + 104.8)
        pdf.set_font("ArialUni", "I", 6.8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(55, 3.5, st_lbl, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # Fila 2 (Pantallas 4, 5, 6)
    y_row2 = y_row1 + 112
    for idx in range(3, 6):
        fn, t_lbl, st_lbl = mockups[idx]
        x_pos = 18 + ((idx - 3) * 59)
        if os.path.exists(fn):
            pdf.image(fn, x=x_pos, y=y_row2, w=55)
        pdf.set_xy(x_pos, y_row2 + 101)
        pdf.set_font("ArialUni", "B", 7.8)
        pdf.set_text_color(15, 76, 129)
        pdf.cell(55, 3.8, t_lbl, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.set_xy(x_pos, y_row2 + 104.8)
        pdf.set_font("ArialUni", "I", 6.8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(55, 3.5, st_lbl, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_y(y_row2 + 112)
    render_info_box("Validación de Interfaz y Fluidez en Hardware Real",
                    "Las vistas fueron probadas en dispositivos Android físicos (Xiaomi, Samsung y Motorola), confirmando tiempos de respuesta menores a 300 ms en el escáner de cámara y renderizado continuo a 60 cuadros por segundo en el mapa GPS.", "blue")

    # ==============================================================
    # PÁGINA 10: CONCLUSIONES INDIVIDUALES POR ROL DEL EQUIPO
    # ==============================================================
    pdf.add_page()
    pdf.set_y(18)
    render_section_title("8", "CONCLUSIÓN DE LA FASE 2 POR INTEGRANTE SEGÚN SU ROL")
    render_p("A continuación se presentan las conclusiones individuales de los cuatro integrantes del equipo de IDGS, fundamentando los aprendizajes, contribuciones técnicas y valor aportado al proyecto SaveBite de acuerdo con el rol que desempeñaron:")

    conclusions = [
        ("Alvaro Jesús Chávez Bazana", "Product Owner (PO) — Gestor de Requisitos",
         "Desde la perspectiva del Product Owner, la consolidación de la Fase 2 representa la maduración técnica indispensable para materializar la propuesta de valor de SaveBite. Al definir una arquitectura desacoplada y un ecosistema de servicios robusto, garantizamos que la solución no sea solo un prototipo académico, sino una plataforma viable que resuelve una problemática real de merma alimentaria en Salamanca bajo el ODS 12. La integración de la calculadora de impacto ecológico y la transparencia jurídica derivada de la LFPDPPP otorgan certeza y confianza plena tanto al estudiante que busca cuidar su economía como al comerciante aliado que desea evitar desperdicios y dinamizar su inventario."),
        
        ("Guillermo Yael Berlín Fomperosa", "Scrum Master (SM) — Facilitador & QA",
         "Como Scrum Master y responsable del aseguramiento de calidad (QA), la definición del flujo de versionamiento con GitFlow, la política de Conventional Commits y la automatización del pipeline en GitHub Actions han transformado radicalmente la sinergia del equipo. Se eliminaron por completo las fricciones por conflictos de ramas y se garantizó que ningún código con advertencias de linter o pruebas unitarias fallidas llegue a la rama principal. Asimismo, la implementación del checklist de seguridad nos brinda un marco de verificación continuo y riguroso para auditar cada entrega quincenal antes de presentarla a la docente, asegurando un producto libre de deuda técnica."),

        ("Juan Pablo Vega Uribe", "Lead Mobile Developer — Frontend & UI/UX",
         "En mi rol de desarrollador frontend líder y diseñador de la experiencia de usuario, la adopción del patrón BLoC en conjunto con Flutter SDK 3.x ha demostrado ser la decisión más acertada. La separación estricta entre los widgets visuales y la lógica de estado permitió lograr una interfaz reactiva, moderna con Material 3 y extraordinariamente fluida a 60 FPS, incluso durante la manipulación de marcadores en el mapa interactivo con Google Maps. La optimización del visor de cámara con Mobile Scanner sobre CameraX logró reducir la latencia de detección del código QR a menos de 300 ms, garantizando una validación en mostrador inmediata y sin fricciones."),

        ("Diego Sebastián Vilegas Enriquez", "Backend & Data Architect — Cloud BaaS & Offline",
         "Desde el ámbito de la arquitectura de datos y servicios en la nube, el mayor desafío y satisfacción técnica de esta Fase 2 fue diseñar la resiliencia Offline-First mediante el Repository Pattern. Al combinar la base de datos documental en tiempo real y el control de acceso por roles (RBAC) en la nube con la caché binaria local de Hive y el hardware criptográfico de Android KeyStore, blindamos por completo los vouchers de canje con firmas HMAC-SHA256. Esto asegura que la transacción sea inalterable, segura y ejecutable en cualquier circunstancia, cumpliendo cabalmente con la normativa mexicana de protección de datos personales.")
    ]

    for member_name, role_title, conc_text in conclusions:
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(203, 213, 225)
        
        # Calcular altura
        pdf.set_font("ArialUni", "", 7.8)
        lines = len(pdf.multi_cell(164, 3.7, conc_text, dry_run=True, output="LINES"))
        card_h = (lines * 3.7) + 12

        cur_y = pdf.get_y()
        pdf.rect(18, cur_y, 174, card_h, "FD")
        pdf.set_fill_color(15, 76, 129)
        pdf.rect(18, cur_y, 3, card_h, "F")

        pdf.set_xy(24, cur_y + 2)
        pdf.set_font("ArialUni", "B", 8.6)
        pdf.set_text_color(15, 76, 129)
        pdf.cell(100, 4, member_name, 0, new_x=XPos.RIGHT, new_y=YPos.TOP)

        pdf.set_font("ArialUni", "I", 7.8)
        pdf.set_text_color(14, 116, 144)
        pdf.cell(64, 4, role_title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

        pdf.set_xy(24, cur_y + 7.5)
        pdf.set_font("ArialUni", "", 7.8)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(164, 3.7, conc_text)
        pdf.set_y(cur_y + card_h + 2)

    pdf.output(output_pdf_path)
    print(f"PDF Fase 2 SaveBite generado con éxito total en: {output_pdf_path}")

if __name__ == "__main__":
    out_pdf = r"c:\Users\galan\OneDrive - Universidad Tecnológica de Salamanca\Aplicación\Fase2_Plan_Desarrollo_Movil_SaveBite.pdf"
    build_pdf(out_pdf)
