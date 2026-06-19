def sign( x):
    return 1 if x > 0 else (-1 if x < 0 else 0)
    
def integer(x):
    return int(x)

def dda_algorithm(self, x1, y1, x2, y2):
        """Алгоритм ЦДА"""
        points = []
        
        length = max(abs(x2 - x1), abs(y2 - y1))
        if length == 0:
            return [(x1, y1, 1.0)]
        
        dx = (x2 - x1) / length
        dy = (y2 - y1) / length
        
        x = x1 + 0.5 * sign(dx)
        y = y1 + 0.5 * sign(dy)
        points.append((integer(x), integer(y), 1.0))
        
        i = 0
        while i < length:
            x += dx
            y += dy
            points.append((integer(x), integer(y), 1.0))
            i += 1
        
        return points
    



def bresenham_algorithm_clear(x1, y1, x2, y2):
    """Более читаемая версия для всех четвертей"""
    points = []
    
    x, y = x1, y1
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    sx = 1 if x2 > x1 else -1   # Шаг по X
    sy = 1 if y2 > y1 else -1   # Шаг по Y
    
    points.append((x, y, 1.0))
    
    # Случай 1: угол меньше 45 градусов (dx > dy)
    if dx > dy:
        e = 2 * dy - dx
        for _ in range(dx):
            if e >= 0:
                y += sy
                e -= 2 * dx
            x += sx
            e += 2 * dy
            points.append((x, y, 1.0))
    
    # Случай 2: угол больше 45 градусов (dy >= dx)
    else:
        e = 2 * dx - dy
        for _ in range(dy):
            if e >= 0:
                x += sx
                e -= 2 * dy
            y += sy
            e += 2 * dx
            points.append((x, y, 1.0))
    
    return points




def wu_algorithm(x1, y1, x2, y2):
    """Алгоритм Ву с отдельной обработкой особых случаев"""
    points = []
    
    # Горизонтальная линия
    if y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            points.append((x, y1, 1.0))
        return points
    
    # Вертикальная линия
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            points.append((x1, y, 1.0))
        return points
    
    # Линия под 45° (dx == dy)
    if abs(x2 - x1) == abs(y2 - y1):
        # Упорядочиваем точки
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        
        step_y = 1 if y2 > y1 else -1
        
        x = x1
        y = y1
        while x <= x2:
            points.append((x, y, 1.0))
            x += 1
            y += step_y
        return points
    
    x = x1
    y = y1
    dx = x2 - x1
    dy = y2 - y1
    k = dy / dx
    
    e = 2 * dy - dx
    
    # Первая точка
    ideal_y = y1 
    y_int = int(ideal_y)
    frac = ideal_y - y_int
    
    points.append((x, y_int, 1 - frac))
    points.append((x, y_int + 1, frac))
    
    i = 1
    while i <= dx:
        if e >= 0:
            y += 1
            e -= 2 * dx
        
        x += 1
        e += 2 * dy
        
        ideal_y = y1 + k * (x - x1)
        y_int = int(ideal_y)
        frac = ideal_y - y_int
        
        # Две точки с разной яркостью
        points.append((x, y_int, 1 - frac))
        points.append((x, y_int + 1, frac))
        
        i += 1
    
    return points





























def circle(self, x1):
    points = []
    x = 0
    y = x1
    lim = 0
    delta = 2 - 2 * x1
    sigma = 0

    points.append((self.integer(x), self.integer(y)))

    while y > lim:
        if delta > 0:
            sigma = 2 * delta - 2 * x - 1
            if sigma > 0:
                y = y - 1
                delta = delta - 2 * y + 1
            else:
                x = x + 1
                y = y - 1
                delta = delta + 2 * x - 2 * y + 2
        elif delta < 0:
            sigma = 2 * delta + 2 * y - 1
            if sigma > 0:
                x = x + 1
                y = y - 1
                delta = delta + 2 * x - 2 * y + 2
            else:
                x = x + 1
                delta = delta + 2 * x + 1
        else:
            x = x + 1
            y = y - 1
            delta = delta + 2 * x - 2 * y + 2

        print(1)  
        points.append((self.integer(x), self.integer(y)))
    return points






