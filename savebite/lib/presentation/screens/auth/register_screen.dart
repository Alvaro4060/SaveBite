import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_styles.dart';
import '../../../domain/entities/user_profile.dart';
import '../../state/app_state.dart';
import '../../widgets/custom_button.dart';
import '../main_shell_screen.dart';

class RegisterScreen extends StatefulWidget {
  final UserRole initialRole;

  const RegisterScreen({
    super.key,
    this.initialRole = UserRole.consumer,
  });

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  late UserRole _selectedRole;
  final _formKey = GlobalKey<FormState>();

  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  // Campos específicos de Comercio
  final _storeNameController = TextEditingController();
  final _storeAddressController = TextEditingController();
  String _storeCategory = 'Panadería';

  bool _isPasswordVisible = false;
  bool _isConfirmPasswordVisible = false;
  bool _acceptTerms = true;
  bool _isLoading = false;

  final List<Map<String, String>> _categories = const [
    {'name': 'Panadería', 'emoji': '🥖'},
    {'name': 'Cafetería', 'emoji': '☕'},
    {'name': 'Frutería', 'emoji': '🍎'},
    {'name': 'Restaurante', 'emoji': '🍕'},
  ];

  @override
  void initState() {
    super.initState();
    _selectedRole = widget.initialRole;
  }

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    _storeNameController.dispose();
    _storeAddressController.dispose();
    super.dispose();
  }

  Future<void> _submitRegister(AppState appState) async {
    if (!_formKey.currentState!.validate()) return;

    if (!_acceptTerms) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          backgroundColor: AppColors.warning,
          content: Text('Debes aceptar los Términos y el Aviso de Privacidad.'),
        ),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final success = await appState.signUp(
        name: _nameController.text.trim(),
        email: _emailController.text.trim(),
        password: _passwordController.text,
        role: _selectedRole,
        storeName: _selectedRole == UserRole.merchant ? _storeNameController.text.trim() : null,
        storeCategory: _selectedRole == UserRole.merchant ? _storeCategory : null,
        storeAddress: _selectedRole == UserRole.merchant ? _storeAddressController.text.trim() : null,
      );

      if (!mounted) return;
      setState(() => _isLoading = false);

      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppColors.success,
            content: Text(
              _selectedRole == UserRole.merchant
                  ? '¡Comercio registrado con éxito! Bienvenido a SaveBite.'
                  : '¡Cuenta creada con éxito! Bienvenido a SaveBite.',
            ),
          ),
        );

        Navigator.of(context).pushAndRemoveUntil(
          MaterialPageRoute(builder: (_) => const MainShellScreen()),
          (route) => false,
        );
      }
    } catch (e) {
      if (!mounted) return;
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: AppColors.error,
          content: Text('No fue posible completar el registro: $e'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final isMerchant = _selectedRole == UserRole.merchant;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Registro de Usuario'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Encabezado
                Text(
                  isMerchant ? 'Registra tu Comercio Aliado' : 'Crea tu Cuenta de Consumidor',
                  style: AppStyles.heading1.copyWith(fontSize: 24),
                ),
                const SizedBox(height: 6),
                Text(
                  isMerchant
                      ? 'Monetiza tus excedentes diarios y contribuye al ODS 12 en Salamanca.'
                      : 'Rescata alimentos de calidad con descuentos de hasta el 70% en Salamanca.',
                  style: AppStyles.body,
                ),

                const SizedBox(height: 20),

                // Selector de Rol (Consumidor / Comercio)
                const Text(
                  'Tipo de cuenta a registrar:',
                  style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
                ),
                const SizedBox(height: 10),

                Row(
                  children: [
                    Expanded(
                      child: _RoleTabCard(
                        title: 'Consumidor',
                        subtitle: 'Comprar packs',
                        icon: Icons.person_outline_rounded,
                        isSelected: !isMerchant,
                        onTap: () => setState(() => _selectedRole = UserRole.consumer),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _RoleTabCard(
                        title: 'Comercio',
                        subtitle: 'Vender excedentes',
                        icon: Icons.storefront_outlined,
                        isSelected: isMerchant,
                        onTap: () => setState(() => _selectedRole = UserRole.merchant),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 24),

                // DATOS GENERALES
                Text(
                  isMerchant ? 'Nombre del Responsable' : 'Nombre Completo',
                  style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
                ),
                const SizedBox(height: 8),
                TextFormField(
                  controller: _nameController,
                  decoration: InputDecoration(
                    hintText: isMerchant ? 'Ej. Roberto Gómez' : 'Ej. Juan Pérez González',
                    prefixIcon: const Icon(Icons.person_outline_rounded, color: AppColors.primary, size: 20),
                  ),
                  validator: (val) {
                    if (val == null || val.trim().isEmpty) return 'Por favor ingresa tu nombre';
                    return null;
                  },
                ),

                // SECCIÓN ESPECÍFICA SI ES COMERCIO
                if (isMerchant) ...[
                  const SizedBox(height: 18),
                  const Text(
                    'Nombre del Negocio o Establecimiento',
                    style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
                  ),
                  const SizedBox(height: 8),
                  TextFormField(
                    controller: _storeNameController,
                    decoration: const InputDecoration(
                      hintText: 'Ej. Panadería San Juan, Café Central...',
                      prefixIcon: Icon(Icons.storefront_rounded, color: AppColors.accent, size: 20),
                    ),
                    validator: (val) {
                      if (val == null || val.trim().isEmpty) return 'Ingresa el nombre del comercio';
                      return null;
                    },
                  ),

                  const SizedBox(height: 18),
                  const Text(
                    'Giro del Comercio en Salamanca',
                    style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
                  ),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: _categories.map((cat) {
                      final isSelected = _storeCategory == cat['name'];
                      return ChoiceChip(
                        avatar: Text(cat['emoji']!, style: const TextStyle(fontSize: 14)),
                        label: Text(
                          cat['name']!,
                          style: TextStyle(
                            fontSize: 12.5,
                            fontWeight: isSelected ? FontWeight.w800 : FontWeight.w500,
                            color: isSelected ? Colors.white : AppColors.textPrimary,
                          ),
                        ),
                        selected: isSelected,
                        selectedColor: AppColors.accent,
                        backgroundColor: AppColors.surface,
                        onSelected: (selected) {
                          if (selected) setState(() => _storeCategory = cat['name']!);
                        },
                      );
                    }).toList(),
                  ),

                  const SizedBox(height: 18),
                  const Text(
                    'Dirección Física en Salamanca',
                    style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
                  ),
                  const SizedBox(height: 8),
                  TextFormField(
                    controller: _storeAddressController,
                    decoration: const InputDecoration(
                      hintText: 'Ej. Calle Morelos 205, Zona Centro',
                      prefixIcon: Icon(Icons.location_on_outlined, color: AppColors.accent, size: 20),
                    ),
                    validator: (val) {
                      if (val == null || val.trim().isEmpty) return 'Ingresa la dirección de tu local';
                      return null;
                    },
                  ),
                ],

                const SizedBox(height: 18),

                // CORREO ELECTRÓNICO
                const Text(
                  'Correo Electrónico',
                  style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
                ),
                const SizedBox(height: 8),
                TextFormField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(
                    hintText: 'correo@ejemplo.com',
                    prefixIcon: Icon(Icons.email_outlined, color: AppColors.primary, size: 20),
                  ),
                  validator: (val) {
                    if (val == null || val.trim().isEmpty) return 'Ingresa tu correo';
                    if (!val.contains('@') || !val.contains('.')) return 'Ingresa un correo válido';
                    return null;
                  },
                ),

                const SizedBox(height: 18),

                // CONTRASEÑA
                const Text(
                  'Contraseña',
                  style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
                ),
                const SizedBox(height: 8),
                TextFormField(
                  controller: _passwordController,
                  obscureText: !_isPasswordVisible,
                  decoration: InputDecoration(
                    hintText: 'Mínimo 6 caracteres',
                    prefixIcon: const Icon(Icons.lock_outline_rounded, color: AppColors.primary, size: 20),
                    suffixIcon: IconButton(
                      icon: Icon(
                        _isPasswordVisible ? Icons.visibility : Icons.visibility_off,
                        color: AppColors.textMuted,
                        size: 20,
                      ),
                      onPressed: () => setState(() => _isPasswordVisible = !_isPasswordVisible),
                    ),
                  ),
                  validator: (val) {
                    if (val == null || val.isEmpty) return 'Ingresa una contraseña';
                    if (val.length < 6) return 'La contraseña debe tener al menos 6 caracteres';
                    return null;
                  },
                ),

                const SizedBox(height: 18),

                // CONFIRMAR CONTRASEÑA
                const Text(
                  'Confirmar Contraseña',
                  style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
                ),
                const SizedBox(height: 8),
                TextFormField(
                  controller: _confirmPasswordController,
                  obscureText: !_isConfirmPasswordVisible,
                  decoration: InputDecoration(
                    hintText: 'Repite tu contraseña',
                    prefixIcon: const Icon(Icons.lock_reset_rounded, color: AppColors.primary, size: 20),
                    suffixIcon: IconButton(
                      icon: Icon(
                        _isConfirmPasswordVisible ? Icons.visibility : Icons.visibility_off,
                        color: AppColors.textMuted,
                        size: 20,
                      ),
                      onPressed: () => setState(() => _isConfirmPasswordVisible = !_isConfirmPasswordVisible),
                    ),
                  ),
                  validator: (val) {
                    if (val != _passwordController.text) return 'Las contraseñas no coinciden';
                    return null;
                  },
                ),

                const SizedBox(height: 16),

                // Aceptación de Términos (LFPDPPP)
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Checkbox(
                      value: _acceptTerms,
                      activeColor: AppColors.primary,
                      onChanged: (val) => setState(() => _acceptTerms = val ?? false),
                    ),
                    const Expanded(
                      child: Text(
                        'Acepto los Términos de Servicio y el Aviso de Privacidad (LFPDPPP) de SaveBite.',
                        style: TextStyle(fontSize: 12, color: AppColors.textSecondary),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 20),

                // Botón de Registro
                CustomButton(
                  text: _isLoading
                      ? 'Registrando cuenta...'
                      : (isMerchant ? 'Registrar mi Comercio Aliado' : 'Crear Cuenta de Consumidor'),
                  backgroundColor: isMerchant ? AppColors.accent : AppColors.primary,
                  icon: isMerchant ? Icons.storefront_rounded : Icons.person_add_alt_1_rounded,
                  onPressed: _isLoading ? null : () => _submitRegister(appState),
                ),

                const SizedBox(height: 20),

                // Enlace a Inicio de Sesión
                Center(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        '¿Ya tienes una cuenta? ',
                        style: TextStyle(fontSize: 13, color: AppColors.textSecondary),
                      ),
                      GestureDetector(
                        onTap: () => Navigator.of(context).pop(),
                        child: const Text(
                          'Inicia Sesión',
                          style: TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.bold,
                            color: AppColors.primary,
                            decoration: TextDecoration.underline,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 24),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _RoleTabCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;
  final bool isSelected;
  final VoidCallback onTap;

  const _RoleTabCard({
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
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
        decoration: BoxDecoration(
          color: isSelected ? AppColors.primary.withOpacity(0.08) : AppColors.surface,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(
            color: isSelected ? AppColors.primary : AppColors.border,
            width: isSelected ? 2 : 1,
          ),
        ),
        child: Row(
          children: [
            Icon(
              icon,
              color: isSelected ? AppColors.primary : AppColors.textSecondary,
              size: 20,
            ),
            const SizedBox(width: 8),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w800,
                      color: isSelected ? AppColors.primary : AppColors.textPrimary,
                    ),
                  ),
                  Text(
                    subtitle,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(fontSize: 10.5, color: AppColors.textMuted),
                  ),
                ],
              ),
            ),
            if (isSelected)
              const Icon(Icons.check_circle_rounded, color: AppColors.primary, size: 16),
          ],
        ),
      ),
    );
  }
}

