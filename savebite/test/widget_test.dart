import 'package:flutter_test/flutter_test.dart';
import 'package:savebite/main.dart';

void main() {
  testWidgets('SaveBite app smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const SaveBiteApp());
    expect(find.byType(SaveBiteApp), findsOneWidget);
    // Avanzar el temporizador de la SplashScreen (2.2 segundos)
    await tester.pump(const Duration(seconds: 3));
    await tester.pumpAndSettle();
  });
}
