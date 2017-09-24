# -*- coding: utf-8 -*-
import re
from lektor.pluginsystem import Plugin


TWO_HYPHENS = re.compile("\s--\s")


class EmDashPlugin(Plugin):
    name = 'Em-Dash Plugin'
    description = 'Replaces two hyphens with an em-dash in paragraphs'

    def on_markdown_config(self, config, **extra):
        class EmDashMixin(object):
            def paragraph(self, text):
                dashed_text = TWO_HYPHENS.sub(" — ", text)
                return '<p>%s</p>\n' % dashed_text.strip(' ')

        config.renderer_mixins.append(EmDashMixin)
