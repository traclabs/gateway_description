# gateway_description
NASA Lunar Gateway robot description (URDF + meshes + launch files to run in Gazebo). Models obtained from [this public repository](https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Gateway) 

**Setup:** ROS2 Jazzy. Gazebo Harmonic

**How to run:**

```
ros2 launch gateway_description gateway.launch.py
```
You should see something like this:

![Screenshot from 2025-03-19 17-05-29](https://github.com/user-attachments/assets/b447b20d-e2cc-47ad-89f0-de5d1feeb2f2)

To move the arms, you can use the big_arm/ and little_arm/ services, named close_arm, open_arm and random_arm. For instance:

```
ros2 service call /big_arm/open_arm std_srvs/srv/Empty {}
ros2 service call /little_arm/random_arm std_srvs/srv/Empty {}
```
