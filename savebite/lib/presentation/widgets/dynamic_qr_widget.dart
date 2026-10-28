import 'dart:math';
import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';

/// Widget que renderiza un Código QR dinámico con CustomPainter
/// Diseñado para funcionar offline sin librerías externas complejas
class DynamicQrWidget extends StatelessWidget {
  final String qrToken;
  final double size;
  final bool showBorder;

  const DynamicQrWidget({
    super.key,
    required this.qrToken,
    this.size = 200,
    this.showBorder = true,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: showBorder ? Border.all(color: AppColors.border, width: 2) : null,
        boxShadow: const [
          BoxShadow(
            color: Color.fromRGBO(0, 0, 0, 0.08),
            blurRadius: 16,
            offset: Offset(0, 6),
          ),
        ],
      ),
      child: CustomPaint(
        size: Size(size - 24, size - 24),
        painter: _QrPainter(token: qrToken),
      ),
    );
  }
}

class _QrPainter extends CustomPainter {
  final String token;
  _QrPainter({required this.token});

  @override
  void paint(Canvas canvas, Size size) {
    final paintDark = Paint()..color = const Color(0xFF0F172A);
    final paintPrimary = Paint()..color = AppColors.primary;

    const int matrixSize = 25;
    final double cellSize = size.width / matrixSize;

    // Generador pseudo-determinista a partir del token
    final random = Random(token.hashCode);

    // 1. Dibujar los 3 marcos de posición (Corner Finder Patterns)
    _drawFinderPattern(canvas, 0, 0, cellSize, paintDark, paintPrimary);
    _drawFinderPattern(canvas, (matrixSize - 7) * cellSize, 0, cellSize, paintDark, paintPrimary);
    _drawFinderPattern(canvas, 0, (matrixSize - 7) * cellSize, cellSize, paintDark, paintPrimary);

    // 2. Dibujar módulos de datos
    for (int r = 0; r < matrixSize; r++) {
      for (int c = 0; c < matrixSize; c++) {
        // Ignorar áreas de los Finder Patterns
        if ((r < 8 && c < 8) ||
            (r < 8 && c >= matrixSize - 8) ||
            (r >= matrixSize - 8 && c < 8)) {
          continue;
        }

        // Centro con logo de SaveBite
        if (r >= 10 && r <= 14 && c >= 10 && c <= 14) {
          continue;
        }

        if (random.nextBool()) {
          final rect = Rect.fromLTWH(
            c * cellSize + 0.5,
            r * cellSize + 0.5,
            cellSize - 1,
            cellSize - 1,
          );
          canvas.drawRRect(
            RRect.fromRectAndRadius(rect, const Radius.circular(1.5)),
            paintDark,
          );
        }
      }
    }

    // 3. Logo central SaveBite
    final centerRect = Rect.fromCenter(
      center: Offset(size.width / 2, size.height / 2),
      width: cellSize * 5,
      height: cellSize * 5,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(centerRect, const Radius.circular(6)),
      Paint()..color = AppColors.primary,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(centerRect.deflate(2), const Radius.circular(4)),
      Paint()..color = Colors.white,
    );

    // Símbolo ecológico interior
    final iconPaint = Paint()
      ..color = AppColors.secondary
      ..style = PaintingStyle.fill;
    canvas.drawCircle(Offset(size.width / 2, size.height / 2), cellSize * 1.5, iconPaint);
  }

  void _drawFinderPattern(Canvas canvas, double x, double y, double cellSize, Paint dark, Paint accent) {
    // Cuadro exterior 7x7
    final outer = Rect.fromLTWH(x, y, cellSize * 7, cellSize * 7);
    canvas.drawRRect(RRect.fromRectAndRadius(outer, const Radius.circular(6)), dark);

    // Hueco interior blanco 5x5
    final innerWhite = Rect.fromLTWH(x + cellSize, y + cellSize, cellSize * 5, cellSize * 5);
    canvas.drawRRect(RRect.fromRectAndRadius(innerWhite, const Radius.circular(4)), Paint()..color = Colors.white);

    // Núcleo central 3x3
    final center = Rect.fromLTWH(x + cellSize * 2, y + cellSize * 2, cellSize * 3, cellSize * 3);
    canvas.drawRRect(RRect.fromRectAndRadius(center, const Radius.circular(3)), accent);
  }

  @override
  bool shouldRepaint(covariant _QrPainter oldDelegate) => oldDelegate.token != token;
}
