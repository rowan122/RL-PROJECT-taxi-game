# env_gui_emoji.py
import pygame
from env import TaxiEnv

CELL = 100
SIZE = 5 * CELL

class TaxiGUI(TaxiEnv):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((SIZE, SIZE + 50))  # مساحة للنص
        pygame.display.set_caption("Taxi RL Game")
        self.font = pygame.font.SysFont("Arial", 24)

        # تحميل الصور/Emojis كـ Surface
        self.taxi_img = pygame.font.Font(None, 72).render("🚕", True, (0,0,0))
        self.passenger_img = pygame.font.Font(None, 72).render("🧍", True, (0,0,0))
        self.dest_img = pygame.font.Font(None, 72).render("🏁", True, (0,0,0))

    def render(self, step=0, reward=0):
        self.screen.fill((255, 255, 255))
        
        # رسم الشبكة
        for x in range(5):
            for y in range(5):
                pygame.draw.rect(self.screen, (200,200,200), (y*CELL, x*CELL, CELL, CELL), 1)

        # رسم الوجهة
        dest_r, dest_c = self.destination
        self.screen.blit(self.dest_img, (dest_c*CELL+10, dest_r*CELL-10))

        # رسم الراكب إذا موجود
        if not self.has_passenger:
            pass_r, pass_c = self.passenger
            self.screen.blit(self.passenger_img, (pass_c*CELL+10, pass_r*CELL-10))

        # رسم التاكسي
        taxi_r, taxi_c = self.taxi
        self.screen.blit(self.taxi_img, (taxi_c*CELL+10, taxi_r*CELL-10))

        # كتابة step و reward
        text_surface = self.font.render(f"Step: {step} | Total Reward: {reward}", True, (0,0,0))
        self.screen.blit(text_surface, (10, SIZE + 10))

        pygame.display.flip()
