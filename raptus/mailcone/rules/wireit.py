import grok

from zope import component

from raptus.mailcone.rules import _
from raptus.mailcone.rules import interfaces
from raptus.mailcone.rules import resource

from raptus.mailcone.layout.views import Page

grok.templatedir('templates')


class WireItBoard(Page):
    grok.context(interfaces.IRuleset)
    
    def update(self):
        super(WireItBoard, self).update()
        resource.wireit.need()

    @property
    def toolbox(self):
        li = list()
        li.append(dict( title = _('Inputs'),
                        items = self._rules(interfaces.IInputItemFactory),)) 
        li.append(dict( title = _('Conditions'),
                        items = self._rules(interfaces.IConditionItemFactory),))
        li.append(dict( title = _('Actions'),
                        items = self._rules(interfaces.IActionItemFactory),))
        return li
    
    def _rules(self, interface):
        gen = component.getAdapters((self.context,),interface,)
        return sorted(gen, key=lambda item:item[1].order)