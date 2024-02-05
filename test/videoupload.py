import dearpygui.dearpygui as dpg
import cv2
import numpy as np

dpg.create_context()

def update_texture(sender, app_data, user_data):
    ret, frame = user_data.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.ascontiguousarray(frame)
        dpg.set_value("webcam_texture", frame)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Could not open video device")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

with dpg.texture_registry():
    dpg.add_dynamic_texture(width, height, np.zeros((height, width, 3), dtype=np.uint8), tag="webcam_texture")

with dpg.window(label="Node Editor Window"):
    with dpg.node_editor():
        with dpg.node(label="Webcam Node"):
            with dpg.node_attribute():
                dpg.add_image("webcam_texture")

with dpg.handler_registry():
    dpg.render_dearpygui_frame(update_texture, user_data=cap)

dpg.create_viewport(title='Webcam Node with Dear PyGui', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

cap.release()
dpg.destroy_context()
