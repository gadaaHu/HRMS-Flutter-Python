import 'dart:convert';
import 'dart:developer';
import 'dart:io';
import 'dart:math' as mth;
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:image_cropper/image_cropper.dart';
import 'package:intl/intl.dart';

import '../../routes/routes.dart';

class AppUtils {
  AppUtils._();

  static printMessage(String message) {
    if (kDebugMode) {
      log(message);
    }
  }

  static int calculateDifference(DateTime now) {
    DateTime date = DateTime.now();
    return DateTime(date.year, date.month, date.day)
        .difference(DateTime(now.year, now.month, now.day))
        .inDays;
  }

  static String getYearMonthFromDays(int days) {
    int noOfDays = days;

    int year = noOfDays ~/ 365;
    noOfDays = noOfDays % 365;

    int month = noOfDays ~/ 30;
    noOfDays = noOfDays % 30;

    int week = noOfDays ~/ 7;
    noOfDays = noOfDays % 7;

    String result = "$year Year $month Months ";
        //"$week Weeks";
    return result;
  }

  static isFirstBeforeOrEqualThanSecond(DateTime  date1, DateTime date2) {
    int diff = DateTime(date1.year, date1.month, date1.day)
        .difference(DateTime(date2.year, date2.month, date2.day))
        .inDays;
    AppUtils.printMessage("isFirstBeforeThanSecond: $diff");
    if(diff<=0){
      return true;
    }else{
      return false;
    }

  }

  static DateTime parseDateTimeFromString(String rawDate){
    return DateFormat("yyyy-MM-dd").parse(rawDate);
  }

  static String getFormattedDateTime(String dateTime) {
    if (dateTime.isEmpty) {
      return "00:00";
    }
    DateTime timeDate = DateTime.parse(dateTime);
    String hour = timeDate.hour.toString();
    if (hour.length < 2) {
      hour = "0$hour";
    }
    String min = timeDate.minute.toString();
    if (min.length < 2) {
      min = "0$min";
    }
    return ("$hour:$min");
  }

  static String getFormattedTime(String time) {
    if (time.isEmpty) {
      return "00:00";
    }
    try {
      String timeFormatted =
      DateFormat.Hm().format(DateFormat("HH:mm:ss").parse(time));
      return (timeFormatted);
    } catch (e) {
      return "00:00";
    }
  }

  static String getDateAndDay() {
    DateTime date = DateTime.now();
    const dayData = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"};
    const monthData = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "June", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"};
    return "${dayData[date.weekday]}, ${monthData[date.month]} ${date.day}";
  }

  static String getDateNumber(String date) {
    if (date.isEmpty) {
      return "00";
    }
    DateTime target = DateTime.parse(date);
    return target.day.toString();
    // date.year.toString();
  }

  static String getDateDay(String date) {
    if (date.isEmpty) {
      return "Nil";
    }
    DateTime target = DateTime.parse(date);
    dynamic dayData =
        '{ "1" : "Mon", "2" : "Tue", "3" : "Wed", "4" : "Thu", "5" : "Fri", "6" : "Sat", "7" : "Sun" }';

    return json.decode(dayData)['${target.weekday}'];
    // date.year.toString();
  }

  static String getStandardFormat(String date) {
    if (date.isEmpty) {
      return "NA";
    }
    DateTime target = DateTime.parse(date);
    dynamic monthData =
        '{  "1": "January", "2": "February","3":  "March", "4":"April","5":"May","6":"June","7":"July","8": "August","9":"September","10":"October","11":"November","12":"December"}';

    String day = target.day.toString();
    String year =  target.year.toString();
    String months =  json.decode(monthData)['${target.month}'];
    return  "$day $months $year";
  }

  static getReversedDate(String date){
    final splitted = date.split('/');
    return '${splitted[2]}-${splitted[1]}-${splitted[0]}';
  }

  static String getCurrentMonth() {
    DateTime date = DateTime.now();
    dynamic monthData =
        '{  "1": "January", "2": "February","3":  "March", "4":"April","5":"May","6":"June","7":"July","8": "August","9":"September","10":"October","11":"November","12":"December"}';

    return json.decode(monthData)['${date.month}'];
  }

