import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_strings.dart';
import '../../../core/utils/formatters.dart';
import '../../../domain/entities/reservation.dart';
import '../../widgets/custom_button.dart';
import '../../widgets/dynamic_qr_widget.dart';

class VoucherScreen extends StatelessWidget {
  final Reservation reservation;

  const VoucherScreen({super.key, required this.reservation});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Voucher Digital'),
        actions: [
          IconButton(
            icon: const Icon(Icons.share_outlined),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Comprobante digital listo para compartir')),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        child: Column(
          children: [
            // Indicador Offline-First
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              margin: const EdgeInsets.only(bottom: 16),
              decoration: BoxDecoration(
                color: AppColors.success.withOpacity(0.1),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: AppColors.success.withOpacity(0.3)),
              ),
              child: const Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.offline_pin_rounded, color: AppColors.greenDark, size: 18),
                  SizedBox(width: 8),
                  Text(
                    'Guardado localmente (Funciona sin internet)',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: AppColors.greenDark,
                    ),
                  ),
                ],
              ),
            ),

            // Tarjeta del Voucher estilo Ticket
            Container(
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(24),
                boxShadow: const [
                  BoxShadow(
                    color: Color.fromRGBO(0, 0, 0, 0.08),
                    blurRadius: 20,
                    offset: Offset(0, 8),
                  ),
                ],
              ),
              child: Column(
                children: [
                  // Cabecera del Ticket
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: const BoxDecoration(
                      gradient: AppColors.heroGradient,
                      borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
                    ),
                    child: Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Row(
                              children: [
                                Icon(Icons.shopping_bag_outlined, color: Colors.white, size: 20),
                                SizedBox(width: 6),
                                Text(
                                  AppStrings.appName,
                                  style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 16),
                                ),
                              ],
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                              decoration: BoxDecoration(
                                color: reservation.isRedeemed ? AppColors.success : AppColors.accent,
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Text(
                                reservation.isRedeemed ? 'CANJEADO' : 'ACTIVO',
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 11,
                                  fontWeight: FontWeight.w800,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 14),
                        Text(
                          reservation.packageTitle,
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          reservation.storeName,
                          style: const TextStyle(
                            color: Color(0xFFBFDBFE),
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Sección Central: Código QR Dinámico
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 24, horizontal: 20),
                    child: Column(
                      children: [
                        DynamicQrWidget(
                          qrToken: reservation.qrToken,
                          size: 210,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          reservation.id,
                          style: const TextStyle(
                            fontSize: 17,
                            fontWeight: FontWeight.w900,
                            letterSpacing: 2,
                            color: AppColors.primaryDark,
                          ),
                        ),
                        const SizedBox(height: 4),
                        const Text(
                          AppStrings.dynamicQrNotice,
                          textAlign: TextAlign.center,
                          style: TextStyle(fontSize: 11.5, color: AppColors.textSecondary),
                        ),
                      ],
                    ),
                  ),

                  // Línea de corte punteada
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    child: Row(
                      children: List.generate(
                        26,
                        (index) => Expanded(
                          child: Container(
                            height: 1.5,
                            color: index % 2 == 0 ? AppColors.border : Colors.transparent,
                          ),
                        ),
                      ),
                    ),
                  ),

                  // Detalles de la Recogida
                  Padding(
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      children: [
                        _DetailRow(
                          label: 'Horario Límite:',
                          value: reservation.pickupWindow,
                          isHighlight: true,
                        ),
                        const SizedBox(height: 10),
                        _DetailRow(
                          label: 'Total Pagado:',
                          value: Formatters.formatCurrency(reservation.amountPaid),
                        ),
                        const SizedBox(height: 10),
                        _DetailRow(
                          label: 'Impacto ODS:',
                          value: '-${reservation.co2SavedKg} kg CO₂ / ${reservation.foodRescuedKg} kg comida',
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // Botón Regresar
            CustomButton(
              text: 'Volver a Mis Reservas',
              backgroundColor: AppColors.primary,
              onPressed: () => Navigator.of(context).pop(),
            ),

            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}

class _DetailRow extends StatelessWidget {
  final String label;
  final String value;
  final bool isHighlight;

  const _DetailRow({
    required this.label,
    required this.value,
    this.isHighlight = false,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: const TextStyle(fontSize: 13, color: AppColors.textSecondary)),
        Text(
          value,
          style: TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.bold,
            color: isHighlight ? AppColors.accentHover : AppColors.textPrimary,
          ),
        ),
      ],
    );
  }
}
