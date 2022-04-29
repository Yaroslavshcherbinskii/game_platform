# connect graphics library
from tkinter import *
# connect modules that are responsible for time and random numbers
import random
import time

# create a new object - a window with a playing field.
# In our case, the window variable is called tk, and we made it from the
# Tk () class - it is in the graphics library

tk = Tk()
# make the title of the window - "game_platform"  using the title property of the object
tk.title('game_platform')
# prohibit resizing the window, for this we use the "resizable" property
tk.resizable(0, 0)
# put our game window above the rest of the windows on the computer so that other windows cannot obscure it
tk.wm_attributes('-topmost', 1)
# create a new canvas - 400 by 500 pixels, where we will draw the game
canvas = Canvas(tk, width=500, height=400, highlightthickness=0)
# tell the canvas that each visible element will have its own separate coordinates
canvas.pack()
# update the canvas window
tk.update()


# Describe the class Ball, which will be responsible for the ball
class Ball:
    # constructor - it is called when a new object is created based on this class
    def __init__(self, canvas, paddle, score, color):
        # set the object parameters that are passed to us in brackets at the time of creation
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        # the color was needed so that we painted over the entire ball with it
        # a new id property appears here, which stores the internal name of the ball
        # and with the create_oval command we create a circle with a radius of 15 pixels
        # and fill it with the desired color
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        # place the ball at the point with coordinates 245,100
        self.canvas.move(self.id, 245, 100)
        # set a list of possible directions to start
        starts = [-2, -1, 1, 2]
        # shuffle it
        random.shuffle(starts)
        # select the first one from the mixed one - this will be the ball's motion vector
        self.x = starts[0]
        # at the very beginning it always falls down, so we decrease the value along the y axis
        self.y = -2
        # the balloon learns its height and width
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        # property that controls whether the ball has reached the bottom or not.
        # Until reached, the value will be False
        self.hit_bottom = False
        # process the touch of the platform, for this we get 4 coordinates of the ball
    # in the pos variable (upper left and lower right points)
    def hit_paddle(self, pos):
          # get platform coordinates via "paddle" object (platform)
          paddle_pos = self.canvas.coords(self.paddle.id)
          # if touch coordinates match platform coordinates
          if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
              if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]: # increase the score (the handler for this event will be described below)
                 self.score.hit()
                 # return a label that we have successfully touched
                 return True
          # return False - there was no touch
          return False
     # process the drawing of the ball
    def draw(self): # move the ball to the given x and y coordinates
         self.canvas.move(self.id, self.x, self.y)
         # remember the new coordinates of the ball
         pos = self.canvas.coords(self.id)
         # if the ball falls from above
         if pos[1] <= 0:
             # set the fall in the next step = 2
             self.y = 2
         # if the bottom right corner of the ball touches the bottom
         if pos[3] >= self.canvas_height:
             # mark it in a separate variable
             self.hit_bottom = True
             # print message and score
             canvas.create_text(250, 120, text='You lose', font=('Courier', 30), fill='red')
         # if there was a platform touch
         if self.hit_paddle(pos)==True:
             # send the ball up
             self.y = -2
         # if touched the left wall
         if pos[0]  <= 0:
             # move right
             self.x = 2
         # if you touched the right wall
         if pos[2] >= self.canvas_width:
             #move left
             self.x = -2
# Describe the "Paddle" class, which is responsible for the platform
class Paddle:
    # конструктор
    def __init__(self, canvas, color):
        # "canvas" means the platform will be drawn on our original canvas
        self.canvas = canvas
        # create a rectangular platform 10 by 100 pixels,
        # paint it with the selected color and get its internal name
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        # set the list of possible starting positions of the platform
        start_1 = [40, 60, 90, 120, 150, 180, 200]
        # shuffle them
        random.shuffle(start_1)
        # select the first of the shuffled
        self.starting_point_x = start_1[0]
        # move the platform to the starting position
        self.canvas.move(self.id, self.starting_point_x, 300)
        # while the platform is not moving anywhere, so there is no change in the x-axis
        self.x = 0
        # the platform recognizes its width
        self.canvas_width = self.canvas.winfo_width()
        # set the click handler
        # if the right arrow is pressed, the turn_right() method is executed
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        # if the arrow is left - turn_left()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        # until the game starts, so wait
        self.started = False
        # as soon as the player presses Enter, everything starts
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)
    # move right
    def turn_right(self, event):
        # will shift to the right by 2 pixels along the x-axis
        self.x = 2

    # move left
    def turn_left(self, event):
        # will shift to the left by 2 pixels along the x-axis
        self.x = -2

    # Start game
    def start_game(self, event):
        # change the value of the variable that is responsible for the start
        self.started = True

    # method that is responsible for platform movement
    def draw(self):
        # shift our platform by the given number of pixels
        self.canvas.move(self.id, self.x, 0)
        # get canvas coordinates
        pos = self.canvas.coords(self.id)
        # if we hit the left border
        if pos[0] <= 0:
            #stop
            self.x = 0
        # if we hit the right border
        elif pos[2] >= self.canvas_width:
            #stop
            self.x = 0

# Describe the "Score" class, which is responsible for displaying scores
class Score:
    #constructor
    def __init__(self, canvas, color):
        # at the very beginning, the count is zero
        self.score = 0
        # we will use our canvas
        self.canvas = canvas
        # create an inscription that shows the current score, make it need colors
        # and remember the internal name of this inscription
        self.id = canvas.create_text(450, 10, text=self.score, font=('Courier', 15), fill=color)

    # handle platform touch
    def hit(self):
        # increment the count by one
        self.score += 2
        # write a new score value
        self.canvas.itemconfig(self.id, text=self.score)

# create an object - green score
score = Score(canvas, 'black')
# create an object - a white platform
paddle = Paddle(canvas, 'Blue')
# create an object - a red ball
ball = Ball(canvas, paddle, score, 'red')
# until the ball touches the bottom
while not ball.hit_bottom:
    # if the game has started and the platform can move
    if paddle.started == True:
        # move the ball
        ball.draw()
        # move the platform
        paddle.draw()
    # update our playfield so that whatever needs to be finished drawing
    tk.update_idletasks()
    # update the playing field and make sure everything that needs to be done gets done
    tk.update()
    # freeze for one hundredth of a second so that the movement of the elements looks smooth
    time.sleep(0.01)
    # if the program has reached this point, then the ball has touched the bottom.
    # We wait 3 seconds until the player reads the final inscription, and end the game.
time.sleep(3)





