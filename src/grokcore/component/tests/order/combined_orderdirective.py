"""

If the grok.order directive is specified with other classes that don't
have the order specified, then the order will be determined by first
sorting on the order specified, and then by the definition order.

  >>> components = [First(), Second(), Third, Fourth(), Fifth(), six]

  >>> from grokcore.component import sort_components
  >>> sort_components(components)
  [<class '...Third'>,
   <...Fourth object at ...>,
   <...Second object at ...>,
   <...Fifth object at ...>,
   <function six at ...>,
   <...First object at ...>]

"""

import grokcore.component as grok

class First(object):
    grok.order(5)

class Second(object):
    grok.order(1)

class Third(object):
    grok.order()

class Fourth(object):
    grok.order()

class Fifth(object):
    grok.order(1)

@grok.order(2)
def six():
    pass
