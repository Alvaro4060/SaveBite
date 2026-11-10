import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:geolocator/geolocator.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/utils/formatters.dart';
import '../../../domain/entities/food_package.dart';
import '../../../domain/entities/store.dart';
import '../../state/app_state.dart';
import '../package_detail/package_detail_screen.dart';

class InteractiveMapView extends StatefulWidget {
  const InteractiveMapView({super.key});

  @override
  State<InteractiveMapView> createState() => _InteractiveMapViewState();
}

typedef SimulatedMapView = InteractiveMapView;

class _InteractiveMapViewState extends State<InteractiveMapView> {
  final MapController _mapController = MapController();
  static const LatLng _salamancaDefaultCenter = LatLng(20.5735, -101.1960);
  LatLng? _currentUserLocation;
  bool _isLocating = false;
  Store? _selectedStore;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final appState = AppStateProvider.of(context);
      if (appState.stores.isNotEmpty) {
        setState(() {
          _selectedStore = appState.stores.first;
        });
      }
      // Obtener ubicación GPS real del teléfono automáticamente
      _fetchRealLocation(moveCamera: true);
    });
  }

  Future<void> _fetchRealLocation({bool moveCamera = false}) async {
    setState(() => _isLocating = true);

    try {
      final serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Por favor activa el GPS / Ubicación en tu teléfono para localizarte exactamente.'),
              duration: Duration(seconds: 3),
            ),
          );
        }
        setState(() => _isLocating = false);
        return;
      }

      var permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Permiso de ubicación denegado.')),
            );
          }
          setState(() => _isLocating = false);
          return;
        }
      }

      if (permission == LocationPermission.deniedForever) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Permiso de ubicación denegado permanentemente. Actívalo en ajustes de la app.')),
          );
        }
        setState(() => _isLocating = false);
        return;
      }

      final position = await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(accuracy: LocationAccuracy.high),
      );

      final realLocation = LatLng(position.latitude, position.longitude);

      if (mounted) {
        setState(() {
          _currentUserLocation = realLocation;
          _isLocating = false;
        });

        if (moveCamera) {
          _mapController.move(realLocation, 16.0);
        }

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            backgroundColor: AppColors.greenDark,
            content: Text('¡Ubicación exacta detectada por GPS!'),
            duration: Duration(seconds: 2),
          ),
        );
      }
    } catch (e) {
      debugPrint('[Map] Error obteniendo GPS: $e');
      if (mounted) {
        setState(() => _isLocating = false);
      }
    }
  }

  void _flyToStore(Store store) {
    setState(() => _selectedStore = store);
    _mapController.move(LatLng(store.latitude, store.longitude), 15.5);
  }

  void _zoomIn() {
    final currentZoom = _mapController.camera.zoom;
    _mapController.move(_mapController.camera.center, currentZoom + 1);
  }

  void _zoomOut() {
    final currentZoom = _mapController.camera.zoom;
    _mapController.move(_mapController.camera.center, currentZoom - 1);
  }

  double _getCalculatedDistance(Store store) {
    if (_currentUserLocation == null) return store.distanceKm;
    final meters = Geolocator.distanceBetween(
      _currentUserLocation!.latitude,
      _currentUserLocation!.longitude,
      store.latitude,
      store.longitude,
    );
    return meters / 1000.0;
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    final stores = appState.stores;

    final userPoint = _currentUserLocation ?? _salamancaDefaultCenter;

    // Paquetes disponibles en la tienda seleccionada
    final selectedStorePackages = _selectedStore == null
        ? <FoodPackage>[]
        : appState.packages.where((p) => p.storeId == _selectedStore!.id || p.storeName == _selectedStore!.name).toList();

    return Stack(
      children: [
        // 1. MAPA INTERACTIVO OPENSTREETMAP
        FlutterMap(
          mapController: _mapController,
          options: MapOptions(
            initialCenter: userPoint,
            initialZoom: 15.0,
            minZoom: 11.0,
            maxZoom: 18.5,
          ),
          children: [
            TileLayer(
              urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
              userAgentPackageName: 'com.example.savebite',
            ),
            MarkerLayer(
              markers: [
                // Marcador de Ubicación del Usuario (GPS Real)
                Marker(
                  point: userPoint,
                  width: 95,
                  height: 56,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
                        decoration: BoxDecoration(
                          color: _currentUserLocation != null ? AppColors.primary : AppColors.secondaryDark,
                          borderRadius: BorderRadius.circular(8),
                          boxShadow: const [
                            BoxShadow(color: Colors.black26, blurRadius: 4, offset: Offset(0, 1)),
                          ],
                        ),
                        child: Text(
                          _currentUserLocation != null ? 'Tu ubicación real' : 'Salamanca Centro',
                          style: const TextStyle(fontSize: 8.5, fontWeight: FontWeight.bold, color: Colors.white),
                        ),
                      ),
                      const SizedBox(height: 2),
                      Container(
                        width: 18,
                        height: 18,
                        decoration: BoxDecoration(
                          color: _currentUserLocation != null ? AppColors.primary : AppColors.secondary,
                          shape: BoxShape.circle,
                          border: Border.all(color: Colors.white, width: 3),
                          boxShadow: const [
                            BoxShadow(color: Colors.black38, blurRadius: 4),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                // Marcadores de Comercios Aliados
                ...stores.map((store) {
                  final isSelected = _selectedStore?.id == store.id;

                  return Marker(
                    point: LatLng(store.latitude, store.longitude),
                    width: isSelected ? 110 : 85,
                    height: isSelected ? 65 : 52,
                    child: GestureDetector(
                      onTap: () => _flyToStore(store),
                      child: AnimatedScale(
                        scale: isSelected ? 1.15 : 1.0,
                        duration: const Duration(milliseconds: 200),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 3),
                              decoration: BoxDecoration(
                                color: isSelected ? AppColors.primary : Colors.white,
                                borderRadius: BorderRadius.circular(10),
                                border: Border.all(
                                  color: isSelected ? Colors.white : AppColors.primary,
                                  width: 1.5,
                                ),
                                boxShadow: const [
                                  BoxShadow(
                                    color: Color.fromRGBO(0, 0, 0, 0.25),
                                    blurRadius: 6,
                                    offset: Offset(0, 2),
                                  ),
                                ],
                              ),
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Text(store.iconEmoji, style: const TextStyle(fontSize: 12)),
                                  const SizedBox(width: 3),
                                  Flexible(
                                    child: Text(
                                      store.name.split(' ').first,
                                      style: TextStyle(
                                        fontSize: 9.5,
                                        fontWeight: FontWeight.w800,
                                        color: isSelected ? Colors.white : AppColors.textPrimary,
                                      ),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            Icon(
                              Icons.location_on,
                              size: isSelected ? 30 : 22,
                              color: isSelected ? AppColors.accent : AppColors.primary,
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                }),
              ],
            ),
          ],
        ),

        // 2. BARRA SUPERIOR FLOTANTE CON SELECTOR DE TIENDAS
        Positioned(
          top: 12,
          left: 12,
          right: 12,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Píldora de Ciudad e indicador GPS
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: const [
                    BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 2)),
                  ],
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      _currentUserLocation != null ? Icons.gps_fixed_rounded : Icons.location_city_rounded,
                      size: 14,
                      color: _currentUserLocation != null ? AppColors.greenDark : AppColors.primary,
                    ),
                    const SizedBox(width: 5),
                    Text(
                      _currentUserLocation != null
                          ? 'GPS Activo • Salamanca, Gto.'
                          : 'Salamanca, Gto. • ${stores.length} comercios',
                      style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 8),

              // Carrusel de Accesos Rápidos por Comercio
              SizedBox(
                height: 38,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: stores.length,
                  itemBuilder: (context, index) {
                    final store = stores[index];
                    final isSelected = _selectedStore?.id == store.id;

                    return Padding(
                      padding: const EdgeInsets.only(right: 8),
                      child: InkWell(
                        onTap: () => _flyToStore(store),
                        borderRadius: BorderRadius.circular(18),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: isSelected ? AppColors.primary : Colors.white,
                            borderRadius: BorderRadius.circular(18),
                            border: Border.all(
                              color: isSelected ? AppColors.primary : AppColors.border,
                            ),
                            boxShadow: const [
                              BoxShadow(color: Colors.black12, blurRadius: 4, offset: Offset(0, 1)),
                            ],
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Text(store.iconEmoji, style: const TextStyle(fontSize: 13)),
                              const SizedBox(width: 5),
                              Text(
                                store.name,
                                style: TextStyle(
                                  fontSize: 11,
                                  fontWeight: FontWeight.bold,
                                  color: isSelected ? Colors.white : AppColors.textPrimary,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        ),

        // 3. CONTROLES DE ZOOM Y CENTRADO FLOTANTES
        Positioned(
          right: 14,
          bottom: _selectedStore != null ? 220 : 30,
          child: Column(
            children: [
              _MapRoundButton(
                icon: _isLocating ? Icons.hourglass_top_rounded : Icons.my_location_rounded,
                tooltip: 'Centrar en mi ubicación GPS exacta',
                onTap: () => _fetchRealLocation(moveCamera: true),
              ),
              const SizedBox(height: 8),
              _MapRoundButton(
                icon: Icons.add,
                tooltip: 'Acercar',
                onTap: _zoomIn,
              ),
              const SizedBox(height: 8),
              _MapRoundButton(
                icon: Icons.remove,
                tooltip: 'Alejar',
                onTap: _zoomOut,
              ),
            ],
          ),
        ),

        // 4. TARJETA FLOTANTE INFERIOR DEL COMERCIO SELECCIONADO
        if (_selectedStore != null)
          Positioned(
            left: 14,
            right: 14,
            bottom: 16,
            child: Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(20),
                boxShadow: const [
                  BoxShadow(
                    color: Color.fromRGBO(0, 0, 0, 0.18),
                    blurRadius: 18,
                    offset: Offset(0, 6),
                  ),
                ],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Fila 1: Icono, Nombre, Dirección y Distancia Real Calculada
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
                      const SizedBox(width: 10),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              _selectedStore!.name,
                              style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                            const SizedBox(height: 2),
                            Row(
                              children: [
                                const Icon(Icons.star_rounded, size: 13, color: Colors.amber),
                                const SizedBox(width: 2),
                                Text(
                                  '${appState.getStoreAverageRating(_selectedStore!.name)} (${appState.getStoreReviewCount(_selectedStore!.name)})',
                                  style: TextStyle(
                                    fontSize: 10.5,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.amber.shade900,
                                  ),
                                ),
                                const SizedBox(width: 5),
                                const Text('•', style: TextStyle(color: Colors.grey, fontSize: 10)),
                                const SizedBox(width: 5),
                                Expanded(
                                  child: Text(
                                    _selectedStore!.address,
                                    style: const TextStyle(fontSize: 10.5, color: AppColors.textSecondary),
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 3),
                        decoration: BoxDecoration(
                          color: AppColors.surfaceMuted,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Icon(Icons.near_me_rounded, size: 12, color: AppColors.primary),
                            const SizedBox(width: 3),
                            Text(
                              Formatters.formatDistance(_getCalculatedDistance(_selectedStore!)),
                              style: const TextStyle(
                                fontSize: 10.5,
                                fontWeight: FontWeight.w800,
                                color: AppColors.primary,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 10),

                  // Fila 2: Paquete Disponible
                  if (selectedStorePackages.isNotEmpty) ...[
                    const Divider(height: 1, color: AppColors.border),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        const Icon(Icons.inventory_2_outlined, size: 16, color: AppColors.accent),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            selectedStorePackages.first.title,
                            style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.w700),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        const SizedBox(width: 6),
                        Text(
                          Formatters.formatCurrency(selectedStorePackages.first.discountedPrice),
                          style: const TextStyle(
                            fontSize: 14,
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
                          elevation: 0,
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                        ),
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              'Ver Paquete y Reservar',
                              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12.5, color: Colors.white),
                            ),
                            SizedBox(width: 6),
                            Icon(Icons.arrow_forward_rounded, size: 15, color: Colors.white),
                          ],
                        ),
                      ),
                    ),
                  ] else ...[
                    const Divider(height: 1, color: AppColors.border),
                    const SizedBox(height: 8),
                    const Row(
                      children: [
                        Icon(Icons.info_outline, size: 15, color: AppColors.textMuted),
                        SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            'Packs de hoy agotados en este establecimiento',
                            style: TextStyle(fontSize: 11.5, color: AppColors.textSecondary),
                          ),
                        ),
                      ],
                    ),
                  ],
                ],
              ),
            ),
          ),
      ],
    );
  }
}

class _MapRoundButton extends StatelessWidget {
  final IconData icon;
  final String tooltip;
  final VoidCallback onTap;

  const _MapRoundButton({
    required this.icon,
    required this.tooltip,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        shape: BoxShape.circle,
        boxShadow: [
          BoxShadow(color: Colors.black26, blurRadius: 6, offset: Offset(0, 2)),
        ],
      ),
      child: IconButton(
        icon: Icon(icon, color: AppColors.primary, size: 20),
        tooltip: tooltip,
        onPressed: onTap,
        constraints: const BoxConstraints(minWidth: 40, minHeight: 40),
        padding: EdgeInsets.zero,
      ),
    );
  }
}
