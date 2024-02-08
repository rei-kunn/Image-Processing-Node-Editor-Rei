import dearpygui.dearpygui as dpg

node_values= {}
attribute_id = 0
dpg.create_context()

def input_changed(sender, app_data, user_data):
    print(sender)
    print(app_data)
    node_values[user_data]= app_data
    print(f"Value of {user_data} updated to {app_data}")

def link_callback(sender, app_data):
    source_attr_id, target_attr_id = app_data
    # Now, ensure you're using the correct source_attr_id to look up the value
    if source_attr_id in node_values:
        # Transfer the value from source to target
        # This assumes you have a mechanism to apply this value to the target attribute's associated input or display
        print(f"Transferring value from {source_attr_id} to {target_attr_id}: {node_values[source_attr_id]}")
    else:
        print(f"Source value for attribute {source_attr_id} not found.")
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)

def delink_callback(sender, app_data):
    print("link has been detached")
    print(app_data)
    dpg.delete_item(app_data)

with dpg.window(label="I/O Test", width=700, height=500):

    with dpg.node_editor(callback=link_callback, delink_callback=delink_callback):
        with dpg.node(label="Node 1"):
            with dpg.node_attribute(label="Node A1 attribute",shape=dpg.mvNode_PinShape_Quad, attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_input_float(label="F1", width=150, callback=input_changed, user_data=attribute_id)
        
        with dpg.node(label="Node 2"):
            with dpg.node_attribute(label="Node A2"):
                dpg.add_input_float(label="F2", width=150, callback=input_changed)

# dpg.get_selected_nodes(22)
# dpg.get_selected_links(22)
# dpg.clear_selected_nodes(22)
# dpg.clear_selected_links(22)

dpg.create_viewport(title='Node Editor input/output test', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()