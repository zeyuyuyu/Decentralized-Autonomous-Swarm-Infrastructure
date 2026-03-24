import random
import time
from typing import List

class Swarm:
    def __init__(self, num_agents: int, communication_radius: float):
        self.agents = [Agent(i, self) for i in range(num_agents)]
        self.communication_radius = communication_radius
        self.target_position = None

    def set_target(self, position: List[float]):
        self.target_position = position

    def update(self):
        for agent in self.agents:
            agent.update()

    def get_nearby_agents(self, agent: 'Agent') -> List['Agent']:
        return [a for a in self.agents if a != agent and self.distance(agent, a) <= self.communication_radius]

    def distance(self, agent1: 'Agent', agent2: 'Agent') -> float:
        return ((agent1.position[0] - agent2.position[0])**2 + (agent1.position[1] - agent2.position[1])**2)**0.5

class Agent:
    def __init__(self, id: int, swarm: Swarm):
        self.id = id
        self.swarm = swarm
        self.position = [random.uniform(-10, 10), random.uniform(-10, 10)]
        self.velocity = [0, 0]

    def update(self):
        nearby_agents = self.swarm.get_nearby_agents(self)
        if self.swarm.target_position is not None:
            self.move_towards_target()
        else:
            self.coordinate_with_neighbors(nearby_agents)
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def move_towards_target(self):
        target_x, target_y = self.swarm.target_position
        dx = target_x - self.position[0]
        dy = target_y - self.position[1]
        distance = (dx**2 + dy**2)**0.5
        if distance > 0.1:
            self.velocity[0] = dx / distance * 0.1
            self.velocity[1] = dy / distance * 0.1

    def coordinate_with_neighbors(self, nearby_agents: List['Agent']):
        if nearby_agents:
            avg_x = sum(a.position[0] for a in nearby_agents) / len(nearby_agents)
            avg_y = sum(a.position[1] for a in nearby_agents) / len(nearby_agents)
            self.velocity[0] = (avg_x - self.position[0]) * 0.1
            self.velocity[1] = (avg_y - self.position[1]) * 0.1

if __name__ == '__main__':
    swarm = Swarm(num_agents=50, communication_radius=2.0)
    swarm.set_target([5, 5])
    while True:
        swarm.update()
        time.sleep(0.1)