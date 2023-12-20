import sys
import copy
import random
import time


lst_r = [f"{y}{x}" for x in range(3) for y in range(3)]  # генератор для проверки правильного ввода данных игроком и создания словаря поля
fild = ["-" for _ in range(9)]  # генератор чистого поля
cell_dict = {f"{x}": i for i, x in enumerate(lst_r)}  # генератор словаря для нахождения индекса по координатам
cell_dict_ai = {f"{i}": x for i, x in enumerate(lst_r)}  # генератор словаря для нахождения координат по индексу
win_speaks = ['💪 (`▿´) 👊 - И опять железо всегда бьет мясо!',
              '(҂◡̀_◡́)ᕤ  - Легко!',
              '٩(˘◡˘)۶ - Повезет в другой раз!\n((≖᷆︵︣≖)👎 - Вообще-то нет )',
              '(≖_≖ ) - Как ребенка...']
u_cant_win_speaks = ['Размечтался...',
                     "(ง︡'-'︠)ง - Неа!",
                     ' (͠≖ ͜ʖ͠≖)👌 - Неплохая попытка.',
                     '(͡• ͜ʖ ͡•) - Я все вижу!',
                     ]
rand_speak = ['v( ‘.’ )v - А если так.',
              '',
              'v( ‘.’ )v - Допустим так.',
              '',
              'v( ‘.’ )v - Попробуем так.',
              '',
              '']


def win_check(fild):
    """Функция проверки окончания игры. Если найдена линия из "о" или "х",
     меняет символы победной линии на подчеркнутые"""
    win_z = ['x', 'x', 'x']
    win_c = ['o', 'o', 'o']
    diag = [fild[0], fild[4], fild[8]]
    diag_r = [fild[2], fild[4], fild[6]]
    win_row_c = ['X̲', 'X̲', 'X̲']
    win_row_z = ['O̲', 'O̲', 'O̲']

    for step in range(3):  # проверка горизонтальных линий
        row = fild[3*step:3*(step+1)]
        if row == win_z:
            fild[3 * step:3 * (step + 1)] = win_row_c
            return 'x'
        if row == win_c:
            fild[3 * step:3 * (step + 1)] = win_row_z
            return 'o'

    for step in range(3):  # проверка вертикальных линий
        row = fild[step::3]
        if row == win_z:
            fild[step::3] = win_row_c
            return 'x'
        if row == win_c:
            fild[step::3] = win_row_z
            return 'o'

    if diag == win_z:  # проверка диагонали
        fild[0], fild[4], fild[8] = 'X̲', 'X̲', 'X̲'
        return 'x'
    if diag == win_c:
        fild[0], fild[4], fild[8] = 'O̲', 'O̲', 'O̲'
        return 'o'

    if diag_r == win_z:  # проверка обратной диагонали
        fild[2], fild[4], fild[6] = 'X̲', 'X̲', 'X̲'
        return 'x'
    if diag_r == win_c:
        fild[2], fild[4], fild[6] = 'O̲', 'O̲', 'O̲'
        return 'o'


def reboot_fild():  # перезагрузка поля
    global fild
    fild = ["-" for _ in range(9)]


def pr_fild(x_y=None):  # отображение поля
    """Функция отображения поля"""
    global fild

    if x_y:
        print(f"ИИ ставит крестик на: {x_y}")
    print("   0  1  2")
    print(f"0  {fild[0]}  {fild[1]}  {fild[2]}")
    print(f"1  {fild[3]}  {fild[4]}  {fild[5]}")
    print(f"2  {fild[6]}  {fild[7]}  {fild[8]}")
    print()


def step(pl):  # ход игрока
    global lst_r
    global fild
    global cell_dict


    while True:
        move = input('Нолик на: ' if pl == 'o' else 'Крестик на: ')  # ход нолика
        if move.lower() == 'q':
            reboot_fild()
            menu()
        if move not in lst_r:
            print('Некорректный ввод!!!')
            continue

        if fild[cell_dict[move]] == '-':
            fild[cell_dict[move]] = pl
            break
        else:
            print('Клетка занята!')
            continue



c_win = 0
z_win = 0


