import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

def generate_patrones_diagram(output_path):
    fig, ax = plt.subplots(figsize=(12, 7.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Fondo general
    bg_box = patches.FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=1,rounding_size=2",
                                    facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.5)
    ax.add_patch(bg_box)

    # Título
    ax.text(50, 96, "ARQUITECTURA DE SOFTWARE Y PATRONES DE DISEÑO EN SAVEBITE",
            fontsize=13, fontweight='bold', ha='center', va='center', color="#0F4C81", fontfamily='sans-serif')
    ax.text(50, 93, "Integración de Clean Architecture, BLoC Pattern (Observer), Repository Pattern y Factory DTOs",
            fontsize=9.5, style='italic', ha='center', va='center', color="#64748B", fontfamily='sans-serif')

    # CAPA 1: PRESENTACIÓN (FLUTTER UI + BLOC)
    c1 = patches.FancyBboxPatch((4, 65), 92, 24, boxstyle="round,pad=0.8,rounding_size=1.5",
                                facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=1.8)
    ax.add_patch(c1)
    ax.text(7, 86, "1. CAPA DE PRESENTACIÓN (UI REACTIVA + BLOC PATTERN)", fontsize=9.5, fontweight='bold', color="#1D4ED8")
    
    # UI Widgets box
    b_ui = patches.FancyBboxPatch((6, 67), 28, 16, boxstyle="round,pad=0.5,rounding_size=1",
                                  facecolor="#FFFFFF", edgecolor="#93C5FD", linewidth=1.2)
    ax.add_patch(b_ui)
    ax.text(20, 80, "Flutter Widgets (Material 3)", fontsize=8.5, fontweight='bold', ha='center', color="#1E3A8A")
    ax.text(20, 75, "• ExplorerMapView\n• PackageCardList\n• DynamicQrVoucher\n• CameraScannerView", fontsize=7.2, ha='center', color="#475569")
    ax.text(20, 69, "Declarativo / Inmutable", fontsize=7, style='italic', ha='center', color="#2563EB")

    # Arrow UI -> Event -> BLoC
    ax.annotate("", xy=(39, 75), xytext=(35, 75), arrowprops=dict(arrowstyle="->", color="#3B82F6", lw=2))
    ax.text(37, 77.5, "Events", fontsize=7.5, fontweight='bold', ha='center', color="#1D4ED8")

    # BLoC Component Box
    b_bloc = patches.FancyBboxPatch((40, 67), 30, 16, boxstyle="round,pad=0.5,rounding_size=1",
                                    facecolor="#DBEAFE", edgecolor="#2563EB", linewidth=1.5)
    ax.add_patch(b_bloc)
    ax.text(55, 80, "BLoC Pattern (Observer)", fontsize=8.5, fontweight='bold', ha='center', color="#1E3A8A")
    ax.text(55, 75, "State Management Reactivo\nStreamController / RxDart\nFlujo Unidireccional (UDF)", fontsize=7.2, ha='center', color="#1E40AF")
    ax.text(55, 69, "Testable Unitario (bloc_test)", fontsize=7, style='italic', ha='center', color="#1D4ED8")

    # Arrow BLoC -> State -> UI
    ax.annotate("", xy=(35, 71), xytext=(39, 71), arrowprops=dict(arrowstyle="->", color="#10B981", lw=2))
    ax.text(37, 68.5, "States", fontsize=7.5, fontweight='bold', ha='center', color="#047857")

    # UseCases trigger Box
    b_trigger = patches.FancyBboxPatch((74, 67), 20, 16, boxstyle="round,pad=0.5,rounding_size=1",
                                       facecolor="#FFFFFF", edgecolor="#93C5FD", linewidth=1.2)
    ax.add_patch(b_trigger)
    ax.text(84, 78, "Invocación de\nCasos de Uso", fontsize=8, fontweight='bold', ha='center', color="#1E3A8A")
    ax.text(84, 71, "Async / Await\nEither<Failure, T>", fontsize=7.2, ha='center', color="#64748B")

    ax.annotate("", xy=(73, 75), xytext=(70.5, 75), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2))

    # FLECHA CAPA 1 -> CAPA 2
    ax.annotate("", xy=(50, 61), xytext=(50, 65), arrowprops=dict(arrowstyle="->", color="#0F4C81", lw=2.5))
    ax.text(55, 63, "Inyección de Dependencias (GetIt Service Locator)", fontsize=7.5, color="#0F4C81", fontweight='bold')

    # CAPA 2: DOMINIO (CASOS DE USO + ENTIDADES PURAS)
    c2 = patches.FancyBboxPatch((4, 38), 92, 22, boxstyle="round,pad=0.8,rounding_size=1.5",
                                facecolor="#F0FDF4", edgecolor="#10B981", linewidth=1.8)
    ax.add_patch(c2)
    ax.text(7, 57, "2. CAPA DE DOMINIO (REGLAS DE NEGOCIO PURAS - DART NATIVO)", fontsize=9.5, fontweight='bold', color="#047857")

    # Use Cases Boxes
    uc_list = [
        ("GetSurprisePackages", "Filtro radio GPS,\nstock y horarios"),
        ("ReservePackage", "Validación cupo,\nreserva atómica"),
        ("ValidateQrVoucher", "Verificación HMAC\ny registro canje"),
        ("CalculateODSImpact", "Cálculo kg merma\ny ahorro CO2e")
    ]
    for i, (uc_title, uc_desc) in enumerate(uc_list):
        bx = 6 + (i * 22.8)
        b_uc = patches.FancyBboxPatch((bx, 40), 21.5, 14, boxstyle="round,pad=0.4,rounding_size=1",
                                      facecolor="#FFFFFF", edgecolor="#6EE7B7", linewidth=1.2)
        ax.add_patch(b_uc)
        ax.text(bx + 10.75, 50.5, uc_title, fontsize=7.6, fontweight='bold', ha='center', color="#065F46")
        ax.text(bx + 10.75, 45, uc_desc, fontsize=6.8, ha='center', color="#374151")
        ax.text(bx + 10.75, 41.5, "Contrato Abstracto", fontsize=6.2, style='italic', ha='center', color="#059669")

    # FLECHA CAPA 2 -> CAPA 3
    ax.annotate("", xy=(50, 34), xytext=(50, 38), arrowprops=dict(arrowstyle="->", color="#0F4C81", lw=2.5))
    ax.text(55, 36, "Inversión de Dependencias (Dependency Inversion)", fontsize=7.5, color="#0F4C81", fontweight='bold')

    # CAPA 3: DATOS E INFRAESTRUCTURA (REPOSITORY PATTERN + FACTORY)
    c3 = patches.FancyBboxPatch((4, 4), 92, 29, boxstyle="round,pad=0.8,rounding_size=1.5",
                                facecolor="#FFFBEB", edgecolor="#F59E0B", linewidth=1.8)
    ax.add_patch(c3)
    ax.text(7, 30.5, "3. CAPA DE DATOS (REPOSITORY PATTERN + DTO FACTORIES + OFFLINE-FIRST)", fontsize=9.5, fontweight='bold', color="#B45309")

    # Central Repository Box
    b_repo = patches.FancyBboxPatch((35, 7), 30, 20, boxstyle="round,pad=0.5,rounding_size=1.2",
                                    facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.8)
    ax.add_patch(b_repo)
    ax.text(50, 23.5, "SaveBiteRepositoryImpl", fontsize=8.8, fontweight='bold', ha='center', color="#92400E")
    ax.text(50, 19, "Patrón Repositorio Único", fontsize=7.5, fontweight='bold', ha='center', color="#B45309")
    ax.text(50, 14.5, "• Arbitra Local vs Remoto\n• Política Offline-First\n• Cifrado de Vouchers QR\n• Sincronización en cola", fontsize=6.8, ha='center', color="#78350F")
    ax.text(50, 8.8, "Factory DTO: fromJson() / toJson()", fontsize=6.5, style='italic', ha='center', color="#B45309")

    # Local DataSource (Left)
    b_local = patches.FancyBboxPatch((6, 7), 25, 20, boxstyle="round,pad=0.4,rounding_size=1",
                                     facecolor="#FFFFFF", edgecolor="#FBBF24", linewidth=1.2)
    ax.add_patch(b_local)
    ax.text(18.5, 23.5, "Local DataSource", fontsize=8, fontweight='bold', ha='center', color="#92400E")
    ax.text(18.5, 19, "Caché Offline & Llaves", fontsize=7.2, ha='center', color="#B45309")
    ax.text(18.5, 14, "• Hive NoSQL DB\n• FlutterSecureStorage\n  (KeyStore / KeyChain)\n• Vouchers locales", fontsize=6.8, ha='center', color="#475569")
    ax.text(18.5, 8.8, "Sin conexión celular", fontsize=6.5, style='italic', ha='center', color="#10B981")

    # Remote DataSource (Right)
    b_remote = patches.FancyBboxPatch((69, 7), 25, 20, boxstyle="round,pad=0.4,rounding_size=1",
                                      facecolor="#FFFFFF", edgecolor="#FBBF24", linewidth=1.2)
    ax.add_patch(b_remote)
    ax.text(81.5, 23.5, "Remote DataSource", fontsize=8, fontweight='bold', ha='center', color="#92400E")
    ax.text(81.5, 19, "Cloud BaaS & APIs", fontsize=7.2, ha='center', color="#B45309")
    ax.text(81.5, 14, "• Supabase / Firebase\n• Realtime WebSockets\n• Google Maps Platform\n• Stripe / MercadoPago", fontsize=6.8, ha='center', color="#475569")
    ax.text(81.5, 8.8, "Conectividad activa", fontsize=6.5, style='italic', ha='center', color="#2563EB")

    # Conexiones bidireccionales Repo <-> DataSources
    ax.annotate("", xy=(34, 17), xytext=(31.5, 17), arrowprops=dict(arrowstyle="<->", color="#D97706", lw=1.8))
    ax.annotate("", xy=(68.5, 17), xytext=(65.5, 17), arrowprops=dict(arrowstyle="<->", color="#D97706", lw=1.8))

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Diagrama de patrones generado: {output_path}")

