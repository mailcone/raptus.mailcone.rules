from zope import interface
from zope import interface, schema

from raptus.mailcone.core.interfaces import IContainer
from raptus.mailcone.core.interfaces import IContainerLocator

from raptus.mailcone.rules import _

class IRulesetContainer(IContainer):
    """ A container for rulesets
    """


class IRulesetContainerLocator(IContainerLocator):
    """ interface for locate the customers folder.
    """


class IRuleset(interface.Interface):
    """ A ruleset
    """
    id = schema.TextLine(title=_(u'Id'), required=True)
    name = schema.TextLine(title=_(u'Name'), required=True)
    description = schema.Text(title=u'description', required=False)