##ВАРИК КРУЧЕЕЕЕ№№№№№№№№№№№№№№№
def circle(self, p):
    points = []
    x = 0
    y = p

    
    points.append((self.integer(x), self.integer(y)))
    
    while x < 19 and y > 0:
        DH =  (x + 1) * (x + 1) +  y * y - p * p
        
        DV =  x * x +  (y - 1) * (y - 1) - p * p
        
        DD =  (x + 1) * (x + 1) +  (y - 1) * (y - 1) - p * p
        
        min_abs = min(abs(DH), abs(DV), abs(DD))
        
        if abs(DD) == min_abs:
            x = x + 1
            y = y - 1
        elif abs(DH) == min_abs:
            x = x + 1
        else:
            y = y - 1
        
        points.append((self.integer(x), self.integer(y)))
    
    return points




def ellipse(self, x1, a, b):
    points = []
    x = 0
    y = x1
    lim = 0
    delta = 2 - 2 * x1
    sigma = 0

    points.append((self.integer(x), self.integer(y)))

    while y > lim:
        if delta > 0:
            sigma = 2 * delta - 2 * x * b**2 - 1
            if sigma > 0:
                y = y - 1
                delta = delta + a**2 *(1 - 2*y)
            else:
                x = x + 1
                y = y - 1
                delta = delta + b**2 * (2 * x + 1) + a**2 *(1 - 2*y)
        elif delta < 0:
            sigma = 2 * delta + 2 * y * a**2 - 1
            if sigma > 0:
                x = x + 1
                y = y - 1
                delta = delta + b**2 * (2 * x + 1) + a**2 *(1 - 2*y)
            else:
                x = x + 1
                delta = delta + b**2 * (2 * x + 1)
        else:
            x = x + 1
            y = y - 1
            delta = delta + b**2 * (2 * x + 1) + a**2 *(1 - 2*y)

        print(1)  
        points.append((self.integer(x), self.integer(y)))
    return points




def hyperbola(self, a, b):
    """
    Алгоритм Брезенхема для гиперболы x²/a² - y²/b² = 1
    """
    points = []
    x = a
    y = 0
    a2 = a * a
    b2 = b * b
    
    points.append((self.integer(x), self.integer(y)))
    
    while x < 19 and y < 19:
        DH = b2 * (x + 1) * (x + 1) - a2 * y * y - a2 * b2
        
        DV = b2 * x * x - a2 * (y + 1) * (y + 1) - a2 * b2
        
        DD = b2 * (x + 1) * (x + 1) - a2 * (y + 1) * (y + 1) - a2 * b2
        
        min_abs = min(abs(DH), abs(DV), abs(DD))
        
        if abs(DD) == min_abs:
            x = x + 1
            y = y + 1
        elif abs(DH) == min_abs:
            x = x + 1
        else:
            y = y + 1
        
        points.append((self.integer(x), self.integer(y)))
    
    return points




def parabola(self, p):
    """
    Алгоритм Брезенхема для параболы y² = 2px
    По аналогии с алгоритмом окружности/эллипса
    """
    points = []
    x = 0
    y = 0
    p2 = 2 * p
    
    # F(x,y) = y² - 2px
    points.append((self.integer(x), self.integer(y)))
    
    while x < 19:
        
        Dh = y * y - p2 * (x + 1)
        
        Dd = (y + 1) * (y + 1) - p2 * (x + 1)
    
        if abs(Dh) < abs(Dd):
            x = x + 1
        else:
            x = x + 1
            y = y + 1
        
        points.append((self.integer(x), self.integer(y)))
    
    return points  
















ermit_matrix = [[2, -2, 1, 1],
                [-3, 3, -2, -1],
                [0, 0, 1, 0],
                [1, 0, 0, 0]]

bezye_matrix = [[-1, 3, -3, 1],
                [3, -6, 3, 0],
                [-3, 3, 0, 0],
                [1, 0, 0, 0]]

v_spline_matrix = [[-1, 3, -3, 1],
                   [3, -6, 3, 0],
                   [-3, 0, 3, 0],
                   [1, 4, 1, 0]]

v_spline_matrix = [[elem / 6 for elem in row] for row in v_spline_matrix]


def ermit_interpolation(vector_x, vector_y, matrix):
    result_x = []
    result_y = []
    for row in matrix:
        t_xi = 0
        t_yi = 0
        for i, elem in enumerate(row):
            t_xi += vector_x[i] * elem
            t_yi += vector_y[i] * elem
        result_x.append(t_xi)
        result_y.append(t_yi)

    points = []
    for i in range(0, 11):
        t = i / 10
        x = t**3 * result_x[0] + t**2 * result_x[1] + t * result_x[2] + result_x[3]
        y = t**3 * result_y[0] + t**2 * result_y[1] + t * result_y[2] + result_y[3]
        points.append((x, y))
    return points