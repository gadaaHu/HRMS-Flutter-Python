import 'package:flutter/material.dart';

class SmallText extends StatelessWidget {
  final String text;
  final Color? color;
  final double size;
  final double height;
  final TextAlign textAlign;
  final FontWeight fontWeight;
  final int? maxLines;

  SmallText(
      {super.key,
        required this.text,
        this.color = const Color(0xFF080808),
        this.size = 12,
        this.height = 1.2,
        this.textAlign = TextAlign.center,
        this.fontWeight = FontWeight.normal, this.maxLines = 3});

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      softWrap: true,
      style: TextStyle(
          color: color,
          fontSize: size,
          height: height,
          fontWeight: fontWeight,
          fontFamily: 'Montserrat'),
      textAlign: textAlign,
      maxLines: maxLines,
    );
  }
}
