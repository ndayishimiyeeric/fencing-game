# Fancy Fencing

> This is a python3 project assigned to me by Université de Paris at the end of the module Advanced programming in the M1 program. In this project I created a terminal and a graphical game version mimicking the Fencing sport game.

## Built with
- Python3

## Modules and Libraries
- `Curses`: for terminal version functionalities
- `Pygame`: for 2D graphical version functionalities
- `Threading`: for running the program concurrently
- `Playsound`: for Sound and music functionalities
- `Datetime`: for accessing the current date and time
- `Time`: for refresh rate per seconds

## Clone the project
*You can download or clone this project by running this command in your terminal:*
- this will create a directory in the name of the project folder.
```
git clone https://github.com/ndayishimiyeeric/fencing-game.git
```
- to change into the project folder. Open the project in a text editor of your choice example [Vs code](https://code.visualstudio.com/)
```
cd fencing-game
```
- Run 
> for windows users.
```
python main.py
```
> for Linux or Mac users.
```
python3 main.py
```
You will be prompted to choose between the terminal or graphical versions of the   game, type t for terminal and g for graphical.
- ***N.B to run the terminal version of the game the terminal width must be above 700 pixels wide and height above 300 pixels wide if the game fails to run, increase both width and height***

## Prerequisites
**To understand the code base of the project at least you must have a basic skill level in python. To run the following program:**
- Must have python3 installed up and running to install head to python website.
- Install all Modules and libraries listed in the Modules and Libraries section:
> Curses for Linux and Mac users it is preinstalled for windows run
```
pip install windows-curses
```
> Pygame run
```
pip install pygame
```
> Playsound run
```
pip install playsound==1.2.2
```
> Threading, Datetime and Time are preinstalled

## Terminal version
**Controls:**
- ***Game controls:***
> Type **W** to access a pause menu. Type **T** and **G** to navigate the pause menu.
> Type **B** to quite the game

- ***Player one (Left, Green):***
> Type **D** to move to the right and **E** to jump to the right.
> Type **Q** to move to the left and **A** to jump to the left.
> Type **Z** to attack and **S** to block.

-**Player Two (Right, Yellow):**
> Type **M** to move to the right and **P** to jump to the right.
> Type **K** to move to the left and **I** to jump to the left.
> Type **O** to attack and **L** to block.

**Game rules:**
- o	If you step on the block element (Red box) the opponent wins one point.
- o	If you attack and the opponent fails to block you win one point.
- o	When you attach you move forward 4 steps

## Graphical Version
**Controls**
- **Game controls**
> Click **Escape** for a pause menu
> Click **Space** bar to start the game **H** for help

- **Player one (Left):**
> Type **D** to move to the right.
> Type **Q** to move to the left.
> Type **Z** to attack and **S** to block.

- **Player Two (Right):**
> Click **Right arrow** to move to the right.
> Click **Left arrow** to move to the left.
> Click **Up arrow** to attack and **Down arrow** to block.

**Game rules:**
- o	If you step outside the pitch behind the blue line the opponent wins one point.
- o	If you attack and the opponent fails to block you win one point.
- o	When you attack to move forward 10 steps.
- o	When you block you move back 10 steps.

## Knowledge and skills
> Through the development of this project, I gained many skills and I get the opportunity to apply all technics and skills of python that I’ve been learning in the Advanced programming module including:
- Working with the system and files through the os python module.
-	Analogy of running a program concurrently, application of multi-programming and asynchronous vs synchronous programming paradigms.
-	Functional programming and object-oriented programming.
-	Python data structure sets, dictionary, tuple, lists, strings, integers, float etc.
-	Python control structures and exceptions handling.
-	Pythonicness and Packaging.

## Acknowledgements
-	All thanks to the Université de Paris institution for giving me the opportunity to work on this project.
-	Thanks to Lecture/Head of the Advanced programming module and the TP supervisor for creating this opportunity for me.

## Author

👤 **Ndayishimiyeeric**

- GitHub: [@ndayishimiyeeric](https://github.com/ndayishimiyeeric)
- Twitter: [@odaltongain](https://twitter.com/odaltongain)
- LinkedIn: [Ndayishimiye Eric](https://linkedin.com/in/nderic)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## Show your support

Give a ⭐️ if you like this project!

## 📝 License

This project is [MIT](./LICENSE) licensed.
