#! python
# -*- coding: utf-8 -*-

"""Inspect Extensions module.

Python script that uses many modules from Python to exposes
as many information that is possible to inspect packages.

Author:
    - Daniel Cosmo Pizetta
"""

__version__ = '0.1.3'

import abc
import argparse
import enum
import importlib
import inspect
import logging
import pkgutil
import sys

import termcolor

_logger = logging.getLogger(__name__)


# functions for member name --------------------------------------------------


def is_special(mbr_name):
    """Check if it is a special Python method, starts and ends with __."""
    return bool(mbr_name.startswith('__') and mbr_name.endswith('__'))


def is_private(mbr_name):
    """Check if a member name 'mbr_name' is a private."""
    return bool(mbr_name.startswith('__'))


def is_protected(mbr_name):
    """Check if a member name 'mbr_name' is a protected."""
    return bool(mbr_name.startswith('_'))


def is_public(mbr_name):
    """Check if a member name 'mbr_name' is a public."""
    return bool(not mbr_name.startswith('__') and not mbr_name.startswith('_'))


# functions for class members ------------------------------------------------


def is_type(kls):
    """Check if a class 'kls' is have a type 'type'.

    Args:
        kls (class): class

    Returns:
        bool: True if has is type type(), False otherwise.
    """
    return bool(isinstance(kls, type(object)) and not is_enum(kls))


def is_meta(kls):
    """Check if a class 'kls' is a type metaclass.

    Args:
        kls (class): class

    Returns:
        bool: True if has is type abc.ABCMeta(), False otherwise.
    """
    return bool(issubclass(kls, abc.ABCMeta))


def is_enum(kls):
    """Check if a class 'kls' is a type enum.

    Args:
        kls (class): class

    Returns:
        bool: True if has is type enum.EnumMeta(), False otherwise.
    """
    return bool(issubclass(kls, enum.Enum) or kls == enum.EnumMeta)


def get_ancestors(kls):
    """Get all ancestors recursively, this is static - depends on code.

    The key is the full class name (including package and module) and the value
    is the class itself.

    This could be used for any Python class.

    Args:
        kls (class): class to get inheritance

    Raises:
        IOError: when 'kls' is not a class

    Returns:
        dict: {'class.full.Name': Class}
    """

    if not inspect.isclass(kls):
        raise IOError("kls parameter must be a class!")

    module_name = kls.__module__
    class_name = kls.__name__
    full_class_name = module_name + "." + class_name
    class_inheritance = {}
    class_inheritance[full_class_name] = kls

    while kls.__base__ and kls.__base__ != object:
        _logger.debug("Full class name: %s", full_class_name)
        kls = kls.__base__
        module_name = kls.__module__
        class_name = kls.__name__
        full_class_name = module_name + "." + class_name
        class_inheritance[full_class_name] = kls

    return class_inheritance


def get_descendants(kls):
    """Get all descendants recursively, this is static - depends on code.

    The key is the full class name (including package and module) and the value
    is the class itself.

    This could be used for any Python class.

    Args:
        kls (class): class to get inheritance

    Raises:
        IOError: when 'kls' is not a class

    Returns:
        dict: {'class.full.Name': Class}
    """
    raise NotImplementedError


# functions for instance members ---------------------------------------------


def is_enum_value(ins):
    """Check if a instance 'ins' is a enum value.

    Args:
        ins (object): an instance

    Returns:
        bool: True if has is enum value, False otherwise.
    """
    return bool(isinstance(ins, enum.Enum))


def is_attribute(ins):
    """Check if a instance 'ins' is a attribute value.

    Args:
        ins (object): an instance

    Returns:
        bool: True if has is an attribute, False otherwise.
    """
    return bool(not is_what(ins) and not is_enum_value(ins))


def get_parents(ins):
    """Get all parents recursively, this is not static - depends on living objects.

    Of course the object must have the parent.

    Args:
        ins (object): instance to get the hierarchy

    Raises:
        AttributeError: if 'ins' (and its parents) have not the attribute parent.

    Returns:
        list: an list starting with closest relative ([parent, parent.parent ...])
    """

    ins_parents = []

    while ins.parent:
        ins = ins.parent
        ins_parents.append(ins)
        _logger.debug("Parent name: %s", ins.name)

    return ins_parents


