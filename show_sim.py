import tkinter
from tkinter.filedialog import *
from parse_data import *

class Window:
    def __init__(self, window_width=800, window_height=800):
        self.space_objects = []
        self.physical_time = 0
        self.perform_execution = False
        self.displayed_time = None
        self.time_step = None
        self.statistics_history = []
        self.frame_counter = 0
        self.space = None
        self.window_width = window_width
        self.window_height = window_height
        self.camera_x = 0
        self.camera_y = 0
        self.pan_start_mouse_x = None
        self.pan_start_mouse_y = None
        self.pan_start_camera_x = None
        self.pan_start_camera_y = None
        self.scale_factor = 1.0
        self.default_scale_factor = 1.0
        self.time_speed = None
        self.start_button = None
        self.parser = Parser()
        self.show_orbits = False

        self.theta = 1 / (2 - 2**(1/3))
        self.FR_C1 = self.theta / 2
        self.FR_C2 = (1-self.theta) / 2
        self.FR_D1 = self.theta
        self.FR_D2 = 1-2*self.theta

        self.camera_target = None

    def scale_x(self, x):
        return int((x - self.camera_x) * self.scale_factor) + self.window_width // 2

    def scale_y(self, y):
        return self.window_height // 2 - int((y - self.camera_y) * self.scale_factor)

    def zoom_in(self):  # Добавили event=None, чтобы можно было вызывать с кнопки
        """Приближает вид."""
        self.scale_factor *= 1.5

    def zoom_out(self):
        """Отдаляет вид."""
        self.scale_factor /= 1.5

    def start_pan(self, event):
        if self.camera_target is not None: return
        self.space.focus_set()
        self.pan_start_mouse_x = event.x
        self.pan_start_mouse_y = event.y

        self.pan_start_camera_x = self.camera_x
        self.pan_start_camera_y = self.camera_y

    def pan_view(self, event):
        if self.camera_target is not None: return
        dx = event.x - self.pan_start_mouse_x
        dy = event.y - self.pan_start_mouse_y

        physical_dx = dx / self.scale_factor
        physical_dy = dy / self.scale_factor

        self.camera_x = self.pan_start_camera_x - physical_dx
        self.camera_y = self.pan_start_camera_y + physical_dy

    def stop_pan(self):
        self.pan_start_mouse_x = None
        self.pan_start_mouse_y = None
        self.pan_start_camera_x = None
        self.pan_start_camera_y = None

    def reset_view(self):
        """Сбрасывает вид к начальному состоянию."""
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.scale_factor = self.default_scale_factor
        print("View has been reset.")

    def select_camera_target(self, event):
        mouse_x, mouse_y = event.x, event.y
        physical_x = (mouse_x - self.window_width / 2) / self.scale_factor + self.camera_x
        physical_y = -(mouse_y - self.window_height / 2) / self.scale_factor + self.camera_y
        target_found = None

        for obj in reversed(self.space_objects):
            zoom_ratio = self.scale_factor / self.default_scale_factor
            try:
                display_radius_px = obj.r * (zoom_ratio ** 0.5)
            except ValueError:
                display_radius_px = obj.r

            display_radius_px = max(2, min(display_radius_px, 50))

            if self.scale_factor == 0: continue
            physical_radius = display_radius_px / self.scale_factor

            distance_sq = (obj.x - physical_x) ** 2 + (obj.y - physical_y) ** 2
            if distance_sq < physical_radius ** 2:
                target_found = obj
                break
        self.camera_target = target_found
        if self.camera_target:
            print(f"Камера привязана к {self.camera_target.name}")
        else:
            print("Камера отвязана. Свободный режим.")

    def drop_camera_target(self):
        self.camera_target = None

    def toggle_orbits_visibility(self):
        """Переключает видимость орбит и обновляет их на холсте."""
        # Инвертируем флаг
        self.show_orbits = not self.show_orbits

        # Проходим по всем объектам и либо показываем, либо прячем их линии орбит
        for body in self.space_objects:
            if body.orbit_line is not None:
                if self.show_orbits:
                    # 'normal' делает объект видимым
                    self.space.itemconfigure(body.orbit_line, state='normal')
                else:
                    # 'hidden' делает объект невидимым
                    self.space.itemconfigure(body.orbit_line, state='hidden')

        print(f"Orbits visibility set to: {self.show_orbits}")

    def calculate_scale_factor(self, max_distance):
        """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине"""
        initial_scale = 0.4 * min(self.window_height, self.window_width) / max_distance
        self.scale_factor = initial_scale
        self.default_scale_factor = initial_scale
        print('Scale factor:', self.scale_factor)

    def execution(self):
        if self.camera_target is not None:
            self.camera_x = self.camera_target.x
            self.camera_y = self.camera_target.y

        for obj in self.space_objects:
            obj.kick(self.FR_C1, self.time_step.get(), self.space_objects, True)

        for obj in self.space_objects:
            obj.drift(self.FR_D1, self.time_step.get())

        for obj in self.space_objects:
            obj.kick(self.FR_C2, self.time_step.get(), self.space_objects)

        for obj in self.space_objects:
            obj.drift(self.FR_D2, self.time_step.get())

        for obj in self.space_objects:
            obj.kick(self.FR_C2, self.time_step.get(), self.space_objects)

        for obj in self.space_objects:
            obj.drift(self.FR_D1, self.time_step.get())

        for obj in self.space_objects:
            obj.kick(self.FR_C1, self.time_step.get(), self.space_objects)

        if self.frame_counter % 10 == 0:  # Сбор статистики каждый 10 кадр для оптимизации
            ke, pe, te = calculate_system_energy(self.space_objects)
            stats_point = {
                "time": self.physical_time,
                "ke": ke,
                "pe": pe,
                "te": te
            }
            self.statistics_history.append(stats_point)
        self.frame_counter += 1

        for body in self.space_objects:
            screen_x = self.scale_x(body.x)
            screen_y = self.scale_y(body.y)
            body.orbit_points.append((body.x, body.y))
            if len(body.orbit_points) > 500:
                body.orbit_points.pop(0)

            if self.show_orbits and len(body.orbit_points) > 1:
                screen_points = []
                for p_x, p_y in body.orbit_points:
                    screen_points.append(self.scale_x(p_x))
                    screen_points.append(self.scale_y(p_y))

                if body.orbit_line is None:
                    if body.type in ['planet', 'satellite']:
                        body.orbit_line = self.space.create_line(
                            screen_points, fill=body.color, width=1)
                        self.space.tag_lower(body.orbit_line)
                else:
                    self.space.coords(body.orbit_line, screen_points)

            body.update_object_position(
                self.space, self.window_width, self.window_height,
                screen_x, screen_y,
                self.scale_factor, self.default_scale_factor
            )

        self.physical_time += self.time_step.get()
        self.displayed_time.set("%.1f" % self.physical_time + " seconds gone")

        if self.perform_execution:
            self.space.after(101 - int(self.time_speed.get()), self.execution)

    def start_execution(self):
        """Обработчик события нажатия на кнопку Start.
        Запускает циклическое исполнение функции execution.
        """
        self.perform_execution = True
        self.start_button['text'] = "Pause"
        self.start_button['command'] = self.stop_execution

        self.execution()
        print('Started execution...')

    def stop_execution(self):
        """Обработчик события нажатия на кнопку Start.
        Останавливает циклическое исполнение функции execution.
        """
        self.perform_execution = False
        self.start_button['text'] = "Start"
        self.start_button['command'] = self.start_execution
        print('Paused execution.')

    def open_file_dialog(self):
        """Открывает диалоговое окно выбора имени файла и вызывает
        функцию считывания параметров системы небесных тел из данного файла.
        Считанные объекты сохраняются в глобальный список space_objects
        """
        self.statistics_history.clear()
        self.frame_counter = 0
        self.perform_execution = False
        for obj in self.space_objects:
            self.space.delete(obj.image)  # удаление старых изображений планет
            if obj.orbit_line is not None:
                self.space.delete(obj.orbit_line)
        in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
        if not in_filename:
            return
        self.space_objects = self.parser.read_space_objects_data_from_file(in_filename)

        print("Инициализация начальных сил...")
        for obj in self.space_objects:
            obj._calculate_force_internal(self.space_objects)

        max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in self.space_objects])
        self.calculate_scale_factor(max_distance)

        for obj in self.space_objects:
            obj.create_object_image(self.space, self.scale_x(obj.x), self.scale_y(obj.y))

    def save_stats_dialog(self):
        """Открывает диалог сохранения файла и записывает статистику."""
        if not self.statistics_history:
            print("No statistics to save yet.")
            return

        out_filename = asksaveasfilename(filetypes=(("CSV file", ".csv"),))
        if out_filename:
            self.parser.write_statistics_to_file(out_filename, self.statistics_history)
            print(f"Statistics saved to {out_filename}")

    def save_file_dialog(self):
        """Открывает диалоговое окно выбора имени файла и вызывает
        функцию считывания параметров системы небесных тел из данного файла.
        Считанные объекты сохраняются в глобальный список space_objects
        """
        out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
        self.parser.write_space_objects_data_to_file(out_filename, self.space_objects)

