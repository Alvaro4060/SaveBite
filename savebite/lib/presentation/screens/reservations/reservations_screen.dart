import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_styles.dart';
import '../../../core/utils/formatters.dart';
import '../../../domain/entities/reservation.dart';
import '../../state/app_state.dart';
import '../qr_voucher/voucher_screen.dart';

class ReservationsScreen extends StatefulWidget {
  const ReservationsScreen({super.key});

  @override
  State<ReservationsScreen> createState() => _ReservationsScreenState();
}

class _ReservationsScreenState extends State<ReservationsScreen> {
  int _selectedFilter = 0; // 0 = Activas, 1 = Todas / Historial

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final allReservations = appState.reservations;
    final activeReservations = appState.pendingReservations;

    final displayedReservations = _selectedFilter == 0 ? activeReservations : allReservations;

    return Column(
      children: [
        // Selector de Pestaña: Activas vs Historial
        Container(
          color: AppColors.surface,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          child: Container(
            padding: const EdgeInsets.all(4),
            decoration: BoxDecoration(
              color: AppColors.surfaceMuted,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(
              children: [
                Expanded(
                  child: _TabPill(
                    label: 'Vouchers Activos (${activeReservations.length})',
                    isSelected: _selectedFilter == 0,
                    onTap: () => setState(() => _selectedFilter = 0),
                  ),
                ),
                Expanded(
                  child: _TabPill(
                    label: 'Historial Completo (${allReservations.length})',
                    isSelected: _selectedFilter == 1,
                    onTap: () => setState(() => _selectedFilter = 1),
                  ),
                ),
              ],
            ),
          ),
        ),

        // Lista de Vouchers
        Expanded(
          child: displayedReservations.isEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(32),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.confirmation_number_outlined, size: 56, color: AppColors.textMuted),
                        const SizedBox(height: 14),
                        Text(
                          _selectedFilter == 0
                              ? 'No tienes vouchers activos por recoger'
                              : 'No tienes historial de reservas aún',
                          style: AppStyles.heading3,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 6),
                        const Text(
                          'Explora el mapa y reserva tu primer paquete sorpresa con descuento.',
                          style: AppStyles.body,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 18),
                        ElevatedButton.icon(
                          onPressed: () => appState.setTabIndex(0),
                          icon: const Icon(Icons.explore_outlined, size: 18),
                          label: const Text('Explorar Ofertas'),
                        ),
                      ],
                    ),
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.fromLTRB(16, 16, 16, 80),
                  itemCount: displayedReservations.length,
                  itemBuilder: (context, index) {
                    final res = displayedReservations[index];
                    return _ReservationItemCard(
                      reservation: res,
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => VoucherScreen(reservation: res),
                          ),
                        );
                      },
                    );
                  },
                ),
        ),
      ],
    );
  }
}

class _TabPill extends StatelessWidget {
  final String label;
  final bool isSelected;
  final VoidCallback onTap;

  const _TabPill({
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(vertical: 8),
        decoration: BoxDecoration(
          color: isSelected ? AppColors.surface : Colors.transparent,
          borderRadius: BorderRadius.circular(10),
          boxShadow: isSelected
              ? const [
                  BoxShadow(color: Color.fromRGBO(0, 0, 0, 0.05), blurRadius: 4, offset: Offset(0, 2)),
                ]
              : null,
        ),
        alignment: Alignment.center,
        child: Text(
          label,
          style: TextStyle(
            fontSize: 12.5,
            fontWeight: isSelected ? FontWeight.w800 : FontWeight.w500,
            color: isSelected ? AppColors.primary : AppColors.textSecondary,
          ),
        ),
      ),
    );
  }
}

class _ReservationItemCard extends StatelessWidget {
  final Reservation reservation;
  final VoidCallback onTap;

  const _ReservationItemCard({
    required this.reservation,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      decoration: AppStyles.cardDecoration,
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                // Mini código QR / Icono
                Container(
                  width: 54,
                  height: 54,
                  decoration: BoxDecoration(
                    color: reservation.isRedeemed
                        ? AppColors.surfaceMuted
                        : AppColors.primary.withOpacity(0.08),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: reservation.isRedeemed ? AppColors.border : AppColors.primary.withOpacity(0.3),
                    ),
                  ),
                  alignment: Alignment.center,
                  child: Icon(
                    reservation.isRedeemed ? Icons.check_circle_outline : Icons.qr_code_2_rounded,
                    color: reservation.isRedeemed ? AppColors.textMuted : AppColors.primary,
                    size: 30,
                  ),
                ),
                const SizedBox(width: 14),
                // Información de la reserva
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Expanded(
                            child: Text(
                              reservation.packageTitle,
                              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: reservation.isRedeemed
                                  ? AppColors.success.withOpacity(0.12)
                                  : AppColors.accent.withOpacity(0.12),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Text(
                              reservation.isRedeemed ? 'CANJEADO' : 'PENDIENTE',
                              style: TextStyle(
                                fontSize: 9.5,
                                fontWeight: FontWeight.w800,
                                color: reservation.isRedeemed ? AppColors.greenDark : AppColors.accentHover,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 3),
                      Text(
                        reservation.storeName,
                        style: const TextStyle(fontSize: 12, color: AppColors.textSecondary),
                      ),
                      const SizedBox(height: 6),
                      Row(
                        children: [
                          Icon(
                            Icons.access_time_rounded,
                            size: 13,
                            color: reservation.isRedeemed ? AppColors.textMuted : AppColors.accent,
                          ),
                          const SizedBox(width: 4),
                          Text(
                            reservation.pickupWindow,
                            style: TextStyle(
                              fontSize: 11.5,
                              fontWeight: FontWeight.w600,
                              color: reservation.isRedeemed ? AppColors.textMuted : AppColors.accentHover,
                            ),
                          ),
                          const Spacer(),
                          Text(
                            Formatters.formatCurrency(reservation.amountPaid),
                            style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w900, color: AppColors.primary),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