def get_children(ins):
    """Get all children recursively, this is not static - depends on living objects.

    Of course the object must have the children.

    Args:
        ins (object): instance to get the hierarchy

    Raises:
        AttributeError: if 'ins' (and its children) have not the attribute children.

    Returns:
        list: an list starting with closest relative
    """

    ins_children = []

    while ins.children:
        ins = ins.children
        ins_children.append(ins)
        _logger.debug("Child name: %s", ins.name)

    return ins_children


MEMBER_INDENTATION = 2

EVIDENCED_CLASSES = {'TYPE': is_type, 'META': is_meta, 'ENUM': is_enum}

EVIDENCED_DATA = {
    'ENUMVALUE': is_enum_value,
    'PROPERTY': inspect.isdatadescriptor,
    'ATTRIBUTE': is_attribute
}

EVIDENCED_METHODS = {
    'FUNCTION': inspect.isfunction,
    'ITERATOR': inspect.isgeneratorfunction,
    'GENERATOR': inspect.isgenerator,
    'BUILTIN': inspect.isbuiltin
}

ENCAPSULATIONS = {
    'PRIVATE': is_private,
    'PROTECTED': is_protected,
    'PUBLIC': is_public
}

TYPES = {
    'PACKAGE': ('', 'red'),
    'MODULE': (inspect.ismodule, 'yellow'),
    'CLASS': (inspect.isclass, 'green'),
    'METHOD': (inspect.ismethod, 'blue'),
    'DATA': ('', 'white'),
    'NOTFOUND': ('', 'red')
}

STR_FORMATED = "{:.<30} {:.<30} {:.<10} {:.<10} {:.<15} {:.<15} {:.<20}"

PREFIX = 0
NAME = 1
TYPE = 2
ENCAPSULATION = 3
EVIDENCED = 4
FTYPE = 5
ISWHAT = 6
MEMBER = 7

FILTER = {TYPE: ['ALL'],
          ENCAPSULATION: ['ALL'],
          EVIDENCED: ['ALL']}


def print_member_colored(members_list):
    """Print members in colored list."""

    for member in members_list:
        str_colored = termcolor.colored(
            STR_FORMATED.format(member[PREFIX], member[NAME], member[TYPE],
                                member[ENCAPSULATION], member[EVIDENCED],
                                str(member[FTYPE]), str(member[ISWHAT])),
            TYPES[member[TYPE]][1])
        print(str_colored)


def get_encapsulation(mbr_name):
    """Get member's encapsulation level."""

    mbr_name = str(mbr_name)
    level = ''

    if mbr_name.startswith('__'):
        level = 'PRIVATE'
    elif mbr_name.startswith('_') and not mbr_name.startswith('__'):
        level = 'PROTECTED'
    else:
        level = 'PUBLIC'

    return level


def get_evidences(mbr, mbr_type):
    """Get special evidences from member."""

    mbr_evidence = []

    if mbr_type == 'CLASS':
        dict_evidences = EVIDENCED_CLASSES
    elif mbr_type == 'METHOD':
        dict_evidences = EVIDENCED_METHODS
    elif mbr_type == 'DATA':
        dict_evidences = EVIDENCED_DATA
    else:
        dict_evidences = {}

    for evidence, func_evidence in dict_evidences.items():
        if func_evidence(mbr):
            mbr_evidence.append(evidence)

    if mbr_evidence:
        return mbr_evidence[0]
    else:
        return ''


def is_what(obj):
    """List of what the member is using inspect."""
    obj_is = []
    # get a list of all functions from inspect
    for func_name, func in inspect.getmembers(inspect):
        # get functions that starts with 'is' and is a function
        if func_name.startswith('is') and inspect.isfunction(func):
            # apply the function to the object
            if func(obj):
                obj_is.append(func_name)
    return obj_is


