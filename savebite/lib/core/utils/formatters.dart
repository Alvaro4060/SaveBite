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
}
