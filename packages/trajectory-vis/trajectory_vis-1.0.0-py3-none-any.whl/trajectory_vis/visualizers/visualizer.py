from abc import ABC, abstractmethod
import pygame
import sys

from trajectory_vis.camera import Camera
from trajectory_vis.game_objects import GameObject
from trajectory_vis.utils import *



class TrajectoryVisualizer(ABC):
    """The base class for trajectory visualizers.
    It creates a pygame interface and a camera that handles the movement and zoom of the user.
    It also define an empty GameObject list that correspond to the objects that will be displayed on the screen. These objects are the ones that must be updated by the user.
    
    The method start() is launching a loop that will call the two methods that must be implemented by the child class:
    - objects_update_from_event(event) : update (or not) the objects from the pygame events
    - objects_update() : update the objects between 2 steps
    
    These two methods define the behavior of the visualizer.
    """
    def __init__(
            self,
            screen_width : int = 800,
            screen_height : int = 600,
            ) -> None:
        
        # Set up the game window
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Trajectory Visualizer")

        # Set up the camera
        self.camera = Camera(
            screen_height=self.screen_height,
            screen_width=self.screen_width,
            speed=10,
        )
        
        # Add clock
        self.clock = pygame.time.Clock()

        # Set up the objects
        if not hasattr(self, "objects"):
            self.objects : list[GameObject] = []


    def start(self) -> None:
        while True:
            
            self.clock.tick(30)
            for event in pygame.event.get():
                
                # Quit event or ESC key event : quit the game
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # Update camera from event
                self.camera.send_event(event)
                        
                # Update objects from event
                self.objects_update_from_event(event)
                    
                    
            # Fill the background with white
            self.screen.fill(WHITE_COLOR)
            
            # Auto-update of the objects
            self.objects_update()
            
                    
            # Draw the objects and display them
            for obj in self.objects:
                obj.display(self.screen, self.camera)
            pygame.display.update()
            
    
    @abstractmethod
    def objects_update_from_event(self, event : pygame.event.Event) -> None:
        """Update the objects from the pygame event.
        Example : if the event is a certain key, start a new episode.

        Args:
            event (pygame.event.Event): the pygame event
        """
        pass
    
    @abstractmethod
    def objects_update(self) -> None:
        """Update the objects inside the game loop.
        Example : simply display the next frame of the episode.
        """
        
            
