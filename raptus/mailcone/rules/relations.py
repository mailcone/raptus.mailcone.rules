from persistent import Persistent



class RelationContainer(Persistent):
    """ Relation holder
    """
    
    relations = list()

    def set_data(self, data):
        self.relations = list()
        for rel in data:
            t1 = rel.get('terminal1')
            t2 = rel.get('terminal2')
            self.relations.append(Relation(t1.get('object_id'), t1.get('terminal_id'),
                                           t2.get('object_id'), t2.get('terminal_id')))

    def get_data(self):
        li = list()
        for rel in self.relations:
            di = dict(terminal1=dict(object_id=rel.object1,
                                     terminal_id=rel.terminal1),
                      terminal2=dict(object_id=rel.object2,
                                     terminal_id=rel.terminal2),
                      )
            li.append(di)
        return li

    def get(self, object, name):
        """ return a generator for a given ruleitem and terminal
        """
        for rel in self.relations:
            if rel.object1 == object and rel.terminal1 == name:
                yield rel



class Relation(Persistent):
    """ a mapping between to IRuleItem and her terminal input/output
    """
    
    def __init__(self, object1, terminal1, object2, terminal2):
        self.object1 = object1
        self.terminal1 = terminal1
        self.object2 = object2
        self.terminal2 = terminal2
        self._p_changed = True
        



