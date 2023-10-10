import 'package:flutter/material.dart';
import 'package:mobile_app/router.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Ayush Connect',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        fontFamily: 'Roboto',
        useMaterial3: false,
        colorSchemeSeed: Colors.greenAccent.shade700,
      ),
      routerConfig: router,
    );
  }
}