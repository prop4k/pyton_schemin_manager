import tkinter as tk
from tkinter import ttk
import pygame
import random
import sys
import math

# ==========================================
# КЛАСС ЗАДАЧИ (Задача 2 и 3)
# ==========================================
class TaskBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 40
        self.task_id = random.randint(1000, 9999)
        self.target = None
        self.speed = 4 # Плавность (скорость) полета

    def set_target(self, target_x, target_y):
        self.target = (target_x, target_y)

    def update(self):
        # Логика плавного перемещения к цели (Задача 3)
        if self.target:
            tx, ty = self.target
            # Вычисляем расстояние по X и Y
            dx = tx - self.x
            dy = ty - self.y
            distance = math.hypot(dx, dy)
            
            # Если почти долетели - фиксируем прибытие
            if distance < self.speed:
                self.x, self.y = tx, ty
                return True # Сигнал, что цель достигнута
            else:
                # Движемся по вектору направления
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        return False

    def draw(self, screen, font):
        # Отрисовка прямоугольника и текста ID
        rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        pygame.draw.rect(screen, (70, 130, 180), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        
        text_surf = font.render(f"ID:{self.task_id}", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.x, self.y))
        screen.blit(text_surf, text_rect)

# ==========================================
# ГЛАВНОЕ ПРИЛОЖЕНИЕ (Задача 1 и 4)
# ==========================================
class App:
    def __init__(self):
        # 1. Настройка Tkinter (Панель управления)
        self.root = tk.Tk()
        self.root.title("Диспетчер задач")
        self.root.geometry("300x150")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Управление ядрами")
        
        self.btn1 = tk.Button(self.tab1, text="Направить на Ядро 1", command=self.send_to_core1)
        self.btn1.pack(pady=10, fill=tk.X, padx=20)
        
        self.btn2 = tk.Button(self.tab1, text="Направить на Ядро 2", command=self.send_to_core2)
        self.btn2.pack(pady=10, fill=tk.X, padx=20)

        # 2. Настройка Pygame (Визуализация)
        pygame.init()
        self.screen_w = 600
        self.screen_h = 400
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Распределитель задач (Визуализация)")
        
        self.font = pygame.font.SysFont("Arial", 16)
        self.big_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Координаты ядер (левый и правый верхние углы)
        self.core1_pos = (120, 80)
        self.core2_pos = (480, 80)
        
        # Счетчики выполненных задач (Задача 4)
        self.core1_score = 0
        self.core2_score = 0
        
        # Создаем первую задачу
        self.spawn_task()

    def spawn_task(self):
        # Появление в центре снизу
        self.current_task = TaskBlock(self.screen_w // 2, self.screen_h - 100)
        # Разблокируем кнопки
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)

    def send_to_core1(self):
        if self.current_task and not self.current_task.target:
            self.current_task.set_target(*self.core1_pos)
            # Блокируем кнопки, пока блок летит
            self.btn1.config(state=tk.DISABLED)
            self.btn2.config(state=tk.DISABLED)

    def send_to_core2(self):
        if self.current_task and not self.current_task.target:
            self.current_task.set_target(*self.core2_pos)
            self.btn1.config(state=tk.DISABLED)
            self.btn2.config(state=tk.DISABLED)

    def on_closing(self):
        self.running = False
        self.root.destroy()

    def draw_core(self, pos, name, score):
        # Рисуем круглое ядро процессора
        pygame.draw.circle(self.screen, (50, 180, 50), pos, 50)
        pygame.draw.circle(self.screen, (255, 255, 255), pos, 50, 3)
        
        # Название ядра
        name_surf = self.big_font.render(name, True, (255, 255, 255))
        name_rect = name_surf.get_rect(center=(pos[0], pos[1] - 15))
        self.screen.blit(name_surf, name_rect)
        
        # Счетчик задач
        score_surf = self.font.render(f"Выполнено: {score}", True, (255, 255, 0))
        score_rect = score_surf.get_rect(center=(pos[0], pos[1] + 15))
        self.screen.blit(score_surf, score_rect)

    def run(self):
        # Главный цикл программы (обновляет и Tkinter, и Pygame)
        while self.running:
            # Обработка закрытия окна Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.on_closing()
                    
            if not self.running:
                break

            # Логика движения и проверки прибытия
            if self.current_task:
                reached = self.current_task.update()
                if reached:
                    # Задача 4: Увеличиваем счетчики при прилете
                    if self.current_task.target == self.core1_pos:
                        self.core1_score += 1
                    elif self.current_task.target == self.core2_pos:
                        self.core2_score += 1
                    # Уничтожаем старую задачу и спавним новую
                    self.spawn_task()

            # Отрисовка элементов в Pygame
            self.screen.fill((40, 40, 40)) # Темно-серый фон
            self.draw_core(self.core1_pos, "ЯДРО 1", self.core1_score)
            self.draw_core(self.core2_pos, "ЯДРО 2", self.core2_score)
            
            if self.current_task:
                self.current_task.draw(self.screen, self.font)
            
            pygame.display.flip()
            self.clock.tick(60) # Ограничение 60 кадров в секунду
            
            # Обновление окна Tkinter
            try:
                self.root.update()
            except tk.TclError:
                self.running = False

        pygame.quit()
        sys.exit()

# Точка входа
if __name__ == "__main__":
    app = App()
    app.run()