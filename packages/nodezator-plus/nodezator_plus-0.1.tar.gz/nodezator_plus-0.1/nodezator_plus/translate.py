from nodezator.userprefsman import validation, main
from nodezator import translation
from nodezator.ourstdlibs.pyl import load_pyl
from pathlib import Path
validation.AVAILABLE_LANGUAGES+=("Русский",)
lang=load_pyl(main.APP_CONFIG_DIR / "config.pyl")["LANGUAGE"]


if lang=="Русский" or lang=="Polski":
    main.USER_PREFS["LANGUAGE"]=lang
    if lang=="Русский": LANG_DEPENDENT_DATA_DIR = Path(__file__).parent/"ru"
    # elif lang=="Polski": LANG_DEPENDENT_DATA_DIR = Path(__file__).parent/"pl"
    
    DIALOGS_MAP = translation.ChainMap(
        load_pyl(LANG_DEPENDENT_DATA_DIR / "dialogs_map.pyl"),
        translation.DIALOGS_MAP,
    )
    STATUS_MESSAGES_MAP = translation.ChainMap(
        load_pyl(LANG_DEPENDENT_DATA_DIR / "status_messages_map.pyl"),
        translation.STATUS_MESSAGES_MAP,
    )

    TRANSLATION_MAP = translation.merge_nested_dicts(
        load_pyl(LANG_DEPENDENT_DATA_DIR / "translations_map.pyl"),
        translation.TRANSLATION_MAP,
    )
    translation.TRANSLATION_HOLDER = translation.NestedObjectFromDict(TRANSLATION_MAP)

    from nodezator.splashscreen import factoryfuncs
    from . import double_translation
    factoryfuncs.get_project_link_objs=double_translation.get_project_link_objs