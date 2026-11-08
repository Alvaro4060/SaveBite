import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_styles.dart';
import '../../../core/utils/formatters.dart';
import '../../../domain/entities/reservation.dart';
import '../../state/app_state.dart';

class MerchantSalesHistoryScreen extends StatefulWidget {
  const MerchantSalesHistoryScreen({super.key});

  @override
  State<MerchantSalesHistoryScreen> createState() => _MerchantSalesHistoryScreenState();
}

class _MerchantSalesHistoryScreenState extends State<MerchantSalesHistoryScreen> {
  String _selectedPeriod = 'Hoy';

  void _showCorteDeCajaDialog(BuildContext context, double totalAmount, int count, double totalKg) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: AppColors.greenDark.withOpacity(0.12),
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Icon(Icons.receipt_long_rounded, color: AppColors.greenDark, size: 22),
            ),
            const SizedBox(width: 10),
            const Expanded(
              child: Text('Corte de Caja Diario', style: AppStyles.heading3),
            ),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: AppColors.surfaceMuted,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppColors.border),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    '🥖 Panadería La Tradición',
                    style: TextStyle(fontWeight: FontWeight.w900, fontSize: 14),
                  ),
                  const Text(
                    'Centro Histórico, Salamanca • ODS 12',
                    style: TextStyle(fontSize: 11, color: AppColors.textSecondary),
                  ),
                  const Divider(height: 16, color: AppColors.border),
                  _ReceiptRow(label: 'Canjes Realizados', value: '$count pedidos'),
                  const SizedBox(height: 4),
                  _ReceiptRow(label: 'Comida Rescatada', value: '${totalKg.toStringAsFixed(1)} kg'),
                  const SizedBox(height: 4),
                  _ReceiptRow(label: 'Método de Cobro', value: 'Efectivo en Tienda'),
                  const Divider(height: 16, color: AppColors.border),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Total Recaudado:',
                        style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                      ),
                      Text(
                        Formatters.formatCurrency(totalAmount),
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w900,
                          color: AppColors.greenDark,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 12),
            const Text(
              'Este corte resume el dinero recuperado por excedentes que no se convirtieron en merma alimentaria.',
              style: TextStyle(fontSize: 11.5, color: AppColors.textSecondary, height: 1.3),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cerrar'),
          ),
          ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primary,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
            ),
            icon: const Icon(Icons.share_rounded, size: 16),
            label: const Text('Compartir Resumen'),
            onPressed: () {
              Navigator.of(ctx).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  backgroundColor: AppColors.primary,
                  content: Text('Resumen de corte listo para compartir o imprimir'),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final user = appState.currentUser;
    final redeemedList = appState.merchantRedeemedReservations;

    final double totalRevenue = redeemedList.fold<double>(
      0.0,
      (acc, r) => acc + r.amountPaid,
    );
    final double totalFoodKg = redeemedList.fold<double>(
      0.0,
      (acc, r) => acc + r.foodRescuedKg,
    );
    final double avgTicket = redeemedList.isNotEmpty ? totalRevenue / redeemedList.length : 0.0;

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 80),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // TARJETA PRINCIPAL DE INGRESOS RECUPERADOS
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: AppColors.accentGradient,
                borderRadius: BorderRadius.circular(22),
                boxShadow: const [
                  BoxShadow(
                    color: Color.fromRGBO(245, 130, 32, 0.25),
                    blurRadius: 16,
                    offset: Offset(0, 6),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: const Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(Icons.monetization_on_rounded, color: Colors.white, size: 13),
                            SizedBox(width: 4),
                            Text(
                              'VENTAS RECUPERADAS',
                              style: TextStyle(
                                fontSize: 9.5,
                                fontWeight: FontWeight.w900,
                                color: Colors.white,
                                letterSpacing: 0.5,
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          user.storeName ?? 'Panadería La Tradición',
                          textAlign: TextAlign.end,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                            fontSize: 12,
                            color: Colors.white,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),
                  Text(
                    Formatters.formatCurrency(totalRevenue),
                    style: const TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.w900,
                      color: Colors.white,
                      letterSpacing: -0.5,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Ingresos generados por alimentos que antes eran merma (Salamanca, Gto.)',
                    style: TextStyle(fontSize: 12, color: Colors.white.withOpacity(0.9)),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: AppColors.accentHover,
                        elevation: 0,
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      icon: const Icon(Icons.receipt_long_rounded, size: 18),
                      label: const Text(
                        'Generar Corte de Caja',
                        style: TextStyle(fontWeight: FontWeight.w900, fontSize: 13),
                      ),
                      onPressed: () => _showCorteDeCajaDialog(
                        context,
                        totalRevenue,
                        redeemedList.length,
                        totalFoodKg,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 18),

            // MÉTRICAS SECUNDARIAS
            Row(
              children: [
                Expanded(
                  child: _MiniCard(
                    title: 'Packs Cobrados',
                    value: redeemedList.length.toString(),
                    icon: Icons.check_circle_outline_rounded,
                    color: AppColors.greenDark,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _MiniCard(
                    title: 'Ticket Promedio',
                    value: Formatters.formatCurrency(avgTicket),
                    icon: Icons.analytics_outlined,
                    color: AppColors.primary,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _MiniCard(
                    title: 'Merma Salvada',
                    value: '${totalFoodKg.toStringAsFixed(1)} kg',
                    icon: Icons.eco_rounded,
                    color: AppColors.accent,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 22),

            // SECCIÓN HISTORIAL Y FILTROS DE PERÍODO (RESPONSIVE)
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Expanded(
                      child: Text(
                        'Historial de Entregas',
                        style: AppStyles.heading3,
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: AppColors.success.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(
                        '${redeemedList.length} canjes',
                        style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: AppColors.greenDark),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                Row(
                  children: ['Hoy', 'Semana', 'Total'].map((period) {
                    final isSelected = _selectedPeriod == period;
                    return Expanded(
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 3),
                        child: InkWell(
                          onTap: () => setState(() => _selectedPeriod = period),
                          borderRadius: BorderRadius.circular(10),
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 7),
                            alignment: Alignment.center,
                            decoration: BoxDecoration(
                              color: isSelected ? AppColors.primary : AppColors.surfaceMuted,
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(
                                color: isSelected ? AppColors.primary : AppColors.border,
                              ),
                            ),
                            child: Text(
                              period,
                              style: TextStyle(
                                fontSize: 11.5,
                                fontWeight: FontWeight.bold,
                                color: isSelected ? Colors.white : AppColors.textSecondary,
                              ),
                            ),
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ],
            ),

            const SizedBox(height: 12),

            // LISTA DE TRANSACCIONES / VOUCHERS CANJEADOS
            if (redeemedList.isEmpty)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(28),
                decoration: AppStyles.cardDecoration,
                alignment: Alignment.center,
                child: const Column(
                  children: [
                    Icon(Icons.point_of_sale_rounded, size: 44, color: AppColors.textMuted),
                    SizedBox(height: 10),
                    Text('Sin transacciones registradas', style: AppStyles.bodyBold),
                    SizedBox(height: 4),
                    Text(
                      'Cuando escanees los códigos QR de los clientes en mostrador, el registro detallado y el desglose de ingresos aparecerán aquí.',
                      style: AppStyles.caption,
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              )
            else
              ...redeemedList.map((r) => _TransactionTile(reservation: r)),
          ],
        ),
      ),
    );
  }
}

class _ReceiptRow extends StatelessWidget {
  final String label;
  final String value;

  const _ReceiptRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
          child: Text(
            label,
            style: const TextStyle(fontSize: 12, color: AppColors.textSecondary),
            overflow: TextOverflow.ellipsis,
          ),
        ),
        const SizedBox(width: 8),
        Text(value, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
      ],
    );
  }
}

class _MiniCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color color;

  const _MiniCard({
    required this.title,
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
              fontSize: 15,
              fontWeight: FontWeight.w900,
              color: color,
            ),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 2),
          Text(
            title,
            style: const TextStyle(fontSize: 11, color: AppColors.textSecondary),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }
}

class _TransactionTile extends StatelessWidget {
  final Reservation reservation;

  const _TransactionTile({required this.reservation});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(14),
      decoration: AppStyles.cardDecoration,
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(9),
            decoration: BoxDecoration(
              color: AppColors.greenDark.withOpacity(0.12),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Icon(Icons.arrow_downward_rounded, color: AppColors.greenDark, size: 18),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  reservation.packageTitle,
                  style: const TextStyle(fontSize: 13.5, fontWeight: FontWeight.bold),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 2),
                Row(
                  children: [
                    const Icon(Icons.access_time_rounded, size: 12, color: AppColors.textMuted),
                    const SizedBox(width: 3),
                    Text(
                      Formatters.formatTime(reservation.reservedAt),
                      style: const TextStyle(fontSize: 11, color: AppColors.textSecondary),
                    ),
                    const SizedBox(width: 8),
                    Flexible(
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1),
                        decoration: BoxDecoration(
                          color: AppColors.surfaceMuted,
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          reservation.id.length > 12 ? reservation.id.substring(0, 12) : reservation.id,
                          style: const TextStyle(fontSize: 9.5, fontFamily: 'monospace', color: AppColors.textSecondary),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                '+${Formatters.formatCurrency(reservation.amountPaid)}',
                style: const TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w900,
                  color: AppColors.greenDark,
                ),
              ),
              const SizedBox(height: 2),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: AppColors.success.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: const Text(
                  'EN TIENDA',
                  style: TextStyle(fontSize: 9, fontWeight: FontWeight.w800, color: AppColors.greenDark),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

