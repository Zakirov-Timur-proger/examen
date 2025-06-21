gravitational_constant = 6.67408E-11

class SpaceObject:
    def __init__(self):
        self.type = ""
        self.name = ""
        self.m = 0
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.r = 0
        self.color = ""
        self.image = ""
        self.Fx = 0
        self.Fy = 0
        self.orbit_points = []
        self.orbit_line = None
    def _calculate_force_internal(self, objects):
        """Вычисляет силу, действующую на тело.

            Параметры:

            **body** — тело, для которого нужно вычислить действующую силу.
            **space_objects** — список объектов, которые воздействуют на тело.
        """
        self.Fx = 0
        self.Fy = 0
        for obj in objects:
            if obj == self:
                continue
            r = (((self.x - obj.x) ** 2) + ((self.y - obj.y) ** 2)) ** 0.5
            force = gravitational_constant * obj.m * self.m / r**2
            r_x = obj.x - self.x
            r_y = obj.y - self.y
            self.Fx += force * r_x/r
            self.Fy += force * r_y/r

    def kick(self, c, dt, all_objects, first_time=False):
        if not first_time:
            self._calculate_force_internal(all_objects)
        ax = self.Fx / self.m
        ay = self.Fy / self.m
        self.Vx += ax * c * dt
        self.Vy += ay * c * dt

    def drift(self, d, dt):
        self.x += self.Vx * d * dt
        self.y += self.Vy * d * dt

    def create_object_image(self, space, x, y):
        """Создаёт отображаемый объект звезды.

        Параметры:

        **space** — холст для рисования.
        **star** — объект звезды.
        """
        r = self.r
        self.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=self.color)

    def update_object_position(self, space, window_width, window_height, x, y, scale_factor, default_scale_factor):
        zoom_ratio = scale_factor / default_scale_factor
        display_radius = self.r * zoom_ratio**0.5
        display_radius = max(2, min(display_radius, 50))
        if x + display_radius < 0 or x - display_radius > window_width or y + display_radius < 0 or y - display_radius > window_height:
            space.coords(self.image, -2 * display_radius, -2 * display_radius, -display_radius, -display_radius)  # <<< ИЗМЕНЕНИЕ: более надежный способ спрятать объект
        else:  # <<< ДОБАВЛЕНО: нужен else
            space.coords(self.image, x - display_radius, y - display_radius, x + display_radius, y + display_radius)


class Planet(SpaceObject):
    def __init__(self):
        super().__init__()
        self.type = "planet"

class Star(SpaceObject):
    def __init__(self):
        super().__init__()
        self.type = "star"

class Satellite(SpaceObject):
    def __init__(self):
        super().__init__()
        self.type = "satellite"
        self.parentPlanet = None

def calculate_system_energy(space_objects):
    """
    Вычисляет полную энергию системы (кинетическую и потенциальную).

    Параметры:
    **space_objects** — список объектов системы.
    """
    kinetic_energy = 0
    potential_energy = 0

    # Считаем кинетическую энергию
    for body in space_objects:
        # КЭ = 0.5 * m * v^2
        velocity_squared = body.Vx ** 2 + body.Vy ** 2
        kinetic_energy += 0.5 * body.m * velocity_squared

    for i in range(len(space_objects)):
        for j in range(i + 1, len(space_objects)):
            body1 = space_objects[i]
            body2 = space_objects[j]

            r = ((body1.x - body2.x) ** 2 + (body1.y - body2.y) ** 2) ** 0.5
            if r == 0:
                continue  # Избегаем деления на ноль

            # ПЭ = -G * m1 * m2 / r
            potential_energy -= gravitational_constant * body1.m * body2.m / r

    total_energy = kinetic_energy + potential_energy

    return kinetic_energy, potential_energy, total_energy

if __name__ == "__main__":
    print("This module is not for direct call!")