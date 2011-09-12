import grok

from zope import schema

from raptus.mailcone.rules import interfaces
from raptus.mailcone.core import bases
from raptus.mailcone.core.interfaces import IMailcone, ISearchable


class Ruleset(bases.Container):
    grok.implements(interfaces.IRuleset)
    
    id = None
    name = None
    address = None


class RulesetContainer(bases.Container):
    grok.implements(interfaces.IRulesetContainer)

@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_rulesets_container(obj, event):
    obj['rulesets'] = RulesetContainer()

class RulesetContainerLocator(bases.BaseLocator):
    splitedpath = ['rulesets']
grok.global_utility(RulesetContainerLocator, provides=interfaces.IRulesetContainerLocator)