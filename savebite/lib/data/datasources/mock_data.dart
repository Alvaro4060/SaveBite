import '../../domain/entities/food_package.dart';
import '../../domain/entities/reservation.dart';
import '../../domain/entities/store.dart';
import '../../domain/entities/eco_impact.dart';

class MockData {
  // Comercios Locales en Salamanca, Gto.
  static final List<Store> stores = [
    const Store(
      id: 'store_1',
      name: 'Panadería La Tradición',
      category: 'Panaderías',
      address: 'Calle Hidalgo #204, Centro, Salamanca',
      latitude: 20.5732,
      longitude: -101.1960,
      distanceKm: 0.8,
      rating: 4.8,
      iconEmoji: '🥖',
    ),
    const Store(
      id: 'store_2',
      name: 'Cafetería La Plazuela',
      category: 'Cafeterías',
      address: 'Calle Morelos #310, Centro, Salamanca',
      latitude: 20.5891,
      longitude: -101.1812,
      distanceKm: 0.5,
      rating: 4.9,
      iconEmoji: '☕',
    ),
    const Store(
      id: 'store_3',
      name: 'Frutería Don Chente',
      category: 'Fruterías',
      address: 'Mercado Tomasa Esteves, Local 45, Salamanca',
      latitude: 20.5710,
      longitude: -101.1988,
      distanceKm: 1.2,
      rating: 4.7,
      iconEmoji: '🍎',
    ),
    const Store(
      id: 'store_4',
      name: 'Pastelería Fina Dulce Antojo',
      category: 'Panaderías',
      address: 'Blvd. Faja de Oro #812, Salamanca',
      latitude: 20.5790,
      longitude: -101.1901,
      distanceKm: 1.5,
      rating: 4.9,
      iconEmoji: '🧁',
    ),
    const Store(
      id: 'store_5',
      name: 'Pizzería & Trattoria Nápoles',
      category: 'Comida Preparada',
      address: 'Av. Cazadora #340, Salamanca',
      latitude: 20.5650,
      longitude: -101.2050,
      distanceKm: 2.1,
      rating: 4.6,
      iconEmoji: '🍕',
    ),
  ];

  // Paquetes Sorpresa Disponibles Hoy
  static final List<FoodPackage> packages = [
    const FoodPackage(
      id: 'pkg_1',
      storeId: 'store_1',
      storeName: 'Panadería La Tradición',
      title: 'Pack Sorpresa Pan Dulce y Bolillo',
      description:
          'Variedad de 6 a 8 piezas de pan recién horneado del día (conchas, cuernos, donas) más 4 bolillos crujientes en perfecto estado.',
      category: 'Panaderías',
      originalPrice: 130.0,
      discountedPrice: 48.0,
      initialStock: 5,
      remainingStock: 3,
      pickupTimeWindow: '19:30 - 20:45',
      estimatedKg: 1.4,
      co2SavedKg: 2.8,
      categoryEmoji: '🥐',
    ),
    const FoodPackage(
      id: 'pkg_2',
      storeId: 'store_2',
      storeName: 'Cafetería La Plazuela',
      title: 'Pack Café & Baguette de la Tarde',
      description:
          '1 Baguette artesanal de jamón y queso gourmet + 1 rebanada de tarta de manzana casera preparada esta mañana.',
      category: 'Cafeterías',
      originalPrice: 155.0,
      discountedPrice: 55.0,
      initialStock: 4,
      remainingStock: 2,
      pickupTimeWindow: '18:00 - 19:15',
      estimatedKg: 0.9,
      co2SavedKg: 1.9,
      categoryEmoji: '☕',
    ),
    const FoodPackage(
      id: 'pkg_3',
      storeId: 'store_3',
      storeName: 'Frutería Don Chente',
      title: 'Canasta de Fruta Dulce para Smoothie',
      description:
          'Lote de plátanos tabasco maduros, manzanas, fresas y mangos ideales para licuados o consumo inmediato.',
      category: 'Fruterías',
      originalPrice: 120.0,
      discountedPrice: 40.0,
      initialStock: 6,
      remainingStock: 4,
      pickupTimeWindow: '17:30 - 19:00',
      estimatedKg: 2.5,
      co2SavedKg: 3.2,
      categoryEmoji: '🍓',
    ),
    const FoodPackage(
      id: 'pkg_4',
      storeId: 'store_4',
      storeName: 'Pastelería Fina Dulce Antojo',
      title: 'Caja Sorpresa de Muffins & Pays',
      description:
          'Surtido de 4 muffins rellenos de arándano y chocolate, y 2 tartaletas de zarzamora del turno matutino.',
      category: 'Panaderías',
      originalPrice: 180.0,
      discountedPrice: 65.0,
      initialStock: 3,
      remainingStock: 1,
      pickupTimeWindow: '20:00 - 21:00',
      estimatedKg: 1.1,
      co2SavedKg: 2.2,
      categoryEmoji: '🧁',
    ),
    const FoodPackage(
      id: 'pkg_5',
      storeId: 'store_5',
      storeName: 'Pizzería & Trattoria Nápoles',
      title: 'Porciones de Pizza Artesanal',
      description:
          '4 Rebanadas grandes de masa madre al estilo napolitano (Pepperoni y Margherita) recién retiradas del horno de piedra.',
      category: 'Comida Preparada',
      originalPrice: 160.0,
      discountedPrice: 60.0,
      initialStock: 4,
      remainingStock: 2,
      pickupTimeWindow: '21:00 - 22:00',
      estimatedKg: 1.3,
      co2SavedKg: 2.7,
      categoryEmoji: '🍕',
    ),
  ];

