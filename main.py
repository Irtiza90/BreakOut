from time import sleep
from turtle import Turtle, Screen


class Bar(Turtle):
    def __init__(self, position: tuple[float, float]):
        super().__init__(shape="square")
        self.amount_to_move = 10
        self.border_cords = (400, -400)
        self.start_post = position

        self.color("white")
        self.penup()
        self.turtlesize(stretch_len=6)

        self.goto(self.start_post)

    def move_right(self):
        if (xcor := self.xcor()) < 340:
            self.setx(xcor + 20)

    def move_left(self):
        # The := calls the self.xcor() func and stores it in a variable 'xcor'

        if (xcor := self.xcor()) > -340:
            self.setx(xcor - 20)

    def reset_pos(self):
        self.goto(self.start_post)


class Ball(Turtle):
    def __init__(self):
        super(Ball, self).__init__(shape="circle")
        # Variables
        self.ball_speed = 0.1
        self.x_move, self.y_move = 10, 10

        self.penup()
        self.color("white")


    def bounce(self, direction_to_bounce: str):
        # Change ball's direction in the y axis
        if direction_to_bounce not in ("x", "y"):
            raise ValueError("direction_to_bounce must be 'x' or 'y'")

        # Will change the ball's direction on the x axis
        if direction_to_bounce == "x":
            self.x_move *= -1
            self.ball_speed *= 0.09

        else:
            self.y_move *= -1

    def update_ball(self):
        """Will Be Called Everytime Screen Is Updated, It will just move to the x and y_move variables"""
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move

        self.goto(new_x, new_y)
        # self.speed(self.ball_speed)


    def reset_pos(self):
        self.goto(0, -230)


class Blocks:
    block_count = 0
    all_blocks: list[Turtle] = []

    def generate_blocks(self):
        original_turtle = Turtle(shape="square")
        original_turtle.penup()
        original_turtle.color("lime")
        original_turtle.turtlesize(4, 5)
        original_turtle.speed(10)

        # original_cords = (-360, 260)

        original_turtle.goto(-345, 260)
        original_turtle.setheading(0)

        original_turtles = [original_turtle]

        for i in range(1, 3):  # 2
            t = original_turtle.clone()
            t.sety(original_turtle.ycor() - 120 * i)

            original_turtles.append(t)

        for turtle_ in original_turtles:
            self.all_blocks.append(turtle_)

            for j in range(1, 6):
                cloned_t = turtle_.clone()
                cloned_t.forward(136 * j)

                self.all_blocks.append(cloned_t)


class BreakOutGame:
    # Constants
    screen_dimensions = {"width": 800, "height": 600}
    # border_cords = [(400, 0), (-400, 0), (0, 300)]

    # Variables
    is_game_over = True
    score = 0

    def __init__(self):
        # Making the UI
        self.screen = Screen()
        self.screen.title("Breakout")
        self.screen.bgcolor("black")
        self.screen.setup(**self.screen_dimensions)  # Converting dict to kwargs (width=800, height=600)

        # Sets the screen to not automatically update
        self.screen.tracer(0)

        # Making blocks
        self.blocks = Blocks()
        self.blocks.generate_blocks()

        # Bar
        self.bar = Bar(position=(0, -250))

        # making the ball
        self.ball = Ball()

        self.score_turtle = Turtle(visible=False)
        self.score_turtle.pencolor("white")
        self.score_turtle.penup()
        self.score_turtle.sety(-200)

        self.screen.listen()

        self.screen.onkeypress(self.bar.move_right, key="Right")
        self.screen.onkeypress(self.bar.move_left, key="Left")
        self.screen.onkeypress(self.start_game, key="space")

    def start_game(self):
        if self.is_game_over:
            self.is_game_over = False
            self.start()

    def start(self):
        self.ball.reset_pos()

        while self.is_game_over is False:
            self.screen.update()
            self.ball.update_ball()
            self.score_turtle.clear()

            print(self.ball.xcor(), self.ball.ycor())

            # If ball hit the right/left border
            if self.ball.xcor() < -380 or self.ball.xcor() > 380:
                self.ball.bounce("x")

            # If ball hit the top border
            elif self.ball.ycor() > 280:
                self.ball.bounce("y")

            # If ball Got Below Bar
            elif self.ball.ycor() < self.bar.ycor() - 10:
                self.is_game_over = True

            # Collision with Bar
            elif self.ball.distance(self.bar) < 40 and abs(self.ball.xcor()) > 20:
                self.ball.bounce("y")

            # Checking for Block Collision
            else:
                for block_ind, block in enumerate(self.blocks.all_blocks):
                    if self.ball.distance(block) < 50:
                        block.hideturtle()
                        self.blocks.all_blocks.pop(block_ind)
                        self.ball.bounce("y")

                        # Increasing the score
                        self.score += 10

            sleep(.070)

        else:
            self.ball.reset_pos()
            self.bar.reset_pos()
            self.score_turtle.clear()

            while True:
                if not self.score:
                    self.score_turtle.write("Press Space to Start", align="center", font=("Arial", 10, ''))
                else:
                    self.score_turtle.write(f"Your Score: {self.score}", align="center", font=("arial", 10, ''))

                self.screen.update()


game = BreakOutGame()
game.start()
