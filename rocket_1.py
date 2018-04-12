import math
m_rocket = 2150
m_fuel = 10000
g = 1.62
а = 29.43
v_fuel = 3660
dt = 0.01
f = open('rocket 1 output.txt', 'w')


def take():  #Функция, считывающая условие из файла в двумерный список.
    field = open('rocket 1 input.txt', 'r').read().split()
    out = []
    for j in range(int(len(field) / 6)):
        out.append([field[6 * j + 3].replace(field[6 * j + 3][0], ''), field[6 * j + 4],
                    field[6 * j + 5].replace(field[6 * j + 5][len(field[6 * j + 5])-1], '')])
    for i in range(len(out)):
        for j in range(3):
            out[i][j] = float(out[i][j])
    return out


first = [0, 0, 0, 0] #скорости по х, у, координаты по х, у

#print(take())

def once (alfa, u, ar): #изменение в движении ракеты за маленький промежуток времени dt, считая движение равноускоренным
    global m_fuel
    a_full = u * v_fuel / (m_fuel + m_rocket)
    vx = ar[0] + a_full * math.cos(math.radians(alfa)) * dt
    vy = ar[1] + (a_full * math.sin(math.radians(alfa)) - g) * dt
    rx = ar[2] + ar[0] * dt + a_full * math.cos(math.radians(alfa)) * dt * dt / 2
    ry = ar[3] + ar[1] * dt + (a_full * math.sin(math.radians(alfa)) - g) * dt * dt / 2
    m_fuel = m_fuel - u * dt
    return [vx, vy, rx, ry]


def many_times (alfa, u_fuel , t, mass): #просчитывает скорость и координаты аппарата через один такт
    for i in range(int(t/dt)):
        mass = once(alfa, u_fuel / t, mass)
        if mass[3] < 0:
            mass[3] = 0
            if (abs(mass[0]) < 1) and (abs(mass[1]) < 3):
                return ['success', [int(j) for j in mass]]
            else:
                return ['crush', [int(j) for j in mass]]
        if m_fuel < u_fuel / t * dt:
            return [int(j) for j in mass]
    return [int(j) for j in mass]


def output (ar): #оформляет вывод
    if len(ar) == 4:
        f.write(str(ar[0]) + '\t\t' + str(ar[1]) + '\t\t' + str(ar[2]) + '\t\t' + str(ar[3]) + '\n')
    else:
        f.write(ar[0] + '\t\t' + str(ar[1][0]) + '\t\t' + str(ar[1][1]) + '\t\t' + str(ar[1][2])
                + '\t\t' + str(ar[1][3]) + '\n')
    return True

def all_the_way (ar): #считает координаты за весь полет
    mass = first
    for i in ar:
        mass = many_times(i[0], i[1], i[2], mass)
        if mass[0] == 'success' or mass[0] == 'crush':
            output (mass)
            return True
        output (mass)
    return True

all_the_way(take())

f.close()
