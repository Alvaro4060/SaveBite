class FoodPackage {
  final String id;
  final String storeId;
  final String storeName;
  final String title;
  final String description;
  final String category;
  final double originalPrice;
  final double discountedPrice;
  final int initialStock;
  final int remainingStock;
  final String pickupTimeWindow; // e.g. "19:30 - 20:30"
  final double estimatedKg;
  final double co2SavedKg;
  final String categoryEmoji;

  const FoodPackage({
    required this.id,
    required this.storeId,
    required this.storeName,
    required this.title,
    required this.description,
    required this.category,
    required this.originalPrice,
    required this.discountedPrice,
    required this.initialStock,
    required this.remainingStock,
    required this.pickupTimeWindow,
    required this.estimatedKg,
    required this.co2SavedKg,
    required this.categoryEmoji,
  });

  int get discountPercentage =>
      (((originalPrice - discountedPrice) / originalPrice) * 100).round();

  bool get isAvailable => remainingStock > 0;

  FoodPackage copyWith({
    int? remainingStock,
  }) {
    return FoodPackage(
      id: id,
      storeId: storeId,
      storeName: storeName,
      title: title,
      description: description,
      category: category,
      originalPrice: originalPrice,
      discountedPrice: discountedPrice,
      initialStock: initialStock,
      remainingStock: remainingStock ?? this.remainingStock,
      pickupTimeWindow: pickupTimeWindow,
      estimatedKg: estimatedKg,
      co2SavedKg: co2SavedKg,
      categoryEmoji: categoryEmoji,
    );
  }
}
