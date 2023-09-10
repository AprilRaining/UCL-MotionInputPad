import json
import os
import cv2
import numpy as np
import webbrowser
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
dir_path = os.path.dirname(os.path.dirname(__file__))


# url_dict = {0: "https://www.amazon.co.uk/",
#             1: "https://www.ubereats.com/gb",
#             2: "https://www.google.com/",
#             3: "https://stablediffusionweb.com/#demo",
#             4: "https://www.youtube.com/",
#             5: "https://www.crazygames.com/",
#             6: "https://www.bilibili.com/",
#             7: "https://twitter.com/home",
#             8: "https://www.ucl.ac.uk/"}


def aveHash(image):

    image = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
    grey_map = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    average = np.mean(grey_map)
    print(average)

    hash_list = []
    for i in range(grey_map.shape[0]):
        for j in range(grey_map.shape[1]):
            if grey_map[i, j] > average:
                hash_list.append(1)
            else:
                hash_list.append(0)
    return hash_list


def diffHash(image):

    image = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
    grey_map = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    hash_list = []

    for i in range(grey_map.shape[0]):
        for j in range(grey_map.shape[1] - 1):
            if grey_map[i, j] > grey_map[i, j + 1]:
                hash_list.append(1)
            else:
                hash_list.append(0)
    return hash_list


def perceptionHash(image):

    image = cv2.resize(image, (32, 32), interpolation=cv2.INTER_CUBIC)
    grey_map = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    dct = cv2.dct(np.float32(grey_map))

    dct_roi = dct[0:8, 0:8]

    hash_list = []
    average = np.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > average:
                hash_list.append(1)
            else:
                hash_list.append(0)
    return hash_list


def greyHistogram(image1, image2):

    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])

    degree = 0

    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree += 1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i])
        else:
            degree += 1
    degree /= len(hist1)

    return degree


def greyHistogramAll(image1, image2, size=(256, 256)):

    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += greyHistogram(im1, im2)
    sub_data /= 3
    return sub_data


def cmpHash(hash_list1, hash_list2):

    n = 0
    if len(hash_list1) != len(hash_list2):
        return -1

    for i in range(len(hash_list1)):
        if hash_list1[i] == hash_list2[i]:
            n = n + 1
    return n/len(hash_list1)


def cmpPicture(image1_path, image2_path):
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    print(aveHash(image1), aveHash(image2))
    print("ave:", cmpHash(aveHash(image1), aveHash(image2)))
    print("diff:", cmpHash(diffHash(image1), diffHash(image2)))
    print("per:", cmpHash(perceptionHash(image1), perceptionHash(image2)))

    print("grey:", greyHistogramAll(image1, image2))


def save_gesture_data(data_list):
    json_dict = {}
    for i, item in enumerate(data_list):
        json_dict[i] = item["list"]
    with open(os.path.join(dir_path, "Picture_data", "picture_data.json"), mode="w") as f:
        json.dump(json_dict, f)


def load_gesture_data(file_name):
    with open(os.path.join(dir_path, "Picture_data", file_name)) as f:
        json_dict = json.load(f)
    return json_dict





def draw_map(point_list, num, path=os.path.join(dir_path, "Pictures")):
    if num > 8:
        return
    x_values = point_list[0]
    y_values = point_list[1]

    y_values = np.array(y_values)
    y_values = 1 - y_values

    plt.plot(x_values, y_values)
    x_min = -0.05
    x_max = 1.05
    y_min = -0.05
    y_max = 1.05
    plt.xlim((x_min, x_max))
    plt.ylim((y_min, y_max))
    plt.axis('off')

    plt.savefig(os.path.join(path, "Raw_" + str(num) + ".png"))
    plt.close()


def refreshPictures(store_lists, path=os.path.join(dir_path, "Pictures")):
    for f in os.listdir(path):
        print(os.path.join(path, f))
        os.remove(os.path.join(path, f))
    for i in store_lists:
        draw_map(i["list"], i["count"])


def openWebpages(signal):
    url_dict = load_gesture_data("commands.json")
    webbrowser.open_new(url_dict[signal])


if __name__ == "__main__":
    openWebpages(0)
    # print("sd")
    # webbrowser.open_new("https://www.amazon.co.uk/")