def get_members_from_class(prefix, member):
    """Get members that are not package."""

    mbr_list = []
    mbr_type = 'NOTFOUND'
    mbr_name = 'NOTFOUND'

    for mbr_name, mbr in inspect.getmembers(member):
        is_imported = True

        try:
            if inspect.isclass(mbr):
                if mbr.__module__ == prefix:
                    is_imported = False
            else:
                is_imported = False
        except AttributeError:
            is_imported = False

        if not is_special(
                mbr_name) and not is_imported and not inspect.isbuiltin(mbr):

            if inspect.isclass(mbr):
                mbr_type = 'CLASS'
            elif inspect.ismethod(mbr) or inspect.isfunction(mbr):
                mbr_type = 'METHOD'
            else:
                mbr_type = 'DATA'

            mbr_evidences = get_evidences(mbr, mbr_type)
            mbr_encapsulation = get_encapsulation(mbr_name)

            _logger.debug("Member name: %s", mbr_name)

            list_item = (prefix, mbr_name, mbr_type, mbr_encapsulation, mbr_evidences,
                         type(mbr).__name__, is_what(mbr), mbr)

            mbr_list.append(list_item)

            if inspect.isclass(mbr):
                mbr_list += get_members_from_class(prefix + '.' + mbr_name, mbr)

    return mbr_list


def filter_members(mbr_list, filter_=FILTER):
    #  mbr_list.sort(key=lambda tup: tup[0])

    def filters(element):
        ret = True
        for key, values in filter_.items():
            if values != ['ALL']:
                if element[key] in values:
                    ret = ret and True
                else:
                    ret = ret and False
            else:
                ret = ret and True
        return ret

    return filter(filters, mbr_list)


def get_object_properties(object_):
    """Object properties dictionary.

    The key is the property name and the value is the property itself.
    This could be used for any Python object (with class derived from Object).

    Args:
        object_ (object): object itself

    Returns:
        dict: object properties dictionary, key is the property name and the value is the property value.
    """

    if not inspect.isclass(object_):
        properties = {}
        class_members = inspect.getmembers(object_)
        for member_name, member in class_members:
            if not member_name.startswith('_') and not inspect.ismethod(member):
                default_property_value = getattr(object_, member_name)
                properties[member_name] = default_property_value
                _logger.debug("Property: %s = %s", member_name,
                              default_property_value)
        return properties


def get_class_properties(class_):
    """Returns the class properties dictionary.

    This could be used for any Python class (derived from Object).

    Args:
        class_ (class): Class to get properties

    Returns:
        dict: properties dictionary, key is the property name and the
        value is the property value.
    """

    if not inspect.isclass(class_):
        class_ = class_.__class__

    properties = {}
    class_instance = class_()
    class_members = inspect.getmembers(class_)

    for member_name, member in class_members:
        if not member_name.startswith('_') and not inspect.ismethod(member):
            default_property_value = getattr(class_instance, member_name)
            properties[member_name] = default_property_value
            _logger.debug("Property: %s = %s", member_name,
                          default_property_value)

    return properties


