

from abc import ABC, abstractmethod
import math
from typing import Dict
import pygame
import sys
from trajectory_vis.camera import Camera


from pygame import Surface, Vector2

from trajectory_vis.utils import *



class GameObject(ABC):
    """The abstract class for all game objects. 
    A game object is a python object that must implement the display method, 
    which displays the object on the pygame screen while taking into account the camera position and scale."""
    @abstractmethod
    def display(self, screen : Surface, camera : Camera) -> None:
        """Display the object on the pygame screen, take into account the camera position and scale

        Args:
            screen (Surface): the pygame screen
            camera (Camera): the camera object
        """
        pass



class Line(GameObject):
    def __init__(self, point1 : Vector2, point2 : Vector2, color : tuple[int, int, int] = BLACK_COLOR) -> None:
        """A simple line between two points

        Args:
            point1 (Vector2): the first point of the line
            point2 (Vector2): the second point of the line
            color (tuple[int, int, int], optional): the color of the line. Defaults to BLACK_COLOR.
        """
        super().__init__()
        self.color = color
        self.point1 = point1
        self.point2 = point2
        
    def display(self, screen: Surface, camera: Camera):
        # Calculate the scaled position of the line based on the camera's properties
        scaled_point1 = (self.point1 - camera.vec) * camera.scale
        scaled_point2 = (self.point2 - camera.vec) * camera.scale

        # Draw the line on the screen
        pygame.draw.line(screen, self.color, scaled_point1, scaled_point2)



class Arrow(Line):
    """An arrow between two points"""
    def display(self, screen: Surface, camera: Camera):
        # Calculate the scaled position of the line based on the camera's properties
        scaled_point1 = (self.point1 - camera.vec) * camera.scale
        scaled_point2 = (self.point2 - camera.vec) * camera.scale

        # Draw the line on the screen
        pygame.draw.line(screen, self.color, scaled_point1, scaled_point2)
        
        # Calculate the angle of the arrow
        angle = math.atan2(scaled_point1.y - scaled_point2.y, scaled_point1.x - scaled_point2.x)
        ARROW_HEAD_LENGTH = 2
        ARROW_HEAD_ANGLE = math.pi / 6
        # Calculate the position of the arrow head
        arrow_head_point = Vector2(
            scaled_point2.x + ARROW_HEAD_LENGTH * math.cos(angle - ARROW_HEAD_ANGLE) * camera.scale,
            scaled_point2.y + ARROW_HEAD_LENGTH * math.sin(angle - ARROW_HEAD_ANGLE) * camera.scale,
        )
        # Draw the arrow head
        pygame.draw.line(screen, self.color, arrow_head_point, scaled_point2)
        # Calculate the other point of the arrow head
        arrow_head_point2 = Vector2(
            scaled_point2.x + ARROW_HEAD_LENGTH * math.cos(angle + ARROW_HEAD_ANGLE) * camera.scale,
            scaled_point2.y + ARROW_HEAD_LENGTH * math.sin(angle + ARROW_HEAD_ANGLE) * camera.scale,
        )
        # Draw the arrow head
        pygame.draw.line(screen, self.color, arrow_head_point2, scaled_point2)
         
        



class Entity(GameObject):
    """An object representing an entity at a certain frame
    """
    def __init__(self, 
            vec : Vector2,
            length : float = 10,
            color : tuple[int, int, int] = BLACK_COLOR,
            shape : str = "circle",
    ) -> None:
        """Create an entity object

        Args:
            vec (Vector2): the position of the entity
            length (float, optional): the length of the entity. Defaults to 10.
            color (tuple[int, int, int], optional): its color. Defaults to BLACK_COLOR.
            shape (str, optional): whether its a "circle" or a "square". Defaults to "circle".
        """
        super().__init__()
        self.vec = vec
        self.length = length
        self.color = color
        assert shape in ["circle", "square"], "The shape must be either 'circle' or 'square'"
        self.shape = shape
        self.surface = Surface((self.length, self.length))
        
    
    def display(self, screen: Surface, camera: Camera):
        # Calculate the scaled position of the circle based on the camera's properties
        scaled_position = (self.vec - camera.vec) * camera.scale

        # Draw the shape on the screen
        if self.shape == "square":
            pygame.draw.rect(screen, self.color, (scaled_position.x, scaled_position.y, self.length, self.length))
        else:
            pygame.draw.circle(screen, self.color, scaled_position, self.length // 2)
         
        

class WritingOnScreen(GameObject):
    """An object representing a text on the screen"""
    
    def __init__(self,
            text : str,
            position : Vector2,
            color : tuple[int, int, int] = BLACK_COLOR,
            font_size : int = 20,
    ) -> None:
        """Create a WritingOnScreen object, which represents a text on the screen

        Args:
            text (str): the content of the text
            position (Vector2): the position of the text
            color (tuple[int, int, int], optional): the color of the text. Defaults to BLACK_COLOR.
            font_size (int, optional): the font size of the text. Defaults to 20.
        """
        self.text = text
        self.position = position
        self.color = color
        self.font_size = font_size
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.surface = self.font.render(self.text, True, self.color)
    
    def display(self, screen: Surface, camera: Camera) -> None:
        screen.blit(self.surface, self.position)