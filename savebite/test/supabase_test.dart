import 'package:flutter_test/flutter_test.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:savebite/core/constants/supabase_constants.dart';

void main() {
  test('Verificar ciclo completo de reserva y canje en Supabase', () async {
    final client = SupabaseClient(
      SupabaseConstants.supabaseUrl,
      SupabaseConstants.supabaseAnonKey,
    );

    // 1. Consultar paquetes
    final packages = await client.from('food_packages').select();
    print('📦 Paquetes sorpresa encontrados: ${packages.length}');
    expect(packages.isNotEmpty, true);
    final targetPkg = packages.first;
    final String pkgId = targetPkg['id'];
    final int initialStock = targetPkg['remaining_stock'];
    print('   -> Paquete prueba: ${targetPkg['title']} (Stock actual: $initialStock)');

    // 2. Insertar reserva de prueba
    final String token = 'SB-TEST-${DateTime.now().millisecondsSinceEpoch}';
    print('🎫 Creando reserva de prueba con token: $token');
    
    try {
      final insertRes = await client.from('reservations').insert({
        'package_id': pkgId,
        'package_title': targetPkg['title'],
        'store_name': targetPkg['store_name'],
        'pickup_window': targetPkg['pickup_time_window'],
        'amount_paid': targetPkg['discounted_price'],
        'original_price': targetPkg['original_price'],
        'qr_token': token,
        'status': 'reserved',
        'co2_saved_kg': targetPkg['co2_saved_kg'],
        'food_rescued_kg': targetPkg['estimated_kg'],
      }).select();
      print('✅ Reserva creada con éxito: $insertRes');
    } catch (e) {
      print('❌ Error insertando reserva: $e');
    }

    // 3. Decrementar stock
    try {
      await client
          .from('food_packages')
          .update({'remaining_stock': initialStock - 1})
          .eq('id', pkgId);
      print('✅ Stock decrementado en base de datos: ${initialStock - 1}');
    } catch (e) {
      print('❌ Error actualizando stock: $e');
    }

    // 4. Canjear cupón
    try {
      final updateRes = await client
          .from('reservations')
          .update({
            'status': 'redeemed',
            'redeemed_at': DateTime.now().toIso8601String(),
          })
          .eq('qr_token', token)
          .select();
      print('✅ Reserva canjeada exitosamente: $updateRes');
    } catch (e) {
      print('❌ Error canjeando reserva: $e');
    }

    // Restaurar stock para no alterar datos de prueba
    await client
        .from('food_packages')
        .update({'remaining_stock': initialStock})
        .eq('id', pkgId);
    print('🔄 Stock restaurado a su valor original ($initialStock).');
  });
}


