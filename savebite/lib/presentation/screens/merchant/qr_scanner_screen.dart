import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_styles.dart';
import '../../state/app_state.dart';
import '../../widgets/custom_button.dart';

class QrScannerScreen extends StatefulWidget {
  const QrScannerScreen({super.key});

  @override
  State<QrScannerScreen> createState() => _QrScannerScreenState();
}

class _QrScannerScreenState extends State<QrScannerScreen> with SingleTickerProviderStateMixin {
  late AnimationController _laserController;
  final TextEditingController _manualCodeController = TextEditingController();
  bool _isTorchOn = false;

  @override
  void initState() {
    super.initState();
    _laserController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _laserController.dispose();
    _manualCodeController.dispose();
    super.dispose();
  }

  void _validateCode(String token, AppState appState) {
    final success = appState.redeemQrToken(token);

    if (success) {
      _showRedeemSuccessDialog(token);
    } else {
      _showRedeemErrorDialog(token);
    }
  }

  void _showRedeemSuccessDialog(String token) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      isScrollControlled: true,
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
              width: 64,
              height: 64,
              decoration: BoxDecoration(
                color: AppColors.success.withOpacity(0.12),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.check_circle_rounded, color: AppColors.success, size: 40),
            ),
            const SizedBox(height: 16),
            const Text('¡Entrega Validada con Éxito!', style: AppStyles.heading2),
            const SizedBox(height: 8),
            const Text(
              'El código QR fue verificado en menos de 2 segundos. La transacción quedó registrada.',
              textAlign: TextAlign.center,
              style: AppStyles.body,
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.surfaceMuted,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.verified_rounded, size: 16, color: AppColors.greenDark),
                  const SizedBox(width: 8),
                  Text(
                    'Token: $token',
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: AppColors.primary),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            CustomButton(
              text: 'Aceptar y Volver al Escáner',
              backgroundColor: AppColors.primary,
              onPressed: () => Navigator.of(ctx).pop(),
            ),
            const SizedBox(height: 10),
          ],
        ),
      ),
    );
  }

  void _showRedeemErrorDialog(String token) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        backgroundColor: AppColors.error,
        content: Text('Código inválido o ya canjeado anteriormente: $token'),
      ),
    );
  }

  void _showManualInputDialog(AppState appState) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Ingresar Código Manual', style: AppStyles.heading3),
        content: TextField(
          controller: _manualCodeController,
          decoration: const InputDecoration(
            hintText: 'Ej. RES-8921-SB o SB-TOKEN-...',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(ctx).pop();
              _validateCode(_manualCodeController.text.trim(), appState);
            },
            child: const Text('Validar'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final pendingReservations = appState.pendingReservations;

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
        title: const Text(
          'Lector de Mostrador (QR)',
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
        actions: [
          IconButton(
            icon: Icon(_isTorchOn ? Icons.flash_on : Icons.flash_off, color: Colors.white),
            onPressed: () => setState(() => _isTorchOn = !_isTorchOn),
          ),
        ],
      ),
      body: Stack(
        children: [
          // Visor de Cámara con Retícula y Láser
          Center(
            child: Container(
              width: 260,
              height: 260,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.white.withOpacity(0.4), width: 1.5),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Stack(
                children: [
                  // Esquinas iluminadas
                  const Positioned(
                    top: 0,
                    left: 0,
                    child: _CornerMarker(isTop: true, isLeft: true),
                  ),
                  const Positioned(
                    top: 0,
                    right: 0,
                    child: _CornerMarker(isTop: true, isLeft: false),
                  ),
                  const Positioned(
                    bottom: 0,
                    left: 0,
                    child: _CornerMarker(isTop: false, isLeft: true),
                  ),
                  const Positioned(
                    bottom: 0,
                    right: 0,
                    child: _CornerMarker(isTop: false, isLeft: false),
                  ),

                  // Línea de Escaneo Láser Animada
                  AnimatedBuilder(
                    animation: _laserController,
                    builder: (context, child) {
                      return Positioned(
                        top: _laserController.value * 240,
                        left: 10,
                        right: 10,
                        child: Container(
                          height: 3,
                          decoration: BoxDecoration(
                            color: AppColors.secondary,
                            boxShadow: [
                              BoxShadow(
                                color: AppColors.secondary.withOpacity(0.8),
                                blurRadius: 8,
                                spreadRadius: 2,
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
          ),

          // Texto de Instrucciones Superior
          Positioned(
            top: 24,
            left: 20,
            right: 20,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.7),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: Colors.white.withOpacity(0.2)),
              ),
              child: const Text(
                'Apunta la cámara al voucher QR del cliente para validar la entrega en mostrador.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.white, fontSize: 12.5),
              ),
            ),
          ),

          // Botones Inferiores de Demostración
          Positioned(
            bottom: 30,
            left: 20,
            right: 20,
            child: Column(
              children: [
                // Simulación Rápida de Escaneo de Voucher Existente
                if (pendingReservations.isNotEmpty)
                  CustomButton(
                    text: 'Simular Escaneo: ${pendingReservations.first.id}',
                    icon: Icons.qr_code_scanner,
                    backgroundColor: AppColors.success,
                    onPressed: () {
                      _validateCode(pendingReservations.first.qrToken, appState);
                    },
                  )
                else
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.white12,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Text(
                      'No hay reservas activas pendientes en la demo.\nReserva primero un paquete como consumidor.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                  ),

                const SizedBox(height: 12),

                // Ingreso Manual de Código
                OutlinedButton.icon(
                  onPressed: () => _showManualInputDialog(appState),
                  icon: const Icon(Icons.keyboard, color: Colors.white, size: 18),
                  label: const Text(
                    'Ingresar Código Alfanumérico Manual',
                    style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13),
                  ),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Colors.white54),
                    padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
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

class _CornerMarker extends StatelessWidget {
  final bool isTop;
  final bool isLeft;

  const _CornerMarker({required this.isTop, required this.isLeft});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 24,
      height: 24,
      decoration: BoxDecoration(
        border: Border(
          top: isTop ? const BorderSide(color: AppColors.secondary, width: 4) : BorderSide.none,
          bottom: !isTop ? const BorderSide(color: AppColors.secondary, width: 4) : BorderSide.none,
          left: isLeft ? const BorderSide(color: AppColors.secondary, width: 4) : BorderSide.none,
          right: !isLeft ? const BorderSide(color: AppColors.secondary, width: 4) : BorderSide.none,
        ),
      ),
    );
  }
}
