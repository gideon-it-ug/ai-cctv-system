class Event {
  final int id;
  final String cameraName;
  final String eventType;
  final double confidence;
  final String timestamp;
  final String? imageUrl;

  Event({
    required this.id,
    required this.cameraName,
    required this.eventType,
    required this.confidence,
    required this.timestamp,
    this.imageUrl,
  });

  factory Event.fromJson(Map<String, dynamic> json) {
    return Event(
      id: json['id'],
      cameraName: json['camera_name'] ?? 'Unknown',
      eventType: json['event_type'] ?? 'unknown',
      confidence: (json['confidence'] as num).toDouble(),
      timestamp: json['timestamp'],
      imageUrl: json['image'],
    );
  }
}