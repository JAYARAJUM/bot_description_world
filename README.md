# OGMEN
PROJECT OVERVIEW :: PROJECT REPORT

## Getting started

#### Visualize the robot

```
ros2 launch bot_description rsp_launch.py
open a terminal and type 
rviz2

```

#### Setup workspace
```
mkdr jayaraju_ws/src
cd jayaraju_ws/src
git clone https://github.com/JAYARAJUM/bot_description_world.git .
```

#### Install dependencies
```
cd rjayaraju_ws
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro humble -r -y
```

#### Build and run
```
cd jayaraju_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch bot_discription spawn_launch.py 
```

#### seperate world launching 
```
ros2 launch bot_description rsp_launch.py
ros2 launch bot_world simulation_launch.py
```
these are used to launch the robot in custom world in gazebo 


#### bot control
```
to read the laser data and remapping into filtered scan 
ros2 launch bot_description rsp_launch.py
ros2 launch bot_control bot_control_launch.py
```

#### bot control with waypaoints
```
when we want to use waypoint navigationn 
ros2 launch bot_description spawn_launch.py
cd jayaraju_ws/src/bot_control/scrits
run the python script 
python3 move.py
```

#### THANK YOU
