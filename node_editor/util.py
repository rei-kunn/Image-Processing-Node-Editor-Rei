#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import dearpygui.dearpygui as dpg
import numpy as np


def convert_cv_to_dpg(image, width, height):
    # Resize the image
    resize_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
    # 8-bit unsigned integer format before color conversion
    if resize_image.dtype != np.uint8:
        resize_image = resize_image.astype(np.uint8)
    # Convert BGR to RGBA
    data = cv2.cvtColor(resize_image, cv2.COLOR_BGR2RGBA)
    # flatten the array, convert to float, and normalize the data to 0-1 range
    texture_data = np.true_divide(data.ravel(), 255.0).astype("f")
    return texture_data


# def check_camera_connection(max_device_count=4, is_debug=False):
#     device_no_list = []

#     for device_no in range(0, max_device_count):
#         if is_debug:
#             print('Check Device No:' + str(device_no).zfill(2), end='')

#         cap = cv2.VideoCapture(device_no)
#         ret, _ = cap.read()
#         if ret:
#             device_no_list.append(device_no)
#             if is_debug:
#                 print(' -> Find')
#         else:
#             if is_debug:
#                 print(' -> None')

#     return device_no_list


def check_camera_connection(specific_device_index=0, is_debug=False):
    if is_debug:
        print(f"Checking Device No: {specific_device_index}")

    cap = cv2.VideoCapture(specific_device_index)
    ret, _ = cap.read()
    cap.release()

    if ret:
        if is_debug:
            print(" -> Found")
        return [specific_device_index]
    else:
        if is_debug:
            print(" -> None")
        return []


def check_serial_connection(is_debug=False):
    import glob
    import sys

    import serial

    serial_device_no_list = []
    serial_device_no_list = []
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            serial_device_no_list.append(port)
        except (OSError, serial.SerialException):
            pass
    return serial_device_no_list


def dpg_set_value(tag, value):
    if dpg.does_item_exist(tag):
        dpg.set_value(tag, value)


def dpg_get_value(tag):
    value = None
    if dpg.does_item_exist(tag):
        value = dpg.get_value(tag)
    return value
