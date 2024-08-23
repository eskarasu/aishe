import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(AISheApp());
}

class AISheApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  String _response = "";

  Future<void> _sendMessage() async {
    final message = _controller.text;
    if (message.isEmpty) return;

    final response = await http.post(
      Uri.parse('http://127.0.0.1:5000/chat'), // Flask sunucusu URL'sini buraya yazın
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"message": message}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      setState(() {
        _response = data['response'];
      });
    } else {
      setState(() {
        _response = "Error: Unable to get response from server.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('AIShe Chat'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                child: Text(_response),
              ),
            ),
            TextField(
              controller: _controller,
              decoration: InputDecoration(labelText: 'Enter your message'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _sendMessage,
              child: Text('Send'),
            ),
          ],
        ),
      ),
    );
  }
}
