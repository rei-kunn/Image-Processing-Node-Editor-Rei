import numpy as np
import cv2
import json
import os
import argparse

def check_camera_connection(specific_device_index=0, is_debug=False):
    if is_debug:
        print(f'Checking Device No: {specific_device_index}')

    cap = cv2.VideoCapture(specific_device_index)
    ret, _ = cap.read()
    cap.release()

    if ret:
        if is_debug:
            print(' -> Found')
        return [specific_device_index]
    else:
        if is_debug:
            print(' -> None')
        return []

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--setting",
        type=str,
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), 'setting.json')),
    )
    parser.add_argument("--unuse_async_draw", action="store_true")
    parser.add_argument("--use_debug_print", action="store_true")

    args = parser.parse_args()
    return args

args = get_args()
setting = args.setting
unuse_async_draw = args.unuse_async_draw
use_debug_print = args.use_debug_print

print('**** Load Config ********')
opencv_setting_dict = None
with open(setting) as fp:
    opencv_setting_dict = json.load(fp)
webcam_width = opencv_setting_dict['webcam_width']
webcam_height = opencv_setting_dict['webcam_height']
print('**** Check Camera Connection ********')
device_no_list = check_camera_connection()
camera_capture_list = []
for device_no in device_no_list:
    video_capture = cv2.VideoCapture(device_no)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, webcam_height)
    camera_capture_list.append(video_capture)

# カメラ設定保持
opencv_setting_dict['device_no_list'] = device_no_list
opencv_setting_dict['camera_capture_list'] = camera_capture_list

# # Directly use the specified device index for "Nuroum V11"
# device_index_nuroum_v11 = 0  # Assuming the Nuroum V11 camera is at index 1
# video_capture = cv2.VideoCapture(device_index_nuroum_v11)
# video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
# video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, webcam_height)

print('**** Camera Initialization Complete ********')

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame")
        break
    cv2.imshow('Camera Test - Nuroum V11', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
