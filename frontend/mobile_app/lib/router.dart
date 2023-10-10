import 'package:go_router/go_router.dart';
import 'package:mobile_app/screens/main_screen.dart';

final GoRouter router = GoRouter(routes: [
  GoRoute(
    path: "/",
    builder: (context, state) => const MainScreen(),
  ),
  // GoRoute(
  //   path: "/news/:id/:path",
  //   name: "news",
  //   builder: (context, state) => NewsPage(
  //     userId: state.params["id"].toString(),
  //     path: state.params["path"].toString(),
  //   ),
  // )
]);