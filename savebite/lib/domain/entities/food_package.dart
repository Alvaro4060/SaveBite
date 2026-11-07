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
  final bool isActive;

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
    this.isActive = true,
  });

  int get discountPercentage =>
      (((originalPrice - discountedPrice) / originalPrice) * 100).round();

  bool get isAvailable => isActive && remainingStock > 0;

  FoodPackage copyWith({
    String? title,
    String? description,
    String? category,
    double? originalPrice,
    double? discountedPrice,
    int? initialStock,
    int? remainingStock,
    String? pickupTimeWindow,
    double? estimatedKg,
    double? co2SavedKg,
    String? categoryEmoji,
    bool? isActive,
  }) {
    return FoodPackage(
      id: id,
      storeId: storeId,
      storeName: storeName,
      title: title ?? this.title,
      description: description ?? this.description,
      category: category ?? this.category,
      originalPrice: originalPrice ?? this.originalPrice,
      discountedPrice: discountedPrice ?? this.discountedPrice,
      initialStock: initialStock ?? this.initialStock,
      remainingStock: remainingStock ?? this.remainingStock,
      pickupTimeWindow: pickupTimeWindow ?? this.pickupTimeWindow,
      estimatedKg: estimatedKg ?? this.estimatedKg,
      co2SavedKg: co2SavedKg ?? this.co2SavedKg,
      categoryEmoji: categoryEmoji ?? this.categoryEmoji,
      isActive: isActive ?? this.isActive,
    );
  }
}
