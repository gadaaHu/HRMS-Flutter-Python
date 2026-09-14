import 'package:employee_attendance_flutter/app/data/service/controller/id_card_controller.dart';
import 'package:get/get.dart';

class IDCARDBinding extends Bindings{
  @override
  void dependencies() {
    Get.lazyPut<IDCARDController>(() => IDCARDController());
  }
}