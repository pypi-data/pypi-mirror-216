import sys
from pathlib import Path

if sys.argv[1]=="on":
    path=str(Path(__file__).parent.parent)+"\\nodezator\\__main__.py"
    l=open(path).read().split("\n")
    if l[0]!="import nodezator_plus":
        l.insert(0, "import nodezator_plus")
        open(path, "w").write("\n".join(l))
elif sys.argv[1]=="off":
    path=str(Path(__file__).parent.parent)+"\\nodezator\\__main__.py"
    l=open(path).read().split("\n")
    if l[0]=="import nodezator_plus":
        open(path, "w").write("\n".join(l[1:]))