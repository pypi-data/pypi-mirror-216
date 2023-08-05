# from widget.checkbutton import CheckButton
# CheckButton(False, "test", 64, command=lambda: print("hello"))
# from graphman import nodepacksissues
import sys
if len(sys.argv)<2:
    from . import translate
    from . import anim, menu1
else:
    from . import cli