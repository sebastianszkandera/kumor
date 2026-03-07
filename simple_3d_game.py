import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

vertices = [
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, -1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

edges = [
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
]

surfaces = [
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
]

colors = [
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
]

def Cube(pos):
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glPopMatrix()

def Sphere(pos, radius=0.5):
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glColor3f(1, 1, 0)  # Yellow spheres
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 20, 20)
    gluDeleteQuadric(quadric)
    glPopMatrix()

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def main():
    print("3D Cube Collector Game")
    print("Controls:")
    print("WASD: Move the cube")
    print("Q/E: Move up/down")
    print("Collect yellow spheres to score points!")
    print("Close the window to quit.")
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -10)
    glEnable(GL_DEPTH_TEST)

    player_pos = [0, 0, 0]
    targets = [[random.uniform(-5,5), random.uniform(-5,5), random.uniform(-5,5)] for _ in range(5)]
    score = 0

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000.0  # Delta time for smooth movement

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        speed = 5 * dt
        if keys[K_w]:
            player_pos[2] -= speed
        if keys[K_s]:
            player_pos[2] += speed
        if keys[K_a]:
            player_pos[0] -= speed
        if keys[K_d]:
            player_pos[0] += speed
        if keys[K_q]:
            player_pos[1] += speed
        if keys[K_e]:
            player_pos[1] -= speed

        # Check collisions
        new_targets = []
        for target in targets:
            if distance(player_pos, target) < 1.5:  # Cube size approx
                score += 10
                print(f"Score: {score}")
                # Add new target
                new_targets.append([random.uniform(-5,5), random.uniform(-5,5), random.uniform(-5,5)])
            else:
                new_targets.append(target)
        targets = new_targets

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Draw player cube
        Cube(player_pos)

        # Draw targets
        for target in targets:
            Sphere(target)

        pygame.display.flip()

if __name__ == "__main__":
    main()
