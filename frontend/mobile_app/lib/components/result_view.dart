import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/handler/plants.dart';

class ResultView extends StatefulWidget {
  final String scientificName;

  const ResultView({Key? key, required this.scientificName}) : super(key: key);

  @override
  State<ResultView> createState() => _ResultViewState();
}

class _ResultViewState extends State<ResultView> {
  final PlantsHandler _plantsHandler = PlantsHandler();
  final List _plantMedia = [];
  List _plants = [];

  @override
  void initState() {
    super.initState();
    searchPlant(widget.scientificName);
  }

  void searchPlant(String plantName) async {
    final response = await _plantsHandler
        .search(query: plantName, fields: ['scientific_name']);
    setState(() {
      _plants = response.data['hits']['hits'];
      for (var element in _plants) {
        var media = element['_source']['media'];
        for (var mediaElement in media) {
          var _mediaElement = mediaElement;
          _mediaElement['id'] = element['_id'];
          if (_mediaElement['identifier'] != null) {
            _plantMedia.add(_mediaElement);
          }
        }
      }
      print(_plantMedia);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: _plants.isNotEmpty && _plantMedia.isNotEmpty
          ? Column(children: [
              Text(_plants[0]['_source']['scientific_name'],
                  style: const TextStyle(
                      fontSize: 24, fontWeight: FontWeight.w700)),
              Text("Species: " + _plants[0]['_source']['species']),
              Text("Family: " + _plants[0]['_source']['family']),
              Expanded(
                child: GridView.builder(
                  itemCount: _plantMedia.length,
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                  ),
                  itemBuilder: (context, index) {
                    return Container(
                      decoration: BoxDecoration(
                        border: Border.all(
                          color: Theme.of(context).canvasColor,
                          width: 3,
                        ),
                      ),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(10),
                        child: CachedNetworkImage(
                          imageUrl: _plantMedia[index]['identifier'],
                          imageBuilder: (context, imageProvider) => Container(
                            decoration: BoxDecoration(
                              image: DecorationImage(
                                image: imageProvider,
                                fit: BoxFit.cover,
                              ),
                            ),
                          ),
                          errorWidget: (BuildContext context, String url, dynamic error) {
                            return const Center(
                              child: Text('Unable to load image'),
                            );
                          },
                          progressIndicatorBuilder: (context, url, downloadProgress) {
                            print(downloadProgress.progress);
                            return Center(
                              child: CircularProgressIndicator(
                                value: downloadProgress.progress,
                              ),
                            );
                          },
                          fit: BoxFit.cover,
                        ),
                      ),
                    );
                  },
                )
              )
            ])
          : const Center(child: Text('No results found')),
    );
  }
}
