#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import cv2
import dearpygui.dearpygui as dpg
import numpy as np
from node.node_abc import DpgNodeABC
from node_editor.util import convert_cv_to_dpg, dpg_get_value, dpg_set_value


def image_process(image):
    return image


class Node(DpgNodeABC):
    _ver = "0.0.1"

    node_label = "ON/OFF Switch"
    node_tag = "OnOffSwitch"

    _switch_on = "ON"
    _switch_off = "OFF"

    _opencv_setting_dict = None

    def __init__(self):
        pass

    def add_node(
        self,
        parent,
        node_id,
        pos=[0, 0],
        opencv_setting_dict=None,
        callback=None,
    ):
        # タグ名
        tag_node_name = str(node_id) + ":" + self.node_tag
        tag_node_input01_name = tag_node_name + ":" + self.TYPE_IMAGE + ":Input01"
        tag_node_input01_value_name = (
            tag_node_name + ":" + self.TYPE_IMAGE + ":Input01Value"
        )
        tag_node_output01_name = tag_node_name + ":" + self.TYPE_IMAGE + ":Output01"
        tag_node_output01_value_name = (
            tag_node_name + ":" + self.TYPE_IMAGE + ":Output01Value"
        )

        tag_switch_select_name = tag_node_name + ":" + self.TYPE_TEXT + ":Switch"
        tag_switch_select_value_name = (
            tag_node_name + ":" + self.TYPE_IMAGE + ":SwitchValue"
        )

        # OpenCV向け設定
        self._opencv_setting_dict = opencv_setting_dict
        small_window_w = int(self._opencv_setting_dict["process_width"] / 2)
        small_window_h = int(self._opencv_setting_dict["process_height"] / 2)

        # 初期化用黒画像
        black_image = np.zeros((small_window_w, small_window_h, 4))
        black_texture = convert_cv_to_dpg(
            black_image,
            small_window_w,
            small_window_h,
        )

        # テクスチャ登録
        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(
                small_window_w,
                small_window_h,
                black_texture,
                tag=tag_node_output01_value_name,
                format=dpg.mvFormat_Float_rgba,
            )

        # ノード
        with dpg.node(
            tag=tag_node_name,
            parent=parent,
            label=self.node_label,
            pos=pos,
        ):
            # 入力端子
            with dpg.node_attribute(
                tag=tag_node_input01_name,
                attribute_type=dpg.mvNode_Attr_Input,
            ):
                dpg.add_text(
                    tag=tag_node_input01_value_name,
                    default_value="Input BGR image",
                )
            # 画像
            with dpg.node_attribute(
                tag=tag_node_output01_name,
                attribute_type=dpg.mvNode_Attr_Output,
            ):
                dpg.add_image(tag_node_output01_value_name)
            # ON/OFF切り替え
            with dpg.node_attribute(
                tag=tag_switch_select_name,
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_radio_button(
                    (self._switch_on, self._switch_off),
                    tag=tag_switch_select_value_name,
                    default_value=self._switch_on,
                    horizontal=True,
                )

        return tag_node_name

    def update(
        self,
        node_id,
        connection_list,
        node_image_dict,
        node_result_dict,
    ):
        tag_node_name = str(node_id) + ":" + self.node_tag
        output_value01_tag = tag_node_name + ":" + self.TYPE_IMAGE + ":Output01Value"

        tag_switch_select_value_name = (
            tag_node_name + ":" + self.TYPE_IMAGE + ":SwitchValue"
        )

        small_window_w = int(self._opencv_setting_dict["process_width"] / 2)
        small_window_h = int(self._opencv_setting_dict["process_height"] / 2)

        # 画像取得元のノード名(ID付き)を取得する
        connection_info_src = ""
        for connection_info in connection_list:
            connection_info_src = connection_info[0]
            connection_info_src = connection_info_src.split(":")[:2]
            connection_info_src = ":".join(connection_info_src)

        # ON/OFF選択状態取得
        switch_status = dpg_get_value(tag_switch_select_value_name)

        # 画像取得
        frame = None
        if switch_status == self._switch_on:
            frame = node_image_dict.get(connection_info_src, None)

            if frame is not None:
                frame = image_process(frame)

        # 描画
        if frame is not None:
            texture = convert_cv_to_dpg(
                frame,
                small_window_w,
                small_window_h,
            )
            dpg_set_value(output_value01_tag, texture)

        return frame, None

    def close(self, node_id):
        pass

    def get_setting_dict(self, node_id):
        tag_node_name = str(node_id) + ":" + self.node_tag

        pos = dpg.get_item_pos(tag_node_name)

        setting_dict = {}
        setting_dict["ver"] = self._ver
        setting_dict["pos"] = pos

        return setting_dict

    def set_setting_dict(self, node_id, setting_dict):
        pass
