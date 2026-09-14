
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class DialogHelper {

  static bool _isShowing = false;

  static void showLoading() async {
    // Guard against multiple concurrent loading dialogs
    if (_isShowing) return;
    _isShowing = true;
    Get.closeAllSnackbars();
    Get.dialog(
      PopScope(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            SizedBox(
              width: 60.0,
              height: 60.0,
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(10.0),
                ),
                child: const Padding(
                  padding: EdgeInsets.all(12.0),
                  child: CircularProgressIndicator(),
                ),
              ),
            )
          ],
        ),
        canPop: false,
      ),
      barrierDismissible: false,
    ).then((_) {
      _isShowing = false;
    });
  }

  static void dismissLoader() {
    // Use null-safe check instead of force-unwrap to avoid "Future already completed"
    if (Get.isDialogOpen == true) {
      _isShowing = false;
      Get.back();
    }
  }

}
