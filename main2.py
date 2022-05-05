import tsplib95
from queue import LifoQueue
import random
import math
import numpy as np
import time


sizeTab = 0
queue_size = 5
max_iteration = 5

tour = [0 for j in range(int(sizeTab))]
optTour = [0 for j in range(int(sizeTab))]
tour_array = [[0 for _ in range(sizeTab)] for _ in range(10)]
parametersSizes = [0 for j in range(5)]
results = [[0 for _ in range(5)] for _ in range(5)]

matr = np.zeros((10,10))

time1 = 0

iteration_counter = 0
minimum2 = 0
minimum_tour = tour.copy()
count_iterations = 0
array_iterator = 0
isLongTermUsed = False


def close_neighbour(optTour, matr, tour):
    for i in range(0, int(sizeTab) - 1):
        cls = matr[optTour[i]][tour[0]]
        optTour[i + 1] = tour[0]
        if len(tour) > 1:
            for j in range(1, len(tour)):
                if matr[optTour[i]][tour[j]] < cls:
                    cls = matr[optTour[i]][tour[j]]
                    optTour[i + 1] = tour[j]
            tour.remove(optTour[i + 1])

        else:
            optTour[i + 1] = tour[0]
    return optTour

def create_and_fill_matrix(n):
    global matr
    matr = np.zeros((n, n))
    for i in range(n):
         for j in range(n):
            if i != j:
                 matr[i][j] = random.randint(0,1000)


def destination(sizeTab, matr, tour3):
    weight = 0
    for i in range(0, int(sizeTab) - 1):
        weight += matr[tour3[i]][tour3[i + 1]]

    weight += matr[tour3[int(sizeTab) - 1]][tour3[0]]
    return weight


def prepare(tour):
    tour_copy = tour.copy()
    optTour[0] = tour[0]
    tour_copy.remove(tour[0])
    random.shuffle(tour_copy)
    close_neighbour(optTour, matr, tour_copy)
    tour2_copy = optTour.copy()
    extended_optimum = destination(sizeTab, matr, tour2_copy)

    for i in range(1, int(sizeTab)):
        tour_copy = tour.copy()
        optTour[0] = tour[i]
        tour_copy.remove(optTour[0])
        random.shuffle(tour_copy)
        close_neighbour(optTour, matr, tour_copy)

        if destination(sizeTab, matr, optTour) < extended_optimum:
            extended_optimum = destination(sizeTab, matr, optTour)
            tour2_copy = optTour.copy()
    return tour2_copy


def reverse_sublist(my_list, start, end):
    my_list[start:end] = my_list[start:end][::-1]
    return my_list


def invert(swap_tour, i, j):
    reverse_sublist(swap_tour, i, j + 1)
    zmienna2 = destination(len(swap_tour), matr, swap_tour)
    reverse_sublist(swap_tour, i, j + 1)
    return zmienna2


def accelerate(act_tour, index1, index2, act_dest):
    if index2 - index1 + 1 != sizeTab:
        for i in range(index1, index2 + 2):
            if i == sizeTab:
                act_dest -= matr[act_tour[i - 1]][act_tour[0]]
            else:
                act_dest -= matr[act_tour[i - 1]][act_tour[i]]

        for i in range(index1 + 1, index2 + 1):
            if i == sizeTab:
                act_dest += matr[act_tour[0]][act_tour[i - 1]]
            else:
                act_dest += matr[act_tour[i]][act_tour[i - 1]]

        if index2 + 1 == sizeTab:
            act_dest += matr[act_tour[index1]][act_tour[0]]
        else:
            act_dest += matr[act_tour[index1]][act_tour[index2 + 1]]

        act_dest += matr[act_tour[index1 - 1]][act_tour[index2]]

    else:
        for i in range(index1, index2 + 1):
            act_dest -= matr[act_tour[i - 1]][act_tour[i]]
        for i in range(index1, index2 + 1):
            act_dest += matr[act_tour[i]][act_tour[i - 1]]

    return act_dest


def invert2(swap_tour, i, j):
    reverse_sublist(swap_tour, i, j + 1)
    zmienna2 = swap_tour
    return zmienna2


