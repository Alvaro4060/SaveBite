import 'package:flutter/material.dart';

/// Paleta cromática oficial de SaveBite
/// Alineada al Documento de Fase 1 - Desarrollo Móvil Integral UTS
class AppColors {
  // Primarios Institucionales
  static const Color primary = Color(0xFF0F4C81); // Azul Profundo
  static const Color primaryDark = Color(0xFF0A2E50);
  static const Color primaryLight = Color(0xFF2563EB);

  // Secundarios y Acentos
  static const Color secondary = Color(0xFF00AE9D); // Verde Turquesa / Sostenible
  static const Color secondaryDark = Color(0xFF0E7490);
  static const Color accent = Color(0xFFF58220); // Naranja Ahorro / Oferta
  static const Color accentHover = Color(0xFFEA580C);

  // Estados y Métricas ODS
  static const Color success = Color(0xFF10B981); // Verde Éxito
  static const Color greenDark = Color(0xFF047857);
  static const Color warning = Color(0xFFF59E0B);
  static const Color error = Color(0xFFEF4444);
  static const Color purple = Color(0xFF8B5CF6);

  // Fondos y Superficies
  static const Color background = Color(0xFFF8FAFC);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color surfaceMuted = Color(0xFFF1F5F9);
  static const Color dark = Color(0xFF0F172A);

  // Textos
  static const Color textPrimary = Color(0xFF1E293B);
  static const Color textSecondary = Color(0xFF64748B);
  static const Color textMuted = Color(0xFF94A3B8);
  static const Color textLight = Color(0xFFFFFFFF);

  // Bordes y Sombras
  static const Color border = Color(0xFFE2E8F0);
  static const Color borderFocused = Color(0xFF94A3B8);

  // Gradientes
  static const LinearGradient heroGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFF071E36),
      Color(0xFF0F4C81),
      Color(0xFF00AE9D),
    ],
  );

  static const LinearGradient accentGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFFF58220),
      Color(0xFFEA580C),
    ],
  );

  static const LinearGradient ecoGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFF10B981),
      Color(0xFF047857),
    ],
  );
}
