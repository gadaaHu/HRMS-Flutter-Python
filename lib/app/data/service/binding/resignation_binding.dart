import 'package:employee_attendance_flutter/app/data/service/controller/resignation_controller.dart';
import 'package:get/get.dart';

class ResignationBinding extends Bindings{
  @override
  void dependencies() {
    Get.lazyPut<ResignationController>(() => ResignationController());
  }
}