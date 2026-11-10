import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';
import '../../domain/entities/reservation.dart';
import '../state/app_state.dart';

class RateExperienceDialog extends StatefulWidget {
  final Reservation reservation;

  const RateExperienceDialog({
    super.key,
    required this.reservation,
  });

  static Future<bool?> show(BuildContext context, Reservation reservation) {
    return showModalBottomSheet<bool>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) => RateExperienceDialog(reservation: reservation),
    );
  }

  @override
  State<RateExperienceDialog> createState() => _RateExperienceDialogState();
}

class _RateExperienceDialogState extends State<RateExperienceDialog> {
  double _selectedRating = 5.0;
  final TextEditingController _commentController = TextEditingController();
  final Set<String> _selectedTags = {
    '🥖 Súper Fresco',
    '💰 Gran Ahorro',
  };
  bool _isSubmitting = false;

  static const List<String> _availableTags = [
    '🥖 Súper Fresco',
    '💰 Gran Ahorro',
    '📦 Muy Abundante',
    '😊 Atención Amable',
    '⚡ Rápido y Fácil',
    '🌱 Empaque Ecológico',
  ];

  @override
  void dispose() {
    _commentController.dispose();
    super.dispose();
  }

  String _getRatingFeedbackText(double rating) {
    if (rating >= 5.0) return '¡Excelente experiencia! 🌟';
    if (rating >= 4.0) return 'Muy bueno y recomendado 👍';
    if (rating >= 3.0) return 'Bueno / Aceptable 👌';
    if (rating >= 2.0) return 'Regular, hay detalles a mejorar ⚠️';
    return 'Mala experiencia 🙁';
  }

  Color _getRatingColor(double rating) {
    if (rating >= 4.0) return AppColors.accent;
    if (rating >= 3.0) return Colors.amber.shade700;
    return AppColors.error;
  }

  void _submit() async {
    setState(() => _isSubmitting = true);
    final appState = AppStateProvider.of(context);

    try {
      await appState.submitReview(
        reservationId: widget.reservation.id,
        storeName: widget.reservation.storeName,
        packageTitle: widget.reservation.packageTitle,
        rating: _selectedRating,
        comment: _commentController.text.trim().isNotEmpty
            ? _commentController.text.trim()
            : '¡Excelente paquete sorpresa! Rescaté comida en perfecto estado.',
        tags: _selectedTags.toList(),
      );

      if (!mounted) return;
      Navigator.of(context).pop(true);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          backgroundColor: AppColors.primary,
          behavior: SnackBarBehavior.floating,
          content: Row(
            children: [
              Icon(Icons.stars_rounded, color: Colors.amber, size: 24),
              SizedBox(width: 10),
              Expanded(
                child: Text(
                  '¡Gracias por tu reseña! Ayudas a más vecinos de Salamanca a salvar alimentos.',
                  style: TextStyle(fontWeight: FontWeight.w600),
                ),
              ),
            ],
          ),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      setState(() => _isSubmitting = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: AppColors.error,
          content: Text('No fue posible guardar la reseña: $e'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final bottomInset = MediaQuery.of(context).viewInsets.bottom;

    return Container(
      constraints: BoxConstraints(
        maxHeight: MediaQuery.of(context).size.height * 0.9,
      ),
      margin: EdgeInsets.only(bottom: bottomInset),
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Barra superior de agarre
            Container(
              width: 44,
              height: 4,
              margin: const EdgeInsets.only(bottom: 16),
              decoration: BoxDecoration(
                color: Colors.grey.shade300,
                borderRadius: BorderRadius.circular(2),
              ),
            ),

            // Encabezado
            Row(
              children: [
                Container(
                  width: 44,
                  height: 44,
                  decoration: BoxDecoration(
                    color: AppColors.accent.withOpacity(0.12),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  alignment: Alignment.center,
                  child: const Icon(Icons.star_rounded, color: AppColors.accentHover, size: 28),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Calificar Experiencia',
                        style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 2),
                      Text(
                        '${widget.reservation.storeName} • ${widget.reservation.packageTitle}',
                        style: const TextStyle(fontSize: 12, color: AppColors.textSecondary),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close_rounded, color: AppColors.textMuted),
                  onPressed: () => Navigator.of(context).pop(),
                ),
              ],
            ),

            const SizedBox(height: 16),
            const Divider(height: 1, color: AppColors.border),
            const SizedBox(height: 18),

            // Selector de Estrellas Interactivo
            const Text(
              '¿Cómo calificarías tu paquete sorpresa?',
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: AppColors.textPrimary),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(5, (index) {
                final starValue = index + 1.0;
                final isSelected = starValue <= _selectedRating;
                return GestureDetector(
                  onTap: () {
                    setState(() {
                      _selectedRating = starValue;
                    });
                  },
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 4),
                    child: Icon(
                      isSelected ? Icons.star_rounded : Icons.star_outline_rounded,
                      size: 40,
                      color: isSelected ? _getRatingColor(_selectedRating) : Colors.grey.shade300,
                    ),
                  ),
                );
              }),
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                color: _getRatingColor(_selectedRating).withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                _getRatingFeedbackText(_selectedRating),
                style: TextStyle(
                  fontSize: 12.5,
                  fontWeight: FontWeight.bold,
                  color: _getRatingColor(_selectedRating),
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Etiquetas rápidas de experiencia
            const Align(
              alignment: Alignment.centerLeft,
              child: Text(
                '¿Qué fue lo más destacable?',
                style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
              ),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _availableTags.map((tag) {
                final isSelected = _selectedTags.contains(tag);
                return InkWell(
                  borderRadius: BorderRadius.circular(20),
                  onTap: () {
                    setState(() {
                      if (isSelected) {
                        _selectedTags.remove(tag);
                      } else {
                        _selectedTags.add(tag);
                      }
                    });
                  },
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 180),
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
                    decoration: BoxDecoration(
                      color: isSelected ? AppColors.primary : AppColors.surfaceMuted,
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(
                        color: isSelected ? AppColors.primary : AppColors.border,
                      ),
                    ),
                    child: Text(
                      tag,
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                        color: isSelected ? Colors.white : AppColors.textSecondary,
                      ),
                    ),
                  ),
                );
              }).toList(),
            ),

            const SizedBox(height: 20),

            // Comentario opcional
            const Align(
              alignment: Alignment.centerLeft,
              child: Text(
                'Comentario o sugerencia (opcional)',
                style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
              ),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: _commentController,
              maxLines: 3,
              style: const TextStyle(fontSize: 13),
              decoration: InputDecoration(
                hintText: 'Ej: El pan venía en excelente estado y muy rico. ¡Súper recomendado!',
                hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 12.5),
                filled: true,
                fillColor: AppColors.surfaceMuted,
                contentPadding: const EdgeInsets.all(12),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: AppColors.border),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: AppColors.border),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
                ),
              ),
            ),

            const SizedBox(height: 22),

            // Botón de Enviar
            SizedBox(
              width: double.infinity,
              height: 48,
              child: ElevatedButton.icon(
                onPressed: _isSubmitting ? null : _submit,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                  elevation: 0,
                ),
                icon: _isSubmitting
                    ? const SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                      )
                    : const Icon(Icons.check_circle_outline_rounded, size: 20),
                label: Text(
                  _isSubmitting ? 'Guardando reseña...' : 'Publicar Calificación',
                  style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

