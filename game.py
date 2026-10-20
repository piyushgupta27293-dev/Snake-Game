
import turtle
import random
import time

# Game variables
delay = 0.1
score = 0
highest_score = 0
bodies = []
game_running = True

# Screen setup
s = turtle.Screen()
s.title("Snake Game")
s.bgcolor("green")
s.setup(width=600, height=600)
s.tracer(0)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("turtle")
head.color("red")
head.fillcolor("yellow")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 200)

# Scoreboard
sb = turtle.Turtle()
sb.speed(0)
sb.shape("square")
sb.color("blue")
sb.penup()
sb.hideturtle()
sb.goto(0, 260)


def update_score():
    sb.clear()
    sb.write(
        f"Score: {score} | Highest Score: {highest_score}",
        align="center",
        font=("Arial", 16, "bold")
    )


update_score()


# Movement functions
def moveup():
    if head.direction != "down":
        head.direction = "up"


def movedown():
    if head.direction != "up":
        head.direction = "down"


def moveleft():
    if head.direction != "right":
        head.direction = "left"


def moveright():
    if head.direction != "left":
        head.direction = "right"


def movestop():
    head.direction = "stop"


# Move snake
def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)

    elif head.direction == "down":
        head.sety(head.ycor() - 20)

    elif head.direction == "left":
        head.setx(head.xcor() - 20)

    elif head.direction == "right":
        head.setx(head.xcor() + 20)


# Place food at a random position
def place_food():
    while True:
        x = random.randrange(-260, 261, 20)
        y = random.randrange(-240, 241, 20)

        occupied = any(
            body.distance(x, y) < 15 for body in bodies
        )

        if head.distance(x, y) >= 15 and not occupied:
            food.goto(x, y)
            break


# Reset game after collision
def reset_game():
    global score, delay, game_running

    time.sleep(0.5)

    for body in bodies:
        body.hideturtle()

    bodies.clear()

    head.goto(0, 0)
    head.direction = "stop"

    score = 0
    delay = 0.1
    game_running = True

    place_food()
    update_score()


# Keyboard controls
s.listen()
s.onkeypress(moveup, "Up")
s.onkeypress(movedown, "Down")
s.onkeypress(moveleft, "Left")
s.onkeypress(moveright, "Right")
s.onkeypress(movestop, "space")

# Also support W, A, S, D
s.onkeypress(moveup, "w")
s.onkeypress(movedown, "s")
s.onkeypress(moveleft, "a")
s.onkeypress(moveright, "d")


# Main game loop
try:
    while True:
        s.update()

        if game_running:
            # Move body segments from tail to head
            for i in range(len(bodies) - 1, 0, -1):
                x = bodies[i - 1].xcor()
                y = bodies[i - 1].ycor()
                bodies[i].goto(x, y)

            # First segment follows the head
            if bodies:
                bodies[0].goto(head.xcor(), head.ycor())

            move()

            # Border collision: wrap around screen
            if head.xcor() > 290:
                head.setx(-290)
            elif head.xcor() < -290:
                head.setx(290)

            if head.ycor() > 290:
                head.sety(-290)
            elif head.ycor() < -290:
                head.sety(290)

            # Food collision
            if head.distance(food) < 20:
                place_food()

                body = turtle.Turtle()
                body.speed(0)
                body.shape("circle")
                body.color("black")
                body.penup()
                bodies.append(body)

                score += 10
                highest_score = max(highest_score, score)

                delay = max(0.03, delay - 0.002)
                update_score()

            # Self collision
            collision = any(
                body.distance(head) < 10
                for body in bodies
            )

            if collision:
                reset_game()

            time.sleep(delay)

except turtle.Terminator:
    pass
