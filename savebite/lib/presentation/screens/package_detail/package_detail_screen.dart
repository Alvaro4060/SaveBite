import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_strings.dart';
import '../../../core/constants/app_styles.dart';
import '../../../core/utils/formatters.dart';
import '../../../domain/entities/food_package.dart';
import '../../../domain/entities/reservation.dart';
import '../../../domain/entities/review.dart';
import '../../state/app_state.dart';
import '../../widgets/custom_button.dart';
import '../qr_voucher/voucher_screen.dart';

class PackageDetailScreen extends StatefulWidget {
  final FoodPackage package;

  const PackageDetailScreen({super.key, required this.package});

  @override
  State<PackageDetailScreen> createState() => _PackageDetailScreenState();
}

class _PackageDetailScreenState extends State<PackageDetailScreen> {
  bool _isReserving = false;

  void _onReserve(BuildContext context) async {
    setState(() => _isReserving = true);
    final appState = AppStateProvider.of(context);

    try {
      final reservation = await appState.reservePackage(widget.package);
      if (!mounted) return;
      setState(() => _isReserving = false);
      _showSuccessDialog(context, reservation);
    } catch (e) {
      if (!mounted) return;
      setState(() => _isReserving = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: AppColors.error,
          content: Text('No fue posible completar la reserva: $e'),
        ),
      );
    }
  }

  void _showSuccessDialog(BuildContext context, Reservation reservation) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) => Container(
        padding: const EdgeInsets.all(24),
        decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 60,
              height: 60,
              decoration: BoxDecoration(
                color: AppColors.success.withOpacity(0.12),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.check_circle_rounded, color: AppColors.success, size: 36),
            ),
            const SizedBox(height: 16),
            const Text('¡Reserva Confirmada!', style: AppStyles.heading2),
            const SizedBox(height: 8),
            Text(
              'Tu paquete sorpresa en ${widget.package.storeName} ha sido apartado con éxito.',
              textAlign: TextAlign.center,
              style: AppStyles.body,
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.surfaceMuted,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppColors.border),
              ),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Código de Canje:', style: TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                      const SizedBox(width: 8),
                      Flexible(
                        child: Text(
                          reservation.id,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: AppColors.primary),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Ventana de Recogida:', style: TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                      const SizedBox(width: 8),
                      Flexible(
                        child: Text(
                          reservation.pickupWindow,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: AppColors.accentHover),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            CustomButton(
              text: 'Ver Mi Voucher Digital (QR)',
              icon: Icons.qr_code_rounded,
              backgroundColor: AppColors.primary,
              onPressed: () {
                Navigator.of(ctx).pop(); // Cierra el modal
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(
                    builder: (_) => VoucherScreen(reservation: reservation),
                  ),
                );
              },
            ),
            const SizedBox(height: 10),
            TextButton(
              onPressed: () {
                Navigator.of(ctx).pop();
                Navigator.of(context).pop();
              },
              child: const Text('Volver al Feed'),
            ),
            const SizedBox(height: 10),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final pkg = widget.package;
    final discount = pkg.discountPercentage;
    final savings = pkg.originalPrice - pkg.discountedPrice;
    final storeReviews = appState.getReviewsForStore(pkg.storeName);
    final avgRating = appState.getStoreAverageRating(pkg.storeName);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Ficha del Paquete Sorpresa'),
        actions: [
          IconButton(
            icon: const Icon(Icons.share_outlined),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Enlace de paquete copiado al portapapeles')),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Banner Visual del Paquete
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                gradient: AppColors.heroGradient,
                borderRadius: BorderRadius.circular(20),
                boxShadow: const [
                  BoxShadow(
                    color: Color.fromRGBO(15, 76, 129, 0.2),
                    blurRadius: 16,
                    offset: Offset(0, 8),
                  ),
                ],
              ),
              child: Column(
                children: [
                  Container(
                    width: 72,
                    height: 72,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.15),
                          blurRadius: 12,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    alignment: Alignment.center,
                    child: Text(pkg.categoryEmoji, style: const TextStyle(fontSize: 38)),
                  ),
                  const SizedBox(height: 14),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      pkg.category,
                      style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    pkg.title,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 20,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    pkg.storeName,
                    style: const TextStyle(
                      color: Color(0xFFBFDBFE),
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Tarjeta de Precios y Ahorro
            Container(
              padding: const EdgeInsets.all(18),
              decoration: AppStyles.cardDecoration,
              child: Column(
                children: [
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Precio SaveBite:',
                              style: TextStyle(fontSize: 12, color: AppColors.textSecondary, fontWeight: FontWeight.w500),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              Formatters.formatCurrency(pkg.discountedPrice),
                              style: const TextStyle(
                                fontSize: 26,
                                fontWeight: FontWeight.w900,
                                color: AppColors.greenDark,
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 8),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 4),
                            decoration: BoxDecoration(
                              gradient: AppColors.accentGradient,
                              borderRadius: BorderRadius.circular(16),
                            ),
                            child: Text(
                              '-$discount% DESCUENTO',
                              style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w800),
                            ),
                          ),
                          const SizedBox(height: 5),
                          Text(
                            'Original: ${Formatters.formatCurrency(pkg.originalPrice)}',
                            style: const TextStyle(
                              fontSize: 12.5,
                              decoration: TextDecoration.lineThrough,
                              color: AppColors.textMuted,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: AppColors.success.withOpacity(0.08),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.savings_rounded, color: AppColors.greenDark, size: 18),
                        const SizedBox(width: 8),
                        Flexible(
                          child: Text(
                            'Ahorras ${Formatters.formatCurrency(savings)} rescatando comida fresca',
                            textAlign: TextAlign.center,
                            style: const TextStyle(
                              color: AppColors.greenDark,
                              fontSize: 12,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 18),

            // Horario de recogida estricto
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppColors.accent.withOpacity(0.3)),
              ),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: AppColors.accent.withOpacity(0.12),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.alarm_on_rounded, color: AppColors.accentHover, size: 24),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          AppStrings.pickupWindow,
                          style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textSecondary),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          'Hoy ${pkg.pickupTimeWindow}',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
                        ),
                        const SizedBox(height: 2),
                        const Text(
                          'Presenta tu QR en mostrador durante este horario',
                          style: TextStyle(fontSize: 11, color: AppColors.textMuted),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 18),

            // ¿Qué incluye este Paquete Sorpresa?
            const Text('¿Qué incluye este Paquete Sorpresa?', style: AppStyles.heading3),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: AppStyles.cardDecoration,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(pkg.description, style: AppStyles.body),
                  const SizedBox(height: 12),
                  const Row(
                    children: [
                      Icon(Icons.info_outline, size: 16, color: AppColors.primary),
                      SizedBox(width: 6),
                      Expanded(
                        child: Text(
                          'El contenido exacto varía cada día según los excedentes de calidad del negocio.',
                          style: TextStyle(fontSize: 11.5, color: AppColors.textSecondary, fontStyle: FontStyle.italic),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 18),

            // Impacto Ambiental ODS 12
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFF0FDF4),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFFA7F3D0)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.eco_rounded, color: AppColors.greenDark, size: 30),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Impacto Ecológico (ODS 12)',
                          style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800, color: AppColors.greenDark),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          'Evitas ~${pkg.co2SavedKg} kg de CO₂e y rescatas ~${pkg.estimatedKg} kg de comida del vertedero.',
                          style: const TextStyle(fontSize: 12, color: Color(0xFF065F46)),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 22),

            // Módulo 1: Opiniones y Reseñas de la Comunidad de Salamanca
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Expanded(
                  child: Text(
                    '⭐ Reseñas de la Comunidad',
                    style: TextStyle(fontSize: 15.5, fontWeight: FontWeight.bold),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.amber.withOpacity(0.12),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.star_rounded, size: 16, color: Colors.amber),
                      const SizedBox(width: 4),
                      Text(
                        '$avgRating (${storeReviews.length})',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w800,
                          color: Colors.amber.shade900,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),

            if (storeReviews.isEmpty)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: AppStyles.cardDecoration,
                child: const Column(
                  children: [
                    Icon(Icons.rate_review_outlined, color: AppColors.textMuted, size: 36),
                    SizedBox(height: 8),
                    Text(
                      'Aún no hay opiniones para este comercio',
                      style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: AppColors.textSecondary),
                      textAlign: TextAlign.center,
                    ),
                    SizedBox(height: 4),
                    Text(
                      '¡Sé el primero en rescatar y calificar tu experiencia!',
                      style: TextStyle(fontSize: 11.5, color: AppColors.textMuted),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              )
            else
              Column(
                children: storeReviews.take(4).map((review) {
                  return Container(
                    margin: const EdgeInsets.only(bottom: 10),
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            CircleAvatar(
                              radius: 14,
                              backgroundColor: AppColors.primary.withOpacity(0.12),
                              child: Text(
                                review.userInitials,
                                style: const TextStyle(
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.primary,
                                ),
                              ),
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                review.userName,
                                style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.bold),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                            const SizedBox(width: 6),
                            Row(
                              mainAxisSize: MainAxisSize.min,
                              children: List.generate(5, (sIdx) {
                                return Icon(
                                  sIdx < review.rating ? Icons.star_rounded : Icons.star_outline_rounded,
                                  size: 13,
                                  color: sIdx < review.rating ? Colors.amber : Colors.grey.shade300,
                                );
                              }),
                            ),
                          ],
                        ),
                        if (review.tags.isNotEmpty) ...[
                          const SizedBox(height: 8),
                          Wrap(
                            spacing: 6,
                            runSpacing: 4,
                            children: review.tags.map((tag) {
                              return Container(
                                padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
                                decoration: BoxDecoration(
                                  color: AppColors.surfaceMuted,
                                  borderRadius: BorderRadius.circular(6),
                                ),
                                child: Text(
                                  tag,
                                  style: const TextStyle(fontSize: 10, color: AppColors.textSecondary),
                                ),
                              );
                            }).toList(),
                          ),
                        ],
                        if (review.comment.isNotEmpty) ...[
                          const SizedBox(height: 8),
                          Text(
                            review.comment,
                            style: const TextStyle(fontSize: 12, color: AppColors.textPrimary),
                          ),
                        ],
                      ],
                    ),
                  );
                }).toList(),
              ),

            const SizedBox(height: 20),

            // Botón de Reserva Directa
            CustomButton(
              text: _isReserving ? 'Procesando reserva...' : AppStrings.reserveNow,
              icon: Icons.check_circle_outline_rounded,
              backgroundColor: AppColors.primary,
              onPressed: pkg.isAvailable && !_isReserving ? () => _onReserve(context) : null,
            ),

            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
