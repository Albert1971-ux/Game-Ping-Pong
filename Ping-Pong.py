import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (0, 120, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Состояния игры
MENU = 0
GAME = 1
PAUSE = 2
GAME_OVER = 3

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

# Создание часов для контроля FPS
clock = pygame.time.Clock()

# Создание ракеток
player1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Создание мяча
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)
ball_speed_x = 0
ball_speed_y = 0

# Счет
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Текущее состояние игры
game_state = MENU


# Функция для создания кнопки
def draw_button(rect, text, text_color=WHITE, button_color=BLUE, hover_color=GREEN):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
        is_hover = True
    else:
        pygame.draw.rect(screen, button_color, rect)
        is_hover = False

    pygame.draw.rect(screen, WHITE, rect, 2)  # Белая граница кнопки

    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

    return is_hover


# Функция для сброса мяча
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = 0
    ball_speed_y = 0


# Функция для старта мяча
def start_ball():
    global ball_speed_x, ball_speed_y
    ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))


# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == MENU:
                if start_button_hover:
                    game_state = GAME
                    player1_score = 0
                    player2_score = 0
                    reset_ball()
                    start_ball()
                elif exit_button_hover:
                    running = False

            elif game_state == GAME:
                if pause_button_hover:
                    game_state = PAUSE

            elif game_state == PAUSE:
                if resume_button_hover:
                    game_state = GAME
                elif menu_button_hover:
                    game_state = MENU

            elif game_state == GAME_OVER:
                if restart_button_hover:
                    game_state = GAME
                    player1_score = 0
                    player2_score = 0
                    reset_ball()
                    start_ball()
                elif menu_button_hover:
                    game_state = MENU

    # Заливка экрана
    screen.fill(BLACK)

    # Меню
    if game_state == MENU:
        # Заголовок игры
        title_text = large_font.render("ПИНГ-ПОНГ", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        # Кнопка старта
        start_button = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
        start_button_hover = draw_button(start_button, "Начать игру")

        # Кнопка выхода
        exit_button = pygame.Rect(WIDTH // 2 - 100, 320, 200, 50)
        exit_button_hover = draw_button(exit_button, "Выход", button_color=RED)

        # Инструкции
        instructions = [
            "Управление:",
            "Используйте мышь, чтобы двигать левую ракетку",
            "Цель: отбивайте мяч, набирайте очки!"
        ]

        for i, line in enumerate(instructions):
            instruction_text = font.render(line, True, GRAY)
            screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 400 + i * 30))

    # Игровой процесс
    elif game_state == GAME:
        # Управление первой ракеткой с помощью мыши
        mouse_y = pygame.mouse.get_pos()[1]
        # Ограничиваем движение ракетки в пределах экрана
        player1.y = min(max(mouse_y - PADDLE_HEIGHT // 2, 0), HEIGHT - PADDLE_HEIGHT)

        # Простой ИИ для второй ракетки
        if ball.centery > player2.centery + PADDLE_HEIGHT // 4:
            player2.y += min(PADDLE_SPEED, ball.centery - player2.centery - PADDLE_HEIGHT // 4)
        elif ball.centery < player2.centery - PADDLE_HEIGHT // 4:
            player2.y -= min(PADDLE_SPEED, player2.centery - PADDLE_HEIGHT // 4 - ball.centery)

        player2.y = min(max(player2.y, 0), HEIGHT - PADDLE_HEIGHT)

        # Движение мяча
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Отскок мяча от верхней и нижней границы
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Отскок мяча от ракеток
        if ball.colliderect(player1):
            ball_speed_x = abs(ball_speed_x)  # Мяч движется вправо
            # Изменение угла в зависимости от места попадания в ракетку
            ball_speed_y = (ball.centery - player1.centery) / (PADDLE_HEIGHT / 2) * BALL_SPEED_Y

        if ball.colliderect(player2):
            ball_speed_x = -abs(ball_speed_x)  # Мяч движется влево
            # Изменение угла в зависимости от места попадания в ракетку
            ball_speed_y = (ball.centery - player2.centery) / (PADDLE_HEIGHT / 2) * BALL_SPEED_Y

        # Проверка на гол
        if ball.left <= 0:
            player2_score += 1
            reset_ball()
            # Автоматический запуск мяча через короткое время
            pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1 секунда
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))

        if ball.right >= WIDTH:
            player1_score += 1
            reset_ball()
            # Автоматический запуск мяча через короткое время
            pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1 секунда
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))

        # Обработка событий таймера
        for event in pygame.event.get(pygame.USEREVENT):
            start_ball()
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Отключаем таймер

        # Проверка на конец игры
        if player1_score >= 10 or player2_score >= 10:
            game_state = GAME_OVER

        # Отрисовка ракеток и мяча
        pygame.draw.rect(screen, WHITE, player1)
        pygame.draw.rect(screen, WHITE, player2)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Отрисовка центральной линии
        for y in range(0, HEIGHT, 30):
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 1, y, 2, 15))

        # Отрисовка счета
        score_text1 = font.render(str(player1_score), True, WHITE)
        score_text2 = font.render(str(player2_score), True, WHITE)
        screen.blit(score_text1, (WIDTH // 4, 20))
        screen.blit(score_text2, (3 * WIDTH // 4, 20))

        # Кнопка паузы
        pause_button = pygame.Rect(WIDTH - 100, 20, 80, 30)
        pause_button_hover = draw_button(pause_button, "Пауза", button_color=GRAY)

    # Пауза
    elif game_state == PAUSE:
        # Полупрозрачный фон
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Текст паузы
        pause_text = large_font.render("ПАУЗА", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(pause_text, pause_rect)

        # Кнопка продолжения
        resume_button = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
        resume_button_hover = draw_button(resume_button, "Продолжить")

        # Кнопка возврата в меню
        menu_button = pygame.Rect(WIDTH // 2 - 100, 320, 200, 50)
        menu_button_hover = draw_button(menu_button, "В меню", button_color=GRAY)

    # Конец игры
    elif game_state == GAME_OVER:
        # Полупрозрачный фон
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Определение победителя
        winner = "Игрок 1" if player1_score >= 10 else "Компьютер"

        # Текст конца игры
        game_over_text = large_font.render("ИГРА ОКОНЧЕНА", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, 120))
        screen.blit(game_over_text, game_over_rect)

        # Текст победителя
        winner_text = font.render(f"Победитель: {winner}", True, WHITE)
        winner_rect = winner_text.get_rect(center=(WIDTH // 2, 180))
        screen.blit(winner_text, winner_rect)

        # Отображение счета
        score_text = font.render(f"Счет: {player1_score} - {player2_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 220))
        screen.blit(score_text, score_rect)

        # Кнопка рестарта
        restart_button = pygame.Rect(WIDTH // 2 - 100, 280, 200, 50)
        restart_button_hover = draw_button(restart_button, "Играть снова", button_color=GREEN)

        # Кнопка возврата в меню
        menu_button = pygame.Rect(WIDTH // 2 - 100, 350, 200, 50)
        menu_button_hover = draw_button(menu_button, "В меню", button_color=BLUE)

    # Обновление экрана
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(FPS)

# Завершение работы
pygame.quit()
sys.exit()
