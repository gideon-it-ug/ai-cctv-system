import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/event.dart';
import '../config.dart';

class ApiService {
  static Future<List<Event>> fetchEvents() async {
    final response = await http.get(Uri.parse('${AppConfig.baseUrl}/events/'));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final List results = data is List ? data : data['results'];
      return results.map((json) => Event.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load events');
    }
  }
}