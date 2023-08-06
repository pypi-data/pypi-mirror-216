from pygame import Vector2
import pygame 

class Camera:
    def __init__(self, 
            screen_width : int,
            screen_height : int,
            speed : float,
            ) -> None:
        """Create a camera object

        Args:
            speed (float, optional): the speed (sensitivity) of the camera. Defaults to 10 (arbitrary).
        """
        self.vec = Vector2(0, 0)
        self.scale = 1
        self.speed = speed
        
        
    def send_event(self, event : pygame.event.Event) -> None:
        """Send a pygame event to the camera, to move it, zoom in/out, etc.

        Args:
            event (pygame.event.Event): the pygame event
        """
        
        # Move the camera with the arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.vec.x -= self.speed
            elif event.key == pygame.K_RIGHT:
                self.vec.x += self.speed
            elif event.key == pygame.K_UP:
                self.vec.y -= self.speed
            elif event.key == pygame.K_DOWN:
                self.vec.y += self.speed

        # Move the camera with the mouse
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                dx_mouse, dy_mouse = event.rel
                self.vec -= Vector2(dx_mouse, dy_mouse) / self.scale
        
        # Zoom in and out with the mouse wheel
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_pos = Vector2(pygame.mouse.get_pos())
            # Zoom in and out with the mouse wheel
            if event.button == 4:
                self.scale *= 1.1
            elif event.button == 5:
                self.scale /= 1.1
                
    
