# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet

import re

def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            match = re.search(r"Star|Planet", line)
            if match.group() == "Star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif match.group() == "Planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return objects


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.
    Входная строка должна иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты звезды, (Vx, Vy) — скорость.
    Пример строки:
    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описанием звезды.
    **star** — объект звезды.
    """
    match = line.split()

    match[1], match[3], match[4], match[5], match[6], match[7] = float(match[1]), float(match[3]), float(
        match[4]), float(
        match[5]), float(match[6]), float(match[7])

    star.name = match[0]
    star.r = match[1]
    star.color = match[2]
    star.m = match[3]
    star.x = match[4]
    star.y = match[5]
    star.Vx = match[6]
    star.Vy = match[7]

def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
    Пример строки:
    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """
    match = line.split()

    match[1], match[3], match[4], match[5], match[6], match[7] = float(match[1]), float(match[3]), float(
        match[4]), float(
        match[5]), float(match[6]), float(match[7])

    planet.name = match[0]
    planet.r = match[1]
    planet.color = match[2]
    planet.m = match[3]
    planet.x = match[4]
    planet.y = match[5]
    planet.Vx = match[6]
    planet.Vy = match[7]


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            print(f"{obj.name} {obj.r} {obj.color} {obj.m} {obj.x} {obj.y} {obj.Vx} {obj.Vy}\n", file=out_file)


def write_statistics_to_file(output_filename, stats_history):
    """Сохраняет собранную статистику (энергию, время) в CSV-файл.

    Параметры:

    **output_filename** — имя выходного файла.
    **stats_history** — список словарей со статистикой.
    """
    with open(output_filename, 'w') as out_file:
        # Записываем заголовок CSV-файла
        out_file.write("Time,KineticEnergy,PotentialEnergy,TotalEnergy\n")

        # Записываем каждую точку данных
        for stats_point in stats_history:
            time = stats_point["time"]
            ke = stats_point["ke"]
            pe = stats_point["pe"]
            te = stats_point["te"]
            # Форматируем строку и записываем. Используем научную нотацию (e) для больших чисел.
            out_file.write(f"{time:.4f},{ke:.4e},{pe:.4e},{te:.4e}\n")

if __name__ == "__main__":
    print("This module is not for direct call!")
