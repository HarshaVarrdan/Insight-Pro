import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.secondary,
        title: Text("Upload your Nakku",
            style: Theme.of(context).textTheme.titleLarge),
        centerTitle: true,
        elevation: 10,
        toolbarHeight: MediaQuery.of(context).size.height / 5,
      ),
      body: Container(
        width: MediaQuery.of(context).size.width,
        padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 20),
        child: Column(
          //mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            SizedBox(
              height: MediaQuery.of(context).size.height / 15,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Text(
                    "The format of the file must be .csv",
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                  Text("The first row should contain headers (column names).",
                      style: Theme.of(context).textTheme.bodySmall),
                  Text("Ensure each column has consistent data types.",
                      style: Theme.of(context).textTheme.bodySmall),
                ],
              ),
            ),
            Card(
              color: Theme.of(context).colorScheme.tertiary,
              elevation: .5,
              shape: RoundedRectangleBorder(
                  side: BorderSide.none,
                  borderRadius: BorderRadius.circular(50)),
              child: SizedBox(
                height: MediaQuery.of(context).size.height / 3,
                width: MediaQuery.of(context).size.width,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
