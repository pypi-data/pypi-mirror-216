"""Decorators facilitating a 'Write Once Read Many' paradigm of evaluation of
decorated items.
"""

import functools
from typing import Any, Type


def onproperties(cls: Type[Any] | None = None, *, prefix: str = '_'):
    """Decorator for classes to compute a property once when it is first read
    and cache the value as private member to not be recomputed again.
    
    The example below will save a member variable named `_member` to an
    instance of `SampleClass` when it is first accessed. Follow-up accesses to
    `.member` will pull from `._member` (or `{prefix}member` if the prefix is 
    explicitly defined) and will avoid re-computing the property's method.

    @worm.onproperties
    class SampleClass:
        @property
        def member(self):
            import time
            print('Sleeping...')
            time.sleep(15)
            print('This took a long time to initialize!')
            return 5
    
            
    >>> x = SampleClass()
    >>> print(x.member)
    Sleeping...
    This took a long time to initialize!
    5
    >>> print(x.member)
    5
    """

    if cls is None:
        # Called when decorator is called or arguments are passed to the decorator.
        # e.g. @worm.onproperties(prefix='__')
        #      @worm.onproperties()
        return functools.partial(onproperties, prefix=prefix)
    
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        return cls(*args, **kwargs)

    def wrapped_getter(instance: cls, member: property, private_name: str):
        if not hasattr(instance, private_name):
            value = member.fget(self=instance)
            setattr(instance, private_name, value)
        
        else:
            value = getattr(instance, private_name)

        return value

    for name, member in vars(cls).items():
        # Skip over anything that is not annotated with @property
        if not isinstance(member, property):
            continue

        if name.startswith('__') and name.endswith('__'):
            continue

        decorated_member = property(
            fget=functools.partial(wrapped_getter, member=member, private_name=f'{prefix}{name}'),
            fset=member.fset,
            fdel=member.fdel,
            doc=member.__doc__
        )

        # Overwrite the property to use the new method.
        setattr(cls, name, decorated_member)
    
    return wrapper
