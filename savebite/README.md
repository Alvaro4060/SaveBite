# SaveBite 🥑🥖 — Frontend Móvil en Flutter (Fase Inicial)
**Universidad Tecnológica de Salamanca (UTS)**  
**División de Tecnologías de la Información y Comunicación**  
**Asignatura:** Desarrollo Móvil Integral (10° Cuatrimestre IDGS)  
**ODS de la ONU:** ODS 12 (Producción y Consumo Responsables) & ODS 2 (Hambre Cero)

---

## 📱 Descripción del Proyecto
**SaveBite** es una plataforma móvil colaborativa que conecta a panaderías, cafeterías, fruterías y restaurantes de Salamanca, Guanajuato, con la comunidad universitaria y urbana para rescatar paquetes de comida del día en perfecto estado con descuentos del 50% al 70%, evitando la merma alimentaria y los gases de efecto invernadero (CO₂).

Este repositorio contiene la **implementación frontend completa de la Fase 1**, estructurada bajo **Clean Architecture** en Flutter y Dart.

---

## 🏛️ Estructura del Código (Clean Architecture)

```
savebite/
├── pubspec.yaml                      # Configuración de dependencias y assets
├── analysis_options.yaml             # Reglas de linting y calidad de código
├── android/app/src/main/
│   └── AndroidManifest.xml           # Permisos de GPS, Cámara e Internet
├── web/
│   ├── index.html                    # Scaffolding Web
│   └── manifest.json                 # PWA Manifest
└── lib/
    ├── main.dart                     # Entrada principal de la aplicación
    ├── core/                         # Núcleo y configuración global
    │   ├── constants/
    │   │   ├── app_colors.dart       # Paleta oficial UTS / SaveBite
    │   │   ├── app_strings.dart      # Textos centralizados de la interfaz
    │   │   └── app_styles.dart       # Tipografías y decoraciones
    │   ├── theme/
    │   │   └── app_theme.dart        # Tema Material 3
    │   └── utils/
    │       └── formatters.dart       # Formateadores de moneda, distancia y descuentos
    ├── domain/                       # Capa de Dominio (Entidades puras de negocio)
    │   └── entities/
    │       ├── food_package.dart     # Entidad de Paquete Sorpresa
    │       ├── reservation.dart      # Entidad de Reserva & Voucher QR
    │       ├── store.dart            # Entidad de Comercio Local
    │       ├── user_profile.dart     # Roles (Consumidor vs Comercio Aliado)
    │       └── eco_impact.dart       # Métricas ODS e insignias ecológicas
    ├── data/                         # Capa de Datos
    │   └── datasources/
    │       └── mock_data.dart        # Dataset realista con comercios de Salamanca
    └── presentation/                 # Capa de Presentación
        ├── state/
        │   ├── app_state.dart        # Estado reactivo global con ChangeNotifier
        │   └── app_state_provider.dart # InheritedNotifier para inyección limpia
        ├── widgets/
        │   ├── custom_button.dart    # Botón principal y secundario
        │   ├── category_chip.dart    # Filtro de categorías (Panadería, etc.)
        │   ├── package_card.dart     # Tarjeta de paquete en el feed
        │   ├── dynamic_qr_widget.dart# Renderizador CustomPainter de QR dinámico
        │   └── eco_stat_card.dart    # Métricas numéricas de impacto
        └── screens/
            ├── splash/
            │   └── splash_screen.dart # Pantalla de carga con animación SaveBite
            ├── auth/
            │   └── login_screen.dart  # Acceso con selector de perfil y botones Demo
            ├── main_shell_screen.dart # Shell con navegación inferior y switch de rol
            ├── explore/
            │   ├── explore_feed_screen.dart # Feed con buscador, filtros y toggle
            │   └── simulated_map_view.dart  # Mapa interactivo de Salamanca con pines
            ├── package_detail/
            │   └── package_detail_screen.dart # Ficha completa y reserva en 1 toque
            ├── reservations/
            │   └── reservations_screen.dart # Vouchers activos e historial
            ├── qr_voucher/
            │   └── voucher_screen.dart # Voucher con código QR dinámico y modo offline
            ├── merchant/
            │   ├── merchant_dashboard_screen.dart # Panel del comercio con métricas
            │   ├── create_package_screen.dart     # Formulario para publicar pack
            │   └── qr_scanner_screen.dart         # Lector óptico / cámara para canje
            └── impact/
                └── impact_calculator_screen.dart  # Calculadora ODS 12 e insignias
```

---

## 🚀 Funcionalidades Frontend Implementadas

1. **Splash Screen Dinámico:**
   - Logotipo con animación de escala y fundido, isotipo de bolsa y hoja ecológica.
   - Créditos oficiales a la Universidad Tecnológica de Salamanca.

2. **Autenticación con Selección de Rol:**
   - Selector visual entre **Consumidor / Estudiante UTS** y **Comercio Aliado**.
   - Botones rápidos de acceso Demo con un solo toque.

3. **Feed y Mapa GPS Interactivo (Salamanca):**
   - Buscador en tiempo real por nombre de producto o establecimiento.
   - Carrusel de categorías: *Panaderías, Cafeterías, Fruterías, Comida Preparada*.
   - Toggle interactivo entre vista de **Lista** y vista de **Mapa GPS** de Salamanca con ubicación del usuario en el Campus UTS y pines interactivos de comercios locales.
   - Cálculo automático de distancias y porcentajes de descuento (-50% a -70%).

4. **Ficha Detallada de Paquete y Reserva con 1 Toque:**
   - Comparación de precio original tachado vs precio con descuento SaveBite.
   - Métrica de ahorro y horario límite de recogida (ej. 19:30 - 20:30).
   - Modal de confirmación con generación instantánea de token de reserva.

5. **Voucher Digital con Código QR Dinámico (Offline-First):**
   - Renderizado vectorial de alta precisión mediante `CustomPainter` sin dependencias externas.
   - Indicador de persistencia en caché local (funciona en la vía pública sin internet).
   - Token de canje de un solo uso para validación en mostrador.

6. **Flujo de Comercio Aliado (Modo Establecimiento):**
   - **Panel de control:** Contador de packs activos, canjes del día y kg de comida rescatados.
   - **Formulario de publicación:** Cálculo dinámico del descuento porcentual y peso en kg.
   - **Lector de Código QR:** Visor simulado con láser animado, linterna y validación en menos de 2 segundos.

7. **Calculadora de Impacto ODS 12 & Gamificación:**
   - Métricas acumuladas: Kg de comida rescatados, Kg de CO₂ mitigados y dinero ahorrado ($ MXN).
   - Insignias de sostenibilidad desbloqueables (*Rescatador Novato, Amigo de Panaderías, Héroe Cero Merma*).

---

## 🛠️ Cómo Ejecutar el Proyecto

### Requisitos:
- Tener instalado el SDK de Flutter (>= 3.0.0).
- Un emulador de Android/iOS o un navegador web (Chrome/Edge).

### Comandos:
```bash
# 1. Navegar a la carpeta del proyecto
cd savebite

# 2. Descargar dependencias
flutter pub get

# 3. Ejecutar en navegador web (modo rápido)
flutter run -d chrome

# 4. O ejecutar en dispositivo Android/Emulador
flutter run
```

---

## 👥 Equipo de Desarrollo (IDGS - UTS)
- **Product Owner:** Alvaro Jesús Chávez Bazana
- **Scrum Master:** Guillermo Yael Berlín Fomperosa
- **Lead Mobile Developer:** Juan Pablo Vega Uribe
- **Backend & Data Architect:** Diego Sebastián Vilegas Enriquez
