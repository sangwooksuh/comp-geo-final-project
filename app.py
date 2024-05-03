import math
import random
import numpy as np
import tkinter as tk
from tkinter import messagebox
from functools import partial


COLORS = [ 
    'dark slate gray', 'dim gray', 'slate gray', 'navy', 'medium slate blue', 'dodger blue', 
    'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue', 
    'light blue',  'pale turquoise', 'dark turquoise', 'turquoise', 'cyan', 
    'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 
    'spring green', 'lawn green', 'medium spring green', 'green yellow', 'lime green', 
    'yellow green', 'forest green', 'olive drab', 'dark khaki', 'khaki', 
    'pale goldenrod', 'light goldenrod yellow', 'light yellow', 'gold', 
    'light goldenrod', 'goldenrod', 'rosy brown', 'indian red', 'saddle brown', 
    'sandy brown', 'salmon', 'light salmon', 'orange', 'dark orange', 'coral', 
    'light coral', 'tomato', 'hot pink', 'deep pink', 'pink','pale violet red', 
    'maroon', 'violet red', 'medium orchid', 'purple', 'medium purple',
]


def partition(pts, r):
    np.random.shuffle(pts)
    H = [[] for _ in range(r)]
    i = 0; j = 0
    while j < len(pts):
        H[i].append(pts[j])
        if i == r - 1:
            i = 0
        else:
            i += 1
        j += 1
    return H


