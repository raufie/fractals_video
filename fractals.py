import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import TextBox, Button
from numpy.polynomial import polynomial as P

COLORS = np.array([[142/255, 1.0, 0.0], [97/255, 0.0, 1.0],
                  [1.0, 0.0, 89.0/255], [1.0, 220/255, 0.0], [0.0, 1.0, 216/255], [1.0, 0.0, 240/255]])


def get_color():
    return [np.random.random(), np.random.random(), np.random.random()]


COLORS = [get_color() for _ in range(25)]


def f(z):
    return z**6 - 1


def fp(z):
    return 6*z**5


roots = np.roots([1, 0, 0, 0, 0, 0, -1])


def make_arr_from_Z(Z, nx, ny, _colors, roots):
    colored_arr = np.zeros(shape=(nx, ny, 3))
    eps = 0.001
    Z_T = []
    for r in roots:
        Z_T.append(abs(Z-r) < eps)

    for i in range(nx):
        for j in range(ny):
            for k, z_t in enumerate(Z_T):
                if z_t[i][j]:
                    colored_arr[i][j] = _colors[k]
                    # colored_arr[i][j] = get_color()

    return colored_arr


def generate_fractals(f, fp, roots, xmin=-2, xmax=2, ymin=-2, ymax=2, nx=500, ny=500, a=1.0, _colors=None):
    if _colors == None:
        _colors = COLORS
    X = np.linspace(xmin, xmax, nx)
    Y = np.linspace(ymin, ymax, ny)
    X, Y = np.meshgrid(X, Y)

    Z = X + 1j*Y
    iters = 50
    for i in range(iters):
        Z = Z - a*(f(Z)/fp(Z))

    colored_arr = make_arr_from_Z(Z, nx, ny, _colors, roots)
    return colored_arr


xmin = -2
xmax = 2
ymin = -2
ymax = 2
nx = 250
ny = 250


class Fractal:
    def __init__(self):
        self.xmin = -2
        self.xmax = 2
        self.ymin = -2
        self.ymax = 2

        self.n = 250
        self.dx = self.xmax
        self.dy = self.ymax

        self.f = [1, 0, 0, 0, 0, 0, -1]
        self.poly = np.poly1d(self.f)
        self.zoom = 0.3

        self.colors = COLORS
        arr = generate_fractals(self.poly, self.poly.deriv(), np.roots(self.f), xmin=self.xmin, ymin=self.ymin,
                                xmax=self.xmax, ymax=self.ymax, nx=nx, ny=ny)
        self.arr = arr
        fig, ax = plt.subplots(1, 1)
        self.img_obj = ax.imshow(arr)
        fig.canvas.mpl_connect('button_press_event', lambda e: self.on_click(
            e, self.xmin, self.xmax, self.ymin, self.ymax, self.img_obj))
        fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        # ax.callbacks.connect(
        #     "xlim_changed", lambda e: on_zoom(e, xmin, xmax, ymin, ymax, img_obj))
        # ax.callbacks.connect('ylim_changed', on_ylims_change)
        axbox = plt.axes([0.4, 0.90, 0.6, 0.075])
        btnbox = plt.axes([0.0, 0.90, 0.3, 0.075])
        resbox = plt.axes([0.65, 0.90, 0.9, 0.075])
        self.text_box = TextBox(axbox, 'POLYNOMIAL', initial="1,0,0,0,0,0,-1")
        self.res = TextBox(resbox, 'res', initial="200")
        btn = Button(btnbox, 'REDRAW')
        btn.on_clicked(self.text_change)
        self.res.on_submit(self.on_res_change)
        plt.show()

    def on_click(self, e, xmin, xmax, ymin, ymax, img_obj):
        if e.xdata == None or e.ydata == None or e.button != 3:
            return
        # IF IT IS RIGHT CLICK ZOOM IN...
        print(e.button)
        self.dx -= (self.xmax - self.xmin)*0.5*self.zoom
        self.dy -= (self.ymax - self.ymin)*0.5*self.zoom
        x = e.xdata
        y = e.ydata
        print(x, y)

        # based on nx/ny get new x1, x2, y1, y2
        pc_x, pc_y = x/nx, y/ny
        Px = self.xmin + (self.xmax - self.xmin)*pc_x
        Py = self.ymin + (self.ymax - self.ymin)*pc_y

        self.xmax = Px + self.dx
        self.xmin = Px - self.dx
        self.ymin = Py - self.dy
        self.ymax = Py + self.dy
        # print(self.xmin, self.xmax)
        # print(x1, x2)
        arr = generate_fractals(self.poly, self.poly.deriv(), np.roots(self.f), xmin=self.xmin, ymin=self.ymin,
                                xmax=self.xmax, ymax=self.ymax, nx=self.n, ny=self.n, _colors=self.colors)

        # ax.callbacks.connect(
        #     "xlim_changed", lambda e: on_zoom(e, xmin, xmax, ymin, ymax, img_obj))
        # ax.callbacks.connect('ylim_changed', on_ylims_change)
        # plt.show()

        img_obj.set_data(arr)
        self.arr = arr
        plt.draw()

    def text_change(self, e):
        try:
            text = self.text_box.text
            values = text.split(",")
            values = [int(i) for i in values]
            self.f = values
            self.poly = np.poly1d(values)
            self.xmin = -5.0
            self.xmax = 5.0
            self.ymin = -5.0
            self.ymax = 5.0
            COLORS = [get_color() for _ in range(25)]
            self.colors = COLORS
            arr = generate_fractals(self.poly, self.poly.deriv(), np.roots(self.f), xmin=self.xmin, ymin=self.ymin,
                                    xmax=self.xmax, ymax=self.ymax, nx=self.n, ny=self.n, _colors=COLORS)

            self.img_obj.set_data(arr)
            self.arr = arr
            plt.draw()
        except Exception as E:
            print(E)
            print("INCORRECT SYNTAX - CORRECT EXAMPLE= 1,1,0,1,1")

    def on_res_change(self, e):
        try:
            n = int(self.res.text)
            self.n = n
            arr = generate_fractals(self.poly, self.poly.deriv(), np.roots(self.f), xmin=self.xmin, ymin=self.ymin,
                                    xmax=self.xmax, ymax=self.ymax, nx=self.n, ny=self.n, _colors=self.colors)

            self.img_obj.set_data(arr)
            self.arr = arr
            plt.draw()
        except Exception as E:
            print(E)
            print("expecting an int")

    def on_key_press(self, e):
        if e.key == "p":
            plt.imsave(f"{int(np.random.random()*1e6)}.png", self.arr)
            # self.img_obj.imsave("t.png")


Fractal()
