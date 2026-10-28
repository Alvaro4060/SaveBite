import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_strings.dart';
import '../../../core/constants/app_styles.dart';
import '../../../domain/entities/user_profile.dart';
import '../../state/app_state.dart';
import '../../widgets/custom_button.dart';
import '../main_shell_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  UserRole _selectedRole = UserRole.consumer;
  final _emailController = TextEditingController(text: 'cliente@gmail.com');
  final _passwordController = TextEditingController(text: '••••••••');
  bool _isPasswordVisible = false;

  void _onRoleChanged(UserRole role) {
    setState(() {
      _selectedRole = role;
      if (role == UserRole.consumer) {
        _emailController.text = 'cliente@gmail.com';
      } else {
        _emailController.text = 'panaderia.latradicion@gmail.com';
      }
    });
  }

  void _submitLogin(AppState appState) {
    appState.switchRole(_selectedRole);
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const MainShellScreen()),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Tomamos AppState si está disponible en ancestro o usamos instancia
    final appState = _getAppState(context);

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 10),

              // Cabecera con logo pequeño e insignia UTS
              Row(
                children: [
                  Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(
                      gradient: AppColors.heroGradient,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    alignment: Alignment.center,
                    child: const Icon(Icons.shopping_bag_outlined, color: Colors.white, size: 24),
                  ),
                  const SizedBox(width: 12),
                  const Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        AppStrings.appName,
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.w900,
                          color: AppColors.primary,
                        ),
                      ),
                      Text(
                        'Salamanca, Gto.',
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textSecondary,
                        ),
                      ),
                    ],
                  ),
                ],
              ),

              const SizedBox(height: 28),

              // Título y Subtítulo
              const Text(
                AppStrings.welcomeBack,
                style: AppStyles.heading1,
              ),
              const SizedBox(height: 8),
              const Text(
                AppStrings.welcomeSubtitle,
                style: AppStyles.body,
              ),

              const SizedBox(height: 24),

              // Selector de Rol (Consumidor vs Comercio Aliado)
              const Text(
                AppStrings.selectRole,
                style: AppStyles.bodyBold,
              ),
              const SizedBox(height: 10),

              Row(
                children: [
                  // Botón Consumidor
                  Expanded(
                    child: _RoleCard(
                      title: 'Consumidor',
                      subtitle: 'Comprar packs',
                      icon: Icons.person_outline_rounded,
                      isSelected: _selectedRole == UserRole.consumer,
                      onTap: () => _onRoleChanged(UserRole.consumer),
                    ),
                  ),
                  const SizedBox(width: 12),
                  // Botón Comercio
                  Expanded(
                    child: _RoleCard(
                      title: 'Comercio',
                      subtitle: 'Vender excedentes',
                      icon: Icons.storefront_outlined,
                      isSelected: _selectedRole == UserRole.merchant,
                      onTap: () => _onRoleChanged(UserRole.merchant),
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 24),

              // Input de Correo
              const Text('Correo Electrónico', style: AppStyles.bodyBold),
              const SizedBox(height: 6),
              TextField(
                controller: _emailController,
                decoration: const InputDecoration(
                  prefixIcon: Icon(Icons.email_outlined, color: AppColors.primary, size: 20),
                  hintText: 'correo@ejemplo.com',
                ),
              ),

              const SizedBox(height: 16),

              // Input de Contraseña
              const Text('Contraseña', style: AppStyles.bodyBold),
              const SizedBox(height: 6),
              TextField(
                controller: _passwordController,
                obscureText: !_isPasswordVisible,
                decoration: InputDecoration(
                  prefixIcon: const Icon(Icons.lock_outline, color: AppColors.primary, size: 20),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _isPasswordVisible ? Icons.visibility : Icons.visibility_off,
                      color: AppColors.textMuted,
                      size: 20,
                    ),
                    onPressed: () => setState(() => _isPasswordVisible = !_isPasswordVisible),
                  ),
                ),
              ),

              const SizedBox(height: 24),

              // Botón Principal de Inicio de Sesión
              CustomButton(
                text: _selectedRole == UserRole.consumer
                    ? 'Ingresar como Consumidor'
                    : 'Ingresar como Comercio',
                backgroundColor: AppColors.primary,
                icon: Icons.arrow_forward_rounded,
                onPressed: () => _submitLogin(appState),
              ),

              const SizedBox(height: 16),

              // Accesos Rápidos Demo
              Center(
                child: Text(
                  '— O ingresa con un toque de demostración —',
                  style: AppStyles.caption.copyWith(color: AppColors.textMuted),
                ),
              ),
              const SizedBox(height: 12),

              Row(
                children: [
                  Expanded(
                    child: CustomButton(
                      text: 'Demo Consumidor',
                      isOutlined: true,
                      height: 44,
                      icon: Icons.person_outline,
                      backgroundColor: AppColors.primary,
                      onPressed: () {
                        _onRoleChanged(UserRole.consumer);
                        _submitLogin(appState);
                      },
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: CustomButton(
                      text: 'Demo Comercio',
                      isOutlined: true,
                      height: 44,
                      icon: Icons.storefront_outlined,
                      backgroundColor: AppColors.accent,
                      onPressed: () {
                        _onRoleChanged(UserRole.merchant);
                        _submitLogin(appState);
                      },
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 28),

              // Aviso Informativo ODS 12
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: AppColors.success.withOpacity(0.08),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppColors.success.withOpacity(0.3)),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.eco_rounded, color: AppColors.greenDark, size: 26),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'SaveBite promueve el ODS 12 de la ONU reduciendo el desperdicio de comida preparada en Salamanca.',
                        style: TextStyle(
                          fontSize: 12,
                          color: AppColors.greenDark,
                          fontWeight: FontWeight.w600,
                          height: 1.35,
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  AppState _getAppState(BuildContext context) {
    final state = AppStateProvider.of(context);
    return state;
  }
}

class _RoleCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;
  final bool isSelected;
  final VoidCallback onTap;

  const _RoleCard({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
        decoration: BoxDecoration(
          color: isSelected ? AppColors.primary.withOpacity(0.08) : AppColors.surface,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(
            color: isSelected ? AppColors.primary : AppColors.border,
            width: isSelected ? 2 : 1,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  icon,
                  color: isSelected ? AppColors.primary : AppColors.textSecondary,
                  size: 22,
                ),
                const Spacer(),
                if (isSelected)
                  const Icon(Icons.check_circle_rounded, color: AppColors.primary, size: 18),
              ],
            ),
            const SizedBox(height: 10),
            Text(
              title,
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w800,
                color: isSelected ? AppColors.primary : AppColors.textPrimary,
              ),
            ),
            const SizedBox(height: 2),
            Text(
              subtitle,
              style: TextStyle(
                fontSize: 11,
                color: isSelected ? AppColors.primaryDark : AppColors.textMuted,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