def get_members_from_module(pkg_mod_name):
    """Get members that are package module."""

    mbr_list = []
    prefix = ''
    mbr_name = ''

    try:
        pkg_mod_start = importlib.import_module(pkg_mod_name)
        mbr_name = pkg_mod_start.__name__
    except ImportError:
        get_members_from_class(pkg_mod_name, pkg_mod_name().__class__)
    else:
        try:
            path_ = pkg_mod_start.__path__
        except AttributeError:
            mbr_type = 'MODULE'
            mbr_encapsulation = get_encapsulation(mbr_name)
            mbr_evidences = get_evidences(pkg_mod_start, mbr_type)
            mod_direct = False
            try:
                prefix, mbr_name = str.rsplit(mbr_name, '.', 1)
            except ValueError:
                prefix, mbr_name = pkg_mod_name, mbr_name
                mod_direct = True

            mbr_list.append((prefix, mbr_name, mbr_type, mbr_encapsulation,
                             mbr_evidences, type(pkg_mod_start).__name__,
                             is_what(pkg_mod_start), pkg_mod_start))

            if not mod_direct:
                mbr_list += get_members_from_class(prefix + '.' + mbr_name,
                                                   pkg_mod_start)
            else:
                mbr_list += get_members_from_class(prefix, pkg_mod_start)

        else:
            for _, mbr_name, is_pkg in pkgutil.walk_packages(
                    path=path_,
                    prefix=pkg_mod_start.__name__ + '.',
                    onerror=lambda _: None):
                try:
                    mbr = importlib.import_module(mbr_name)
                except ImportError as err:
                    _logger.exception("ImportError - We could not import: %s", mbr_name)
                except IOError as err:
                    _logger.exception("IOError - We could not import: %s", mbr_name)

                mod_direct = False
                if is_pkg:
                    mbr_type = 'PACKAGE'
                else:
                    mbr_type = 'MODULE'

                mbr_encapsulation = get_encapsulation(mbr_name)
                mbr_evidences = get_evidences(mbr, mbr_type)

                try:
                    prefix, mbr_name = str.rsplit(mbr_name, '.', 1)
                except ValueError:
                    prefix, mbr_name = '', mbr_name
                    mod_direct = True
                mbr_list.append((prefix, mbr_name, mbr_type, mbr_encapsulation,
                                 mbr_evidences, type(mbr).__name__, is_what(mbr), mbr))
                mbr_list += get_members_from_class(prefix + '.' + mbr_name, mbr)

    return mbr_list


def main():
    """Run inspect extensions."""

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('obj', help="Input object name (package, module, class). Ex.: pathlib", type=str)

    parser.add_argument('--count_members', help="Shows the number of members", action='store_true')
    parser.add_argument('--colored', help="Print colored members", action='store_true')
    parser.add_argument('--text_only', help="Print just text characters - not colorized", action='store_true')

    parser.add_argument('--filter', help="[PACKAGE, MODULE, CLASS, METHOD, DATA, ALL]")
    parser.add_argument('-p', '--packages', help="Show just packages")
    parser.add_argument('-m', '--modules', help="Show just modules")
    parser.add_argument('-c', '--classes', help="Show just classes")
    parser.add_argument('-t', '--methods', help="Show just methods, must have 'self' as first arg")
    parser.add_argument('-f', '--functions', help="Show just functions, not associated with any object")
    parser.add_argument('-d', '--data', help="Show just data, variables")
    parser.add_argument('-a', '--all_members', help="Show all members (DEFAULT)(packages, modules, classes, methods, functions, data)")

    parser.add_argument('--encapsulation', help="[NONE, PUBLIC, PROTECTED, PRIVATE, ALL]")
    parser.add_argument('-b', '--public', help="Show just public members (DEFAULT)")
    parser.add_argument('-o', '--protected', help="Show just protected members")
    parser.add_argument('-i', '--private', help="Show just private members")
    parser.add_argument('-e', '--all_encapsulation', help="Show all encapsulation")

    parser.add_argument('--special_classes', help="Print special classes, '__' before and after name", type=str)
    parser.add_argument('--special_methods', help="Print special methods, '__' before and after name", type=str)
    parser.add_argument('--special_data', help="Print special data, '__' before and after name", type=str)

    parser.add_argument('--remove_special_classes', help="Filter special classes, see special_classes", type=str)
    parser.add_argument('--remove_special_methods', help="Filter special methods, see special_methods", type=str)
    parser.add_argument('--remove_special_data', help="Filter special data, see special_data", type=str)
    parser.add_argument('--remove_special_members', help="Filter special members, see special_members", type=str)

    parser.add_argument('--version', action='version', version=f'inspect-extensions v{__version__}')

    args = parser.parse_args(sys.argv[1:])
    mbr_list = get_members_from_module(args.obj)

    termcolor.cprint(STR_FORMATED.format('PREFIX', 'NAME', 'TYPE', 'ENCAPS', 'EVINDECED', 'type()', 'inspect'),
                     'red', attrs={'bold': True})

    mbr_list_filtered = filter_members(mbr_list, {TYPE: ['DATA']})
    print_member_colored(mbr_list)


if __name__ == '__main__':
    sys.exit(main())
