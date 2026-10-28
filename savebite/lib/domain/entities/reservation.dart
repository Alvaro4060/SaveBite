enum ReservationStatus {
  reserved,
  redeemed,
  expired,
}

class Reservation {
  final String id;
  final String packageId;
  final String packageTitle;
  final String storeName;
  final String pickupWindow;
  final double amountPaid;
  final double originalPrice;
  final DateTime reservedAt;
  final String qrToken; // Token cifrado para canje
  final ReservationStatus status;
  final double co2SavedKg;
  final double foodRescuedKg;
  final bool isOfflineCached;

  const Reservation({
    required this.id,
    required this.packageId,
    required this.packageTitle,
    required this.storeName,
    required this.pickupWindow,
    required this.amountPaid,
    required this.originalPrice,
    required this.reservedAt,
    required this.qrToken,
    required this.status,
    required this.co2SavedKg,
    required this.foodRescuedKg,
    this.isOfflineCached = true,
  });

  bool get isRedeemed => status == ReservationStatus.redeemed;
  bool get isPending => status == ReservationStatus.reserved;

  Reservation copyWith({
    ReservationStatus? status,
  }) {
    return Reservation(
      id: id,
      packageId: packageId,
      packageTitle: packageTitle,
      storeName: storeName,
      pickupWindow: pickupWindow,
      amountPaid: amountPaid,
      originalPrice: originalPrice,
      reservedAt: reservedAt,
      qrToken: qrToken,
      status: status ?? this.status,
      co2SavedKg: co2SavedKg,
      foodRescuedKg: foodRescuedKg,
      isOfflineCached: isOfflineCached,
    );
  }
}