def generate_gitflow_diagram(output_path):
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Fondo
    bg_box = patches.FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=1,rounding_size=2",
                                    facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.5)
    ax.add_patch(bg_box)

    # Título
    ax.text(50, 96, "ESTRATEGIA DE VERSIONAMIENTO: GITFLOW, SEMVER & CI/CD",
            fontsize=13, fontweight='bold', ha='center', va='center', color="#0F4C81", fontfamily='sans-serif')
    ax.text(50, 93, "Flujo de Trabajo Colaborativo, Protección de Ramas, Convención de Commits y Compilación Continua",
            fontsize=9.5, style='italic', ha='center', va='center', color="#64748B", fontfamily='sans-serif')

    # Líneas de ramas horizontales
    # main (y=78)
    ax.plot([15, 95], [78, 78], color="#0F4C81", lw=3.5, zorder=1)
    ax.text(8, 78, "main", fontsize=10, fontweight='bold', ha='center', va='center', color="#0F4C81",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#E0F2FE", edgecolor="#0F4C81", lw=1))

    # hotfix (y=66)
    ax.plot([45, 65], [66, 66], color="#EF4444", lw=2.2, linestyle="--", zorder=1)
    ax.text(38, 66, "hotfix/*", fontsize=8.5, fontweight='bold', ha='center', va='center', color="#DC2626",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEE2E2", edgecolor="#DC2626", lw=1))

    # release (y=54)
    ax.plot([60, 80], [54, 54], color="#F59E0B", lw=2.2, linestyle="-.", zorder=1)
    ax.text(53, 54, "release/*", fontsize=8.5, fontweight='bold', ha='center', va='center', color="#B45309",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF3C7", edgecolor="#B45309", lw=1))

    # develop (y=42)
    ax.plot([15, 95], [42, 42], color="#10B981", lw=3.5, zorder=1)
    ax.text(8, 42, "develop", fontsize=10, fontweight='bold', ha='center', va='center', color="#047857",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#DCFCE7", edgecolor="#047857", lw=1))

    # feature branches (y=30)
    ax.plot([25, 45], [30, 30], color="#6366F1", lw=2, linestyle=":", zorder=1)
    ax.plot([45, 65], [30, 30], color="#8B5CF6", lw=2, linestyle=":", zorder=1)
    ax.text(12, 30, "feature/*", fontsize=8.5, fontweight='bold', ha='center', va='center', color="#4338CA",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#EDE9FE", edgecolor="#4338CA", lw=1))

    # Puntos de commits en main
    ax.scatter([18, 50, 78, 92], [78, 78, 78, 78], color="#0F4C81", s=110, zorder=3)
    ax.text(18, 82.5, "v0.1.0\nInitial", fontsize=7, fontweight='bold', ha='center', color="#0F4C81")
    ax.text(50, 82.5, "v0.2.1\nHotfix", fontsize=7, fontweight='bold', ha='center', color="#DC2626")
    ax.text(78, 82.5, "v0.3.0\nSprint 3", fontsize=7, fontweight='bold', ha='center', color="#0F4C81")
    ax.text(92, 82.5, "v1.0.0+1\nRelease", fontsize=7.5, fontweight='bold', ha='center', color="#059669")

    # Commits en develop
    ax.scatter([20, 32, 44, 56, 68, 76, 88], [42, 42, 42, 42, 42, 42, 42], color="#10B981", s=85, zorder=3)
    ax.text(20, 38.5, "Init Dev", fontsize=6.8, ha='center', color="#047857")
    ax.text(44, 38.5, "Merge feat/map", fontsize=6.8, ha='center', color="#047857")
    ax.text(68, 38.5, "Merge feat/qr", fontsize=6.8, ha='center', color="#047857")
    ax.text(88, 38.5, "Sprint 4 ready", fontsize=6.8, ha='center', color="#047857")

    # Branching de feature 1: map
    ax.annotate("", xy=(25, 30), xytext=(20, 42), arrowprops=dict(arrowstyle="->", color="#6366F1", lw=1.8))
    ax.scatter([30, 38], [30, 30], color="#6366F1", s=70, zorder=3)
    ax.text(34, 26, "feat(map): vista gps", fontsize=6.5, ha='center', color="#4338CA")
    ax.annotate("", xy=(44, 42), xytext=(40, 30), arrowprops=dict(arrowstyle="->", color="#6366F1", lw=1.8))
    ax.text(42, 35, "PR #12\nApproved", fontsize=6.5, fontweight='bold', color="#059669")

    # Branching de feature 2: qr scanner
    ax.annotate("", xy=(48, 30), xytext=(44, 42), arrowprops=dict(arrowstyle="->", color="#8B5CF6", lw=1.8))
    ax.scatter([52, 60], [30, 30], color="#8B5CF6", s=70, zorder=3)
    ax.text(56, 26, "feat(qr): camara scanner", fontsize=6.5, ha='center', color="#6D28D9")
    ax.annotate("", xy=(68, 42), xytext=(62, 30), arrowprops=dict(arrowstyle="->", color="#8B5CF6", lw=1.8))
    ax.text(66, 35, "PR #18\nApproved", fontsize=6.5, fontweight='bold', color="#059669")

    # Release branch flow
    ax.annotate("", xy=(62, 54), xytext=(56, 42), arrowprops=dict(arrowstyle="->", color="#F59E0B", lw=1.8))
    ax.scatter([66, 72], [54, 54], color="#F59E0B", s=75, zorder=3)
    ax.text(69, 58, "QA / Bugfixes", fontsize=6.8, fontweight='bold', ha='center', color="#B45309")
    ax.annotate("", xy=(78, 78), xytext=(74, 54), arrowprops=dict(arrowstyle="->", color="#0F4C81", lw=2))
    ax.annotate("", xy=(76, 42), xytext=(74, 54), arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.8))

    # Hotfix flow
    ax.annotate("", xy=(45, 66), xytext=(35, 78), arrowprops=dict(arrowstyle="->", color="#EF4444", lw=1.8))
    ax.scatter([48, 55], [66, 66], color="#EF4444", s=70, zorder=3)
    ax.text(51.5, 62, "fix(sec): auth token leak", fontsize=6.5, ha='center', color="#B91C1C")
    ax.annotate("", xy=(50, 78), xytext=(56, 66), arrowprops=dict(arrowstyle="->", color="#0F4C81", lw=2))
    ax.annotate("", xy=(56, 42), xytext=(56, 66), arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.8))

    # PANEL INFERIOR: POLÍTICAS DE CALIDAD Y CI/CD PIPELINE
    b_ci = patches.FancyBboxPatch((4, 4), 92, 19, boxstyle="round,pad=0.6,rounding_size=1.2",
                                  facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.5)
    ax.add_patch(b_ci)
    ax.text(7, 20, "PIPELINE CI/CD AUTOMATIZADO CON GITHUB ACTIONS (.github/workflows/mobile_ci.yml)", fontsize=8.5, fontweight='bold', color="#0F4C81")

    steps = [
        ("1. Lint & Static Analysis", "flutter analyze --fatal-infos\nReglas stricts lints"),
        ("2. Tests Unitarios & Mock", "flutter test --coverage\nVerificación BLoC & Repos"),
        ("3. Compilación Release", "flutter build apk --release\nOfuscación ProGuard/R8"),
        ("4. Artefacto Verificado", "SaveBite.apk (150MB+)\nListo para QA y Entrega")
    ]
    for i, (s_title, s_desc) in enumerate(steps):
        bx = 6 + (i * 22.8)
        b_st = patches.FancyBboxPatch((bx, 6), 21.5, 11.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                                      facecolor="#F1F5F9", edgecolor="#94A3B8", linewidth=1)
        ax.add_patch(b_st)
        ax.text(bx + 10.75, 14.5, s_title, fontsize=7.2, fontweight='bold', ha='center', color="#1E293B")
        ax.text(bx + 10.75, 10, s_desc, fontsize=6.2, ha='center', color="#475569")
        if i < 3:
            ax.annotate("", xy=(bx + 22.5, 12), xytext=(bx + 21.5, 12), arrowprops=dict(arrowstyle="->", color="#0F4C81", lw=1.5))

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Diagrama de versionamiento generado: {output_path}")

def generate_ecosistema_diagram(output_path):
    fig, ax = plt.subplots(figsize=(12, 7.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Fondo
    bg_box = patches.FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=1,rounding_size=2",
                                    facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.5)
    ax.add_patch(bg_box)

    # Título
    ax.text(50, 96, "ECOSISTEMA DE SERVICIOS E INTEGRACIÓN CLOUD (SAVEBITE)",
            fontsize=13, fontweight='bold', ha='center', va='center', color="#0F4C81", fontfamily='sans-serif')
    ax.text(50, 93, "Interconexión de APIs Externas, Hardware Móvil y Servicios Críticos en la Nube",
            fontsize=9.5, style='italic', ha='center', va='center', color="#64748B", fontfamily='sans-serif')

    # APLICACIÓN MÓVIL CENTRAL (FLUTTER)
    b_core = patches.FancyBboxPatch((36, 36), 28, 48, boxstyle="round,pad=0.8,rounding_size=2",
                                    facecolor="#0F4C81", edgecolor="#0A2E50", linewidth=2.5)
    ax.add_patch(b_core)
    ax.text(50, 79, "SAVEBITE APP", fontsize=11, fontweight='bold', ha='center', color="#FFFFFF")
    ax.text(50, 76, "Flutter Client (Dart 3.x)", fontsize=8, ha='center', color="#93C5FD")

    # Módulos internos de la app
    in_mods = [
        ("Capa UI / BLoC", "#1E3A8A"),
        ("Google Maps Widget", "#047857"),
        ("Mobile Scanner Engine", "#B45309"),
        ("Hive / SecureStorage", "#6D28D9"),
        ("Network Repositories", "#0369A1")
    ]
    for idx, (m_name, m_color) in enumerate(in_mods):
        my = 71 - (idx * 6.8)
        b_m = patches.FancyBboxPatch((38, my - 2), 24, 5.2, boxstyle="round,pad=0.2,rounding_size=0.6",
                                     facecolor="#FFFFFF", edgecolor=m_color, linewidth=1)
        ax.add_patch(b_m)
        ax.text(50, my + 0.5, m_name, fontsize=7.2, fontweight='bold', ha='center', color=m_color)

    ax.text(50, 39, "Android 10+ / iOS 14+", fontsize=6.8, style='italic', ha='center', color="#BAE6FD")

    # LADO IZQUIERDO: APIS DE TERCEROS Y HARDWARE NATIVO
    c_left = patches.FancyBboxPatch((3, 10), 30, 74, boxstyle="round,pad=0.6,rounding_size=1.5",
                                    facecolor="#EFF6FF", edgecolor="#60A5FA", linewidth=1.5)
    ax.add_patch(c_left)
    ax.text(18, 80.5, "APIS DE TERCEROS Y HARDWARE", fontsize=8.5, fontweight='bold', ha='center', color="#1D4ED8")

    apis = [
        ("Google Maps Platform", "Maps SDK, Places & Haversine", "Renderizado de comercios cercanos\nen vivo y cálculo de rutas a pie.", "#2563EB"),
        ("Pasarela de Pagos (Stripe / MP)", "Tokenización PCI-DSS Nivel 1", "Cobro in-app sin retener datos de tarjeta,\nliquidación directa a comercios.", "#4F46E5"),
        ("Google Sign-In OAuth 2.0", "Autenticación Federada", "Inicio de sesión seguro en 1 toque con\ncuenta institucional UTS o Gmail.", "#059669"),
        ("Sensor Cámara (Mobile Scanner)", "CameraX / AVFoundation", "Escaneo QR en tiempo real (<2s)\ncon feedback háptico en mostrador.", "#D97706")
    ]

    for i, (title, sub, desc, col) in enumerate(apis):
        ay = 74 - (i * 15.5)
        b_a = patches.FancyBboxPatch((5, ay - 11), 26, 13.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                                     facecolor="#FFFFFF", edgecolor=col, linewidth=1.2)
        ax.add_patch(b_a)
        ax.text(18, ay + 0.2, title, fontsize=7.2, fontweight='bold', ha='center', color=col)
        ax.text(18, ay - 3, sub, fontsize=6.2, fontweight='bold', ha='center', color="#475569")
        ax.text(18, ay - 7.5, desc, fontsize=5.8, ha='center', color="#64748B")

        # Flecha conectora a la app
        ax.annotate("", xy=(36, ay - 4), xytext=(31, ay - 4), arrowprops=dict(arrowstyle="<->", color=col, lw=1.5))

    # LADO DERECHO: ARQUITECTURA CLOUD BAAS Y MICROSERVICIOS
    c_right = patches.FancyBboxPatch((67, 10), 30, 74, boxstyle="round,pad=0.6,rounding_size=1.5",
                                     facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=1.5)
    ax.add_patch(c_right)
    ax.text(82, 80.5, "ARQUITECTURA CLOUD (BAAS)", fontsize=8.5, fontweight='bold', ha='center', color="#B45309")

    clouds = [
        ("Supabase Auth / Firebase Auth", "Gestión de Identidades & JWT", "Control de acceso basado en roles (RBAC),\ncifrado Argon2 y tokens efímeros.", "#B45309"),
        ("PostgreSQL PostGIS / Firestore", "Base de Datos en Tiempo Real", "Consultas geoespaciales por radio y\nsincronización de stock por WebSockets.", "#065F46"),
        ("Cloud Storage (S3-Compatible)", "Almacenamiento de Archivos", "Buckets seguros con CDN para fotos de\ncomercios optimizadas en formato WebP.", "#1D4ED8"),
        ("Cloud Messaging (FCM Push)", "Alertas en Tiempo Real", "Notificación cuando comercios favoritos\npublican paquetes y avisos de expiración.", "#DC2626"),
        ("Edge Functions (Serverless)", "Cron Jobs & Reglas de Negocio", "Vencimiento automático de paquetes,\nconciliación y cálculo de CO2 mitigado.", "#7C3AED")
    ]

    for i, (title, sub, desc, col) in enumerate(clouds):
        cy = 74 - (i * 12.8)
        b_c = patches.FancyBboxPatch((69, cy - 9), 26, 11, boxstyle="round,pad=0.3,rounding_size=0.8",
                                     facecolor="#FFFFFF", edgecolor=col, linewidth=1.2)
        ax.add_patch(b_c)
        ax.text(82, cy + 0.2, title, fontsize=6.8, fontweight='bold', ha='center', color=col)
        ax.text(82, cy - 2.5, sub, fontsize=6, fontweight='bold', ha='center', color="#475569")
        ax.text(82, cy - 6, desc, fontsize=5.6, ha='center', color="#64748B")

        # Flecha conectora a la app
        ax.annotate("", xy=(69, cy - 3), xytext=(64, cy - 3), arrowprops=dict(arrowstyle="<->", color=col, lw=1.5))

    # FOOTER: SEGURIDAD Y ENCRIPTACIÓN TRANSVERSAL
    b_sec = patches.FancyBboxPatch((3, 3), 94, 6, boxstyle="round,pad=0.4,rounding_size=1",
                                   facecolor="#10B981", edgecolor="#059669", linewidth=1.2)
    ax.add_patch(b_sec)
    ax.text(50, 6, "SEGURIDAD INTEGRAL: TLS 1.3 CIFRADO EN TRÁNSITO + TOKENS QR FIRMADOS (HMAC-SHA256) + COMPLIMIENTO LFPDPPP (MÉXICO)",
            fontsize=7.2, fontweight='bold', ha='center', va='center', color="#FFFFFF")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Diagrama de ecosistema cloud generado: {output_path}")

def generate_app_mockup_screens():
    """Genera 6 capturas de alta definición con marco de teléfono representando el avance real revisado en clase"""
    screens = [
        ("screen_1_auth.png", "Splash & Login Multi-Rol", "Acceso Alumno / Comercio", [
            ("Header", "SaveBite", "#0F4C81"),
            ("Tagline", "Rescate de Alimentos UTS\nODS 12: Cero Merma", "#00AE9D"),
            ("Btn1", "Ingresar como Consumidor (Alumno)", "#0F4C81"),
            ("Btn2", "Ingresar como Comercio Aliado", "#F58220"),
            ("Footer", "Protección LFPDPPP | Auth JWT Segura", "#64748B")
        ]),
        ("screen_2_explore_map.png", "Mapa GPS y Feed de Ofertas", "Salamanca, Gto. - Radio 3 km", [
            ("Search", "Buscar panaderías, fruterías...", "#FFFFFF"),
            ("MapPin1", "Panadería La Tradición (3 packs)", "#10B981"),
            ("MapPin2", "Pizzería Nápoles (1 pack)", "#10B981"),
            ("Card1", "Pack Dulce & Salado\n$45.00 MXN (-65% dto)\nRecogida: 19:30 - 20:30 hrs", "#0F4C81"),
            ("Card2", "Caja Fruta Fresca Selección\n$35.00 MXN (-60% dto)\nRecogida: 18:00 - 19:00 hrs", "#0F4C81")
        ]),
        ("screen_3_package_detail.png", "Ficha Detallada de Paquete", "Reserva In-App con 1 Toque", [
            ("Store", "Panadería La Tradición\nCalle Hidalgo #204, Centro", "#0F4C81"),
            ("Price", "$45.00 MXN  (Antes $130.00)  -65%", "#10B981"),
            ("Desc", "Paquete sorpresa con bollería del día,\npan campesino y donas horneadas hoy.\nEn perfecto estado para consumo.", "#334155"),
            ("Window", "Ventana de recogida estricta:\nHoy de 19:30 a 20:30 hrs", "#F58220"),
            ("BtnReserve", "RESERVAR AHORA (VOUCHER QR)", "#00AE9D")
        ]),
        ("screen_4_voucher_qr.png", "Voucher Digital con QR Dinámico", "Token Efímero Cifrado HMAC", [
            ("Title", "¡Reserva Confirmada #SB-8921!", "#047857"),
            ("Timer", "Expira en: 00:48:22\nPresenta este código en caja", "#DC2626"),
            ("QR_Placeholder", "[ CÓDIGO QR DINÁMICO ACTIVO ]\nHMAC: 9f8a...c24e\nModo Offline-First Disponible", "#0F4C81"),
            ("Notice", "Al escanearse se liberará el paquete y\nse sumarán 1.2 kg al Impacto ODS.", "#64748B")
        ]),
        ("screen_5_scanner.png", "Escáner QR para Comercio", "Cámara de Baja Latencia (<2s)", [
            ("CameraUI", "[ VISOR DE CÁMARA ACTIVO ]\nCameraX Native Engine\nApunte al QR del estudiante", "#1E293B"),
            ("ScanResult", "VOUCHER VÁLIDO DETECTADO\nAlumno: Alvaro Chávez (UTS)\nPack: Surtido Panadería #SB-8921", "#10B981"),
            ("BtnDeliver", "CONFIRMAR ENTREGA DE PAQUETE", "#10B981")
        ]),
        ("screen_6_eco_impact.png", "Calculadora de Impacto ODS", "Métricas Ambientales en Tiempo Real", [
            ("HeroStat1", "14.5 kg", "Comida Rescatada"),
            ("HeroStat2", "$860.00 MXN", "Dinero Ahorrado"),
            ("HeroStat3", "36.2 kg CO2e", "Emisiones Evitadas"),
            ("Badge", "Insignia: Rescatador Oro UTS (Nivel 4)", "#F58220"),
            ("ODSInfo", "Alineado con ODS 12 (Consumo Responsable)\ny ODS 2 (Hambre Cero)", "#00AE9D")
        ])
    ]

    for filename, title, subtitle, items in screens:
        w, h = 420, 780
        img = Image.new("RGB", (w, h), color="#0F172A")
        draw = ImageDraw.Draw(img)

        # Marco del teléfono
        draw.rounded_rectangle([(10, 10), (w - 10, h - 10)], radius=36, fill="#F8FAFC", outline="#334155", width=6)
        
        # Barra de estado superior
        draw.rounded_rectangle([(w//2 - 60, 16), (w//2 + 60, 36)], radius=10, fill="#0F172A")
        draw.text((32, 22), "09:41", fill="#0F172A")
        draw.text((w - 70, 22), "5G  100%", fill="#0F172A")

        # Barra de aplicación / AppBar
        draw.rectangle([(13, 44), (w - 13, 105)], fill="#0F4C81")
        draw.text((26, 52), title, fill="#FFFFFF")
        draw.text((26, 76), subtitle, fill="#A7F3D0")

        # Contenido de la pantalla
        y_pos = 120
        for item in items:
            itype = item[0]
            if itype == "Header":
                draw.rectangle([(25, y_pos), (w - 25, y_pos + 65)], fill="#EFF6FF", outline="#93C5FD", width=2)
                draw.text((40, y_pos + 12), item[1], fill=item[2])
                y_pos += 80
            elif itype == "Tagline":
                draw.text((35, y_pos), item[1], fill=item[2])
                y_pos += 45
            elif itype.startswith("Btn"):
                btn_col = item[2] if len(item) > 2 else "#0F4C81"
                draw.rounded_rectangle([(25, y_pos), (w - 25, y_pos + 46)], radius=12, fill=btn_col)
                draw.text((38, y_pos + 14), item[1], fill="#FFFFFF")
                y_pos += 58
            elif itype == "Footer":
                draw.text((35, y_pos + 10), item[1], fill=item[2])
                y_pos += 35
            elif itype.startswith("Card") or itype == "Desc" or itype == "Store":
                bg = "#FFFFFF" if itype != "Store" else "#F0FDF4"
                draw.rounded_rectangle([(25, y_pos), (w - 25, y_pos + 72)], radius=10, fill=bg, outline="#E2E8F0", width=2)
                draw.text((35, y_pos + 8), item[1], fill=item[2])
                y_pos += 82
            elif itype == "Search":
                draw.rounded_rectangle([(25, y_pos), (w - 25, y_pos + 40)], radius=20, fill="#FFFFFF", outline="#CBD5E1", width=2)
                draw.text((45, y_pos + 12), item[1], fill="#94A3B8")
                y_pos += 50
            elif itype.startswith("MapPin"):
                draw.rounded_rectangle([(30, y_pos), (w - 30, y_pos + 38)], radius=8, fill="#DCFCE7", outline="#10B981", width=2)
                draw.text((42, y_pos + 10), f"📍 {item[1]}", fill="#047857")
                y_pos += 46
            elif itype == "Price":
                draw.rounded_rectangle([(25, y_pos), (w - 25, y_pos + 40)], radius=8, fill="#DCFCE7")
                draw.text((35, y_pos + 10), item[1], fill=item[2])
                y_pos += 48
            elif itype == "Window":
                draw.rounded_rectangle([(25, y_pos), (w - 25, y_pos + 48)], radius=8, fill="#FFFBEB", outline="#F59E0B", width=1)
                draw.text((35, y_pos + 8), item[1], fill=item[2])
                y_pos += 56
            elif itype == "QR_Placeholder":
                draw.rounded_rectangle([(65, y_pos), (w - 65, y_pos + 160)], radius=16, fill="#FFFFFF", outline="#0F4C81", width=3)
                # Dibujar patrón simulado de QR
                draw.rectangle([(85, y_pos + 20), (135, y_pos + 70)], fill="#0F4C81")
                draw.rectangle([(95, y_pos + 30), (125, y_pos + 60)], fill="#FFFFFF")
                draw.rectangle([(102, y_pos + 37), (118, y_pos + 53)], fill="#0F4C81")

                draw.rectangle([(w - 135, y_pos + 20), (w - 85, y_pos + 70)], fill="#0F4C81")
                draw.rectangle([(w - 125, y_pos + 30), (w - 95, y_pos + 60)], fill="#FFFFFF")
                draw.rectangle([(w - 118, y_pos + 37), (w - 102, y_pos + 53)], fill="#0F4C81")

                draw.rectangle([(85, y_pos + 90), (135, y_pos + 140)], fill="#0F4C81")
                draw.rectangle([(95, y_pos + 100), (125, y_pos + 130)], fill="#FFFFFF")
                draw.rectangle([(102, y_pos + 107), (118, y_pos + 123)], fill="#0F4C81")

                draw.text((150, y_pos + 55), "TOKEN ACTIVO\nROTATIVO 60s", fill="#047857")
                y_pos += 175
            elif itype == "Timer" or itype == "Title":
                draw.text((35, y_pos), item[1], fill=item[2])
                y_pos += 38
            elif itype == "CameraUI":
                draw.rounded_rectangle([(25, y_pos), (w - 25, y_pos + 140)], radius=12, fill="#0F172A", outline="#10B981", width=2)
                draw.text((45, y_pos + 30), item[1], fill="#FFFFFF")
                y_pos += 150
            elif itype == "ScanResult":
                draw.rounded_rectangle([(25, y_pos), (w - 25, y_pos + 60)], radius=8, fill="#DCFCE7", outline="#10B981", width=2)
                draw.text((35, y_pos + 8), item[1], fill="#065F46")
                y_pos += 70
            elif itype.startswith("HeroStat"):
                draw.rounded_rectangle([(25, y_pos), (w - 25, y_pos + 52)], radius=10, fill="#F0FDF4", outline="#10B981", width=1)
                draw.text((38, y_pos + 8), item[1], fill="#047857")
                draw.text((38, y_pos + 28), item[2], fill="#475569")
                y_pos += 60
            elif itype == "Badge" or itype == "ODSInfo" or itype == "Notice":
                draw.rounded_rectangle([(25, y_pos), (w - 25, y_pos + 42)], radius=8, fill="#F1F5F9", outline="#CBD5E1", width=1)
                draw.text((35, y_pos + 8), item[1], fill=item[2])
                y_pos += 50

        # Barra inferior de navegación
        draw.rectangle([(13, h - 65), (w - 13, h - 13)], fill="#FFFFFF")
        draw.line([(13, h - 65), (w - 13, h - 65)], fill="#E2E8F0", width=1)
        draw.text((40, h - 45), "Explorar", fill="#0F4C81")
        draw.text((150, h - 45), "Reservas", fill="#64748B")
        draw.text((250, h - 45), "Impacto", fill="#64748B")
        draw.text((330, h - 45), "Perfil", fill="#64748B")

        # Botón home indicador inferior
        draw.rounded_rectangle([(w//2 - 50, h - 22), (w//2 + 50, h - 17)], radius=3, fill="#94A3B8")

        img.save(filename)
        print(f"Mockup generado: {filename}")

if __name__ == "__main__":
    generate_patrones_diagram("diagram_fase2_patrones_arquitectura.png")
    generate_gitflow_diagram("diagram_fase2_versionamiento_gitflow.png")
    generate_ecosistema_diagram("diagram_fase2_ecosistema_integracion.png")
    generate_app_mockup_screens()
