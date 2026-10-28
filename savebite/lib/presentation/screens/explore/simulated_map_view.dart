import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_styles.dart';
import '../../../core/utils/formatters.dart';
import '../../../domain/entities/food_package.dart';
import '../../../domain/entities/store.dart';
import '../../state/app_state.dart';
import '../package_detail/package_detail_screen.dart';

class SimulatedMapView extends StatefulWidget {
  const SimulatedMapView({super.key});

  @override
  State<SimulatedMapView> createState() => _SimulatedMapViewState();
}

class _SimulatedMapViewState extends State<SimulatedMapView> {
  Store? _selectedStore;

  @override
  void initState() {
    super.initState();
    // Iniciar con la primera tienda seleccionada
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final appState = AppStateProvider.of(context);
      if (appState.stores.isNotEmpty) {
        setState(() {
          _selectedStore = appState.stores.first;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final stores = appState.stores;

    // Paquetes de la tienda seleccionada
    final selectedStorePackages = _selectedStore == null
        ? <FoodPackage>[]
        : appState.packages.where((p) => p.storeId == _selectedStore!.id).toList();

    return Stack(
      children: [
        // Mapa simulado vectorial de Salamanca
        Positioned.fill(
          child: Container(
            color: const Color(0xFFE8ECEF),
            child: CustomPaint(
              painter: _SalamancaMapGridPainter(),
            ),
          ),
        ),

        // Pines interactivos de comercios
        ...stores.map((store) {
          final isSelected = _selectedStore?.id == store.id;
          // Coordenadas relativas en pantalla para demo
          final offset = _getStoreScreenCoordinates(store.id);

          return Positioned(
            left: offset.dx,
            top: offset.dy,
            child: GestureDetector(
              onTap: () {
                setState(() {
                  _selectedStore = store;
                });
              },
              child: AnimatedScale(
                scale: isSelected ? 1.25 : 1.0,
                duration: const Duration(milliseconds: 250),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: isSelected ? AppColors.primary : Colors.white,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                          color: isSelected ? Colors.white : AppColors.primary,
                          width: 1.5,
                        ),
                        boxShadow: const [
                          BoxShadow(
                            color: Color.fromRGBO(0, 0, 0, 0.2),
                            blurRadius: 6,
                            offset: Offset(0, 3),
                          ),
                        ],
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(store.iconEmoji, style: const TextStyle(fontSize: 12)),
                          const SizedBox(width: 4),
                          Text(
                            store.name.split(' ').first,
                            style: TextStyle(
                              fontSize: 10,
                              fontWeight: FontWeight.w800,
                              color: isSelected ? Colors.white : AppColors.textPrimary,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Icon(
                      Icons.location_on,
                      size: isSelected ? 34 : 28,
                      color: isSelected ? AppColors.accent : AppColors.primary,
                    ),
                  ],
                ),
              ),
            ),
          );
        }),

        // Pin de Ubicación Actual del Usuario (Salamanca Centro)
        Positioned(
          left: 175,
          top: 240,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.secondary,
                  borderRadius: BorderRadius.circular(10),
                  boxShadow: const [
                    BoxShadow(color: Colors.black26, blurRadius: 4, offset: Offset(0, 2)),
                  ],
                ),
                child: const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.person_pin_circle_rounded, size: 13, color: Colors.white),
                    SizedBox(width: 4),
                    Text(
                      'Tu ubicación',
                      style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.white),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.my_location, size: 22, color: AppColors.secondaryDark),
            ],
          ),
        ),

