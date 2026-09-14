import 'package:employee_attendance_flutter/app/data/service/controller/regularization_controller.dart';
import 'package:get/get.dart';

class RegularizationBinding extends Bindings{
  @override
  void dependencies() {
    Get.lazyPut<RegularizationController>(() => RegularizationController());
  }
}