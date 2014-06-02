from Products.validation import validation
from Products.validation.interfaces.IValidator import IValidator
from zope.interface import classImplements
from Products.FacultyStaffDirectory import FSDMessageFactory as _

class SequenceValidator(object):
    """A wrapper that runs a validator on each item of a sequence-like Field.
    
    For example, if you have a Lines field that should contain one URL per line,
    `SequenceValidator` can apply the `isURL` validator individually to each
    line:
        Person_schema['websites'].validators = 
                   SequenceValidator('isURLs', validation.validatorFor('isURL'))
    """
    
    def __init__(self, name, validator, description='', **kw):
        """Constructor
        
        validator - a validator (or ValidatorChain) to run against each item in
        the sequence. For reasonable results, make sure your chain cites the bad
        input in its error message. Otherwise, the user won't know what the
        error message applies to.
        """
        self.name = name
        self.title = kw.get('title', name)
        self.description = description
        self.validator = validator
    
    def __call__(self, values, *args, **kwargs):
        errors = [self.validator(v) for v in values]
        errors = [x for x in errors if x not in (True, 1)]  # Filter out non-errors.
        if errors:
            return '\n\n'.join(errors)
        else:
            # Not sure why this needs to be True, but returning 1 (like
            # RegexValidator) throws an Unsubscriptable Object exception. [Ed:
            # It's because that's what the IValidator interface proclaims. The
            # stock validators are just nonconformant.]
            return True

classImplements(SequenceValidator, IValidator)

# Change some error messages to improve grammar
validation.validatorFor('isURL').errmsg = _(u'is not a valid URL.'),

