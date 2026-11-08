class Formatters {
  /// Formatea precio en pesos mexicanos
  static String formatCurrency(double amount) {
    return '\$${amount.toStringAsFixed(0)} MXN';
  }

  /// Calcula el porcentaje de descuento
  static int calculateDiscount(double original, double discounted) {
    if (original <= 0) return 0;
    return (((original - discounted) / original) * 100).round();
  }

  /// Formatea distancia en metros o kilómetros
  static String formatDistance(double distanceInKm) {
    if (distanceInKm < 1.0) {
      return '${(distanceInKm * 1000).toInt()} m';
    }
    return '${distanceInKm.toStringAsFixed(1)} km';
  }

  /// Formatea la hora (ej: 19:45 hrs)
  static String formatTime(DateTime dt) {
    final h = dt.hour.toString().padLeft(2, '0');
    final m = dt.minute.toString().padLeft(2, '0');
    return '$h:$m hrs';
  }

  /// Formatea la fecha (ej: 07 Nov 2026)
  static String formatDate(DateTime dt) {
    const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    return '${dt.day.toString().padLeft(2, '0')} ${months[dt.month - 1]} ${dt.year}';
  }
}
