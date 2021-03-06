from zope import schema
from zope import interface
from zope import component

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
    description = schema.Text(title=u'Description', required=False)
    relations = interface.Attribute('RelationContainer with all relation between Ruleitem')



class IRuleItem(interface.Interface):
    """ Base interface
    """
    title = interface.Attribute('a static title of this item')
    position = interface.Attribute('per. dict where the position are stored (required for js)')
    overrides = interface.Attribute('per. dict attribute:boolean store all attributes where can be override by a customer')
    indentifer = interface.Attribute('per. dict store the used factory for this element')
    
    def test(self, email, factory):
        """ test if this rule match
            and return a string with matching information for display
        """
        
    def process(self, charter):
        """ process this rule and call the next process on a rule
        """


class IInputItem(IRuleItem):
    """ first node element in flowchart
    """



class IConditionItem(IRuleItem):
    """ check if a mail match and pass to next condition or action.
    """
    
    title = schema.TextLine(title=_('Title'), required=True, description=_('title of the condition rule'),)
    description = schema.Text(title=u'Description', required=False, description=_('description of the condition rule'),)



class IActionItem(IRuleItem):
    """ end node of the flowchart and done some action.
    """
    
    title = schema.TextLine(title=_(u'Title'), required=True, description=_('title of the action item'),)
    description = schema.Text(title=u'Description', required=False, description=_('description of the action item'),)



class IRuleItemFactory(interface.Interface):
    """ Base interface
    """
    
    order = interface.Attribute('int: order of the rule item')
    form_fields = interface.Attribute('interface for properties form')
    title = interface.Attribute('title of factory')
    description = interface.Attribute('factory description')
    metadata_json = interface.Attribute('return a json string with all required data for js')
    
    def metadata(self):
        """ return a dict with all information over the instance for js.
        """
    
    def override_properties(self):
        """ return all fields that can be overrided by a customer
        """

    def create(self):
        """ create and return a new RuleItem
        """



class IInputItemFactory(IRuleItemFactory):
    """ special adapter to build the first node element in flowchart
    """



class IConditionItemFactory(IRuleItemFactory):
    """ adapter to build a IConditionItem
    """



class IActionItemFactory(IRuleItemFactory):
    """ adapter to build a IActionItem
    """



class IBaseRuleProcessingEvent(interface.Interface):
    charter = interface.Attribute('charter object where hold all emails')



class IBaseRulesetProcessingEvent(IBaseRuleProcessingEvent):
    ruleset = interface.Attribute('ruleset object where is processing')



class IBeginRuleProcessingEvent(IBaseRuleProcessingEvent):
    """ send begin event before rules are processed
    """



class IEndRuleProcessingEvent(IBaseRuleProcessingEvent):
    """ send end event after processing rules
    """



class IRuleProcessingErrorEvent(IBaseRuleProcessingEvent):
    """ send error event while rules processing need to be aborted
    """
    exception = interface.Attribute('causer exception')



class IBeginRulesetProcessingEvent(IBaseRulesetProcessingEvent):
    """ send begin event before a ruleset are processed
    """



class IEndRulesetProcessingEvent(IBaseRulesetProcessingEvent):
    """ send end event after a ruleset are processed
    """



class IRulesetProcessingErrorEvent(IBaseRulesetProcessingEvent):
    """ send error event while a ruleset is aborted
    """
    exception = interface.Attribute('causer exception')





