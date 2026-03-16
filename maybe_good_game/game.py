import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 255, 0))  # Zelené pozadí
    
    # Kreslení hor v pozadí
    width, height = screen.get_size()
    mountain_color = (100, 100, 100)
    # Hory nahoře
    pygame.draw.polygon(screen, mountain_color, [(0, 100), (200, 50), (400, 80), (600, 30), (800, 70), (width, 100)])
    # Hory dole
    pygame.draw.polygon(screen, mountain_color, [(0, height-100), (200, height-50), (400, height-80), (600, height-30), (800, height-70), (width, height-100)])
    
    # Kreslení stromů kolem obrazovky
    tree_spacing = 150
    for x in range(0, width, tree_spacing):
        # Stromy nahoře
        if x > 100 and x < width - 100:  # Vyhnout se rohům kvůli horám
            trunk_x = x
            trunk_y = 120
            pygame.draw.rect(screen, (139, 69, 19), (trunk_x, trunk_y, 15, 80))  # Kmen
            pygame.draw.circle(screen, (0, 150, 0), (trunk_x + 7, trunk_y - 20), 30)  # Listy
            pygame.draw.circle(screen, (0, 120, 0), (trunk_x + 7, trunk_y - 10), 25)  # Další listy
        # Stromy dole
        trunk_y_bottom = height - 200
        pygame.draw.rect(screen, (139, 69, 19), (x, trunk_y_bottom, 15, 80))
        pygame.draw.circle(screen, (0, 150, 0), (x + 7, trunk_y_bottom - 20), 30)
        pygame.draw.circle(screen, (0, 120, 0), (x + 7, trunk_y_bottom - 10), 25)
    
    # Stromy po stranách
    for y in range(200, height - 200, tree_spacing):
        # Levá strana
        pygame.draw.rect(screen, (139, 69, 19), (20, y, 15, 80))
        pygame.draw.circle(screen, (0, 150, 0), (27, y - 20), 30)
        pygame.draw.circle(screen, (0, 120, 0), (27, y - 10), 25)
        # Pravá strana
        pygame.draw.rect(screen, (139, 69, 19), (width - 35, y, 15, 80))
        pygame.draw.circle(screen, (0, 150, 0), (width - 28, y - 20), 30)
        pygame.draw.circle(screen, (0, 120, 0), (width - 28, y - 10), 25)

    pygame.display.flip()
def gui():
    okno_pro_penize = pygame.Rect(50, 50, 200, 100)
    pygame.draw.rect(screen, (255, 255, 255), okno_pro_penize)
    font = pygame.font.Font(None, 36)

    pygame.display.flip()