import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import 'package:insigth_pro/functions/commonfunctions.dart';

class BackendFunction {
  Future<void> uploadFile(String filePath, BuildContext context) async {
    var request = http.MultipartRequest(
        'POST', Uri.parse('http://192.168.19.237:5000/upload'));
    request.files.add(await http.MultipartFile.fromPath('file', filePath));
    var response = await request.send();

    if (response.statusCode == 200) {
      var responseData = await response.stream.toBytes();
      var responseString = String.fromCharCodes(responseData);
      CommonFunctions().showMessageSnackBar("Success", context);
      Object result = json.decode(responseString)['result'];
      print(result);
    } else {
      print("Error : ${response.statusCode}");
      CommonFunctions()
          .showMessageSnackBar('Error: ${response.statusCode}', context);
    }
  }
}
