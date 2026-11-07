import 'package:flutter/foundation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../core/constants/supabase_constants.dart';
import '../../domain/entities/food_package.dart';
import '../../domain/entities/reservation.dart';
import '../../domain/entities/user_profile.dart';
import '../../domain/entities/redeem_result.dart';

class SupabaseService {
  static final SupabaseService instance = SupabaseService._internal();
  SupabaseService._internal();

  bool _initialized = false;
  bool get isReady => _initialized && SupabaseConstants.isConfigured;

  SupabaseClient get client => Supabase.instance.client;

  Future<void> initialize() async {
    if (!SupabaseConstants.isConfigured) {
      debugPrint('[SupabaseService] Claves no configuradas. Operando en modo local (Mock).');
      return;
    }

    try {
      await Supabase.initialize(
        url: SupabaseConstants.supabaseUrl,
        anonKey: SupabaseConstants.supabaseAnonKey,
      );
      _initialized = true;
      debugPrint('[SupabaseService] Conectado exitosamente a Supabase!');
    } catch (e) {
      debugPrint('[SupabaseService] Error inicializando Supabase: $e');
    }
  }

  // ==========================================
  // AUTENTICACIÓN
  // ==========================================
  Future<UserProfile?> signIn({required String email, required String password}) async {
    if (!isReady) return null;
    try {
      final response = await client.auth.signInWithPassword(email: email, password: password);
      final user = response.user;
      if (user == null) return null;

      final profileData = await client.from('profiles').select().eq('id', user.id).maybeSingle();
      if (profileData != null) {
        return UserProfile(
          id: user.id,
          name: profileData['name'] ?? 'Usuario',
          email: user.email ?? email,
          role: profileData['role'] == 'merchant' ? UserRole.merchant : UserRole.consumer,
          storeId: profileData['store_id'],
          storeName: profileData['store_name'],
          avatarInitials: profileData['avatar_initials'] ?? 'SB',
        );
      }
      return null;
    } catch (e) {
      debugPrint('[SupabaseService] Error en signIn: $e');
      rethrow;
    }
  }

  Future<UserProfile?> signUp({
    required String email,
    required String password,
    required String name,
    required UserRole role,
    String? storeName,
  }) async {
    if (!isReady) return null;
    try {
      final response = await client.auth.signUp(
        email: email,
        password: password,
        data: {'name': name, 'role': role == UserRole.merchant ? 'merchant' : 'consumer'},
      );
      final user = response.user;
      if (user == null) return null;

      await client.from('profiles').upsert({
        'id': user.id,
        'name': name,
        'email': email,
        'role': role == UserRole.merchant ? 'merchant' : 'consumer',
        'store_name': storeName,
        'avatar_initials': name.trim().split(' ').map((p) => p.isNotEmpty ? p[0] : '').take(2).join().toUpperCase(),
      });

      return UserProfile(
        id: user.id,
        name: name,
        email: email,
        role: role,
        storeName: storeName,
        avatarInitials: name.trim().split(' ').map((p) => p.isNotEmpty ? p[0] : '').take(2).join().toUpperCase(),
      );
    } catch (e) {
      debugPrint('[SupabaseService] Error en signUp: $e');
      rethrow;
    }
  }

  Future<void> signOut() async {
    if (!isReady) return;
    try {
      await client.auth.signOut();
    } catch (e) {
      debugPrint('[SupabaseService] Error en signOut: $e');
    }
  }

