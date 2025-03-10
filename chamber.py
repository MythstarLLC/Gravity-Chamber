import tkinter as tk
import math
import random

class GravitySimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravity Simulation")
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack()

        # Physics parameters
        self.time_step = 0.02  # seconds
        self.scale = 20  # pixels per meter
        
        # Increase gravitational constant for a stronger pull.
        self.G = 1.0
        
        # List to store celestial bodies
        self.bodies = []
        
        # Add controls
        self.add_controls()
        
        # Start animation
        self.animate()

    def add_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack()
        
        tk.Button(control_frame, text="Add Planet", command=self.add_planet).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Add Star", command=self.add_star).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Clear", command=self.clear_balls).pack(side=tk.LEFT)

    def add_body(self, body_type):
        # Random initial position and velocity
        x = random.randint(50, 750)
        y = random.randint(50, 200)
        vx = random.uniform(-1, 1)
        vy = random.uniform(-1, 1)
        
        if body_type == 'star':
            mass = random.uniform(50, 100)
            color = 'yellow'
            radius = 15  # larger for stars
        else:
            mass = random.uniform(5, 20)
            color = 'white'
            radius = 10  # smaller for planets
        
        body = {
            'id': self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color),
            'x': x,
            'y': y,
            'vx': vx,
            'vy': vy,
            'mass': mass,
            'r': radius
        }
        self.bodies.append(body)

    def add_planet(self):
        self.add_body('planet')

    def add_star(self):
        self.add_body('star')

    def clear_balls(self):
        # Clear bodies and grid elements
        for body in self.bodies:
            self.canvas.delete(body['id'])
        self.bodies.clear()
        self.canvas.delete("grid")

    def potential_gradient(self, x, y):
        # Compute net gradient from all bodies using a softened inverse-cube law.
        gx, gy = 0, 0
        epsilon = 1e-3
        for body in self.bodies:
            dx = x - body['x']
            dy = y - body['y']
            r = math.sqrt(dx*dx + dy*dy) + epsilon
            factor = self.G * body['mass'] / (r**3)
            gx += factor * dx
            gy += factor * dy
        return gx, gy

    def draw_grid(self):
        # Draw grid lines that distort based on the gravitational potential gradient.
        dist_factor = 20  # distortion factor
        grid_spacing = 50
        width = int(self.canvas['width'])
        height = int(self.canvas['height'])
        step = 10  # sampling step along each line
        
        # Draw vertical grid lines
        for x in range(0, width + grid_spacing, grid_spacing):
            points = []
            for y in range(0, height + step, step):
                gx, gy = self.potential_gradient(x, y)
                new_x = x + dist_factor * gx
                new_y = y + dist_factor * gy
                points.extend((new_x, new_y))
            self.canvas.create_line(*points, fill='gray', tags="grid")
        
        # Draw horizontal grid lines
        for y in range(0, height + grid_spacing, grid_spacing):
            points = []
            for x in range(0, width + step, step):
                gx, gy = self.potential_gradient(x, y)
                new_x = x + dist_factor * gx
                new_y = y + dist_factor * gy
                points.extend((new_x, new_y))
            self.canvas.create_line(*points, fill='gray', tags="grid")

    def animate(self):
        # Update physics for each body using gravitational attraction among bodies.
        dt = self.time_step
        width = int(self.canvas['width'])
        height = int(self.canvas['height'])
        epsilon = 1e-3

        # Compute acceleration for each body
        for i, body in enumerate(self.bodies):
            ax, ay = 0, 0
            for j, other in enumerate(self.bodies):
                if i == j:
                    continue
                dx = other['x'] - body['x']
                dy = other['y'] - body['y']
                r = math.sqrt(dx*dx + dy*dy) + epsilon
                # Newton's law: F = G * m1*m2 / r^2; acceleration = F/m1 = G*m2/r^2; direction normalized by r.
                a = self.G * other['mass'] / (r**2)
                ax += a * (dx / r)
                ay += a * (dy / r)
            # Update velocity and position
            body['vx'] += ax * dt
            body['vy'] += ay * dt
            body['x'] += body['vx'] * dt * self.scale
            body['y'] += body['vy'] * dt * self.scale

            # Wrap-around boundaries
            if body['x'] < 0:
                body['x'] += width
            elif body['x'] > width:
                body['x'] -= width

            if body['y'] < 0:
                body['y'] += height
            elif body['y'] > height:
                body['y'] -= height

            # Update the body's position on canvas
            self.canvas.coords(body['id'], 
                               body['x']-body['r'], body['y']-body['r'],
                               body['x']+body['r'], body['y']+body['r'])
        # Redraw grid each frame
        self.canvas.delete("grid")
        self.draw_grid()
        self.root.after(20, self.animate)  # Update every 20ms

if __name__ == "__main__":
    root = tk.Tk()
    app = GravitySimulation(root)
    root.mainloop()