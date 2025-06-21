# coding: utf-8
# license: GPLv3

"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие графические объекты и перемещающие их на экране, принимают физические координаты
"""

header_font = "Arial-16"
"""Шрифт в заголовке"""

window_width = 800
"""Ширина окна"""

window_height = 800
"""Высота окна"""

scale_factor = 1.0

default_scale_factor = 1.0

camera_x = 0.0

camera_y = 0.0
"""Масштабирование экранных координат по отношению к физическим.
Тип: float
Мера: количество пикселей на один метр."""


def calculate_scale_factor(max_distance):
    """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине"""
    global scale_factor, default_scale_factor
    initial_scale = 0.4*min(window_height, window_width)/max_distance
    scale_factor = initial_scale
    default_scale_factor = initial_scale
    print('Scale factor:', scale_factor)


def scale_x(x):
    """Возвращает экранную **x** координату по **x** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **x** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.

    Параметры:

    **x** — x-координата модели.
    """

    return int((x - camera_x) * scale_factor) + window_width // 2


def scale_y(y):
    """Возвращает экранную **y** координату по **y** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **y** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.
    Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

    Параметры:

    **y** — y-координата модели.
    """

    return window_height // 2 - int((y - camera_y) * scale_factor)  #FIXME: not done yet


def create_star_image(space, star):
    """Создаёт отображаемый объект звезды.

    Параметры:

    **space** — холст для рисования.
    **star** — объект звезды.
    """

    x = scale_x(star.x)
    y = scale_y(star.y)
    r = star.R
    star.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=star.color)


def create_planet_image(space, planet):
    """Создаёт отображаемый объект планеты.

    Параметры:

    **space** — холст для рисования.
    **planet** — объект планеты.
    """
    x = scale_x(planet.x)
    y = scale_y(planet.y)
    r = planet.R
    planet.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=planet.color)
#    pass  # FIXME: сделать как у звезды

def create_satellite_image(space, satellite):
    """Создаёт отображаемый объект планеты.

        Параметры:

        **space** — холст для рисования.
        **satellite** — объект планеты.
    """
    x = scale_x(satellite.x)
    y = scale_y(satellite.y)
    r = satellite.R
    satellite.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=satellite.color)

def update_system_name(space, system_name):
    """Создаёт на холсте текст с названием системы небесных тел.
    Если текст уже был, обновляет его содержание.

    Параметры:

    **space** — холст для рисования.
    **system_name** — название системы тел.
    """
    space.create_text(30, 80, tag="header", text=system_name, font=header_font)

# --- Новые функции управления ---

def zoom_in(event=None): # Добавили event=None, чтобы можно было вызывать с кнопки
    """Приближает вид."""
    global scale_factor
    scale_factor *= 1.5

def zoom_out(event=None):
    """Отдаляет вид."""
    global scale_factor
    scale_factor /= 1.5

def move_camera(direction):
    """Перемещает камеру с помощью стрелок."""
    global camera_x, camera_y
    # Смещение будет зависеть от масштаба, чтобы движение было комфортным
    pan_step = min(window_width, window_height) / scale_factor / 10 # 1/10 ширины экрана

    if direction == "up":
        camera_y += pan_step
    elif direction == "down":
        camera_y -= pan_step
    elif direction == "left":
        camera_x -= pan_step
    elif direction == "right":
        camera_x += pan_step

def reset_view(event=None):
    """Сбрасывает вид к начальному состоянию."""
    global camera_x, camera_y, scale_factor
    camera_x = 0.0
    camera_y = 0.0
    scale_factor = default_scale_factor
    print("View has been reset.")

def update_object_position(space, body):
    """Перемещает отображаемый объект на холсте.

    Параметры:

    **space** — холст для рисования.
    **body** — тело, которое нужно переместить.
    """
    x = scale_x(body.x)
    y = scale_y(body.y)
    r = body.R
    if x + r < 0 or x - r > window_width or y + r < 0 or y - r > window_height:
        space.coords(body.image, window_width + r, window_height + r,
                     window_width + 2*r, window_height + 2*r)  # положить за пределы окна
    space.coords(body.image, x - r, y - r, x + r, y + r)


if __name__ == "__main__":
    print("This module is not for direct call!")
