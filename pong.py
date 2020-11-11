import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
HALF_PAD_HEIGHT = 40

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_pos = float(HEIGHT / 2)
paddle2_pos = float(HEIGHT / 2)
paddle1_vel = 0.0
paddle2_vel = 0.0
score1 = 0
score2 = 0

# helper function that spawns a ball by updating the
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]

    # start ball on the left side or on the right side
    if direction:
        ball_vel = [random.randrange (120, 240) // 60, -random.randrange (60, 180) // 60]
    else:
        ball_vel = [-random.randrange (120, 240) // 60, -random.randrange (60, 180) // 60]

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints

    score1 = 0
    score2 = 0

    paddle1_pos = float(HEIGHT / 2)
    paddle2_pos = float(HEIGHT / 2)
    paddle1_vel = 0.0
    paddle2_vel = 0.0

    if not random.randint(0, 1):
        start_side = False
    else:
        start_side = True
    spawn_ball(start_side)

# define event handlers
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    if paddle1_pos - HALF_PAD_HEIGHT < 0:
        paddle1_pos = HALF_PAD_HEIGHT
    if paddle1_pos + HALF_PAD_HEIGHT > (HEIGHT - 1):
        paddle1_pos = (HEIGHT - 1) - HALF_PAD_HEIGHT

    paddle2_pos += paddle2_vel
    if paddle2_pos - HALF_PAD_HEIGHT < 0:
        paddle2_pos = HALF_PAD_HEIGHT
    if paddle2_pos + HALF_PAD_HEIGHT > (HEIGHT - 1):
        paddle2_pos = (HEIGHT - 1) - HALF_PAD_HEIGHT

    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # draw paddles
    c.draw_polygon([(0, paddle1_pos - HALF_PAD_HEIGHT), (PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT),
                    (PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), (0, paddle1_pos + HALF_PAD_HEIGHT)],
                   1, "White", "White")
    c.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), (WIDTH, paddle2_pos - HALF_PAD_HEIGHT),
                    (WIDTH, paddle2_pos + HALF_PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)],
                   1, "White", "White")

    # update ball position
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] *= -1

    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] > paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            spawn_ball(True)

    if ball_pos[0] >= (WIDTH - 1) - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] > paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            spawn_ball(False)

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]


    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "Green")

    c.draw_text(str(score1), (WIDTH / 4 - 10, 50), 40, "Red")
    c.draw_text(str(score2), (WIDTH / 4 * 3 - 10, 50), 40, "Blue")

def keydown(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -12

    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 12

    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -12

    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 12

def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0

    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0


frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart game", new_game, 200)


frame.start()
new_game()