def game():
    """Вариант игры для 2-х игроков"""
    print('\n!! ИГРА НАЧИНАЕТСЯ !!')
    print('\nПравила и так знаем с детства :-)\n'
          'Вам нужно по очереди вводить координаты вашего хода.\n'
          'Первый ход всегда за крестиком!\n'
          'Ввод производится в формате двух цифр(без пробела), сначала координата по оси Х, потом по оси У. Пример: 02\n'
          '(Для возврата в меню введите "q")'
          'И так начнем!')
    global c_win
    global z_win
    global fild
    pr_fild()  # принт чистого поля
    tern = 1  # счетчик игры

    while True:  # цикл игры
        pl = ('o' if tern % 2 == 0 else 'x')
        step(pl)
        if 4 < tern < 9:
            win = win_check(fild)
            if win:  # при выигрыше возвращает список
                pr_fild()
                print("Победил Крестик!!!" if win == 'x' else "Победил Нолик!!!")
                if win == "x":
                    c_win += 1
                if win == "o":
                    z_win += 1
                print(f"Счет:\nКрестик:{c_win} - Нолик:{z_win}\n")
                break
            pass
        elif tern == 9:
            pr_fild()
            print("Ничья!")
            print(f"Счет: X: {c_win} vs O: {z_win}\n")
            break
        pr_fild()
        tern += 1



    while True:  # цикл вопроса о повторе игры
        again = input("""Повторим?\n'1' == "ДА"\n'2' == "НЕТ"\nВведите цифру: """)
        if again == '1':  # при повторе, обновляет поле и рекурсивно запускает game()
            reboot_fild()
            c_win = 0
            z_win = 0
            game()
            break
        elif again == '2':  # возврат в меню и откат счета
            reboot_fild()
            c_win = 0
            z_win = 0
            return None
        else:
            print("Введите '1' или '0' !!")
            continue


def game_ai(diff):
    """Вариант игры для против ИИ выбранного уровня сложности"""
    print('\n!! ИГРА НАЧИНАЕТСЯ !!')
    print('\nПравила и так знаем с детства :-)\n'
          'Вам нужно во время своей очереди вводить координаты вашего хода.\n'
          'Первый ход всегда за крестиком!\n'
          'Ввод производится в формате двух цифр(без пробела), сначала координата по оси Х, потом по оси У. Пример: 02\n'
          'Для возврата в меню введите "q"\n'
          'И так начнем!')
    global c_win
    global z_win
    global fild

    reboot_fild()
    pr_fild()  # принт чистого поля
    tern = 1  # счетчик игры

    while True:
        x_y = None
        pl = ('o' if tern % 2 == 0 else 'x')
        if pl == 'x':  # переключение сложности ИИ
            if diff == '1':
                x_y = step_ai_1(pl)
            elif diff == '2':
                x_y = step_ai_2(pl, tern)
        else:
            step(pl)
            x_y = None

        if 4 < tern < 9:  # С 5 того хода начало проверок окончания игры
            win = win_check(fild)  # при выигрыше возвращает "x" или "о"
            if win:
                pr_fild(x_y)
                print("Победил Крестик!!!" if win == 'x' else "Победил Нолик!!!")
                if win == "x":
                    c_win += 1
                if win == "o":
                    z_win += 1
                print(f"Счет: Крестик {c_win} - {z_win} Нолик:\n")

                break
            pass

        elif tern == 9:  # проверка на последнем ходу
            win = win_check(fild)
            if win:
                pr_fild(x_y)
                print("Победил Крестик!!!" if win == 'x' else "Победил Нолик!!!")
                if win == "x":
                    c_win += 1
                if win == "o":
                    z_win += 1
                print(f"Счет: Крестик {c_win} - {z_win} Нолик:\n")
                break
            pr_fild(x_y)
            print("Ничья!")
            print(f"Счет: Крестик {c_win} - {z_win} Нолик:\n")
            break

        pr_fild(x_y)
        tern += 1


    while True:  # цикл вопроса о повторе игры
        again = input("""Повторим?\n'1' == "ДА"\n'2' == "НЕТ"\nВведите цифру: """)

        if again == '1':  # при повторе, обновляет поле и рекурсивно запускает game()
            reboot_fild()
            game_ai(diff)
            break
        elif again == '2':  # возврат в меню и откат счета
            reboot_fild()
            c_win = 0
            z_win = 0
            return
        else:
            print("Введите '1' или '0' !!")
            continue


