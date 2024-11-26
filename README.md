# space_demos
Some robot setups for testing Edoras and other robotic projects. Right now, 2 are available:

1. JSC's iMetro mockup
2. Gateway with 2 arms 

Gateway demo:
-------------
Launches a kinematic simulation of Gateway. The user can use the joint state publisher gui to move any of the 2 robot arms available:

```
ros2 launch gateway_description view_gateway.launch.py 
```

You should see something like this:

![Gateway in Rviz](docs/images/gateway_rviz.png)
