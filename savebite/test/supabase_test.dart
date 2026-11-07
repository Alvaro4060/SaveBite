import 'package:flutter_test/flutter_test.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:savebite/core/constants/supabase_constants.dart';

void main() {
  test('Verificar lectura de paquetes y tiendas en Supabase', () async {
    final client = SupabaseClient(
      SupabaseConstants.supabaseUrl,
      SupabaseConstants.supabaseAnonKey,
    );

    // 1. Consultar tiendas
    final stores = await client.from('stores').select();
    print('🏪 Tiendas en Supabase: ${stores.length}');
    expect(stores.isNotEmpty, true);

    // 2. Consultar paquetes
    final packages = await client.from('food_packages').select();
    print('📦 Paquetes en Supabase: ${packages.length}');
    expect(packages.isNotEmpty, true);

    // 3. Consultar reservas existentes
    final reservations = await client.from('reservations').select();
    print('🎫 Reservas en Supabase: ${reservations.length}');
  });
}



