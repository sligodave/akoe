
from htmlentitydefs import name2codepoint

from lxml.html import document_fromstring, CheckboxValues,\
                                            MultipleSelectOptions


def decode_entity(entity):
    if entity.startswith('&'):
        entity = entity[1:]
    if entity.endswith(';'):
        entity = entity[:-1]

    if entity.startswith('#x'):
        entity = unichr(int(entity[2:], 16))
    elif entity.startswith('#'):
        entity = unichr(int(entity[1:]))
    elif entity in name2codepoint:
        entity = name2codepoint[entity]
    return entity


def get_form_data(html, form_name=None, form_id=None):
    """
    Return a dictionary of all fields of a form.
    Either the first form or an identified form.
    You can identify a form by it's name or id or both.
    """
    data = {}
    doc = document_fromstring(html)
    if not form_name == None or not form_name == None:
        for form in doc.forms:
            if form_id == None and form.attrib.get('name') == form_name or\
                    form_name == None and form.attrib.get('id') == form_id or\
                    form.attrib.get('id') == form_id and\
                    form.attrib.get('name') == form_name:
                data = dict(form.fields)
    elif doc.forms:
        data = dict(doc.forms[0].fields)
    # Default empty values to an empty string rather than None
    # Convert field objects to lists where necessary
    # If we don't do these changes, simply submitting the form will fail.
    for n, v in data.items():
        if v == None:
            data[n] = ''
        elif isinstance(v, (CheckboxValues, MultipleSelectOptions)):
            data[n] = list(v)
    return data
