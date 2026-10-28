import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_strings.dart';
import '../../../core/constants/app_styles.dart';
import '../../../core/utils/formatters.dart';
import '../../state/app_state.dart';
import '../../widgets/eco_stat_card.dart';

class ImpactCalculatorScreen extends StatelessWidget {
  const ImpactCalculatorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final impact = appState.ecoImpact;

    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 80),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Banner ODS 12
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(20),
            decoration: const BoxDecoration(
              gradient: AppColors.ecoGradient,
              borderRadius: BorderRadius.all(Radius.circular(20)),
              boxShadow: [
                BoxShadow(
                  color: Color.fromRGBO(16, 185, 129, 0.25),
                  blurRadius: 14,
                  offset: Offset(0, 6),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Text(
                        'ODS 12 • CERO MERMA',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 11,
                          fontWeight: FontWeight.w900,
                          letterSpacing: 1,
                        ),
                      ),
                    ),
                    const Icon(Icons.public, color: Colors.white, size: 24),
                  ],
                ),
                const SizedBox(height: 14),
                const Text(
                  'Tu Huella Positiva en Salamanca',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.w900,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  'Cada paquete que rescatas evita que alimentos preparados en perfecto estado terminen en rellenos sanitarios.',
                  style: TextStyle(
                    fontSize: 13,
                    color: Colors.white.withOpacity(0.9),
                    height: 1.35,
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 20),

          // Tarjetas de Métricas ODS
          Row(
            children: [
              Expanded(
                child: EcoStatCard(
                  title: AppStrings.totalFoodRescued,
                  value: '${impact.totalKgRescued.toStringAsFixed(1)} kg',
                  subtitle: 'En ${impact.totalPacksRescued} paquetes',
                  icon: Icons.eco_rounded,
                  iconColor: AppColors.greenDark,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: EcoStatCard(
                  title: AppStrings.totalCo2Avoided,
                  value: '${impact.totalCo2AvoidedKg.toStringAsFixed(1)} kg',
                  subtitle: 'Mitigado a la atmósfera',
                  icon: Icons.cloud_outlined,
                  iconColor: AppColors.secondaryDark,
                ),
              ),
            ],
          ),

          const SizedBox(height: 12),

          // Tarjeta de Dinero Ahorrado
          Container(
            padding: const EdgeInsets.all(18),
            decoration: BoxDecoration(
              color: AppColors.surface,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: AppColors.border),
            ),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.warning.withOpacity(0.12),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: const Icon(Icons.savings_rounded, color: AppColors.warning, size: 28),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        Formatters.formatCurrency(impact.totalMoneySavedMxn),
                        style: const TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.w900,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const Text(
                        'Dinero Total Ahorrado en Alimentación',
                        style: TextStyle(fontSize: 12, color: AppColors.textSecondary, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 24),

          // Sección de Insignias Gamificadas
          const Text(AppStrings.ecoBadgesTitle, style: AppStyles.heading3),
          const SizedBox(height: 4),
          const Text(
            'Desbloquea logros por cada lote rescatado de panaderías y cafeterías.',
            style: AppStyles.caption,
          ),
          const SizedBox(height: 12),

          ...impact.badges.map((badge) => _BadgeItem(badge: badge)),

          const SizedBox(height: 16),

          // Botón Compartir Impacto
          SizedBox(
            width: double.infinity,
            child: OutlinedButton.icon(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Reporte de impacto ecológico generado para compartir'),
                  ),
                );
              },
              icon: const Icon(Icons.share_outlined, size: 18),
              label: const Text('Compartir Mi Impacto en Redes'),
              style: OutlinedButton.styleFrom(
                side: const BorderSide(color: AppColors.primary),
                padding: const EdgeInsets.symmetric(vertical: 12),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _BadgeItem extends StatelessWidget {
  final dynamic badge;

  const _BadgeItem({required this.badge});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: badge.isUnlocked ? Colors.white : AppColors.surfaceMuted,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: badge.isUnlocked ? AppColors.secondary.withOpacity(0.4) : AppColors.border,
        ),
      ),
      child: Row(
        children: [
          Container(
            width: 44,
            height: 44,
            decoration: BoxDecoration(
              color: badge.isUnlocked ? AppColors.secondary.withOpacity(0.12) : Colors.black12,
              borderRadius: BorderRadius.circular(12),
            ),
            alignment: Alignment.center,
            child: Text(
              badge.iconEmoji,
              style: TextStyle(
                fontSize: 22,
                color: badge.isUnlocked ? null : Colors.grey,
              ),
            ),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(
                      badge.title,
                      style: TextStyle(
                        fontSize: 13.5,
                        fontWeight: FontWeight.bold,
                        color: badge.isUnlocked ? AppColors.textPrimary : AppColors.textMuted,
                      ),
                    ),
                    const SizedBox(width: 6),
                    if (badge.isUnlocked)
                      const Icon(Icons.check_circle_rounded, color: AppColors.success, size: 16),
                  ],
                ),
                const SizedBox(height: 2),
                Text(
                  badge.description,
                  style: TextStyle(
                    fontSize: 11.5,
                    color: badge.isUnlocked ? AppColors.textSecondary : AppColors.textMuted,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  badge.dateEarned,
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.w600,
                    color: badge.isUnlocked ? AppColors.greenDark : AppColors.textMuted,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
