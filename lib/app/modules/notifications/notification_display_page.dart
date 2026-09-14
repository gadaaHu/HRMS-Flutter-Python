import 'package:employee_attendance_flutter/app/core/colors/colors.dart';
import 'package:employee_attendance_flutter/app/data/service/controller/notification_controller.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../../core/utils/dimensions.dart';
import '../../widgets/no_data_widget.dart';

class NotificationDisplayPage extends StatelessWidget {
  const NotificationDisplayPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        iconTheme: const IconThemeData(
          color: Colors.black, //change your color here
        ),
        centerTitle: true,
        title: Padding(
          padding: const EdgeInsets.only(top: 10.0),
          child: Text("NOTIFICATIONS",
              textAlign: TextAlign.center,
              style: TextStyle(
                color: AppColors.kMainBlackColor,
                fontWeight: FontWeight.bold,
                fontSize: Dimensions.font18,
              )),
        ),
        elevation: 0,
        backgroundColor: AppColors.kTransparentColor,
      ),
      body: GetBuilder<NotificationController>(
          init: NotificationController(),
          builder: (controller) {
            return const Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  NoDataWidget(),
                ]);
          }),
    );
  }
}
