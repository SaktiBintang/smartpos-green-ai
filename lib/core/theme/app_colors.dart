import 'package:flutter/material.dart';

/// Design tokens for colors based on the SmartPOS Green AI visual system.
class AppColors {
  const AppColors._();

  // Brand Greens
  static const Color primary = Color(0xFF166534); // Forest Green
  static const Color primaryLight = Color(0xFF16A34A); // Vibrant Eco Green
  static const Color primaryAccent = Color(0xFF22C55E); // Emerald Green
  static const Color ecoSurface = Color(0xFFF0FDF4); // Eco badge tint
  static const Color ecoBorder = Color(0x3316A34A); // Subtle green border

  // Neutral Background & Surfaces
  static const Color background = Color(0xFFF8FAFC);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color surfaceMuted = Color(0xFFF1F5F9);

  // Typography
  static const Color textPrimary = Color(0xFF111827); // Dark Slate / Black
  static const Color textSecondary = Color(0xFF374151); // Slate Grey
  static const Color textMuted = Color(0xFF9CA3AF); // Muted Grey
  static const Color textInverse = Color(0xFFFFFFFF);

  // Borders & Dividers
  static const Color border = Color(0xFFE5E7EB);
  static const Color borderSubtle = Color(0x1A000000);

  // Feedback & State
  static const Color error = Color(0xFFDC2626);
  static const Color errorSurface = Color(0xFFFEF2F2);
  static const Color warning = Color(0xFFF59E0B);
  static const Color warningSurface = Color(0xFFFFFBEB);
  static const Color success = Color(0xFF16A34A);
  static const Color info = Color(0xFF0284C7);
}
