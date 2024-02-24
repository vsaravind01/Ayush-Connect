import 'package:flutter/material.dart';

class ChatBubble extends StatefulWidget {
  final String? text;
  final String? type;
  const ChatBubble({Key? key, required this.text, required this.type})
      : super(key: key);

  @override
  State<ChatBubble> createState() => _ChatBubbleState();
}

class _ChatBubbleState extends State<ChatBubble> {
  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment:
          widget.type == 'bot' ? CrossAxisAlignment.start : CrossAxisAlignment.end,
      children: [
        SizedBox(
          width: MediaQuery.of(context).size.width * 0.65,
          child: Container(
            padding: const EdgeInsets.all(10),
            margin: const EdgeInsets.only(top: 10),
            decoration: BoxDecoration(
              color: widget.type == 'bot' ? Colors.grey[300] : Colors.blue[300],
              borderRadius: BorderRadius.circular(10),
            ),
            child: Text(
              "${widget.text}",
              style: const TextStyle(
                fontSize: 16,
              ),
            ),
          ),
        ),
      ],
    );
  }
}
