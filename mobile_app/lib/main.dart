import 'dart:async';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'models/event.dart';
import 'services/api_service.dart';

void main() {
  runApp(const CCTVApp());
}

class CCTVApp extends StatelessWidget {
  const CCTVApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI CCTV',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0B0E11),
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF3DDC84),
          brightness: Brightness.dark,
        ),
        cardColor: const Color(0xFF12161B),
      ),
      home: const EventFeedScreen(),
    );
  }
}

class EventFeedScreen extends StatefulWidget {
  const EventFeedScreen({super.key});

  @override
  State<EventFeedScreen> createState() => _EventFeedScreenState();
}

class _EventFeedScreenState extends State<EventFeedScreen> {
  List<Event> _events = [];
  bool _loading = true;
  String? _error;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _loadEvents();
    _timer = Timer.periodic(const Duration(seconds: 5), (_) => _loadEvents());
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> _loadEvents() async {
    try {
      final events = await ApiService.fetchEvents();
      setState(() {
        _events = events;
        _loading = false;
        _error = null;
      });
    } catch (e) {
      setState(() {
        _error = 'Could not reach backend';
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF12161B),
        title: const Text('🎥 Event Feed'),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(child: Text(_error!, style: const TextStyle(color: Colors.redAccent)))
              : _events.isEmpty
                  ? const Center(child: Text('No events yet.'))
                  : RefreshIndicator(
                      onRefresh: _loadEvents,
                      child: ListView.builder(
                        padding: const EdgeInsets.all(12),
                        itemCount: _events.length,
                        itemBuilder: (context, index) {
                          final event = _events[index];
                          return Card(
                            margin: const EdgeInsets.only(bottom: 10),
                            child: ListTile(
                              leading: event.imageUrl != null
                                  ? ClipRRect(
                                      borderRadius: BorderRadius.circular(6),
                                      child: Image.network(
                                        event.imageUrl!,
                                        width: 60,
                                        height: 60,
                                        fit: BoxFit.cover,
                                        errorBuilder: (_, __, ___) =>
                                            const Icon(Icons.image_not_supported),
                                      ),
                                    )
                                  : const Icon(Icons.camera_alt),
                              title: Text('${event.cameraName} — ${event.eventType}'),
                              subtitle: Text(
                                '${(event.confidence * 100).toStringAsFixed(0)}% confidence\n'
                                '${DateFormat.yMMMd().add_jm().format(DateTime.parse(event.timestamp).toLocal())}',
                              ),
                              isThreeLine: true,
                            ),
                          );
                        },
                      ),
                    ),
    );
  }
}