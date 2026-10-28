class Store {
  final String id;
  final String name;
  final String category; // 'Panadería', 'Cafetería', 'Frutería', 'Restaurante'
  final String address;
  final double latitude;
  final double longitude;
  final double distanceKm;
  final double rating;
  final String iconEmoji;

  const Store({
    required this.id,
    required this.name,
    required this.category,
    required this.address,
    required this.latitude,
    required this.longitude,
    required this.distanceKm,
    required this.rating,
    required this.iconEmoji,
  });
}