def main():
    window = Window()
    print('Modelling started!')
    window.physical_time = 0

    root = tkinter.Tk()
    window.space = tkinter.Canvas(root, width=window.window_width, height=window.window_height, bg="black")

    window.space.pack(side=tkinter.TOP)

    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    window.space.focus_set()

    window.space.bind("<MouseWheel>", lambda event: window.zoom_in() if event.delta > 0 else window.zoom_out())

    window.space.bind("<Button-1>", window.start_pan)
    window.space.bind("<B1-Motion>", window.pan_view)
    window.space.bind("<ButtonRelease-1>", lambda event: window.stop_pan())

    window.space.bind("<Double-Button-1>", window.select_camera_target)
    window.space.bind("<Escape>", lambda event: window.drop_camera_target())

    reset_view_button = tkinter.Button(frame, text="Reset View", command=window.reset_view)
    reset_view_button.pack(side=tkinter.LEFT)

    window.start_button = tkinter.Button(frame, text="Start", command=window.start_execution, width=6)
    window.start_button.pack(side=tkinter.LEFT)

    window.time_step = tkinter.DoubleVar()
    window.time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=window.time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    window.time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=window.time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(frame, text="Open file...", command=window.open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    save_stats_button = tkinter.Button(frame, text="Save Stats...", command=window.save_stats_dialog)
    save_stats_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(frame, text="Save to file...", command=window.save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)
    toggle_orbits_button = tkinter.Button(frame, text="Toggle Orbits", command=window.toggle_orbits_visibility)
    toggle_orbits_button.pack(side=tkinter.LEFT)

    window.displayed_time = tkinter.StringVar()
    window.displayed_time.set(str(window.physical_time) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=window.displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    main()