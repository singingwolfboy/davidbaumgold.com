#!/usr/bin/env python
from inifile import IniFile
from pygments.formatters import HtmlFormatter

ifile = IniFile("../../configs/highlighter.ini")
style = ifile.get('pygments.style', 'default')
fmt = HtmlFormatter(style=style)
with open("pygments.css", "w") as f:
    f.write(fmt.get_style_defs())
