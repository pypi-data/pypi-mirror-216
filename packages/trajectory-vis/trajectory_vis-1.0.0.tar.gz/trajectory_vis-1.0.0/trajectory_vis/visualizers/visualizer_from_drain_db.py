import time
from typing import Any
import argparse
import json
import os
import random
from typing import Dict, List

from drain.job import Job
from drain.utils.config import JobConfig
from drain.utils.episode.episode import EpisodeFrameFromDict
from drain.utils.imports import instantiate_class

import pygame
from pygame import Vector2

from trajectory_vis.visualizers.visualizer import TrajectoryVisualizer
from trajectory_vis.game_objects import Arrow, GameObject, Entity, Line, WritingOnScreen
from trajectory_vis.utils import BLACK_COLOR, BLUE_COLOR, GREEN_COLOR



class DroneFromDrainDB(Entity):
    def __init__(self, frame: Dict[str, float]) -> None:
        x, y = frame["position"][0:2]
        super().__init__(
            vec=Vector2(x, y) * 10,
            length=5,
            color=GREEN_COLOR,
            shape="circle",
            )



class TrajectoryVisualizerFromDatabase(TrajectoryVisualizer):
    def __init__(
            self,
            job : Job,
            input_db : str,
            random_order : bool = True,
            n_traj_at_once : int = 4,
            ) -> None:
        """A visualizer that displays the trajectories of drones from the Drain database.

        Args:
            job (Job): the job using the visualizer
            input_db (str): the path to the directory containing the json files
            random_order (bool, optional): if True, the json files will be displayed in a random order. Defaults to True.
            n_traj_at_once (int, optional): the number of trajectories to display at once. Defaults to 1.
        """
        
        super().__init__()

        # Set up parameters
        self.job = job
        self.random_order = random_order
        self.n_traj_at_once = n_traj_at_once
        self.input_db = input_db
        
        # Set up the link to the database
        self.job_cfg = job._configuration
        self.episodes_reader = job.get_episodes_reader(name=self.job_cfg.input_db)
        self.nb_episodes = len(self.episodes_reader)
        self.episodes_ids = self.episodes_reader.episodes_ids()

        # Set up currently displayed episodes
        self.current_episode_indexes = [k for k in range(self.n_traj_at_once)]
        self.current_episode_ids = [self.episodes_ids[index] for index in self.current_episode_indexes]
        self.current_episodes = [self.episodes_reader[episode_id] for episode_id in self.current_episode_ids]
        self.is_episode_running = False
        
        # Add text
        writing_start = WritingOnScreen(text="Use Q, Z and D for changing of episodes", position=Vector2(self.screen_width/100, self.screen_height/100))
        
        # Intialize the objects list
        self.objects : list[GameObject] = [writing_start]
        
    
    def objects_update_from_event(self, event) -> None:
        
        # Q and D are used to move through the episodes. Z is used for restarting the episode.
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_q, pygame.K_d, pygame.K_z]:
                        
            # Clear any previous objects
            self.objects.clear()
            
            # Set up the episode (index, filename, data, frames)
            if event.key == pygame.K_q:
                delta_index = -1
            elif event.key == pygame.K_d:
                delta_index = 1
            elif event.key == pygame.K_z:
                delta_index = 0
            self.is_episode_running = True
            self.current_episode_indexes = [(index + delta_index * self.n_traj_at_once) % self.nb_episodes for index in self.current_episode_indexes]
            self.current_episode_ids = [self.episodes_ids[index] for index in self.current_episode_indexes]
            self.current_episodes : List[List[EpisodeFrameFromDict]] = [self.episodes_reader[episode_id] for episode_id in self.current_episode_ids]
            
            self.max_len_traj = max([len(traj) for traj in self.current_episodes])
            self.n_frame = 0
            
            # Add writing indicating the episode advancement
            self.objects = [WritingOnScreen(
                text=f"Frame 0/{self.max_len_traj}",
                position=Vector2(10, self.screen_height - 10 - 20),
                color=BLACK_COLOR,
                font_size=20,
            )]
            
            # Create the drones from the first frames of the trajectories
            self.previous_drones : List[DroneFromDrainDB] = []
            for episode in self.current_episodes:
                frame = episode[self.n_frame].to_dict()
                drone = DroneFromDrainDB(frame)
                self.previous_drones.append(drone)
                self.objects.append(drone)
            
            # Add writing on screen
            self.objects.append(WritingOnScreen(text=f"Episodes n°{self.current_episode_indexes}. First is of ID : {self.current_episode_ids[0]}", position=Vector2(self.screen_width/100, self.screen_height/100)))
            
            # Set up the camera position so that the (last) drone is in the center of the screen
            self.camera.vec = drone.vec - Vector2(400, 300)


    def objects_update(self) -> None:
        if not self.is_episode_running:
            return
        
        # Update the writing indicating the episode advancement
        self.objects[0] = WritingOnScreen(
                text=f"Frame {self.n_frame}/{self.max_len_traj}",
                position=Vector2(10, self.screen_height - 10 - 20),
                color=BLACK_COLOR,
                font_size=20,
            )
        self.n_frame += 1
        
        for k in range(self.n_traj_at_once):
            
            # Create the drone from the next frame
            episode = self.current_episodes[k]
            if len(episode) <= self.n_frame:
                continue
            frame = episode[self.n_frame].to_dict()
            drone = DroneFromDrainDB(frame)
            
            # Add the drone to the objects list
            self.objects.append(drone)
            
            # Add an arrow between the previous drone and the current one, then update the previous drone
            if self.previous_drones[k] is not None:
                self.objects.append(Arrow(self.previous_drones[k].vec, drone.vec, color=BLACK_COLOR))
            self.previous_drones[k] = drone
            
        # Episode stop running if all the trajectories are empty
        self.is_episode_running = any([len(episode) > self.n_frame for episode in self.current_episodes])
                
    
    
    
    
class TrajectoryVisualizerJob(Job):

    def __init__(self, job_id, configuration, db, launcher, debug=False):
        super().__init__(job_id, configuration, db, launcher, debug)

    def _run(self):
        visualizer = TrajectoryVisualizerFromDatabase(
            job=self,
            input_db=self._configuration.input_db,
            random_order=self._configuration.random_order,
            n_traj_at_once=self._configuration.n_traj_at_once,
        )
        visualizer.start()
            
            

    