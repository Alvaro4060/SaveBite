import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_strings.dart';
import '../../../core/constants/app_styles.dart';
import '../../../core/utils/formatters.dart';
import '../../state/app_state.dart';
import '../../widgets/custom_button.dart';
import 'create_package_screen.dart';
import 'qr_scanner_screen.dart';

class MerchantDashboardScreen extends StatelessWidget {
  const MerchantDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final user = appState.currentUser;
    final merchantPackages = appState.merchantPackages;

    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 80),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Tarjeta del Establecimiento
          Container(
            padding: const EdgeInsets.all(18),
            decoration: BoxDecoration(
              gradient: AppColors.heroGradient,
              borderRadius: BorderRadius.circular(20),
              boxShadow: const [
                BoxShadow(
                  color: Color.fromRGBO(15, 76, 129, 0.15),
                  blurRadius: 12,
                  offset: Offset(0, 4),
                ),
              ],
            ),
            child: Row(
              children: [
                Container(
                  width: 50,
                  height: 50,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(14),
                  ),
                  alignment: Alignment.center,
                  child: const Text('🥖', style: TextStyle(fontSize: 26)),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        user.storeName ?? 'Comercio Aliado',
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w900,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 2),
                      const Text(
                        'Centro Histórico, Salamanca • ODS 12',
                        style: TextStyle(
                          fontSize: 12,
                          color: Color(0xFFBFDBFE),
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.accent,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Text(
                    'ABIERTO',
                    style: TextStyle(fontSize: 10.5, fontWeight: FontWeight.w900, color: Colors.white),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 18),

          // Métricas del Día
          Row(
            children: [
              Expanded(
                child: _MetricCard(
                  label: AppStrings.activePacksCount,
                  value: merchantPackages.length.toString(),
                  icon: Icons.inventory_2_outlined,
                  color: AppColors.primary,
                ),
              ),
              const SizedBox(width: 10),
              const Expanded(
                child: _MetricCard(
                  label: AppStrings.redeemedToday,
                  value: '4',
                  icon: Icons.qr_code_scanner_rounded,
                  color: AppColors.success,
                ),
              ),
              const SizedBox(width: 10),
              const Expanded(
                child: _MetricCard(
                  label: AppStrings.totalSavedKg,
                  value: '6.2 kg',
                  icon: Icons.eco_rounded,
                  color: AppColors.accent,
                ),
              ),
            ],
          ),

          const SizedBox(height: 20),

          // Botones de Acción Rápida para el Comerciante
          Row(
            children: [
              Expanded(
                child: CustomButton(
                  text: 'Publicar Pack',
                  icon: Icons.add_circle_outline,
                  backgroundColor: AppColors.accent,
                  height: 48,
                  onPressed: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => const CreatePackageScreen()),
                    );
                  },
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: CustomButton(
                  text: 'Escanear QR',
                  icon: Icons.qr_code_scanner,
                  backgroundColor: AppColors.primary,
                  height: 48,
                  onPressed: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => const QrScannerScreen()),
                    );
                  },
                ),
              ),
            ],
          ),

          const SizedBox(height: 24),

          // Listado de Paquetes Publicados por este Comercio
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Tus Paquetes Publicados Hoy', style: AppStyles.heading3),
              Text(
                '${merchantPackages.length} activos',
                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textSecondary),
              ),
            ],
          ),
          const SizedBox(height: 12),

          if (merchantPackages.isEmpty)
            Container(
              padding: const EdgeInsets.all(24),
              decoration: AppStyles.cardDecoration,
              alignment: Alignment.center,
              child: const Column(
                children: [
                  Icon(Icons.inventory_2_outlined, size: 40, color: AppColors.textMuted),
                  SizedBox(height: 8),
                  Text('No tienes paquetes sorpresa publicados', style: AppStyles.bodyBold),
                  SizedBox(height: 4),
                  Text(
                    'Publica tus excedentes del día para que la comunidad pueda rescatarlos.',
                    style: AppStyles.caption,
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            )
          else
            ...merchantPackages.map((pkg) => _MerchantPackageItem(package: pkg)),
        ],
      ),
    );
  }
}

class _MetricCard extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color color;

  const _MetricCard({
    required this.label,
    required this.value,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: AppStyles.cardDecoration,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 20),
          const SizedBox(height: 8),
          Text(
            value,
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w900,
              color: color,
            ),
          ),
          const SizedBox(height: 2),
          Text(
            label,
            style: const TextStyle(fontSize: 11, color: AppColors.textSecondary, fontWeight: FontWeight.w500),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }
}

class _MerchantPackageItem extends StatelessWidget {
  final dynamic package;

  const _MerchantPackageItem({required this.package});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(14),
      decoration: AppStyles.cardDecoration,
      child: Row(
        children: [
          Container(
            width: 44,
            height: 44,
            decoration: BoxDecoration(
              color: AppColors.surfaceMuted,
              borderRadius: BorderRadius.circular(10),
            ),
            alignment: Alignment.center,
            child: Text(package.categoryEmoji, style: const TextStyle(fontSize: 22)),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  package.title,
                  style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 2),
                Text(
                  'Horario: ${package.pickupTimeWindow}',
                  style: const TextStyle(fontSize: 11, color: AppColors.accentHover, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 2),
                Text(
                  'Precio: ${Formatters.formatCurrency(package.discountedPrice)} (Original: ${Formatters.formatCurrency(package.originalPrice)})',
                  style: const TextStyle(fontSize: 11, color: AppColors.textSecondary),
                ),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            decoration: BoxDecoration(
              color: AppColors.primary.withOpacity(0.08),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              '${package.remainingStock} disp.',
              style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w800, color: AppColors.primary),
            ),
          ),
        ],
      ),
    );
  }
}
