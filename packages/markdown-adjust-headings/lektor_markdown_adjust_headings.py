from lektor.pluginsystem import Plugin
from lektor.types.formats import MarkdownType


class MarkdownAdjustHeadingsPlugin(Plugin):
    name = 'Adjust Markdown headings'
    description = 'Adjust Markdown headings to different relative levels.'

    def on_setup_env(self, **extra):
        should_slugify = self.get_config().get('slugify')
        if should_slugify:
            from slugify import slugify
            self.slugify = slugify
        else:
            self.slugify = None

    def on_markdown_config(self, config, **extra):
        slugify = self.slugify

        class AdjustHeadingsMixin(object):
            def header(self, text, level, raw=None):
                markdown_fields = [
                    field for field in self.record.datamodel.fields
                    if isinstance(field.type, MarkdownType)
                ]
                adjustments = [
                    field.options.get("markdown_headings_adjust")
                    for field in markdown_fields
                    if field.options.get("markdown_headings_adjust")
                ]
                if adjustments:
                    # need a way to figure out which field is being rendered
                    # but for now, arbitrarily take the first one
                    adjustment = adjustments[0]
                    # convert to int
                    adjustment = int(adjustment)
                    # modify level
                    adjusted_level = level + adjustment
                    # bound between h1 and h6
                    adjusted_level = max(1, min(6, adjusted_level))
                else:
                    # no adjustment, leave level as it is
                    adjusted_level = level
                # generate the html
                if slugify:
                    attrs = ' id="{slug}"'.format(slug=slugify(text))
                else:
                    attrs = ''
                return '<h{level}{attrs}>{text}</h{level}>\n'.format(
                    level=adjusted_level,
                    attrs=attrs,
                    text=text,
                )

        config.renderer_mixins.append(AdjustHeadingsMixin)
