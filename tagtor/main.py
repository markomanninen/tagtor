#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: main.py

from copy import deepcopy

class TAG(object):
    """ Simple html tag generator """
    def __init__(self, *args, **kw):
        self._name = self.__class__.__name__.lower()
        self._attributes = dict([k.lower(), str(w)] for k, w in kw.iteritems())
        self._in = []
        self._left = []
        self._right = []
        map(self.__lshift__, args)
    
    def getName(self):
        return self._name
    def setName(self, name):
        self._name = name
        return self
    
    def getAttribute(self, key):
        return self._attributes[key] if self._attributes.has_key(key) else None
    def setAttribute(self, key, value):
        self._attributes[key] = value
        return self
    
    def rcontent(self, item):
        return self.__rshift__(item)
    def __rshift__(self, item):
        self._in = [item] + self._in
        return self
    
    def content(self, item):
        return self.__lshift__(item)
    def __lshift__(self, item):
        self._in.append(item)
        return self
    
    def prepend(self, item):
        return self.__radd__(item)
    def __radd__(self, item):
        self._left.append(item)
        return self
    
    def append(self, item):
        return self.__add__(item)
    def __add__(self, item):
        self._right.append(item)
        return self
    
    def renderAttributes(self):
        attr = ''
        if self._attributes:
            attr = ''.join([' %s="%s"' % (k, v) for k, v in self._attributes.iteritems()])
        return attr
    
    def _repr_html_(self):
        return self.__str__()
    def __str__(self):
        
        left = ''
        right = ''
        element = ''
        
        if self._in:
            in_elements = ''.join([str(item() if callable(item) else item) for item in self._in])
            element = '<%s%s>%s</%s>' % (self._name, self.renderAttributes(), in_elements, self._name)
        else:
            element = '<%s%s/>' % (self._name, self.renderAttributes())
        
        if self._left:
            left = ''.join(map(lambda item: str(item() if callable(item) else item), self._left))
        
        if self._right:
            right = ''.join(map(lambda item: str(item() if callable(item) else item), self._right))
        
        return left + element + right

class htmlHelper(object):
    """ Tag generation factory """
    def __getattr__(self, tag):
        """ Only create tag object, if it hasn't been created before. """
        if not self.__dict__.has_key(tag):
            self.__dict__[tag] = type(tag, (TAG,), {})
        # Don't return reference to the object, but "deeply" new object.
        return deepcopy(self.__dict__[tag])

"""
All tag elements are accessible via readily constructed factory variable. This helper
should be imported from the module in this wise: ´from tagtor import helper´
OR ´from tagtor import helper as h´ if shorter variable name is preferred
"""
helper = htmlHelper()