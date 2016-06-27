# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin


class JsxSyntaxHighlightingPlugin(Plugin):
    name = 'JSX Syntax Highlighting'
    description = 'No-op plugin that declares a dependency on pygments-lexer-babylon'
