import math
import random

G = 6.67408E-11
pi = 3.1415926535
black_hole_mass = 1E35
sun_mass = 1.989E30
earth_mass = 5.972E24

star_mass_min = 0.08 * sun_mass
star_mass_max = 20.0 * sun_mass
planet_mass_min = 0.5 * earth_mass
planet_mass_max = 1500 * earth_mass
satellite_mass_ratio_min = 0.0001
satellite_mass_ratio_max = 0.01

star_orbit_radius_min = 2E14
star_orbit_radius_max = 1E15
planet_orbit_radius_min = 0.5 * 1.496E11
planet_orbit_radius_max = 50.0 * 1.496E11
satellite_orbit_radius_min = 3.844E8
satellite_orbit_radius_max = 2.0E9


def calculate_orbital_velocity(center_mass, radius):
    """Вспомогательная функция для расчета скорости."""
    if radius == 0:
        return 0
    return (G * center_mass / radius) ** 0.5


with open('mega_system_v2.txt', 'w') as f:
    print(f"Star0 20 black {black_hole_mass} 0 0 0 0\n", file=f)

    for i in range(1, 8):
        star_num = i
        is_odd_star = (star_num % 2 != 0)

        angle_star = random.uniform(0, 2 * pi)
        r_star = star_orbit_radius_min + (star_num - 1) * (star_orbit_radius_max - star_orbit_radius_min) / 6
        x_star = r_star * math.cos(angle_star)
        y_star = r_star * math.sin(angle_star)
        m_star = random.uniform(star_mass_min, star_mass_max)

        v_star_mag = calculate_orbital_velocity(black_hole_mass, r_star)
        vx_star = v_star_mag * -math.sin(angle_star)
        vy_star = v_star_mag * math.cos(angle_star)

        print(f"Star{star_num} 5 blue {m_star} {x_star} {y_star} {vx_star} {vy_star}\n", file=f)

        num_planets = 30 if is_odd_star else 15
        planets_per_orbit = 4 if is_odd_star else 3

        orbit_masses = {}

        num_planets_copy = num_planets

        planets_count_on_orbits = []

        orbit_num = 0

        while num_planets_copy > 0:
            curr_num = random.randint(1, min(planets_per_orbit, num_planets_copy))
            planets_count_on_orbits.append(curr_num)
            num_planets_copy -= curr_num
            orbit_num += 1
            orbit_masses[orbit_num] = random.uniform(planet_mass_min, planet_mass_max)

        planet_num_in_system = 0

        for i in range(1,len(planets_count_on_orbits)+1):
            for j in range(planets_count_on_orbits[i-1]):
                planet_num_in_system += 1

                pos_on_orbit = j
                is_odd_orbit = (i % 2 != 0)

                direction_planet = -1 if is_odd_orbit else 1

                total_orbits = (num_planets - 1) // planets_per_orbit
                orbit_step = (planet_orbit_radius_max - planet_orbit_radius_min) / len(planets_count_on_orbits) if total_orbits > 0 else 0
                r_planet = planet_orbit_radius_min + (i-1) * orbit_step

                angle_planet = (2 * pi / planets_count_on_orbits[i-1]) * pos_on_orbit

                x_planet = x_star + r_planet * math.cos(angle_planet)
                y_planet = y_star + r_planet * math.sin(angle_planet)
                m_planet = orbit_masses[i]

                v_planet_rel_mag = calculate_orbital_velocity(m_star, r_planet)
                vx_planet_rel = v_planet_rel_mag * -math.sin(angle_planet) * direction_planet
                vy_planet_rel = v_planet_rel_mag * math.cos(angle_planet) * direction_planet
                vx_planet_abs = vx_star + vx_planet_rel
                vy_planet_abs = vy_star + vy_planet_rel

                print(
                    f"Planet{planet_num_in_system}_{star_num} 3 green {m_planet} {x_planet} {y_planet} {vx_planet_abs} {vy_planet_abs}\n",
                    file=f)

                num_satellites = 0
                if is_odd_star and planet_num_in_system in [10, 20, 30]:
                    num_satellites = 2
                elif not is_odd_star and planet_num_in_system in [5, 10, 15]:
                    num_satellites = 1

                if num_satellites > 0:
                    direction_sat = -1

                    for k in range(num_satellites):
                        satellite_num_in_system = k + 1

                        angle_sat = (2 * pi / num_satellites) * k
                        r_sat = random.uniform(satellite_orbit_radius_min, satellite_orbit_radius_max)
                        m_sat = m_planet * random.uniform(satellite_mass_ratio_min, satellite_mass_ratio_max)

                        x_sat = x_planet + r_sat * math.cos(angle_sat)
                        y_sat = y_planet + r_sat * math.sin(angle_sat)

                        v_sat_rel_mag = calculate_orbital_velocity(m_planet, r_sat)
                        vx_sat_rel = v_sat_rel_mag * -math.sin(angle_sat) * direction_sat
                        vy_sat_rel = v_sat_rel_mag * math.cos(angle_sat) * direction_sat
                        vx_sat_abs = vx_planet_abs + vx_sat_rel
                        vy_sat_abs = vy_planet_abs + vy_sat_rel

                        print(
                            f"Satellite{satellite_num_in_system}_{planet_num_in_system}_{star_num} 1 white {m_sat} {x_sat} {y_sat} {vx_sat_abs} {vy_sat_abs}\n",
                            file=f)

    f.close()
print("Завершено формирование звездной системы")