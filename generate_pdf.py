import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class PDFReport(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        
    def header(self):
        if self.page_no() > 1:
            self.set_fill_color(245, 247, 250)
            self.rect(0, 0, 210, 16, "F")
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(70, 80, 95)
            self.set_xy(15, 5)
            self.cell(100, 6, "UNIVERSIDAD TECNOLOGICA DE SALAMANCA - IDGS 10B", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.set_font("Helvetica", "I", 8)
            self.cell(80, 6, "LabPass QR | Inicio de Proyecto APP", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
            self.set_draw_color(200, 210, 225)
            self.line(15, 14, 195, 14)
            self.ln(12)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(130, 140, 155)
            self.line(15, 282, 195, 282)
            self.set_x(15)
            self.cell(90, 8, "Desarrollo Movil Integral - Entrega de Proyecto", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.cell(90, 8, f"Pagina {self.page_no()}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

def create_full_pdf(output_path):
    pdf = PDFReport()
    
    # ---------------------------------------------
    # PORTADA COLORIDA
    # ---------------------------------------------
    pdf.add_page()
    
    # Fondo superior azul marino tecnológico
    pdf.set_fill_color(15, 76, 129)
    pdf.rect(0, 0, 210, 95, "F")
    
    # Franja turquesa
    pdf.set_fill_color(0, 174, 157)
    pdf.rect(0, 92, 210, 5, "F")

    # Franja naranja/ambar
    pdf.set_fill_color(245, 130, 32)
    pdf.rect(0, 97, 210, 3, "F")
    
    # Textos Portada - Header
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_xy(15, 18)
    pdf.cell(180, 7, "UNIVERSIDAD TECNOLOGICA DE SALAMANCA", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(180, 6, "DIVISION DE TECNOLOGIAS DE LA INFORMACION Y COMUNICACION", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(180, 6, "INGENIERIA EN DESARROLLO Y GESTION DE SOFTWARE", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(180, 10, "LabPass QR", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(220, 240, 250)
    pdf.cell(180, 7, "Sistema Movil de Prestamo de Materiales y Laboratorios", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    
    # Tarjeta de Datos de la Materia
    pdf.set_xy(20, 115)
    pdf.set_fill_color(245, 248, 252)
    pdf.set_draw_color(210, 225, 240)
    pdf.rect(20, 115, 170, 38, "FD")
    
    pdf.set_xy(25, 120)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 76, 129)
    pdf.cell(40, 6, "Asignatura:", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 50, 60)
    pdf.cell(110, 6, "Desarrollo Movil Integral / Integradora", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(25)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 76, 129)
    pdf.cell(40, 6, "Actividad:", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 50, 60)
    pdf.cell(110, 6, "Inicio de proyecto APP (Fase de Alcance y Definicion)", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(25)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 76, 129)
    pdf.cell(40, 6, "Grado y Grupo:", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 50, 60)
    pdf.cell(110, 6, "10 B (IDGS)", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(25)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 76, 129)
    pdf.cell(40, 6, "Fecha:", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 50, 60)
    pdf.cell(110, 6, "Octubre 2026", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Tarjeta de Integrantes
    pdf.set_xy(20, 162)
    pdf.set_fill_color(237, 246, 255)
    pdf.set_draw_color(180, 210, 245)
    pdf.rect(20, 162, 170, 75, "FD")
    
    pdf.set_fill_color(15, 76, 129)
    pdf.rect(20, 162, 170, 10, "F")
    pdf.set_xy(20, 163)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(170, 8, "EQUIPO DE DESARROLLO (INTEGRANTES)", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    
    miembros = [
        "Alvaro Jesus Chavez Bazana",
        "Guillermo Yael Berlin Fomperosa",
        "Juan Pablo Vega Uribe",
        "Diego Sebastian Vilegas Enriquez"
    ]
    
    y_m = 178
    for m in miembros:
        pdf.set_fill_color(0, 174, 157)
        pdf.circle(30, y_m + 3, 2, "F")
        pdf.set_xy(36, y_m)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(30, 45, 65)
        pdf.cell(130, 6, m, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        y_m += 13

    # Pie de portada
    pdf.set_xy(20, 250)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(100, 115, 130)
    pdf.cell(170, 6, "Salamanca, Guanajuato, Mexico", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    
    # ---------------------------------------------
    # PAGINAS DE CONTENIDO
    # ---------------------------------------------
    pdf.add_page()
    
    def section_header(num_str, title_str):
        pdf.ln(3)
        pdf.set_fill_color(15, 76, 129)
        pdf.rect(15, pdf.get_y(), 4, 8, "F")
        pdf.set_x(22)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(15, 76, 129)
        pdf.cell(170, 8, f"{num_str}. {title_str}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_draw_color(210, 220, 235)
        pdf.line(15, pdf.get_y()+1, 195, pdf.get_y()+1)
        pdf.ln(3)

    def sub_header(question_str):
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(20, 100, 150)
        pdf.multi_cell(180, 5, question_str)
        pdf.ln(1)

    def body_p(text_str):
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(50, 60, 70)
        pdf.multi_cell(180, 4.5, text_str)
        pdf.ln(2)

    def bullet_p(label, text_str):
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(40, 50, 60)
        pdf.set_x(20)
        pdf.cell(5, 4.5, ">", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(45, 4.5, f"{label}: ", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 70, 80)
        pdf.multi_cell(130, 4.5, text_str)
        pdf.ln(1.5)

    # 1. Definicion del Problema y Justificacion
    section_header("1", "DEFINICION DEL PROBLEMA Y JUSTIFICACION")
    
    sub_header("1.1 ¿Cual es el problema real, necesidad u oportunidad que detectaron en el mercado o en el entorno?")
    body_p("En las instituciones educativas de nivel superior, especificamente en campus tecnologicos y universidades como la UTS, los laboratorios (computo, electronica, mecatronica, quimica y redes) manejan a diario decenas de componentes, herramientas especializadas, laptops y tarjetas de desarrollo. Actualmente, el proceso de solicitud, asignacion y devolucion de estos recursos se realiza de forma manual y fragmentada (en bitacoras de papel o libros de registro en mostrador).")
    body_p("Esto ocasiona largos tiempos de espera en las horas pico de inicio y fin de clase, falta de certeza sobre quien tiene un equipo especifico en tiempo real, extravio recurrente de accesorios/cables, y ausencia de metricas claras sobre la tasa de uso o deterioro del inventario institucional.")

    sub_header("1.2 ¿Por que los metodos actuales para resolver este problema son ineficientes o insuficientes?")
    bullet_p("Bitacoras en papel", "Presentan letra ilegible, propensas al desgaste fisico, firmas falsificables y nula posibilidad de busqueda automatizada o auditoria inmediata.")
    bullet_p("Hojas de calculo (Excel local)", "Requieren captura manual lenta en la PC del encargado. No se actualizan al instante si hay varios laboratoristas o turnos, y los alumnos no tienen visibilidad de si un componente esta libre sin tener que formarse en mostrador.")
    bullet_p("Carencia de notificaciones activas", "No existe ningun mecanismo automatico que le recuerde al estudiante que su horario de practica ha concluido o que debe entregar el material antes de salir del campus, lo que provoca retenciones involuntarias de dias enteros.")

    pdf.ln(2)

    # 2. Propuesta de Valor y Solucion
    section_header("2", "PROPUESTA DE VALOR Y SOLUCION")
    
    sub_header("2.1 ¿Como resuelve su aplicacion el problema antes mencionado? (Descripcion conceptual)")
    body_p("LabPass QR es un ecosistema movil disenado para agilizar radicalmente el prestamo y resguardo de inventario en laboratorios escolares. La aplicacion asigna un identificador QR unico tanto a cada recurso fisico (cables, osciloscopios, kits de sensores, computadoras) como a la credencial digital de cada estudiante matriculado.")
    body_p("Al momento del prestamo, el laboratorista o el propio alumno escanea el codigo QR del material con la camara de su dispositivo movil, vinculando instantaneamente el activo con la sesion del alumno en la nube en menos de 5 segundos. La aplicacion gestiona temporizadores en tiempo real y emite confirmaciones digitales de entrega y recepcion.")

    sub_header("2.2 ¿Cual es el factor diferenciador (propuesta de valor)?")
    bullet_p("Check-in/Check-out ultra rapido con camara", "Elimina filas en ventanilla al reducir el registro de prestamos de 2 minutos por persona a solo unos segundos mediante lectura nativa de codigo QR.")
    bullet_p("Visibilidad en tiempo real para el estudiante", "El alumno puede consultar desde el aula si hay equipo disponible antes de desplazarse hasta el almacen o laboratorio.")
    bullet_p("Trazabilidad y evidencia visual", "Permite registrar fotos del estado fisico del equipo tanto al recibirlo como al entregarlo, deslindando responsabilidades ante danos o faltantes.")

    # ---------------------------------------------
    # PAGINA 3: SECCIONES 3, 4 Y 5
    # ---------------------------------------------
    pdf.add_page()
    
    # 3. Perfil del Usuario y Segmento de Mercado
    section_header("3", "PERFIL DEL USUARIO Y SEGMENTO DE MERCADO")
    
    sub_header("3.1 ¿Quien es el usuario final y quien es el cliente? (User Persona)")
    body_p("Se identifican claramente dos perfiles complementarios dentro del entorno universitario:")
    bullet_p("Usuario Final 1 (El Alumno)", "Estudiantes universitarios (18-24 anos) que requieren equipo para practicas y proyectos. Su prioridad es rapidez, no perder tiempo en filas y tener un comprobante digital en su telefono que acredite que devolvio el equipo en orden.")
    bullet_p("Usuario Final 2 (El Encargado)", "Personal tecnico y docente responsable del resguardo del inventario. Requiere control estricto, saber quien tiene cada articulo, que esta por vencer y reportar fallas de forma rapida.")
    bullet_p("El Cliente", "La direccion de carrera o coordinacion de laboratorios de la universidad, interesada en optimizar la preservacion del patrimonio universitario, reducir mermas y digitalizar la operacion academica.")

    sub_header("3.2 ¿En que entorno o situacion se utilizara principalmente la aplicacion?")
    body_p("Se utilizara en movilidad dentro del campus universitario: directamente en los mostradores de recepcion de laboratorios, talleres de mecatronica/electronica y aulas de clase durante los cambios de horario y sesiones practicas.")

    pdf.ln(1)

    # 4. Alcance Inicial (El MVP - Producto Minimo Viable)
    section_header("4", "ALCANCE INICIAL (MVP - PRODUCTO MINIMO VIABLE)")
    
    sub_header("4.1 Las 3 funcionalidades principales (Core Features) indispensables:")
    bullet_p("1. Escaneo y Vinculacion Instantanea QR", "Modulo nativo para leer el codigo del material y la credencial del alumno, registrando fecha, hora, estado y responsable del prestamo con un solo toque.")
    bullet_p("2. Catalogo Dinamico de Disponibilidad", "Listado categorizado de materiales y kits disponibles en tiempo real, indicando si un activo esta 'Libre', 'En Prestamo' o 'En Mantenimiento'.")
    bullet_p("3. Modulo de Devolucion y Registro de Incidencias", "Cierre del prestamo mediante re-escaneo con confirmacion mutua y capacidad de registrar notas rapidas sobre el estado o faltantes.")

    sub_header("4.2 Funciones descartadas deliberadamente para el lanzamiento inicial:")
    bullet_p("Modulo de cobro de multas o sanciones", "No se integraran pasarelas de pago ni cargos monetarios para no complejizar la regulacion legal y financiera.")
    bullet_p("Lectores RFID o hardware externo especializado", "Se limitara exclusivamente a codigos QR generados por software y legibles con la camara del smartphone.")
    bullet_p("Reservaciones anticipadas para fechas lejanas", "En el MVP el prestamo sera de asignacion inmediata en ventanilla para asegurar consistencia del stock fisico.")

    pdf.ln(1)

    # 5. Viabilidad Tecnica Preliminar
    section_header("5", "VIABILIDAD TECNICA PRELIMINAR")
    
    sub_header("5.1 ¿Bajo que arquitectura o enfoque tecnologico estiman desarrollarla?")
    bullet_p("Frontend Movil", "Framework multiplataforma Flutter (Dart) o React Native, garantizando rendimiento nativo fluido en Android/iOS con arquitectura modular por capas (separacion limpia entre UI, logica y datos).")
    bullet_p("Backend y Base de Datos", "Firebase (Cloud Firestore + Firebase Authentication) o Supabase (PostgreSQL), garantizando sincronizacion en tiempo real y autenticacion segura de usuarios.")

    sub_header("5.2 ¿Que integraciones criticas o servicios de terceros requerira la aplicacion?")
    bullet_p("Sensor de Camara y Libreria de Escaneo", "Integracion de APIs de lectura de codigos de barra/QR (Mobile Scanner / Google ML Kit) de baja latencia.")
    bullet_p("Notificaciones Push (FCM)", "Envio de alertas automatizadas al telefono del alumno cuando su tiempo limite de entrega este proximo a expirar.")
    bullet_p("Cache y Almacenamiento Local (Offline)", "Persistencia temporal en el dispositivo para operar de forma confiable aun con senal Wi-Fi debil en zonas de talleres.")

    pdf.output(output_path)
    print(f"PDF generado exitosamente en: {output_path}")

if __name__ == "__main__":
    out = "c:\\Users\\galan\\OneDrive - Universidad Tecnológica de Salamanca\\Aplicación\\Inicio_Proyecto_APP_LabPassQR.pdf"
    create_full_pdf(out)
