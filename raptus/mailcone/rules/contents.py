import grok
import copy
import json
import logging

from grokcore.formlib import formlib

from zope import schema
from zope import component
from zope.formlib import form
from zope.i18n import translate
from zope.annotation.interfaces import IAnnotations

from xml.sax import saxutils
from persistent.dict import PersistentDict

from raptus.mailcone.core import utils
from raptus.mailcone.core import bases
from raptus.mailcone.core.interfaces import IMailcone
from raptus.mailcone.customers.interfaces import ICustomersContainerLocator

from raptus.mailcone.rules import _
from raptus.mailcone.rules import wireit
from raptus.mailcone.rules import interfaces
from raptus.mailcone.rules import relations




logger = logging.getLogger('raptus.mailcone.rules')
RELATIONS_ANNOTATIONS_KEY = 'raptus.mailcone.rules.relations'





def process(func):
    """ decorator to be set on every process method
    """
    def pre(self, charter):
        self.set_customer(charter.customer)
        try:
            func(self, charter)
        except Exception, e:
            self.reset_customer()
            raise e
        self.reset_customer()
    return pre



class Ruleset(bases.Container):
    grok.implements(interfaces.IRuleset)
    
    id = None
    description = None
    
    @property
    def relations(self):
        storage = IAnnotations(self)
        if not storage.has_key(RELATIONS_ANNOTATIONS_KEY):
            storage[RELATIONS_ANNOTATIONS_KEY] = relations.RelationContainer()
        return storage[RELATIONS_ANNOTATIONS_KEY]
    
    def add_object(self, obj, id):
        """ override the default method and don't build a new id
        """
        obj.id = id
        self[str(obj.id)] = obj
        return obj.id

class RulesetContainer(bases.Container):
    grok.implements(interfaces.IRulesetContainer)

@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_rulesets_container(obj, event):
    obj['rulesets'] = RulesetContainer()

class RulesetContainerLocator(bases.BaseLocator):
    splitedpath = ['rulesets']
grok.global_utility(RulesetContainerLocator, provides=interfaces.IRulesetContainerLocator)



class BaseRuleItem(grok.Model):
    grok.baseclass()
    grok.implements(interfaces.IRuleItem)
    
    position = PersistentDict()
    overrides = PersistentDict()
    identifer = PersistentDict()
    
    _v_customer = None
    
    def __getattribute__(self, attr):
        """ proxy to get the overrides of a customer. to set the
            right customer use the decorator process.
        """
        g = grok.Model.__getattribute__
        customer = g(self, '_v_customer')
        if customer is None:
            return g(self, attr)
        if g(self, 'overrides').get(attr, False):
            rule = utils.parent(self).id
            return customer.get_ruleset_data(rule).get(attr, None)
        return g(self, attr)
    
    def set_customer(self, customer):
        self._v_customer = customer
    
    def reset_customer(self):
        self._v_customer = None
    
    @property
    def properties_prefix(self):
        return wireit.RuleBoxEditForm.prefix
    
    @property
    def override_prefix(self):
        return wireit.RuleBoxEditForm.override_prefix
    
    def apply_data(self, data, factory):
        self._apply_properties(data, factory)
        self._apply_overrides(data, factory)

    def _apply_properties(self, data, factory):
        request = utils.getRequest()
        fake = copy.copy(request)
        fake.form = data
        widgets = form.setUpWidgets(factory.form_fields, form_prefix=self.properties_prefix,
                                    request=fake, context=self)
        results = dict()
        form.getWidgetsData(widgets, self.properties_prefix, results)
        formlib.apply_data_event(self, factory.form_fields, results,
                                 adapters=None, update=False)
    
    def _apply_overrides(self, data, factory):
        di = dict()
        for name, value in data.iteritems():
            if name.startswith('%s.'%self.override_prefix):
                name = name[len('%s.'%self.override_prefix):]
                di[name] = value
        self.overrides = PersistentDict(di)

    def json_data(self, factory):
        """ prepare json: return object as dict ready to parse
        """
        di = dict()
        di.update(self._json_properties(factory))
        di.update(self._json_overrides(factory))
        results = dict(factory.metadata())
        results.update(id=self.id,
                         properties=di,
                         position=self._position())
        return results
            
    def _json_properties(self, factory):
        request = utils.getRequest()
        widgets = form.setUpEditWidgets(factory.form_fields, form_prefix=self.properties_prefix,
                                        request=request, context=self)
        properties = dict()
        for widget in widgets:
            properties.update({widget.name:widget._getCurrentValue()})
        return properties

    def _json_overrides(self, factory):
        di = dict()
        for k, v in self.overrides.iteritems():
            di['%s.%s' % (self.override_prefix, k,)] = v
        return di

    def _position(self):
        """ need make a int instead of a float to parse it with json
        """
        pos = dict()
        for name, value in self.position.iteritems():
            pos[name] = int(value)
        return pos

    def _relations(self, name):
        container = utils.parent(self)
        return container.relations.get(self, name)

    def translate(self, msg):
        txt = translate(msg, context=utils.getRequest())
        return saxutils.escape(txt)


class BaseInputItem(BaseRuleItem):
    grok.baseclass()
    grok.implements(interfaces.IInputItem)



class BaseConditionItem(BaseRuleItem):
    grok.baseclass()
    grok.implements(interfaces.IConditionItem)

    title = u''
    description = u''

    def check(self, mail):
        NotImplementedError('you need to override check method in your subclass!')
    
    def test(self, mail, factory):
        try:
            mapping = dict(factory=factory.title, title=self.title)
            if self.check(mail):
                return self.translate(_("Rule for <${factory}@${title}> match", mapping=mapping))
            else:
                return self.translate(_("Rule for <${factory}@${title}> dosen't match", mapping=mapping))
        except Exception, e:
            return str(e)
            
    @process
    def process(self, charter):
        
        match = list()
        notmatch = list()
        
        for mail in charter.mails:
            if self.check(mail):
                match.append(mail)
            else:
                notmatch.append(mail)
            
        for rel in self._relations('match'):
            copy = charter.copy(match)
            rel.peer(self).process(copy)
        for rel in self._relations('not_match'):
            copy = charter.copy(notmatch)
            rel.peer(self).process(copy)



class BaseActionItem(BaseRuleItem):
    grok.baseclass()
    grok.implements(interfaces.IActionItem)

    title = u''
    description = u''
    


class InputItem(BaseInputItem):
    grok.implements(interfaces.IInputItem)
    title = 'Input'

    def process(self, charter):
        for rel in self._relations('mailoutput'):
            copy = charter.copy()
            rel.peer(self).process(copy)



class InputCustomerItem(BaseInputItem):
    grok.implements(interfaces.IInputItem)
    title = 'Customer Input'
    
    def process(self, charter):
        for rel in self._relations('mailoutput'):
            for customer in component.getUtility(ICustomersContainerLocator)().objects():
                copy = charter.copy()
                copy.customer = customer
                rel.peer(self).process(copy)






