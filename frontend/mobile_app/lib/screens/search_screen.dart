import 'package:flutter/material.dart';
import 'package:mobile_app/components/result_view.dart';
import 'package:mobile_app/components/search_autocomplete.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  late String _query = '';
  late bool showResult = false;

  void onQuerySet(String query, bool showResult) {
    setState(() {
      _query = query;
      this.showResult = showResult;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        padding: const EdgeInsets.only(left: 25, right: 25, bottom: 54),
        child: Column(
          children: [
            SearchAutoComplete(
              onQuerySet: onQuerySet,
            ),
            if (showResult)
              Flexible(
                child: ResultView(
                  scientificName: _query,
                ),
              )
          ],
        ),
      ),
    );
  }
}
