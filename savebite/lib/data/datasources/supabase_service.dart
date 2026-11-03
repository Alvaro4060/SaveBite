import 'package:flutter/foundation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../core/constants/supabase_constants.dart';
import '../../domain/entities/food_package.dart';
import '../../domain/entities/reservation.dart';
import '../../domain/entities/user_profile.dart';

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
  // CANJE Y RESERVAS
  // ==========================================
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

