class Review {
  final String id;
  final String reservationId;
  final String? storeId;
  final String storeName;
  final String packageTitle;
  final String userName;
  final String userInitials;
  final double rating; // 1.0 to 5.0
  final String comment;
  final List<String> tags;
  final DateTime createdAt;

  const Review({
    required this.id,
    required this.reservationId,
    this.storeId,
    required this.storeName,
    required this.packageTitle,
    required this.userName,
    required this.userInitials,
    required this.rating,
    required this.comment,
    this.tags = const [],
    required this.createdAt,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'reservation_id': reservationId,
      'store_id': storeId,
      'store_name': storeName,
      'package_title': packageTitle,
      'user_name': userName,
      'user_initials': userInitials,
      'rating': rating,
      'comment': comment,
      'tags': tags,
      'created_at': createdAt.toIso8601String(),
    };
  }

  factory Review.fromJson(Map<String, dynamic> json) {
    return Review(
      id: json['id'] as String? ?? 'rev_${DateTime.now().millisecondsSinceEpoch}',
      reservationId: json['reservation_id'] as String? ?? '',
      storeId: json['store_id'] as String?,
      storeName: json['store_name'] as String? ?? 'Comercio Local',
      packageTitle: json['package_title'] as String? ?? 'Paquete Sorpresa',
      userName: json['user_name'] as String? ?? 'Usuario SaveBite',
      userInitials: json['user_initials'] as String? ?? 'SB',
      rating: (json['rating'] as num?)?.toDouble() ?? 5.0,
      comment: json['comment'] as String? ?? '',
      tags: (json['tags'] as List<dynamic>?)?.map((e) => e.toString()).toList() ?? const [],
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'].toString()) ?? DateTime.now()
          : DateTime.now(),
    );
  }
}

