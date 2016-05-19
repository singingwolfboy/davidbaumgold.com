from lektor.pluginsystem import Plugin
from lektor.types.formats import MarkdownType
from mistune import BlockLexer
from markupsafe import Markup
from textwrap import indent

def headings(text):
    """
    Given Markdown-formatted text, return a list of heading tokens.
    """
    tokens = BlockLexer().parse(text)
    headings = [token for token in tokens if token['type'] == 'heading']
    for heading in headings:
        del heading['type']
    return headings


def nested_headings(headings):
    """
    Given a list of heading tokens, return a nested list that represents
    the structure of those headings.

    This code was shamelessly stolen from
    https://github.com/waylan/Python-Markdown/blob/master/markdown/extensions/toc.py
    """
    ordered_list = []
    if len(headings):
        # Initialize everything by processing the first entry
        last = headings.pop(0)
        last['children'] = []
        levels = [last['level']]
        ordered_list.append(last)
        parents = []

        # Walk the rest nesting the entries properly
        while headings:
            t = headings.pop(0)
            current_level = t['level']
            t['children'] = []

            # Reduce depth if current level < last item's level
            if current_level < levels[-1]:
                # Pop last level since we know we are less than it
                levels.pop()

                # Pop parents and levels we are less than or equal to
                to_pop = 0
                for p in reversed(parents):
                    if current_level <= p['level']:
                        to_pop += 1
                    else:  # pragma: no cover
                        break
                if to_pop:
                    levels = levels[:-to_pop]
                    parents = parents[:-to_pop]

                # Note current level as last
                levels.append(current_level)

            # Level is the same, so append to
            # the current parent (if available)
            if current_level == levels[-1]:
                (parents[-1]['children'] if parents
                 else ordered_list).append(t)

            # Current level is > last item's level,
            # So make last item a parent and append current as child
            else:
                last['children'].append(t)
                parents.append(last)
                levels.append(current_level)
            last = t

    return ordered_list


def html_from_nested_headings(nested_headings, slug_links=False, list_class=""):
    if slug_links:
        from slugify import slugify
        def link_target(heading):
            return slugify(heading['text'])
    else:
        def link_target(heading):
            return "heading-{level}".format(level=heading['level'])

    ol = '<ol class="{list_class}">'.format(list_class=list_class)
    lines = [ol]
    for heading in nested_headings:
        if heading['children']:
            subhtml = recursive_html(heading['children'], link_target)
        else:
            subhtml = ""
        item_html = '  <li><a href="#{target}">{text}</a>{subhtml}</li>'.format(
            text=heading['text'],
            target=link_target(heading),
            subhtml=subhtml,
        )
        lines.append(item_html)
    lines.append("</ol>")
    return Markup("\n".join(lines))


def recursive_html(headings, link_target, depth=1):
    lines = ["<ol>"]
    for heading in headings:
        if heading['children']:
            subhtml = recursive_html(headings['children'], link_target, depth+1)
        else:
            subhtml = ""
        item_html = '  <li><a href="#{target}">{text}</a>{subhtml}</li>'.format(
            text=heading['text'],
            target=link_target(heading),
            subhtml=subhtml,
        )
        lines.append(item_html)
    lines.append("</ol>")
    return indent("\n".join(lines), "  "*depth)


def render_table_of_contents(field, slug_links=False, list_class=""):
    nh = nested_headings(headings(field.source))
    return html_from_nested_headings(
        nh, slug_links=slug_links, list_class=list_class,
    )


class MarkdownTOCPlugin(Plugin):
    name = 'Markdown Table of Contents'
    description = 'Generate a table of contents from a Markdown field.'

    def on_setup_env(self, **extra):
        list_class = self.get_config().get("class", "toc")
        links = self.get_config().get("links")
        slug_links = (links == "slug")
        if slug_links:
            from slugify import slugify

        def render_toc(field):
            return render_table_of_contents(
                field, slug_links=slug_links, list_class=list_class,
            )

        self.env.jinja_env.globals['render_toc'] = render_toc
