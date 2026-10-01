import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:smartpos_green_ai/main.dart';

void main() {
  testWidgets('App initialization smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const ProviderScope(child: SmartPosApp()));
    await tester.pumpAndSettle();

    // Verify login screen elements are present
    expect(find.text('Masuk ke Akun Anda'), findsOneWidget);
    expect(find.text('Masuk'), findsOneWidget);
  });
}
