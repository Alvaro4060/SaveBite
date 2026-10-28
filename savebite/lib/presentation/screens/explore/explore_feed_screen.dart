import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_strings.dart';
import '../../../core/constants/app_styles.dart';
import '../../state/app_state.dart';
import '../../widgets/category_chip.dart';
import '../../widgets/package_card.dart';
import '../package_detail/package_detail_screen.dart';
import 'simulated_map_view.dart';

class ExploreFeedScreen extends StatefulWidget {
  const ExploreFeedScreen({super.key});

  @override
  State<ExploreFeedScreen> createState() => _ExploreFeedScreenState();
}

class _ExploreFeedScreenState extends State<ExploreFeedScreen> {
  bool _isMapView = false;
  final TextEditingController _searchController = TextEditingController();

  final List<Map<String, String>> _categories = const [
    {'label': 'Todos', 'emoji': '✨'},
    {'label': 'Panaderías', 'emoji': '🥖'},
    {'label': 'Cafeterías', 'emoji': '☕'},
    {'label': 'Fruterías', 'emoji': '🍎'},
    {'label': 'Comida Preparada', 'emoji': '🍕'},
  ];

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final packages = appState.packages;

    return Column(
      children: [
        // Barra Superior: Buscador y Switch Lista/Mapa
        Container(
          color: AppColors.surface,
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
          child: Column(
            children: [
              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _searchController,
                      onChanged: (val) => appState.setSearchQuery(val),
                      decoration: InputDecoration(
                        hintText: AppStrings.searchHint,
                        hintStyle: const TextStyle(fontSize: 13, color: AppColors.textMuted),
                        prefixIcon: const Icon(Icons.search, size: 20, color: AppColors.primary),
                        suffixIcon: _searchController.text.isNotEmpty
                            ? IconButton(
                                icon: const Icon(Icons.clear, size: 18),
                                onPressed: () {
                                  _searchController.clear();
                                  appState.setSearchQuery('');
                                },
                              )
                            : null,
                        contentPadding: const EdgeInsets.symmetric(vertical: 10),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  // Botón Toggle Mapa / Lista
                  InkWell(
                    onTap: () {
                      setState(() {
                        _isMapView = !_isMapView;
                      });
                    },
                    borderRadius: BorderRadius.circular(12),
                    child: Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: _isMapView ? AppColors.primary : AppColors.surfaceMuted,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: AppColors.border),
                      ),
                      child: Icon(
                        _isMapView ? Icons.format_list_bulleted_rounded : Icons.map_outlined,
                        color: _isMapView ? Colors.white : AppColors.primary,
                        size: 22,
                      ),
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 12),

              // Carrusel de Categorías
              SizedBox(
                height: 38,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: _categories.length,
                  itemBuilder: (context, index) {
                    final cat = _categories[index];
                    final isSelected = appState.selectedCategory == cat['label'];
                    return CategoryChip(
                      label: cat['label']!,
                      emoji: cat['emoji']!,
                      isSelected: isSelected,
                      onTap: () => appState.setCategory(cat['label']!),
                    );
                  },
                ),
              ),
            ],
          ),
        ),

        // Cuerpo: Lista de Paquetes o Mapa GPS Interactivo
        Expanded(
          child: _isMapView
              ? const SimulatedMapView()
              : packages.isEmpty
                  ? Center(
                      child: Padding(
                        padding: const EdgeInsets.all(32),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(Icons.search_off_rounded, size: 54, color: AppColors.textMuted),
                            const SizedBox(height: 14),
                            const Text(
                              'No se encontraron paquetes sorpresa',
                              style: AppStyles.heading3,
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 6),
                            const Text(
                              'Intenta cambiar la categoría o limpiar el término de búsqueda.',
                              style: AppStyles.body,
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 16),
                            TextButton(
                              onPressed: () {
                                _searchController.clear();
                                appState.setCategory('Todos');
                                appState.setSearchQuery('');
                              },
                              child: const Text('Mostrar todos los paquetes'),
                            ),
                          ],
                        ),
                      ),
                    )
                  : ListView.builder(
                      padding: const EdgeInsets.fromLTRB(16, 16, 16, 80),
                      itemCount: packages.length + 1,
                      itemBuilder: (context, index) {
                        if (index == 0) {
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 12),
                            child: Row(
                              children: [
                                Text(
                                  '${packages.length} paquetes sorpresa hoy',
                                  style: const TextStyle(
                                    fontSize: 14,
                                    fontWeight: FontWeight.w700,
                                    color: AppColors.textSecondary,
                                  ),
                                ),
                                const Spacer(),
                                const Row(
                                  children: [
                                    Icon(Icons.bolt, size: 14, color: AppColors.accent),
                                    SizedBox(width: 2),
                                    Text(
                                      'Actualizado en vivo',
                                      style: TextStyle(
                                        fontSize: 11,
                                        fontWeight: FontWeight.w700,
                                        color: AppColors.accent,
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          );
                        }

                        final package = packages[index - 1];
                        return PackageCard(
                          package: package,
                          onTap: () {
                            Navigator.of(context).push(
                              MaterialPageRoute(
                                builder: (_) => PackageDetailScreen(package: package),
                              ),
                            );
                          },
                        );
                      },
                    ),
        ),
      ],
    );
  }
}
