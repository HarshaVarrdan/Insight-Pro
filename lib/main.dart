import 'package:flutter/material.dart';
import 'package:insigth_pro/pages/homepage.dart';

void main() {
  runApp(MaterialApp(
    title: "Insight Pro",
    theme: ThemeData(
      useMaterial3: true,
      scaffoldBackgroundColor: const Color(0xFFDEDEDE),
      // Define the default brightness and colors.
      colorScheme: ColorScheme.fromSeed(
        seedColor: Colors.green,
        primary: Colors.white,
        secondary: const Color(0xFF0095FF),
        tertiary: const Color(0xFFD9D9D9),
        background: const Color(0xFFDEDEDE),
        // ···
        brightness: Brightness.light,
      ),
      textTheme: const TextTheme(
        titleLarge: TextStyle(
          fontFamily: "DMSans",
          fontWeight: FontWeight.w700,
          fontSize: 30,
          color: Colors.white,
        ),
        bodySmall: TextStyle(
          fontFamily: "DMSans",
          fontWeight: FontWeight.w400,
          fontSize: 12,
          color: Color(0xFF909090),
        ),
      ),
    ),
    home: const HomePage(),
    initialRoute: '/',
    routes: const {
      //'/accountpage': (context) => const (),
      //'/paymentpage': (context) => const (),
      //'/documentspage': (context) => const (),
      //'/policiespage': (context) => const (),
    },
  ));
}