  // ==========================================
  // PAQUETES (STREAM EN TIEMPO REAL)
  // ==========================================
  Stream<List<FoodPackage>> getPackagesStream() {
    if (!isReady) {
      return const Stream.empty();
    }

    return client
        .from('food_packages')
        .stream(primaryKey: ['id'])
        .order('created_at', ascending: false)
        .map((rows) {
          return rows.map((row) {
            return FoodPackage(
              id: row['id'] as String,
              storeId: (row['store_id'] ?? '').toString(),
              storeName: (row['store_name'] ?? 'Comercio Aliado') as String,
              title: (row['title'] ?? 'Paquete Sorpresa') as String,
              description: (row['description'] ?? '') as String,
              category: (row['category'] ?? 'General') as String,
              originalPrice: (row['original_price'] as num?)?.toDouble() ?? 0.0,
              discountedPrice: (row['discounted_price'] as num?)?.toDouble() ?? 0.0,
              initialStock: (row['initial_stock'] as num?)?.toInt() ?? 1,
              remainingStock: (row['remaining_stock'] as num?)?.toInt() ?? 1,
              pickupTimeWindow: (row['pickup_time_window'] ?? '19:00 - 20:00') as String,
              estimatedKg: (row['estimated_kg'] as num?)?.toDouble() ?? 1.0,
              co2SavedKg: (row['co2_saved_kg'] as num?)?.toDouble() ?? 2.0,
              categoryEmoji: (row['category_emoji'] ?? '🍱') as String,
            );
          }).toList();
        });
  }

  Future<void> insertPackage(FoodPackage pkg) async {
    if (!isReady) return;
    try {
      await client.from('food_packages').insert({
        'store_id': pkg.storeId,
        'store_name': pkg.storeName,
        'title': pkg.title,
        'description': pkg.description,
        'category': pkg.category,
        'category_emoji': pkg.categoryEmoji,
        'original_price': pkg.originalPrice,
        'discounted_price': pkg.discountedPrice,
        'initial_stock': pkg.initialStock,
        'remaining_stock': pkg.remainingStock,
        'pickup_time_window': pkg.pickupTimeWindow,
        'estimated_kg': pkg.estimatedKg,
        'co2_saved_kg': pkg.co2SavedKg,
      });
    } catch (e) {
      debugPrint('[SupabaseService] Error creando paquete en Supabase: $e');
      rethrow;
    }
  }

