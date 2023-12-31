import math
import pyray
import random
from raylib import colors

def is_number(a):
    try:
        float(a)
        return True
    except ValueError:
        return False
class text_box:

    def __init__(self, x, y, size, title):
        self.x = x
        self.y = y
        self.size = size
        self.title = title
        self.pointed = False
        self.text = ""

    def text_input(self):
        key = pyray.get_key_pressed()
        if key >= 48 and key <= 57 and len(self.text) < 10:
            self.text += chr(key)
        if key == 259:
            self.text = self.text[:-1]
        if key == 45:
            self.text += '-'
        if key == 46:
            self.text += '.'

    def check_pointed(self):
        self.pointed = pyray.get_mouse_x() > round(self.x + self.size * 3.5) and pyray.get_mouse_x() < round(self.x + self.size * 3.5) + self.size * 7 and pyray.get_mouse_y() > round(self.y - self.size * 0.5) and pyray.get_mouse_y() < round(self.y - self.size * 0.5) + self.size * 2

    def logic(self):
        self.check_pointed()
        if self.pointed:
            self.text_input()
        elif not is_number(self.text):
            self.text = "0"
        self.draw()

    def draw(self):
        pyray.draw_text(self.title, self.x, self.y, self.size, colors.BLACK)
        if self.pointed:
            pyray.draw_rectangle(round(self.x + self.size * 4), round(self.y - self.size * 0.5), self.size * 7, self.size * 2, colors.WHITE)
            pyray.draw_text(self.text, round(self.x + self.size * 4.5), self.y, self.size, colors.BLACK)
        else:
            pyray.draw_rectangle(round(self.x + self.size * 4), round(self.y - self.size * 0.5), self.size * 7, self.size * 2, colors.BLACK)
            pyray.draw_text(self.text, round(self.x + self.size * 4.5), self.y, self.size, colors.WHITE)




class vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class planet:

    def __init__(self, x, y, mass, radius, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.mass = mass
        self.rad = radius
        self.vx = velocity_x
        self.vy = velocity_y
        self.color = colors.WHITE

    def step(self):
        self.x += self.vx
        self.y += self.vy

    def check_colision(self, other):
        a = abs(self.x - other.x)
        b = abs(self.y - other.y)
        s = (a ** 2 + b ** 2) ** 0.5
        if s <= self.rad + other.rad:
            self.color = colors.RED
        else:
            self.color = colors.WHITE

    def speed_change(self, acceleration_x, acceleration_y):
        self.vx += acceleration_x
        self.vy += acceleration_y

    def force_act(self, force):
        ax = force.x / self.mass
        ay = force.y / self.mass
        self.speed_change(ax, ay)

    def draw(self, name):
        pyray.draw_circle(round(self.x + 500), round(self.y + 400), self.rad, self.color)
        pyray.draw_text(name, round(self.x + 500) - 2, round(self.y + 400) + round(self.rad) + 5, 10, colors.GRAY)

    def same(self, other):
        return self.x == other.x and self.y == other.y and self.mass == other.mass and self.rad == other.rad and self.vx == other.vx and self.vy == other.vy


def check_force(planet_a, planet_b):
    if not(planet_a.same(planet_b)):
        a = abs(planet_a.x - planet_b.x)
        b = abs(planet_a.y - planet_b.y)
        s = (a ** 2 + b ** 2) ** 0.5
        f = (planet_a.mass + planet_b.mass) / s
        f *= 5
        angle = math.atan2(planet_b.y - planet_a.y, planet_b.x - planet_a.x)
        fa = vector(f * math.cos(angle), f * math.sin(angle))
        return fa
    else:
        return vector(0 ,0)

def text_input(text):
    key = pyray.get_key_pressed()
    if key >= 48 and key <= 57 and len(text) < 10:
        text += chr(key)
    elif key == 259:
        text = text[:-1]
    elif key == 45:
        text += "-"
    return text


def phase_0(count, phase):
    pyray.clear_background(colors.WHITE)
    count.logic()
    if pyray.gui_button(pyray.Rectangle(425, 500, 300, 100), "START"):
        phase = 1
        count = float(count.text)
    pyray.end_drawing()
    return [count, phase]

def phase_1(count, phase, curent_planet, params, planets):
    pyray.clear_background(colors.WHITE)
    if curent_planet < count:
        for param in params:
            param.logic()
        if pyray.gui_button(pyray.Rectangle(650, 600, 300, 100), "NEXT_PLANET"):
            curent_planet += 1
            planets.append(planet(float(params[0].text), float(params[1].text), float(params[4].text), float(params[5].text), float(params[2].text), float(params[3].text)))
            for param in params:
                param.text = ''
        if pyray.gui_button(pyray.Rectangle(300, 600, 300, 100), "FILL_RANDOM"):
            curent_planet += 1
            planets.append(planet(random.randint(-200, 200), random.randint(-100, 100), random.randint(1, 100), random.randint(3, 20), random.randint(-5, 5), random.randint(-5, 5)))
            for param in params:
                param.text = ''
    else:
        phase = 2
    pyray.end_drawing()
    return count, phase, curent_planet, params, planets



def phase_2(planets, planets_rec, trajectory, trajectory_rec, time_inp, phase):
    pyray.clear_background(colors.WHITE)
    time_inp.logic()
    if pyray.gui_button(pyray.Rectangle(425, 500, 300, 100), "START_SIMULATION"):
        for i in range(int(time_inp.text)):
            new_planets = []
            for plane in planets:
                tr = []
                tr.append(plane.x + 500)
                tr.append(plane.y + 400)
                for planet_b in planets:
                    plane.force_act(check_force(plane, planet_b))
                    if not plane.same(planet_b):
                        plane.check_colision(planet_b)
                plane.step()
                tr.append(plane.x + 500)
                tr.append(plane.y + 400)
                trajectory.append(tr)
                new_planets.append(planet(plane.x, plane.y, plane.mass, plane.rad, plane.vx, plane.vy))
            trajectory_rec.append(list(trajectory))
            planets_rec.append(list(new_planets))
        phase = 3
    pyray.end_drawing()
    return [planets, planets_rec, trajectory, trajectory_rec, time_inp, phase]



def phase_3(planets_rec, trajectory_rec, time, time_speed, time_rec_inp, time_speed_inp, paused):
    pyray.clear_background(colors.BLACK)
    new_time = int(time // 1)

    for i, planet in enumerate(planets_rec[new_time]):
        planet.draw(str(i))
        pyray.draw_text(f"{i}. x:{round(planet.x)} y:{round(planet.y)} vx:{round(planet.vx)} vy:{round(planet.vy)}", 1025, 100 + (i * 25), 10, colors.BLACK)

    for tr in trajectory_rec[new_time]:
        pyray.draw_line(round(tr[0]), round(tr[1]), round(tr[2]), round(tr[3]), colors.GRAY)

    pyray.draw_rectangle(1000, 0, 200, 800, colors.WHITE)

    if not time_speed_inp.pointed and not time_rec_inp.pointed:
        time_rec_inp.text = str(time)
        time_speed_inp.text = str(time_speed * 60)
    time_rec_inp.logic()
    time_speed_inp.logic()
    if not time_speed_inp.pointed and not time_rec_inp.pointed:
        time = float(time_rec_inp.text)
        time_speed = float(time_speed_inp.text) / 60

    if time + time_speed < len(planets_rec) and time + time_speed >= 0 and not paused:
        time += time_speed

    if paused:
        pyray.draw_rectangle(10, 10, 20, 50, colors.WHITE)
        pyray.draw_rectangle(40, 10, 20, 50, colors.WHITE)

    if pyray.get_key_pressed() == 32:
        paused = not paused

    for i, planet in enumerate(planets_rec[new_time]):
        pyray.draw_text(f"{i}. x:{round(planet.x)} y:{round(planet.y)} vx:{round(planet.vx)} vy:{round(planet.vy)}", 1025, 100 + (i * 25), 10, colors.BLACK)

    pyray.end_drawing()

    return [planets_rec, trajectory_rec, time, time_speed, time_rec_inp, time_speed_inp, paused]



def main():
    current_planet = 0
    phase = 0
    trajectory = []
    planets_rec = []
    trajectory_rec = []
    time = 0
    time_speed = 1
    paused = True

    pyray.init_window(1200, 800, "PCalc")
    count = text_box(300, 250, 50, "count:")
    x_inp = text_box(150, 100, 30, "X:")
    y_inp = text_box(150, 175, 30, "Y:")
    vx_inp = text_box(150, 250, 30, "Velo_X:")
    vy_inp = text_box(150, 325, 30, "Velo_Y:")
    mass_inp = text_box(150, 400, 30, "Mass:")
    rad_inp = text_box(150, 475, 30, "Radius:")
    time_inp = text_box(300, 250, 50, "Time:")
    time_rec_inp = text_box(1050, 50, 10, "time")
    time_speed_inp = text_box(1050, 75, 10, "time_sp")
    time_rec_inp.text = str(time)
    time_speed_inp.text = str(time_speed)
    params = [x_inp, y_inp, vx_inp, vy_inp, mass_inp, rad_inp]

    planets = []
    pyray.set_target_fps(60)
    while not pyray.window_should_close():
        if phase == 0:
            [count, phase] = phase_0(count, phase)
        elif phase == 1:
            [count, phase, current_planet, params, planets] = phase_1(count, phase, current_planet, params, planets)
        elif phase == 2:
            [planets, planets_rec, trajectory, trajectory_rec, time_inp, phase] = phase_2(planets, planets_rec, trajectory, trajectory_rec, time_inp, phase)
        elif phase == 3:
            [planets_rec, trajectory_rec, time, time_speed, time_rec_inp, time_speed_inp, paused] = phase_3(planets_rec, trajectory_rec, time, time_speed, time_rec_inp, time_speed_inp, paused)


if __name__ == "__main__":
    main()