import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_screen_flow_savebite(output_path):
    fig, ax = plt.subplots(figsize=(12, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Canvas de fondo
    bg_box = patches.FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=1,rounding_size=2",
                                    facecolor="#F8FAFC", edgecolor="#E2E8F0", linewidth=1.5)
    ax.add_patch(bg_box)

    # Encabezado del Diagrama
    ax.text(50, 96, "MAPA DE NAVEGACIÓN Y FLUJO DE PANTALLAS (SAVEBITE)",
            fontsize=13, fontweight='bold', ha='center', va='center', color="#0F4C81", fontfamily='sans-serif')
    ax.text(50, 93.5, "Estructura de Vistas, Permisos por Perfil y Transiciones de Usuario (ODS 12: Cero Merma)",
            fontsize=9.5, style='italic', ha='center', va='center', color="#64748B", fontfamily='sans-serif')

    # Flujo Central / Inicio
    # 1. Splash Screen
    box_splash = patches.FancyBboxPatch((40, 83), 20, 7, boxstyle="round,pad=0.5,rounding_size=1",
                                       facecolor="#0F4C81", edgecolor="#0A2E50", linewidth=1)
    ax.add_patch(box_splash)
    ax.text(50, 87.2, "1. Splash Screen", fontsize=10, fontweight='bold', ha='center', va='center', color="white")
    ax.text(50, 84.8, "Carga de Sesión & Logo SaveBite", fontsize=7.5, ha='center', va='center', color="#BFDBFE")

    # Flecha Splash -> Login
    ax.annotate("", xy=(50, 76), xytext=(50, 83),
                arrowprops=dict(arrowstyle="->", color="#0F4C81", lw=2))

    # 2. Login & Onboarding
    box_login = patches.FancyBboxPatch((36, 69), 28, 7, boxstyle="round,pad=0.5,rounding_size=1",
                                      facecolor="#FFFFFF", edgecolor="#0F4C81", linewidth=2)
    ax.add_patch(box_login)
    ax.text(50, 73.2, "2. Login / Registro / Auth", fontsize=10, fontweight='bold', ha='center', va='center', color="#0F4C81")
    ax.text(50, 70.8, "Acceso Alumno / Comercio Aliado", fontsize=7.5, ha='center', va='center', color="#475569")

    # Bifurcación por Roles
    # Izquierda: Consumidor / Estudiante
    ax.annotate("", xy=(24, 61), xytext=(39, 69),
                arrowprops=dict(arrowstyle="->", color="#10B981", lw=2, linestyle="--"))
    ax.text(28, 66.5, "Rol: Consumidor", fontsize=8.5, fontweight='bold', color="#047857", ha='center')

    # Derecha: Comercio Aliado (Panadería, Frutería, etc.)
    ax.annotate("", xy=(76, 61), xytext=(61, 69),
                arrowprops=dict(arrowstyle="->", color="#F58220", lw=2, linestyle="--"))
    ax.text(72, 66.5, "Rol: Comercio Aliado", fontsize=8.5, fontweight='bold', color="#C2410C", ha='center')

    # =================== CONTENEDOR ROL CONSUMIDOR (IZQUIERDA) ===================
    c_user = patches.FancyBboxPatch((3, 5), 44, 55, boxstyle="round,pad=0.8,rounding_size=2",
                                    facecolor="#F0FDF4", edgecolor="#A7F3D0", linewidth=1.5)
    ax.add_patch(c_user)
    ax.text(25, 57.5, "MODO CONSUMIDOR (ESTUDIANTE / USUARIO)", fontsize=9.5, fontweight='bold', ha='center', va='center', color="#047857")

    # 3A. Dashboard & Mapa Interactivo GPS
    b_3a = patches.FancyBboxPatch((7, 49), 36, 6, boxstyle="round,pad=0.4,rounding_size=1",
                                  facecolor="#10B981", edgecolor="#047857", linewidth=1)
    ax.add_patch(b_3a)
    ax.text(25, 52.8, "3A. Mapa GPS & Feed de Ofertas", fontsize=8.8, fontweight='bold', ha='center', va='center', color="white")
    ax.text(25, 50.5, "Geolocalización en Vivo y Comercios Cercanos", fontsize=6.8, ha='center', va='center', color="#D1FAE5")

    # Sub-vistas Consumidor
    # 4A. Detalle de Paquete Sorpresa
    b_4a = patches.FancyBboxPatch((6, 39), 17, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#10B981", linewidth=1.2)
    ax.add_patch(b_4a)
    ax.text(14.5, 43.2, "4A. Ficha Paquete", fontsize=8, fontweight='bold', ha='center', va='center', color="#047857")
    ax.text(14.5, 40.8, "Horario, Precio & -60%", fontsize=6.8, ha='center', va='center', color="#64748B")

    # 4B. Favoritos & Alertas Push
    b_4b = patches.FancyBboxPatch((27, 39), 18, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#10B981", linewidth=1.2)
    ax.add_patch(b_4b)
    ax.text(36, 43.2, "4B. Tiendas Favoritas", fontsize=8, fontweight='bold', ha='center', va='center', color="#047857")
    ax.text(36, 40.8, "Alertas Inmediatas FCM", fontsize=6.8, ha='center', va='center', color="#64748B")

    ax.annotate("", xy=(14.5, 45.5), xytext=(18, 49), arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.2))
    ax.annotate("", xy=(36, 45.5), xytext=(32, 49), arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.2))

    # 5A. Checkout & Reserva con 1 Toque
    b_5a = patches.FancyBboxPatch((6, 29), 17, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#10B981", linewidth=1.2)
    ax.add_patch(b_5a)
    ax.text(14.5, 33.2, "5A. Reserva & Pago", fontsize=8, fontweight='bold', ha='center', va='center', color="#047857")
    ax.text(14.5, 30.8, "Reserva Directa In-App", fontsize=6.8, ha='center', va='center', color="#64748B")
    ax.annotate("", xy=(14.5, 35.5), xytext=(14.5, 39), arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.2))

    # 6A. Voucher Digital con Código QR Dinámico
    b_6a = patches.FancyBboxPatch((7, 19), 36, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#047857", linewidth=1.5)
    ax.add_patch(b_6a)
    ax.text(25, 23.2, "6A. Voucher con Código QR Dinámico", fontsize=8.5, fontweight='bold', ha='center', va='center', color="#047857")
    ax.text(25, 20.8, "Token de Canje, Temporizador & Modo Offline", fontsize=7, ha='center', va='center', color="#64748B")
    ax.annotate("", xy=(25, 25.5), xytext=(14.5, 29), arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.2))

    # 7A. Impacto Ecológico y Ahorro CO2 (Adicional)
    b_7a = patches.FancyBboxPatch((6, 8), 38, 7.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=1.5)
    ax.add_patch(b_7a)
    ax.text(25, 12.8, "★ 7A. Calculadora de Impacto ODS", fontsize=8.2, fontweight='bold', ha='center', va='center', color="#B45309")
    ax.text(25, 10.2, "Kg de Comida Rescatada, CO2 Evitado & Ahorro ($)", fontsize=6.8, ha='center', va='center', color="#78350F")
    ax.annotate("", xy=(25, 15.5), xytext=(25, 19), arrowprops=dict(arrowstyle="->", color="#F59E0B", lw=1.5))


    # =================== CONTENEDOR ROL COMERCIO (DERECHA) ===================
    c_store = patches.FancyBboxPatch((53, 5), 44, 55, boxstyle="round,pad=0.8,rounding_size=2",
                                     facecolor="#FFFBEB", edgecolor="#FDE68A", linewidth=1.5)
    ax.add_patch(c_store)
    ax.text(75, 57.5, "MODO COMERCIO (PANADERÍA / CAFETERÍA)", fontsize=9.5, fontweight='bold', ha='center', va='center', color="#C2410C")

    # 3B. Panel de Control del Establecimiento
    b_3b = patches.FancyBboxPatch((57, 49), 36, 6, boxstyle="round,pad=0.4,rounding_size=1",
                                  facecolor="#F58220", edgecolor="#C2410C", linewidth=1)
    ax.add_patch(b_3b)
    ax.text(75, 52.8, "3B. Panel del Establecimiento", fontsize=8.8, fontweight='bold', ha='center', va='center', color="white")
    ax.text(75, 50.5, "Gestión de Paquetes Activos y Ventas del Día", fontsize=6.8, ha='center', va='center', color="#FEF3C7")

    # Sub-vistas Comercio
    # 4C. Publicación Express de Paquetes Sorpresa
    b_4c = patches.FancyBboxPatch((56, 39), 17, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#F58220", linewidth=1.5)
    ax.add_patch(b_4c)
    ax.text(64.5, 43.2, "4C. Publicar Pack", fontsize=8, fontweight='bold', ha='center', va='center', color="#C2410C")
    ax.text(64.5, 40.8, "Cantidad & Ventana Horaria", fontsize=6.8, ha='center', va='center', color="#64748B")

    # 4D. Monitor de Reservas Activas
    b_4d = patches.FancyBboxPatch((77, 39), 18, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#F58220", linewidth=1.2)
    ax.add_patch(b_4d)
    ax.text(86, 43.2, "4D. Pedidos en Cola", fontsize=8, fontweight='bold', ha='center', va='center', color="#C2410C")
    ax.text(86, 40.8, "Vouchers por Canjear", fontsize=6.8, ha='center', va='center', color="#64748B")

    ax.annotate("", xy=(64.5, 45.5), xytext=(68, 49), arrowprops=dict(arrowstyle="->", color="#F58220", lw=1.2))
    ax.annotate("", xy=(86, 45.5), xytext=(82, 49), arrowprops=dict(arrowstyle="->", color="#F58220", lw=1.2))

    # 5B. Lector QR de Cámara para Validación
    b_5b = patches.FancyBboxPatch((56, 29), 17, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#F58220", linewidth=1.2)
    ax.add_patch(b_5b)
    ax.text(64.5, 33.2, "5B. Escáner QR Cámara", fontsize=7.8, fontweight='bold', ha='center', va='center', color="#C2410C")
    ax.text(64.5, 30.8, "Validación en < 2 seg", fontsize=6.8, ha='center', va='center', color="#64748B")
    ax.annotate("", xy=(64.5, 35.5), xytext=(64.5, 39), arrowprops=dict(arrowstyle="->", color="#F58220", lw=1.2))

    # 6B. Confirmación de Entrega & Liquidación
    b_6b = patches.FancyBboxPatch((57, 19), 36, 6.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#C2410C", linewidth=1.5)
    ax.add_patch(b_6b)
    ax.text(75, 23.2, "6B. Confirmación & Entrega de Pack", fontsize=8.5, fontweight='bold', ha='center', va='center', color="#C2410C")
    ax.text(75, 20.8, "Finiquito de Reserva y Stock Actualizado", fontsize=7, ha='center', va='center', color="#64748B")

    ax.annotate("", xy=(68, 25.5), xytext=(64.5, 29), arrowprops=dict(arrowstyle="->", color="#F58220", lw=1.2))
    ax.annotate("", xy=(82, 25.5), xytext=(86, 39), arrowprops=dict(arrowstyle="->", color="#F58220", lw=1.2))

    # 7B. Métricas de Rescate de Merma y Ganancias
    b_7b = patches.FancyBboxPatch((57, 8), 36, 7.5, boxstyle="round,pad=0.3,rounding_size=1",
                                  facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=1.5)
    ax.add_patch(b_7b)
    ax.text(75, 12.8, "7B. Reportes de Merma & Finanzas", fontsize=8.2, fontweight='bold', ha='center', va='center', color="#1E40AF")
    ax.text(75, 10.2, "Ingresos Recuperados y Residuos Mitigados", fontsize=6.8, ha='center', va='center', color="#475569")
    ax.annotate("", xy=(75, 15.5), xytext=(75, 19), arrowprops=dict(arrowstyle="->", color="#3B82F6", lw=1.5))

    # Conexión transversal: 6A Voucher escaneado por 5B / 6B
    ax.annotate("", xy=(56, 32), xytext=(43, 23),
                arrowprops=dict(arrowstyle="->", color="#F58220", lw=2, linestyle=":"))
    ax.text(50, 27, "Escaneo QR en Mostrador", fontsize=7.5, fontweight='bold', color="#C2410C", ha='center', rotation=30)

    # Conexión transversal: 6B actualiza impacto 7A
    ax.annotate("", xy=(44, 12), xytext=(57, 22),
                arrowprops=dict(arrowstyle="->", color="#10B981", lw=2, linestyle=":"))
    ax.text(51, 16.5, "Suma Impacto ODS", fontsize=7.5, fontweight='bold', color="#047857", ha='center', rotation=-28)

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Diagrama de flujo SaveBite generado: {output_path}")

def generate_architecture_savebite(output_path):
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Canvas de fondo
    bg_box = patches.FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=1,rounding_size=2",
                                    facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.5)
    ax.add_patch(bg_box)

    # Título del Diagrama
    ax.text(50, 95.5, "ARQUITECTURA DE SOFTWARE LIMPIA (CLEAN ARCHITECTURE + BaaS)",
            fontsize=13, fontweight='bold', ha='center', va='center', color="#0F4C81", fontfamily='sans-serif')
    ax.text(50, 93, "Estructura por Capas, Servicios de Geolocalización y Persistencia Offline en SaveBite",
            fontsize=9.5, style='italic', ha='center', va='center', color="#64748B", fontfamily='sans-serif')

    # CAPA 1: PRESENTACIÓN (FLUTTER 3.x UI / UX)
    l1 = patches.FancyBboxPatch((4, 65), 92, 24, boxstyle="round,pad=0.8,rounding_size=1.5",
                                facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=1.8)
    ax.add_patch(l1)
    ax.text(7, 85.5, "1. CAPA DE PRESENTACIÓN (FLUTTER 3.x / DART UI)", fontsize=10.5, fontweight='bold', color="#1E40AF")
    ax.text(7, 82.5, "Interfaces reactivas Material Design 3, integración con Google Maps SDK, lector de cámara y gestores de estado BLoC",
            fontsize=8, color="#475569")

    # Módulos UI
    p1 = patches.FancyBboxPatch((7, 68), 20, 11, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#BFDBFE")
    ax.add_patch(p1)
    ax.text(17, 74.5, "Vistas Consumidor", fontsize=8.5, fontweight='bold', color="#1D4ED8", ha='center')
    ax.text(17, 71, "Mapa GPS, Filtros, Packs", fontsize=7, color="#64748B", ha='center')

    p2 = patches.FancyBboxPatch((29, 68), 20, 11, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#BFDBFE")
    ax.add_patch(p2)
    ax.text(39, 74.5, "Vistas Comercio", fontsize=8.5, fontweight='bold', color="#1D4ED8", ha='center')
    ax.text(39, 71, "Publicador, Ventas, Stock", fontsize=7, color="#64748B", ha='center')

    p3 = patches.FancyBboxPatch((51, 68), 21, 11, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#BFDBFE")
    ax.add_patch(p3)
    ax.text(61.5, 74.5, "Map & Scanner Overlays", fontsize=8.5, fontweight='bold', color="#1D4ED8", ha='center')
    ax.text(61.5, 71, "Google Maps & Mobile Scanner", fontsize=7, color="#64748B", ha='center')

    p4 = patches.FancyBboxPatch((74, 68), 19, 11, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#BFDBFE")
    ax.add_patch(p4)
    ax.text(83.5, 74.5, "State Management", fontsize=8.5, fontweight='bold', color="#1D4ED8", ha='center')
    ax.text(83.5, 71, "BLoC / Riverpod Notifiers", fontsize=7, color="#64748B", ha='center')

    # Flecha Capa 1 -> Capa 2
    ax.annotate("", xy=(50, 60), xytext=(50, 65), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2.5))

    # CAPA 2: DOMINIO (CORE EMPRESARIAL PURO)
    l2 = patches.FancyBboxPatch((4, 36), 92, 23, boxstyle="round,pad=0.8,rounding_size=1.5",
                                facecolor="#F0FDF4", edgecolor="#10B981", linewidth=1.8)
    ax.add_patch(l2)
    ax.text(7, 55.5, "2. CAPA DE DOMINIO (CASOS DE USO PUROS Y ENTIDADES)", fontsize=10.5, fontweight='bold', color="#065F46")
    ax.text(7, 52.5, "Lógica de negocio pura de rescate de alimentos independiente de frameworks y SDKs (Altamente Testeable)",
            fontsize=8, color="#475569")

    # Módulos Dominio
    d1 = patches.FancyBboxPatch((7, 39), 20, 10.5, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#A7F3D0")
    ax.add_patch(d1)
    ax.text(17, 45, "ExplorarCercanos", fontsize=8.2, fontweight='bold', color="#047857", ha='center')
    ax.text(17, 42, "UseCase (Radio GPS km)", fontsize=7, color="#64748B", ha='center')

    d2 = patches.FancyBboxPatch((29, 39), 20, 10.5, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#A7F3D0")
    ax.add_patch(d2)
    ax.text(39, 45, "ReservarPaquete", fontsize=8.2, fontweight='bold', color="#047857", ha='center')
    ax.text(39, 42, "UseCase (Bloqueo de Stock)", fontsize=7, color="#64748B", ha='center')

    d3 = patches.FancyBboxPatch((51, 39), 21, 10.5, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#A7F3D0")
    ax.add_patch(d3)
    ax.text(61.5, 45, "ValidarEntregaQR", fontsize=8.2, fontweight='bold', color="#047857", ha='center')
    ax.text(61.5, 42, "UseCase (Finiquito de Token)", fontsize=7, color="#64748B", ha='center')

    d4 = patches.FancyBboxPatch((74, 39), 19, 10.5, boxstyle="round,pad=0.3,rounding_size=1", facecolor="white", edgecolor="#A7F3D0")
    ax.add_patch(d4)
    ax.text(83.5, 45, "CalcularImpactoODS", fontsize=8.2, fontweight='bold', color="#047857", ha='center')
    ax.text(83.5, 42, "UseCase (Métricas CO2)", fontsize=7, color="#64748B", ha='center')

    # Flecha Capa 2 -> Capa 3
    ax.annotate("", xy=(50, 31), xytext=(50, 36), arrowprops=dict(arrowstyle="->", color="#10B981", lw=2.5))

    # CAPA 3: DATOS Y PERSISTENCIA (OFFLINE + CLOUD BaaS)
    l3 = patches.FancyBboxPatch((4, 4), 92, 26, boxstyle="round,pad=0.8,rounding_size=1.5",
                                facecolor="#FFFBEB", edgecolor="#F58220", linewidth=1.8)
    ax.add_patch(l3)
    ax.text(7, 26.5, "3. CAPA DE DATOS & INFRAESTRUCTURA (OFFLINE-FIRST + CLOUD BaaS)", fontsize=10.5, fontweight='bold', color="#92400E")
    ax.text(7, 23.5, "Implementación del Repositorio: Caché local para vouchers y geolocalización geoespacial en la nube",
            fontsize=8, color="#475569")

    # Local DataSource
    b_local = patches.FancyBboxPatch((7, 7), 26, 14, boxstyle="round,pad=0.4,rounding_size=1", facecolor="white", edgecolor="#FDE68A")
    ax.add_patch(b_local)
    ax.text(20, 16.5, "Local DataSource (Offline)", fontsize=8.5, fontweight='bold', color="#B45309", ha='center')
    ax.text(20, 13.5, "Caché Hive / SQLite Local", fontsize=7.2, color="#475569", ha='center')
    ax.text(20, 10.5, "Vouchers QR activos sin internet", fontsize=6.8, style='italic', color="#78350F", ha='center')

    # Repositorio Mediador
    b_repo = patches.FancyBboxPatch((37, 7), 26, 14, boxstyle="round,pad=0.4,rounding_size=1", facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.5)
    ax.add_patch(b_repo)
    ax.text(50, 16.5, "SaveBiteRepositoryImpl", fontsize=8.8, fontweight='bold', color="#0F4C81", ha='center')
    ax.text(50, 13.5, "Árbitro de Persistencia", fontsize=7.5, color="#334155", ha='center')
    ax.text(50, 10.5, "Conexión ? Firestore : Local", fontsize=7, color="#059669", ha='center')

    # Remote DataSource
    b_remote = patches.FancyBboxPatch((67, 7), 26, 14, boxstyle="round,pad=0.4,rounding_size=1", facecolor="white", edgecolor="#FDE68A")
    ax.add_patch(b_remote)
    ax.text(80, 16.5, "Remote DataSource (BaaS)", fontsize=8.5, fontweight='bold', color="#B45309", ha='center')
    ax.text(80, 13.5, "Cloud Firestore + Geohash API", fontsize=7.2, color="#475569", ha='center')
    ax.text(80, 10.5, "Firebase Auth • FCM • Maps SDK", fontsize=6.8, color="#78350F", ha='center')

    # Conexiones internas
    ax.annotate("", xy=(37, 14), xytext=(33, 14), arrowprops=dict(arrowstyle="<->", color="#B45309", lw=1.5))
    ax.annotate("", xy=(67, 14), xytext=(63, 14), arrowprops=dict(arrowstyle="<->", color="#B45309", lw=1.5))

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Diagrama de arquitectura SaveBite generado: {output_path}")

if __name__ == "__main__":
    generate_screen_flow_savebite("diagram_flujo_pantallas_savebite.png")
    generate_architecture_savebite("diagram_arquitectura_capas_savebite.png")
