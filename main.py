import pygame
import random
import sys
import arabic_reshaper
from bidi.algorithm import get_display

pygame.init()


def ar(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

WIDTH, HEIGHT = 600, 800
GAME_H = 580
CELL = 20
COLS = WIDTH // CELL
ROWS = GAME_H // CELL
FPS = 7

BLACK   = (10,  10,  10)
BG      = (15,  15,  15)
GRID_C  = (22,  22,  22)
SNAKE_H = (120, 220,  80)
SNAKE_B = ( 80, 170,  50)
SNAKE_E = (240, 240, 240)
APPLE_G = ( 60, 160,  40)
APPLE_S = ( 80,  60,  30)
WHITE   = (240, 240, 240)
GRAY    = ( 80,  80,  80)
DGRAY   = ( 30,  30,  30)
YELLOW  = (255, 220,  50)
BTN_BG  = ( 50,  50,  50)
BTN_HL  = ( 70, 160,  70)
START_C = ( 50, 170,  50)
START_H = ( 80, 220,  80)
SECRET_OFF = ( 80,  40, 100)
SECRET_ON  = (200,  80, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

ARABIC_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ARABIC_FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

font_big   = pygame.font.Font(ARABIC_FONT, 52)
font_med   = pygame.font.Font(ARABIC_FONT, 26)
font_small = pygame.font.Font(ARABIC_FONT_REG, 18)
font_btn   = pygame.font.Font(ARABIC_FONT, 26)
font_start = pygame.font.Font(ARABIC_FONT, 24)
font_lose  = pygame.font.Font(ARABIC_FONT, 20)

PAD_CX  = WIDTH // 2
PAD_CY  = GAME_H + 110
BTN_R   = 44
BTN_GAP = 66

DPAD = {
    "up":    (PAD_CX,           PAD_CY - BTN_GAP),
    "down":  (PAD_CX,           PAD_CY + BTN_GAP),
    "left":  (PAD_CX - BTN_GAP, PAD_CY),
    "right": (PAD_CX + BTN_GAP, PAD_CY),
}
DPAD_DIRS = {
    "up":    (0, -1),
    "down":  (0,  1),
    "left":  (-1, 0),
    "right": (1,  0),
}
DPAD_LABELS = {"up": "▲", "down": "▼", "left": "◄", "right": "►"}

SECRET_RECT = pygame.Rect(WIDTH - 90, 6, 82, 30)


def draw_apple(surface, col, row, fleeing=False):
    cx = col * CELL + CELL // 2
    cy = row * CELL + CELL // 2
    r  = CELL // 2 - 1
    body_color = (220, 55, 55) if not fleeing else (255, 140, 0)
    shine_color = (245, 120, 120) if not fleeing else (255, 200, 100)
    dark_color  = (155, 20,  20) if not fleeing else (195, 85,  0)
    pygame.draw.circle(surface, body_color, (cx, cy + 1), r)
    pygame.draw.circle(surface, shine_color, (cx - r // 3, cy - r // 3), r // 3)
    pygame.draw.circle(surface, dark_color, (cx, cy - r + 2), 3)
    pygame.draw.line(surface, APPLE_S, (cx, cy - r + 2), (cx + 3, cy - r - 4), 2)
    leaf_pts = [
        (cx + 2, cy - r - 2),
        (cx + 8, cy - r - 8),
        (cx + 9, cy - r - 1),
    ]
    pygame.draw.polygon(surface, APPLE_G, leaf_pts)


def draw_snake_nokia(surface, snake):
    for i, seg in enumerate(snake):
        col, row = seg
        x = col * CELL
        y = row * CELL
        pad = 1
        rect = pygame.Rect(x + pad, y + pad, CELL - pad * 2, CELL - pad * 2)
        if i == 0:
            pygame.draw.rect(surface, SNAKE_H, rect, border_radius=5)
            if len(snake) > 1:
                dx = snake[0][0] - snake[1][0]
                dy = snake[0][1] - snake[1][1]
            else:
                dx, dy = 1, 0
            if dx == 1:
                e1 = (x + CELL - 5, y + 4)
                e2 = (x + CELL - 5, y + CELL - 5)
            elif dx == -1:
                e1 = (x + 5, y + 4)
                e2 = (x + 5, y + CELL - 5)
            elif dy == -1:
                e1 = (x + 4, y + 5)
                e2 = (x + CELL - 5, y + 5)
            else:
                e1 = (x + 4, y + CELL - 5)
                e2 = (x + CELL - 5, y + CELL - 5)
            pygame.draw.circle(surface, BLACK, e1, 2)
            pygame.draw.circle(surface, SNAKE_E, e1, 1)
            pygame.draw.circle(surface, BLACK, e2, 2)
            pygame.draw.circle(surface, SNAKE_E, e2, 1)
        else:
            pygame.draw.rect(surface, SNAKE_B, rect, border_radius=3)
            inner = rect.inflate(-4, -4)
            pygame.draw.rect(surface, (100, 190, 70), inner, 1, border_radius=2)


def draw_grid(surface):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(surface, GRID_C, (c * CELL, r * CELL, CELL, CELL), 1)


def draw_dpad(surface, pressed=None):
    pygame.draw.rect(surface, DGRAY, (0, GAME_H, WIDTH, HEIGHT - GAME_H))
    for name, (cx, cy) in DPAD.items():
        color = BTN_HL if name == pressed else BTN_BG
        pygame.draw.circle(surface, color, (cx, cy), BTN_R)
        pygame.draw.circle(surface, GRAY, (cx, cy), BTN_R, 2)
        lbl = font_btn.render(DPAD_LABELS[name], True, WHITE)
        surface.blit(lbl, lbl.get_rect(center=(cx, cy)))


def draw_secret_button(surface, crazy_mode):
    color = SECRET_ON if crazy_mode else SECRET_OFF
    pygame.draw.rect(surface, color, SECRET_RECT, border_radius=6)
    pygame.draw.rect(surface, WHITE, SECRET_RECT, 1, border_radius=6)
    label = "CRAZY ON" if crazy_mode else "CRAZY OFF"
    lbl = font_small.render(label, True, WHITE)
    surface.blit(lbl, lbl.get_rect(center=SECRET_RECT.center))


def draw_start_button(surface, hovered=False):
    bw, bh = 200, 52
    bx = WIDTH // 2 - bw // 2
    by = GAME_H // 2 + 70
    rect = pygame.Rect(bx, by, bw, bh)
    color = START_H if hovered else START_C
    pygame.draw.rect(surface, color, rect, border_radius=12)
    pygame.draw.rect(surface, (30, 100, 30), rect, 2, border_radius=12)
    lbl = font_start.render(">  START", True, WHITE)
    surface.blit(lbl, lbl.get_rect(center=rect.center))
    return rect


def btn_rect_get():
    bw, bh = 200, 52
    bx = WIDTH // 2 - bw // 2
    by = GAME_H // 2 + 70
    return pygame.Rect(bx, by, bw, bh)


def hit_dpad(pos):
    for name, (cx, cy) in DPAD.items():
        dx, dy = pos[0] - cx, pos[1] - cy
        if dx * dx + dy * dy <= BTN_R * BTN_R:
            return name
    return None


def random_food(snake):
    occupied = set(snake)
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in occupied:
            return pos


def apple_flee(apple, snake_head, snake):
    ax, ay = apple
    hx, hy = snake_head
    occupied = set(snake)
    candidates = []
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = ax + dx, ay + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in occupied:
            dist = (nx - hx) ** 2 + (ny - hy) ** 2
            candidates.append((dist, (nx, ny)))
    if not candidates:
        return apple
    candidates.sort(reverse=True)
    return candidates[0][1]


def run_game(crazy_mode=False):
    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    next_dir  = direction
    food = random_food(snake)
    score = 0
    touch_start = {}
    pressed_btn = None

    while True:
        clock.tick(FPS)
        pressed_btn = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    next_dir = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    next_dir = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    next_dir = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    next_dir = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    return score, True
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn = hit_dpad(event.pos)
                if btn:
                    pressed_btn = btn
                    d = DPAD_DIRS[btn]
                    opp = (-direction[0], -direction[1])
                    if d != opp:
                        next_dir = d
            if event.type == pygame.FINGERDOWN:
                fx, fy = event.x * WIDTH, event.y * HEIGHT
                touch_start[event.finger_id] = (fx, fy)
                btn = hit_dpad((fx, fy))
                if btn:
                    pressed_btn = btn
                    d = DPAD_DIRS[btn]
                    opp = (-direction[0], -direction[1])
                    if d != opp:
                        next_dir = d
            if event.type == pygame.FINGERUP:
                fx, fy = event.x * WIDTH, event.y * HEIGHT
                if event.finger_id in touch_start:
                    sx, sy = touch_start.pop(event.finger_id)
                    dx, dy = fx - sx, fy - sy
                    if sy < GAME_H and (abs(dx) > 30 or abs(dy) > 30):
                        if abs(dx) >= abs(dy):
                            d = (1, 0) if dx > 0 else (-1, 0)
                        else:
                            d = (0, 1) if dy > 0 else (0, -1)
                        opp = (-direction[0], -direction[1])
                        if d != opp:
                            next_dir = d

        direction = next_dir
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (head[0] < 0 or head[0] >= COLS or
                head[1] < 0 or head[1] >= ROWS or
                head in snake):
            return score, False

        if crazy_mode:
            food = apple_flee(food, snake[0], snake)

        snake.insert(0, head)

        if head == food:
            score += 10
            food = random_food(snake)
        else:
            snake.pop()

        screen.fill(BG)
        draw_grid(screen)
        draw_snake_nokia(screen, snake)
        draw_apple(screen, food[0], food[1], fleeing=crazy_mode)

        score_surf = font_small.render(ar(f"رصيد الستر: {score}"), True, YELLOW)
        screen.blit(score_surf, (8, 6))

        draw_dpad(screen, pressed=pressed_btn)
        pygame.display.flip()


def show_start_screen():
    crazy_mode = False
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(BG)
        draw_grid(screen)
        t = font_big.render("SNAKE", True, SNAKE_H)
        screen.blit(t, t.get_rect(center=(WIDTH // 2, GAME_H // 2 - 80)))
        h = font_small.render(ar("اسحب او اضغط الاسهم للتحريك"), True, GRAY)
        screen.blit(h, h.get_rect(center=(WIDTH // 2, GAME_H // 2 - 20)))
        draw_apple(screen, COLS // 2, ROWS // 2 + 1, fleeing=crazy_mode)
        btn_rect = draw_start_button(screen, hovered=btn_rect_get().collidepoint(mx, my))
        draw_secret_button(screen, crazy_mode)
        draw_dpad(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return crazy_mode
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    return crazy_mode
                if SECRET_RECT.collidepoint(event.pos):
                    crazy_mode = not crazy_mode
            if event.type == pygame.FINGERUP:
                fx, fy = event.x * WIDTH, event.y * HEIGHT
                if btn_rect.collidepoint((fx, fy)):
                    return crazy_mode
                if SECRET_RECT.collidepoint((fx, fy)):
                    crazy_mode = not crazy_mode
        clock.tick(30)


def show_game_over(score):
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(BG)
        draw_grid(screen)
        t = font_big.render("GAME OVER", True, (220, 60, 60))
        screen.blit(t, t.get_rect(center=(WIDTH // 2, GAME_H // 2 - 100)))
        insult = font_med.render(ar("هههههه خسرت يقحبة"), True, (255, 200, 0))
        screen.blit(insult, insult.get_rect(center=(WIDTH // 2, GAME_H // 2 - 30)))
        s = font_med.render(ar(f"رصيد الستر: {score}"), True, WHITE)
        screen.blit(s, s.get_rect(center=(WIDTH // 2, GAME_H // 2 + 20)))
        btn_rect = draw_start_button(screen, hovered=btn_rect_get().collidepoint(mx, my))
        draw_dpad(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    return
            if event.type == pygame.FINGERUP:
                fx, fy = event.x * WIDTH, event.y * HEIGHT
                if btn_rect.collidepoint((fx, fy)):
                    return
        clock.tick(30)


def main():
    while True:
        crazy_mode = show_start_screen()
        score, quit_early = run_game(crazy_mode=crazy_mode)
        if not quit_early:
            show_game_over(score)


if __name__ == "__main__":
    main()
