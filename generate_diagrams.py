import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_screen_flow_diagram(output_path):
    fig, ax = plt.subplots(figsize=(12, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background canvas
    bg_box = patches.FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=1,rounding_size=2",
                                    facecolor="#F8FAFC", edgecolor="#E2E8F0", linewidth=1.5)
    ax.add_patch(bg_box)

    # Title header
    ax.text(50, 96, "MAPA DE NAVEGACIÓN Y FLUJO DE PANTALLAS (LABPASS QR)",
            fontsize=13, fontweight='bold', ha='center', va='center', color="#0F4C81", fontfamily='sans-serif')
    ax.text(50, 93.5, "Estructura de Vistas, Permisos por Rol y Transiciones de Usuario",
            fontsize=9.5, style='italic', ha='center', va='center', color="#64748B", fontfamily='sans-serif')

    # Common flow
    # 1. Splash Screen
    box_splash = patches.FancyBboxPatch((40, 83), 20, 7, boxstyle="round,pad=0.5,rounding_size=1",
                                       facecolor="#0F4C81", edgecolor="#0A2E50", linewidth=1)
    ax.add_patch(box_splash)
    ax.text(50, 87.2, "1. Splash Screen", fontsize=10, fontweight='bold', ha='center', va='center', color="white")
    ax.text(50, 84.8, "Carga de Sesión & Logo UTS", fontsize=7.5, ha='center', va='center', color="#BFDBFE")

    # Arrow Splash -> Login
    ax.annotate("", xy=(50, 76), xytext=(50, 83),
                arrowprops=dict(arrowstyle="->", color="#0F4C81", lw=2))

    # 2. Login UTS
    box_login = patches.FancyBboxPatch((37.5, 69), 25, 7, boxstyle="round,pad=0.5,rounding_size=1",
                                      facecolor="#FFFFFF", edgecolor="#0F4C81", linewidth=2)
    ax.add_patch(box_login)
    ax.text(50, 73.2, "2. Login / Auth UTS", fontsize=10, fontweight='bold', ha='center', va='center', color="#0F4C81")
    ax.text(50, 70.8, "Credenciales Universitarias (RBAC)", fontsize=7.5, ha='center', va='center', color="#475569")

    # Branch arrows
    # Left: Alumno
    ax.annotate("", xy=(24, 61), xytext=(40, 69),
                arrowprops=dict(arrowstyle="->", color="#00AE9D", lw=2, linestyle="--"))
    ax.text(28, 66.5, "Rol: Alumno", fontsize=8.5, fontweight='bold', color="#0F766E", ha='center')

    # Right: Laboratorista
    ax.annotate("", xy=(76, 61), xytext=(60, 69),
                arrowprops=dict(arrowstyle="->", color="#F58220", lw=2, linestyle="--"))
    ax.text(72, 66.5, "Rol: Laboratorista", fontsize=8.5, fontweight='bold', color="#C2410C", ha='center')

    # Container Alumno (Left)
    c_alum = patches.FancyBboxPatch((3, 5), 44, 55, boxstyle="round,pad=0.8,rounding_size=2",
                                    facecolor="#F0FDFA", edgecolor="#99F6E4", linewidth=1.5)
    ax.add_patch(c_alum)
    ax.text(25, 57.5, "MODO ESTUDIANTE (VISTAS)", fontsize=10, fontweight='bold', ha='center', va='center', color="#0F766E")

    # 3A Dashboard Alumno
    b_3a = patches.FancyBboxPatch((7, 49), 36, 6, boxstyle="round,pad=0.4,rounding_size=1",
                                  facecolor="#00AE9D", edgecolor="#0F766E", linewidth=1)
    ax.add_patch(b_3a)
    ax.text(25, 52.8, "3A. Dashboard del Estudiante", fontsize=9, fontweight='bold', ha='center', va='center', color="white")
    ax.text(25, 50.5, "Resumen, Atajos & Estado de Solicitudes", fontsize=7, ha='center', va='center', color="#CCFBF1")

    # Sub-views Alumno
    # 4A Credencial QR
    b_4a = patches.FancyBboxPatch((6, 39), 17, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#00AE9D", linewidth=1.2)
    ax.add_patch(b_4a)
    ax.text(14.5, 43.2, "4A. Credencial QR", fontsize=8, fontweight='bold', ha='center', va='center', color="#0F766E")
    ax.text(14.5, 40.8, "Código Dinámico", fontsize=6.8, ha='center', va='center', color="#64748B")

    # 4B Catálogo Stock
    b_4b = patches.FancyBboxPatch((27, 39), 18, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#00AE9D", linewidth=1.2)
    ax.add_patch(b_4b)
    ax.text(36, 43.2, "4B. Catálogo Stock", fontsize=8, fontweight='bold', ha='center', va='center', color="#0F766E")
    ax.text(36, 40.8, "Stock en Tiempo Real", fontsize=6.8, ha='center', va='center', color="#64748B")

    # Conexiones 3A -> 4A y 4B
    ax.annotate("", xy=(14.5, 45.5), xytext=(18, 49), arrowprops=dict(arrowstyle="->", color="#00AE9D", lw=1.2))
    ax.annotate("", xy=(36, 45.5), xytext=(32, 49), arrowprops=dict(arrowstyle="->", color="#00AE9D", lw=1.2))

    # 5A Detalle Insumo
    b_5a = patches.FancyBboxPatch((27, 29), 18, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#00AE9D", linewidth=1.2)
    ax.add_patch(b_5a)
    ax.text(36, 33.2, "5A. Detalle Activo", fontsize=8, fontweight='bold', ha='center', va='center', color="#0F766E")
    ax.text(36, 30.8, "Ficha Técnica & Guía", fontsize=6.8, ha='center', va='center', color="#64748B")
    ax.annotate("", xy=(36, 35.5), xytext=(36, 39), arrowprops=dict(arrowstyle="->", color="#00AE9D", lw=1.2))

    # 6A Préstamos Activos
    b_6a = patches.FancyBboxPatch((10, 19), 30, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#0F766E", linewidth=1.5)
    ax.add_patch(b_6a)
    ax.text(25, 23.2, "6A. Mis Préstamos Activos", fontsize=8.5, fontweight='bold', ha='center', va='center', color="#0F766E")
    ax.text(25, 20.8, "Temporizador de Entrega & Alertas FCM", fontsize=7, ha='center', va='center', color="#64748B")

    ax.annotate("", xy=(18, 25.5), xytext=(14.5, 39), arrowprops=dict(arrowstyle="->", color="#00AE9D", lw=1.2))
    ax.annotate("", xy=(32, 25.5), xytext=(36, 29), arrowprops=dict(arrowstyle="->", color="#00AE9D", lw=1.2))

    # 7A Comprobante Digital Criptográfico
    b_7a = patches.FancyBboxPatch((6, 8), 38, 7.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=1.5)
    ax.add_patch(b_7a)
    ax.text(25, 12.8, "★ 7A. Comprobante Digital No-Adeudo", fontsize=8.2, fontweight='bold', ha='center', va='center', color="#B45309")
    ax.text(25, 10.2, "Firma Criptográfica, PDF & Finiquito Escolar", fontsize=6.8, ha='center', va='center', color="#78350F")
    ax.annotate("", xy=(25, 15.5), xytext=(25, 19), arrowprops=dict(arrowstyle="->", color="#F59E0B", lw=1.5))


    # Container Laboratorista (Right)
    c_lab = patches.FancyBboxPatch((53, 5), 44, 55, boxstyle="round,pad=0.8,rounding_size=2",
                                   facecolor="#FFFBEB", edgecolor="#FDE68A", linewidth=1.5)
    ax.add_patch(c_lab)
    ax.text(75, 57.5, "MODO LABORATORISTA (GESTIÓN)", fontsize=10, fontweight='bold', ha='center', va='center', color="#C2410C")

    # 3B Dashboard Laboratorista
    b_3b = patches.FancyBboxPatch((57, 49), 36, 6, boxstyle="round,pad=0.4,rounding_size=1",
                                  facecolor="#F58220", edgecolor="#C2410C", linewidth=1)
    ax.add_patch(b_3b)
    ax.text(75, 52.8, "3B. Panel de Control Almacén", fontsize=9, fontweight='bold', ha='center', va='center', color="white")
    ax.text(75, 50.5, "Estatus de Mesas, Préstamos y Stock", fontsize=7, ha='center', va='center', color="#FEF3C7")

    # Sub-views Laboratorista
    # 4C Lector QR Cámara
    b_4c = patches.FancyBboxPatch((56, 39), 17, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#F58220", linewidth=1.5)
    ax.add_patch(b_4c)
    ax.text(64.5, 43.2, "4C. Lector QR Cámara", fontsize=8, fontweight='bold', ha='center', va='center', color="#C2410C")
    ax.text(64.5, 40.8, "Escaneo Dual Continuo", fontsize=6.8, ha='center', va='center', color="#64748B")

    # 4D Monitor de Préstamos
    b_4d = patches.FancyBboxPatch((77, 39), 18, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#F58220", linewidth=1.2)
    ax.add_patch(b_4d)
    ax.text(86, 43.2, "4D. Monitor Préstamos", fontsize=8, fontweight='bold', ha='center', va='center', color="#C2410C")
    ax.text(86, 40.8, "Semáforo de Devolución", fontsize=6.8, ha='center', va='center', color="#64748B")

    ax.annotate("", xy=(64.5, 45.5), xytext=(68, 49), arrowprops=dict(arrowstyle="->", color="#F58220", lw=1.2))
    ax.annotate("", xy=(86, 45.5), xytext=(82, 49), arrowprops=dict(arrowstyle="->", color="#F58220", lw=1.2))

    # 5B Confirmar Préstamo
    b_5b = patches.FancyBboxPatch((56, 29), 17, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#F58220", linewidth=1.2)
    ax.add_patch(b_5b)
    ax.text(64.5, 33.2, "5B. Confirmar Salida", fontsize=8, fontweight='bold', ha='center', va='center', color="#C2410C")
    ax.text(64.5, 30.8, "Asignación < 3 seg", fontsize=6.8, ha='center', va='center', color="#64748B")
    ax.annotate("", xy=(64.5, 35.5), xytext=(64.5, 39), arrowprops=dict(arrowstyle="->", color="#F58220", lw=1.2))

    # 6B Recepción & Incidencias
    b_6b = patches.FancyBboxPatch((60, 19), 30, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#C2410C", linewidth=1.5)
    ax.add_patch(b_6b)
    ax.text(75, 23.2, "6B. Devolución & Foto Daños", fontsize=8.5, fontweight='bold', ha='center', va='center', color="#C2410C")
    ax.text(75, 20.8, "Finiquito, Evidencia Cámara e Incidencias", fontsize=7, ha='center', va='center', color="#64748B")

    ax.annotate("", xy=(68, 25.5), xytext=(64.5, 29), arrowprops=dict(arrowstyle="->", color="#F58220", lw=1.2))
    ax.annotate("", xy=(82, 25.5), xytext=(86, 39), arrowprops=dict(arrowstyle="->", color="#F58220", lw=1.2))

    # 7B Administración de Inventario
    b_7b = patches.FancyBboxPatch((60, 8), 30, 7.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=1.5)
    ax.add_patch(b_7b)
    ax.text(75, 12.8, "7B. Inventario & Catálogo", fontsize=8.2, fontweight='bold', ha='center', va='center', color="#1E40AF")
    ax.text(75, 10.2, "Alta de Insumos, Bajas y Códigos QR", fontsize=6.8, ha='center', va='center', color="#475569")
    ax.annotate("", xy=(75, 15.5), xytext=(75, 19), arrowprops=dict(arrowstyle="->", color="#3B82F6", lw=1.5))

    # Cross connection: 6B triggers 7A
    ax.annotate("", xy=(44, 12), xytext=(60, 22),
                arrowprops=dict(arrowstyle="->", color="#10B981", lw=2, linestyle=":"))
    ax.text(51, 17, "Sincronización en Vivo", fontsize=7.5, fontweight='bold', color="#059669", ha='center', rotation=-28)

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Diagrama de flujo generado: {output_path}")

def generate_architecture_diagram(output_path):
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background canvas
    bg_box = patches.FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=1,rounding_size=2",
                                    facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.5)
    ax.add_patch(bg_box)

    # Title header
    ax.text(50, 95.5, "ARQUITECTURA DE SOFTWARE LIMPIA (CLEAN ARCHITECTURE + BaaS)",
            fontsize=13, fontweight='bold', ha='center', va='center', color="#0F4C81", fontfamily='sans-serif')
    ax.text(50, 93, "Estructura por Capas, Desacoplamiento y Estrategia Offline-First en LabPass QR",
            fontsize=9.5, style='italic', ha='center', va='center', color="#64748B", fontfamily='sans-serif')

    # LAYER 1: PRESENTATION LAYER
    l1 = patches.FancyBboxPatch((4, 65), 92, 24, boxstyle="round,pad=0.8,rounding_size=1.5",
                                facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=1.8)
    ax.add_patch(l1)
    ax.text(7, 85.5, "1. CAPA DE PRESENTACIÓN (FLUTTER 3.x UI / UX)", fontsize=10.5, fontweight='bold', color="#1E40AF")
    ax.text(7, 82.5, "Vistas reactivas, componentes Material Design 3, navegación GoRouter y controladores de estado BLoC",
            fontsize=8, color="#475569")

    # Boxes inside Layer 1
    p1 = patches.FancyBboxPatch((7, 68), 20, 11, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#BFDBFE")
    ax.add_patch(p1)
    ax.text(17, 74.5, "Vistas Estudiante", fontsize=8.5, fontweight='bold', color="#1D4ED8", ha='center')
    ax.text(17, 71, "Credencial, Stock, Historial", fontsize=7, color="#64748B", ha='center')

    p2 = patches.FancyBboxPatch((29, 68), 20, 11, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#BFDBFE")
    ax.add_patch(p2)
    ax.text(39, 74.5, "Vistas Laboratorista", fontsize=8.5, fontweight='bold', color="#1D4ED8", ha='center')
    ax.text(39, 71, "Panel Almacén, Inventario", fontsize=7, color="#64748B", ha='center')

    p3 = patches.FancyBboxPatch((51, 68), 21, 11, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#BFDBFE")
    ax.add_patch(p3)
    ax.text(61.5, 74.5, "Mobile Scanner Overlay", fontsize=8.5, fontweight='bold', color="#1D4ED8", ha='center')
    ax.text(61.5, 71, "Visor de Enfoque Cámara QR", fontsize=7, color="#64748B", ha='center')

    p4 = patches.FancyBboxPatch((74, 68), 19, 11, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#BFDBFE")
    ax.add_patch(p4)
    ax.text(83.5, 74.5, "State Management", fontsize=8.5, fontweight='bold', color="#1D4ED8", ha='center')
    ax.text(83.5, 71, "BLoC / Riverpod Notifiers", fontsize=7, color="#64748B", ha='center')

    # Arrow Layer 1 -> Layer 2
    ax.annotate("", xy=(50, 60), xytext=(50, 65), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2.5))

    # LAYER 2: DOMAIN LAYER
    l2 = patches.FancyBboxPatch((4, 36), 92, 23, boxstyle="round,pad=0.8,rounding_size=1.5",
                                facecolor="#F0FDF4", edgecolor="#10B981", linewidth=1.8)
    ax.add_patch(l2)
    ax.text(7, 55.5, "2. CAPA DE DOMINIO (CORE EMPRESARIAL PURO)", fontsize=10.5, fontweight='bold', color="#065F46")
    ax.text(7, 52.5, "Lógica de negocio independiente de frameworks, UI o bases de datos (Reglas puras de validación)",
            fontsize=8, color="#475569")

    # Boxes inside Layer 2
    d1 = patches.FancyBboxPatch((7, 39), 20, 10.5, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#A7F3D0")
    ax.add_patch(d1)
    ax.text(17, 45, "RegistrarPrestamo", fontsize=8.2, fontweight='bold', color="#047857", ha='center')
    ax.text(17, 42, "UseCase (Validar Stock)", fontsize=7, color="#64748B", ha='center')

    d2 = patches.FancyBboxPatch((29, 39), 20, 10.5, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#A7F3D0")
    ax.add_patch(d2)
    ax.text(39, 45, "DevolverActivo", fontsize=8.2, fontweight='bold', color="#047857", ha='center')
    ax.text(39, 42, "UseCase (Foto e Incidencia)", fontsize=7, color="#64748B", ha='center')

    d3 = patches.FancyBboxPatch((51, 39), 21, 10.5, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#A7F3D0")
    ax.add_patch(d3)
    ax.text(61.5, 45, "ConsultarStockEnVivo", fontsize=8.2, fontweight='bold', color="#047857", ha='center')
    ax.text(61.5, 42, "UseCase (Stream Firestore)", fontsize=7, color="#64748B", ha='center')

    d4 = patches.FancyBboxPatch((74, 39), 19, 10.5, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#A7F3D0")
    ax.add_patch(d4)
    ax.text(83.5, 45, "Entities & Contracts", fontsize=8.2, fontweight='bold', color="#047857", ha='center')
    ax.text(83.5, 42, "Préstamo, Activo, User", fontsize=7, color="#64748B", ha='center')

    # Arrow Layer 2 -> Layer 3
    ax.annotate("", xy=(50, 31), xytext=(50, 36), arrowprops=dict(arrowstyle="->", color="#10B981", lw=2.5))

    # LAYER 3: DATA LAYER
    l3 = patches.FancyBboxPatch((4, 4), 92, 26, boxstyle="round,pad=0.8,rounding_size=1.5",
                                facecolor="#FFFBEB", edgecolor="#F58220", linewidth=1.8)
    ax.add_patch(l3)
    ax.text(7, 26.5, "3. CAPA DE DATOS & INFRAESTRUCTURA (OFFLINE-FIRST + CLOUD BaaS)", fontsize=10.5, fontweight='bold', color="#92400E")
    ax.text(7, 23.5, "Implementación del Repositorio: Almacenamiento local resiliente con sincronización en la nube",
            fontsize=8, color="#475569")

    # Local DataSource
    b_local = patches.FancyBboxPatch((7, 7), 26, 14, boxstyle="round,pad=0.4,rounding_size=1", facecolor="white", edgecolor="#FDE68A")
    ax.add_patch(b_local)
    ax.text(20, 16.5, "Local DataSource (Offline)", fontsize=8.5, fontweight='bold', color="#B45309", ha='center')
    ax.text(20, 13.5, "Caché Local Hive / SQLite", fontsize=7.2, color="#475569", ha='center')
    ax.text(20, 10.5, "Cola de transacciones offline", fontsize=6.8, style='italic', color="#78350F", ha='center')

    # Repository Mediator
    b_repo = patches.FancyBboxPatch((37, 7), 26, 14, boxstyle="round,pad=0.4,rounding_size=1", facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.5)
    ax.add_patch(b_repo)
    ax.text(50, 16.5, "PrestamosRepositoryImpl", fontsize=8.8, fontweight='bold', color="#0F4C81", ha='center')
    ax.text(50, 13.5, "Árbitro de Persistencia", fontsize=7.5, color="#334155", ha='center')
    ax.text(50, 10.5, "¿Hay conexión? Nube : Local", fontsize=7, color="#059669", ha='center')

    # Remote DataSource
    b_remote = patches.FancyBboxPatch((67, 7), 26, 14, boxstyle="round,pad=0.4,rounding_size=1", facecolor="white", edgecolor="#FDE68A")
    ax.add_patch(b_remote)
    ax.text(80, 16.5, "Remote DataSource (BaaS)", fontsize=8.5, fontweight='bold', color="#B45309", ha='center')
    ax.text(80, 13.5, "Firebase Cloud Firestore", fontsize=7.2, color="#475569", ha='center')
    ax.text(80, 10.5, "Firebase Auth • FCM • Storage", fontsize=6.8, color="#78350F", ha='center')

    # Connections inside Data Layer
    ax.annotate("", xy=(37, 14), xytext=(33, 14), arrowprops=dict(arrowstyle="<->", color="#B45309", lw=1.5))
    ax.annotate("", xy=(67, 14), xytext=(63, 14), arrowprops=dict(arrowstyle="<->", color="#B45309", lw=1.5))

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Diagrama de arquitectura generado: {output_path}")

if __name__ == "__main__":
    generate_screen_flow_diagram("diagram_flujo_pantallas.png")
    generate_architecture_diagram("diagram_arquitectura_capas.png")
