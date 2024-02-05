import dearpygui.dearpygui as dpg

dpg.create_context()

def link_callback(sender, app_data):
    print(app_data)
    print(sender)
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)

def delink_callback(sender, app_data):
    print("link has been detached")
    print(app_data)
    dpg.delete_item(app_data)

with dpg.window(label="I/O Test", width=700, height=500):

    with dpg.node_editor(callback=link_callback, delink_callback=delink_callback):
        with dpg.node(label="Node 1"):
            with dpg.node_attribute(label="Node A1 attribute",shape=dpg.mvNode_PinShape_Quad, attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_input_float(label="F1", width=150)
        
        with dpg.node(label="Node 2"):
            with dpg.node_attribute(label="Node A2"):
                dpg.add_input_float(label="F2", width=200)

# dpg.get_selected_nodes(22)
# dpg.get_selected_links(22)
# dpg.clear_selected_nodes(22)
# dpg.clear_selected_links(22)


dpg.create_viewport(title='Node Editor input/output test', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()