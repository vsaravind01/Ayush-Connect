import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/handler/plants.dart';

class ResultsView extends StatefulWidget {
  final String scientificName;

  const ResultsView({Key? key, required this.scientificName}) : super(key: key);

  @override
  State<ResultsView> createState() => _ResultsViewState();
}

class _ResultsViewState extends State<ResultsView> {
  final PlantsHandler _plantsHandler = PlantsHandler();
  final List _plantMedia = [];
  List _plants = [];

  @override
  void initState() {
    super.initState();
    searchPlant(widget.scientificName);
  }

  Map getPlantFromId(String id) {
    for (var plant in _plants) {
      if (plant['_id'] == id) {
        return plant['_source'];
      }
    }
    return {};
  }

  String convertDate(String date) {
    // format should be dd month yyyy
    date =
        DateTime.parse(date.toString()).toLocal().toString().substring(0, 10);
    var dateSplit = date.split('-');
    var month = dateSplit[1];
    var day = dateSplit[2];
    var year = dateSplit[0];
    switch (month) {
      case '01':
        month = 'January';
        break;
      case '02':
        month = 'February';
        break;
      case '03':
        month = 'March';
        break;
      case '04':
        month = 'April';
        break;
      case '05':
        month = 'May';
        break;
      case '06':
        month = 'June';
        break;
      case '07':
        month = 'July';
        break;
      case '08':
        month = 'August';
        break;
      case '09':
        month = 'September';
        break;
      case '10':
        month = 'October';
        break;
      case '11':
        month = 'November';
        break;
      case '12':
        month = 'December';
        break;
    }
    return '$day $month $year';
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
              Text("Species: ${_plants[0]['_source']['species']}"),
              Text("Family: ${_plants[0]['_source']['family']}"),
              Expanded(
                  child: GridView.builder(
                itemCount: _plantMedia.length,
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                ),
                itemBuilder: (context, index) {
                  return InkWell(
                    onTap: () {
                      showModalBottomSheet(
                          isDismissible: true,
                          isScrollControlled: true,
                          showDragHandle: true,
                          shape: const RoundedRectangleBorder(
                            borderRadius: BorderRadius.only(
                              topLeft: Radius.circular(10),
                              topRight: Radius.circular(10),
                            ),
                          ),
                          anchorPoint: const Offset(0.5, 0.5),
                          context: context,
                          builder: (context) {
                            return Container(
                              height: MediaQuery.of(context).size.height * 0.90,
                              color: Colors.transparent,
                              child: Column(
                                children: [
                                  SizedBox(
                                    height: 50,
                                    child: Container(
                                      margin: const EdgeInsets.symmetric(
                                          horizontal: 10),
                                      alignment: Alignment.center,
                                      child: Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.spaceAround,
                                        children: [
                                          Container(
                                            margin:
                                                const EdgeInsets.only(top: 10),
                                            width: MediaQuery.of(context)
                                                    .size
                                                    .width *
                                                0.8,
                                            child: Text(
                                              _plants[0]['_source']
                                                  ['scientific_name'],
                                              style: const TextStyle(
                                                fontSize: 18,
                                                fontWeight: FontWeight.w700,
                                              ),
                                            ),
                                          ),
                                          IconButton(
                                            splashColor: Colors.grey,
                                            splashRadius: 15,
                                            onPressed: () {
                                              Navigator.pop(context);
                                            },
                                            icon:
                                                const Icon(Icons.close_rounded),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                  Expanded(
                                    child: SizedBox(
                                      width: 350,
                                      child: CachedNetworkImage(
                                        repeat: ImageRepeat.noRepeat,
                                        imageUrl: _plantMedia[index]
                                            ['identifier'],
                                        imageBuilder:
                                            (context, imageProvider) =>
                                                Container(
                                          decoration: BoxDecoration(
                                            image: DecorationImage(
                                              image: imageProvider,
                                            ),
                                          ),
                                        ),
                                        errorWidget: (BuildContext context,
                                            String url, dynamic error) {
                                          return const Center(
                                            child: Text('Unable to load image'),
                                          );
                                        },
                                        progressIndicatorBuilder:
                                            (context, url, downloadProgress) {
                                          return Center(
                                            child: CircularProgressIndicator(
                                              value: downloadProgress.progress,
                                            ),
                                          );
                                        },
                                      ),
                                    ),
                                  ),
                                  Padding(
                                      padding: const EdgeInsets.all(10),
                                      child: Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.spaceAround,
                                        children: [
                                          Text(
                                              "${convertDate(getPlantFromId(_plantMedia[index]['id'])['eventDate'])}",
                                              style: const TextStyle(
                                                fontSize: 16,
                                                fontWeight: FontWeight.w700,
                                              )),
                                        ],
                                      )),
                                  Padding(
                                    padding: const EdgeInsets.all(10),
                                    child: Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceAround,
                                      children: [
                                        if (getPlantFromId(_plantMedia[index]
                                                    ['id'])['level0'] !=
                                                null &&
                                            getPlantFromId(_plantMedia[index]
                                                    ['id'])['level1'] !=
                                                null &&
                                            getPlantFromId(_plantMedia[index]
                                                    ['id'])['level2'] !=
                                                null) ...[
                                          Row(
                                            children: [
                                              const Text(
                                                  "Place: ",
                                                  style: TextStyle(
                                                    fontSize: 16,
                                                    fontWeight: FontWeight.w700,
                                                  )
                                              ),
                                              Text(
                                                  "${getPlantFromId(_plantMedia[index]['id'])['level0']}, ${getPlantFromId(_plantMedia[index]['id'])['level1']}, ${getPlantFromId(_plantMedia[index]['id'])['level2']}",
                                                  style: const TextStyle(
                                                    fontSize: 16,
                                                    fontWeight: FontWeight.normal,
                                                  )),
                                            ],
                                          ),
                                        ],
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            );
                          });
                    },
                    child: Container(
                      decoration: BoxDecoration(
                        border: Border.all(
                          color: Theme.of(context).canvasColor,
                          width: 3,
                        ),
                      ),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(10),
                        child: CachedNetworkImage(
                          repeat: ImageRepeat.noRepeat,
                          imageUrl: _plantMedia[index]['identifier'],
                          imageBuilder: (context, imageProvider) => Container(
                            decoration: BoxDecoration(
                              image: DecorationImage(
                                image: imageProvider,
                                fit: BoxFit.cover,
                              ),
                            ),
                          ),
                          errorWidget: (BuildContext context, String url,
                              dynamic error) {
                            return const Center(
                              child: Text('Unable to load image'),
                            );
                          },
                          progressIndicatorBuilder:
                              (context, url, downloadProgress) {
                            return Center(
                              child: CircularProgressIndicator(
                                value: downloadProgress.progress,
                              ),
                            );
                          },
                          fit: BoxFit.cover,
                        ),
                      ),
                    ),
                  );
                },
              ))
            ])
          : const Center(child: Text('No results found')),
    );
  }
}
