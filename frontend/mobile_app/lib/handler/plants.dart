import 'package:dio/dio.dart';

const baseUrl = 'http://10.0.2.2:8000';

class PlantsHandler {
  final Dio _dio = Dio();
  static const List<String> defaultSearchFields = ['scientific_name'];

  Future<Response> search({required String query, List<
      String> fields = defaultSearchFields}) async {
    try {
      final fieldsString = fields.join(',');
      var response = await _dio.get(
          '$baseUrl/index/plants/search?query=$query&fields=$fieldsString');
      return response;
    } catch (e) {
      rethrow;
    }
  }

  Future<Response> autocomplete({required String query, String field = "scientific_name.autocomplete"}) async {
    try {
      var response = await _dio.get(
          '$baseUrl/index/plants/autocomplete?query=$query&field=$field');
      return response;
    } catch (e) {
      rethrow;
    }
  }
}