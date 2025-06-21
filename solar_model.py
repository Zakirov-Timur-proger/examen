# coding: utf-8
# license: GPLv3
gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.
    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5
        force = gravitational_constant * obj.m * body.m / (r**2)
        r_x = obj.x - body.x
        r_y = obj.y - body.y
        body.Fx += force * r_x/r # FIXME: нужно вывести формулу...
        body.Fy += force * r_y/r  # FIXME: нужно вывести формулу...


def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    **dt** — шаг по времени
    """

    ax = body.Fx/body.m
    body.x += body.Vx * dt + (ax*dt**2)/2  # FIXME: не понимаю как менять...
    body.Vx += ax*dt

    ay = body.Fy / body.m
    body.y += body.Vy * dt + (ay * dt ** 2) / 2  # FIXME: не понимаю как менять...
    body.Vy += ay * dt
    # FIXME: not done recalculation of y coordinate!


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список объектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    """

    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt)


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
