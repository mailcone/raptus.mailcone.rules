from zope.interface import implements

from raptus.mailcone.rules import interfaces






class BaseRuleProcessingEvent(object):

    def __init__(self, charter):
        self.charter = charter



class BaseRulesetProcessingEvent(BaseRuleProcessingEvent):

    def __init__(self, charter, ruleset):
        super(BaseRulesetProcessingEvent, self).__init__(charter)
        self.ruleset = ruleset



class BeginRuleProcessingEvent(BaseRuleProcessingEvent):
    implements(interfaces.IBeginRuleProcessingEvent)



class EndRuleProcessingEvent(BaseRuleProcessingEvent):
    implements(interfaces.IEndRuleProcessingEvent)



class RuleProcessingErrorEvent(BaseRuleProcessingEvent):
    implements(interfaces.IRuleProcessingErrorEvent)
    
    def __init__(self, exception, charter):
        super(RuleProcessingErrorEvent, self).__init__(charter)
        self.exception = exception



class BeginProcessingRulesetEvent(BaseRulesetProcessingEvent):
    implements(interfaces.IBeginRulesetProcessingEvent)



class EndProcessingRulesetEvent(BaseRulesetProcessingEvent):
    implements(interfaces.IEndRulesetProcessingEvent)



class RulesetProcessingErrorEvent(BaseRulesetProcessingEvent):
    implements(interfaces.IRulesetProcessingErrorEvent)

    def __init__(self, exception, charter, ruleset):
        super(RulesetProcessingErrorEvent, self).__init__(charter, ruleset)
        self.exception = exception





