import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_strings.dart';
import '../../../core/constants/app_styles.dart';
import '../../../core/utils/formatters.dart';
import '../../../domain/entities/food_package.dart';
import '../../../domain/entities/reservation.dart';
import '../../state/app_state.dart';
import '../../widgets/custom_button.dart';
import 'create_package_screen.dart';
import 'qr_scanner_screen.dart';

class MerchantDashboardScreen extends StatelessWidget {
  const MerchantDashboardScreen({super.key});

  void _showEditPackageDialog(BuildContext context, FoodPackage package, AppState appState) {
    final titleCtrl = TextEditingController(text: package.title);
    final discPriceCtrl = TextEditingController(text: package.discountedPrice.toStringAsFixed(0));
    final origPriceCtrl = TextEditingController(text: package.originalPrice.toStringAsFixed(0));
    final windowCtrl = TextEditingController(text: package.pickupTimeWindow);
    final stockCtrl = TextEditingController(text: package.remainingStock.toString());

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Editar Paquete Sorpresa', style: AppStyles.heading3),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: titleCtrl,
                decoration: const InputDecoration(labelText: 'Título del Paquete'),
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: discPriceCtrl,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(labelText: 'Precio Rescate (\$ MXN)'),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: TextField(
                      controller: origPriceCtrl,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(labelText: 'Original (\$ MXN)'),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: stockCtrl,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(labelText: 'Stock Disp.'),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: TextField(
                      controller: windowCtrl,
                      decoration: const InputDecoration(labelText: 'Horario Recogida'),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () {
              final newTitle = titleCtrl.text.trim();
              final newDisc = double.tryParse(discPriceCtrl.text) ?? package.discountedPrice;
              final newOrig = double.tryParse(origPriceCtrl.text) ?? package.originalPrice;
              final newStock = int.tryParse(stockCtrl.text) ?? package.remainingStock;
              final newWindow = windowCtrl.text.trim();

              final updated = package.copyWith(
                title: newTitle.isNotEmpty ? newTitle : package.title,
                discountedPrice: newDisc,
                originalPrice: newOrig,
                remainingStock: newStock,
                pickupTimeWindow: newWindow.isNotEmpty ? newWindow : package.pickupTimeWindow,
                isActive: newStock > 0 ? package.isActive : false,
              );

              appState.editPackage(updated);
              Navigator.of(ctx).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  backgroundColor: AppColors.greenDark,
                  content: Text('Paquete actualizado en tiempo real'),
                ),
              );
            },
            child: const Text('Guardar'),
          ),
        ],
      ),
    );
  }

  void _confirmDeletePackage(BuildContext context, FoodPackage package, AppState appState) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('¿Eliminar Paquete?', style: AppStyles.heading3),
        content: Text('¿Estás seguro de que deseas eliminar "${package.title}"? Esta acción se sincronizará con la nube.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AppColors.error),
            onPressed: () {
              appState.deletePackage(package.id);
              Navigator.of(ctx).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  backgroundColor: AppColors.error,
                  content: Text('Paquete eliminado'),
                ),
              );
            },
            child: const Text('Eliminar', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final user = appState.currentUser;
    final merchantPackages = appState.merchantPackages;
    final redeemedList = appState.merchantRedeemedReservations;
    final totalKg = redeemedList.fold<double>(0.0, (acc, r) => acc + r.foodRescuedKg);

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

          // Métricas Dinámicas del Día
          Row(
            children: [
              Expanded(
                child: _MetricCard(
                  label: AppStrings.activePacksCount,
                  value: merchantPackages.where((p) => p.isActive && p.remainingStock > 0).length.toString(),
                  icon: Icons.inventory_2_outlined,
                  color: AppColors.primary,
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: _MetricCard(
                  label: AppStrings.redeemedToday,
                  value: redeemedList.length.toString(),
                  icon: Icons.qr_code_scanner_rounded,
                  color: AppColors.success,
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: _MetricCard(
                  label: AppStrings.totalSavedKg,
                  value: totalKg > 0 ? '${totalKg.toStringAsFixed(1)} kg' : '6.2 kg',
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

          // Listado y Control de Paquetes Publicados por este Comercio
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Expanded(
                child: Text(
                  'Gestión de Paquetes Hoy',
                  style: AppStyles.heading3,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: AppColors.surfaceMuted,
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  '${merchantPackages.length} en total',
                  style: const TextStyle(fontSize: 11.5, fontWeight: FontWeight.w700, color: AppColors.textSecondary),
                ),
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
                    'Publica tus excedentes del día para que la comunidad de Salamanca pueda rescatarlos.',
                    style: AppStyles.caption,
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            )
          else
            ...merchantPackages.map(
              (pkg) => _MerchantPackageItem(
                package: pkg,
                onStockChange: (delta) => appState.updatePackageStock(pkg.id, delta),
                onToggleActive: () => appState.togglePackageActive(pkg.id),
                onEdit: () => _showEditPackageDialog(context, pkg, appState),
                onDelete: () => _confirmDeletePackage(context, pkg, appState),
              ),
            ),

          const SizedBox(height: 26),

          // SECCIÓN DE AUDITORÍA: CANJES VALIDADOS HOY
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Expanded(
                child: Text(
                  'Entregas Validadas Hoy',
                  style: AppStyles.heading3,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: AppColors.success.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  '${redeemedList.length} canjes',
                  style: const TextStyle(fontSize: 11.5, fontWeight: FontWeight.w700, color: AppColors.greenDark),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),

          if (redeemedList.isEmpty)
            Container(
              padding: const EdgeInsets.all(20),
              decoration: AppStyles.cardDecoration,
              alignment: Alignment.center,
              child: const Column(
                children: [
                  Icon(Icons.qr_code_2_rounded, size: 36, color: AppColors.textMuted),
                  SizedBox(height: 8),
                  Text('Aún no has registrado canjes el día de hoy', style: AppStyles.bodyBold),
                  SizedBox(height: 4),
                  Text(
                    'Usa el botón "Escanear QR" cuando un cliente se presente en el mostrador.',
                    style: AppStyles.caption,
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            )
          else
            ...redeemedList.map((r) => _RedeemedReservationCard(reservation: r)),
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
  final FoodPackage package;
  final ValueChanged<int> onStockChange;
  final VoidCallback onToggleActive;
  final VoidCallback onEdit;
  final VoidCallback onDelete;

  const _MerchantPackageItem({
    required this.package,
    required this.onStockChange,
    required this.onToggleActive,
    required this.onEdit,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    final bool isSoldOut = package.remainingStock <= 0;
    final bool isActive = package.isActive && !isSoldOut;

    Color badgeColor;
    String badgeText;
    if (isSoldOut) {
      badgeColor = AppColors.error;
      badgeText = 'AGOTADO';
    } else if (package.isActive) {
      badgeColor = AppColors.greenDark;
      badgeText = 'ACTIVO';
    } else {
      badgeColor = AppColors.warning;
      badgeText = 'PAUSADO';
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isActive ? AppColors.border : AppColors.warning.withOpacity(0.4),
          width: isActive ? 1 : 1.5,
        ),
        boxShadow: const [
          BoxShadow(
            color: Color.fromRGBO(0, 0, 0, 0.04),
            blurRadius: 8,
            offset: Offset(0, 3),
          ),
        ],
      ),
      child: Column(
        children: [
          // Fila 1: Emoji, Título, Horario y Badge de Estado
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: 46,
                height: 46,
                decoration: BoxDecoration(
                  color: AppColors.surfaceMuted,
                  borderRadius: BorderRadius.circular(12),
                ),
                alignment: Alignment.center,
                child: Text(package.categoryEmoji, style: const TextStyle(fontSize: 24)),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      package.title,
                      style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.bold),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 2),
                    Row(
                      children: [
                        const Icon(Icons.access_time_rounded, size: 13, color: AppColors.accent),
                        const SizedBox(width: 3),
                        Expanded(
                          child: Text(
                            'Recoger: ${package.pickupTimeWindow}',
                            style: const TextStyle(fontSize: 11, color: AppColors.accentHover, fontWeight: FontWeight.w600),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: badgeColor.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  badgeText,
                  style: TextStyle(fontSize: 10, fontWeight: FontWeight.w900, color: badgeColor),
                ),
              ),
            ],
          ),

          const SizedBox(height: 12),
          const Divider(height: 1, color: AppColors.border),
          const SizedBox(height: 10),

          // Fila 2: Precios y Control Rápido de Stock (+ / -)
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              // Precios
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    Formatters.formatCurrency(package.discountedPrice),
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w900, color: AppColors.greenDark),
                  ),
                  Text(
                    'Original: ${Formatters.formatCurrency(package.originalPrice)}',
                    style: const TextStyle(
                      fontSize: 11,
                      decoration: TextDecoration.lineThrough,
                      color: AppColors.textMuted,
                    ),
                  ),
                ],
              ),

              // Contador de Stock Interactivo
              Row(
                children: [
                  const Text('Stock: ', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textSecondary)),
                  InkWell(
                    onTap: package.remainingStock > 0 ? () => onStockChange(-1) : null,
                    borderRadius: BorderRadius.circular(16),
                    child: Container(
                      width: 28,
                      height: 28,
                      decoration: BoxDecoration(
                        color: package.remainingStock > 0 ? AppColors.surfaceMuted : Colors.grey.shade100,
                        shape: BoxShape.circle,
                        border: Border.all(color: AppColors.border),
                      ),
                      child: Icon(Icons.remove, size: 16, color: package.remainingStock > 0 ? AppColors.textPrimary : Colors.grey),
                    ),
                  ),
                  Container(
                    constraints: const BoxConstraints(minWidth: 32),
                    alignment: Alignment.center,
                    child: Text(
                      '${package.remainingStock}',
                      style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w900, color: AppColors.primary),
                    ),
                  ),
                  InkWell(
                    onTap: () => onStockChange(1),
                    borderRadius: BorderRadius.circular(16),
                    child: Container(
                      width: 28,
                      height: 28,
                      decoration: BoxDecoration(
                        color: AppColors.primary.withOpacity(0.1),
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.add, size: 16, color: AppColors.primary),
                    ),
                  ),
                ],
              ),
            ],
          ),

          const SizedBox(height: 8),

          // Fila 3: Botones de Gestión (Pausar/Reanudar, Editar, Eliminar)
          Row(
            children: [
              TextButton.icon(
                onPressed: onToggleActive,
                style: TextButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                  minimumSize: Size.zero,
                  tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                ),
                icon: Icon(
                  package.isActive ? Icons.pause_circle_outline_rounded : Icons.play_circle_outline_rounded,
                  size: 16,
                  color: package.isActive ? AppColors.warning : AppColors.greenDark,
                ),
                label: Text(
                  package.isActive ? 'Pausar' : 'Activar',
                  style: TextStyle(
                    fontSize: 11.5,
                    fontWeight: FontWeight.bold,
                    color: package.isActive ? AppColors.warning : AppColors.greenDark,
                  ),
                ),
              ),
              const Spacer(),
              IconButton(
                onPressed: onEdit,
                icon: const Icon(Icons.edit_outlined, size: 18, color: AppColors.primary),
                tooltip: 'Editar detalles',
                visualDensity: VisualDensity.compact,
              ),
              IconButton(
                onPressed: onDelete,
                icon: const Icon(Icons.delete_outline_rounded, size: 18, color: AppColors.error),
                tooltip: 'Eliminar paquete',
                visualDensity: VisualDensity.compact,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _RedeemedReservationCard extends StatelessWidget {
  final Reservation reservation;

  const _RedeemedReservationCard({required this.reservation});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(12),
      decoration: AppStyles.cardDecoration,
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: AppColors.success.withOpacity(0.12),
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.check_rounded, color: AppColors.greenDark, size: 18),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  reservation.packageTitle,
                  style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 2),
                Text(
                  'Código: ${reservation.qrToken.length > 16 ? reservation.qrToken.substring(0, 16) : reservation.qrToken}...',
                  style: const TextStyle(fontSize: 10.5, color: AppColors.textSecondary, fontFamily: 'monospace'),
                ),
              ],
            ),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                Formatters.formatCurrency(reservation.amountPaid),
                style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w900, color: AppColors.primary),
              ),
              Container(
                margin: const EdgeInsets.only(top: 2),
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: AppColors.surfaceMuted,
                  borderRadius: BorderRadius.circular(6),
                ),
                child: const Text('COBRADO', style: TextStyle(fontSize: 9, fontWeight: FontWeight.w800, color: AppColors.textSecondary)),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
