class screen(object):
    screenName = 'defaultScreen'
    frame = []
    symbol = '*'
    space = '-'

    def __init__(self, x, y, symbol, space, name):
        self.frame = [[space for _ in range(x)] for _ in range(y)]
        self.symbol = symbol
        self.space = space
        self.screenName = name

    def __str__(self):
        self.draw()
        return ''

    def draw(self):
        for i in range(len(self.frame)):
            for j in range(len(self.frame[0])):
                print(self.frame[i][j], end='')
            print('')


defaultScreen = screen(40, 40, '* ', '- ', 'defaultScreen')

def brezenhem(st, en):
    x1, y1 = st
    x2, y2 = en
    dx = x2 - x1
    dy = y2 - y1
    istep = abs(dy) > abs(dx)
    if istep:
        x1, y1, x2, y2 = y1, x1, y2, x2
    reverse = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        reverse = True
    dx = x2 - x1
    dy = y2 - y1
    error = int(dx / 2)
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        if istep:
            coord = (y, x)
        else:
            coord = (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
    if reverse:
        points.reverse()
    return points


def get_lineS(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (0.5)


class shape(object):
    __x = 0
    __y = 0

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def get_s(self):
        if isinstance(self, shape):
            return 0

    def __init__(self, x, y, f_screen=defaultScreen):
        self.__x = x
        self.__y = y
        self.f_screen = f_screen

    def draw(self):
        for i in range(len(self.f_screen.frame)):
            for j in range(len(self.f_screen.frame[0])):
                if self.__x == i and self.__y == j:
                    self.f_screen.frame[j][i] = self.f_screen.symbol


class rectangle(shape):
    __x1 = 0
    __x2 = 0
    __y1 = 0
    __y2 = 0

    @property
    def x1(self):
        return self.__x1

    @property
    def y1(self):
        return self.__y1

    @property
    def x2(self):
        return self.__x2

    @property
    def y2(self):
        return self.__y2

    def get_s(self):
        return abs(self.__x1 - self.__x2) * abs(self.__y1 - self.__y2)

    def __init__(self, x1, y1, x2, y2, f_screen=defaultScreen):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        self.f_screen = f_screen

    def draw(self):
        for i in range(len(self.f_screen.frame)):
            for j in range(len(self.f_screen.frame[0])):
                if j >= self.__x1 and j <= self.__x2 and i >= self.__y1 and i <= self.__y2 and (i == self.__y1 or i == self.__y2 or j == self.__x1 or j == self.__x2):
                    self.f_screen.frame[i][j] = self.f_screen.symbol


class triangle(shape):
    __x1 = __x2 = __x3 = __y1 = __y2 = __y3 = 0

    @property
    def x1(self):
        return self.__x1

    @property
    def y1(self):
        return self.__y1

    @property
    def x2(self):
        return self.__x2

    @property
    def y2(self):
        return self.__y2

    @property
    def x3(self):
        return self.__x3

    @property
    def y3(self):
        return self.__y3

    @property
    def get_s(self):
        lines = [get_lineS(self.__x1, self.__y1, self.__x2, self.__y2),
                 get_lineS(self.__x1, self.__y1, self.__x3, self.__y3),
                 get_lineS(self.__x2, self.__y2, self.__x3, self.__y3)]
        p = sum(lines) / 2
        return (p * (p - lines[0]) * (p - lines[1]) * (p - lines[2])) ** (0.5)

    def __init__(self, x1, y1, x2, y2, x3, y3, f_screen=defaultScreen):
        self.__x1 = x1
        self.__x2 = x2
        self.__x3 = x3
        self.__y1 = y1
        self.__y2 = y2
        self.__y3 = y3
        self.f_screen = f_screen

    def draw(self):
        mas = [brezenhem((self.__x1, self.__y1), (self.__x2, self.__y2)),
               brezenhem((self.__x1, self.__y1), (self.__x3, self.__y3)),
               brezenhem((self.__x2, self.__y2), (self.__x3, self.__y3))]
        for i in range(len(self.f_screen.frame)):
            for j in range(len(self.f_screen.frame[0])):
                if (i, j) in mas[0] or (i, j) in mas[1] or (i, j) in mas[2]:
                    self.f_screen.frame[j][i] = self.f_screen.symbol


class rombus(rectangle):  ### Точки задавать по часовой стрелке
    __x3 = __x4 = __y3 = __y3 = 0

    @property
    def x3(self):
        return self.__x3

    @property
    def y3(self):
        return self.__y3

    @property
    def x4(self):
        return self.__x4

    @property
    def y4(self):
        return self.__y4

    @property
    def get_s(self):
        return (get_lineS(self.__x1, self.__y1, self.__x3, self.__y3) * get_lineS(self.__x2, self.__y2, self.__x4,
                                                                                  self.__y4)) / 2

    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4, f_screen=defaultScreen):
        self.__x1, self.__x2, self.__x3, self.__x4, self.__y1, self.__y2, self.__y3, self.__y4 = x1, x2, x3, x4, y1, y2, y3, y4
        self.f_screen = f_screen

    def draw(self):
        mas = [brezenhem((self.__x1, self.__y1), (self.__x2, self.__y2)),
               brezenhem((self.__x2, self.__y2), (self.__x3, self.__y3)),
               brezenhem((self.__x3, self.__y3), (self.__x4, self.__y4)),
               brezenhem((self.__x4, self.__y4), (self.__x1, self.__y1))]
        for i in range(len(self.f_screen.frame)):
            for j in range(len(self.f_screen.frame[0])):
                if (i, j) in mas[0] or (i, j) in mas[1] or (i, j) in mas[2] or (i, j) in mas[3]:
                    self.f_screen.frame[j][i] = self.f_screen.symbol


class line(object):
    __x1 = __x2 = __y1 = __y2 = 0

    @property
    def x1(self):
        return self.__x1

    @property
    def y1(self):
        return self.__y1

    @property
    def x2(self):
        return self.__x2

    @property
    def y2(self):
        return self.__y2

    @property
    def get_s(self):
        if isinstance(self, line):
            return 0

    def __str__(self):
        self.draw()
        return ''

    def __init__(self, x1, y1, x2, y2, f_screen=defaultScreen):
        self.__x1, self.__y1, self.__x2, self.__y2 = x1, y1, x2, y2
        self.f_screen = f_screen

    def draw(self):
        mas = [brezenhem((self.x1, self.y1), (self.x2, self.y2))]
        for i in range(len(self.f_screen.frame)):
            for j in range(len(self.f_screen.frame[0])):
                if (i, j) in mas[0]:
                    self.f_screen.frame[j][i] = self.f_screen.symbol


class square(line):
    __x3 = __x4 = __y3 = __y4 = 0

    @property
    def x3(self):
        return self.__x3

    @property
    def y3(self):
        return self.__y3

    @property
    def x4(self):
        return self.__x4

    @property
    def y4(self):
        return self.__y4

    @property
    def get_s(self):
        return max(abs(self.x1 - self.x2), abs(self.x1 - self.x4)) * max(abs(self.y1 - self.y2), abs(self.y1 - self.y4))

    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4, f_screen=defaultScreen):
        self.__x1, self.__x2, self.__x3, self.__x4, self.__y1, self.__y2, self.__y3, self.__y4 = x1, x2, x3, x4, y1, y2, y3, y4
        self.f_screen = f_screen

    def draw(self):
        mas = [brezenhem((self.__x1, self.__y1), (self.__x2, self.__y2)), brezenhem((self.__x2, self.__y2), (self.__x3, self.__y3)),
               brezenhem((self.__x3, self.__y3), (self.__x4, self.__y4)), brezenhem((self.__x4, self.__y4), (self.__x1, self.__y1))]
        for i in range(len(self.f_screen.frame)):
            for j in range(len(self.f_screen.frame[0])):
                if (i, j) in mas[0] or (i, j) in mas[1] or (i, j) in mas[2] or (i, j) in mas[3]:
                    self.f_screen.frame[j][i] = self.f_screen.symbol




