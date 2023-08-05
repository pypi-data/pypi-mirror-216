from nodezator.winman.menu import *


def create_menubar(self):
        menu_list = [
            {"label": t.menu.file,"children": [
                    {"label": t.menu.new, "key_text": "Ctrl+N", "icon": "new_native_file", "command": self.new},
                    {"label": t.menu.open, "key_text": "Ctrl+O", "icon": "folder", "command": self.open},
                    {"label": "------"},
                    { "label": t.menu.quit_app, "key_text": "Ctrl+W", "icon": "quit", "command": quit_app}
                ]
            },
            {
                "label": t.menu.edit,
                "children": [
                    {"label": t.menu.user_preferences, "icon": "tools", "command": edit_user_preferences}
                    ]
            },
            {
                "label": t.menu.help,
                "children": [
                    {"label": t.menu.help, "key_text": "F1", "icon": "question", "command": (partial(open_htsl_link, "htap://help.nodezator.pysite"))},
                    {"label": "General controls", "icon": "aww_icon", "command": (partial(open_htsl_link,("htap://help.nodezator.pysite", "/general-controls.htsl")))},
                    {"label": "Read manual", "icon": "aww_icon", "command": (partial(open_htsl_link, "htap://manual.nodezator.pysite"))},
                    {"label": "Find, download, publish nodes", "icon": "web_icon", "command": (partial(open_url,"https://gallery.nodezator.com"))},
                    {"label": t.menu.show_splash_screen, "command": self.splash_screen.get_focus},
                    {"label": t.menu.license, "icon": "badge", "command": (partial(open_htsl_link, "htap://nodezator.pysite/license.htsl"))},
                    {"label": "------"},
                    {"label": "Show user log","key_text": "Shift+Ctrl+J","command": (APP_REFS.ea.show_user_log_contents)},
                    {"label": t.menu.about,"icon": "info","command": (partial(open_htsl_link, "htap://nodezator.pysite/about.htsl"))},
                    {"label": "------"},
                    {"label": "nodezator plus", "command": lambda: print("now is not working")},
                ]
            },
        ]
        recent_files = get_recent_files()

        if recent_files:
            menu_list[0]["children"].insert(2, {"label": t.menu.open_recent, "icon": "folder", "children": [{"label": filepath.name, "command": partial(self.open,filepath)} for filepath in recent_files]})
        try:
            APP_REFS.source_path
        except AttributeError:
            graph_menu = {"label": t.menu.graph, "children": [{"label": (t.menu.rename_node_packs), "command": (APP_REFS.ea.present_rename_node_packs_form)}]}
            menu_list.insert(2, graph_menu)
        else:
            file_children_data = menu_list[0]["children"]
            file_children_data.insert(4, {"label": t.menu.save, "key_text": "Ctrl+S", "icon": "save", "command": self.save})
            file_children_data.insert(5, { "label": t.menu.save_as, "key_text": "Ctrl+Shift+S", "icon": "save_as", "command": self.save_as})
            file_children_data.insert(6, {"label": "-----"})

            for (index, label_text, icon_key, key_text, command_callable,) in (
                (7,t.menu.export_as_image,"image","Ctrl+E",APP_REFS.ea.export_as_image), 
                (8, t.menu.export_as_python,"python", "Ctrl+P", APP_REFS.ea.export_as_python)):

                command_data = {"label": label_text, "icon": icon_key, "key_text": key_text, "command": command_callable}
                file_children_data.insert(index, command_data)
            file_children_data.insert(9, {"label": "----"})

            graph_menu = {
                "label": t.menu.graph,
                "children": [
                    {"label": (t.menu.change_category_colors),"command": (APP_REFS.ea.change_category_colors)},
                    {"label": (t.menu.load_nodes), "command": (APP_REFS.ea.present_change_node_packs_form)},
                    {"label": "------"},
                    {"label": t.menu.execute_graph, "key_text": "F12", "command": APP_REFS.gm.execute_graph, "icon": "execute"},
                    {"label": (t.menu.execute_with_custom_stdout), "key_text": "Shift+F12", "command": (APP_REFS.gm.execute_with_custom_stdout), "icon": "execute_with_text"},
                ],
            }

            menu_list.insert(2, graph_menu)

            help_children_data = menu_list[-1]["children"]

            new_child = {"label": "Show custom stdout", "key_text": "Ctrl+J", "command": (APP_REFS.ea.show_custom_stdout_contents)}

            help_children_data.insert(-2, new_child)

        self.menubar = MenuManager(menu_list, horiz_bg_width=(SCREEN.get_width()))









