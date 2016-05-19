from lektor.pluginsystem import Plugin
from mistune import BlockLexer
from markupsafe import Markup
from textwrap import indent
try:
    from slugify import slugify
except ImportError:
    slugify = None


def headings(text):
    """
    Given Markdown-formatted text, return a list of heading tokens.
    """
    tokens = BlockLexer().parse(text)
    htokens = [token for token in tokens if token['type'] == 'heading']
    for token in htokens:
        del token['type']
    return htokens


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


def html_from_nested_headings(
        nested_headings, links=True, slug_links=False,
        toc_class="", list_class="", list_item_class="",
        position=None,
    ):
    """
    Recursive function to generate HTML from a list of nested headings.

    Arguments:
        nested_headings: List of nested heading tokens
        links: Should the table of contents include links to the section on
            the page?
        slug_links: Link to slugified text, instead of heading position.
            Only used if `links` is True. Requires the `slugify` module
            to be installed.
        toc_class: The CSS class(es) to apply to the outermost <ol> element
            in the table of contents.
        list_class: The CSS class(es) to apply to *every* <ol> element in the
            table of contents, including all nested <ol>s.
        list_item_class: The CSS class(es) to apply to *every* <li> element
            in the table of contents, including all nested <li>s.
        position: A tuple of positional indicators, used for generating
            non-slug links. Do not pass this yourself; it is used for keeping
            track of position with recursion.
    """
    ol = "<ol>"

    if not position:
        position = []
        # this is the outermost <ol>, so include the toc_class
        if toc_class or list_class:
            ol = '<ol class="{toc_class} {list_class}">'.format(
                toc_class=toc_class,
                list_class=list_class,
            )
    else:
        if list_class:
            ol = '<ol class="{list_class}">'.format(list_class=list_class)

    depth = len(position)

    lines = [ol]
    for index, heading in enumerate(nested_headings, start=1):
        if heading['children']:
            subpos = position.copy()
            subpos.append(index)
            subhtml = html_from_nested_headings(
                nested_headings=heading['children'],
                links=links, slug_links=slug_links, toc_class=toc_class,
                list_class=list_class, list_item_class=list_item_class,
                position=subpos,
            )
        else:
            subhtml = ""

        item_html = ["  "]  # indent li
        if list_item_class:
            li = '<li class="{li_class}">'.format(li_class=list_item_class)
        else:
            li = '<li>'
        item_html.append(li)
        if links:
            if slug_links:
                target = slugify(heading['text'])
            else:
                strpos = [str(i) for i in position]
                strpos.insert(0, "heading")
                strpos.append(str(index))
                target = "-".join(strpos)
            item_html.append('<a href="#{target}">'.format(target=target))
        item_html.append(heading['text'])
        if links:
            item_html.append('</a>')
        item_html.append(subhtml)
        item_html.append('</li>')

        lines.append("".join(item_html))

    lines.append("</ol>")
    indented = indent("\n".join(lines), "  " * depth)
    return Markup(indented)


def render_table_of_contents(
        field, links=True, slug_links=False,
        toc_class="", list_class="", list_item_class=""
    ):
    nh = nested_headings(headings(field.source))
    return html_from_nested_headings(
        nh, links=links, slug_links=slug_links,
        toc_class=toc_class, list_class=list_class,
        list_item_class=list_item_class,
    )


class MarkdownTOCPlugin(Plugin):
    name = 'Markdown Table of Contents'
    description = 'Generate a table of contents from a Markdown field.'

    def on_setup_env(self, **extra):
        config = self.get_config()
        links = config.get("links", "index")
        use_links = (links.lower() not in ("no", "none"))
        slug_links = (links == "slug")
        toc_class = config.get("class", "toc")
        list_class = config.get("list_class", "")
        list_item_class = config.get("list_item_class", "")

        if slug_links:
            # throw ImportError if not installed
            from slugify import slugify

        def render_toc(field):
            return render_table_of_contents(
                field=field, links=use_links, slug_links=slug_links,
                toc_class=toc_class, list_class=list_class,
                list_item_class=list_item_class,
            )

        self.env.jinja_env.globals['render_toc'] = render_toc
