import 'package:flutter/material.dart';

import '../theme/app_colors.dart';

/// Reusable pill badge highlighting sustainability and eco credentials.
class EcoBadge extends StatelessWidget {
  final String label;
  final IconData icon;

  const EcoBadge({
    super.key,
    this.label = 'Inovasi Digital Berkelanjutan',
    this.icon = Icons.eco_rounded,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: AppColors.ecoSurface,
        borderRadius: BorderRadius.circular(50),
        border: Border.all(color: AppColors.ecoBorder, width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 14, color: AppColors.primary),
          const SizedBox(width: 6),
          Text(
            label,
            style: const TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w600,
              color: AppColors.primary,
              letterSpacing: 0.2,
            ),
          ),
        ],
      ),
    );
  }
}
