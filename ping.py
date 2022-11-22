import pygame
pygame.init()
WIDTH, HEIGHT = 1280, 620
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
FPS = 60
WHITE = ("grey")
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 9
SCORE_FONT = pygame.font.SysFont("Arial", 50)


class Paddle:
    COLOR = WHITE
    VEL = 10

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y += self.VEL
        else:
            self.y -= self.VEL


class Ball:
    MAX_VEL = 10
    COLOR = "red"

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self,):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win, paddles, ball, left_score, right_score):
    win.fill("#004000")
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, ((WIDTH * (3/4)) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 10, i, 10, HEIGHT//15))
    ball.draw(win)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height/2
                difference_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2)/ball.MAX_VEL
                y_vel = difference_y/reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=False)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + PADDLE_HEIGHT\
            <= HEIGHT:
        left_paddle.move(up=True)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=False)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + PADDLE_HEIGHT\
            <= HEIGHT:
        right_paddle.move(up=True)


def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, (HEIGHT / 2) - (PADDLE_HEIGHT / 2),
                         PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH,
                          (HEIGHT / 2) - (PADDLE_HEIGHT / 2),
                          PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2 - 5, HEIGHT//2, BALL_RADIUS)
    left_score = 0
    right_score = 0

    while run:
        keys = pygame.key.get_pressed()
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

    pygame.quit()


if __name__ == '__main__':
    main()