def step_ai_1(pl):
    """Ход ИИ на низкой сложности. Полностью случаен"""
    global fild
    global cell_dict_ai
    empty_cells = [i for i, cell in enumerate(fild) if cell == "-"]
    if empty_cells:
        rnd_i = random.choice(empty_cells)
        fild[rnd_i] = pl
        x_y = cell_dict_ai[str(rnd_i)]
        return x_y


def step_ai_2(pl, tern):
    """Ход ИИ на средней сложности. Первые 2 случайных хода, затем делает победный или блокирующий ход"""
    global fild
    time.sleep(1)
    if tern <= 4:
        print(random.choice(rand_speak))
        return step_ai_1(pl)
    else:
        empty_i = [i for i, cell in enumerate(fild) if cell == '-']
        if len(empty_i) > 1:  # если возможных вариантов хода больше 1
            for i in empty_i:  # цикл проверки всех возможных ходов
                fild_ai = copy.deepcopy(fild)  # копия не затрагивающая оригинал
                fild_ai[i] = pl  # виртуальный ход
                win = win_check(fild_ai)  # проверка виртуального хода
                if win == pl:
                    fild[i] = pl  # в случае победы, сохранение хода
                    x_y = cell_dict_ai[str(i)]
                    print(random.choice(win_speaks))
                    return x_y

            for i in empty_i:  # если не может выиграть, не дает выиграть сопернику
                fild_ai = copy.deepcopy(fild)
                fild_ai[i] = ('o' if pl == 'x' else 'x')
                win = win_check(fild_ai)
                if win == ('o' if pl == 'x' else 'x'):
                    fild[i] = pl
                    x_y = cell_dict_ai[str(i)]
                    print(random.choice(u_cant_win_speaks))
                    return x_y

            return step_ai_1(pl)  # если не было более удачного хода, делает случайный
        else:  # если ход последний
            fild_ai = copy.deepcopy(fild)  # проверка ради одной фразы)).
            fild_ai[empty_i[-1]] = pl
            win = win_check(fild_ai)
            if win == ('o' if pl == 'x' else 'x'):
                print('(ㆆ_ㆆ) - Как ты этого не заметил!!')
            return step_ai_1(pl)


def menu():
    while True:
        """Меню игры"""
        choice = input("    \nГлавное меню    \nВыберите один из вариантов, путем ввода символа варианта.\n"
                       "'1' == Игра против друга\n"
                       "'2' == Игра против компьютера\n"
                       "'q' == Выход.\n"
                       "Введите цифру:  ")
        c_lst = ['1', '2', 'q']

        if choice in c_lst:
            if choice == '1':
                game()
                continue  # при выходе из игры через "q" показывает меню
            elif choice == '2':
                flag = True
                while flag:
                    d_lst = ['1', '2', '3']
                    diff = input(("\nВыберите сложность, путем ввода символа варианта.\n"
                           "'1' == Низкая\n"
                           "'2' == Средняя\n"
                           "'3' == Назад.\n"
                           "Введите цифру:  "))

                    if diff in d_lst[:-1]:
                        game_ai(diff)
                        flag = False  # запуск игры и выход из обоих циклов
                    if diff == '3':
                        flag = False  # нормальная остановка цикла переход к else
                    elif diff not in d_lst:
                        print("Неправильный ввод! Убедитесь что ввели одну цифру!")
                        continue  # повтор выбора при некорректном вводе
                else:
                    continue  # возврат на внешний цикл при выборе "Назад"
                # break  # остановка внешнего цикла после окончания игры

            elif choice == 'q':
                print('\nПока Пока!')
                sys.exit()  # закрытие всех возможных рекурсий
        else:
            print("Неправильный ввод! Убедитесь что ввели одну цифру!")
            continue


print("\n!! ДОБРО ПОЖАЛОВАТЬ В ИГРУ КРЕСТИКИ-НОЛИКИ !!")  # при первом запуске программы
menu()


print("## Играюсь с гитом")







