# Convex Hull Algorithm Demo Applet

CSE 546T Final Project: Sangwook Suh

**Description**

This is a interactive GUI applet that demonstrates two 2D convex hull algorithms, Graham Scan and Chan's algorithm.

**Background**

Chan's algorithm is a convex hull algorithm that has O(nlogn) worst-case performance while still providing an output-sensitive O(nlogh) time, by doing a Gift Wrap of partition convex hulls, and being smart about searching for parition sizes. Compared to Kirkpatrick-Seidel's ultimate convex hull algorithm, it is much easier to intuitively understand. I aimed to create a GUI demo for Chan's algorithm, and also included Graham Scan for completeness, as Chan's algorithm internally uses a O(nlogn) convex hull algorithm such as Graham Scan. I wrote the demo using Python's Tkinter package and some functions from NumPy, but mostly implemented the algorithm from scratch. I used a 'flipped approach' to accomodate the Tkinter's canvas coordinates starting at the top left instead of bottom right. Input points can be generated randomly or manually drawn by clicking. 

**Dependancies** 

- Python 3.12.3
- Numpy 1.26.4

Modules math, random, functools, and tkinter from Python's standard library are also used.
Clone the repository, set up a python 3 virtual environment with numpy (environment.yml is included in repo), then run the following in the terminal:

`$ python app.py`
  
## Directions

Running the app opens up a GUI. The left part contains a white canvas of size (600, 600) pixels. You can click anywhere on the canvas to draw a point. 

The right side is a control panel with buttons. 

- **Random:** Generate 20 random points on the canvas.
- **Graham Scan:** Run the Graham Scan demo on the current points in the canvas. Once finished the canvas 
- **Chan's Alg:** Run the Chan's Algorithm demo on the currnet points in the canvas.
- **Reset:** Reset the canvas to an empty state.
- **Close:** Close the applet.

## Algorithm Demos:

During a demo, pseudocode of the current algorithm is displayed underneath the buttons. The current step of the algorithm is highlighted in yellow. There are three new navigation buttons:

- **Previous:** Go to the previous step of the algorithm.
- **Next:** Go to the next step of the algorithm.
- **Finish:** End the demo, highlight the convex hull returned by the algorithm in red.

1. **Graham Scan**
   - Implemented a 'radial sort' version from [Wikipedia](https://en.wikipedia.org/wiki/Graham_scan).
   - Find the lowest point then radially sort all others with respect to the lowest point.
   - Pseudocode adapted from [Wikipedia](https://en.wikipedia.org/wiki/Graham_scan) page and class slides.

Example:
<img width="1062" alt="grahamscan" src="https://github.com/sangwooksuh/comp-geo-final-project/assets/77888267/6d23c1b8-acfe-4dd3-b5c4-67323d7c78c5">


2. **Chan's Algorithm**
   - Internally uses self-implemented Graham Scan.
   - Pseudocode adapted from class slides.
   - Colors are chosen at random.

Example:

- t=1:
<img width="1083" alt="Chan loop1" src="https://github.com/sangwooksuh/comp-geo-final-project/assets/77888267/0d4153b7-d1f6-44f7-9e34-6b51fefa4644">

- t=2:
<img width="1083" alt="chan loop2" src="https://github.com/sangwooksuh/comp-geo-final-project/assets/77888267/96cb46b1-46b9-4358-9d21-e1070db0166e">


Example: Output Sensitive

<img width="1121" alt="chan output sensitive" src="https://github.com/sangwooksuh/comp-geo-final-project/assets/77888267/001e220b-6131-40d3-8a63-c70517a149b4">
  
## Implementation Notes

1. **Flipped Algorithm:** `Tkinter`, the Python standard library's GUI module, has a coordinate system with the origin (0,0) at the _top left_: thus the y-coordinate _increases_ as you go _down_. I implemented a flipped version of the algorithm to match the pseudocode: (Graham Scan) I find the higest point, then sort the points radially in a clockwise order with respect to the original point. This visually shows to the user as first finding the lowest boundary point, and proceeding the algorithm in a counterclockwise direction. Similar adjustments are made to Chan's algorithm.
2. **General Position:** It is assumed that the points given are in general position. For instance the Graham Scan might fail if three points, including the lower boundary point are colinear, because two points would share the same angle at the lower boundary point. There is no checking or validation for general position or numerical stability issues.
3. **Tkinter Click Register Bug:** TKinter canvas seems to have an issue where it sometimes fails to register click events if they are done too fast succesively, or if the mouse does not move betwen clicks, especially on the newer MacOS. It seems to happen randomly sometimes.
4. **Choice of Random=20:** The random button produces 20 points. I found this to be a good number to see how Chan's algortihm works, as in a general case, it will go up to t=2, with the set partitioned into 5, and 2 at each t. Depending on the configuration, 20 points could sometimes still terminate while t=1, (i.e. if the convex hull is a simple triangle or quadrilateral). These cases can demonstrate the output-sensitive nature of Chan's algorithm.

   


