import 'package:flutter/material.dart';

class CommonFunctions {
  void showMessageSnackBar(String msg, BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(msg),
      ),
    );
  }
}
