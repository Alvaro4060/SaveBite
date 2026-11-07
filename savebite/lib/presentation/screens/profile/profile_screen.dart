import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_styles.dart';
import '../../../core/utils/formatters.dart';
import '../../../domain/entities/user_profile.dart';
import '../../state/app_state.dart';
import '../../widgets/custom_button.dart';
import '../auth/login_screen.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  void _showEditNameDialog(BuildContext context, AppState appState) {
    final controller = TextEditingController(text: appState.currentUser.name);

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Editar Nombre', style: AppStyles.heading3),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(
            labelText: 'Nombre Completo',
            prefixIcon: Icon(Icons.person_outline_rounded, color: AppColors.primary),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () {
              final newName = controller.text.trim();
              if (newName.isNotEmpty) {
                appState.updateProfileName(newName);
              }
              Navigator.of(ctx).pop();
            },
            child: const Text('Guardar'),
          ),
        ],
      ),
    );
  }

  void _showPrivacyNotice(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Aviso de Privacidad (LFPDPPP)', style: AppStyles.heading3),
        content: const SingleChildScrollView(
          child: Text(
            'SaveBite cumple estrictamente con la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP) en los Estados Unidos Mexicanos.\n\n'
            'Tus datos de contacto, ubicación en Salamanca y registros de canjes se utilizan exclusivamente para conectar a comensales con comercios aliados en la reducción de merma alimentaria (ODS 12) y no son transferidos a terceros con fines comerciales.',
            style: TextStyle(fontSize: 13, height: 1.4, color: AppColors.textSecondary),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Entendido'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final user = appState.currentUser;
    final isMerchant = user.isMerchant;
    final impact = appState.ecoImpact;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded, color: AppColors.textPrimary, size: 19),
          onPressed: () => Navigator.of(context).pop(),
        ),
        title: const Text(
          'Mi Perfil',
          style: TextStyle(
            color: AppColors.textPrimary,
            fontSize: 17,
            fontWeight: FontWeight.w900,
          ),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
        child: Column(
          children: [
            // TARJETA PRINCIPAL DEL PERFIL
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: isMerchant ? AppColors.accentGradient : AppColors.heroGradient,
                borderRadius: BorderRadius.circular(24),
                boxShadow: const [
                  BoxShadow(
                    color: Color.fromRGBO(15, 76, 129, 0.2),
                    blurRadius: 16,
                    offset: Offset(0, 8),
                  ),
                ],
              ),
              child: Column(
                children: [
                  CircleAvatar(
                    radius: 40,
                    backgroundColor: Colors.white,
                    child: Text(
                      user.avatarInitials,
                      style: TextStyle(
                        fontSize: 26,
                        fontWeight: FontWeight.w900,
                        color: isMerchant ? AppColors.accent : AppColors.primary,
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    user.name,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w900,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    user.email,
                    style: TextStyle(
                      fontSize: 13,
                      color: Colors.white.withOpacity(0.85),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          isMerchant ? Icons.storefront_rounded : Icons.person_rounded,
                          color: Colors.white,
                          size: 15,
                        ),
                        const SizedBox(width: 6),
                        Text(
                          isMerchant ? 'COMERCIO ALIADO' : 'CONSUMIDOR ACTIVO',
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 11,
                            fontWeight: FontWeight.w900,
                            letterSpacing: 0.5,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 18),

            // TARJETA DE RESUMEN DE ACTIVIDAD / IMPACTO
            if (isMerchant)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: AppStyles.cardDecoration,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.storefront_outlined, color: AppColors.accent, size: 22),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            user.storeName ?? 'Mi Comercio',
                            style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            color: AppColors.success.withOpacity(0.12),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: const Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.star_rounded, color: AppColors.accent, size: 14),
                              SizedBox(width: 2),
                              Text(
                                '4.9',
                                style: TextStyle(fontSize: 11.5, fontWeight: FontWeight.bold, color: AppColors.accentHover),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const Divider(height: 20, color: AppColors.border),
                    Row(
                      children: [
                        Expanded(
                          child: _MiniMetric(
                            label: 'Packs Publicados',
                            value: appState.merchantPackages.length.toString(),
                            color: AppColors.primary,
                          ),
                        ),
                        Expanded(
                          child: _MiniMetric(
                            label: 'Entregas Hoy',
                            value: '4',
                            color: AppColors.success,
                          ),
                        ),
                        const Expanded(
                          child: _MiniMetric(
                            label: 'Salamanca, Gto.',
                            value: 'Centro',
                            color: AppColors.accent,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              )
            else
              Container(
                padding: const EdgeInsets.all(16),
                decoration: AppStyles.cardDecoration,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(
                      children: [
                        Icon(Icons.eco_rounded, color: AppColors.greenDark, size: 20),
                        SizedBox(width: 8),
                        Text('Tu Aporte Ecológico ODS 12', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
                      ],
                    ),
                    const Divider(height: 20, color: AppColors.border),
                    Row(
                      children: [
                        Expanded(
                          child: _MiniMetric(
                            label: 'Rescatados',
                            value: '${impact.totalPacksRescued} packs',
                            color: AppColors.primary,
                          ),
                        ),
                        Expanded(
                          child: _MiniMetric(
                            label: 'Ahorro Total',
                            value: Formatters.formatCurrency(impact.totalMoneySavedMxn),
                            color: AppColors.greenDark,
                          ),
                        ),
                        Expanded(
                          child: _MiniMetric(
                            label: 'CO₂ Evitado',
                            value: '${impact.totalCo2AvoidedKg.toStringAsFixed(1)} kg',
                            color: AppColors.accent,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

            const SizedBox(height: 20),

            // SECCIÓN DE CONFIGURACIÓN Y PREFERENCIAS
            const Align(
              alignment: Alignment.centerLeft,
              child: Text('Configuración y Cuenta', style: AppStyles.heading3),
            ),
            const SizedBox(height: 10),

            Container(
              decoration: AppStyles.cardDecoration,
              child: Column(
                children: [
                  _SettingsTile(
                    icon: Icons.person_outline_rounded,
                    title: 'Nombre de Perfil',
                    subtitle: user.name,
                    onTap: () => _showEditNameDialog(context, appState),
                  ),
                  const Divider(height: 1, indent: 54, color: AppColors.border),
                  _SettingsTile(
                    icon: Icons.email_outlined,
                    title: 'Correo Electrónico',
                    subtitle: user.email,
                  ),
                  const Divider(height: 1, indent: 54, color: AppColors.border),
                  _SettingsTile(
                    icon: Icons.location_on_outlined,
                    title: 'Ciudad Base',
                    subtitle: 'Salamanca, Guanajuato (ODS 12)',
                  ),
                  const Divider(height: 1, indent: 54, color: AppColors.border),
                  SwitchListTile(
                    secondary: Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: appState.isOfflineMode
                            ? AppColors.warning.withOpacity(0.12)
                            : AppColors.surfaceMuted,
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Icon(
                        appState.isOfflineMode ? Icons.wifi_off : Icons.wifi,
                        color: appState.isOfflineMode ? AppColors.warning : AppColors.primary,
                        size: 20,
                      ),
                    ),
                    title: const Text('Modo Sin Conexión (Offline)', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
                    subtitle: Text(
                      appState.isOfflineMode
                          ? 'Operando con caché local'
                          : 'Conectado a la nube Supabase',
                      style: const TextStyle(fontSize: 12, color: AppColors.textSecondary),
                    ),
                    value: appState.isOfflineMode,
                    activeThumbColor: AppColors.primary,
                    onChanged: (_) => appState.toggleOfflineMode(),
                  ),
                  const Divider(height: 1, indent: 54, color: AppColors.border),
                  _SettingsTile(
                    icon: Icons.swap_horiz_rounded,
                    title: 'Cambiar a Modo ${isMerchant ? 'Consumidor' : 'Comercio'}',
                    subtitle: 'Alternar vista de prueba instantáneamente',
                    onTap: () => appState.switchRole(isMerchant ? UserRole.consumer : UserRole.merchant),
                  ),
                  const Divider(height: 1, indent: 54, color: AppColors.border),
                  _SettingsTile(
                    icon: Icons.privacy_tip_outlined,
                    title: 'Aviso de Privacidad',
                    subtitle: 'Protección de datos conforme a la LFPDPPP',
                    onTap: () => _showPrivacyNotice(context),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // BOTÓN CERRAR SESIÓN
            CustomButton(
              text: 'Cerrar Sesión',
              icon: Icons.logout_rounded,
              isOutlined: true,
              backgroundColor: AppColors.error,
              onPressed: () {
                Navigator.of(context).pushAndRemoveUntil(
                  MaterialPageRoute(builder: (_) => const LoginScreen()),
                  (route) => false,
                );
              },
            ),

            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}

class _MiniMetric extends StatelessWidget {
  final String label;
  final String value;
  final Color color;

  const _MiniMetric({
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          value,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: TextStyle(
            fontSize: 15,
            fontWeight: FontWeight.w900,
            color: color,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          label,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(fontSize: 11, color: AppColors.textSecondary),
        ),
      ],
    );
  }
}

class _SettingsTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback? onTap;

  const _SettingsTile({
    required this.icon,
    required this.title,
    required this.subtitle,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Container(
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(
          color: AppColors.surfaceMuted,
          borderRadius: BorderRadius.circular(10),
        ),
        child: Icon(icon, color: AppColors.primary, size: 20),
      ),
      title: Text(title, style: const TextStyle(fontSize: 13.5, fontWeight: FontWeight.w600)),
      subtitle: Text(
        subtitle,
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
        style: const TextStyle(fontSize: 11.5, color: AppColors.textSecondary),
      ),
      trailing: onTap != null
          ? const Icon(Icons.chevron_right_rounded, size: 20, color: AppColors.textMuted)
          : null,
      onTap: onTap,
    );
  }
}

