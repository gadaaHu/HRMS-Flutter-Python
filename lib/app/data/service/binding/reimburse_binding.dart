import 'package:employee_attendance_flutter/app/data/service/controller/reimburse_controller.dart';
import 'package:get/get.dart';

class ReimburseBinding extends Bindings{
  @override
  void dependencies() {
    Get.lazyPut<ReimburseController>(() => ReimburseController());
  }
}