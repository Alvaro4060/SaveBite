import 'package:flutter/material.dart';
import '../../domain/entities/user_profile.dart';
import '../../domain/entities/food_package.dart';
import '../../domain/entities/reservation.dart';
import '../../domain/entities/store.dart';
import '../../domain/entities/eco_impact.dart';
import '../../data/datasources/mock_data.dart';
export 'app_state_provider.dart';

class AppState extends ChangeNotifier {
  // Perfiles de demostración
  static const UserProfile consumerUser = UserProfile(
    id: 'user_01',
    name: 'Juan Pablo Vega',
    email: 'juan.vega@gmail.com',
    role: UserRole.consumer,
    avatarInitials: 'JV',
  );

  static const UserProfile merchantUser = UserProfile(
    id: 'merchant_01',
    name: 'Don Ricardo Torres',
    email: 'panaderia.latradicion@gmail.com',
    role: UserRole.merchant,
    storeId: 'store_1',
    storeName: 'Panadería La Tradición',
    avatarInitials: 'RT',
  );

  // Estado Actual
  UserProfile _currentUser = consumerUser;
  List<FoodPackage> _packages = List.from(MockData.packages);
  List<Reservation> _reservations = List.from(MockData.initialReservations);
  final List<Store> _stores = List.from(MockData.stores);
  EcoImpact _ecoImpact = MockData.getInitialImpact();

  String _selectedCategory = 'Todos';
  String _searchQuery = '';
  bool _isOfflineMode = false;
  int _currentTabIndex = 0;

  // Getters
  UserProfile get currentUser => _currentUser;
  bool get isMerchant => _currentUser.isMerchant;
  List<FoodPackage> get packages => _filteredPackages();
  List<FoodPackage> get allPackages => _packages;
  List<Reservation> get reservations => _reservations;
  List<Store> get stores => _stores;
  EcoImpact get ecoImpact => _ecoImpact;
  String get selectedCategory => _selectedCategory;
  String get searchQuery => _searchQuery;
  bool get isOfflineMode => _isOfflineMode;
  int get currentTabIndex => _currentTabIndex;

  // Paquetes para el comercio actual
  List<FoodPackage> get merchantPackages {
    return _packages.where((p) => p.storeId == (_currentUser.storeId ?? 'store_1')).toList();
  }

  // Reservas activas pendientes de recoger
  List<Reservation> get pendingReservations {
    return _reservations.where((r) => r.isPending).toList();
  }

  // Filtrado reactivo de paquetes
  List<FoodPackage> _filteredPackages() {
    return _packages.where((p) {
      final matchesCategory = _selectedCategory == 'Todos' || p.category == _selectedCategory;
      final matchesSearch = _searchQuery.isEmpty ||
          p.title.toLowerCase().contains(_searchQuery.toLowerCase()) ||
          p.storeName.toLowerCase().contains(_searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    }).toList();
  }

  // Métodos de Cambio de Estado
  void setTabIndex(int index) {
    _currentTabIndex = index;
    notifyListeners();
  }

  void switchRole(UserRole newRole) {
    if (newRole == UserRole.merchant) {
      _currentUser = merchantUser;
      _currentTabIndex = 0; // Tab comercio
    } else {
      _currentUser = consumerUser;
      _currentTabIndex = 0; // Tab feed
    }
    notifyListeners();
  }

  void setCategory(String category) {
    _selectedCategory = category;
    notifyListeners();
  }

  void setSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }

  void toggleOfflineMode() {
    _isOfflineMode = !_isOfflineMode;
    notifyListeners();
  }

  /// Realiza la reserva in-app de un paquete sorpresa
  Reservation reservePackage(FoodPackage package) {
    final newReservationId = 'RES-${DateTime.now().millisecondsSinceEpoch.toString().substring(7)}-SB';
    final qrToken = 'SB-TOKEN-${package.id}-${DateTime.now().millisecondsSinceEpoch}';

    final reservation = Reservation(
      id: newReservationId,
      packageId: package.id,
      packageTitle: package.title,
      storeName: package.storeName,
      pickupWindow: package.pickupTimeWindow,
      amountPaid: package.discountedPrice,
      originalPrice: package.originalPrice,
      reservedAt: DateTime.now(),
      qrToken: qrToken,
      status: ReservationStatus.reserved,
      co2SavedKg: package.co2SavedKg,
      foodRescuedKg: package.estimatedKg,
      isOfflineCached: true,
    );

    // Reducir stock del paquete
    final index = _packages.indexWhere((p) => p.id == package.id);
    if (index != -1 && _packages[index].remainingStock > 0) {
      final updatedPkg = _packages[index].copyWith(
        remainingStock: _packages[index].remainingStock - 1,
      );
      _packages[index] = updatedPkg;
    }

    _reservations.insert(0, reservation);

    // Actualizar impacto estimado
    _ecoImpact = EcoImpact(
      totalKgRescued: _ecoImpact.totalKgRescued + package.estimatedKg,
      totalCo2AvoidedKg: _ecoImpact.totalCo2AvoidedKg + package.co2SavedKg,
      totalMoneySavedMxn: _ecoImpact.totalMoneySavedMxn + (package.originalPrice - package.discountedPrice),
      totalPacksRescued: _ecoImpact.totalPacksRescued + 1,
      badges: _ecoImpact.badges,
    );

    notifyListeners();
    return reservation;
  }

  /// Publicar nuevo paquete (Modo Comercio)
  void publishNewPackage({
    required String title,
    required String description,
    required String category,
    required double originalPrice,
    required double discountedPrice,
    required int stock,
    required String pickupWindow,
    required double estimatedKg,
    required String categoryEmoji,
  }) {
    final newPkg = FoodPackage(
      id: 'pkg_${DateTime.now().millisecondsSinceEpoch}',
      storeId: _currentUser.storeId ?? 'store_1',
      storeName: _currentUser.storeName ?? 'Panadería La Tradición',
      title: title,
      description: description,
      category: category,
      originalPrice: originalPrice,
      discountedPrice: discountedPrice,
      initialStock: stock,
      remainingStock: stock,
      pickupTimeWindow: pickupWindow,
      estimatedKg: estimatedKg,
      co2SavedKg: estimatedKg * 2.1,
      categoryEmoji: categoryEmoji,
    );

    _packages.insert(0, newPkg);
    notifyListeners();
  }

  /// Canjear y validar entrega mediante escáner QR en mostrador
  bool redeemQrToken(String token) {
    final index = _reservations.indexWhere(
      (r) => r.qrToken == token || r.id == token,
    );

    if (index != -1) {
      final res = _reservations[index];
      if (res.status == ReservationStatus.reserved) {
        _reservations[index] = res.copyWith(status: ReservationStatus.redeemed);
        notifyListeners();
        return true;
      }
    }
    return false;
  }
}
