##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Grok utility functions.
"""
import zope.component
import zope.component.hooks
from types import ClassType
from grokcore.component import directive
from zope.interface.interfaces import IInterface

def _sort_key(component):
    # If components have a grok.order directive, sort by that.
    explicit_order, implicit_order = directive.order.bind().get(component)
    return (explicit_order,
            component.__module__,
            implicit_order,
            component.__class__.__name__)


def sort_components(components):
    """Sort a list of components using the information provided by
    `grok.order`.
    """
    return sorted(components, key=_sort_key)


def getSite():
    site = zope.component.hooks.getSite()
    if site is None:
        sm = zope.component.getGlobalSiteManager() 
    else:
        sm = site.getSiteManager()
    return sm


def provideUtility(component, provides=None, name=u''):
    sm = getSite()
    sm.registerUtility(component, provides, name, event=False) 


def provideAdapter(factory, adapts=None, provides=None, name=''):
    sm = getSite()
    sm.registerAdapter(factory, adapts, provides, name, event=False)


def provideSubscriptionAdapter(factory, adapts=None, provides=None):
    sm = getSite()
    sm.registerSubscriptionAdapter(factory, adapts, provides, event=False)


def provideHandler(factory, adapts=None):
    sm = getSite()
    sm.registerHandler(factory, adapts, event=False)

def provideInterface(id, interface, iface_type=None, info=''):
    """register Interface with global site manager as utility

    >>> gsm = zope.component.getGlobalSiteManager()

    >>> from zope.interface import Interface
    >>> from zope.interface.interfaces import IInterface
    >>> from zope.component.tests import ITestType

    >>> class I(Interface):
    ...     pass
    >>> IInterface.providedBy(I)
    True
    >>> ITestType.providedBy(I)
    False
    >>> interfaces = gsm.getUtilitiesFor(ITestType)
    >>> list(interfaces)
    []

    # provide first interface type
    >>> provideInterface('', I, ITestType)
    >>> ITestType.providedBy(I)
    True
    >>> interfaces = list(gsm.getUtilitiesFor(ITestType))
    >>> [name for (name, iface) in interfaces]
    [u'zope.component.interface.I']
    >>> [iface.__name__ for (name, iface) in interfaces]
    ['I']

    # provide second interface type
    >>> class IOtherType(IInterface):
    ...     pass
    >>> provideInterface('', I, IOtherType)

    >>> ITestType.providedBy(I)
    True
    >>> IOtherType.providedBy(I)
    True
    >>> interfaces = list(gsm.getUtilitiesFor(ITestType))
    >>> [name for (name, iface) in interfaces]
    [u'zope.component.interface.I']
    >>> interfaces = list(gsm.getUtilitiesFor(IOtherType))
    >>> [name for (name, iface) in interfaces]
    [u'zope.component.interface.I']

    >>> class I1(Interface):
    ...     pass
    >>> provideInterface('', I1)
    >>> IInterface.providedBy(I1)
    True
    >>> ITestType.providedBy(I1)
    False
    >>> interfaces = list(gsm.getUtilitiesFor(ITestType))
    >>> [name for (name, iface) in interfaces]
    [u'zope.component.interface.I']
    >>> [iface.__name__ for (name, iface) in interfaces]
    ['I']
    """
    if not id:
        id = "%s.%s" % (interface.__module__, interface.__name__)

    if not IInterface.providedBy(interface):
        if not isinstance(interface, (type, ClassType)):
            raise TypeError(id, "is not an interface or class")
        return

    if iface_type is not None:
        if not iface_type.extends(IInterface):
            raise TypeError(iface_type, "is not an interface type")
        alsoProvides(interface, iface_type)
    else:
        iface_type = IInterface

    sm = getSite() 
    sm.registerUtility(interface, iface_type, id, info)

