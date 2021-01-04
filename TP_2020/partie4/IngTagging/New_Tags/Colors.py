# Recognize main colors of the image


# Importing packages
import collections
import cv2
import numpy as np


# Definition Color list to store color components (upper and lower limits)
# Ex: {color: [min component, max component]}
# {'red': [array([160,  43,  46]), array([179, 255, 255])]}
def CreateColorList():
    dict = collections.defaultdict(list)

    # black
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 46])
    color_list = []
    color_list.append(lower_black)
    color_list.append(upper_black)
    dict['black'] = color_list

    # gray
    lower_gray = np.array([0, 0, 46])
    upper_gray = np.array([180, 43, 220])
    color_list = []
    color_list.append(lower_gray)
    color_list.append(upper_gray)
    dict['gray']=color_list

    # white
    lower_white = np.array([0, 0, 221])
    upper_white = np.array([180, 30, 255])
    color_list = []
    color_list.append(lower_white)
    color_list.append(upper_white)
    dict['white'] = color_list

    # red
    lower_red = np.array([156, 43, 46])
    upper_red = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['red'] = color_list

    # red2
    # lower_red = np.array([0, 43, 46])
    # upper_red = np.array([10, 255, 255])
    # color_list = []
    # color_list.append(lower_red)
    # color_list.append(upper_red)
    # dict['red_2'] = color_list

    # orange
    lower_orange = np.array([11, 43, 46])
    upper_orange = np.array([25, 255, 255])
    color_list = []
    color_list.append(lower_orange)
    color_list.append(upper_orange)
    dict['orange'] = color_list

    # yellow
    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([34, 255, 255])
    color_list = []
    color_list.append(lower_yellow)
    color_list.append(upper_yellow)
    dict['yellow'] = color_list

    # green
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    # upper_green = np.array([99, 255, 255])
    color_list = []
    color_list.append(lower_green)
    color_list.append(upper_green)
    dict['green'] = color_list

    # cyan [ like blue and green ==> Subsequent processing ]
    lower_cyan = np.array([78, 43, 46])
    upper_cyan = np.array([99, 255, 255])
    color_list = []
    color_list.append(lower_cyan)
    color_list.append(upper_cyan)
    dict['cyan'] = color_list

    # blue
    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])
    color_list = []
    color_list.append(lower_blue)
    color_list.append(upper_blue)
    dict['blue'] = color_list

    # purple
    # lower_purple = np.array([125, 43, 46])
    # upper_purple = np.array([155, 255, 255])
    # color_list = []
    # color_list.append(lower_purple)
    # color_list.append(upper_purple)
    # dict['purple'] = color_list

    # brown
    lower_brown = np.array([0, 43, 46])
    upper_brown = np.array([10, 255, 255])
    color_list = []
    color_list.append(lower_brown)
    color_list.append(upper_brown)
    dict['brown'] = color_list

    return dict


# Treat image + get color
def get_color(file_path):
    frame = cv2.imread(file_path)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_list = []
    sum_cnts = 0
    color_eff = []
    sum_list = []
    num_color_all = 0
    color_dict = CreateColorList()
    for d in color_dict:
        num_color_all = num_color_all + 1
        mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary, None, iterations=2)
        cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in cnts:
            sum += cv2.contourArea(c)
        sum_cnts = sum + sum_cnts
        sum_list.append([d, sum])

        if sum > 0:
            color_eff.append([d,sum])

    # Get the second element of the list
    def takeSecond(elem):
        return elem[1]

    # Sort by the second element of the list
    sum_list.sort(key=takeSecond, reverse=True)
    color_eff.sort(key=takeSecond, reverse=True)

    color_eff_index = []
    color_eff_sum = []
    for e in color_eff:
        color_eff_index.append(e[0])
        color_eff_sum.append(e[1])
    color_eff.clear()

    # convert "cyan" to "blue" or "green"
    if "cyan" in color_eff_index:
        tmp_index = color_eff_index.index("cyan")
        if tmp_index - 1 >= 0 and tmp_index + 1 < len(color_eff_index):
            diff_pre = color_eff_sum[tmp_index - 1] - color_eff_sum[tmp_index]
            diff_next = color_eff_sum[tmp_index] - color_eff_sum[tmp_index + 1]
            if diff_pre < diff_next:
                color_eff_sum[tmp_index - 1] += color_eff_sum[tmp_index]
            else:
                color_eff_sum[tmp_index + 1] += color_eff_sum[tmp_index]
        elif tmp_index - 1 >= 0:
            color_eff_sum[tmp_index - 1] += color_eff_sum[tmp_index]
        else:
            color_eff_sum[tmp_index + 1] += color_eff_sum[tmp_index]
        del color_eff_index[tmp_index]
        del color_eff_sum[tmp_index]

    # Regenerate color_eff and sort
    for i in range(len(color_eff_index)):
        color_eff.append([color_eff_index[i], color_eff_sum[i]])
    color_eff.sort(key=takeSecond, reverse=True)

    if len(color_eff) / num_color_all <= 3/10:
        for e in color_eff:
            if (e[1] / sum_cnts) >= 0.1:
                color_list.append(e[0])
    else:
        tmp = 0
        for e in color_eff:
            tmp = tmp + e[1] / sum_cnts
            if tmp <= 0.95 and (e[1] / sum_cnts) >= 0.2:
                color_list.append(e[0])
            else:
                pass

    return color_list