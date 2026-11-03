class SupabaseConstants {
  static const String supabaseUrl = 'https://qbpfprndtnvtmjxhwgry.supabase.co';
  static const String supabaseAnonKey = 'sb_publishable_Eg70s58ppaFqJHT5M4H03Q_ZnrXm0N_';

  static bool get isConfigured =>
      supabaseUrl.isNotEmpty &&
      supabaseAnonKey.isNotEmpty &&
      !supabaseUrl.contains('TU-PROYECTO');
}
