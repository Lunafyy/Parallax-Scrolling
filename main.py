import pygame
pygame.init()

import random

class Vector3D:
    def __init__(self, velocity: list, direction: int):
        self.velocity = velocity
        self.direction = direction
    
    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    @property
    def current_velocity(self):
        return self.velocity
    

class Star:
    def __init__(self, x: int, y: int, z: int, star_vector: Vector3D):
        self.x = x
        self.y = y
        self.z = z

        # self.size = size

        self.star_vector = star_vector
    
    def set_coordinates(self, new_coordinates):
        self.x = new_coordinates[0]
        self.y = new_coordinates[1]
    
    @property
    def coordinates(self):
        return (self.x, self.y)

    @property
    def scale(self):
        return self.z

    @property
    def vector(self):
        return self.star_vector

    @property
    def velocity(self):
        return self.star_vector.velocity
    
    @property
    def direction(self):
        return self.star_vector.direction

class ParallaxScrolling(object):
    def __init__(self, screen_x, screen_y, star_count):
        self.window = pygame.display.set_mode([screen_x, screen_y])

        self.screen_x = screen_x
        self.screen_y = screen_y

        self.star_count = star_count
        
        self.is_running = True

        self.font = pygame.font.SysFont(None, 30)

        self.game_loop()

    def game_loop(self):
        stars = []

        for i in range(self.star_count):
            stars.append(Star( random.randint(0, self.screen_x), random.randint(0, self.screen_y), random.randint(1, 4), Vector3D([0, 0], 0) ))

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                pressed = pygame.key.get_pressed()

                if pressed[pygame.K_UP]:
                    for star in stars:
                        current_velocity = star.vector.current_velocity
                        if current_velocity[0] >= 1:
                            current_velocity[0] = 1
                        else:
                            current_velocity[0] += 0.1

                        star.vector.set_velocity(current_velocity)
                elif pressed[pygame.K_DOWN]:
                    for star in stars:
                        current_velocity = star.vector.current_velocity
                        if current_velocity[0] <= 0:
                            current_velocity[0] = 0
                        else:
                            current_velocity[0] -= 0.1
                        star.vector.set_velocity(current_velocity)

            self.window.fill((0, 0, 0))
            
            # Render Stars
            for star in stars:
                star_coords = star.coordinates

                star_velocity = star.vector.current_velocity
                x_vel = star_velocity[0]
                y_vel = star_velocity[1]
                

                next_position = list(star_coords)

                if x_vel > 0:
                    next_position[0] -= x_vel * star.scale

                    star.set_coordinates(next_position)

                    if next_position[0] <= 0:
                        next_position[0] = self.screen_x - 1 

                        star.set_coordinates(next_position)
                    
                pygame.draw.circle(self.window, (255, 255, 255), star.coordinates, star.scale)
            
            velocity_to_mph = int(((star_velocity[0]*10) * 2.2) * 100)

            font_background_colour = (0, 0, 0)

            if velocity_to_mph < 0:
                velocity_to_mph = 0

            if velocity_to_mph < 500:
                font_background_colour = (119, 221, 119)
            elif velocity_to_mph > 600 and velocity_to_mph < 1200:
                font_background_colour = (255, 179, 71)
            elif velocity_to_mph > 1200 and velocity_to_mph < 2000:
                font_background_colour = (255, 105, 97)
            elif velocity_to_mph >= 2000:
                font_background_colour = (255, 0, 0)
            
            speed = self.font.render(f"Current Speed: ~{velocity_to_mph}mph", 1, (255, 255, 255), font_background_colour)
            self.window.blit(speed, (5, 5))
            pygame.display.flip()
        

if __name__ == "__main__":
    PS = ParallaxScrolling(1280, 720, 200)