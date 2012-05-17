# -*- coding: utf-8 -*-
import re
from django.conf import settings
from django.db.models import Q


def _no_diacritics_regexp(query):
    """ returns a regexp for searching for a query without diacritics

    should be locale-aware """
    names = {
        u'a':u'aąĄ', u'c':u'cćĆ', u'e':u'eęĘ', u'l': u'lłŁ', u'n':u'nńŃ', u'o':u'oóÓ', u's':u'sśŚ', u'z':u'zźżŹŻ',
        u'ą':u'ąĄ', u'ć':u'ćĆ', u'ę':u'ęĘ', u'ł': u'łŁ', u'ń':u'ńŃ', u'ó':u'óÓ', u'ś':u'śŚ', u'ź':u'źŹ', u'ż':u'żŻ'
        }
    def repl(m):
        l = m.group()
        return u"(%s)" % '|'.join(names[l])
    return re.sub(u'[%s]' % (u''.join(names.keys())), repl, query)

def unicode_re_escape(query):
    """ Unicode-friendly version of re.escape """
    return re.sub('(?u)(\W)', r'\\\1', query)

def word_starts_with(name, prefix):
    """returns a Q object getting models having `name` contain a word
    starting with `prefix`

    We define word characters as alphanumeric and underscore, like in JS.

    Works for MySQL, PostgreSQL, Oracle.
    For SQLite, _sqlite* version is substituted for this.
    """
    kwargs = {}

    prefix = _no_diacritics_regexp(unicode_re_escape(prefix))
    # can't use [[:<:]] (word start),
    # but we want both `xy` and `(xy` to catch `(xyz)`
    kwargs['%s__iregex' % name] = u"(^|[^[:alnum:]_])%s" % prefix

    return Q(**kwargs)


def _word_starts_with_regexp(prefix):
    prefix = _no_diacritics_regexp(unicode_re_escape(prefix))
    return ur"(^|(?<=[^\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]))%s" % prefix


def _sqlite_word_starts_with(name, prefix):
    """ version of _word_starts_with for SQLite

    SQLite in Django uses Python re module
    """
    kwargs = {}
    kwargs['%s__iregex' % name] = _word_starts_with_regexp(prefix)
    return Q(**kwargs)


if hasattr(settings, 'DATABASES'):
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        word_starts_with = _sqlite_word_starts_with
elif settings.DATABASE_ENGINE == 'sqlite3':
    word_starts_with = _sqlite_word_starts_with
