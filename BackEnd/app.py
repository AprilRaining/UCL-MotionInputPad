import numpy as np
from flask import Flask, request, url_for, redirect
from Utilities.treatment import *
from Utilities.Compare_lines import *
import os
import matplotlib
matplotlib.use('Agg')
app = Flask(import_name=__name__)


picture_path = "./Pictures"
tem_path = "./tem_picture"

store_list = []


@app.route('/check', methods=["POST"])
def check_gestures():
    if request.method == "POST":
        # print(request.values)
        val = request.get_json()
        # print("val is ", val)
        gestures_dict = load_gesture_data("picture_data.json")
        # signal_list = []
        signal_number = check_input(val, gestures_dict)
        print(signal_number)
        # for i, gesture in gestures_dict.items():
        #     # gesture_sim = check_input(val, gesture)
        #     gesture_sim = similarity(val, gesture)
        #     if math.isnan(gesture_sim):
        #         gesture_sim = 0
        #     signal_list.append(gesture_sim)
        #     print("the simi of " + str(i) + " is ", gesture_sim)
        # min_val = min(signal_list)
        if signal_number == -1:
            return "-1"

        if signal_number in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
            openWebpages(signal_number)

        # print("The signal is ", signal_number)
        draw_map(val, 0, tem_path)
        # cmpPicture(os.path.join(picture_path, "Raw_0.png"), os.path.join(tem_path, "Raw_0.png"))

        return signal_number


@app.route('/input', methods=["POST"])
def input_gestures():
    if request.method == "POST":
        print(request.values)
        val = request.get_json()
        print(val)
        global store_list
        store_list.append(val)
        print(len(store_list))
        return redirect(url_for('Home'))


@app.route('/input/cancel', methods=["POST"])
def cancel_gestures():
    if request.method == "POST":
        val = request.get_json()
        print(val)
        if val["clean"]:
            global store_list
            if len(store_list) >= 9:
                save_gesture_data(store_list)
                refreshPictures(store_list)
            store_list = []
        return redirect(url_for('Home'))


@app.route('/')
def Home():
    return "Home Page"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8081, debug=False)
    # cmpPicture(os.path.join(picture_path, "Raw_0.png"), os.path.join(tem_path, "Raw_0.png"))
