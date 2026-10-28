import 'package:flutter/material.dart';
import 'core/theme/app_theme.dart';
import 'presentation/screens/splash/splash_screen.dart';
import 'presentation/state/app_state.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const SaveBiteApp());
}

class SaveBiteApp extends StatefulWidget {
  const SaveBiteApp({super.key});

  @override
  State<SaveBiteApp> createState() => _SaveBiteAppState();
}

class _SaveBiteAppState extends State<SaveBiteApp> {
  late final AppState _appState;

  @override
  void initState() {
    super.initState();
    _appState = AppState();
  }

  @override
  void dispose() {
    _appState.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AppStateProvider(
      appState: _appState,
      child: MaterialApp(
        title: 'SaveBite - Cero Merma',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        home: const SplashScreen(),
      ),
    );
  }
}
