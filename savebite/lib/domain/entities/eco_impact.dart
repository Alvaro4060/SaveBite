class EcoBadge {
  final String title;
  final String description;
  final String iconEmoji;
  final bool isUnlocked;
  final String dateEarned;

  const EcoBadge({
    required this.title,
    required this.description,
    required this.iconEmoji,
    required this.isUnlocked,
    required this.dateEarned,
  });
}

class EcoImpact {
  final double totalKgRescued;
  final double totalCo2AvoidedKg;
  final double totalMoneySavedMxn;
  final int totalPacksRescued;
  final List<EcoBadge> badges;

  const EcoImpact({
    required this.totalKgRescued,
    required this.totalCo2AvoidedKg,
    required this.totalMoneySavedMxn,
    required this.totalPacksRescued,
    required this.badges,
  });
}
