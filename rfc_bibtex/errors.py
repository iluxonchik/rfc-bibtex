class UpdatedEntity(object):
    """
    Data object encopsuling the information regarding updated drafts.
    """
    @property
    def old_id(self):
        return self._old_id
        
    @property
    def new_id(self):
        return self._new_id
    
    def __init__(self, old_id, new_id):
        self._old_id = old_id
        self._new_id = new_id

class Errors(object):
    """
    Class encapsulating the errors to be reported at the end of the program's execution.
    """
    @property
    def updated_entity(self):
        """Iterator over all of the updated entity errors"""
        return iter(self._updated_entity_errors)

    @property
    def draft_updated_to_rfc(self):
        """Entity errors subset in which drafts were updated to RFCs"""
        return filter(lambda x: x.new_id.startswith('rfc'), self.updated_entity)
    
    @property
    def draft_updated_to_draft(self):
        """Entity errors subset in which drafts were updated to a new draft"""
        return filter(lambda x: x.new_id.startswith('draft'), self.updated_entity)


    def __init__(self):
        self._updated_entity_errors = []

    def add_updated_entity(self, old_id, new_id):
        self._updated_entity_errors.append(UpdatedEntity(old_id, new_id))
