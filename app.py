import tkinter as tk
from tkinter import messagebox

import numpy as np
from scipy.spatial import ConvexHull


def orient(p1, p2, p3):
    return (p2[1] - p1[1]) * (p3[0] - p1[0]) - (p2[0] - p1[0]) * (p3[1] - p1[1])


class DisplayBoard:

    def __init__(self, window):
        self.window = window
        self.window.title("Convex Hull Demo")

        self.frm_display = tk.Frame()
        self.frm_controls = tk.Frame()

        self.canvas = tk.Canvas(self.frm_display, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.TOP)
        self.canvas.bind("<Button-1>", self.click_event)

        self.points = []

        self.btn_rand = tk.Button(self.frm_controls, text="Random", command=self.rand_event)
        self.btn_rand.pack(fill=tk.X)

        self.btn_ch = tk.Button(self.frm_controls, text="Convex Hull", command=self.ch_event)
        self.btn_ch.pack(fill=tk.X)

        self.btn_reset = tk.Button(self.frm_controls, text="Reset", command=self.reset_event)
        self.btn_reset.pack(fill=tk.X)

        self.btn_close = tk.Button(self.frm_controls, text="Close", command=self.close_event)
        self.btn_close.pack(fill=tk.X)

        self.frm_display.pack(side=tk.LEFT)
        self.frm_controls.pack(side=tk.LEFT)


    def draw_ch(self, ccw_vertices):
        n = len(ccw_vertices)
        for i, pt in enumerate(ccw_vertices):
            x1, y1 = pt
            x2, y2 = ccw_vertices[i+1] if i < n - 1 else ccw_vertices[0]
            self.canvas.create_oval(x1-3, y1-3, x1+3, y1+3, outline="red", fill="red", tags="ch")
            self.canvas.create_line(x1, y1, x2, y2, fill="red", tags="ch", width=2)

            # if i >= 4: break


    def rand_event(self, n=10):
        for x, y in np.random.randint(10, 590, size=(n, 2)):
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black", tags="black")
            self.points.append((x, y))
        

    def click_event(self, event):
        self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="black", tags="black")
        self.points.append((event.x, event.y))

    
    def ch_event(self):
        if len(self.points) > 2:
            self.canvas.delete("ch")
            pts = np.array(self.points)

            ### SCIPY IMPLEMENTATION ###
            # pts = pts[ConvexHull(pts).vertices]
            
            ### GRAHAM SCAN IMPLEMENTATION ###
            pts = self.graham_scan(pts)

            self.draw_ch(pts)
        else: 
            messagebox.showwarning(
                "Warning: Not Enough Points", 
                "At least 3 points needed for a convex hull!"
            )

    def reset_event(self):
        self.points = []
        self.canvas.delete("all")

    def close_event(self):
        self.window.destroy()

    def graham_scan(self, pts):
        # input: np array of shape (n, 2) where n is the # of pts
        # output: ccw convex hull vertices

        # Find a boundary point to start: O(n)
        boundary_pt = pts[np.argmax(pts[:, 1])]

        # Radially sort all other points with respect to the boundary point: O(nlog(n))
        angles = np.arctan2( pts[:, 1] - boundary_pt[1], pts[:, 0] - boundary_pt[0])
        pts = pts[np.argsort(angles)[::-1]]

        # Initialize stack
        stack = [pts[0], pts[1]]

        # Test all points: O(n) - each point is popped at most once.
        for pt in pts[2:]:

            # Pop last point in stack if angle with next point is not ccw
            while len(stack) >= 2 and orient(stack[-2], stack[-1], pt) <= 0:
                stack.pop()

            # Push next point
            stack.append(pt)

        return stack


if __name__ == "__main__":
    
    window = tk.Tk()
    board = DisplayBoard(window)
    window.mainloop()