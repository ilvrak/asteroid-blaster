import numpy as np

class AsteroidBuilder:
    def __init__(self):
        self.center = None
        self.radius = None
        self.polygon = None

    def set_center(self, center):
        self.center = center

    def set_radius(self, radius):
        self.radius = radius

    def build_polygon(self, num_vertices):
        angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False)
        radius_variation = 0.2 * self.radius  # Разброс радиуса

        polygon = []
        for angle in angles:
            radius = self.radius + np.random.uniform(-radius_variation, radius_variation)
            x = self.center[0] + radius * np.cos(angle)
            y = self.center[1] + radius * np.sin(angle)
            polygon.append((x, y))

        self.polygon = polygon

    def get_asteroid(self):
        asteroid = Asteroid()
        asteroid.set_center(self.center)
        asteroid.set_radius(self.radius)
        asteroid.set_polygon(self.polygon)
        return asteroid


builder = AsteroidBuilder()
builder.set_center((0, 0))
builder.set_radius(10)
builder.build_polygon(8)  # 8 вершин полигона
asteroid = builder.get_asteroid()
