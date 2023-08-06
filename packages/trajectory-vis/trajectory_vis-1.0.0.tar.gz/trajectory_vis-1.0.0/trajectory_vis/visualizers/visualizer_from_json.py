import argparse
import json
import os
import random
from typing import Dict, List

import pygame
from pygame import Vector2

from trajectory_vis.visualizers.visualizer import TrajectoryVisualizer
from trajectory_vis.game_objects import Arrow, GameObject, Entity, Line, WritingOnScreen
from trajectory_vis.utils import BLACK_COLOR, BLUE_COLOR, GREEN_COLOR



class DroneFromJsonData(Entity):
    def __init__(self, frame: Dict[str, float]) -> None:
        x, y = frame["transform"][0:2]
        super().__init__(
            vec=Vector2(x, y) * 10,
            length=5,
            color=BLUE_COLOR,
            shape="circle",
            )



class TrajectoryVisualizerFromJsonDroneData(TrajectoryVisualizer):
    def __init__(
            self,
            path_json_dir : str,
            random_order : bool = True,
            n_traj_at_once : int = 4,
            ) -> None:
        """A visualizer that displays the trajectories of drones from json files.

        Args:
            path_json_dir (str): the path to the directory containing the json files
            random_order (bool, optional): if True, the json files will be displayed in a random order. Defaults to True.
            n_traj_at_once (int, optional): the number of trajectories to display at once. Defaults to 1.
        """
        
        super().__init__()

        # Set up the filenames
        self.path_json_dir = path_json_dir
        self.filename_list = os.listdir(path_json_dir)
        assert len(self.filename_list) > 0, f"The directory {path_json_dir} is empty"
        if random_order:
            random.shuffle(self.filename_list)
        self.filename_list = [filename for filename in self.filename_list if filename.startswith("DroneTransforms")]
        assert len(self.filename_list) > 0, f"The directory {path_json_dir} does not contain any json file starting with 'DroneTransforms'"
        self.n_traj_at_once = min(n_traj_at_once, len(self.filename_list))
        self.current_filename_indexes = [k for k in range(self.n_traj_at_once)]
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
            self.current_filename_indexes = [(index + delta_index * self.n_traj_at_once) % len(self.filename_list) for index in self.current_filename_indexes]
            self.current_filenames = [self.filename_list[index] for index in self.current_filename_indexes]
            current_datas = [json.load(open(os.path.join(self.path_json_dir, filename), "r")) for filename in self.current_filenames]
            self.current_trajectories : List[List[Dict[str, float]]] = [data["DroneSnapShots"] for data in current_datas]
            self.max_len_traj = max([len(traj) for traj in self.current_trajectories])
            self.n_frame = 0
            
            # Add writing indicating the episode advancement
            self.objects = [WritingOnScreen(
                text=f"Frame 0/{self.max_len_traj}",
                position=Vector2(10, self.screen_height - 10 - 20),
                color=BLACK_COLOR,
                font_size=20,
            )]
            
            # Create the drones from the first frames of the trajectories
            self.previous_drones : List[DroneFromJsonData] = [None for _ in range(self.n_traj_at_once)]
            self.drones = []
            for traj in self.current_trajectories:
                frame = traj.pop(0)
                drone = DroneFromJsonData(frame)
                self.drones.append(drone)
                self.objects.append(drone)
                
            # Add writing on screen
            self.objects.append(WritingOnScreen(text=f"Json files n°{self.current_filename_indexes}. First is {self.current_filenames[0]}", position=Vector2(self.screen_width/100, self.screen_height/100)))
            
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
            traj = self.current_trajectories[k]
            if len(traj) == 0:
                continue
            frame = traj.pop(0)
            drone = DroneFromJsonData(frame)
            
            # Add the drone to the objects list
            self.objects.append(drone)
            
            # Add an arrow between the previous drone and the current one, then update the previous drone
            if self.previous_drones[k] is not None:
                self.objects.append(Arrow(self.previous_drones[k].vec, drone.vec, color=BLACK_COLOR))
            self.previous_drones[k] = drone
            
        # Episode stop running if all the trajectories are empty
        self.is_episode_running = not all([len(traj) == 0 for traj in self.current_trajectories])
                
                
                

if __name__ == "__main__":
    # Parse the arguments
    parser = argparse.ArgumentParser()
    default_path = "//ubisoft.org/projects/r6/mtl/Public/AIBots/playerdata/y8s1.2/bigresults/output"
    parser.add_argument("--path", type=str, default=default_path)
    parser.add_argument("--random", type=bool, default=True)
    parser.add_argument("--n", type=int, default=1)
    args = parser.parse_args()
    
    # Start the visualizer
    visualizer = TrajectoryVisualizerFromJsonDroneData(
        path_json_dir=args.path,
        random_order=args.random,
        n_traj_at_once=args.n,
    )
    visualizer.start()