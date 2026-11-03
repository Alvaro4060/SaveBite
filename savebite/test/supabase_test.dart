import 'package:flutter_test/flutter_test.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:savebite/core/constants/supabase_constants.dart';

void main() {
  test('Verificar conexión y lectura de datos desde Supabase', () async {
    final client = SupabaseClient(
      SupabaseConstants.supabaseUrl,
      SupabaseConstants.supabaseAnonKey,
    );

    // Consultar tiendas
    final stores = await client.from('stores').select();
    print(' Tiendas encontradas en Supabase: ${stores.length}');
    for (final s in stores) {
      print('   -> ${s['name']} (${s['category']}) - ${s['address']}');
    }

    // Consultar paquetes sorpresa
    final packages = await client.from('food_packages').select();
    print(' Paquetes sorpresa encontrados en Supabase: ${packages.length}');
    for (final p in packages) {
      print('   -> ${p['title']} en ${p['store_name']} [\$${p['discounted_price']} MXN]');
    }

    expect(stores.isNotEmpty, true);
    expect(packages.isNotEmpty, true);
  });
}

