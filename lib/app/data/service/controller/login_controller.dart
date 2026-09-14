import 'dart:convert';

import 'package:employee_attendance_flutter/app/data/model/user_data_model.dart';
import 'package:employee_attendance_flutter/app/data/service/repository/login_repo.dart';
import 'package:employee_attendance_flutter/app/routes/routes.dart';
import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';

import '../../../core/utils/dialog_helper.dart';
import '../../../core/utils/storage_utils.dart';
import '../../api/error_handling.dart';

class LoginController extends GetxController with StateMixin<dynamic>{
  final textFieldEmail = TextEditingController(text: ''); //rdnet0001690
  final textFieldPassword = TextEditingController(text: '');
  final isPasswordVisible = true.obs;


  void onPasswordToggle(){
    isPasswordVisible(!isPasswordVisible.value);
    update();
  }

  void validate(){
    if(textFieldEmail.text.isEmpty){
      ErrorHandling.showToast('Email is required');
    }else if(textFieldPassword.text.isEmpty){
      ErrorHandling.showToast('Password is required');
    }else{
      submit();
    }
  }

  Future<void> submit() async {
    try {
      DialogHelper.showLoading();
      final value = await LoginRepository().login(textFieldEmail.text.trim(), textFieldPassword.text.trim());
      DialogHelper.dismissLoader();

      var js = jsonDecode(value);
      final model = UserDataModel.fromJson(js);

      StorageUtils.instance.setIsLoggedIn(true);
      StorageUtils.instance.setToken(model.data!.token!);
      StorageUtils.instance.setUsername(textFieldEmail.text);

      Get.offAllNamed(Routes.navigationPage);
    } catch (e) {
      DialogHelper.dismissLoader();
      ErrorHandling.handleErrors(e);
    }
  }
  
  @override
  void onClose() {
    textFieldEmail.dispose();
    textFieldPassword.dispose();
    super.onClose();
  }
}