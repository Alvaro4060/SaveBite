import os

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fase 2: Arquitectura, Planificación y Seguridad | SaveBite - UTS</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {
      --primary: #0F4C81;
      --primary-dark: #0A2E50;
      --primary-light: #2563EB;
      --secondary: #00AE9D;
      --secondary-dark: #0E7490;
      --accent: #F58220;
      --accent-hover: #EA580C;
      --success: #10B981;
      --green-dark: #047857;
      --purple: #8B5CF6;
      --dark: #0F172A;
      --text: #334155;
      --text-muted: #64748B;
      --bg: #F1F5F9;
      --card-bg: #FFFFFF;
      --border: #E2E8F0;
      --border-focus: #94A3B8;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      color: var(--text);
      background-color: var(--bg);
      line-height: 1.65;
      padding: 30px 15px;
      -webkit-font-smoothing: antialiased;
    }

    .document-wrapper {
      max-width: 1000px;
      margin: 0 auto;
      background: white;
      box-shadow: 0 20px 40px -15px rgba(15, 76, 129, 0.15), 0 0 1px 1px rgba(0, 0, 0, 0.05);
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid var(--border);
    }

    /* PORTADA OFICIAL */
    .cover {
      background: linear-gradient(135deg, #0A2E50 0%, #0F4C81 60%, #0A698A 100%);
      color: white;
      padding: 50px 45px 45px 45px;
      position: relative;
      border-bottom: 5px solid var(--secondary);
    }

    .cover-accent-bar {
      position: absolute;
      bottom: -9px;
      left: 0;
      right: 0;
      height: 4px;
      background: var(--accent);
    }

    .uni-badge {
      display: inline-block;
      font-family: 'Outfit', sans-serif;
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: #A7F3D0;
      margin-bottom: 8px;
    }

    .cover h1 {
      font-family: 'Outfit', sans-serif;
      font-size: 2.1rem;
      font-weight: 800;
      margin-bottom: 6px;
      letter-spacing: -0.5px;
    }

    .cover h2 {
      font-size: 1.05rem;
      font-weight: 400;
      color: #E2E8F0;
      margin-bottom: 4px;
    }

    .cover-career {
      font-weight: 700;
      color: #5EEAD4;
      font-size: 1.05rem;
      margin-bottom: 25px;
    }

    .phase-badge {
      display: inline-block;
      background: var(--accent);
      color: white;
      font-weight: 800;
      padding: 6px 16px;
      border-radius: 30px;
      font-size: 0.85rem;
      letter-spacing: 1px;
      text-transform: uppercase;
      box-shadow: 0 4px 12px rgba(245, 130, 32, 0.4);
      margin-bottom: 15px;
    }

    .project-hero {
      font-family: 'Outfit', sans-serif;
      font-size: 3rem;
      font-weight: 900;
      color: #FFFFFF;
      letter-spacing: -1px;
      line-height: 1.1;
      margin-bottom: 6px;
    }

    .project-subtitle {
      font-size: 1.05rem;
      color: #BAE6FD;
      font-style: italic;
      margin-bottom: 35px;
    }

    /* METADATA GRID */
    .meta-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 25px;
      background: rgba(255, 255, 255, 0.08);
      backdrop-filter: blur(8px);
      padding: 24px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.15);
    }

    .meta-card h3 {
      font-family: 'Outfit', sans-serif;
      font-size: 0.95rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #93C5FD;
      margin-bottom: 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.15);
      padding-bottom: 6px;
    }

    .meta-item {
      display: flex;
      margin-bottom: 8px;
      font-size: 0.9rem;
    }

    .meta-label {
      width: 140px;
      font-weight: 600;
      color: #E2E8F0;
    }

    .meta-val {
      flex: 1;
      color: #FFFFFF;
    }

    .team-member {
      margin-bottom: 12px;
    }

    .member-name {
      font-weight: 700;
      color: #FFFFFF;
      font-size: 0.95rem;
    }

    .member-role {
      font-size: 0.8rem;
      color: #5EEAD4;
      font-style: italic;
    }

    /* CONTENIDO DEL REPORTE */
    .content-body {
      padding: 45px;
    }

    .section-header {
      display: flex;
      align-items: center;
      gap: 14px;
      margin: 40px 0 18px 0;
      border-bottom: 2px solid var(--border);
      padding-bottom: 10px;
    }

    .section-header:first-of-type {
      margin-top: 0;
    }

    .section-num {
      background: var(--primary);
      color: white;
      width: 38px;
      height: 38px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Outfit', sans-serif;
      font-size: 1.15rem;
      font-weight: 800;
      flex-shrink: 0;
      box-shadow: 0 4px 10px rgba(15, 76, 129, 0.25);
    }

    .section-title {
      font-family: 'Outfit', sans-serif;
      font-size: 1.45rem;
      font-weight: 800;
      color: var(--primary);
      letter-spacing: -0.3px;
    }

    .sub-heading {
      font-family: 'Outfit', sans-serif;
      font-size: 1.12rem;
      font-weight: 700;
      color: var(--secondary-dark);
      margin: 24px 0 10px 0;
    }

    p {
      margin-bottom: 14px;
      color: var(--text);
      font-size: 0.96rem;
      text-align: justify;
    }

    ul.bullet-list {
      list-style: none;
      margin-bottom: 16px;
      padding-left: 0;
    }

    ul.bullet-list li {
      position: relative;
      padding-left: 22px;
      margin-bottom: 10px;
      font-size: 0.94rem;
      color: var(--text);
    }

    ul.bullet-list li::before {
      content: "■";
      position: absolute;
      left: 0;
      color: var(--secondary);
      font-size: 0.8rem;
      top: 1px;
    }

    ul.bullet-list strong {
      color: var(--primary);
    }

    /* CALLOUT BOXES */
    .callout {
      border-radius: 10px;
      padding: 16px 20px;
      margin: 20px 0;
      border-left: 4px solid;
    }

    .callout.blue {
      background-color: #F0F9FF;
      border-color: #0E7490;
    }

    .callout.blue .callout-title {
      color: #0E7490;
    }

    .callout.orange {
      background-color: #FFFBEB;
      border-color: var(--accent);
    }

    .callout.orange .callout-title {
      color: var(--accent);
    }

    .callout.green {
      background-color: #F0FDF4;
      border-color: var(--success);
    }

    .callout.green .callout-title {
      color: var(--green-dark);
    }

    .callout-title {
      font-weight: 700;
      font-size: 0.98rem;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .callout-desc {
      font-size: 0.9rem;
      color: var(--text);
      line-height: 1.5;
    }

    /* TABLAS ESTILIZADAS */
    .table-container {
      margin: 20px 0;
      overflow-x: auto;
      border-radius: 10px;
      border: 1px solid var(--border);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }

    table.data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      text-align: left;
    }

    table.data-table th {
      background: var(--primary);
      color: white;
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      padding: 12px 14px;
      border: 1px solid #1E5C94;
    }

    table.data-table td {
      padding: 10px 14px;
      border: 1px solid var(--border);
      color: var(--text);
      vertical-align: top;
    }

    table.data-table tr:nth-child(even) td {
      background: #F8FAFC;
    }

    table.data-table tr:hover td {
      background: #F1F5F9;
    }

    .tag-status {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
    }

    .tag-status.done {
      background: #DCFCE7;
      color: #166534;
    }

    .tag-status.progress {
      background: #FEF3C7;
      color: #92400E;
    }

    /* IMÁGENES Y DIAGRAMAS */
    .diagram-card {
      margin: 25px 0;
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      text-align: center;
    }

    .diagram-card img {
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
    }

    .diagram-caption {
      margin-top: 10px;
      font-size: 0.85rem;
      font-style: italic;
      color: var(--text-muted);
    }

    /* GRID DE MOCKUPS DE LA APP */
    .mockups-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin: 25px 0;
    }

    .mockup-item {
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px;
      text-align: center;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .mockup-item:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
    }

    .mockup-item img {
      max-width: 100%;
      border-radius: 8px;
      margin-bottom: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .mockup-title {
      font-weight: 700;
      font-size: 0.88rem;
      color: var(--primary);
      margin-bottom: 4px;
    }

    .mockup-sub {
      font-size: 0.76rem;
      color: var(--text-muted);
      font-style: italic;
    }

    /* TARJETAS DE CONCLUSIÓN */
    .conclusions-grid {
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-top: 20px;
    }

    .conclusion-card {
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-left: 5px solid var(--primary);
      border-radius: 10px;
      padding: 18px 22px;
    }

    .conclusion-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      flex-wrap: wrap;
      gap: 6px;
    }

    .conclusion-author {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 1.05rem;
      color: var(--primary);
    }

    .conclusion-role {
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--secondary-dark);
      background: #E0F2FE;
      padding: 3px 10px;
      border-radius: 20px;
    }

    .conclusion-text {
      font-size: 0.92rem;
      color: var(--text);
      line-height: 1.6;
      text-align: justify;
      margin-bottom: 0;
    }

    /* FOOTER */
    .footer-note {
      text-align: center;
      padding: 25px;
      background: #F8FAFC;
      border-top: 1px solid var(--border);
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    @media (max-width: 768px) {
      .meta-grid { grid-template-columns: 1fr; }
      .mockups-grid { grid-template-columns: 1fr; }
      .content-body { padding: 25px 20px; }
      .cover { padding: 35px 20px; }
    }
  </style>
</head>
<body>

  <div class="document-wrapper">
    <!-- PORTADA -->
    <div class="cover">
      <div class="uni-badge">UTS • DIVISIÓN TIC • 10° CUATRIMESTRE</div>
      <h1>UNIVERSIDAD TECNOLÓGICA DE SALAMANCA</h1>
      <h2>División de Tecnologías de la Información y Comunicación</h2>
      <div class="cover-career">Ingeniería en Desarrollo y Gestión de Software (IDGS)</div>

      <div class="phase-badge">FASE 2: ARQUITECTURA, PLANIFICACIÓN Y SEGURIDAD DEL DESARROLLO MÓVIL</div>
      <div class="project-hero">SaveBite</div>
      <div class="project-subtitle">Plataforma Móvil Colaborativa de Rescate de Alimentos Locales a Precio Reducido (ODS 12: Cero Merma)</div>

      <div class="meta-grid">
        <div class="meta-card">
          <h3>Datos de la Asignatura</h3>
          <div class="meta-item"><span class="meta-label">Asignatura:</span><span class="meta-val">Desarrollo Móvil Integral</span></div>
          <div class="meta-item"><span class="meta-label">Carrera:</span><span class="meta-val">IDGS (10° Cuatrimestre)</span></div>
          <div class="meta-item"><span class="meta-label">Docente:</span><span class="meta-val">Ericka Nohemí Álvarez Valencia</span></div>
          <div class="meta-item"><span class="meta-label">Fecha de Entrega:</span><span class="meta-val" style="color: #FBBF24; font-weight:700;">04 de Noviembre de 2026</span></div>
          <div class="meta-item"><span class="meta-label">Entregable:</span><span class="meta-val">Documento Digital Fase 2</span></div>
        </div>

        <div class="meta-card">
          <h3>Equipo de Desarrollo (IDGS)</h3>
          <div class="team-member">
            <div class="member-name">• Alvaro Jesús Chávez Bazana</div>
            <div class="member-role">Rol: Product Owner (PO) — Gestor de Requisitos</div>
          </div>
          <div class="team-member">
            <div class="member-name">• Guillermo Yael Berlín Fomperosa</div>
            <div class="member-role">Rol: Scrum Master (SM) — Facilitador & QA</div>
          </div>
          <div class="team-member">
            <div class="member-name">• Juan Pablo Vega Uribe</div>
            <div class="member-role">Rol: Lead Mobile Dev (UI/UX) — Frontend Flutter</div>
          </div>
          <div class="team-member">
            <div class="member-name">• Diego Sebastián Vilegas Enriquez</div>
            <div class="member-role">Rol: Backend & Data Architect — Cloud BaaS & Offline</div>
          </div>
        </div>
      </div>
      <div class="cover-accent-bar"></div>
    </div>

    <!-- CUERPO DEL INFORME -->
    <div class="content-body">

      <!-- SECCIÓN 1: INTRODUCCIÓN -->
      <div class="section-header">
        <div class="section-num">1</div>
        <div class="section-title">INTRODUCCIÓN A LA FASE 2: ARQUITECTURA, PLANIFICACIÓN Y SEGURIDAD</div>
      </div>

      <p>Habiendo fundamentado el alcance, la metodología ágil Scrum y los requerimientos funcionales en la Fase 1 para la plataforma <strong>SaveBite</strong>, la presente Fase 2 tiene como objetivo formalizar el diseño arquitectónico profundo, la justificación técnica de frameworks, los esquemas de versionamiento profesional, el blindaje de seguridad móvil y el ecosistema de servicios integrados en la nube.</p>

      <div class="sub-heading">> 1.1 Propósito Técnico y Estratégico de la Fase 2</div>
      <p>El desarrollo móvil profesional demanda una ingeniería defensiva que responda con solvencia a las restricciones severas del hardware móvil: fluctuación de red en calle, consumo estricto de batería al operar el sensor GPS, latencia en la decodificación de códigos QR con la cámara y estrictas regulaciones sobre la privacidad de la geolocalización del usuario.</p>
      <p>Mediante esta planeación integral se asegura que SaveBite no dependa de implementaciones acopladas o código improvisado, garantizando que cada módulo desarrollado por el equipo (UI en Flutter, BaaS en la nube, sincronización offline y escaneo de vouchers) converja bajo estándares de la industria como Clean Architecture, OWASP Mobile Top 10 y la legislación mexicana LFPDPPP.</p>

      <!-- SECCIÓN 2: PATRONES DE DISEÑO -->
      <div class="section-header">
        <div class="section-num">2</div>
        <div class="section-title">PROPUESTA Y JUSTIFICACIÓN DE PATRONES DE DISEÑO</div>
      </div>

      <div class="callout blue">
        <div class="callout-title">🏛️ Patrones de Diseño Seleccionados para SaveBite</div>
        <div class="callout-desc">Para responder a los desafíos de persistencia híbrida, reactividad en tiempo real y alta testabilidad, se seleccionaron formalmente cuatro patrones de diseño complementarios: <strong>Repository Pattern</strong>, <strong>BLoC Pattern (Observer)</strong>, <strong>Service Locator (Singleton)</strong> y <strong>Data Transfer Object (DTO) con Factory Method</strong>.</div>
      </div>

      <div class="sub-heading">> 2.1 Patrón Repositorio (Repository Pattern) - Fuente Única de Verdad</div>
      <ul class="bullet-list">
        <li><strong>Uso en SaveBite:</strong> Actúa como un intermediario y árbitro inteligente entre la capa de Dominio (Casos de Uso) y las múltiples fuentes de datos (<code>RemoteDataSource</code> vía Supabase/Firebase y <code>LocalDataSource</code> vía Hive/SQLite). Centraliza la lógica de almacenamiento y recuperación de paquetes sorpresa, comercios y vouchers de reserva.</li>
        <li><strong>Justificación Técnica:</strong> Garantiza el desacoplamiento total de la lógica de negocio respecto a los mecanismos concretos de persistencia. Si el comensal se encuentra en mostrador sin cobertura celular (3G/4G/5G débil), el repositorio entrega el voucher de reserva desde la caché local sin disparar excepciones ni bloquear la UI, permitiendo un canje 100% resiliente (Offline-First).</li>
      </ul>

      <div class="sub-heading">> 2.2 Patrón BLoC (Business Logic Component) / Observer Pattern</div>
      <ul class="bullet-list">
        <li><strong>Uso en SaveBite:</strong> Rige la gestión reactiva de estado en la Capa de Presentación bajo el paradigma de Flujo Unidireccional de Datos (UDF). La interfaz emite eventos discretos (ej. <code>SolicitarReservaEvent</code>, <code>ActualizarFiltroDistanciaEvent</code>), el BLoC procesa la lógica invocando el Caso de Uso y emite nuevos estados inmutables (<code>ReservaCargando</code>, <code>ReservaExitosa</code>, <code>ErrorState</code>) escuchados por la UI mediante Streams de Dart.</li>
        <li><strong>Justificación Técnica:</strong> Elimina de raíz el desorden derivado de llamadas dispersas a <code>setState()</code>, reduciendo el consumo de batería y CPU al evitar repintados innecesarios en el árbol de widgets. Facilita la elaboración de pruebas unitarias automatizadas con la suite <code>bloc_test</code> sin requerir emuladores ni mocks complejos de interfaz.</li>
      </ul>

      <div class="sub-heading">> 2.3 Patrón Service Locator / Singleton (Inyección de Dependencias con GetIt)</div>
      <ul class="bullet-list">
        <li><strong>Uso en SaveBite:</strong> Administra de forma centralizada la instanciación perezosa (Lazy Singleton) de servicios críticos globales, tales como el cliente de red <code>SupabaseClient</code>, el motor de almacenamiento seguro <code>FlutterSecureStorage</code>, los controladores de ubicación satelital y el manejador de notificaciones push.</li>
        <li><strong>Justificación Técnica:</strong> Previene la creación descontrolada de sockets, conexiones HTTP redundantes o relecturas de llaves de cifrado en memoria, disminuyendo el footprint de RAM en el dispositivo móvil y permitiendo inyectar implementaciones ficticias (Mocks) de forma limpia durante las pruebas unitarias.</li>
      </ul>

      <div class="sub-heading">> 2.4 Patrón Factory Method y Data Transfer Object (DTO)</div>
      <ul class="bullet-list">
        <li><strong>Uso en SaveBite:</strong> Encapsula la serialización y deserialización segura de payloads JSON procedentes de la nube hacia entidades inmutables del dominio (<code>FoodPackage</code>, <code>Store</code>, <code>Reservation</code>, <code>EcoImpact</code>) a través de constructores nombrados Factory (ej. <code>FoodPackageModel.fromJson(json)</code>).</li>
        <li><strong>Justificación Técnica:</strong> Otorga tipado fuerte y validación de esquemas en tiempo de compilación. Resguarda a la aplicación contra anomalías de valores nulos imprevistos (Sound Null Safety en Dart 3) y fallos de parseo en caso de inconsistencias remotas.</li>
      </ul>

      <div class="diagram-card">
        <img src="diagram_fase2_patrones_arquitectura.png" alt="Arquitectura y Patrones de Diseño SaveBite">
        <div class="diagram-caption">Figura 1: Arquitectura de Software y Patrones de Diseño Aplicados en SaveBite (Clean Architecture + BLoC + Repository)</div>
      </div>

      <!-- SECCIÓN 3: FRAMEWORKS Y HERRAMIENTAS -->
      <div class="section-header">
        <div class="section-num">3</div>
        <div class="section-title">JUSTIFICACIÓN DE FRAMEWORKS Y HERRAMIENTAS A UTILIZAR</div>
      </div>

      <p>La selección tecnológica de SaveBite responde a una rigurosa evaluación de criterios de ingeniería de software móvil, priorizando rendimiento nativo, reducción de tiempos de desarrollo y soporte a largo plazo:</p>

      <div class="sub-heading">> 3.1 Framework Principal de Desarrollo: Flutter SDK (Dart 3.x)</div>
      <ul class="bullet-list">
        <li><strong>Rendimiento Extremo (Compilación AOT):</strong> Flutter compila directamente a código máquina nativo C/C++ ARM64 mediante Ahead-Of-Time (AOT), eliminando los puentes de JavaScript (presentes en React Native). Gracias a su nuevo motor gráfico Impeller sobre Vulkan/Metal, renderiza animaciones fluidas a 60 y 120 FPS sin caídas de cuadros ni jitter al mover el mapa interactivo.</li>
        <li><strong>Soporte Multiplataforma Real:</strong> Un único código fuente (Single Codebase) genera binarios nativos para Android (APK/AAB) e iOS (IPA), maximizando la productividad del equipo y garantizando paridad total de interfaz y lógica entre ambos sistemas operativos.</li>
        <li><strong>Curva de Aprendizaje y Tipado Fuerte:</strong> Dart 3 implementa Sound Null Safety estricto, pattern matching y records, reduciendo errores en tiempo de ejecución en más del 80%. Su sintaxis orientada a objetos es sumamente intuitiva para desarrolladores con bases en Java/C#.</li>
        <li><strong>Comunidad y Ecosistema pub.dev:</strong> Respaldado directamente por Google y con millones de paquetes mantenidos por la comunidad, pub.dev ofrece librerías de grado productivo para el control de hardware móvil nativo.</li>
      </ul>

      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Tecnología / Herramienta</th>
              <th>Categoría / Función</th>
              <th>Argumentación y Ventaja Técnica</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Flutter SDK 3.x</strong></td>
              <td>Framework UI Móvil</td>
              <td>Compilación AOT nativa C++, motor Impeller a 60 FPS, Material 3 reactivo y soporte multiplataforma unificado.</td>
            </tr>
            <tr>
              <td><strong>Supabase / Firebase BaaS</strong></td>
              <td>Cloud Backend & DB</td>
              <td>Auth JWT, PostgreSQL con PostGIS / Firestore NoSQL, WebSockets en tiempo real y reglas de seguridad RBAC.</td>
            </tr>
            <tr>
              <td><strong>mobile_scanner (CameraX)</strong></td>
              <td>Visor y Decodificador QR</td>
              <td>Escaneo ultrarrápido (<300 ms) integrado directo a los drivers de hardware nativos de la cámara.</td>
            </tr>
            <tr>
              <td><strong>Hive & Secure Storage</strong></td>
              <td>Persistencia Local</td>
              <td>Caché NoSQL binaria ultraligera para modo offline y cifrado de llaves AES-256 en Android KeyStore.</td>
            </tr>
            <tr>
              <td><strong>flutter_lints & DevTools</strong></td>
              <td>Calidad y Profiling</td>
              <td>Análisis estático de código estricto y perfilado en vivo de consumo de memoria y CPU.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- SECCIÓN 4: ESTRATEGIAS DE VERSIONAMIENTO -->
      <div class="section-header">
        <div class="section-num">4</div>
        <div class="section-title">ESTRATEGIAS DE VERSIONAMIENTO Y GESTIÓN DEL CÓDIGO</div>
      </div>

      <p>Para salvaguardar la integridad del código fuente, habilitar la integración continua entre los 4 desarrolladores y prevenir regresiones en las entregas quincenales, se definió una estrategia de versionamiento profesional basada en GitFlow, Semantic Versioning y CI/CD:</p>

      <div class="sub-heading">> 4.1 Estructura del Flujo de Ramas (GitFlow Adaptado)</div>
      <ul class="bullet-list">
        <li><strong>main (Producción):</strong> Rama protegida contra escritura directa. Solo alberga releases estables, etiquetadas y validadas con firmas criptográficas de producción. Requiere Pull Request obligatorio con 2 aprobaciones.</li>
        <li><strong>develop (Integración):</strong> Rama principal de trabajo continuo. Centraliza las funcionalidades validadas en cada Sprint. Es la base para pruebas de control de calidad (QA).</li>
        <li><strong>feature/&lt;nombre&gt;:</strong> Ramas de corta duración nacidas de develop para cada historia de usuario (ej. <code>feature/modulo-mapa-gps</code>, <code>feature/lector-qr-camerax</code>). Se eliminan tras merge.</li>
        <li><strong>release/vX.Y.Z:</strong> Ramas de estabilización previas a un hito de entrega. Se congelan cambios mayores y solo se admiten parches de pulido de UI y documentación.</li>
        <li><strong>hotfix/&lt;incidencia&gt;:</strong> Ramas de emergencia que se originan directamente de main para mitigar vulnerabilidades o errores críticos en producción, integrándose a main y develop.</li>
      </ul>

      <div class="sub-heading">> 4.2 Versionado Semántico (SemVer 2.0.0 + Build Numbers)</div>
      <p>Se adopta la nomenclatura formal <code>MAJOR.MINOR.PATCH+BUILD</code> (ejemplo: <code>v1.0.0+1</code>):</p>
      <ul class="bullet-list">
        <li><strong>MAJOR (1.x.x):</strong> Incrementa ante rupturas de compatibilidad con la API o cambios estructurales en la base de datos.</li>
        <li><strong>MINOR (x.1.x):</strong> Incrementa al incorporar nuevas funcionalidades compatibles hacia atrás (ej. APK v0.2.0 al sumar el módulo de publicación de paquetes).</li>
        <li><strong>PATCH (x.x.1):</strong> Incrementa ante correcciones de errores, bugs menores de interfaz o ajustes de rendimiento.</li>
        <li><strong>BUILD NUMBER (+X):</strong> Entero secuencial autoincrementable requerido por Android (<code>versionCode</code>) para identificar cada compilación física de APK.</li>
      </ul>

      <div class="sub-heading">> 4.3 Convención de Commits Semánticos (Conventional Commits)</div>
      <ul class="bullet-list">
        <li><code>feat(scanner):</code> Implementación de decodificador de códigos QR con Mobile Scanner en cámara.</li>
        <li><code>fix(auth):</code> Resolución de fallo de expiración en refresh tokens JWT de Supabase Auth.</li>
        <li><code>perf(map):</code> Optimización de marcadores de comercios mediante clustering geoespacial en Haversine.</li>
        <li><code>security(voucher):</code> Incorporación de firma criptográfica HMAC-SHA256 en payload de códigos QR.</li>
      </ul>

      <div class="diagram-card">
        <img src="diagram_fase2_versionamiento_gitflow.png" alt="Estrategia GitFlow y CI/CD SaveBite">
        <div class="diagram-caption">Figura 2: Estrategia de Versionamiento GitFlow, SemVer y Automatización CI/CD con GitHub Actions</div>
      </div>

      <!-- SECCIÓN 5: SEGURIDAD Y PRIVACIDAD -->
      <div class="section-header">
        <div class="section-num">5</div>
        <div class="section-title">SEGURIDAD, PRIVACIDAD Y CUMPLIMIENTO LEGAL EN ENTORNOS MÓVILES</div>
      </div>

      <p>La confianza de los estudiantes y de los comercios gastronómicos locales es el pilar de SaveBite. La aplicación implementa una estrategia de <strong>seguridad por diseño (Security by Design)</strong>, alineada rigurosamente con el marco jurídico mexicano y con los estándares internacionales de seguridad móvil:</p>

      <div class="sub-heading">> 5.1 Cumplimiento de la Normativa Local Vigente en México (LFPDPPP e INAI)</div>
      <ul class="bullet-list">
        <li><strong>Principio de Licitud:</strong> El tratamiento de los datos personales de estudiantes y dueños de negocios se apega estrictamente a las leyes mexicanas y al orden público.</li>
        <li><strong>Principio de Consentimiento:</strong> Se recaba el consentimiento expreso y verificable del usuario mediante un opt-in activo durante el registro previo a recopilar cualquier información personal o activar permisos de hardware.</li>
        <li><strong>Principio de Información (Avisos de Privacidad):</strong> SaveBite despliega dos modalidades: 1) Aviso de Privacidad Simplificado al solicitar acceso al GPS y cámara, y 2) Aviso de Privacidad Integral accesible permanentemente desde los ajustes de la app y portal web.</li>
        <li><strong>Principio de Finalidad y Lealtad:</strong> La información recolectada se utiliza exclusivamente para la reserva, canje de alimentos y cálculo de métricas ODS. Queda terminantemente prohibida su comercialización o perfilamiento publicitario a terceros.</li>
        <li><strong>Principio de Proporcionalidad (Minimización):</strong> Únicamente se solicitan los datos indispensables para ejecutar la transacción. No se solicitan contactos de la agenda, acceso a fotos privadas ni SMS.</li>
        <li><strong>Ejercicio de Derechos ARCO:</strong> La aplicación provee una sección directa en el perfil del usuario para ejercer sus derechos de Acceso, Rectificación, Cancelación y Oposición de sus datos.</li>
      </ul>

      <div class="sub-heading">> 5.2 Principios de Codificación Segura Móvil (OWASP Mobile Top 10 & MASVS)</div>
      <ul class="bullet-list">
        <li><strong>M1 - Almacenamiento Seguro:</strong> Las llaves de sesión, tokens JWT y credenciales se guardan exclusivamente en el hardware criptográfico nativo: Android KeyStore (AES-256-GCM) y iOS Keychain mediante <code>flutter_secure_storage</code>.</li>
        <li><strong>M2 - Criptografía Robusta en Vouchers QR:</strong> El código QR contiene un token firmado con HMAC-SHA256 que incluye el identificador de reserva, un Nonce aleatorio de un solo uso y un Timestamp de caducidad (ventana de recogida de 60 min).</li>
        <li><strong>M3 - Comunicaciones Cifradas en Tránsito:</strong> Conexiones forzadas bajo TLS 1.3 / HTTPS. En <code>AndroidManifest.xml</code> se declara <code>android:usesCleartextTraffic="false"</code>.</li>
        <li><strong>M4 - Autenticación y Autorización Robusta:</strong> Tokens JWT efímeros firmados por el servidor con expiración de 1 hora y refresh tokens rotativos con control RBAC en base de datos.</li>
        <li><strong>M5 - Validación Estricta de Entradas:</strong> Sanitización exhaustiva en cliente Flutter y servidor en la nube, bloqueando inyecciones SQL, NoSQL y ataques XSS.</li>
        <li><strong>M6 - Protección de Binarios y Ofuscación:</strong> Compilación AOT nativa y configuración de ProGuard/R8 con ofuscación de nombres de clases y métodos en el APK Release.</li>
      </ul>

      <div class="sub-heading">> 5.3 Checklist Exhaustivo de Seguridad para Entornos Móviles</div>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Categoría</th>
              <th>Control Técnico / Criterio</th>
              <th>Estado</th>
              <th>Mecanismo / Herramienta</th>
              <th>Responsable</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Autenticación</td>
              <td>Almacenamiento seguro de tokens JWT sin exposición en logs ni caché.</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>FlutterSecureStorage / KeyStore</td>
              <td>Diego Villegas</td>
            </tr>
            <tr>
              <td>Autenticación</td>
              <td>Sesiones efímeras con refresh tokens rotativos y revocación remota.</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>Supabase Auth / RLS</td>
              <td>Diego Villegas</td>
            </tr>
            <tr>
              <td>Comunicaciones</td>
              <td>Tráfico cifrado mandatorio TLS 1.3 en todas las peticiones de red.</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>HTTPS / android:usesCleartextTraffic</td>
              <td>Diego Villegas</td>
            </tr>
            <tr>
              <td>Comunicaciones</td>
              <td>Bloqueo de certificados autofirmados e inspección de proxys MitM.</td>
              <td><span class="tag-status progress">En Proceso</span></td>
              <td>Network Security Config (Android)</td>
              <td>Guillermo Berlín</td>
            </tr>
            <tr>
              <td>Criptografía</td>
              <td>Vouchers QR firmados con token HMAC-SHA256 y timestamp de expiración.</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>Crypto Dart / CameraX Scanner</td>
              <td>Juan Pablo Vega</td>
            </tr>
            <tr>
              <td>Criptografía</td>
              <td>Caché de vouchers offline cifrada en base de datos local NoSQL.</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>Hive Encrypted Box (AES-256)</td>
              <td>Diego Villegas</td>
            </tr>
            <tr>
              <td>Almacenamiento</td>
              <td>Prohibición de volcado de datos sensibles en SQLite o SharedPrefs.</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>Code Review / Static Lints</td>
              <td>Guillermo Berlín</td>
            </tr>
            <tr>
              <td>Privacidad</td>
              <td>Aviso de Privacidad Integral y Simplificado conforme a LFPDPPP.</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>Pantalla Legal / Dialog Consent</td>
              <td>Alvaro Chávez</td>
            </tr>
            <tr>
              <td>Privacidad</td>
              <td>Acceso a GPS solo durante el uso activo de la app (Foreground Only).</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>geolocator (ACCESS_FINE_LOCATION)</td>
              <td>Juan Pablo Vega</td>
            </tr>
            <tr>
              <td>Privacidad</td>
              <td>Mecanismo interactivo para ejercicio de Derechos ARCO y borrado de cuenta.</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>Endpoint Serverless / Ajustes Perfil</td>
              <td>Alvaro Chávez</td>
            </tr>
            <tr>
              <td>Plataforma</td>
              <td>Ofuscación de código fuente y eliminación de símbolos en el APK Release.</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>ProGuard / R8 / Dart Obfuscation</td>
              <td>Guillermo Berlín</td>
            </tr>
            <tr>
              <td>Plataforma</td>
              <td>Validación estricta de formato y rango en formularios de publicación.</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>Form Validators & RegExp en Dart</td>
              <td>Juan Pablo Vega</td>
            </tr>
            <tr>
              <td>Resiliencia</td>
              <td>Timeouts de red configurados y manejo elegante de pérdida de señal.</td>
              <td><span class="tag-status done">Implementado</span></td>
              <td>BLoC Exception Handlers</td>
              <td>Juan Pablo Vega</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- SECCIÓN 6: ECOSISTEMA DE SERVICIOS -->
      <div class="section-header">
        <div class="section-num">6</div>
        <div class="section-title">ECOSISTEMA DE SERVICIOS E INTEGRACIÓN CLOUD</div>
      </div>

      <p>SaveBite combina de forma sinérgica APIs de terceros de clase mundial con una infraestructura en la nube elástica (Cloud BaaS) para brindar una experiencia inmediata tanto al comensal universitario como al dueño del establecimiento comercial:</p>

      <div class="sub-heading">> 6.1 Consumo de APIs de Terceros</div>
      <ul class="bullet-list">
        <li><strong>Google Maps Platform & Places API:</strong> Provee mapas vectoriales fluidos para Android e iOS. Se utiliza el servicio de geocodificación inversa y cálculo de distancias geodésicas mediante la fórmula de Haversine para listar en tiempo real los comercios con paquetes activos a menos de 3 km del estudiante.</li>
        <li><strong>Pasarela de Pagos Digitales (Stripe / Mercado Pago SDK):</strong> Permite cobros seguros in-app mediante tarjetas de débito/crédito y transferencias electrónicas SPEI. Cumple la certificación PCI-DSS Nivel 1 mediante tokenización de tarjetas: la app jamás toca ni almacena datos financieros del comprador.</li>
        <li><strong>Autenticación Federada (Google Sign-In OAuth 2.0):</strong> Facilita el registro y login en un solo toque mediante cuentas de Google institucionales (@utsalamanca.edu.mx) o personales, disminuyendo la fricción inicial de adopción.</li>
        <li><strong>Motor de Cámara y Escaneo (Mobile Scanner / Google ML Kit Vision):</strong> Procesa el stream de video de la cámara física a 60 FPS mediante los subsistemas nativos CameraX (Android) y AVFoundation (iOS) decodificando códigos QR en menos de 300 ms en el mostrador.</li>
      </ul>

      <div class="sub-heading">> 6.2 Arquitectura Cloud y Servicios Críticos en la Nube</div>
      <ul class="bullet-list">
        <li><strong>Supabase Auth / Firebase Auth:</strong> Gestión centralizada de identidades con tokens criptográficos JWT y hashing seguro de contraseñas con algoritmos Argon2 / bcrypt.</li>
        <li><strong>Base de Datos en Tiempo Real y Espacial (PostgreSQL PostGIS / Cloud Firestore):</strong> Almacena el catálogo de paquetes y comercios con soporte geoespacial. Mediante suscripciones por WebSockets / Streams, el mapa se sincroniza al instante cuando un usuario reserva un paquete.</li>
        <li><strong>Almacenamiento de Archivos (Cloud Storage):</strong> Buckets seguros compatibles con S3 para fotos de locales y comida, optimizadas en WebP con CDN para reducir el consumo de megabytes.</li>
        <li><strong>Notificaciones Push en Tiempo Real (Firebase Cloud Messaging - FCM):</strong> Envío de alertas automáticas al celular cuando un comercio favorito publica ofertas y recordatorios preventivos cuando restan 30 minutos de la ventana de recogida.</li>
        <li><strong>Lógica Serverless (Edge Functions):</strong> Microservicios que liberan automáticamente reservas no reclamadas y consolidan los reportes de kg de comida rescatada y CO2 mitigado.</li>
      </ul>

      <div class="diagram-card">
        <img src="diagram_fase2_ecosistema_integracion.png" alt="Ecosistema Cloud SaveBite">
        <div class="diagram-caption">Figura 3: Ecosistema de Servicios e Integración Cloud en SaveBite (BaaS, APIs y Hardware)</div>
      </div>

      <!-- SECCIÓN 7: CAPTURAS DEL AVANCE DE LA APP -->
      <div class="section-header">
        <div class="section-num">7</div>
        <div class="section-title">EVIDENCIAS Y CAPTURAS DEL AVANCE DE LA APP REVISADAS EN CLASE</div>
      </div>

      <p>Durante las sesiones prácticas y revisiones de Sprint en clase con la docente <strong>Ericka Nohemí Álvarez Valencia</strong>, el equipo presentó avances funcionales de los componentes core de SaveBite. A continuación se presentan las evidencias de las pantallas operativas implementadas en Flutter:</p>

      <div class="mockups-grid">
        <div class="mockup-item">
          <img src="screen_1_auth.png" alt="Pantalla de Splash & Auth">
          <div class="mockup-title">1. Splash & Multi-Rol</div>
          <div class="mockup-sub">Acceso Alumno / Comercio Aliado</div>
        </div>
        <div class="mockup-item">
          <img src="screen_2_explore_map.png" alt="Pantalla de Mapa GPS">
          <div class="mockup-title">2. Mapa GPS & Feed</div>
          <div class="mockup-sub">Comercios y Ofertas -65% en Vivo</div>
        </div>
        <div class="mockup-item">
          <img src="screen_3_package_detail.png" alt="Ficha Detallada de Paquete">
          <div class="mockup-title">3. Ficha de Paquete</div>
          <div class="mockup-sub">Reserva In-App con 1 Toque</div>
        </div>
        <div class="mockup-item">
          <img src="screen_4_voucher_qr.png" alt="Voucher QR Dinámico">
          <div class="mockup-title">4. Voucher QR Dinámico</div>
          <div class="mockup-sub">Token HMAC y Modo Offline</div>
        </div>
        <div class="mockup-item">
          <img src="screen_5_scanner.png" alt="Escáner QR de Mostrador">
          <div class="mockup-title">5. Escáner de Comercio</div>
          <div class="mockup-sub">Lectura Cámara CameraX (<2s)</div>
        </div>
        <div class="mockup-item">
          <img src="screen_6_eco_impact.png" alt="Calculadora de Impacto ODS">
          <div class="mockup-title">6. Impacto ODS 12</div>
          <div class="mockup-sub">Métricas CO2, Dinero y Alimentos</div>
        </div>
      </div>

      <!-- SECCIÓN 8: CONCLUSIONES POR ROL -->
      <div class="section-header">
        <div class="section-num">8</div>
        <div class="section-title">CONCLUSIÓN DE LA FASE 2 POR INTEGRANTE SEGÚN SU ROL</div>
      </div>

      <p>A continuación se presentan las conclusiones individuales de los cuatro integrantes del equipo de IDGS, fundamentando los aprendizajes, contribuciones técnicas y valor aportado al proyecto SaveBite de acuerdo con el rol que desempeñaron:</p>

      <div class="conclusions-grid">
        <div class="conclusion-card">
          <div class="conclusion-header">
            <div class="conclusion-author">Alvaro Jesús Chávez Bazana</div>
            <div class="conclusion-role">Product Owner (PO) — Gestor de Requisitos</div>
          </div>
          <p class="conclusion-text">Desde la perspectiva del Product Owner, la consolidación de la Fase 2 representa la maduración técnica indispensable para materializar la propuesta de valor de SaveBite. Al definir una arquitectura desacoplada y un ecosistema de servicios robusto, garantizamos que la solución no sea solo un prototipo académico, sino una plataforma viable que resuelve una problemática real de merma alimentaria en Salamanca bajo el ODS 12. La integración de la calculadora de impacto ecológico y la transparencia jurídica derivada de la LFPDPPP otorgan certeza y confianza plena tanto al estudiante que busca cuidar su economía como al comerciante aliado que desea evitar desperdicios y dinamizar su inventario.</p>
        </div>

        <div class="conclusion-card">
          <div class="conclusion-header">
            <div class="conclusion-author">Guillermo Yael Berlín Fomperosa</div>
            <div class="conclusion-role">Scrum Master (SM) — Facilitador & QA</div>
          </div>
          <p class="conclusion-text">Como Scrum Master y responsable del aseguramiento de calidad (QA), la definición del flujo de versionamiento con GitFlow, la política de Conventional Commits y la automatización del pipeline en GitHub Actions han transformado radicalmente la sinergia del equipo. Se eliminaron por completo las fricciones por conflictos de ramas y se garantizó que ningún código con advertencias de linter o pruebas unitarias fallidas llegue a la rama principal. Asimismo, la implementación del checklist de seguridad nos brinda un marco de verificación continuo y riguroso para auditar cada entrega quincenal antes de presentarla a la docente, asegurando un producto libre de deuda técnica.</p>
        </div>

        <div class="conclusion-card">
          <div class="conclusion-header">
            <div class="conclusion-author">Juan Pablo Vega Uribe</div>
            <div class="conclusion-role">Lead Mobile Developer — Frontend & UI/UX</div>
          </div>
          <p class="conclusion-text">En mi rol de desarrollador frontend líder y diseñador de la experiencia de usuario, la adopción del patrón BLoC en conjunto con Flutter SDK 3.x ha demostrado ser la decisión más acertada. La separación estricta entre los widgets visuales y la lógica de estado permitió lograr una interfaz reactiva, moderna con Material 3 y extraordinariamente fluida a 60 FPS, incluso durante la manipulación de marcadores en el mapa interactivo con Google Maps. La optimización del visor de cámara con Mobile Scanner sobre CameraX logró reducir la latencia de detección del código QR a menos de 300 ms, garantizando una validación en mostrador inmediata y sin fricciones.</p>
        </div>

        <div class="conclusion-card">
          <div class="conclusion-header">
            <div class="conclusion-author">Diego Sebastián Vilegas Enriquez</div>
            <div class="conclusion-role">Backend & Data Architect — Cloud BaaS & Offline</div>
          </div>
          <p class="conclusion-text">Desde el ámbito de la arquitectura de datos y servicios en la nube, el mayor desafío y satisfacción técnica de esta Fase 2 fue diseñar la resiliencia Offline-First mediante el Repository Pattern. Al combinar la base de datos documental en tiempo real y el control de acceso por roles (RBAC) en la nube con la caché binaria local de Hive y el hardware criptográfico de Android KeyStore, blindamos por completo los vouchers de canje con firmas HMAC-SHA256. Esto asegura que la transacción sea inalterable, segura y ejecutable en cualquier circunstancia, cumpliendo cabalmente con la normativa mexicana de protección de datos personales.</p>
        </div>
      </div>

    </div>

    <!-- PIE DEL DOCUMENTO -->
    <div class="footer-note">
      Salamanca, Guanajuato, México — Universidad Tecnológica de Salamanca (UTS) • División TIC • IDGS 10° Cuatrimestre<br>
      Asignatura: Desarrollo Móvil Integral — Docente: Ericka Nohemí Álvarez Valencia
    </div>
  </div>

</body>
</html>
"""

with open("Fase2_Plan_Desarrollo_Movil_SaveBite.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML Fase 2 SaveBite generado con éxito.")
