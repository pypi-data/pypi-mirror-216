from commonmark import Node
from commonmark.renderer import Renderer
from commonmark.parser import Parser
from commonmark.blocks import HtmlBlockParser
from commonmark.inline import HtmlInlineParser

class YouTubeRenderer(Renderer):
    def __init__(self):
        super().__init__()

    def render_youtube(self, node):
        youtube_link = node.literal[4:-1]  # Remove the '[yt]' and parentheses from the link
        embed_code = (
            f'<div style="padding-bottom: 56.25%; position: relative;">'
            f'<iframe width="100%" height="100%" src="{youtube_link}" frameborder="0" '
            f'allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen" '
            f'style="position: absolute; top: 0px; left: 0px; width: 100%; height: 100%;">'
            f'<small>Powered by <a href="https://embed.tube/embed-code-generator/youtube/">youtube embed video</a> generator</small>'
            f'</iframe></div>'
        )
        return embed_code

class YouTubeParser(HtmlBlockParser, HtmlInlineParser):
    def __init__(self, parser):
        super().__init__(parser)

    def try_opening_tag(self, parser, input_string, start_position):
        if input_string[start_position:].startswith('[yt]('):
            return True

    def try_closing_tag(self, parser, input_string, start_position):
        if input_string[start_position:].startswith(')'):
            return True

    def handle_tag(self, parser, input_string, tag, open_position, close_position):
        node = Node()
        node.literal = input_string[open_position:close_position + 1]
        node.tag = tag
        parser.add_child(node)
        return node

parser = Parser()
parser.block_parsers.register(YouTubeParser(parser))
parser.inline_parsers.register(YouTubeParser(parser))

renderer = YouTubeRenderer()
renderer.HTML_BLOCK_TAGS['youtube'] = renderer.render_youtube
renderer.HTML_INLINE_TAGS['youtube'] = renderer.render_youtube
