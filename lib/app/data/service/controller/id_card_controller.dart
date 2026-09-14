
import 'package:employee_attendance_flutter/app/core/utils/app_utils.dart';
import 'package:employee_attendance_flutter/app/modules/idcard/id_card_arguments.dart';
import 'package:get/get.dart';

import '../../../core/utils/dialog_helper.dart';

class IDCARDController extends SuperController {
  static IDCARDController get to => Get.find();



  final idCardDetails = Rxn<IDCARDArguments>();
/*
  final leaveUsed = 0.obs;
  final leaveDetails = Rxn<Leave>();
*/





  @override
  void onDetached() {
    AppUtils.printMessage('DetachInvoked');
  }

  @override
  void onInactive() {
    AppUtils.printMessage('InactiveInvoked');
  }

  @override
  void onPaused() {
    AppUtils.printMessage('PauseInvoked');
  }

  @override
  void onResumed() {
    AppUtils.printMessage('ResumeInvoked');
  }


  void closeScreen() {
    DialogHelper.dismissLoader();
    Get.back();
  }

  void setIDCard(IDCARDArguments args){
    idCardDetails(args);
    update();
  }

  @override
  void onHidden() {
    // TODO: implement onHidden
  }

}
