import 'package:flutter/material.dart';

import '../core/utils/dimensions.dart';

class BigText extends StatelessWidget {
  final String text;
  final Color? color;
  final double size;
  final TextOverflow overflow;
  final TextAlign textAlign;
  final int maxLines;

  BigText(
      {super.key,
      required this.text,
      this.color = const Color(0xFF332d2b),
      this.size = 0,
      this.overflow = TextOverflow.ellipsis,
      this.textAlign = TextAlign.center, this.maxLines = 3});

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      overflow: overflow,
      style: TextStyle(
          color: color,
          fontSize: size == 0 ? Dimensions.font20 : size,
          fontWeight: FontWeight.bold,
          fontFamily: 'Montserrat'),
      textAlign: textAlign,
      maxLines: maxLines,
    );
  }
}