        // Brújula y Controles flotantes de GPS
        Positioned(
          top: 16,
          right: 16,
          child: Column(
            children: [
              _MapControlButton(
                icon: Icons.my_location_rounded,
                onTap: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Centrado en tu ubicación actual'),
                      duration: Duration(seconds: 1),
                    ),
                  );
                },
              ),
              const SizedBox(height: 8),
              _MapControlButton(
                icon: Icons.layers_outlined,
                onTap: () {},
              ),
            ],
          ),
        ),

        // Tarjeta flotante inferior de la tienda seleccionada
        if (_selectedStore != null)
          Positioned(
            left: 16,
            right: 16,
            bottom: 20,
            child: Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(20),
                boxShadow: const [
                  BoxShadow(
                    color: Color.fromRGBO(0, 0, 0, 0.15),
                    blurRadius: 18,
                    offset: Offset(0, 6),
                  ),
                ],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        width: 44,
                        height: 44,
                        decoration: BoxDecoration(
                          color: AppColors.primary.withOpacity(0.08),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        alignment: Alignment.center,
                        child: Text(_selectedStore!.iconEmoji, style: const TextStyle(fontSize: 22)),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              _selectedStore!.name,
                              style: AppStyles.heading3.copyWith(fontSize: 16),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                            const SizedBox(height: 2),
                            Text(
                              _selectedStore!.address,
                              style: AppStyles.caption,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ],
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: AppColors.surfaceMuted,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          Formatters.formatDistance(_selectedStore!.distanceKm),
                          style: const TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: AppColors.primary,
                          ),
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 12),

                  // Si tiene paquetes disponibles
                  if (selectedStorePackages.isNotEmpty) ...[
                    const Divider(height: 1, color: AppColors.border),
                    const SizedBox(height: 10),
                    Row(
                      children: [
                        const Icon(Icons.shopping_bag_outlined, size: 16, color: AppColors.accent),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            selectedStorePackages.first.title,
                            style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold),
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        Text(
                          Formatters.formatCurrency(selectedStorePackages.first.discountedPrice),
                          style: const TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.w900,
                            color: AppColors.greenDark,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: () {
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (_) => PackageDetailScreen(
                                package: selectedStorePackages.first,
                              ),
                            ),
                          );
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primary,
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                        ),
                        child: const Text(
                          'Ver Paquete Sorpresa',
                          style: TextStyle(fontWeight: FontWeight.w700, fontSize: 13, color: Colors.white),
                        ),
                      ),
                    ),
                  ] else ...[
                    const Text(
                      'No hay paquetes sorpresa restantes en este momento.',
                      style: TextStyle(fontSize: 12, color: AppColors.textMuted),
                    ),
                  ],
                ],
              ),
            ),
          ),
      ],
    );
  }

  Offset _getStoreScreenCoordinates(String storeId) {
    switch (storeId) {
      case 'store_1':
        return const Offset(70, 110);
      case 'store_2':
        return const Offset(200, 190);
      case 'store_3':
        return const Offset(50, 310);
      case 'store_4':
        return const Offset(240, 100);
      case 'store_5':
        return const Offset(250, 320);
      default:
        return const Offset(150, 200);
    }
  }
}

class _MapControlButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback onTap;

  const _MapControlButton({required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        shape: BoxShape.circle,
        boxShadow: [
          BoxShadow(color: Colors.black12, blurRadius: 6, offset: Offset(0, 2)),
        ],
      ),
      child: IconButton(
        icon: Icon(icon, color: AppColors.primary, size: 20),
        onPressed: onTap,
      ),
    );
  }
}

/// Dibuja calles y cuadrícula representativa de Salamanca
class _SalamancaMapGridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final roadPaint = Paint()
      ..color = Colors.white
      ..strokeWidth = 14
      ..style = PaintingStyle.stroke;

    final secondaryRoadPaint = Paint()
      ..color = const Color(0xFFDFE5EB)
      ..strokeWidth = 7
      ..style = PaintingStyle.stroke;

    final riverPaint = Paint()
      ..color = const Color(0xFFC7E2FE)
      ..strokeWidth = 20
      ..style = PaintingStyle.stroke;

    // Río Lerma pasando por Salamanca
    final riverPath = Path()
      ..moveTo(0, size.height * 0.75)
      ..cubicTo(
        size.width * 0.3,
        size.height * 0.8,
        size.width * 0.7,
        size.height * 0.7,
        size.width,
        size.height * 0.85,
      );
    canvas.drawPath(riverPath, riverPaint);

    // Calles principales
    canvas.drawLine(Offset(0, size.height * 0.35), Offset(size.width, size.height * 0.35), roadPaint);
    canvas.drawLine(Offset(0, size.height * 0.55), Offset(size.width, size.height * 0.55), roadPaint);
    canvas.drawLine(Offset(size.width * 0.35, 0), Offset(size.width * 0.35, size.height), roadPaint);
    canvas.drawLine(Offset(size.width * 0.7, 0), Offset(size.width * 0.7, size.height), roadPaint);

    // Calles secundarias diagonales
    canvas.drawLine(Offset(0, 0), Offset(size.width, size.height * 0.5), secondaryRoadPaint);
    canvas.drawLine(Offset(0, size.height * 0.9), Offset(size.width, size.height * 0.2), secondaryRoadPaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
