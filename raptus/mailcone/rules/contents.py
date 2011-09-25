import grok
import copy
import json

from grokcore.formlib import formlib

from zope import schema
from zope.formlib import form
from zope.annotation.interfaces import IAnnotations

from persistent.dict import PersistentDict


from raptus.mailcone.rules import wireit
from raptus.mailcone.rules import interfaces
from raptus.mailcone.rules import relations

from raptus.mailcone.core import utils
from raptus.mailcone.core import bases
from raptus.mailcone.core.interfaces import IMailcone, ISearchable


RELATIONS_ANNOTATIONS_KEY = 'raptus.mailcone.rules.relations'

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
        return self.overrides

    def _position(self):
        """ need make a int instead of a float to parse it with json
        """
        pos = dict()
        for name, value in self.position.iteritems():
            pos[name] = int(value)
        return pos


class BaseInputItem(BaseRuleItem):
    grok.baseclass()
    grok.implements(interfaces.IInputItem)


class BaseConditionItem(BaseRuleItem):
    grok.baseclass()
    grok.implements(interfaces.IConditionItem)

    title = u''
    description = u''


class BaseActionItem(BaseRuleItem):
    grok.baseclass()
    grok.implements(interfaces.IActionItem)

    title = u''
    description = u''


class InputItem(BaseInputItem):
    grok.implements(interfaces.IInputItem)


class InputCustomerItem(BaseInputItem):
    grok.implements(interfaces.IInputItem)
    
    