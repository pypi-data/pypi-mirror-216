`jafdecs`: Just A Few Decorators
================================

Pretty useful decorators for Python functions, classes, and class methods.


Write Once, Read Many on Class Properties
=========================================

If a class property takes a long time to compute and is referenced many times, it is useful to lazily compute it once (when it is first referenced) and cache the result for later references.
This is where the `worm` submodule comes in.

::

    class SlowExample:
        @property
        def hard_property(self):
            import time
            time.sleep(5)
            print('This took a long time to compute!')
            return 5

    ex = SlowExample()
    print(ex.hard_property)
    print(ex.hard_property)


In the example above, the code will take around 10 seconds to run.
But it only needs to take 5 seconds if the property's value is cached, like in the example below.

::

    from jafdecs import worm

    @worm.onproperties
    class QuickerExample:
        @property
        def hard_property(self):
            import time
            time.sleep(5)
            print('This took a long time to compute!')
            return 5

    ex = QuickerExample()
    print(ex.hard_property)
    print(ex.hard_property)