  // Reservas activas de ejemplo para el Estudiante
  static final List<Reservation> initialReservations = [
    Reservation(
      id: 'RES-8921-SB',
      packageId: 'pkg_1',
      packageTitle: 'Pack Sorpresa Pan Dulce y Bolillo',
      storeName: 'Panadería La Tradición',
      pickupWindow: '19:30 - 20:45',
      amountPaid: 48.0,
      originalPrice: 130.0,
      reservedAt: DateTime.now().subtract(const Duration(minutes: 25)),
      qrToken: 'SB-TOKEN-8921-PANADERIA-2026',
      status: ReservationStatus.reserved,
      co2SavedKg: 2.8,
      foodRescuedKg: 1.4,
      isOfflineCached: true,
    ),
    Reservation(
      id: 'RES-7419-SB',
      packageId: 'pkg_2',
      packageTitle: 'Pack Café & Baguette de la Tarde',
      storeName: 'Cafetería La Plazuela',
      pickupWindow: 'Ayer 18:00 - 19:15',
      amountPaid: 55.0,
      originalPrice: 155.0,
      reservedAt: DateTime.now().subtract(const Duration(days: 1)),
      qrToken: 'SB-TOKEN-7419-CAFE-DONE',
      status: ReservationStatus.redeemed,
      co2SavedKg: 1.9,
      foodRescuedKg: 0.9,
      isOfflineCached: true,
    ),
  ];

  // Datos de Impacto ODS Iniciales
  static EcoImpact getInitialImpact() {
    return const EcoImpact(
      totalKgRescued: 8.6,
      totalCo2AvoidedKg: 17.2,
      totalMoneySavedMxn: 520.0,
      totalPacksRescued: 6,
      badges: [
        EcoBadge(
          title: 'Rescatador Novato',
          description: 'Rescataste tu primer paquete sorpresa evitando el vertedero.',
          iconEmoji: '🌱',
          isUnlocked: true,
          dateEarned: '10 Oct 2026',
        ),
        EcoBadge(
          title: 'Amigo de Panaderías',
          description: 'Salvaste más de 5 kg de pan dulce y bolillos locales.',
          iconEmoji: '🥖',
          isUnlocked: true,
          dateEarned: '18 Oct 2026',
        ),
        EcoBadge(
          title: 'Héroe Cero Merma (ODS 12)',
          description: 'Alcanzaste más de 15 kg de CO₂ equivalente mitigados.',
          iconEmoji: '🏆',
          isUnlocked: true,
          dateEarned: '24 Oct 2026',
        ),
        EcoBadge(
          title: 'Guardián de Salamanca',
          description: 'Rescata 10 paquetes en cualquier establecimiento de la ciudad.',
          iconEmoji: '🌟',
          isUnlocked: false,
          dateEarned: 'En progreso (6/10)',
        ),
      ],
    );
  }
}
