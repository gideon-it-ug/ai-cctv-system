import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../config.dart';

class AuthService {
  static const _storage = FlutterSecureStorage();

  static Future<String?> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/auth/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      await _storage.write(key: 'access_token', value: data['access']);
      await _storage.write(key: 'refresh_token', value: data['refresh']);
      return null; // no error
    } else {
      final data = jsonDecode(response.body);
      return data['detail'] ?? 'Login failed. Check your username and password.';
    }
  }

  static Future<String?> register(String username, String email, String password) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/auth/register/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'email': email, 'password': password}),
    );

    if (response.statusCode == 201) {
      return null; // no error
    } else {
      final data = jsonDecode(response.body);
      return data.values.first is List ? data.values.first[0].toString() : 'Registration failed.';
    }
  }

  static Future<String?> getAccessToken() async {
    return await _storage.read(key: 'access_token');
  }

  static Future<bool> isLoggedIn() async {
    final token = await getAccessToken();
    return token != null;
  }

  static Future<void> logout() async {
    await _storage.delete(key: 'access_token');
    await _storage.delete(key: 'refresh_token');
  }

  static Future<Map<String, dynamic>?> getCurrentUser() async {
    final token = await getAccessToken();
    if (token == null) return null;

    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/auth/me/'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }
}