import pygame
from env import TaxiEnv  # تأكدي إن env.py موجود

class TaxiGUIReal(TaxiEnv):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.CELL = 100
        self.GRID_SIZE = 5
        self.WIDTH = self.CELL * self.GRID_SIZE
        self.HEIGHT = self.CELL * self.GRID_SIZE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Taxi RL Game")
        
        # Load images
        self.taxi_img = pygame.image.load("taxi.png")
        self.taxi_img = pygame.transform.scale(self.taxi_img, (120, 120))
        
        self.passenger_img = pygame.image.load("man.png")
        self.passenger_img = pygame.transform.scale(self.passenger_img, (80, 80))
        
        self.dest_img = pygame.image.load("locations.png")
        self.dest_img = pygame.transform.scale(self.dest_img, (80, 80))
        
        self.font = pygame.font.SysFont(None, 28)
        self.has_passenger_flag = False
        self.steps = 0
        
        # Restart button
        self.restart_rect = pygame.Rect(self.WIDTH - 110, self.HEIGHT - 40, 100, 30)

    def render(self, show_message=None):
      self.screen.fill((200, 200, 200))  # Grey background
 
    # Draw grid (optional, can be removed for cleaner look)
      for x in range(self.GRID_SIZE):
          for y in range(self.GRID_SIZE):
              pygame.draw.rect(self.screen, (180,180,180), 
                             (y*self.CELL, x*self.CELL, self.CELL, self.CELL), 1)
    
    # Draw destination
      dest_r, dest_c = self.destination
      self.screen.blit(self.dest_img, (dest_c * self.CELL + 10, dest_r * self.CELL + 10))
    
    # Draw passenger if not in taxi
      if not self.has_passenger_flag:
          px, py = self.passenger
          self.screen.blit(self.passenger_img, (py*self.CELL + 10, px*self.CELL + 10))
    
    # Draw taxi
      tx, ty = self.taxi
      self.screen.blit(self.taxi_img, (ty*self.CELL, tx*self.CELL))
    
    # Draw message
      if show_message:
         text = self.font.render(show_message, True, (0,128,0))
         self.screen.blit(text, (10, self.HEIGHT - 30))
    
    # Draw restart button
      pygame.draw.rect(self.screen, (255, 105, 180), self.restart_rect)
      btn_text = self.font.render("New game", True, (255,255,255))
      self.screen.blit(btn_text, (self.restart_rect.x + 5, self.restart_rect.y + 5))

     # 2 pixels under

      pygame.display.flip()


    def check_restart(self, pos):
        return self.restart_rect.collidepoint(pos)

    # Optional: animations
    def pickup_animation(self):
        pass

    def delivered_animation(self):
        pass
