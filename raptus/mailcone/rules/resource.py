import grok

from zope.interface import Interface

from fanstatic import Library, Resource

from js.yui_wireit import wireit
from raptus.mailcone.layout.resource import ui_elements

library = Library('raptus.mailcone.rules', 'static')

wireit_css = Resource(
    library,
    'wireit.css',
    depends=[wireit]
)

wireit_js = Resource(
    library,
    'wireit.js',
    depends=[wireit, wireit_css, ui_elements]
)

wireit = wireit_js