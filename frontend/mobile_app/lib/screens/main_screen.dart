import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/screens/camera_screen.dart';
import 'package:mobile_app/screens/home_screen.dart';
import 'package:mobile_app/screens/plantgpt_screen.dart';
import 'package:mobile_app/screens/profile_screen.dart';
import 'package:mobile_app/screens/search_screen.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _selectedIndex = 0;

  static const Map<String, Widget> _widgetOptions = {
    "Ayush Connect": HomeScreen(),
    "Search": SearchScreen(),
    "PlantGPT": PlantgptScreen(),
    "Profile": ProfileScreen(),
  };

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => FocusManager.instance.primaryFocus?.unfocus(),
      child: Placeholder(
        child: Scaffold(
          extendBody: true,
          appBar: AppBar(
            scrolledUnderElevation: 9.0,
            forceMaterialTransparency: true,
            titleTextStyle: const TextStyle(
                fontWeight: FontWeight.w700, color: Colors.black87, fontSize: 24),
            title: Text(_widgetOptions.keys.elementAt(_selectedIndex)),
          ),
          bottomNavigationBar: BottomAppBar(
            color: Colors.lightGreenAccent.shade100,
            elevation: 10.0,
            shape: const CircularNotchedRectangle(),
            notchMargin: 5,
            child: SizedBox(
              height: 75,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  IconButton(
                    splashColor: Colors.transparent,
                    icon: _selectedIndex == 0
                        ? const Icon(Icons.home_rounded)
                        : const Icon(Icons.home_outlined),
                    color: _selectedIndex == 0
                        ? Theme.of(context).primaryColor
                        : Theme.of(context).disabledColor,
                    onPressed: () {
                      setState(() {
                        _selectedIndex = 0;
                      });
                    },
                  ),
                  IconButton(
                    splashColor: Colors.transparent,
                    icon: const Icon(Icons.search),
                    color: _selectedIndex == 1
                        ? Theme.of(context).primaryColor
                        : Theme.of(context).disabledColor,
                    onPressed: () {
                      setState(() {
                        _selectedIndex = 1;
                      });
                    },
                  ),
                  IconButton(
                    splashColor: Colors.transparent,
                    icon: _selectedIndex == 2
                        ? const Icon(Icons.energy_savings_leaf_rounded)
                        : const Icon(Icons.energy_savings_leaf_outlined),
                    color: _selectedIndex == 2
                        ? Theme.of(context).primaryColor
                        : Theme.of(context).disabledColor,
                    onPressed: () {
                      setState(() {
                        _selectedIndex = 2;
                      });
                    },
                  ),
                  IconButton(
                    splashColor: Colors.transparent,
                    icon: _selectedIndex == 3
                        ? const Icon(Icons.person_rounded)
                        : const Icon(Icons.person_outline_rounded),
                    color: _selectedIndex == 3
                        ? Theme.of(context).primaryColor
                        : Theme.of(context).disabledColor,
                    onPressed: () {
                      setState(() {
                        _selectedIndex = 3;
                      });
                    },
                  ),
                ],
              ),
            ),
          ),
          body: Center(
            child: _widgetOptions.values.elementAt(_selectedIndex),
          ),
          floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
          floatingActionButton: FloatingActionButton(
            backgroundColor: Colors.greenAccent.shade700,
            shape: const CircleBorder(),
            tooltip: 'Camera',
            onPressed: () async {
              await availableCameras().then((value) => Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (_) => CameraScreen(cameras: value))));
            },
            child: const Icon(Icons.camera_alt_rounded),
          ),
        ),
      ),
    );
  }
}
