import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';
import '../../core/constants/app_strings.dart';
import '../../domain/entities/user_profile.dart';
import '../state/app_state.dart';
import 'explore/explore_feed_screen.dart';
import 'reservations/reservations_screen.dart';
import 'impact/impact_calculator_screen.dart';
import 'merchant/merchant_dashboard_screen.dart';
import 'merchant/qr_scanner_screen.dart';
import 'merchant/create_package_screen.dart';
import 'merchant/merchant_sales_history_screen.dart';
import 'profile/profile_screen.dart';
import 'auth/login_screen.dart';

class MainShellScreen extends StatelessWidget {
  const MainShellScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final isMerchant = appState.isMerchant;

    // Pantallas por Rol
    final List<Widget> consumerScreens = [
      const ExploreFeedScreen(),
      const ReservationsScreen(),
      const ImpactCalculatorScreen(),
    ];

    final List<Widget> merchantScreens = [
      const MerchantDashboardScreen(),
      const QrScannerScreen(),
      const MerchantSalesHistoryScreen(),
    ];

    final activeScreens = isMerchant ? merchantScreens : consumerScreens;
    final currentIndex = appState.currentTabIndex < activeScreens.length
        ? appState.currentTabIndex
        : 0;

    return Scaffold(
      appBar: AppBar(
        titleSpacing: 16,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: isMerchant ? AppColors.accent : AppColors.primary,
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(
                isMerchant ? Icons.storefront_rounded : Icons.shopping_bag_outlined,
                color: Colors.white,
                size: 20,
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Text(
                        AppStrings.appName,
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w900,
                          color: AppColors.primary,
                        ),
                      ),
                      const SizedBox(width: 6),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: isMerchant
                              ? AppColors.accent.withOpacity(0.15)
                              : AppColors.secondary.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          isMerchant ? 'COMERCIO' : 'CONSUMIDOR',
                          style: TextStyle(
                            fontSize: 9.5,
                            fontWeight: FontWeight.w800,
                            color: isMerchant ? AppColors.accentHover : AppColors.secondaryDark,
                            letterSpacing: 0.5,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const Text(
                    'Salamanca, Gto.',
                    style: TextStyle(
                      fontSize: 11,
                      color: AppColors.textSecondary,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        actions: [
          // Menú Desplegable de Usuario Estilizado
          PopupMenuButton<String>(
            tooltip: 'Menú de Usuario',
            elevation: 12,
            shadowColor: Colors.black38,
            color: Colors.white,
            surfaceTintColor: Colors.transparent,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(20),
              side: const BorderSide(color: Color(0xFFE2E8F0), width: 1),
            ),
            offset: const Offset(0, 48),
            constraints: const BoxConstraints(minWidth: 265, maxWidth: 300),
            icon: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 5),
              decoration: BoxDecoration(
                color: isMerchant
                    ? AppColors.accent.withOpacity(0.12)
                    : AppColors.primary.withOpacity(0.08),
                borderRadius: BorderRadius.circular(24),
                border: Border.all(
                  color: isMerchant
                      ? AppColors.accent.withOpacity(0.35)
                      : AppColors.primary.withOpacity(0.25),
                  width: 1.2,
                ),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  CircleAvatar(
                    radius: 12,
                    backgroundColor: isMerchant ? AppColors.accent : AppColors.primary,
                    child: Text(
                      appState.currentUser.avatarInitials,
                      style: const TextStyle(
                        fontSize: 10,
                        color: Colors.white,
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                  ),
                  const SizedBox(width: 4),
                  Icon(
                    Icons.keyboard_arrow_down_rounded,
                    size: 18,
                    color: isMerchant ? AppColors.accentHover : AppColors.primary,
                  ),
                ],
              ),
            ),
            onSelected: (value) {
              if (value == 'view_profile') {
                Navigator.of(context).push(
                  MaterialPageRoute(builder: (_) => const ProfileScreen()),
                );
              } else if (value == 'switch_role') {
                appState.switchRole(
                  isMerchant ? UserRole.consumer : UserRole.merchant,
                );
              } else if (value == 'toggle_offline') {
                appState.toggleOfflineMode();
              } else if (value == 'logout') {
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (_) => const LoginScreen()),
                );
              }
            },
            itemBuilder: (context) => [
              // 1. Tarjeta resumen de Perfil (Header con Gradiente y Avatar)
              PopupMenuItem<String>(
                value: 'view_profile',
                padding: const EdgeInsets.fromLTRB(10, 8, 10, 4),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                  decoration: BoxDecoration(
                    gradient: isMerchant ? AppColors.accentGradient : AppColors.heroGradient,
                    borderRadius: BorderRadius.circular(14),
                    boxShadow: [
                      BoxShadow(
                        color: (isMerchant ? AppColors.accent : AppColors.primary).withOpacity(0.25),
                        blurRadius: 8,
                        offset: const Offset(0, 3),
                      ),
                    ],
                  ),
                  child: Row(
                    children: [
                      CircleAvatar(
                        radius: 17,
                        backgroundColor: Colors.white,
                        child: Text(
                          appState.currentUser.avatarInitials,
                          style: TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w900,
                            color: isMerchant ? AppColors.accent : AppColors.primary,
                          ),
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              appState.currentUser.name,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.w800,
                                fontSize: 13,
                              ),
                            ),
                            const SizedBox(height: 2),
                            Row(
                              children: [
                                Text(
                                  isMerchant ? 'Ver Perfil Comercial' : 'Ver Mi Perfil',
                                  style: TextStyle(
                                    color: Colors.white.withOpacity(0.9),
                                    fontSize: 11,
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                                const SizedBox(width: 3),
                                const Icon(Icons.arrow_forward_ios_rounded, color: Colors.white70, size: 9),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),

              const PopupMenuDivider(height: 12),

              // 2. Cambiar de Rol (Consumidor <-> Comercio)
              PopupMenuItem<String>(
                value: 'switch_role',
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(7),
                      decoration: BoxDecoration(
                        color: (isMerchant ? AppColors.primary : AppColors.accent).withOpacity(0.12),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Icon(
                        isMerchant ? Icons.person_rounded : Icons.storefront_rounded,
                        color: isMerchant ? AppColors.primary : AppColors.accent,
                        size: 18,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            isMerchant ? 'Modo Consumidor' : 'Modo Comercio',
                            style: const TextStyle(
                              fontSize: 12.5,
                              fontWeight: FontWeight.w700,
                              color: AppColors.textPrimary,
                            ),
                          ),
                          const Text(
                            'Alternar vista de prueba',
                            style: TextStyle(fontSize: 10.5, color: AppColors.textSecondary),
                          ),
                        ],
                      ),
                    ),
                    const Icon(Icons.swap_horiz_rounded, size: 18, color: AppColors.textMuted),
                  ],
                ),
              ),

              // 3. Simular / Alternar Modo Offline
              PopupMenuItem<String>(
                value: 'toggle_offline',
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(7),
                      decoration: BoxDecoration(
                        color: (appState.isOfflineMode ? AppColors.warning : AppColors.success).withOpacity(0.12),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Icon(
                        appState.isOfflineMode ? Icons.wifi_off_rounded : Icons.wifi_rounded,
                        color: appState.isOfflineMode ? AppColors.warning : AppColors.success,
                        size: 18,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            appState.isOfflineMode ? 'Desactivar Offline' : 'Modo Offline',
                            style: const TextStyle(
                              fontSize: 12.5,
                              fontWeight: FontWeight.w700,
                              color: AppColors.textPrimary,
                            ),
                          ),
                          Text(
                            appState.isOfflineMode ? 'Operando con caché' : 'Conectado a la nube',
                            style: const TextStyle(fontSize: 10.5, color: AppColors.textSecondary),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: (appState.isOfflineMode ? AppColors.warning : AppColors.success).withOpacity(0.15),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(
                        appState.isOfflineMode ? 'OFF' : 'ONLINE',
                        style: TextStyle(
                          fontSize: 9,
                          fontWeight: FontWeight.w800,
                          color: appState.isOfflineMode ? AppColors.warning : AppColors.success,
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              const PopupMenuDivider(height: 12),

              // 4. Cerrar Sesión
              PopupMenuItem<String>(
                value: 'logout',
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(7),
                      decoration: BoxDecoration(
                        color: AppColors.error.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: const Icon(Icons.logout_rounded, color: AppColors.error, size: 18),
                    ),
                    const SizedBox(width: 12),
                    const Expanded(
                      child: Text(
                        'Cerrar Sesión',
                        style: TextStyle(
                          fontSize: 12.5,
                          fontWeight: FontWeight.w700,
                          color: AppColors.error,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(width: 8),
        ],
      ),

      // Banner Offline si está activado
      body: Column(
        children: [
          if (appState.isOfflineMode)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 12),
              color: AppColors.dark,
              child: const Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.wifi_off_rounded, color: Colors.amber, size: 15),
                  SizedBox(width: 6),
                  Flexible(
                    child: Text(
                      'Modo Offline Activo • Usando caché local',
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.white, fontSize: 11.5, fontWeight: FontWeight.w600),
                    ),
                  ),
                ],
              ),
            ),
          Expanded(child: activeScreens[currentIndex]),
        ],
      ),

      // Barra de Navegación Inferior Adaptada por Rol
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: currentIndex,
        onTap: (index) => appState.setTabIndex(index),
        type: BottomNavigationBarType.fixed,
        selectedItemColor: isMerchant ? AppColors.accentHover : AppColors.primary,
        unselectedItemColor: AppColors.textMuted,
        selectedFontSize: 11,
        unselectedFontSize: 11,
        items: isMerchant
            ? const [
                BottomNavigationBarItem(
                  icon: Icon(Icons.dashboard_outlined),
                  activeIcon: Icon(Icons.dashboard_rounded),
                  label: 'Packs Tienda',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.qr_code_scanner_rounded),
                  activeIcon: Icon(Icons.qr_code_scanner_rounded),
                  label: 'Escanear QR',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.receipt_long_outlined),
                  activeIcon: Icon(Icons.receipt_long_rounded),
                  label: 'Ventas & Corte',
                ),
              ]
            : [
                const BottomNavigationBarItem(
                  icon: Icon(Icons.explore_outlined),
                  activeIcon: Icon(Icons.explore_rounded),
                  label: AppStrings.navExplore,
                ),
                BottomNavigationBarItem(
                  icon: Badge(
                    label: Text(appState.pendingReservations.length.toString()),
                    isLabelVisible: appState.pendingReservations.isNotEmpty,
                    child: const Icon(Icons.confirmation_number_outlined),
                  ),
                  activeIcon: const Icon(Icons.confirmation_number_rounded),
                  label: AppStrings.navReservations,
                ),
                const BottomNavigationBarItem(
                  icon: Icon(Icons.eco_outlined),
                  activeIcon: Icon(Icons.eco_rounded),
                  label: AppStrings.navImpact,
                ),
              ],
      ),
    );
  }
}