def create_canvas_popup_menu(self):
        menu_list = []

        menu_list.append({"label": t.menu.new_text_block, "icon": "new_text_block", "command": APP_REFS.ea.insert_text_block})

        menu_list.append({"label": "New redirect node", "icon": "new_redirect_node", "command": partial(APP_REFS.ea.insert_node, None)})

        add_data_node_menu = {
            "label": "New data node",
            "icon": "new_data_node",
            "children": [],
        }

        menu_list.append(add_data_node_menu)

        ## populate it

        children = add_data_node_menu["children"]

        for preset_name, widget_data in WIDGET_DATA_PRESET_MAP.items():

            label_text = WIDGET_PRESET_MENU_LABEL_MAP[preset_name]

            children.append(
                {
                    "label": label_text,
                    "command": partial(
                        (APP_REFS.ea.insert_node),
                        widget_data,
                    ),
                }
            )

        children.append(
            {
                "label": "More options...",
                "command": (APP_REFS.ea.pick_widget_for_proxy_node),
            }
        )

        ### add a submenu to add a common operation
        ### (operation node)

        common_operations_menu = {
            "label": "Common operations",
            "icon": "operations",
            "children": [],
        }

        menu_list.append(common_operations_menu)

        ## populate it

        children = common_operations_menu["children"]

        for operation_id in OPERATIONS_MAP:

            children.append(
                {
                    "label": operation_id,
                    "command": partial(
                        (APP_REFS.ea.insert_node),
                        operation_id,
                    ),
                }
            )

        ### add a submenu to add builtin picks

        builtin_nodes_menu = {
            "label": "Builtin picks",
            "children": [],
        }

        menu_list.append(builtin_nodes_menu)

        ## divide into groups by first letter

        builtin_ids = sorted(
            BUILTIN_IDS_TO_CALLABLES_MAP,
            key=lambda item: item.lower(),
        )

        first_letter_and_group_pairs = groupby(
            builtin_ids, key=lambda item: item[0].lower()
        )

        ## populate it

        group_to_add = []
        children = builtin_nodes_menu["children"]

        for _, group in first_letter_and_group_pairs:

            group_to_add.extend(group)

            if len(group_to_add) > 10:

                first_letter = group_to_add[0][0]
                last_letter = group_to_add[-1][0]

                label_text = (
                    f"{first_letter}-{last_letter}"
                    if first_letter != last_letter
                    else f"{first_letter}"
                ).upper()

                children.append(
                    {
                        "label": label_text,
                        "children": [
                            {
                                "label": builtin_id,
                                "command": (
                                    partial(
                                        (APP_REFS.ea.insert_node),
                                        builtin_id,
                                    )
                                ),
                            }
                            for builtin_id in (group_to_add)
                        ],
                    }
                )

                group_to_add.clear()

        if group_to_add:

            first_letter = group_to_add[0][0]
            last_letter = group_to_add[-1][0]

            label_text = (
                f"{first_letter}-{last_letter}"
                if first_letter != last_letter
                else f"{first_letter}"
            ).upper()

            children.append(
                {
                    "label": label_text,
                    "children": [
                        {
                            "label": builtin_id,
                            "command": (
                                partial(
                                    APP_REFS.ea.insert_node,
                                    builtin_id,
                                )
                            ),
                        }
                        for builtin_id in group_to_add
                    ],
                }
            )

            group_to_add.clear()

        ### add a submenu to add a standard lib node

        stlib_nodes_menu = {
            "label": "Standard lib picks",
            "children": [],
        }

        menu_list.append(stlib_nodes_menu)

        ## divide into groups by first letter

        module_name_id_pairs = sorted(
            (
                (module_obj.__name__, stlib_id)
                for stlib_id, module_obj in STLIB_IDS_TO_MODULE.items()
            ),
            key=lambda item: (item[0], item[1].lower()),
        )

        module_name_and_group_pairs = groupby(
            module_name_id_pairs, key=lambda item: item[0]
        )

        ## populate it

        children = stlib_nodes_menu["children"]

        for module_name, group in module_name_and_group_pairs:

            stlib_ids = [item[1] for item in group]

            children.append(
                {
                    "label": module_name,
                    "children": [
                        {
                            "label": stlib_id,
                            "command": (
                                partial(
                                    APP_REFS.ea.insert_node,
                                    stlib_id,
                                )
                            ),
                        }
                        for stlib_id in stlib_ids
                    ],
                }
            )

        ### add a submenu to add useful encapsulations

        add_capsule_node_menu = {
            "label": "Useful encapsulations",
            "children": [],
        }

        menu_list.append(add_capsule_node_menu)

        ## populate it

        children = add_capsule_node_menu["children"]

        for capsule_id in sorted(CAPSULE_IDS_TO_CALLABLES_MAP):

            children.append(
                {
                    "label": capsule_id,
                    "command": partial(
                        (APP_REFS.ea.insert_node),
                        capsule_id,
                    ),
                }
            )

        ### reference the callable map, which we'll use to
        ### create the menu
        node_def_map = APP_REFS.node_def_map

        ### but before that, if the map isn't empty,
        ### add a separator

        if node_def_map:
            menu_list.append({"label": "-----"})

        ### iterate over the node defining map sorted keys
        ### using them to add "New [category name] node"
        ### submenus and their commands

        for (
            (node_pack_name, category_name, script_name),
            node_defining_object,
        ) in sorted(
            node_def_map.items(),
            key=lambda i: i[0],
        ):

            ### define the label text

            label_text = t.menu.new_category_node.format(category_name)

            ## check whether a submenu for that category
            ## already exists and reference it if so,
            ## otherwise create it and append it to the
            ## menu list

            for item in menu_list:

                if item["label"] == label_text:

                    category_submenu = item
                    break

            else:

                # create category submenu and append it to
                # the menu list

                # define icon key

                color_index = APP_REFS.category_index_map[
                    (
                        node_pack_name,
                        category_name,
                    )
                ]

                icon_key = "new_color_index_" + str(color_index) + "_node"

                category_submenu = {
                    "label": label_text,
                    "icon": icon_key,
                    "children": [],
                }

                menu_list.append(category_submenu)

            # build the command data and append it
            # to the children list

            category_submenu["children"].append(
                {
                    "label": script_name,
                    "command": partial(
                        APP_REFS.ea.insert_node,
                        node_defining_object,
                    ),
                }
            )

        ### finally instantiate the canvas popup menu using
        ### the data you put together

        self.canvas_popup_menu = MenuManager(
            menu_list,
            is_menubar=False,
            use_outline=True,
            keep_focus_when_unhovered=True,
        )



from nodezator.winman import menu


menu.MenuSetup.create_menubar=lambda self: create_menubar(self)