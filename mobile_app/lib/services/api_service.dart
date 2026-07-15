import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/event.dart';

class ApiService {
  // Use your laptop's LAN IP, same one your React dashboard uses
  static const String baseUrl = "http://192.168.1.4:8000/api";

  static Future<List<Event>> fetchEvents() async {
    final response = await http.get(Uri.parse('$baseUrl/events/'));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final List results = data is List ? data : data['results'];
      return results.map((json) => Event.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load events');
    }
  }
}