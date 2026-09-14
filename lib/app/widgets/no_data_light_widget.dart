import 'package:flutter/material.dart';

import '../core/colors/colors.dart';

class NoDataLightWidget extends StatelessWidget {
  const NoDataLightWidget({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text(
        "No Data Found",
        style:
            TextStyle(fontWeight: FontWeight.w600, color: AppColors.kTextColor),
      ),
    );
  }
}