def angle(a, b, c):
    if np.all(b==c) or np.all(a==c): 
        return -np.inf # Do not consider degenerate angles
    v1 = b - a; v2 = c - b
    ang = np.arctan2(np.cross(v1, v2), np.dot(v1, v2))
    ang = ang + 2*np.pi if ang < 0 else ang
    return ang


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

        self.btn_gs = tk.Button(self.frm_btns, text="Graham Scan", command=partial(self.ch_event,"gs"))
        self.btn_gs.grid(row=0, column=1, sticky="n")
        
        self.btn_chan = tk.Button(self.frm_btns, text="Chan's Alg", command=partial(self.ch_event,"chan"))
        self.btn_chan.grid(row=0, column=2, sticky="n")

        self.btn_prev = tk.Button(self.frm_btns, text="Previous", command=partial(self.gs_step_event, "prev"))
        self.btn_next = tk.Button(self.frm_btns, text="Next", command=partial(self.gs_step_event, "next"))
        self.btn_finish = tk.Button(self.frm_btns, text="Finish", command=self.exit_gs_steps)

        self.btn_prev2 = tk.Button(self.frm_btns, text="Previous", command=partial(self.chan_step_event, "prev"))
        self.btn_next2 = tk.Button(self.frm_btns, text="Next", command=partial(self.chan_step_event, "next"))
        self.btn_finish2 = tk.Button(self.frm_btns, text="Finish", command=self.exit_chan_steps)

        self.btn_reset = tk.Button(self.frm_btns, text="Reset", command=self.reset_event)
        self.btn_reset.grid(row=1, column=0, sticky="n")

        self.btn_close = tk.Button(self.frm_btns, text="Close", command=self.close_event)
        self.btn_close.grid(row=1, column=2, sticky="n")

        # Algorithm
        self.is_step_mode = False
        self.current_alg = ''
        self.steps = None
        self.current_step = 0
        self.lbl_gs = [
            tk.Label(self.frm_alg, text="FUNCTION graham_scan(S):", font=("Menlo", 11)), #0
            tk.Label(self.frm_alg, text="    p1 <- lowest point of S", font=("Menlo", 11)), #1
            tk.Label(self.frm_alg, text="    {p1, ... pn} <- sort S radially with respect to p1", font=("Menlo", 11)), #2
            tk.Label(self.frm_alg, text="    H <- new Stack()", font=("Menlo", 11)), #3
            tk.Label(self.frm_alg, text="    H.push(p1); H.push(p2)", font=("Menlo", 11)), #4
            tk.Label(self.frm_alg, text="    FOR i=3 TO n:", font=("Menlo", 11)), #5
            tk.Label(self.frm_alg, text="        WHILE |H| > 1 AND Orient(H.second, H.first, pi) < 0:\t", font=("Menlo", 11)), #6
            tk.Label(self.frm_alg, text="            H.pop()", font=("Menlo", 11)), #7
            tk.Label(self.frm_alg, text="        H.push(pi)", font=("Menlo", 11)), #8
            tk.Label(self.frm_alg, text="    RETURN H.reverse()", font=("Menlo", 11)), #9
        ]
        self.chan_firstline = "FUNCTION chan_hull(S): "
        self.lbl_chan = [
            tk.Label(self.frm_alg, text="FUNCTION chan_hull(S): ", font=("Menlo", 11)), #0
            tk.Label(self.frm_alg, text="    t <- 1", font=("Menlo", 11)), #1
            tk.Label(self.frm_alg, text="    REPEAT:", font=("Menlo", 11)), #2
            tk.Label(self.frm_alg, text="        m <- min(n, 2^(2^t)); r <- ceil(n/m)", font=("Menlo", 11)), #3
            tk.Label(self.frm_alg, text="        {S1, ... Sr} <- partition S s.t. |Si|<=m for all i", font=("Menlo", 11)), #4
            tk.Label(self.frm_alg, text="        FOR i=1 TO r:", font=("Menlo", 11)), #5
            tk.Label(self.frm_alg, text="            Hi <- convex hull of Si", font=("Menlo", 11)), #6
            tk.Label(self.frm_alg, text="        p0 <- (-inf, 0); p1 <- lowest point of S", font=("Menlo", 11)), #7
            tk.Label(self.frm_alg, text="        FOR i=2 TO m+1:", font=("Menlo", 11)), #8
            tk.Label(self.frm_alg, text="            FOR j=1 TO r:", font=("Menlo", 11)), #9
            tk.Label(self.frm_alg, text="                qj <- point in Hj s.t. side p(i-1)qj forms", font=("Menlo", 11)), #10
            tk.Label(self.frm_alg, text="                      least angle with previous side p(i-2)p(i-1)\t", font=("Menlo", 11)), #11            
            tk.Label(self.frm_alg, text="            pi <- point in {q1, ... qr} s.t. p(i-1)pi forms", font=("Menlo", 11)), #12
            tk.Label(self.frm_alg, text="                  least angle with previous side p(i-2)p(i-1)", font=("Menlo", 11)), #13
            tk.Label(self.frm_alg, text="            IF pi == p1:", font=("Menlo", 11)), #14
            tk.Label(self.frm_alg, text="                RETURN {p1, ... p(i-1)}", font=("Menlo", 11)), #15
            tk.Label(self.frm_alg, text="        t <- t+1", font=("Menlo", 11)), #16
        ]

        # Pack frames
        self.frm_display.grid(row=0, column=0)
        self.frm_controls.grid(row=0, column=1, sticky='nsew')
        self.frm_btns.grid(row=0, column=0, sticky='n', padx=10, pady=20)
        self.frm_alg.grid(row=1, column=0, sticky='n')


    def draw_ch(self, ccw_vertices, tag="ch", color="red"):
        n = len(ccw_vertices)
        for i, pt in enumerate(ccw_vertices):
            x1, y1 = pt
            x2, y2 = ccw_vertices[i+1] if i < n - 1 else ccw_vertices[0]
            self.canvas.create_oval(x1-3, y1-3, x1+3, y1+3, outline=color, fill=color, tags=tag)
            self.canvas.create_line(x1, y1, x2, y2, fill=color, tags=tag, width=2)

            # if i >= 4: break


    def rand_event(self, n=16):   
        for _ in range(n):
            x, y = random.randint(15,585), random.randint(15,585)
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black", tags="black")
            self.points.append((x, y))


    def click_event(self, event):

        if self.is_step_mode:
            messagebox.showwarning("Warning: Showing Step", "Finish the current demo process to add more points!")
        self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="black", tags="black")
        self.points.append((event.x, event.y))

    
    def ch_event(self, alg="gs"):
        if len(self.points) > 2:
            self.canvas.delete("ch")
            pts = np.array(self.points)
            
            if alg == "gs":
                self.steps = self.graham_scan(pts, demo=True)
                self.enter_gs_steps()
            if alg == "chan":
                self.steps = self.chan(pts, demo=True)
                self.enter_chan_steps()

        else: 
            messagebox.showwarning(
                "Warning: Not Enough Points", 
                "At least 3 points needed for a convex hull!"
            )


    def gs_step_event(self, direction):

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
            self.canvas.create_oval(x-10, y-10, x+10, y+10, outline="yellow", fill="yellow", tags="steps")
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
            self.lbl_gs[5].config(bg="light yellow")
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

    def chan_step_event(self, direction):

        if self.current_step == len(self.steps) - 1 and direction == "next":
            messagebox.showwarning("Warning: No More Steps", "Last step of algorithm!")
            return
        
        if self.current_step == 0 and direction == "prev":
            messagebox.showwarning("Warning: No Previous Steps", "First step of algorithm!")
            return
                
        self.canvas.delete("steps")
        for lbl in self.lbl_chan:
            lbl.config(bg=self.bg)

        if direction == "next":
            self.current_step += 1
        else:
            self.current_step -= 1

        step = self.steps[self.current_step]
        if step[0] == 'start':
            self.lbl_chan[0].config(text=self.chan_firstline, bg='yellow')
        elif step[0] == 't':
            self.lbl_chan[0].config(text=self.chan_firstline + f" // t: {step[1]}" , bg=self.bg)
            self.lbl_chan[1].config(bg='yellow')
        elif step[0] == 'm':
            self.lbl_chan[0].config(text=self.chan_firstline + f" // t: {step[1][0]}, m: {step[1][1]}, r: {step[1][2]}" , bg=self.bg)
            self.lbl_chan[2].config(bg='light yellow')
            self.lbl_chan[3].config(bg='yellow')
        elif step[0] == 'partition':
            self.lbl_chan[2].config(bg='light yellow')
            self.lbl_chan[4].config(bg='yellow')
            for i, Si in enumerate(step[1]):
                i %= len(COLORS)
                for x, y in Si:
                    self.canvas.create_oval(x-5, y-5, x+5, y+5, outline=COLORS[i], fill=COLORS[i], tag='steps')
        elif step[0] == 'convex_hulls':
            self.lbl_chan[2].config(bg='light yellow')
            self.lbl_chan[5].config(bg='light yellow')
            self.lbl_chan[6].config(bg='yellow')
            for i, Hi in enumerate(step[1]):
                i %= len(COLORS)
                self.draw_ch(Hi, tag="steps", color=COLORS[i])
        elif step[0] == 'start_wrap':
            self.lbl_chan[2].config(bg='light yellow')
            self.lbl_chan[7].config(bg='yellow')
            for i, Hi in enumerate(step[1]):
                i %= len(COLORS)
                self.draw_ch(Hi, tag="steps", color=COLORS[i])
            x, y = step[2]
            self.canvas.create_oval(x-10, y-10, x+10, y+10, outline='black', fill='yellow', tag='steps')
            self.canvas.create_oval(x-3, y-3, x+3, y+3, outline='red', fill='red', tag='steps')
        elif step[0] == 'candidates':
            for i in [2,8,9]:
                self.lbl_chan[i].config(bg='light yellow')
            for i in range(10, 12):
                self.lbl_chan[i].config(bg='yellow')
            for i, Hi in enumerate(step[1]):
                i %= len(COLORS)
                self.draw_ch(Hi, tag="steps", color=COLORS[i])
            for i, (x, y) in enumerate(step[3]):
                self.canvas.create_oval(x-3, y-3, x+3, y+3, outline='red', fill='red', tag='steps')
                if i < len(step[3]) - 1:
                    x2, y2 = step[3][i+1]  
                    self.canvas.create_line(x, y, x2, y2, fill='red', tags='steps', width=2)
            for i, (x, y) in enumerate(step[2]):
                self.canvas.create_oval(x-10, y-10, x+10, y+10, outline='black', fill='yellow', tag='steps')
                self.canvas.create_oval(x-3, y-3, x+3, y+3, outline='blue', fill='blue', tag='steps')
            x, y = step[3][-1]
            self.canvas.create_oval(x-10, y-10, x+10, y+10, outline='black', fill='yellow', tag='steps')
            self.canvas.create_oval(x-3, y-3, x+3, y+3, outline='red', fill='red', tag='steps')
        elif step[0] == 'chosen': # ('chosen', H.copy(), q.copy(), [pt.copy() for pt in hull], pi.copy())
            self.lbl_chan[2].config(bg='light yellow')
            self.lbl_chan[8].config(bg='light yellow')
            self.lbl_chan[12].config(bg='yellow')
            self.lbl_chan[13].config(bg='yellow')
            for i, Hi in enumerate(step[1]):
                i %= len(COLORS)
                self.draw_ch(Hi, tag="steps", color=COLORS[i])
            for i, (x, y) in enumerate(step[3]):
                self.canvas.create_oval(x-3, y-3, x+3, y+3, outline='red', fill='red', tag='steps')
                if i < len(step[3]) - 1:
                    x2, y2 = step[3][i+1]  
                    self.canvas.create_line(x, y, x2, y2, fill='red', tags='steps', width=2)
            for i, (x, y) in enumerate(step[2]):
                x2, y2 = step[3][-1]
                self.canvas.create_oval(x-3, y-3, x+3, y+3, outline='blue', fill='blue', tag='steps')
                self.canvas.create_line(x,y,x2,y2, dash=(4,2), fill='blue', width=2, tags='steps' )
            x, y = step[4]
            x2, y2 = step[3][-1]
            self.canvas.create_oval(x-3, y-3, x+3, y+3, outline='red', fill='red', tag='steps')
            self.canvas.create_line(x,y,x2,y2, fill='red', width=2, tags='steps' )
        elif step[0] == 'hull':
            if direction == 'prev':
                self.lbl_chan[0].config(text=self.chan_firstline + f" // t: {step[3][0]}, m: {step[3][1]}, r: {step[3][2]}")
            self.lbl_chan[2].config(bg='light yellow')
            self.lbl_chan[8].config(bg='light yellow')
            self.lbl_chan[14].config(bg='yellow')
            for i, Hi in enumerate(step[1]):
                i %= len(COLORS)
                self.draw_ch(Hi, tag="steps", color=COLORS[i])
            for i, (x, y) in enumerate(step[2]):
                if i == 0 or i == len(step[2]) - 1:
                    self.canvas.create_oval(x-10, y-10, x+10, y+10, outline='black', fill='yellow', tag='steps') 
                self.canvas.create_oval(x-3, y-3, x+3, y+3, outline='red', fill='red', tag='steps')
                if i < len(step[2]) - 1:
                    x2, y2 = step[2][i+1]  
                    self.canvas.create_line(x, y, x2, y2, fill='red', tags='steps', width=2)
        elif step[0] == 'final':
            self.lbl_chan[2].config(bg='light yellow')
            self.lbl_chan[15].config(bg='yellow')
            for i, Hi in enumerate(step[1]):
                i %= len(COLORS)
                self.draw_ch(Hi, tag="steps", color=COLORS[i])
            for i, (x, y) in enumerate(step[2]):
                self.canvas.create_oval(x-3, y-3, x+3, y+3, outline='red', fill='red', tag='steps')
                x2, y2 = step[2][i+1]  if i < len(step[2]) - 1 else step[2][0]
                self.canvas.create_line(x, y, x2, y2, fill='red', tags='steps', width=2)
        else: # step[0] == 'increment'
            self.lbl_chan[0].config(text=self.chan_firstline + f" // t: {step[1]}" , bg=self.bg)
            self.lbl_chan[2].config(bg='light yellow')
            self.lbl_chan[16].config(bg='yellow')
        

    def enter_gs_steps(self):
        self.is_step_mode = True
        self.btn_rand.grid_forget()
        self.btn_gs.grid_forget()
        self.btn_chan.grid_forget()
        self.btn_prev.grid(row=0, column=0, sticky="n")
        self.btn_next.grid(row=0, column=1, sticky="n")
        self.btn_finish.grid(row=0, column=2, sticky="n")
        self.lbl_gs[0].config(bg="yellow")
        for i, lbl in enumerate(self.lbl_gs):
            lbl.grid(row=i, column=0, sticky="w")

    def enter_chan_steps(self):
        self.is_step_mode = True
        self.current_alg = "chan"
        self.btn_rand.grid_forget()
        self.btn_gs.grid_forget()
        self.btn_chan.grid_forget()
        self.btn_prev2.grid(row=0, column=0, sticky="n")
        self.btn_next2.grid(row=0, column=1, sticky="n")
        self.btn_finish2.grid(row=0, column=2, sticky="n")
        self.lbl_chan[0].config(bg="yellow")
        random.shuffle(COLORS)
        for i, lbl in enumerate(self.lbl_chan):
            lbl.grid(row=i, column=0, sticky="w")


    def exit_gs_steps(self):

        self.is_step_mode = False
        self.current_step = 0

        self.btn_prev.grid_forget()
        self.btn_next.grid_forget()
        self.btn_finish.grid_forget()
        self.btn_rand.grid(row=0, column=0, sticky="n")
        self.btn_gs.grid(row=0, column=1, sticky="n")
        self.btn_chan.grid(row=0, column=2, sticky="n")
        
        self.canvas.delete("steps")
        self.draw_ch(self.steps[-1])

        self.steps = None

        for lbl in self.lbl_gs:
            lbl.config(bg=self.bg)
            lbl.grid_forget()
    
    def exit_chan_steps(self):
        
        self.is_step_mode = False
        self.current_alg = ''
        self.current_step = 0

        self.btn_prev2.grid_forget()
        self.btn_next2.grid_forget()
        self.btn_finish2.grid_forget()
        self.btn_rand.grid(row=0, column=0, sticky="n")
        self.btn_gs.grid(row=0, column=1, sticky="n")
        self.btn_chan.grid(row=0, column=2, sticky="n")
        
        self.canvas.delete("steps")
        self.draw_ch(self.steps[-1][-1])

        self.steps = None

        for lbl in self.lbl_chan:
            lbl.config(bg=self.bg)
            lbl.grid_forget()

        self.lbl_chan[0].config(text=self.chan_firstline)


    def reset_event(self):
        if self.is_step_mode:
            if self.current_alg=='chan': 
                self.exit_chan_steps()
            else:
                self.exit_gs_steps()
        self.points = []
        self.canvas.delete("all")


    def close_event(self):
        self.win.destroy()


    def graham_scan(self, pts, demo=False):
        # input: np array of shape (n, 2) where n is the # of pts
        # output: ccw convex hull vertices

        # Get a boundary pt
        boundary_pt = pts[np.argmax(pts[:, 1])]
        if demo: steps = ['start', boundary_pt]

        # Sort radially w/ respect to boundary pt
        angles = np.arctan2( pts[:, 1] - boundary_pt[1], pts[:, 0] - boundary_pt[0])
        pts = pts[np.argsort(angles)[::-1]]

        # Initialize stack
        stack = [pts[0], pts[1]]
        if demo: steps.append(stack.copy())

        for pt in pts[2:]:
            if demo: steps.append(("test", stack.copy(), pt))

            while len(stack) >= 2 and orient(stack[-2], stack[-1], pt) <= 0:
                stack.pop()
                if demo: steps.append(("popped", stack.copy(), pt))

            stack.append(pt)
            if demo: steps.append(("push", stack.copy()))
        
        if demo: steps.append(stack.copy())

        return steps if demo else np.array(stack)
    


    def chan(self, pts, demo=False):
        # input: np array of shape (n, 2) where n is the # of pts
        # output: ccw convex hull vertices
        if demo: steps = [('start', None)]

        n = len(pts)
        t = 1
        if demo: steps.append(('t',t))
        while True: 
            m = min(n, 2**(2**t))
            r = math.ceil(n / m)
            if demo: steps.append(('m', (t, m, r)))
            
            H = partition(pts, r)
            if demo: steps.append(('partition', H.copy()))
            
            H = [self.graham_scan(np.array(S)) for S in H]
            if demo: steps.append(('convex_hulls', H.copy()))
            
            p0 = np.array([-1, 0])
            p1 = pts[np.argmax(pts[:, 1])]
            hull = [p1]
            if demo: steps.append(('start_wrap', H.copy(), p1.copy()))
            
            for _ in range(2, m+2):
                q = [Hj[np.argmax(np.array([angle(p0, p1, pt) for pt in Hj]))] for Hj in H]
                if demo: steps.append(('candidates', H.copy(), q.copy(), [pt.copy() for pt in hull]))
                
                pi = q[np.argmax(np.array([angle(p0, p1, pt) for pt in q ]))] 
                if demo: steps.append(('chosen', H.copy(), q.copy(), [pt.copy() for pt in hull], pi.copy()))
                
                hull.append(pi)
                if demo: steps.append(('hull', H.copy(), [pt.copy() for pt in hull], (t, m, r)))
                
                if np.all(hull[0] == pi):
                    if demo: steps.append(('final', H.copy(), [pt.copy() for pt in hull][:-1]))
                    return steps if demo else hull[:-1]
                p0, p1 = p1, pi
            t += 1
            if demo: steps.append(('increment', t))

if __name__ == "__main__":
    
    window = tk.Tk()
    board = DisplayBoard(window)
    window.mainloop()
