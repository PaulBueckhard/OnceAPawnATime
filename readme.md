How to run the board client:
1. Make sure you pip installed the requirements (`$ pip install -r requirements.txt`)
2. Run client.py
3. answer with yes/any whether you want to play against AI
4. answer with yes/any whether you want board visualisation
5. You get the codes plus a link that you can click

After 5. you get directed to the website and automatically connected to a game. In most cases it will not connect the first time and but the second time you will.
If you have answered with yes on the AI question you will play against the algorithm. If one of you wins the program will crash tho (still have to fix that).
If you have answered yes on the visualitsion question in the terminal you will get a little board in form of lists (useful if you send the link to other people and can't actually see the board).
To end the program simply leave the game on the website or press ctrl+c in the terminal.

`stepper_motor_test.py` is a script that makes the motor move back and forth a predetermined amount until indefinitely until interrupted.

`motor_move.py` contains functions that move the motor with parameters given on call.

If motor is moved `enable` pin needs to be set to HIGH after the movement is finished `GPIO.output(EN, GPIO.HIGH)`. This is especially important if the function is interrupted.
We don't yet have the endstops implemented, so it's safest to only run the motor through funcitons that have a keyboard interrupt.