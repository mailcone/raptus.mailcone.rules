import grok

from raptus.mailcone.rules import _
from raptus.mailcone.rules import interfaces


class BaseFactory(grok.Adapter):
    grok.baseclass()
    
    order = 0


class InputCondition(BaseFactory):
    grok.name('raptus.mailcone.rules.input')
    grok.implements(interfaces.IInputItemFactory)
    grok.context(interfaces.IRuleset)
    
    
    title = _('Input')
    description = _('All mails came in through the Input Element')