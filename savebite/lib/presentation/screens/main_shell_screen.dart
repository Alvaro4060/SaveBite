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
      const CreatePackageScreen(),
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
            Column(
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
          ],
        ),
        actions: [
          // Switch rápido de Perfil / Rol (Ideal para pruebas en vivo)
          PopupMenuButton<String>(
            tooltip: 'Cambiar Perfil / Modo',
            icon: Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              decoration: BoxDecoration(
                color: AppColors.surfaceMuted,
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: AppColors.border),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  CircleAvatar(
                    radius: 11,
                    backgroundColor: isMerchant ? AppColors.accent : AppColors.primary,
                    child: Text(
                      appState.currentUser.avatarInitials,
                      style: const TextStyle(fontSize: 10, color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                  const SizedBox(width: 4),
                  const Icon(Icons.arrow_drop_down, size: 18, color: AppColors.textSecondary),
                ],
              ),
            ),
            onSelected: (value) {
              if (value == 'switch_role') {
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
              PopupMenuItem(
                value: 'switch_role',
                child: Row(
                  children: [
                    Icon(
                      isMerchant ? Icons.person_outline_rounded : Icons.storefront_outlined,
                      color: AppColors.primary,
                      size: 20,
                    ),
                    const SizedBox(width: 10),
                    Text(
                      isMerchant ? 'Cambiar a Modo Consumidor' : 'Cambiar a Modo Comercio',
                      style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                    ),
                  ],
                ),
              ),
              PopupMenuItem(
                value: 'toggle_offline',
                child: Row(
                  children: [
                    Icon(
                      appState.isOfflineMode ? Icons.wifi : Icons.wifi_off,
                      color: appState.isOfflineMode ? AppColors.success : AppColors.warning,
                      size: 20,
                    ),
                    const SizedBox(width: 10),
                    Text(
                      appState.isOfflineMode ? 'Desactivar Modo Offline' : 'Simular Modo Offline',
                      style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                    ),
                  ],
                ),
              ),
              const PopupMenuDivider(),
              const PopupMenuItem(
                value: 'logout',
                child: Row(
                  children: [
                    Icon(Icons.logout_rounded, color: AppColors.error, size: 20),
                    SizedBox(width: 10),
                    Text(
                      'Cerrar Sesión',
                      style: TextStyle(color: AppColors.error, fontWeight: FontWeight.w600, fontSize: 13),
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
              padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 16),
              color: AppColors.dark,
              child: const Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.wifi_off_rounded, color: Colors.amber, size: 16),
                  SizedBox(width: 8),
                  Text(
                    'Modo Offline Activo: Vouchers cargados desde la caché local',
                    style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600),
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
        selectedItemColor: isMerchant ? AppColors.accentHover : AppColors.primary,
        unselectedItemColor: AppColors.textMuted,
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
                  icon: Icon(Icons.add_circle_outline_rounded),
                  activeIcon: Icon(Icons.add_circle_rounded),
                  label: 'Publicar Pack',
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
