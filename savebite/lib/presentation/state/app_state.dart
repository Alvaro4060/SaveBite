import 'package:flutter/material.dart';
import '../../domain/entities/user_profile.dart';
import '../../domain/entities/food_package.dart';
import '../../domain/entities/reservation.dart';
import '../../domain/entities/store.dart';
import '../../domain/entities/eco_impact.dart';
import '../../domain/entities/redeem_result.dart';
import '../../data/datasources/mock_data.dart';
import '../../data/datasources/supabase_service.dart';
export 'app_state_provider.dart';

class AppState extends ChangeNotifier {
  AppState() {
    _initSupabaseListener();
  }

  void _initSupabaseListener() {
    if (SupabaseService.instance.isReady) {
      SupabaseService.instance.getPackagesStream().listen((realtimePackages) {
        if (realtimePackages.isNotEmpty) {
          _packages = realtimePackages;
          notifyListeners();
        }
      });

      SupabaseService.instance.getReservationsStream().listen((realtimeReservations) {
        if (realtimeReservations.isNotEmpty) {
          _reservations = realtimeReservations;
          notifyListeners();
        }
      });
    }
  }
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
    storeId: '11111111-1111-1111-1111-111111111111',
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
    final currentStoreId = _currentUser.storeId ?? '11111111-1111-1111-1111-111111111111';
    final currentStoreName = (_currentUser.storeName ?? 'Panadería La Tradición').toLowerCase().trim();
    return _packages.where((p) {
      return p.storeId == currentStoreId ||
          (currentStoreName.isNotEmpty && p.storeName.toLowerCase().trim() == currentStoreName);
    }).toList();
  }

  // Canjes realizados hoy para este comercio
  List<Reservation> get merchantRedeemedReservations {
    final currentStoreName = (_currentUser.storeName ?? 'Panadería La Tradición').toLowerCase().trim();
    return _reservations.where((r) {
      return r.isRedeemed &&
          (r.storeName.toLowerCase().trim() == currentStoreName ||
              r.storeName.toLowerCase().contains('tradición'));
    }).toList();
  }

  // Reservas activas pendientes de recoger
  List<Reservation> get pendingReservations {
    return _reservations.where((r) => r.isPending).toList();
  }

  // Filtrado reactivo de paquetes
  List<FoodPackage> _filteredPackages() {
    return _packages.where((p) {
      // Si es vista de consumidor, ocultar paquetes pausados o inactivos
      if (!isMerchant && !p.isActive) return false;
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

  void setCurrentUser(UserProfile user) {
    _currentUser = user;
    _currentTabIndex = 0;
    notifyListeners();
  }

  void updateProfileName(String newName) {
    final initials = newName.trim().split(' ').map((p) => p.isNotEmpty ? p[0] : '').take(2).join().toUpperCase();
    _currentUser = UserProfile(
      id: _currentUser.id,
      name: newName,
      email: _currentUser.email,
      role: _currentUser.role,
      storeId: _currentUser.storeId,
      storeName: _currentUser.storeName,
      avatarInitials: initials.isNotEmpty ? initials : _currentUser.avatarInitials,
    );
    notifyListeners();
  }

  Future<bool> signUp({
    required String name,
    required String email,
    required String password,
    required UserRole role,
    String? storeName,
    String? storeCategory,
    String? storeAddress,
  }) async {
    UserProfile? registeredUser;

    if (SupabaseService.instance.isReady && !_isOfflineMode) {
      try {
        registeredUser = await SupabaseService.instance.signUp(
          email: email,
          password: password,
          name: name,
          role: role,
          storeName: storeName,
          storeCategory: storeCategory,
          storeAddress: storeAddress,
        );
      } catch (e) {
        debugPrint('[AppState] Error registrando en Supabase: $e');
      }
    }

    final initials = name.trim().split(' ').map((p) => p.isNotEmpty ? p[0] : '').take(2).join().toUpperCase();
    final user = registeredUser ??
        UserProfile(
          id: 'user_${DateTime.now().millisecondsSinceEpoch}',
          name: name,
          email: email,
          role: role,
          storeId: role == UserRole.merchant ? 'store_${DateTime.now().millisecondsSinceEpoch}' : null,
          storeName: storeName ?? (role == UserRole.merchant ? 'Mi Comercio' : null),
          avatarInitials: initials.isNotEmpty ? initials : (role == UserRole.merchant ? 'MC' : 'SB'),
        );

    _currentUser = user;
    _currentTabIndex = 0;
    notifyListeners();
    return true;
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

  /// Realiza la reserva in-app de un paquete sorpresa (híbrido Supabase + local)
  Future<Reservation> reservePackage(FoodPackage package) async {
    Reservation? supabaseReservation;

    if (SupabaseService.instance.isReady && !_isOfflineMode) {
      supabaseReservation = await SupabaseService.instance.createReservation(
        package: package,
        userId: _currentUser.id,
      );
    }

    final newReservationId = supabaseReservation?.id ??
        'RES-${DateTime.now().millisecondsSinceEpoch.toString().substring(7)}-SB';
    final qrToken = supabaseReservation?.qrToken ??
        'SB-TOKEN-${package.id.substring(0, package.id.length > 8 ? 8 : package.id.length)}-${DateTime.now().millisecondsSinceEpoch}';

    final reservation = supabaseReservation ??
        Reservation(
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

    // Reducir stock del paquete en memoria local
    final index = _packages.indexWhere((p) => p.id == package.id);
    if (index != -1 && _packages[index].remainingStock > 0) {
      final updatedPkg = _packages[index].copyWith(
        remainingStock: _packages[index].remainingStock - 1,
      );
      _packages[index] = updatedPkg;
    }

    if (_reservations.every((r) => r.id != reservation.id && r.qrToken != reservation.qrToken)) {
      _reservations.insert(0, reservation);
    }

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
  Future<FoodPackage> publishNewPackage({
    required String title,
    required String description,
    required String category,
    required double originalPrice,
    required double discountedPrice,
    required int stock,
    required String pickupWindow,
    required double estimatedKg,
    required String categoryEmoji,
  }) async {
    final localId = 'pkg_${DateTime.now().millisecondsSinceEpoch}';
    final storeId = _currentUser.storeId ?? '11111111-1111-1111-1111-111111111111';
    final storeName = _currentUser.storeName ?? 'Panadería La Tradición';

    FoodPackage newPkg = FoodPackage(
      id: localId,
      storeId: storeId,
      storeName: storeName,
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
      isActive: true,
    );

    if (SupabaseService.instance.isReady && !_isOfflineMode) {
      final remotePkg = await SupabaseService.instance.insertPackage(newPkg);
      if (remotePkg != null) {
        newPkg = remotePkg;
      }
    }

    final existingIdx = _packages.indexWhere((p) => p.id == newPkg.id);
    if (existingIdx != -1) {
      _packages[existingIdx] = newPkg;
    } else {
      _packages.insert(0, newPkg);
    }
    notifyListeners();
    return newPkg;
  }

  /// Incrementar o decrementar stock de un paquete (Comercio)
  Future<void> updatePackageStock(String packageId, int delta) async {
    final idx = _packages.indexWhere((p) => p.id == packageId);
    if (idx == -1) return;

    final current = _packages[idx];
    final newStock = (current.remainingStock + delta).clamp(0, 99);
    final updated = current.copyWith(
      remainingStock: newStock,
      isActive: newStock > 0 ? current.isActive : false,
    );

    _packages[idx] = updated;
    notifyListeners();

    if (SupabaseService.instance.isReady && !_isOfflineMode) {
      await SupabaseService.instance.updatePackageStock(packageId, newStock);
    }
  }

  /// Alternar estado de venta Activo / Pausado (Comercio)
  Future<void> togglePackageActive(String packageId) async {
    final idx = _packages.indexWhere((p) => p.id == packageId);
    if (idx == -1) return;

    final current = _packages[idx];
    final newStatus = !current.isActive;
    // Si se activa y tenía 0 stock, darle al menos 1
    final newStock = (newStatus && current.remainingStock == 0) ? 1 : current.remainingStock;

    final updated = current.copyWith(
      isActive: newStatus,
      remainingStock: newStock,
    );

    _packages[idx] = updated;
    notifyListeners();

    if (SupabaseService.instance.isReady && !_isOfflineMode) {
      await SupabaseService.instance.togglePackageActive(packageId, newStatus);
      if (newStock != current.remainingStock) {
        await SupabaseService.instance.updatePackageStock(packageId, newStock);
      }
    }
  }

  /// Editar paquete existente (Comercio)
  Future<void> editPackage(FoodPackage updatedPkg) async {
    final idx = _packages.indexWhere((p) => p.id == updatedPkg.id);
    if (idx != -1) {
      _packages[idx] = updatedPkg;
      notifyListeners();
    }

    if (SupabaseService.instance.isReady && !_isOfflineMode) {
      await SupabaseService.instance.updatePackage(updatedPkg);
    }
  }

  /// Eliminar paquete (Comercio)
  Future<void> deletePackage(String packageId) async {
    _packages.removeWhere((p) => p.id == packageId);
    notifyListeners();

    if (SupabaseService.instance.isReady && !_isOfflineMode) {
      await SupabaseService.instance.deletePackage(packageId);
    }
  }

  /// Canjear y validar entrega mediante escáner QR en mostrador (Supabase + fallback)
  Future<RedeemResult> redeemQrToken(String token) async {
    // 1. Intentar validar directamente contra Supabase
    if (SupabaseService.instance.isReady && !_isOfflineMode) {
      final remoteResult = await SupabaseService.instance.redeemVoucher(token);
      if (remoteResult.isSuccess || remoteResult.isAlreadyRedeemed) {
        final localIdx = _reservations.indexWhere(
          (r) => r.qrToken == token || r.id == token,
        );
        if (localIdx != -1) {
          _reservations[localIdx] = _reservations[localIdx].copyWith(
            status: ReservationStatus.redeemed,
          );
        }
        notifyListeners();
        return remoteResult;
      }
    }

    // 2. Fallback de verificación local en memoria/caché
    final index = _reservations.indexWhere(
      (r) => r.qrToken == token || r.id == token,
    );

    if (index != -1) {
      final res = _reservations[index];
      if (res.status == ReservationStatus.reserved) {
        _reservations[index] = res.copyWith(status: ReservationStatus.redeemed);
        if (SupabaseService.instance.isReady) {
          SupabaseService.instance.updateReservationStatus(token, ReservationStatus.redeemed);
        }
        notifyListeners();
        return RedeemResult(
          status: RedeemStatus.success,
          message: '¡Entrega validada y canjeada con éxito en mostrador!',
          token: token,
          packageTitle: res.packageTitle,
          storeName: res.storeName,
          amountPaid: res.amountPaid,
          redeemedAt: DateTime.now(),
        );
      } else if (res.status == ReservationStatus.redeemed) {
        return RedeemResult(
          status: RedeemStatus.alreadyRedeemed,
          message: 'Este código QR ya fue canjeado con anterioridad.',
          token: token,
          packageTitle: res.packageTitle,
          storeName: res.storeName,
          amountPaid: res.amountPaid,
        );
      }
    }

    return RedeemResult(
      status: RedeemStatus.notFound,
      message: 'Código no encontrado o no pertenece a SaveBite: $token',
      token: token,
    );
  }
}
