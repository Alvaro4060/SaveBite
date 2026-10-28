enum UserRole { consumer, merchant }

class UserProfile {
  final String id;
  final String name;
  final String email;
  final UserRole role;
  final String? storeId;
  final String? storeName;
  final String avatarInitials;

  const UserProfile({
    required this.id,
    required this.name,
    required this.email,
    required this.role,
    this.storeId,
    this.storeName,
    required this.avatarInitials,
  });

  bool get isMerchant => role == UserRole.merchant;
}