figMas = []
scrMas = [defaultScreen]
pos = '0'
curScr = 0
print('***************************************************')
print('*Добро пожаловать в простой редактор псевдографики*')
print('***************************************************')
print('*******************Внимание************************')
print('*****Координатная плоскость начинается с точки*****')
print('*(X-ширина,Y-высота) = (0,0) В левом верхнем углу**')
print('***************************************************')
print('*******************Внимание************************')
print('*****Координаты фигур задаются в порядке***********')
print('***начиная с самой верхней, по часовой стрелке*****')
print('***При выходе за пределы экрана программа может****')
print('************экстренно завершиться******************')
while True:
    if pos == '0':
        print('***************************************************')
        print('1 - Выбрать экран')
        print('2 - Создать экран')
        print('3 - Добавить фигуру')
        print('4 - Нарисовать экран')
        print('***************************************************')
        pos = input('Выберите опцию: ')
    elif pos == '1':
        print('***************************************************')
        for i in range(len(scrMas)):
            print(f"    {i} - {vars(scrMas[i])['screenName']}")
        print('***************************************************')
        curScr = input('Выберите экран: ')
        pos = '0'
    elif pos == '2':
        print('***************************************************')
        newScr = "screen_" + input('Введите название нового экрана: ')
        newX = input('Введите ширину нового экрана: ')
        newY = input('Введите высоту нового экрана: ')
        newSymbol = input('Введите символ для рисования: ')
        newSpace = input('Введите символ для пустоты: ')
        if newSpace == '':
            newSpace = ' '
            print('Пробел установлен в качестве символа пустоты')
        exec(f'{newScr} = screen({newX},{newY},"{newSymbol}","{newSpace}","{newScr}")')
        eval(f'scrMas.append({newScr})')
        pos = '0'
    elif pos == '3':
        print('***************************************************')
        print('1 - Точка')
        print('2 - Прямоугольник')
        print('3 - Треугольник')
        print('4 - Ромб')
        print('5 - Линия')
        print('6 - Квадрат')
        print('***************************************************')
        curFig = (input('Выберите фигуру: '))
        if curFig == '1':
            newX = input('Введите координату X: ')
            newY = input('Введите координату Y: ')
            eval(f'figMas.append(shape({newX}, {newY}, {vars(scrMas[int(curScr)])["screenName"]}))')
        elif curFig == '2':
            newX1 = input('Введите координату X1: ')
            newY1 = input('Введите координату Y1: ')
            newX2 = input('Введите координату X2: ')
            newY2 = input('Введите координату Y2: ')
            eval(f'figMas.append(rectangle({newX1}, {newY1}, {newX2}, {newY2}, {vars(scrMas[int(curScr)])["screenName"]}))')
        elif curFig == '3':
            newX1 = input('Введите координату X1: ')
            newY1 = input('Введите координату Y1: ')
            newX2 = input('Введите координату X2: ')
            newY2 = input('Введите координату Y2: ')
            newX3 = input('Введите координату X3: ')
            newY3 = input('Введите координату Y3: ')
            eval(f'figMas.append(triangle({newX1}, {newY1}, {newX2}, {newY2}, {newX3}, {newY3}, {vars(scrMas[int(curScr)])["screenName"]}))')
        elif curFig == '4':
            newX1 = input('Введите координату X1: ')
            newY1 = input('Введите координату Y1: ')
            newX2 = input('Введите координату X2: ')
            newY2 = input('Введите координату Y2: ')
            newX3 = input('Введите координату X3: ')
            newY3 = input('Введите координату Y3: ')
            newX4 = input('Введите координату X4: ')
            newY4 = input('Введите координату Y4: ')
            eval(f'figMas.append(rombus({newX1}, {newY1}, {newX2}, {newY2}, {newX3}, {newY3}, {newX4}, {newY4}, {vars(scrMas[int(curScr)])["screenName"]}))')
        elif curFig == '5':
            newX1 = input('Введите координату X1: ')
            newY1 = input('Введите координату Y1: ')
            newX2 = input('Введите координату X2: ')
            newY2 = input('Введите координату Y2: ')
            eval(f'figMas.append(line({newX1}, {newY1}, {newX2}, {newY2}, {vars(scrMas[int(curScr)])["screenName"]}))')
        elif curFig == '6':
            newX1 = input('Введите координату X1: ')
            newY1 = input('Введите координату Y1: ')
            newX2 = input('Введите координату X2: ')
            newY2 = input('Введите координату Y2: ')
            newX3 = input('Введите координату X3: ')
            newY3 = input('Введите координату Y3: ')
            newX4 = input('Введите координату X4: ')
            newY4 = input('Введите координату Y4: ')
            eval(f'figMas.append(square({newX1}, {newY1}, {newX2}, {newY2}, {newX3}, {newY3}, {newX4}, {newY4}, {vars(scrMas[int(curScr)])["screenName"]}))')
        print('***************************************************')
        pos = '0'
    elif pos == '4':
        for i in figMas:
            i.draw()
        print('-'*100)
        print('')
        print(scrMas[int(curScr)])
        print('-' * 100)
        pos = '0'
    elif pos!='0' and pos!='1' and pos!='2' and pos!='3' and pos!='4':
        print('Повторите снова')
        pos = '0'