  // ==========================================
  // CANJE Y RESERVAS EN TIEMPO REAL
  // ==========================================
  Future<Reservation?> createReservation({
    required FoodPackage package,
    String? userId,
  }) async {
    if (!isReady) return null;

    final reservationId = 'RES-${DateTime.now().millisecondsSinceEpoch.toString().substring(7)}-SB';
    final qrToken = 'SB-TOKEN-${package.id.substring(0, package.id.length > 8 ? 8 : package.id.length)}-${DateTime.now().millisecondsSinceEpoch}';

    try {
      // 1. Descontar stock atómicamente en la base de datos
      if (package.remainingStock > 0) {
        await client.from('food_packages').update({
          'remaining_stock': package.remainingStock - 1,
        }).eq('id', package.id);
      }

      // 2. Insertar reserva en la tabla de Supabase
      final insertData = <String, dynamic>{
        'package_id': package.id,
        'package_title': package.title,
        'store_name': package.storeName,
        'pickup_window': package.pickupTimeWindow,
        'amount_paid': package.discountedPrice,
        'original_price': package.originalPrice,
        'qr_token': qrToken,
        'status': 'reserved',
        'co2_saved_kg': package.co2SavedKg,
        'food_rescued_kg': package.estimatedKg,
      };

      // Si el userId es un UUID válido de Supabase, lo incluimos
      if (userId != null && userId.contains('-') && userId.length >= 32) {
        insertData['user_id'] = userId;
      }

      final resList = await client.from('reservations').insert(insertData).select();
      final row = resList.isNotEmpty ? resList.first : null;
      final actualId = row != null && row['id'] != null ? row['id'].toString() : reservationId;

      return Reservation(
        id: actualId,
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
    } catch (e) {
      debugPrint('[SupabaseService] Error creando reserva en Supabase: $e');
      return null;
    }
  }

  Future<RedeemResult> redeemVoucher(String token) async {
    if (!isReady) {
      return RedeemResult(
        status: RedeemStatus.networkError,
        message: 'Sin conexión a Supabase. Se utilizará verificación local.',
        token: token,
      );
    }

    try {
      // Buscar la reserva por qr_token o por id
      final response = await client
          .from('reservations')
          .select()
          .or('qr_token.eq.$token,id.eq.$token')
          .maybeSingle();

      if (response == null) {
        return RedeemResult(
          status: RedeemStatus.notFound,
          message: 'El código escaneado no corresponde a ninguna reserva de SaveBite.',
          token: token,
        );
      }

      final statusStr = response['status'] as String? ?? 'reserved';
      final packageTitle = response['package_title'] as String? ?? 'Paquete Sorpresa';
      final storeName = response['store_name'] as String? ?? 'Comercio Aliado';
      final amountPaid = (response['amount_paid'] as num?)?.toDouble() ?? 0.0;

      if (statusStr == 'redeemed') {
        final redeemedAtStr = response['redeemed_at'] as String?;
        final redeemedDate = redeemedAtStr != null ? DateTime.tryParse(redeemedAtStr) : null;
        return RedeemResult(
          status: RedeemStatus.alreadyRedeemed,
          message: 'Este código QR ya fue canjeado con anterioridad.',
          token: token,
          packageTitle: packageTitle,
          storeName: storeName,
          amountPaid: amountPaid,
          redeemedAt: redeemedDate,
        );
      }

      // Marcar como canjeado en tiempo real
      final now = DateTime.now();
      await client.from('reservations').update({
        'status': 'redeemed',
        'redeemed_at': now.toIso8601String(),
      }).eq('id', response['id']);

      return RedeemResult(
        status: RedeemStatus.success,
        message: '¡Entrega validada y canjeada con éxito en mostrador!',
        token: token,
        packageTitle: packageTitle,
        storeName: storeName,
        amountPaid: amountPaid,
        redeemedAt: now,
      );
    } catch (e) {
      debugPrint('[SupabaseService] Error validando QR: $e');
      return RedeemResult(
        status: RedeemStatus.networkError,
        message: 'Error de comunicación con el servidor: $e',
        token: token,
      );
    }
  }

  Stream<List<Reservation>> getReservationsStream() {
    if (!isReady) return const Stream.empty();

    return client
        .from('reservations')
        .stream(primaryKey: ['id'])
        .order('reserved_at', ascending: false)
        .map((rows) {
          return rows.map((row) {
            final statusStr = row['status'] as String? ?? 'reserved';
            final status = statusStr == 'redeemed'
                ? ReservationStatus.redeemed
                : (statusStr == 'expired' ? ReservationStatus.expired : ReservationStatus.reserved);

            return Reservation(
              id: row['id'].toString(),
              packageId: row['package_id'].toString(),
              packageTitle: (row['package_title'] ?? 'Paquete') as String,
              storeName: (row['store_name'] ?? 'Comercio') as String,
              pickupWindow: (row['pickup_window'] ?? '') as String,
              amountPaid: (row['amount_paid'] as num?)?.toDouble() ?? 0.0,
              originalPrice: (row['original_price'] as num?)?.toDouble() ?? 0.0,
              reservedAt: DateTime.tryParse(row['reserved_at'] as String? ?? '') ?? DateTime.now(),
              qrToken: (row['qr_token'] ?? '') as String,
              status: status,
              co2SavedKg: (row['co2_saved_kg'] as num?)?.toDouble() ?? 0.0,
              foodRescuedKg: (row['food_rescued_kg'] as num?)?.toDouble() ?? 0.0,
              isOfflineCached: true,
            );
          }).toList();
        });
  }

  Future<void> updateReservationStatus(String qrToken, ReservationStatus newStatus) async {
    if (!isReady) return;
    try {
      await client.from('reservations').update({
        'status': newStatus.name,
        if (newStatus == ReservationStatus.redeemed) 'redeemed_at': DateTime.now().toIso8601String(),
      }).eq('qr_token', qrToken);
    } catch (e) {
      debugPrint('[SupabaseService] Error actualizando estado de reserva: $e');
    }
  }
}

