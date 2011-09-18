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


class IRuleItem(interface.Interface):
    """ Base interface
    """


class IConditionItem(IRuleItem):
    """ check if a mail match and pass to next condition or action.
    """


class IActionItem(IRuleItem):
    """ end node of the flowchart and done some action.
    """


class IRuleItemFactory(interface.Interface):
    """ Base interface
    """
    
    order = interface.Attribute("int: order of the rule item")
    title = interface.Attribute("title of factory")
    description = interface.Attribute("factory description")


    
class IInputItemFactory(IRuleItemFactory):
    """ special adapter to build the first node element in flowchart
    """


class IConditionItemFactory(IRuleItemFactory):
    """ adapter to build a IConditionItem
    """


class IActionItemFactory(IRuleItemFactory):
    """ adapter to build a IActionItem
    """

