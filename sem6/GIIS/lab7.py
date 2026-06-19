import tkinter as tk
import math

class DelaunayVoronoiApp:
    def __init__(self, root):
        self.root = root
        self.W, self.H = 800, 600
        self.canvas = tk.Canvas(root, width=self.W, height=self.H, bg='#f5f5f5')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Панель управления
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(self.btn_frame, text="Очистить", command=self.clear).pack(side=tk.LEFT)
        tk.Label(self.btn_frame, text="  |  Кликните по холсту, чтобы добавить точку.").pack(side=tk.LEFT)

        self.points = []
        self.triangles = []  # Список кортежей индексов точек (i, j, k)
        self.voronoi_edges = []

        self.init_super_triangle()
        self.canvas.bind('<Button-1>', self.on_click)
        self.draw()

    def init_super_triangle(self):
        """Инициализация гигантского треугольника, охватывающего весь холст."""
        m = 50
        self.points = [(-m, -m), (self.W + m, -m), (self.W / 2, self.H + m)]
        self.triangles = [(0, 1, 2)]

    @staticmethod
    def circumcircle(a, b, c):
        """Возвращает (cx, cy, r_sq) описанной окружности или None, если точки коллинеарны."""
        x1, y1 = a
        x2, y2 = b
        x3, y3 = c
        D = 2.0 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        if abs(D) < 1e-9:
            return None
        Ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D
        Uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D
        r_sq = (Ux - x1)**2 + (Uy - y1)**2
        return Ux, Uy, r_sq

    @staticmethod
    def in_circumcircle(p, center, r_sq):
        return (p[0] - center[0])**2 + (p[1] - center[1])**2 < r_sq + 1e-9

    def bowyer_watson(self, px, py):
        """Инкрементальный алгоритм триангуляции Делоне (Боуэра-Уотсона)."""
        # Проверка на дубликаты
        for p in self.points:
            if math.hypot(px - p[0], py - p[1]) < 2.0:
                return

        idx = len(self.points)
        self.points.append((px, py))

        # 1. Находим все треугольники, чьи описанные окружности содержат новую точку
        bad_indices = []
        for i, t in enumerate(self.triangles):
            circ = self.circumcircle(self.points[t[0]], self.points[t[1]], self.points[t[2]])
            if circ and self.in_circumcircle((px, py), circ[:2], circ[2]):
                bad_indices.append(i)

        # 2. Извлекаем границу "дыры" (рёбра, принадлежащие только одному плохому треугольнику)
        edge_count = {}
        for i in bad_indices:
            t = self.triangles[i]
            for e in [(t[0], t[1]), (t[1], t[2]), (t[2], t[0])]:
                ke = tuple(sorted(e))
                edge_count[ke] = edge_count.get(ke, 0) + 1

        boundary = [e for e, cnt in edge_count.items() if cnt == 1]

        # 3. Удаляем плохие треугольники и создаём новые с новой точкой
        self.triangles = [self.triangles[i] for i in range(len(self.triangles)) if i not in bad_indices]
        for e in boundary:
            self.triangles.append((e[0], e[1], idx))

    def compute_voronoi(self):
        """Построение диаграммы Вороного как двойственного графа Делоне."""
        self.voronoi_edges = []
        centers = {}

        # Предрасчёт центров описанных окружностей для каждого треугольника
        for t in self.triangles:
            circ = self.circumcircle(self.points[t[0]], self.points[t[1]], self.points[t[2]])
            if circ:
                centers[t] = (circ[0], circ[1])

        # Сопоставление рёбер -> списки соседних треугольников
        edge_to_tris = {}
        for t in self.triangles:
            for e in [(t[0], t[1]), (t[1], t[2]), (t[2], t[0])]:
                ke = tuple(sorted(e))
                edge_to_tris.setdefault(ke, []).append(t)

        # Формируем рёбра Вороного
        for e, tris in edge_to_tris.items():
            if len(tris) == 2:
                c1 = centers.get(tris[0])
                c2 = centers.get(tris[1])
                if c1 and c2:
                    self.voronoi_edges.append((c1, c2))
            elif len(tris) == 1:
                # Граничное ребро: рисуем луч от центра перпендикулярно ребру наружу
                t = tris[0]
                c = centers.get(t)
                if not c: continue

                p1, p2 = self.points[e[0]], self.points[e[1]]
                mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
                dx, dy = p2[0] - p1[0], p2[1] - p1[1]
                nx, ny = -dy, dx  # Перпендикуляр
                length = math.hypot(nx, ny)
                if length < 1e-9: continue
                nx, ny = nx / length, ny / length

                # Выбираем направление "наружу" (от треугольника)
                vcx, vcy = c[0] - mx, c[1] - my
                if vcx * nx + vcy * ny < 0:
                    nx, ny = -nx, -ny

                self.voronoi_edges.append((c, (c[0] + nx * 3000, c[1] + ny * 3000)))

    def draw(self):
        self.canvas.delete('all')

        # Рисуем триангуляцию Делоне (синие линии)
        drawn_edges = set()
        for t in self.triangles:
            # Пропускаем рёбра, касающиеся супер-треугольника
            if any(v < 3 for v in t):
                continue
            for e in [(t[0], t[1]), (t[1], t[2]), (t[2], t[0])]:
                ke = tuple(sorted(e))
                if ke[0] < 3 or ke[1] < 3:
                    continue
                if ke not in drawn_edges:
                    drawn_edges.add(ke)
                    p1, p2 = self.points[ke[0]], self.points[ke[1]]
                    self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill='#3498db', width=1)

        # Рисуем диаграмму Вороного (красные линии)
        for e in self.voronoi_edges:
            self.canvas.create_line(e[0][0], e[0][1], e[1][0], e[1][1], fill='#e74c3c', width=2)

        # Рисуем точки (чёрные кружки)
        for i, p in enumerate(self.points):
            if i < 3:  # Не рисуем вершины супер-треугольника
                continue
            self.canvas.create_oval(p[0]-4, p[1]-4, p[0]+4, p[1]+4, fill='#2c3e50')

    def on_click(self, event):
        self.bowyer_watson(event.x, event.y)
        self.compute_voronoi()
        self.draw()

    def clear(self):
        self.init_super_triangle()
        self.voronoi_edges = []
        self.draw()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Триангуляция Делоне и Диаграмма Вороного")
    app = DelaunayVoronoiApp(root)
    root.mainloop()