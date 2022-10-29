# Overview

This software uses Firestore to create a database of dice. As I make dice as a hobby, it's essential to have a way to categorize them and know when they're ready to be sanded or polished. This program helps keep them separate, and can be used by anyone looking to organize their dice making process.

This small program is a text-based program, so all of your work is done in the console. In my tutorial I briefly show how to hook it up to Google Firestore.

[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database

Dice Scheduler uses Google Firestore. To use on your computer, install firebase-admin
```
pip install firebase-admin
```
create an account, a Firebase project, and a Firebase database to hook into the Scheduler for your own projects. 

Firebase is a NoSQL database, and uses this JSON structure:

```
dice: {
 id: {
  "name": name,
  "description": description,
  "date": date,
  "resin": resin
  "demoldTime": date,
  "fullCureTime": date,
  "tumbler": boolean,
  "tumblerDate": date
 }
}
```

# Development Environment

Dice Scheduler was made in Visual Studio Code in Python, using Google Firestore's Realtime Database.

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Google's Firestore Docs](https://firebase.google.com/docs/firestore/manage-data/structure-data)
* [Free Code Camp](https://www.freecodecamp.org/news/how-to-get-started-with-firebase-using-python/)

# Future Work

* Move finished dice (inked, polished, or ready to be sold) to another database
* Create GUI for project, either as a web project or Android app
