# This is a sample Python script.
import math
import os

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
x = []
y = []
z = []
data_dir = "data/dataset/"


def read_file():
    files = os.listdir(f"{data_dir}")
    for j in files:
        file = open(f"{data_dir + j}", "r")
        for i in file:
            line_i = i.split(",")
            if len(line_i) == 3:
                x.append(float(line_i[0]))
                y.append(float(line_i[1]))
                z.append(float(line_i[2].rstrip("\n")))
        print_hi()

def clear_array():
    x.clear()
    y.clear()
    z.clear()


def calculate_mean(val):
    return sum(val) / len(val)


def calculate_std(val):
    mean = calculate_mean(val)
    summation = 0
    for i in val:
        deviation = (i - mean) * (i - mean)
        summation = summation + deviation
    return math.sqrt(summation / len(val))


def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    x_avg = calculate_mean(x)
    y_avg = calculate_mean(y)
    z_avg = calculate_mean(z)
    print(f"Avg of x: {x_avg}")
    print(f"Avg of y: {y_avg}")
    print(f"Avg of z: {z_avg}")
    x_std = calculate_std(x)
    y_std = calculate_std(y)
    z_std = calculate_std(z)
    print(f"Std of x: {x_std}")
    print(f"Std of y: {y_std}")
    print(f"Std of z: {z_std}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_file()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
