# Convex Hull Algorithm Demo Applet

CSE 546T Final Project: Sangwook Suh

**Description**

This is a interactive GUI applet that demonstrates two 2D convex hull algorithms, Graham Scan and Chan's algorithm.

**Dependancies** 

- Python 3.12.3
- Numpy 1.26.4

Modules math, random, functools, and tkinter from Python's standard library are also used.
Clone the repository, set up a python 3 virtual environment with numpy (environment.yml is included in repo), then run the following in the terminal:

`$ python app.py`
  
### Directions

Running the app opens up a GUI. The left part contains a white canvas of size (600, 600) pixels. You can click anywhere on the canvas to draw a point. 

The right side is a control panel with buttons. 

- Random: Generate 15 random points on the canvas.
- Graham Scan: Run the Graham Scan demo on the current points in the canvas. Once finished the canvas 
- Chan's Alg: Run the Chan's Algorithm demo on the currnet points in the canvas.
- Reset: Reset the canvas to an empty state.
- Close: Close the applet.

### Algorithm Demos:

During a demo, pseudocode of the current algorithm is displayed underneath the buttons. The current step of the algorithm is highlighted in yellow. There are three new navigation buttons:

- Previous: Go to the previous step of the algorithm.
- Next: Go to the next step of the algorithm.
- Finish: End the demo, highlight the returned convex hull in red.

1. Graham Scan
   - Implemented a 'radial sort' version from [Wikipedia](https://en.wikipedia.org/wiki/Graham_scan).
   - Find the lowest point then radially sort all others with respect to the lowest point.
   - Pseudocode adapted from [Wikipedia](https://en.wikipedia.org/wiki/Graham_scan) page and class slides.

3. Chan's Algorithm
   - Internally uses self-implemented Graham Scan.
   - Pseudocode adapted from class slides.
   - Colors are chosen at random.


