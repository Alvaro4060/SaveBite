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
  final bool isReviewed;
  final double? userRating;
  final String? userReviewComment;

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
    this.isReviewed = false,
    this.userRating,
    this.userReviewComment,
  });

  bool get isRedeemed => status == ReservationStatus.redeemed;
  bool get isPending => status == ReservationStatus.reserved;

  Reservation copyWith({
    ReservationStatus? status,
    bool? isReviewed,
    double? userRating,
    String? userReviewComment,
    bool? isOfflineCached,
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
      isOfflineCached: isOfflineCached ?? this.isOfflineCached,
      isReviewed: isReviewed ?? this.isReviewed,
      userRating: userRating ?? this.userRating,
      userReviewComment: userReviewComment ?? this.userReviewComment,
    );
  }
}
