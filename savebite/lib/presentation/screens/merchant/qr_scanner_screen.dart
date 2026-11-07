import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_styles.dart';
import '../../../core/utils/formatters.dart';
import '../../../domain/entities/redeem_result.dart';
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
  final MobileScannerController _scannerController = MobileScannerController(
    detectionSpeed: DetectionSpeed.normal,
    facing: CameraFacing.back,
    torchEnabled: false,
  );

  bool _isProcessingCode = false;
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
    _scannerController.dispose();
    super.dispose();
  }

  void _onDetectBarcode(BarcodeCapture capture, AppState appState) {
    if (_isProcessingCode) return;
    final barcodes = capture.barcodes;
    for (final barcode in barcodes) {
      final rawValue = barcode.rawValue;
      if (rawValue != null && rawValue.trim().isNotEmpty) {
        _isProcessingCode = true;
        _validateCode(rawValue.trim(), appState);
        break;
      }
    }
  }

  void _validateCode(String token, AppState appState) async {
    final result = await appState.redeemQrToken(token);

    if (!mounted) return;

    if (result.isSuccess) {
      _showRedeemSuccessDialog(result);
    } else if (result.isAlreadyRedeemed) {
      _showAlreadyRedeemedDialog(result);
    } else {
      _showRedeemErrorDialog(result.message);
    }
  }

  void _showRedeemSuccessDialog(RedeemResult result) {
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
                color: AppColors.success.withValues(alpha: 0.12),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.check_circle_rounded, color: AppColors.success, size: 40),
            ),
            const SizedBox(height: 16),
            const Text('¡Entrega Validada con Éxito!', style: AppStyles.heading2),
            const SizedBox(height: 8),
            Text(
              result.packageTitle != null
                  ? 'Paquete: ${result.packageTitle}'
                  : 'El código QR fue verificado y el canje quedó registrado en Supabase.',
              textAlign: TextAlign.center,
              style: AppStyles.body.copyWith(fontWeight: FontWeight.w600),
            ),
            if (result.amountPaid != null) ...[
              const SizedBox(height: 4),
              Text(
                'Cobrado / Pagado: ${Formatters.formatCurrency(result.amountPaid!)}',
                style: const TextStyle(fontSize: 13, color: AppColors.textSecondary),
              ),
            ],
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
                  Flexible(
                    child: Text(
                      'Cupón: ${result.token}',
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: AppColors.primary),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            CustomButton(
              text: 'Aceptar y Volver al Escáner',
              backgroundColor: AppColors.primary,
              onPressed: () {
                Navigator.of(ctx).pop();
                setState(() => _isProcessingCode = false);
              },
            ),
            const SizedBox(height: 10),
          ],
        ),
      ),
    ).then((_) {
      if (mounted) setState(() => _isProcessingCode = false);
    });
  }

  void _showAlreadyRedeemedDialog(RedeemResult result) {
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
                color: AppColors.warning.withValues(alpha: 0.15),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.warning_amber_rounded, color: AppColors.warning, size: 40),
            ),
            const SizedBox(height: 16),
            const Text('Cupón Ya Canjeado', style: AppStyles.heading2),
            const SizedBox(height: 8),
            Text(
              'Este paquete (${result.packageTitle ?? 'reserva'}) ya fue entregado y canjeado previamente.',
              textAlign: TextAlign.center,
              style: AppStyles.body,
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.warning.withValues(alpha: 0.08),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppColors.warning.withValues(alpha: 0.3)),
              ),
              child: Text(
                'Código: ${result.token}',
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: AppColors.accentHover),
              ),
            ),
            const SizedBox(height: 20),
            CustomButton(
              text: 'Cerrar',
              backgroundColor: AppColors.warning,
              onPressed: () {
                Navigator.of(ctx).pop();
                setState(() => _isProcessingCode = false);
              },
            ),
            const SizedBox(height: 10),
          ],
        ),
      ),
    ).then((_) {
      if (mounted) setState(() => _isProcessingCode = false);
    });
  }

  void _showRedeemErrorDialog(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        backgroundColor: AppColors.error,
        content: Text(message),
        duration: const Duration(seconds: 3),
      ),
    );
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) setState(() => _isProcessingCode = false);
    });
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
              _isProcessingCode = true;
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
          'Lector de Mostrador (Cámara QR)',
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
        actions: [
          IconButton(
            icon: Icon(_isTorchOn ? Icons.flash_on : Icons.flash_off, color: Colors.white),
            onPressed: () async {
              await _scannerController.toggleTorch();
              setState(() => _isTorchOn = !_isTorchOn);
            },
          ),
          IconButton(
            icon: const Icon(Icons.cameraswitch_outlined, color: Colors.white),
            onPressed: () => _scannerController.switchCamera(),
          ),
        ],
      ),
      body: Stack(
        fit: StackFit.expand,
        children: [
          // Visor de Cámara Nativa
          MobileScanner(
            controller: _scannerController,
            onDetect: (capture) => _onDetectBarcode(capture, appState),
            errorBuilder: (context, error) {
              return Center(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.videocam_off_outlined, color: Colors.white70, size: 48),
                      const SizedBox(height: 12),
                      Text(
                        'Cámara no disponible o sin permisos:\n${error.errorDetails?.message ?? error.toString()}',
                        textAlign: TextAlign.center,
                        style: const TextStyle(color: Colors.white70, fontSize: 13),
                      ),
                    ],
                  ),
                ),
              );
            },
          ),

          // Máscara oscura alrededor de la zona de escaneo
          Center(
            child: Container(
              width: 270,
              height: 270,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.white.withValues(alpha: 0.4), width: 1.5),
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

                  // Línea Láser Animada
                  AnimatedBuilder(
                    animation: _laserController,
                    builder: (context, child) {
                      return Positioned(
                        top: _laserController.value * 250,
                        left: 10,
                        right: 10,
                        child: Container(
                          height: 3,
                          decoration: BoxDecoration(
                            color: AppColors.secondary,
                            boxShadow: [
                              BoxShadow(
                                color: AppColors.secondary.withValues(alpha: 0.8),
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

          // Instrucción Superior
          Positioned(
            top: 20,
            left: 20,
            right: 20,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              decoration: BoxDecoration(
                color: Colors.black.withValues(alpha: 0.7),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: Colors.white.withValues(alpha: 0.2)),
              ),
              child: const Text(
                'Apunta la cámara al voucher QR del cliente para validar la entrega en mostrador.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.white, fontSize: 12.5),
              ),
            ),
          ),

          // Controles Inferiores (Simulador + Código Manual)
          Positioned(
            bottom: 24,
            left: 20,
            right: 20,
            child: Column(
              children: [
                if (pendingReservations.isNotEmpty)
                  CustomButton(
                    text: 'Probar con reserva activa: ${pendingReservations.first.id}',
                    icon: Icons.qr_code_scanner,
                    backgroundColor: AppColors.success,
                    onPressed: () {
                      _isProcessingCode = true;
                      _validateCode(pendingReservations.first.qrToken, appState);
                    },
                  )
                else
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.black54,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Text(
                      'Cámara activa lista para leer cualquier QR de SaveBite.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                  ),

                const SizedBox(height: 10),

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
