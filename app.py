import random
import numpy as np
import tkinter as tk
from tkinter import messagebox
from functools import partial


def orient(p1, p2, p3):
    return (p2[1] - p1[1]) * (p3[0] - p1[0]) - (p2[0] - p1[0]) * (p3[1] - p1[1])


class DisplayBoard:

    def __init__(self, win):
        self.win = win
        self.win.title("Convex Hull Demo")
        self.bg = self.win.cget('bg')
        self.points = []

        self.frm_display = tk.Frame(self.win)
        self.frm_controls = tk.Frame(self.win)
        self.frm_btns = tk.Frame(self.frm_controls)
        self.frm_alg =tk.Frame(self.frm_controls)

        # Display Panel
        self.canvas = tk.Canvas(self.frm_display, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.TOP)
        self.canvas.bind("<Button-1>", self.click_event)

        # Control Panel
        self.btn_rand = tk.Button(self.frm_btns, text="Random", command=self.rand_event)
        self.btn_rand.grid(row=0, column=0, sticky="n")

        self.btn_gs = tk.Button(self.frm_btns, text="Graham Scan", command=self.gs_event)
        self.btn_gs.grid(row=0, column=1, sticky="n")

        self.btn_prev = tk.Button(self.frm_btns, text="Previous", command=partial(self.step_event, "prev"))
        self.btn_next = tk.Button(self.frm_btns, text="Next", command=partial(self.step_event, "next"))
        self.btn_finish = tk.Button(self.frm_btns, text="Finish", command=self.exit_step_mode)

        self.btn_reset = tk.Button(self.frm_btns, text="Reset", command=self.reset_event)
        self.btn_reset.grid(row=1, column=0, sticky="n")

        self.btn_close = tk.Button(self.frm_btns, text="Close", command=self.close_event)
        self.btn_close.grid(row=1, column=1, sticky="n")

        # Algorithm
        self.is_step_mode = False
        self.steps = None
        self.current_step = 0
        self.lbl_gs = [
            tk.Label(self.frm_alg, text="FUNCTION graham_scan(S):", font=("Menlo", 11)), #0
            tk.Label(self.frm_alg, text="    p1 <- boundary point of S", font=("Menlo", 11)), #1
            tk.Label(self.frm_alg, text="    {p1, p2, ..., pn} <- sort S radially with respect to p1", font=("Menlo", 11)), #2
            tk.Label(self.frm_alg, text="    H <- new Stack()", font=("Menlo", 11)), #3
            tk.Label(self.frm_alg, text="    H.push(p1); H.push(p2)", font=("Menlo", 11)), #4
            tk.Label(self.frm_alg, text="    FOR i=3 TO n:", font=("Menlo", 11)), #5
            tk.Label(self.frm_alg, text="        WHILE |H| > 1 AND Orient(H.second, H.first, pi) < 0:", font=("Menlo", 11)), #6
            tk.Label(self.frm_alg, text="            H.pop()", font=("Menlo", 11)), #7
            tk.Label(self.frm_alg, text="        H.push(pi)", font=("Menlo", 11)), #8
            tk.Label(self.frm_alg, text="    RETURN H.reverse()", font=("Menlo", 11)), #9
        ]

        # Pack frames
        self.frm_display.grid(row=0, column=0)
        self.frm_controls.grid(row=0, column=1, sticky='nsew')
        self.frm_btns.grid(row=0, column=0, sticky='n', padx=10, pady=20)
        self.frm_alg.grid(row=1, column=0, sticky='n')


    def draw_ch(self, ccw_vertices, tag="ch"):
        n = len(ccw_vertices)
        for i, pt in enumerate(ccw_vertices):
            x1, y1 = pt
            x2, y2 = ccw_vertices[i+1] if i < n - 1 else ccw_vertices[0]
            self.canvas.create_oval(x1-3, y1-3, x1+3, y1+3, outline="red", fill="red", tags=tag)
            self.canvas.create_line(x1, y1, x2, y2, fill="red", tags=tag, width=2)

            # if i >= 4: break


    def rand_event(self, n=10):   
        for _ in range(n):
            x, y = (random.randint(10, 590), random.randint(10, 590))
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black", tags="black")
            self.points.append((x, y))


    def click_event(self, event):
        self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="black", tags="black")
        self.points.append((event.x, event.y))

    
    def gs_event(self):
        if len(self.points) > 2:
            self.canvas.delete("ch")
            pts = np.array(self.points)
            
            self.steps = self.graham_scan_steps(pts)
            self.enter_step_mode()

        else: 
            messagebox.showwarning(
                "Warning: Not Enough Points", 
                "At least 3 points needed for a convex hull!"
            )


    def step_event(self, direction):

        if self.current_step == len(self.steps) - 1 and direction == "next":
            messagebox.showwarning("Warning: No More Steps", "Last step of algorithm!")
            return
        
        if self.current_step == 0 and direction == "prev":
            messagebox.showwarning("Warning: No Previous Steps", "First step of algorithm!")
            return

        self.canvas.delete("steps")
        for lbl in self.lbl_gs:
            lbl.config(bg=self.bg)

        if direction == "next":
            self.current_step += 1
        else:
            self.current_step -= 1

        if self.current_step == 1:
            self.lbl_gs[1].config(bg="yellow")
            x, y = self.steps[1]
            self.canvas.create_oval(x-3, y-3, x+3, y+3, outline="red", fill="red", tags="steps")

        elif self.current_step == 2:
            for i in range(2, 5):
                self.lbl_gs[i].config(bg='yellow')
            x1, y1 = self.steps[2][0]
            x2, y2 = self.steps[2][1]
            self.canvas.create_oval(x1-3, y1-3, x1+3, y1+3, outline="red", fill="red", tags="steps")
            self.canvas.create_line(x1,y1,x2,y2, fill="red", tags="steps", width=2)
            self.canvas.create_oval(x2-3, y2-3, x2+3, y2+3, outline="red", fill="red", tags="steps")
        
        elif self.current_step == len(self.steps) - 1:
            self.lbl_gs[-1].config(bg="yellow")
            self.draw_ch(self.steps[-1], tag="steps")

        else:
            self.lbl_gs[5].config(bg="yellow")
            step = self.steps[self.current_step]
            stack = step[1]
            for i, (x, y) in enumerate(stack):
                self.canvas.create_oval(x-3, y-3, x+3, y+3, outline="red", fill="red", tags="steps")
                if i < len(stack) - 1:
                    x2, y2 = stack[i+1] 
                    self.canvas.create_line(x, y, x2, y2, fill="red", tags="steps", width=2)
            if step[0] == "push":
                x, y = stack[-1]
                self.canvas.create_oval(x-3, y-3, x+3, y+3, outline="red", fill="red", tags="steps")
                self.lbl_gs[8].config(bg="yellow")
            else:
                corner = stack[-1]
                test_pt = step[2]
                self.canvas.create_oval(corner[0]-3, corner[1]-3, corner[0]+3, corner[1]+3, outline="blue", fill="blue", tags="steps")
                self.canvas.create_line(corner[0], corner[1], test_pt[0], test_pt[1], dash=(4,2), fill="blue", tags="steps", width=2)
                self.canvas.create_oval(test_pt[0]-3, test_pt[1]-3, test_pt[0]+3, test_pt[1]+3, outline="blue", fill="blue", tags="steps")
                if step[0] == "test":
                    self.lbl_gs[6].config(bg="yellow")
                else:
                    self.lbl_gs[7].config(bg="yellow")


    def enter_step_mode(self):
        self.is_step_mode = True
        self.btn_rand.grid_forget()
        self.btn_gs.grid_forget()
        self.btn_prev.grid(row=0, column=0, sticky="n")
        self.btn_next.grid(row=0, column=1, sticky="n")
        self.btn_finish.grid(row=0, column=2, sticky="n")
        self.btn_close.grid(row=1,column=2, sticky="n" )

        self.lbl_gs[0].config(bg="yellow")
        for i, lbl in enumerate(self.lbl_gs):
            lbl.grid(row=i, column=0, sticky="w")

    def exit_step_mode(self):

        self.is_step_mode = False
        self.current_step = 0

        self.btn_prev.grid_forget()
        self.btn_next.grid_forget()
        self.btn_finish.grid_forget()
        self.btn_rand.grid(row=0, column=0, sticky="n")
        self.btn_gs.grid(row=0, column=1, sticky="n")
        self.btn_close.grid(row=1, column=1, sticky="n")

        self.canvas.delete("steps")
        self.draw_ch(self.steps[-1])

        self.steps = None

        for lbl in self.lbl_gs:
            lbl.config(bg=self.bg)
            lbl.grid_forget()

    def reset_event(self):
        if self.is_step_mode: 
            self.exit_step_mode()
        self.points = []
        self.canvas.delete("all")

    def close_event(self):
        self.win.destroy()

    def graham_scan_steps(self, pts):
        # input: np array of shape (n, 2) where n is the # of pts
        # output: ccw convex hull vertices

        # Get a boundary pt
        boundary_pt = pts[np.argmax(pts[:, 1])]
        steps = ['start', boundary_pt]

        # Sort radially w/ respect to boundary pt
        angles = np.arctan2( pts[:, 1] - boundary_pt[1], pts[:, 0] - boundary_pt[0])
        pts = pts[np.argsort(angles)[::-1]]

        # Initialize stack
        stack = [pts[0], pts[1]]
        steps.append(stack.copy())

        for pt in pts[2:]:
            steps.append(("test", stack.copy(), pt))

            while len(stack) >= 2 and orient(stack[-2], stack[-1], pt) <= 0:
                stack.pop()
                steps.append(("popped", stack.copy(), pt))

            stack.append(pt)
            steps.append(("push", stack.copy()))
        
        steps.append(stack.copy())

        return steps


if __name__ == "__main__":
    
    window = tk.Tk()
    board = DisplayBoard(window)
    window.mainloop()


    # def graham_scan(self, pts):
    #     # input: np array of shape (n, 2) where n is the # of pts
    #     # output: ccw convex hull vertices

    #     # Find a boundary point to start: O(n)
    #     boundary_pt = pts[np.argmax(pts[:, 1])]

    #     # Radially sort all other points with respect to the boundary point: O(nlog(n))
    #     angles = np.arctan2( pts[:, 1] - boundary_pt[1], pts[:, 0] - boundary_pt[0])
    #     pts = pts[np.argsort(angles)[::-1]]

    #     # Initialize stack
    #     stack = [pts[0], pts[1]]

    #     # Test all points: O(n) - each point is popped at most once.
    #     for pt in pts[2:]:

    #         # Pop last point in stack if angle with next point is not ccw
    #         while len(stack) >= 2 and orient(stack[-2], stack[-1], pt) <= 0:
    #             stack.pop()

    #         # Push next point
    #         stack.append(pt)

    #     return np.array(stack)