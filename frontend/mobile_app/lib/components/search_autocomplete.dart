import 'package:flutter/material.dart';
import 'package:mobile_app/handler/plants.dart';

class SearchAutoComplete extends StatefulWidget {
  final Function(String, bool) onQuerySet;
  const SearchAutoComplete({Key? key, required this.onQuerySet}): super(key: key);

  @override
  State<SearchAutoComplete> createState() => _SearchAutoCompleteState();
}

class _SearchAutoCompleteState extends State<SearchAutoComplete> {
  final PlantsHandler _plantsHandler = PlantsHandler();
  late String _query = '';

  @override
  Widget build(BuildContext context) {
    return Autocomplete<String>(
        fieldViewBuilder: (BuildContext context, TextEditingController fieldTextEditingController, FocusNode fieldFocusNode, VoidCallback onFieldSubmitted) {
          return TextField(
            controller: fieldTextEditingController,
            onChanged: (String value) {
              setState(() {
                _query = value;
              });
            },
            focusNode: fieldFocusNode,
            decoration: InputDecoration(
              border: const OutlineInputBorder(
                borderRadius: BorderRadius.all(Radius.circular(25)),
              ),
              suffixIcon: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  if (_query.isNotEmpty)
                    IconButton(
                      splashRadius: 20,
                      splashColor: Colors.transparent,
                      color: Colors.grey,
                      onPressed: () {
                        setState(() {
                          _query = '';
                          fieldTextEditingController.clear();
                        });
                        widget.onQuerySet('', false);
                      },
                      icon: const Icon(Icons.clear_rounded),
                    ),
                  Container(
                    margin: const EdgeInsets.only(top: 7, bottom:7, right: 5),
                    child: Ink(
                      decoration: ShapeDecoration(
                        color: Colors.deepPurpleAccent.withOpacity(0.2),
                        shape: const CircleBorder(),
                      ),
                      child: IconButton(
                        splashRadius: 20,
                        splashColor: Colors.transparent,
                        color: Colors.deepPurpleAccent,
                        onPressed: () {
                          setState(() {
                            _query = fieldTextEditingController.text;
                          });
                          widget.onQuerySet(fieldTextEditingController.text, true);
                          FocusScope.of(context).unfocus();
                        },
                        icon: const Icon(
                          Icons.search_rounded,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
        displayStringForOption: (String option) => option,
        onSelected: (String selection) {
          setState(() {
            _query = selection;
          });
          widget.onQuerySet(selection, true);
        },
        optionsBuilder: (TextEditingValue textEditingValue) async {
          if (textEditingValue.text == '') {
            return const Iterable<String>.empty();
          }
          final response = await _plantsHandler.autocomplete(query: textEditingValue.text, field: 'scientific_name.autocomplete');
          List<String> options = [];
          for (var option in response.data['suggest']['autocomplete_suggest'][0]['options']) {
            options.add(option['text']);
          }
          return options;
        }
    );
  }
}
