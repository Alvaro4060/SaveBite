enum RedeemStatus {
  success,
  alreadyRedeemed,
  notFound,
  networkError,
}

class RedeemResult {
  final RedeemStatus status;
  final String message;
  final String token;
  final String? packageTitle;
  final String? storeName;
  final double? amountPaid;
  final DateTime? redeemedAt;

  const RedeemResult({
    required this.status,
    required this.message,
    required this.token,
    this.packageTitle,
    this.storeName,
    this.amountPaid,
    this.redeemedAt,
  });

  bool get isSuccess => status == RedeemStatus.success;
  bool get isAlreadyRedeemed => status == RedeemStatus.alreadyRedeemed;
  bool get isNotFound => status == RedeemStatus.notFound;
}

