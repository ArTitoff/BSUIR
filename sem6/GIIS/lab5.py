import tkinter as tk
import math

class SimpleZoomGrid:
    def __init__(self, root):
        self.root = root
        self.root.title("Сетка с зумом")
        self.offset_x = self.offset_y = 0
        self.window_width, self.window_height = 1600, 1200
        self.grid_cols, self.grid_rows = 200, 100
        self.cell_size = 50

        self.polygons = []          # точки полигонов (для закраски)
        self.polygons_vertex = []   # вершины полигонов
        self.lines = []              # линии
        self.filled_cells = [[False] * self.grid_cols for _ in range(self.grid_rows)]

        # Кнопки
        btn_frame = tk.Frame(root, bg='lightgray')
        btn_frame.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

        tk.Button(btn_frame, text="Построить полигон", command=self.create_polygon).pack(pady=5)
        tk.Button(btn_frame, text="Закончить полигон", command=self.end_poligon).pack(pady=5)
        tk.Button(btn_frame, text="Очистить всё", command=self.clear_all).pack(pady=5)
        tk.Button(btn_frame, text="Проверить выпуклость", command=self.check_convexity).pack(pady=5)
        tk.Button(btn_frame, text="Показать нормали", command=self.show_normals).pack(pady=5)
        tk.Button(btn_frame, text="Грэхема", command=lambda: self.build_convex_hull(False)).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Джарвиса", command=lambda: self.build_convex_hull(True)).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Построить линию", command=self.create_line).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Найти пересечение", command=self.line_intersection).pack(fill=tk.X, pady=2)

        # Проверка точки
        point_frame = tk.Frame(btn_frame, bg='lightgray')
        point_frame.pack(fill=tk.X, pady=10)
        tk.Label(point_frame, text="Проверка точки:", bg='lightgray').pack()
        coord_frame = tk.Frame(point_frame, bg='lightgray')
        coord_frame.pack()
        tk.Label(coord_frame, text="X:", bg='lightgray').pack(side=tk.LEFT)
        self.point_x_entry = tk.Entry(coord_frame, width=5)
        self.point_x_entry.pack(side=tk.LEFT, padx=2)
        tk.Label(coord_frame, text="Y:", bg='lightgray').pack(side=tk.LEFT)
        self.point_y_entry = tk.Entry(coord_frame, width=5)
        self.point_y_entry.pack(side=tk.LEFT, padx=2)
        tk.Button(point_frame, text="Проверить точку", command=self.check_point_in_polygon).pack(fill=tk.X, pady=5)

        self.canvas = tk.Canvas(root, width=self.window_width, height=self.window_height, bg='white')
        self.canvas.pack()

        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Button-4>", self.zoom)
        self.canvas.bind("<Button-5>", self.zoom)
        self.canvas.bind("<ButtonPress-3>", self.on_press)
        self.canvas.bind("<B3-Motion>", self.on_drag)


        self.draw_grid()


    def create_polygon(self):
        self.canvas.bind("<Button-1>", self.fill_cell)
        self.polygons.append([])
        self.polygons_vertex.append([])


    def fill_cell(self, event):
        cell = self.get_cell_coords(event.x, event.y)
        if cell:
            gx, gy = cell
            self.polygons_vertex[-1].append((gx, gy))
            if (gx, gy) not in self.polygons[-1]:
                if self.polygons[-1]:
                    x1, y1 = self.polygons[-1][-1]
                    for p in self.dda_algorithm(x1, y1, gx, gy)[1:]:
                        self.polygons[-1].append(p)
                        self.filled_cells[p[1]][p[0]] = True
                else:
                    self.polygons[-1].append((gx, gy))
                    self.filled_cells[gy][gx] = True
                self.draw_grid()


    def end_poligon(self):
        self.canvas.unbind("<Button-1>")
        if len(self.polygons[-1]) > 2:
            p1 = self.polygons[-1][0]
            p2 = self.polygons[-1][-1]
            for p in self.dda_algorithm(p2[0], p2[1], p1[0], p1[1])[1:]:
                if p not in self.polygons[-1]:
                    self.polygons[-1].append(p)
                    self.filled_cells[p[1]][p[0]] = True
        self.draw_grid()


    def clear_all(self):
        self.polygons = []
        self.lines = []
        self.polygons_vertex = []
        self.filled_cells = [[False] * self.grid_cols for _ in range(self.grid_rows)]
        self.draw_grid()


    def get_cell_coords(self, x, y):
        gx = int((x + self.offset_x) // self.cell_size)
        gy = int((y + self.offset_y) // self.cell_size)
        if 0 <= gx < self.grid_cols and 0 <= gy < self.grid_rows:
            return (gx, gy)
        return None


    def on_press(self, event): self.x, self.y = event.x, event.y

    def on_drag(self, event):
        self.offset_x -= event.x - self.x
        self.offset_y -= event.y - self.y
        self.offset_x = max(0, min(self.offset_x, self.grid_cols * self.cell_size - self.window_width))
        self.offset_y = max(0, min(self.offset_y, self.grid_rows * self.cell_size - self.window_height))
        self.x, self.y = event.x, event.y
        self.draw_grid()

    def zoom(self, event):
        old = self.cell_size
        self.cell_size = max(20, min(200, self.cell_size + (5 if (event.num == 4 or event.delta > 0) else -5)))
        s = self.cell_size / old
        self.offset_x = event.x - (event.x - self.offset_x) * s
        self.offset_y = event.y - (event.y - self.offset_y) * s
        self.offset_x = max(0, min(self.offset_x, self.grid_cols * self.cell_size - self.window_width))
        self.offset_y = max(0, min(self.offset_y, self.grid_rows * self.cell_size - self.window_height))
        self.draw_grid()

    def dda_algorithm(self, x1, y1, x2, y2):
        steps = max(abs(x2-x1), abs(y2-y1))
        if steps == 0: return [(x1, y1)]
        x, y = x1, y1
        dx, dy = (x2-x1)/steps, (y2-y1)/steps
        pts = []
        for _ in range(steps + 1):
            pts.append((round(x), round(y)))
            x += dx; y += dy
        return [pts[0]] + [p for i, p in enumerate(pts[1:]) if p != pts[i]]

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                x1 = c * self.cell_size - self.offset_x
                y1 = r * self.cell_size - self.offset_y
                if self.filled_cells[r][c] and 0 <= x1 < self.window_width and 0 <= y1 < self.window_height:
                    self.canvas.create_rectangle(x1, y1, x1+self.cell_size, y1+self.cell_size, fill='black', outline='gray')
        for c in range(int(self.offset_x/self.cell_size), min(self.grid_cols, int((self.offset_x+self.window_width)/self.cell_size)+1)):
            x = c * self.cell_size - self.offset_x
            self.canvas.create_line(x, 0, x, self.window_height, fill='gray')
        for r in range(int(self.offset_y/self.cell_size), min(self.grid_rows, int((self.offset_y+self.window_height)/self.cell_size)+1)):
            y = r * self.cell_size - self.offset_y
            self.canvas.create_line(0, y, self.window_width, y, fill='gray')


    def is_polygon_convex(self, pts):
        if len(pts) < 3: return False, 0
        sign = 0
        n = len(pts)
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i+1)%n]
            x3, y3 = pts[(i+2)%n]
            cross = (x2-x1)*(y3-y2) - (y2-y1)*(x3-x2)
            if cross != 0:
                current_sign = 1 if cross > 0 else -1
                if sign == 0: sign = current_sign
                elif sign != current_sign: return False, 0
        return True, sign


    def check_convexity(self):
        if not self.polygons_vertex: return
        pts = self.polygons_vertex[-1]
        if len(pts) < 3: return
        ok, sign = self.is_polygon_convex(pts)
        print(f"{'ВЫПУКЛЫЙ' if ok else 'НЕ ВЫПУКЛЫЙ'}, {len(pts)} точек")


    def show_normals(self):
        if not self.polygons_vertex: return
        filled = [row[:] for row in self.filled_cells]
        normals = [[False]*self.grid_cols for _ in range(self.grid_rows)]
        for pts in self.polygons_vertex:
            if len(pts) < 3: continue
            ok, sign = self.is_polygon_convex(pts)
            if ok:
                for i in range(len(pts)):
                    x1, y1 = pts[i]
                    x2, y2 = pts[(i+1)%len(pts)]
                    nx = -(y2-y1)
                    ny = x2-x1
                    l = math.hypot(nx, ny)
                    if l:
                        nx, ny = nx/l, ny/l
                    if sign < 0: nx, ny = -nx, -ny
                    mx, my = (x1+x2)/2, (y1+y2)/2
                    for p in self.dda_algorithm(int(mx), int(my), int(mx+nx*3), int(my+ny*3)):
                        if 0 <= p[0] < self.grid_cols and 0 <= p[1] < self.grid_rows:
                            normals[p[1]][p[0]] = True
        self.draw_grid_with_overlay(filled, normals, 'red')
        self.root.after(3000, self.draw_grid)


    def graham_scan(self, pts):
        if len(pts) < 3: return pts[:]
        p0 = min(pts, key=lambda p: (p[1], p[0]))
        def angle(p): return math.atan2(p[1]-p0[1], p[0]-p0[0])
        def dist(p): return (p[0]-p0[0])**2 + (p[1]-p0[1])**2
        sorted_pts = sorted(pts, key=lambda p: (angle(p), dist(p)))
        if sorted_pts[0] == p0: sorted_pts.pop(0)
        stack = [p0]
        for p in sorted_pts:
            while len(stack) >= 2:
                p1, p2 = stack[-2], stack[-1]
                cross = (p2[0]-p1[0])*(p[1]-p1[1]) - (p2[1]-p1[1])*(p[0]-p1[0])
                if cross <= 0: stack.pop()
                else: break
            stack.append(p)
        return stack


    def jarvis_march(self, pts):
        if len(pts) < 3: return pts[:]
        p0 = min(pts, key=lambda p: (p[1], p[0]))
        hull = [p0]
        cur = p0
        while True:
            nxt = None
            for p in pts:
                if p == cur: continue
                if nxt is None: nxt = p; continue
                cross = (nxt[0]-cur[0])*(p[1]-cur[1]) - (nxt[1]-cur[1])*(p[0]-cur[0])
                if cross < 0 or (cross == 0 and (p[0]-cur[0])**2+(p[1]-cur[1])**2 > (nxt[0]-cur[0])**2+(nxt[1]-cur[1])**2):
                    nxt = p
            if nxt == hull[0]: break
            hull.append(nxt)
            cur = nxt
        return hull


    def build_convex_hull(self, jarvis):
        if not self.polygons_vertex: return
        pts = self.polygons_vertex[-1]
        if len(pts) < 3: return
        hull = self.jarvis_march(pts) if jarvis else self.graham_scan(pts)
        for p in self.polygons[-1]: self.filled_cells[p[1]][p[0]] = False
        self.polygons.pop()
        self.polygons_vertex.pop()
        self.polygons.append([])
        self.polygons_vertex.append([])
        for v in hull: self.polygons_vertex[-1].append(v)
        for i in range(len(hull)):
            for p in self.dda_algorithm(hull[i][0], hull[i][1], hull[(i+1)%len(hull)][0], hull[(i+1)%len(hull)][1]):
                if p not in self.polygons[-1]:
                    self.polygons[-1].append(p)
                    self.filled_cells[p[1]][p[0]] = True
        self.draw_grid()


    def create_line(self):
        self.lines.append([])
        self.canvas.bind("<Button-1>", self.fill_line_cell)


    def fill_line_cell(self, event):
        cell = self.get_cell_coords(event.x, event.y)
        if not cell: return
        gx, gy = cell
        line = self.lines[-1]
        if len(line) == 0:
            line.append((gx, gy))
            self.filled_cells[gy][gx] = True
            self.draw_grid()
        else:
            x1, y1 = line[0]
            for p in self.dda_algorithm(x1, y1, gx, gy):
                if p not in line:
                    line.append(p)
                    self.filled_cells[p[1]][p[0]] = True
            self.draw_grid()
            self.canvas.unbind("<Button-1>")


    def line_intersection(self):
        if not self.lines or not self.polygons: return
        filled = [row[:] for row in self.filled_cells]
        inter = [[False]*self.grid_cols for _ in range(self.grid_rows)]
        for poly in self.polygons:
            for line in self.lines:
                for dot in line:
                    if dot in poly:
                        x, y = dot
                        inter[y][x] = True
        self.draw_grid_with_overlay(filled, inter, 'green')
        self.root.after(3000, self.draw_grid)


    def seg_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        dx1, dy1 = x2-x1, y2-y1
        dx2, dy2 = x4-x3, y4-y3
        denom = dx1*dy2 - dy1*dx2
        if abs(denom) < 1e-10: return None, None
        t = ((x3-x1)*dy2 - (y3-y1)*dx2) / denom
        u = ((x3-x1)*dy1 - (y3-y1)*dx1) / denom
        if 0 <= t <= 1 and 0 <= u <= 1:
            return round(x1 + t*dx1), round(y1 + t*dy1)
        return None, None


    def check_point_in_polygon(self):
        try:
            x, y = int(self.point_x_entry.get()), int(self.point_y_entry.get())
        except:
            print("Ошибка: введите целые числа")
            return
        
        if not self.polygons:
            print("Нет полигонов для проверки")
            return
        
        print(f"Проверка точки ({x}, {y}):")
        filled = [row[:] for row in self.filled_cells]
        point_cell = [[False]*self.grid_cols for _ in range(self.grid_rows)]
        
        for i, poly in enumerate(self.polygons):
            if (x, y) in poly:
                print(f"  Точка принадлежит полигону {i+1}")
                point_found = True
                if 0 <= x < self.grid_cols and 0 <= y < self.grid_rows:
                    point_cell[y][x] = True
            else:
                print(f"  Точка не принадлежит полигону {i+1}")
        
        
        self.draw_grid_with_overlay(filled, point_cell, 'green')
        self.root.after(3000, self.draw_grid)


    def on_segment(self, pt, a, b):
        px, py = pt
        x1, y1 = a
        x2, y2 = b
        cross = (x2-x1)*(py-y1) - (y2-y1)*(px-x1)
        if abs(cross) > 1e-10: return False
        return min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2)


    def draw_grid_with_overlay(self, base_filled, overlay, color):
        self.canvas.delete("all")
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                x1 = c * self.cell_size - self.offset_x
                y1 = r * self.cell_size - self.offset_y
                if 0 <= x1 < self.window_width and 0 <= y1 < self.window_height:
                    if base_filled[r][c]:
                        self.canvas.create_rectangle(x1, y1, x1+self.cell_size, y1+self.cell_size, fill='black', outline='gray')
                    if overlay[r][c]:
                        self.canvas.create_rectangle(x1, y1, x1+self.cell_size, y1+self.cell_size, fill=color, outline='gray')
        for c in range(int(self.offset_x/self.cell_size), min(self.grid_cols, int((self.offset_x+self.window_width)/self.cell_size)+1)):
            x = c * self.cell_size - self.offset_x
            self.canvas.create_line(x, 0, x, self.window_height, fill='gray')
        for r in range(int(self.offset_y/self.cell_size), min(self.grid_rows, int((self.offset_y+self.window_height)/self.cell_size)+1)):
            y = r * self.cell_size - self.offset_y
            self.canvas.create_line(0, y, self.window_width, y, fill='gray')


if __name__ == "__main__":
    root = tk.Tk()
    SimpleZoomGrid(root)
    root.mainloop()