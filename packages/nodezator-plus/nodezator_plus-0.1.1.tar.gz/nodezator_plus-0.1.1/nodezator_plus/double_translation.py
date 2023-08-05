from nodezator.splashscreen.factoryfuncs import *
from nodezator import translation


def get_project_link_objs():
    node_icons = [
    render_layered_icon(
        chars=[chr(ordinal) for ordinal in (177, 178, 179)],
        dimension_name="height",
        dimension_value=18,
        colors=[
            BLACK,
            color,
            NODE_BODY_BG,
        ],
        background_width=18,
        background_height=18,
    )
    for color in (
        (185, 0, 100),
        (0, 155, 185),
        (0, 185, 100),
    )]


    WEB_ICON = render_layered_icon(
    chars=[chr(ordinal) for ordinal in (90, 91)],
    dimension_name="height",
    dimension_value=24,
    colors=[BLACK, (0, 100, 255)],
    background_width=24,
    background_height=24,)



    NODES_GALLERY_ICON = combine_surfaces(
    node_icons,
    retrieve_pos_from="topleft",
    assign_pos_to="topleft",
    offset_pos_by=(5, 5),
    )



    t=translation.TRANSLATION_HOLDER

    project_link_objs = List2D()

    surfaces = [
        (
            render_layered_icon(
                chars=[chr(ordinal) for ordinal in (183, 184, 185)],
                dimension_name="width",
                dimension_value=28,
                colors=[BLACK, WHITE, (77, 77, 105)],
                background_width=30,
                background_height=30,
            )
        ),
        (IMAGE_SURFS_DB["github_mark.png"][{"use_alpha": True}]),
        (IMAGE_SURFS_DB["github_mark.png"][{"use_alpha": True}]),
        NODES_GALLERY_ICON,
        (IMAGE_SURFS_DB["indie_python_logo.png"][{"use_alpha": True}]),
        (IMAGE_SURFS_DB["kennedy_logo.png"][{"use_alpha": True}]),
        (IMAGE_SURFS_DB["twitter_logo.png"][{"use_alpha": True}]),
        (IMAGE_SURFS_DB["discord_logo.png"][{"use_alpha": True}]),
        (IMAGE_SURFS_DB["patreon_logo.png"][{"use_alpha": True}]),
        WEB_ICON,
    ]

    rects = [surf.get_rect() for surf in surfaces]


    rectsman = RectsManager(rects.__iter__)

    rectsman.snap_rects_ip(
        retrieve_pos_from="bottomleft",
        assign_pos_to="topleft",
        offset_pos_by=(0, 5),
    )

    right = rectsman.move(10, 0).right

    project_links_data = (
        (
            t.splash_screen.application_website,
            t.splash_screen.application_website_url,
        ),
        (
            "Открытый код",
            "https://github.com/IndiePython/nodezator",
        ),
        (
            "Дискусии/форум",
            "https://github.com/IndiePython/nodezator/discussions",
        ),
        (
            "Публичные пакеты узлов",
            "https://gallery.nodezator.com",
        ),
        (
            t.splash_screen.project_website,
            t.splash_screen.project_website_url,
        ),
        (
            t.splash_screen.developer_website,
            t.splash_screen.developer_website_url,
        ),
        (
            t.splash_screen.developer_twitter,
            "https://twitter.com/KennedyRichard",
        ),
        (
            "Присоединись до нас",
            "https://indiepython.com/discord",
        ),
        (
            "Поддержите нас на патреоне",
            "https://patreon.com/KennedyRichard",
        ),
        (
            "Другой способ поддержки",
            "https://indiepython.com/donate",
        ),
    )


    for icon, rect, (text, url) in zip(surfaces, rects, project_links_data):


        text_surf = render_text(text=text, **TEXT_SETTINGS)

        text_rect = text_surf.get_rect()
        text_rect.midleft = (right, rect.centery)


        final_surf = unite_surfaces(
            [(icon, rect), (text_surf, text_rect)],
            padding=3,
            background_color=SPLASH_BG,
        )

        link_obj = Object2D.from_surface(
            surface=final_surf,
            on_mouse_release=(get_oblivious_callable(partial(open_url, url))),
            href=url,
        )

        project_link_objs.append(link_obj)


    project_link_objs.rect.snap_rects_ip(
        retrieve_pos_from="bottomleft",
        assign_pos_to="topleft",
        offset_pos_by=(0, 3),
    )


    project_links_caption = Object2D.from_surface(
        surface=(render_text(text=t.splash_screen.links, **TEXT_SETTINGS))
    )

    project_links_caption.rect.bottomleft = project_link_objs.rect.move(-10, -5).topleft

    project_link_objs.insert(0, project_links_caption)
    return project_link_objs