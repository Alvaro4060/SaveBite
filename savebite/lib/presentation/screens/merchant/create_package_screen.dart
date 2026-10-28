import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_styles.dart';
import '../../../core/utils/formatters.dart';
import '../../state/app_state.dart';
import '../../widgets/custom_button.dart';

class CreatePackageScreen extends StatefulWidget {
  const CreatePackageScreen({super.key});

  @override
  State<CreatePackageScreen> createState() => _CreatePackageScreenState();
}

class _CreatePackageScreenState extends State<CreatePackageScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController(text: 'Pack Sorpresa de Panadería Especial');
  final _descController = TextEditingController(
    text: 'Surtido de pan dulce artesanal, baguettes y donas horneadas el día de hoy.',
  );
  final _originalPriceController = TextEditingController(text: '140');
  final _discountedPriceController = TextEditingController(text: '50');
  final _stockController = TextEditingController(text: '4');
  final _pickupWindowController = TextEditingController(text: '19:45 - 20:45');
  final _kgController = TextEditingController(text: '1.2');

  String _selectedCategory = 'Panaderías';
  String _categoryEmoji = '🥐';

  final List<Map<String, String>> _categories = const [
    {'name': 'Panaderías', 'emoji': '🥐'},
    {'name': 'Cafeterías', 'emoji': '☕'},
    {'name': 'Fruterías', 'emoji': '🍎'},
    {'name': 'Comida Preparada', 'emoji': '🍕'},
  ];

  @override
  void dispose() {
    _titleController.dispose();
    _descController.dispose();
    _originalPriceController.dispose();
    _discountedPriceController.dispose();
    _stockController.dispose();
    _pickupWindowController.dispose();
    _kgController.dispose();
    super.dispose();
  }

  void _onPublish(BuildContext context) {
    final original = double.tryParse(_originalPriceController.text) ?? 100.0;
    final discounted = double.tryParse(_discountedPriceController.text) ?? 40.0;
    final stock = int.tryParse(_stockController.text) ?? 3;
    final kg = double.tryParse(_kgController.text) ?? 1.0;

    final appState = AppStateProvider.of(context);
    appState.publishNewPackage(
      title: _titleController.text.trim(),
      description: _descController.text.trim(),
      category: _selectedCategory,
      originalPrice: original,
      discountedPrice: discounted,
      stock: stock,
      pickupWindow: _pickupWindowController.text.trim(),
      estimatedKg: kg,
      categoryEmoji: _categoryEmoji,
    );

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        backgroundColor: AppColors.greenDark,
        content: Text('¡Paquete sorpresa publicado con éxito en Salamanca!'),
      ),
    );

    // Si viene en pila de navegación, hacer pop
    if (Navigator.of(context).canPop()) {
      Navigator.of(context).pop();
    } else {
      appState.setTabIndex(0); // Regresa a panel
    }
  }

  @override
  Widget build(BuildContext context) {
    final original = double.tryParse(_originalPriceController.text) ?? 100.0;
    final discounted = double.tryParse(_discountedPriceController.text) ?? 40.0;
    final discount = Formatters.calculateDiscount(original, discounted);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Publicar Paquete Sorpresa'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Banner Explicativo ODS 12
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: AppColors.accent.withOpacity(0.08),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: AppColors.accent.withOpacity(0.3)),
                ),
                child: const Row(
                  children: [
                    Icon(Icons.tips_and_updates_outlined, color: AppColors.accentHover, size: 24),
                    SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        'Publica tus excedentes 2 a 3 horas antes del cierre con descuento del 50% al 70% para mitigar merma.',
                        style: TextStyle(fontSize: 12, color: AppColors.accentHover, fontWeight: FontWeight.w600),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 20),

              // Categoría
              const Text('Categoría del Alimento', style: AppStyles.bodyBold),
              const SizedBox(height: 8),
              SizedBox(
                height: 40,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: _categories.length,
                  itemBuilder: (context, index) {
                    final cat = _categories[index];
                    final isSelected = _selectedCategory == cat['name'];
                    return GestureDetector(
                      onTap: () {
                        setState(() {
                          _selectedCategory = cat['name']!;
                          _categoryEmoji = cat['emoji']!;
                        });
                      },
                      child: Container(
                        margin: const EdgeInsets.only(right: 8),
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                        decoration: BoxDecoration(
                          color: isSelected ? AppColors.primary : Colors.white,
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(
                            color: isSelected ? AppColors.primary : AppColors.border,
                          ),
                        ),
                        child: Row(
                          children: [
                            Text(cat['emoji']!, style: const TextStyle(fontSize: 14)),
                            const SizedBox(width: 6),
                            Text(
                              cat['name']!,
                              style: TextStyle(
                                fontSize: 12.5,
                                fontWeight: FontWeight.w700,
                                color: isSelected ? Colors.white : AppColors.textPrimary,
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ),

              const SizedBox(height: 18),

              // Título
              const Text('Nombre del Paquete Sorpresa', style: AppStyles.bodyBold),
              const SizedBox(height: 6),
              TextFormField(
                controller: _titleController,
                decoration: const InputDecoration(
                  hintText: 'Ej. Pack Pan Dulce y Bolillos del Día',
                ),
              ),

              const SizedBox(height: 16),

              // Descripción
              const Text('Descripción del Contenido Tentativo', style: AppStyles.bodyBold),
              const SizedBox(height: 6),
              TextFormField(
                controller: _descController,
                maxLines: 2,
                decoration: const InputDecoration(
                  hintText: 'Describe el tipo de piezas o porciones que contendrá el paquete',
                ),
              ),

              const SizedBox(height: 16),

              // Precios y Descuento
              Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Precio Normal (\$ MXN)', style: AppStyles.bodyBold),
                        const SizedBox(height: 6),
                        TextFormField(
                          controller: _originalPriceController,
                          keyboardType: TextInputType.number,
                          onChanged: (_) => setState(() {}),
                          decoration: const InputDecoration(prefixText: '\$ '),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Precio SaveBite (\$)', style: AppStyles.bodyBold),
                        const SizedBox(height: 6),
                        TextFormField(
                          controller: _discountedPriceController,
                          keyboardType: TextInputType.number,
                          onChanged: (_) => setState(() {}),
                          decoration: const InputDecoration(prefixText: '\$ '),
                        ),
                      ],
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 8),

              // Indicador dinámico de descuento
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.greenDark.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  'Descuento aplicado: $discount% de ahorro para el cliente',
                  style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppColors.greenDark),
                ),
              ),

              const SizedBox(height: 16),

              // Stock y Peso en Kg
              Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Cantidad de Packs', style: AppStyles.bodyBold),
                        const SizedBox(height: 6),
                        TextFormField(
                          controller: _stockController,
                          keyboardType: TextInputType.number,
                          decoration: const InputDecoration(hintText: 'Ej. 4'),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Peso Est. (Kg comida)', style: AppStyles.bodyBold),
                        const SizedBox(height: 6),
                        TextFormField(
                          controller: _kgController,
                          keyboardType: const TextInputType.numberWithOptions(decimal: true),
                          decoration: const InputDecoration(hintText: 'Ej. 1.2'),
                        ),
                      ],
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 16),

              // Ventana de Recogida
              const Text('Horario de Recogida en Mostrador', style: AppStyles.bodyBold),
              const SizedBox(height: 6),
              TextFormField(
                controller: _pickupWindowController,
                decoration: const InputDecoration(
                  prefixIcon: Icon(Icons.access_time_rounded, color: AppColors.accent, size: 20),
                  hintText: 'Ej. 19:30 - 20:30',
                ),
              ),

              const SizedBox(height: 28),

              // Botón Publicar
              CustomButton(
                text: 'Publicar Paquete Ahora',
                icon: Icons.cloud_upload_outlined,
                backgroundColor: AppColors.primary,
                onPressed: () => _onPublish(context),
              ),

              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}
