import 'package:employee_attendance_flutter/app/data/service/controller/holiday_controller.dart';
import 'package:get/get.dart';

class HolidayBinding extends Bindings{
  @override
  void dependencies() {
    Get.lazyPut<HolidayController>(() => HolidayController());
  }
}