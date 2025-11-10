#This code is provided by Hack Club for use in our #accelerate program.
#It is licensed under the MIT License (see LICENSE).
#Feel free to use and modify it as you see fit!

#Remember to install Hackatime, and use it to track your coding time!

#Your goal is to think outside the box. Think about what cool features you could add to this model.

#You have two weeks for this. You must submit your progress by the end of the first week, and your final project by the end of the second week.

import math, threading
from flask import Flask, render_template, jsonify

app = Flask(__name__)

class ThreeBodySimulation:
    def __init__(self, origin_x: float=300, origin_y: float=300):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.G = 1.0
        self.scale = 150.0
        
        x1 = -0.372008640907423
        v1 = 1.21800411067968
        v2 = 0.4531080538336022
        
        self.bodies = [
            {
                'mass': 1.0,
                'x': x1,
                'y': 0.0,
                'vx': 0.0,
                'vy': v1,
                'color': '#1976d2'
            },
            {
                'mass': 1.0,
                'x': 1.0,
                'y': 0.0,
                'vx': 0.0,
                'vy': v2,
                'color': '#ef6c00'
            },
            {
                'mass': 1.0,
                'x': 0.0,
                'y': 0.0,
                'vx': 0.0,
                'vy': -(v1 + v2),
                'color': '#388e3c'
            }
        ]
    
    def step(self, dt: float=0.06):
        forces = [{'fx': 0.0, 'fy': 0.0} for _ in self.bodies]
        
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                dx = self.bodies[j]['x'] - self.bodies[i]['x']
                dy = self.bodies[j]['y'] - self.bodies[i]['y']
                
                distance = math.sqrt(dx**2 + dy**2)
                if distance < 1.0:
                    distance = 1.0
                
                force = self.G * self.bodies[i]['mass'] * self.bodies[j]['mass'] / (distance**2)
                
                fx = force * dx / distance
                fy = force * dy / distance
                
                forces[i]['fx'] += fx
                forces[i]['fy'] += fy
                forces[j]['fx'] -= fx
                forces[j]['fy'] -= fy
        
        for i, body in enumerate(self.bodies):
            ax = forces[i]['fx'] / body['mass']
            ay = forces[i]['fy'] / body['mass']
            
            body['vx'] += ax * dt
            body['vy'] += ay * dt
            
            body['x'] += body['vx'] * dt
            body['y'] += body['vy'] * dt
    
    def get_coords(self):
        return [
            {
                'x': self.origin_x + body['x'] * self.scale,
                'y': self.origin_y + body['y'] * self.scale,
                'color': body['color']
            }
            for body in self.bodies
        ]

simulation = ThreeBodySimulation()

def run_simulation():
    while True:
        simulation.step()
        threading.Event().wait(0.03)

threading.Thread(target=run_simulation, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html', origin_x=simulation.origin_x, origin_y=simulation.origin_y)

@app.route('/coords')
def coords():
    return jsonify(simulation.get_coords())