  static String getCurrentYear() {
    DateTime date = DateTime.now();
    return date.year.toString();
  }


  static String getCurrentDate(){
    DateTime today = DateTime.now();
    return "${today.day}-${today.month}-${today.year}";
  }

  static String getCurrentDateInverse(){
    DateTime today = DateTime.now();
    return "${today.year}-${today.month}-${today.day}";
  }

  static String getAddedDays(int numberOfDays){
    DateTime today = DateTime.now();
    final resignationDateFromNow = today.add(Duration(days: numberOfDays));
    return "${resignationDateFromNow.year}-${resignationDateFromNow.month}-${resignationDateFromNow.day}";
  }

  static String getYearFromDate(DateTime? dateTime) {
    dateTime ??= DateTime.now();
    return dateTime.year.toString();
  }

  static bool isTimePassed(String time) {
    final now = DateTime.now();
    final todayDate = "${now.year}-${now.month}-${now.day} $time";
    DateTime expirationDate = DateFormat("yyyy-MM-dd HH:mm:ss").parse(
        todayDate);
    return expirationDate.isBefore(now);
  }

  static Future<CroppedFile?> cropImage(BuildContext context,
      String value) async {
    CroppedFile? croppedImage = await ImageCropper().cropImage(
      sourcePath: value,
      uiSettings: [
        AndroidUiSettings(
            toolbarTitle: 'Crop Image',
            toolbarColor: Colors.deepOrange,
            toolbarWidgetColor: Colors.white,
            initAspectRatio: CropAspectRatioPreset.original,
            lockAspectRatio: true,
            aspectRatioPresets: [CropAspectRatioPreset.square]),
        IOSUiSettings(
          title: 'Crop Image',
          aspectRatioPresets: [CropAspectRatioPreset.square],
        ),
        WebUiSettings(
          context: context,
        ),
      ],
    );
    return croppedImage;
  }

  static getFileSize(File file) async {
    int decimals = 1;
    int bytes = await file.length();
    if (bytes <= 0) return "0 B";
    const suffixes = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
    var i = (mth.log(bytes) / mth.log(1024)).floor();
    return '${(bytes / mth.pow(1024, i)).toStringAsFixed(
        decimals)} ${suffixes[i]}';
  }

  static IconData getEditIcon(String key) => switch (key) {
        'Designation' => Icons.chair_outlined,
        'Experience' => Icons.auto_graph_outlined,
        'Skills' => Icons.menu_book_outlined,
        'Bio' => Icons.featured_play_list_outlined,
        'Address1' => Icons.location_on_outlined,
        'Address2' => Icons.location_on_outlined,
        'Zipcode' => Icons.location_on_outlined,
        'City' => Icons.location_on_outlined,
        'State' => Icons.location_on_outlined,
        'Country' => Icons.location_on_outlined,
        'Blood Group' => Icons.bloodtype_outlined,
        'Father Name' => Icons.elderly_outlined,
        'Mother Name' => Icons.elderly_woman_outlined,
        'Personal Email' => Icons.email_outlined,
        'Alternate Contact' => Icons.phone_android_outlined,
        'Family Address' => Icons.home_outlined,
        'Bank Name' => Icons.account_balance_outlined,
        'Account No.' => Icons.money,
        'IFSC Code' => Icons.pin,
        'Branch Name' => Icons.location_city_outlined,
        'Name as per Bank' => Icons.verified_user_outlined,
        'Pan No.' => Icons.credit_card_outlined,
        'AADHAR No.' => Icons.perm_identity_outlined,
        _ => Icons.star_purple500_rounded,
      };

  static String getRoutedAction(String action) => switch (action) {
        'HL' => Routes.splashPage,
        'LV' => Routes.leaveStatusPage,
        'RG' => Routes.regularizationDisplay,
        'RN' => Routes.resinStatusPage,
        'RM' => Routes.reimburseStatusPage,
        'HB' => Routes.splashPage,
        'GN' => Routes.splashPage,
        _ => Routes.splashPage,
      };

}
