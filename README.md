
# Chess:E Board Client

Chess:E is an internet-enabled, physical chess robot that allows remote players to connect and play chess together in a tangible, analog experience. The robot is equipped with an electromagnet that holds chess pieces from beneath the board and two stepper motors that move the electromagnet across each of the two axes. The board client, which runs on a Raspberry Pi 400, serves as a bridge between the robot's motors and the backend server of our website, [https://chesse.koeni.dev](https://chesse.koeni.dev).

  

This documentation describes the board client and how it enables players to play chess remotely.

  

## Setup

Clone the repository

	$ git clone https://github.com/PawnHubChess/client-board

Install dependencies

	$ pip install -r requirements.txt

## Gamemode 1: Play against human on robot
This gamemode assumes you are playing on the robot.
- Run `main/client.py`
- Answer with `1` to choose the first gamemode
- Answer with `1` if you want a textual board visualisation in the console, answer with `2`, if you don't 

Go to [https://chesse.koeni.dev/play](https://chesse.koeni.dev/play) and enter your connection code and ID **OR** click on the connection link provided in the console.

Every move your opponent (white player) makes on the website is reflected on the robot through motor movements.
Every move you (black player) make is captured by the camera and reflected on the website.

## Gamemode 2: Play against AI on robot
This gamemode assumes you are playing on the robot.
- Run `main/client.py`
- Answer with `2` to choose the second gamemode
- Choose a difficulty level (higher difficulties result in longer response times)
	- Answer with `1`, for easy difficulty
	- Answer with `2`, for medium difficulty
	- Answer with `3`, for hard difficulty

Every move you (white player) make is captured by the camera and sent to the AI.
Every move the AI (black player) makes is reflected on the robot through motor movements.

##  Gamemode 3: Play against AI on website
This gamemode assumes you are playing on the website.
- Run `main/client.py`
- Answer with `3` to choose the third gamemode
- Choose a difficulty level (higher difficulties result in longer response times)
	- Answer with `1`, for easy difficulty
	- Answer with `2`, for medium difficulty
	- Answer with `3`, for hard difficulty
- Answer with `1` if you want a textual board visualisation in the console, answer with `2`, if you don't 

Go to [https://chesse.koeni.dev/play](https://chesse.koeni.dev/play) and enter your connection code and ID **OR** click on the connection link provided in the console.

Every move you (white player) make is captured by the website and sent to the AI.
Every move the AI (black player) makes is reflected on the website.

## Architecture

![architecure](diagrams/architecure.png)

The Chess:E project is composed of multiple components that work together to enable remote gameplay. The focus of this documentation is the architecture of the board client.

### Client
The `client` module is the main program of the board client and serves as the entry point for all other modules. It connects to the backend server via websockets and generates a randomized connection code and link for each game. It sends and receives JSON string commands to and from the backend, accepts or declines attendee requests from website players, and sends and receives chess moves. The program exits when the opponent disconnects from the game.

### Chess AI
The `chess_ai` module hosts every function which is responsible for enabling a game against the AI. It assigns a score to the local chess board based on the values of the pieces, iterates over every square, retrieves the piece on the square, and adds or subtracts the piece’s value to the score depending on the piece color.

It searches through the game tree to determine the best move for the current player. The `depth` parameter determines how many moves ahead to consider, the `alpha` and `beta` parameter are used to prune the search tree. It generates all possible moves and recursively calls `minimax` on each possible one while updating `alpha` and `beta`.

It first checks whether the `player_move` is legal and pushes it onto the board. Then, it uses the `minimax` function to find the best move and adds the one with the highest score to the board.

### Image Capturing & Recognition
The `capture_image` module is designed for image capturing within the robot. The script's primary function is to capture images of the chessboard and save them for further processing. When triggered, it initiates the camera, captures a frame, and processes it to ensure it's appropriately cropped and focused on the chessboard. The captured images are then saved as `image1.jpg` and `image2.jpg`.

The `image_recognition` module is responsible for detecting chess piece movements on the board through image analysis, using OpenCV. It analyzes two grayscale images, taken before and after a move, to identify changes on the chessboard. The script highlights these changes using thresholding and then finds contours to pinpoint the areas of movement. It calculates the central points of these contours to determine the exact starting and ending positions of the moved piece on the chessboard, assigning these positions to `move_from` and `move_to` attributes.

### Motors & Magnet
The `motor`, `motor_move`, `motor_off` and `magnet` modules host classes which are responsible for the general movement of the robot's motors and magnet. The `motor` module sets up the connection between Raspberry Pi and motors by configuring their pins. The `motor_move` inherits from the `motor` and hosts all functions that make the motors move with the parameters given on call. The `magnet` module hosts the functions to set up the electromagnet, and turn it on and off.

### Piece Coordinates
The `piece_coordinates` module hosts the `ChessPiece` class which is responsible for the translation of the different move coordinate formats across all used applications.

- Converts backend suitable coordinates into motor suitable coordinates

- Converts JSON string dictionaries into integers

- Calculates the numerical difference in X- and Y-coordinate for each move and returns it to the motors

- Converts backend suitable coordinates into AI suitable coordinates and vice versa

- Converts JSON string dictionaries into algebraic notation and vice versa

Additionally it hosts a `fen_visualiser` function which prints the current board state, in the form of a 2D array, into the console.

### Units
Saves all required units, which are used for motor movements.

### Pins
Saves the pin assignment for the connection of Raspberry Pi and motors.

## Requestflow

![requestflow](diagrams/requestflow.png)

The board client connects to the backend server via websockets and hosts a game of chess. Opponents who join the game can make moves on their digital board, which are transmitted to the backend server. The backend server forwards this move data to the board client, which interprets the information. The board client translates this move data into motor inputs that position the electromagnet from its origin location to the starting position of the move, activating the electromagnet. Then, the robot moves the chess piece to its destination and deactivates the electromagnet. Finally, the robot returns the electromagnet to its origin location, completing the move.