def invert3(swap_tour, i, j):
    reverse_sublist(swap_tour, i, j + 1)
    zmienna2 = swap_tour
    reverse_sublist(swap_tour, i, j + 1)
    return zmienna2


def isInQueue(x, y):
    temp = (x, y)

    for elem in list(q.queue):
        if elem == temp:
            return True
    return False


def koks_funkcja(acutal_tour):
    actual_destination = destination(sizeTab, matr, acutal_tour)
    mini = accelerate(acutal_tour, 0, 2, actual_destination)
    tour_mini = acutal_tour.copy()
    k = 0
    l = 1

    global minimum2
    global minimum_tour
    for i in range(0, len(acutal_tour)):
        for j in range(i + 1, len(acutal_tour)):
            potential_mini = accelerate(acutal_tour, i, j, actual_destination)

            if isInQueue(i, j):
                if potential_mini < minimum2:
                    minimum2 = potential_mini
                    mini = potential_mini
                    minimum_tour = invert3(acutal_tour, i, j)
                    tour_mini = invert3(acutal_tour, i, j)
                    k = i
                    l = j
            else:
                if potential_mini < mini:
                    mini = potential_mini
                    tour_mini = invert3(acutal_tour, i, j)

                    k = i
                    l = j

    if not isInQueue(k, l):
        if q.full():
            q.get()

        q.put((k, l))

    global iteration_counter

    if mini < minimum2:
        minimum2 = mini
        minimum_tour = tour_mini.copy()
        iteration_counter = 0
    else:
        iteration_counter = iteration_counter + 1

    global array_iterator
    global max_iteration
    global tour_array
    if iteration_counter >= max_iteration:

        global isLongTermUsed
        if isLongTermUsed:
            return
        else:
            iteration_counter = 0
            num = random.randint(0, array_iterator - 1)
            isLongTermUsed = True
            koks_funkcja(tour_array[num])

    if array_iterator < 10:
        tour_array[array_iterator] = acutal_tour
        array_iterator += 1
    else:
        for i in range(9):
            tour_array[i] = tour_array[i + 1]
        tour_array[9] = acutal_tour.copy()

    koks_funkcja(invert2(acutal_tour, k, l))


def setSizes():
    global parametersSizes
    global sizeTab
    parametersSizes[0] = math.floor(math.log2(sizeTab))
    parametersSizes[1] = math.floor(math.sqrt(sizeTab))
    parametersSizes[2] = math.floor(sizeTab / 2)
    parametersSizes[3] = sizeTab
    parametersSizes[4] = math.floor(sizeTab * math.log2(sizeTab))


def main():
    global sizeTab
    while sizeTab<=0:
        sizeTab = int(input("Podaj wielkość instancji: "))
        if sizeTab <= 0:
            print("Wielkosc instancji musi byc liczba dodatnia")

    create_and_fill_matrix(sizeTab)

    global tour
    global optTour
    global tour_array
    tour = [0 for j in range(int(sizeTab))]
    optTour = [0 for j in range(int(sizeTab))]
    tour_array = [[0 for _ in range(sizeTab)] for _ in range(10)]

    global matr
    #print(matr)
    setSizes()
    global count_iterations
    count_iterations = 0

    for i in range(0, int(sizeTab)):
        tour[i] = i
    random.shuffle(tour)

    global mini_tour
    global minimum_tour
    global time1

    sum = 0
    for j in range(10):
        global iteration_counter
        iteration_counter = 0
        for i in range(0, int(sizeTab)):
            tour[i] = i
        random.shuffle(tour)
        tourrr = prepare(tour)
        global minimum2
        minimum2 = destination(sizeTab, matr, tourrr)
        global max_iteration
        max_iteration = sizeTab/2
        global queue_size
        queue_size = sizeTab/2
        global q
        q = LifoQueue(queue_size)
        a1 = time.time()
        koks_funkcja(tourrr)
        b1 = time.time()

        time1+= ((b1-a1)*1000)
        tour_array = [[0 for _ in range(sizeTab)] for _ in range(10)]
        global array_iterator
        array_iterator = 0
        global isLongTermUsed
        isLongTermUsed = False

        sum += minimum2

    avgg = sum / 10
    time1 /= 10
    print(avgg)
    print(time1)

if __name__ == "__main__":
    main()