import turtle
import colorsys

# Setup screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Colourful Kolam Design")

# Setup turtle
pen = turtle.Turtle()
pen.speed(0)  # fastest
pen.width(2)

# Generate colours using HSV
num_colors = 36
colors = []
for i in range(num_colors):
    hue = i / num_colors
    col = colorsys.hsv_to_rgb(hue, 1, 1)  # (r,g,b)
    colors.append(col)

# Kolam Design
def draw_kolam(radius, petals):
    for j in range(petals):
        pen.color(colors[j % num_colors])
        pen.circle(radius)
        pen.right(360 / petals)

# Main pattern
pen.penup()
pen.goto(0, -200)   # position start
pen.pendown()

for r in range(6):  # layers
    draw_kolam(50 + r*20, 12 + r*6)
    pen.right(10)

pen.hideturtle()
turtle.done()


































