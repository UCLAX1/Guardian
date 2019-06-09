# The Guardian

### ASME UCLA X1 Robotics Project, 2018-2019

This year, X1 Robotics tackled a project dear to video game fans around the world: the Guardian from Nintendo Entertainment's Legend of Zelda: Breath of the Wild. The project, an interactive Hexapod with a rotating head, was a unique challenge. The Guardian features target tracking, life-like gait, organic behavior, and a laser pointer "turret" capable of following its target.


- - - -


To setup and run the code:

* Download the code from the repository
    * Save the files from the pi3 folder on the Raspberry Pi 3
    * Save the files from the pizero folder on the Raspberry Pi Zero
    * Save the files from the server and web_dashboard folders onto a computer
* Connect both Raspberry Pis and the computer to a router 
    * For our implementation, we have the computer's IP as '192.168.0.101' and the Raspberry Pis IPs are statically set to '192.168.0.124' (for the Pi Zero) and '192.168.0.125' (for the Pi 3)
* Run the following programs
    * 'python server.py' on the computer
        * Note: you can run this file either with the Tensorflow or YOLO implementation
    * 'npm start' on the computer (for the web dashboard)
    * 'python3 pi3_client.py' on the Pi 3
    * 'python pizero_client.py' on the Pi Zero
