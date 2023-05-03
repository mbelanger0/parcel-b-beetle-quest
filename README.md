# Parcel B Beetle Quest
See more information on the [project website](https://olincollege.github.io/parcel-b-beetle-quest)!

A text-based choose-your-own-adventure game themed around a quintessential
memory for students at Olin College of Engineering: hunting in Parcel B for a
click beetle.

This game is written in Python using the pygame library. Code is structured
using the MVC (model, view, controller) software architecture, with the
character, scene, and controller class representing each respectively.

This project was created by Carter Harris, Mark Belanger, and Elin O'Neill as
a final project for Olin College of Engineering's Software Design Course.

## Setup Requirements & Usage
In order to run this game:
* Clone the repo to your computer or download the latest GitHub release
* Install pygame and pillow (the two external libraries this game depends on) by
running `pip install -r requirements.txt`
* Run the file `main.py` by typing `python main.py` into a terminal open to the
project directory.

### Dependencies
The pygame library is used extensively to create game windows, grab user input,
and overall construct all visuals of the game. Additionally, the pillow library
is used for some basic image processing (mainly getting image sizes) to aid
in creating pygame windows and ensuring backgrounds are large enough to fill
the screen. 
