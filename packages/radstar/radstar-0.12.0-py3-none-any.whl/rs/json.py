# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from base64 import a85decode, a85encode
from datetime import date, datetime, time
from decimal import Decimal
import json

# -------------------------------------------------------------------------------------------------------------------- #

def load(*args, **kw):
    return json.load(*args, object_hook=_load_objhook, **kw)

def loads(*args, **kw):
    return json.loads(*args, object_hook=_load_objhook, **kw)


def _load_objhook(obj):
    d = _decoders.get(obj.get('$t'))
    if d is not None and '$v' in obj:
        return d(obj['$v'])
    return obj

_decoders = {
    'bin':  a85decode,
    'date': date.fromisoformat,
    'dec':  Decimal,
    'dt':   datetime.fromisoformat,
    'time': time.fromisoformat,
}

# -------------------------------------------------------------------------------------------------------------------- #

def dump(*args, **kw):
    return json.dump(*args, default=_dump_default, **kw)

def dumps(*args, **kw):
    return json.dumps(*args, default=_dump_default, **kw)


def _dump_default(obj):
    e = _encoders.get(type(obj))
    if e is not None:
        return {'$t': e[0], '$v': e[1](obj)}
    return obj

_encoders = {
    bytes:      ('bin', lambda obj: a85encode(obj).decode('ascii')),
    date:       ('date', str),
    datetime:   ('dt', lambda obj: obj.isoformat()),
    Decimal:    ('dec', str),
    memoryview: ('bin', lambda obj: a85encode(obj).decode('ascii')),
    time:       ('time', str),
}

# -------------------------------------------------------------------------------------------------------------------- #

def register_type(tp, name, encoder, decoder):
    _encoders[tp] = (name, encoder)
    _decoders[name] = decoder

# -------------------------------------------------------------------------------------------------------------------- #
