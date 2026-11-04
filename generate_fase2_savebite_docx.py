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

def create_savebite_fase2_docx(output_path):
    doc = docx.Document()

    # Configuración de márgenes estándar (2.2 cm)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
        # Header y Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("UNIVERSIDAD TECNOLÓGICA DE SALAMANCA • IDGS | SaveBite Fase 2")
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
    # 1. PORTADA FORMAL UTS
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
    r_car.font.size = Pt(11)
    r_car.font.bold = True
    r_car.font.color.rgb = RGBColor(0, 174, 157)

    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_badge = p_badge.add_run(" FASE 2: ARQUITECTURA, PLANIFICACIÓN Y SEGURIDAD DEL DESARROLLO MÓVIL ")
    r_badge.font.name = "Arial"
    r_badge.font.size = Pt(10)
    r_badge.font.bold = True
    r_badge.font.color.rgb = RGBColor(245, 130, 32)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("SaveBite\n")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 76, 129)

    r_sub = p_title.add_run("Plataforma Móvil Colaborativa de Rescate de Alimentos Locales a Precio Reducido\n(ODS 12: Cero Merma)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(10.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    # Tabla de Portada: Asignatura (Izq) y Equipo (Der)
    table_cover = doc.add_table(rows=1, cols=2)
    table_cover.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_l, cell_r = table_cover.rows[0].cells
    cell_l.width = Inches(3.2)
    cell_r.width = Inches(3.6)
    set_cell_background(cell_l, "F8FAFC")
    set_cell_background(cell_r, "F8FAFC")
    set_cell_margins(cell_l, 120, 120, 160, 160)
    set_cell_margins(cell_r, 120, 120, 160, 160)

    p_cl = cell_l.paragraphs[0]
    r_cl_h = p_cl.add_run("DATOS DE LA ASIGNATURA\n")
    r_cl_h.font.bold = True
    r_cl_h.font.size = Pt(10)
    r_cl_h.font.color.rgb = RGBColor(15, 76, 129)
    p_cl.add_run("Asignatura: ").font.bold = True
    p_cl.add_run("Desarrollo Móvil Integral\n")
    p_cl.add_run("Carrera: ").font.bold = True
    p_cl.add_run("IDGS (10° Cuatrimestre)\n")
    p_cl.add_run("Docente: ").font.bold = True
    p_cl.add_run("Ericka Nohemí Álvarez Valencia\n")
    p_cl.add_run("Fecha de Entrega: ").font.bold = True
    p_cl.add_run("04 de Noviembre de 2026\n")
    p_cl.add_run("Entregable: ").font.bold = True
    p_cl.add_run("Documento Digital Fase 2")

    p_cr = cell_r.paragraphs[0]
    r_cr_h = p_cr.add_run("INTEGRANTES DEL EQUIPO (IDGS)\n")
    r_cr_h.font.bold = True
    r_cr_h.font.size = Pt(10)
    r_cr_h.font.color.rgb = RGBColor(0, 174, 157)

    team = [
        ("Alvaro Jesús Chávez Bazana", "Product Owner (PO)"),
        ("Guillermo Yael Berlín Fomperosa", "Scrum Master (SM)"),
        ("Juan Pablo Vega Uribe", "Lead Mobile Dev (UI/UX)"),
        ("Diego Sebastián Vilegas Enriquez", "Backend & Data Architect")
    ]
    for m_name, m_role in team:
        p_cr.add_run(f"• {m_name}\n").font.bold = True
        r_rl = p_cr.add_run(f"   Rol: {m_role}\n")
        r_rl.font.italic = True
        r_rl.font.size = Pt(8.5)
        r_rl.font.color.rgb = RGBColor(14, 116, 144)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(20)
    r_loc = p_loc.add_run("Salamanca, Guanajuato, México — Universidad Tecnológica de Salamanca")
    r_loc.font.size = Pt(8.5)
    r_loc.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # Helpers para secciones en docx
    def add_sec_heading(num_str, title_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        r_num = p.add_run(f"{num_str}. ")
        r_num.font.bold = True
        r_num.font.size = Pt(12)
        r_num.font.color.rgb = RGBColor(0, 174, 157)
        r_t = p.add_run(title_str)
        r_t.font.bold = True
        r_t.font.size = Pt(12)
        r_t.font.color.rgb = RGBColor(15, 76, 129)

    def add_sub_heading(sub_title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f"> {sub_title}")
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(14, 116, 144)

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(51, 65, 85)

    def add_bullet(b_title, b_desc):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run(f"{b_title}: ")
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(15, 76, 129)
        r2 = p.add_run(b_desc)
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = RGBColor(51, 65, 85)

    def add_callout(box_title, box_text, hex_bg="F0F9FF", hex_border="0E7490"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        cell.width = Inches(6.8)
        set_cell_background(cell, hex_bg)
        set_cell_margins(cell, 100, 100, 150, 150)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(f"{box_title}\n")
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(14, 116, 144)
        r2 = p.add_run(box_text)
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = RGBColor(51, 65, 85)

    # ==============================================================
    # SECCIÓN 1: INTRODUCCIÓN
    # ==============================================================
    add_sec_heading("1", "INTRODUCCIÓN A LA FASE 2: ARQUITECTURA, PLANIFICACIÓN Y SEGURIDAD")
    add_p("Habiendo fundamentado el alcance, la metodología ágil Scrum y los requerimientos funcionales en la Fase 1 para la plataforma SaveBite, la presente Fase 2 tiene como objetivo formalizar el diseño arquitectónico profundo, la justificación técnica de frameworks, los esquemas de versionamiento profesional, el blindaje de seguridad móvil y el ecosistema de servicios integrados en la nube.")
    
    add_sub_heading("1.1 Propósito Técnico y Estratégico de la Fase 2")
    add_p("El desarrollo móvil profesional demanda una ingeniería defensiva que responda con solvencia a las restricciones severas del hardware móvil: fluctuación de red en calle, consumo estricto de batería al operar el sensor GPS, latencia en la decodificación de códigos QR con la cámara y estrictas regulaciones sobre la privacidad de la geolocalización del usuario.")
    add_p("Mediante esta planeación integral se asegura que SaveBite no dependa de implementaciones acopladas o código improvisado, garantizando que cada módulo desarrollado por el equipo converja bajo estándares de la industria como Clean Architecture, OWASP Mobile Top 10 y la legislación mexicana LFPDPPP.")

    # ==============================================================
    # SECCIÓN 2: PATRONES DE DISEÑO
    # ==============================================================
    add_sec_heading("2", "PROPUESTA Y JUSTIFICACIÓN DE PATRONES DE DISEÑO")
    add_callout("Patrones de Diseño Seleccionados para SaveBite",
                "Para responder a los desafíos de persistencia híbrida, reactividad en tiempo real y alta testabilidad, se seleccionaron formalmente cuatro patrones de diseño complementarios: Repository Pattern, BLoC Pattern (Observer), Service Locator (Singleton) y Data Transfer Object (DTO) con Factory Method.")

    add_sub_heading("2.1 Patrón Repositorio (Repository Pattern) - Fuente Única de Verdad")
    add_bullet("Uso en SaveBite", "Actúa como un intermediario y árbitro inteligente entre la capa de Dominio (Casos de Uso) y las múltiples fuentes de datos (Remote DataSource vía Supabase/Firebase y Local DataSource vía Hive/SQLite). Centraliza la lógica de almacenamiento y recuperación de paquetes sorpresa, comercios y vouchers de reserva.")
    add_bullet("Justificación Técnica", "Garantiza el desacoplamiento total de la lógica de negocio respecto a los mecanismos concretos de persistencia. Si el comensal se encuentra en mostrador sin cobertura celular (3G/4G/5G débil), el repositorio entrega el voucher de reserva desde la caché local sin disparar excepciones ni bloquear la UI, permitiendo un canje 100% resiliente (Offline-First).")

    add_sub_heading("2.2 Patrón BLoC (Business Logic Component) / Observer Pattern")
    add_bullet("Uso en SaveBite", "Rige la gestión reactiva de estado en la Capa de Presentación bajo el paradigma de Flujo Unidireccional de Datos (UDF). La interfaz emite eventos discretos (ej. SolicitarReservaEvent, ActualizarFiltroDistanciaEvent), el BLoC procesa la lógica invocando el Caso de Uso y emite nuevos estados inmutables (ReservaCargando, ReservaExitosa, ErrorState) escuchados por la UI mediante Streams de Dart.")
    add_bullet("Justificación Técnica", "Elimina de raíz el desorden derivado de llamadas dispersas a setState(), reduciendo el consumo de batería y CPU al evitar repintados innecesarios en el árbol de widgets. Facilita la elaboración de pruebas unitarias automatizadas con la suite bloc_test sin requerir emuladores ni mocks complejos de interfaz.")

    add_sub_heading("2.3 Patrón Service Locator / Singleton (Inyección de Dependencias con GetIt)")
    add_bullet("Uso en SaveBite", "Administra de forma centralizada la instanciación perezosa (Lazy Singleton) de servicios críticos globales, tales como el cliente de red SupabaseClient, el motor de almacenamiento seguro FlutterSecureStorage, los controladores de ubicación satelital y el manejador de notificaciones push.")
    add_bullet("Justificación Técnica", "Previene la creación descontrolada de sockets, conexiones HTTP redundantes o relecturas de llaves de cifrado en memoria, disminuyendo el footprint de RAM en el dispositivo móvil.")

    add_sub_heading("2.4 Patrón Factory Method y Data Transfer Object (DTO)")
    add_bullet("Uso en SaveBite", "Encapsula la serialización y deserialización segura de payloads JSON procedentes de la nube hacia entidades inmutables del dominio (FoodPackage, Store, Reservation, EcoImpact) a través de constructores nombrados Factory (ej. FoodPackageModel.fromJson(json)).")
    add_bullet("Justificación Técnica", "Otorga tipado fuerte y validación de esquemas en tiempo de compilación. Resguarda a la aplicación contra anomalías de valores nulos imprevistos (Null Safety en Dart 3).")

    if os.path.exists("diagram_fase2_patrones_arquitectura.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture("diagram_fase2_patrones_arquitectura.png", width=Inches(6.6))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 1: Arquitectura de Software y Patrones de Diseño Aplicados en SaveBite")
        r_cap.font.italic = True
        r_cap.font.size = Pt(8.5)

    # ==============================================================
    # SECCIÓN 3: FRAMEWORKS Y HERRAMIENTAS
    # ==============================================================
    add_sec_heading("3", "JUSTIFICACIÓN DE FRAMEWORKS Y HERRAMIENTAS A UTILIZAR")
    add_p("La selección tecnológica de SaveBite responde a una rigurosa evaluación de criterios de ingeniería de software móvil, priorizando rendimiento nativo, reducción de tiempos de desarrollo y soporte a largo plazo.")

    add_sub_heading("3.1 Framework Principal de Desarrollo: Flutter SDK (Dart 3.x)")
    add_bullet("Rendimiento Extremo (Compilación AOT)", "Flutter compila directamente a código máquina nativo C/C++ ARM64 mediante Ahead-Of-Time (AOT), eliminando los puentes de JavaScript. Gracias a su nuevo motor gráfico Impeller sobre Vulkan/Metal, renderiza animaciones fluidas a 60 y 120 FPS sin caídas de cuadros.")
    add_bullet("Soporte Multiplataforma Real", "Un único código fuente (Single Codebase) genera binarios nativos para Android (APK/AAB) e iOS (IPA), maximizando la productividad del equipo y garantizando paridad total de interfaz y lógica.")
    add_bullet("Curva de Aprendizaje y Tipado Fuerte", "Dart 3 implementa Sound Null Safety estricto, pattern matching y records, reduciendo errores en tiempo de ejecución en más del 80%.")
    add_bullet("Comunidad y Ecosistema pub.dev", "Respaldado directamente por Google y con millones de paquetes mantenidos por la comunidad, pub.dev ofrece librerías optimizadas para hardware móvil nativo.")

    # Tabla de Herramientas
    table_tools = doc.add_table(rows=6, cols=3)
    table_tools.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_t = ["Tecnología / Herramienta", "Categoría / Función", "Argumentación y Ventaja Técnica"]
    widths_t = [Inches(1.8), Inches(1.8), Inches(3.2)]
    
    for c_idx, h_text in enumerate(headers_t):
        cell = table_tools.rows[0].cells[c_idx]
        cell.width = widths_t[c_idx]
        set_cell_background(cell, "0F4C81")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    tools_data = [
        ("Flutter SDK 3.x", "Framework UI Móvil", "Compilación AOT nativa C++, motor Impeller a 60 FPS, Material 3 reactivo."),
        ("Supabase / Firebase BaaS", "Cloud Backend & DB", "Auth JWT, PostgreSQL con PostGIS / Firestore NoSQL, WebSockets en tiempo real."),
        ("mobile_scanner (CameraX)", "Visor y Decodificador QR", "Escaneo ultrarrápido (<300 ms) integrado directo a los drivers de hardware."),
        ("Hive & Secure Storage", "Persistencia Local", "Caché NoSQL binaria ultraligera para modo offline y cifrado AES-256 en KeyStore."),
        ("flutter_lints & DevTools", "Calidad y Profiling", "Análisis estático de código estricto y perfilado de consumo de memoria y CPU.")
    ]

    for row_idx, data_row in enumerate(tools_data):
        for col_idx, cell_value in enumerate(data_row):
            cell = table_tools.rows[row_idx + 1].cells[col_idx]
            cell.width = widths_t[col_idx]
            bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(cell_value)
            r.font.size = Pt(8.0)
            r.font.color.rgb = RGBColor(51, 65, 85)

    # ==============================================================
    # SECCIÓN 4: ESTRATEGIAS DE VERSIONAMIENTO
    # ==============================================================
    add_sec_heading("4", "ESTRATEGIAS DE VERSIONAMIENTO Y GESTIÓN DEL CÓDIGO")
    add_p("Para salvaguardar la integridad del código fuente, habilitar la integración continua entre los 4 desarrolladores y prevenir regresiones en las entregas quincenales, se definió una estrategia de versionamiento profesional basada en GitFlow, Semantic Versioning y CI/CD.")

    add_sub_heading("4.1 Estructura del Flujo de Ramas (GitFlow Adaptado)")
    add_bullet("main (Producción)", "Rama protegida contra escritura directa. Solo alberga releases estables, etiquetadas y validadas con firmas criptográficas de producción. Requiere Pull Request obligatorio con 2 aprobaciones.")
    add_bullet("develop (Integración)", "Rama principal de trabajo continuo. Centraliza las funcionalidades validadas en cada Sprint. Es la base para pruebas de control de calidad (QA).")
    add_bullet("feature/<nombre>", "Ramas de corta duración nacidas de develop para cada historia de usuario (ej. feature/modulo-mapa-gps, feature/lector-qr-camerax). Se eliminan tras merge.")
    add_bullet("release/vX.Y.Z", "Ramas de estabilización previas a un hito de entrega. Se congelan cambios mayores y solo se admiten parches de pulido de UI y documentación.")
    add_bullet("hotfix/<incidencia>", "Ramas de emergencia que se originan directamente de main para mitigar vulnerabilidades o errores críticos en producción, integrándose a main y develop.")

    add_sub_heading("4.2 Versionado Semántico (SemVer 2.0.0 + Build Numbers)")
    add_p("Se adopta la nomenclatura formal MAJOR.MINOR.PATCH+BUILD (ejemplo: v1.0.0+1):")
    add_bullet("MAJOR (1.x.x)", "Incrementa ante rupturas de compatibilidad con la API o cambios estructurales en la arquitectura de base de datos.")
    add_bullet("MINOR (x.1.x)", "Incrementa al incorporar nuevas funcionalidades compatibles hacia atrás (ej. APK v0.2.0 al sumar el módulo de publicación de paquetes).")
    add_bullet("PATCH (x.x.1)", "Incrementa ante correcciones de errores, bugs menores de interfaz o ajustes de rendimiento sin alterar los contratos existentes.")
    add_bullet("BUILD NUMBER (+X)", "Entero secuencial autoincrementable requerido por Android (versionCode) y Play Store para identificar cada compilación física de APK.")

    add_sub_heading("4.3 Convención de Commits Semánticos (Conventional Commits)")
    add_bullet("feat(scanner)", "Implementación de decodificador de códigos QR con Mobile Scanner en cámara.")
    add_bullet("fix(auth)", "Resolución de fallo de expiración en refresh tokens JWT de Supabase Auth.")
    add_bullet("perf(map)", "Optimización de marcadores de comercios mediante clustering geoespacial en Haversine.")
    add_bullet("security(voucher)", "Incorporación de firma criptográfica HMAC-SHA256 en payload de códigos QR.")

    if os.path.exists("diagram_fase2_versionamiento_gitflow.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture("diagram_fase2_versionamiento_gitflow.png", width=Inches(6.6))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 2: Estrategia de Versionamiento GitFlow, SemVer y Automatización CI/CD")
        r_cap.font.italic = True
        r_cap.font.size = Pt(8.5)

    # ==============================================================
    # SECCIÓN 5: SEGURIDAD, PRIVACIDAD Y CUMPLIMIENTO LEGAL
    # ==============================================================
    add_sec_heading("5", "SEGURIDAD, PRIVACIDAD Y CUMPLIMIENTO LEGAL EN ENTORNOS MÓVILES")
    add_p("La confianza de los estudiantes y de los comercios gastronómicos locales es el pilar de SaveBite. La aplicación implementa una estrategia de seguridad por diseño (Security by Design), alineada rigurosamente con el marco jurídico mexicano y con los estándares internacionales de seguridad móvil.")

    add_sub_heading("5.1 Cumplimiento de la Normativa Local Vigente en México (LFPDPPP)")
    add_p("SaveBite opera bajo la jurisdicción de la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP) y las directrices del Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales (INAI), rigiéndose por los siguientes principios rectores:")
    add_bullet("Principio de Licitud", "El tratamiento de los datos personales de estudiantes y dueños de negocios se apega estrictamente a las leyes mexicanas y al orden público.")
    add_bullet("Principio de Consentimiento", "Se recaba el consentimiento expreso y verificable del usuario mediante un opt-in activo durante el registro previo a recopilar cualquier información personal o activar permisos de hardware.")
    add_bullet("Principio de Información (Avisos de Privacidad)", "SaveBite despliega dos modalidades: 1) Aviso de Privacidad Simplificado al solicitar acceso al GPS y cámara, y 2) Aviso de Privacidad Integral accesible permanentemente desde los ajustes de la app y portal web.")
    add_bullet("Principio de Finalidad y Lealtad", "La información recolectada se utiliza exclusivamente para la reserva, canje de alimentos y cálculo de métricas ODS. Queda terminantemente prohibida su comercialización o perfilamiento publicitario a terceros.")
    add_bullet("Principio de Proporcionalidad (Minimización)", "Únicamente se solicitan los datos indispensables para ejecutar la transacción. No se solicitan contactos de la agenda, acceso a fotos privadas ni SMS.")
    add_bullet("Ejercicio de Derechos ARCO", "La aplicación provee una sección directa en el perfil del usuario para ejercer sus derechos de Acceso, Rectificación, Cancelación y Oposición de sus datos.")

    add_sub_heading("5.2 Principios de Codificación Segura Móvil (OWASP Mobile Top 10 & MASVS)")
    add_bullet("M1 - Almacenamiento Seguro", "Las llaves de sesión, tokens JWT y credenciales se guardan exclusivamente en el hardware criptográfico nativo: Android KeyStore (AES-256-GCM) y iOS Keychain mediante la librería flutter_secure_storage.")
    add_bullet("M2 - Criptografía Robusta en Vouchers QR", "El código QR contiene un token firmado con HMAC-SHA256 que incluye el identificador de reserva, un Nonce aleatorio de un solo uso y un Timestamp de caducidad (ventana de recogida de 60 min).")
    add_bullet("M3 - Comunicaciones Cifradas en Tránsito", "Todas las conexiones hacia el BaaS y APIs externas exigen TLS 1.3 / HTTPS forzado. En AndroidManifest.xml se declara android:usesCleartextTraffic='false'.")
    add_bullet("M4 - Autenticación y Autorización Robusta", "Tokens JWT efímeros firmados por el servidor con expiración de 1 hora y refresh tokens rotativos con control RBAC.")
    add_bullet("M5 - Validación Estricta de Entradas", "Sanitización exhaustiva en cliente Flutter y servidor en la nube, bloqueando inyecciones SQL, NoSQL y ataques XSS.")
    add_bullet("M6 - Protección de Binarios y Ofuscación", "Compilación AOT nativa y configuración de ProGuard/R8 con ofuscación de nombres de clases y métodos en el APK Release.")

    add_sub_heading("5.3 Checklist Exhaustivo de Seguridad Móvil")
    # Tabla de Checklist
    sec_data = [
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

    table_sec = doc.add_table(rows=len(sec_data) + 1, cols=5)
    table_sec.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_s = ["Categoría", "Control Técnico / Criterio", "Estado", "Mecanismo / Herramienta", "Responsable"]
    widths_s = [Inches(1.1), Inches(2.3), Inches(0.9), Inches(1.5), Inches(1.0)]

    for c_idx, h_text in enumerate(headers_s):
        cell = table_sec.rows[0].cells[c_idx]
        cell.width = widths_s[c_idx]
        set_cell_background(cell, "0F4C81")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.0)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, s_row in enumerate(sec_data):
        for col_idx, s_val in enumerate(s_row):
            cell = table_sec.rows[row_idx + 1].cells[col_idx]
            cell.width = widths_s[col_idx]
            bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(s_val)
            r.font.size = Pt(7.5)
            if col_idx == 2:
                r.font.bold = True
                r.font.color.rgb = RGBColor(4, 120, 87) if s_val == "Implementado" else RGBColor(180, 83, 9)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    # ==============================================================
    # SECCIÓN 6: ECOSISTEMA DE SERVICIOS E INTEGRACIÓN CLOUD
    # ==============================================================
    add_sec_heading("6", "ECOSISTEMA DE SERVICIOS E INTEGRACIÓN")
    add_p("SaveBite combina de forma sinérgica APIs de terceros de clase mundial con una infraestructura en la nube elástica (Cloud BaaS) para brindar una experiencia inmediata tanto al comensal universitario como al dueño del establecimiento comercial.")

    add_sub_heading("6.1 Consumo de APIs de Terceros")
    add_bullet("Google Maps Platform & Places API", "Provee mapas vectoriales fluidos para Android e iOS. Se utiliza el servicio de geocodificación inversa y cálculo de distancias geodésicas mediante la fórmula de Haversine para listar en tiempo real los comercios con paquetes activos a menos de 3 km del estudiante.")
    add_bullet("Pasarela de Pagos Digitales (Stripe / Mercado Pago SDK)", "Permite cobros seguros in-app mediante tarjetas de débito/crédito y transferencias SPEI. Cumple la certificación PCI-DSS Nivel 1 mediante tokenización de tarjetas: la app de SaveBite jamás toca ni almacena datos financieros del comprador.")
    add_bullet("Autenticación Federada (Google Sign-In OAuth 2.0)", "Facilita el registro y login en un solo toque mediante cuentas de Google institucionales (@utsalamanca.edu.mx) o personales, disminuyendo la fricción inicial de adopción.")
    add_bullet("Motor de Cámara y Escaneo (Mobile Scanner / Google ML Kit Vision)", "Procesa el stream de video de la cámara física a 60 FPS mediante los subsistemas nativos CameraX (Android) y AVFoundation (iOS) decodificando códigos QR en menos de 300 ms en el mostrador.")

    add_sub_heading("6.2 Arquitectura Cloud y Servicios Críticos en la Nube")
    add_bullet("Supabase Auth / Firebase Auth", "Gestión centralizada de identidades con tokens criptográficos JWT y hashing seguro de contraseñas con algoritmos Argon2 / bcrypt.")
    add_bullet("Base de Datos en Tiempo Real y Espacial (PostgreSQL PostGIS / Cloud Firestore)", "Almacena el catálogo de paquetes y comercios con soporte geoespacial. Mediante suscripciones por WebSockets / Streams, el mapa se sincroniza al instante.")
    add_bullet("Almacenamiento de Archivos (Cloud Storage)", "Buckets seguros compatibles con S3 para fotos de locales y comida, optimizadas en WebP con CDN.")
    add_bullet("Notificaciones Push en Tiempo Real (Firebase Cloud Messaging - FCM)", "Envío de alertas automáticas al celular cuando un comercio favorito publica ofertas y recordatorios preventivos cuando restan 30 minutos de la ventana de recogida.")
    add_bullet("Lógica Serverless (Edge Functions)", "Microservicios que liberan automáticamente reservas no reclamadas y consolidan los reportes de kg de comida rescatada y CO2 mitigado.")

    if os.path.exists("diagram_fase2_ecosistema_integracion.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture("diagram_fase2_ecosistema_integracion.png", width=Inches(6.6))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 3: Ecosistema de Servicios e Integración Cloud en SaveBite")
        r_cap.font.italic = True
        r_cap.font.size = Pt(8.5)

    # ==============================================================
    # SECCIÓN 7: CAPTURAS DEL AVANCE DE LA APP
    # ==============================================================
    add_sec_heading("7", "EVIDENCIAS Y CAPTURAS DEL AVANCE DE LA APP REVISADAS EN CLASE")
    add_p("Durante las sesiones prácticas y revisiones de Sprint en clase con la docente Ericka Nohemí Álvarez Valencia, el equipo presentó avances funcionales de los componentes core de SaveBite. A continuación se presentan las evidencias de las pantallas operativas implementadas en Flutter:")

    mockups = [
        ("screen_1_auth.png", "1. Splash & Multi-Rol (Alumno / Comercio)"),
        ("screen_2_explore_map.png", "2. Mapa GPS & Feed de Paquetes con Descuento"),
        ("screen_3_package_detail.png", "3. Ficha Detallada de Paquete y Reserva In-App"),
        ("screen_4_voucher_qr.png", "4. Voucher Digital de Canje con QR Dinámico"),
        ("screen_5_scanner.png", "5. Escáner QR de Mostrador con Cámara CameraX"),
        ("screen_6_eco_impact.png", "6. Calculadora de Impacto Ecológico ODS 12")
    ]

    # Insertar en tabla de 2 columnas x 3 filas
    table_mock = doc.add_table(rows=3, cols=2)
    table_mock.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (m_fn, m_title) in enumerate(mockups):
        r_idx = idx // 2
        c_idx = idx % 2
        cell = table_mock.rows[r_idx].cells[c_idx]
        cell.width = Inches(3.4)
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, 80, 80, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if os.path.exists(m_fn):
            run_img = p.add_run()
            run_img.add_picture(m_fn, width=Inches(2.5))
        p_lbl = cell.add_paragraph()
        p_lbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_lbl = p_lbl.add_run(m_title)
        r_lbl.font.bold = True
        r_lbl.font.size = Pt(8.0)
        r_lbl.font.color.rgb = RGBColor(15, 76, 129)

    # ==============================================================
    # SECCIÓN 8: CONCLUSIONES INDIVIDUALES POR ROL
    # ==============================================================
    add_sec_heading("8", "CONCLUSIÓN DE LA FASE 2 POR INTEGRANTE SEGÚN SU ROL")
    add_p("A continuación se presentan las conclusiones individuales de los cuatro integrantes del equipo de IDGS, fundamentando los aprendizajes, contribuciones técnicas y valor aportado al proyecto SaveBite de acuerdo con el rol que desempeñaron:")

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
        tbl_c = doc.add_table(rows=1, cols=1)
        tbl_c.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl_c.rows[0].cells[0]
        cell.width = Inches(6.8)
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, 100, 100, 140, 140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(f"{member_name} — ")
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(15, 76, 129)
        r2 = p.add_run(f"Rol: {role_title}\n")
        r2.font.bold = True
        r2.font.italic = True
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = RGBColor(14, 116, 144)
        r3 = p.add_run(conc_text)
        r3.font.size = Pt(8.8)
        r3.font.color.rgb = RGBColor(51, 65, 85)

    doc.save(output_path)
    print(f"Documento Word Fase 2 SaveBite generado con éxito en: {output_path}")

if __name__ == "__main__":
    out_docx = r"c:\Users\galan\OneDrive - Universidad Tecnológica de Salamanca\Aplicación\Fase2_Plan_Desarrollo_Movil_SaveBite.docx"
    create_savebite_fase2_docx(out_docx)
