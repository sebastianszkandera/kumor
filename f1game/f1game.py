import pygame
import random
import math

def f1car():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("F1 Car Game")
    clock = pygame.time.Clock()
    
    # Car position and speed
    car_x = 400
    car_y = 500
    car_speed_x = 0
    car_speed_y = 0
    base_speed = 5
    drs_multiplier = 1.5
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Controls with WASD
        keys = pygame.key.get_pressed()
        car_speed_x = 0
        car_speed_y = 0
        
        if keys[pygame.K_a]:
            car_speed_x = -base_speed
        if keys[pygame.K_d]:
            car_speed_x = base_speed
        if keys[pygame.K_w]:
            car_speed_y = -base_speed
        if keys[pygame.K_s]:
            car_speed_y = base_speed
        
        # DRS with Shift
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            car_speed_x *= drs_multiplier
            car_speed_y *= drs_multiplier
        
        # Update position
        car_x += car_speed_x
        car_y += car_speed_y
        
        # Keep car on screen
        car_x = max(0, min(800 - 50, car_x))
        car_y = max(0, min(600 - 80, car_y))
        
        # Clear screen
        screen.fill((100, 200, 100))  # Green background
        
        # Draw F1 car as polygon
        car_body = [
            (car_x + 10, car_y + 20),  # Front left
            (car_x + 40, car_y + 20),  # Front right
            (car_x + 45, car_y + 40),  # Mid right
            (car_x + 50, car_y + 60),  # Rear right
            (car_x + 0, car_y + 60),   # Rear left
            (car_x + 5, car_y + 40),   # Mid left
        ]
        pygame.draw.polygon(screen, (255, 0, 0), car_body)  # Red body
        
        # Draw cockpit (black)
        pygame.draw.rect(screen, (0, 0, 0), (car_x + 15, car_y + 25, 20, 15))
        
        # Draw wheels (black circles)
        pygame.draw.circle(screen, (0, 0, 0), (car_x + 15, car_y + 70), 8)  # Rear left
        pygame.draw.circle(screen, (0, 0, 0), (car_x + 35, car_y + 70), 8)  # Rear right
        pygame.draw.circle(screen, (0, 0, 0), (car_x + 15, car_y + 10), 6)  # Front left
        pygame.draw.circle(screen, (0, 0, 0), (car_x + 35, car_y + 10), 6)  # Front right
        
        # Draw rear wing
        pygame.draw.line(screen, (255, 255, 255), (car_x, car_y + 60), (car_x + 50, car_y + 60), 3)
        pygame.draw.line(screen, (255, 255, 255), (car_x + 10, car_y + 50), (car_x + 40, car_y + 50), 3)
        
        # HUD
        font = pygame.font.SysFont(None, 30)
        speed_text = font.render(f"Speed: {int(math.sqrt(car_speed_x**2 + car_speed_y**2) * 10)}", True, (255, 255, 255))
        screen.blit(speed_text, (10, 10))
        
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            drs_text = font.render("DRS ACTIVE", True, (255, 255, 0))
            screen.blit(drs_text, (10, 40))
        
        pygame.display.flip()
        clock.tick(60)

f1car()
