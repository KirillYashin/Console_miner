import random
import os

first_flag = True
game = 0
while first_flag:
    print('Введите 1, если хотите начать новую игру')
    print('Введите 2, если хотите загрузить сохранение')
    game = int(input())
    if game == 2 or game == 1:
        first_flag = False
    else:
        print('Сказано же, введите 1 или 2')

if game == 2:
    is_empty = os.stat('save.txt')
    if is_empty.st_size:
        with open('save.txt', 'r') as input_file:
            mines = input_file.readline().strip().split()
            length = int(mines[-1])
            size = length ** 2
            mines = mines[:-1]
            list_of_mines = []
            for mine in mines:
                list_of_mines.append(int(mine))
            game_over_check = list_of_mines
        with open('field.txt', 'r') as output_file:
            field = output_file.readline().strip().split()
    else:
        print('Сохранений нет, создаю новую игру')
        game = 1


def mines_generator(_length, _mines: int) -> list:
    mines_list = sorted(random.sample(range(0, _length ** 2), _mines))
    return mines_list


def visualization(_length: int, _field: list):
    for i in range(_length):
        print(*_field[0 + i * _length:_length + i * _length])


if game == 1:
    length = int(input('Введите ширину поля\n'))

    size = length ** 2
    mines = size + 1
    field = ['?'] * size

    while mines > size:
        mines = int(input('Введите количество мин на поле\n'))
        if mines > size:
            print('Введите еще раз, так много мин быть не может')

    list_of_mines = mines_generator(length, mines)
    game_over_check = list_of_mines


def checker(_coord_1, _coord_2, _length: int) -> bool:
    if (_coord_1 * _length + _coord_2) in list_of_mines:
        return True
    return False


def out_of_bounds(_coord_1, _coord_2, _length: int):
    return _coord_1 < 0 or _coord_2 < 0 or _coord_1 >= _length or _coord_2 >= length


def mines_around(_coord_1, _coord_2, _length: int) -> int:
    global field
    counter = 0
    for offset_x in range(-1, 2):
        for offset_y in range(-1, 2):
            if offset_x == 0 and offset_y == 0:
                continue
            if out_of_bounds(offset_x + _coord_1, offset_y + _coord_2, _length):
                continue
            elif checker(offset_x + _coord_1, offset_y + _coord_2, _length):
                counter += 1
    # field[_coord_1 * _length + _coord_2] = str(counter)
    return counter


def reveal(_coord_1, _coord_2, _length: int):
    global field
    if out_of_bounds(_coord_1, _coord_2, _length):
        return
    if field[_coord_1 * _length + _coord_2] != '?':
        return
    if mines_around(_coord_1, _coord_2, _length) != 0:
        field[_coord_1 * _length + _coord_2] = str(mines_around(_coord_1, _coord_2, _length))
        return
    else:
        field[_coord_1 * _length + _coord_2] = '0'
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if offset_x == 0 and offset_y == 0:
                    continue
                reveal(_coord_1 + offset_x, _coord_2 + offset_y, _length)


flag = True
mode = 0

while flag:
    if not game_over_check:
        visualization(length, field)
        print('Вы отметили все мины, поздравляю с победой!')
        flag = False
        continue

    visualization(length, field)
    print('Введите 1, если хотите открыть ячейку')
    print('Введите 2, если хотите отметить мину')
    print('Введите 3, чтобы сохранить игру и выйти')
    mode = int(input())

    if mode == 1:
        coord_1 = int(input('Введите номер строки (нумерация начинается с 1)\n'))
        coord_1 -= 1
        coord_2 = int(input('Введите номер столбца (нумерация начинается с 1)\n'))
        coord_2 -= 1
        if checker(coord_1, coord_2, length):
            flag = False
            print('BOOM, GAME OVER')
            continue
        else:
            reveal(coord_1, coord_2, length)
    elif mode == 2:
        coord_1 = int(input('Введите номер строки (нумерация начинается с 1)\n'))
        coord_1 -= 1
        coord_2 = int(input('Введите номер столбца (нумерация начинается с 1)\n'))
        coord_2 -= 1
        field[coord_1 * length + coord_2] = '*'
        if checker(coord_1, coord_2, length):
            game_over_check.remove(coord_1 * length + coord_2)
    elif mode == 3:
        with open('save.txt', 'w') as output_file:
            to_write = ''
            for i in range(size):
                if i in game_over_check:
                    to_write += str(i)
                    to_write += ' '
            to_write += str(length)
            output_file.write(to_write.strip())
        with open('field.txt', 'w') as output_file:
            to_write = ''
            for i in field:
                to_write += i
                to_write += ' '
            output_file.write(to_write.strip())
        flag = False
    else:
        print('Сказано же, введите 1, 2 или 3')
