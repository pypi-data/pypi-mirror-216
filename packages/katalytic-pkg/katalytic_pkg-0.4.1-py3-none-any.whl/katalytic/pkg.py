import re
import sys
import traceback
import warnings

from glob import iglob
from pathlib import Path
from importlib import import_module

# NOTE: __version__ and __version_info__ are defined below get_version()


def __get_version_from_metadata(path):
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('Version:'):
                return line.split(':')[-1].strip()


def __find_paths(pkg):
    pkg = pkg.replace('-', '_').replace('.', '_')
    for p in sys.path:
        if not Path(p).is_dir():
            continue

        for p2 in iglob(f'{p}/**.dist-info', recursive=True):
            if re.search(f'{pkg}-[^/]*[.]dist-info', p2):
                yield p2
                if Path(f'{p2}/METADATA').is_file():
                    yield p2

        for p2 in iglob(f'{p}/**.egg-info', recursive=True):
            if re.search(f'{pkg}-[^/]*[.]egg-info', p2):
                yield p2
                if Path(f'{p2}/PKG-INFO').is_file():
                    yield f'{p2}/PKG-INFO'


def get_version(dunder_name):  # pragma: no cover -- I can't test all branches at the same time
    """
    Get the version information for a package.

    Args:
        dunder_name (str):
            The dunder name of the package (i.e., __name__).

    Returns:
        tuple:
            A tuple containing the version string and the version information as a tuple of integers.
            If the version information cannot be determined, None is returned.

    """
    if sys.version_info >= (3, 8):
        from importlib import metadata
        dunder_name = dunder_name.replace('.', '-')
        dunder_name = dunder_name.replace('-__init__', '')
        version = metadata.version(dunder_name)
        version_info = tuple(map(int, version.split('.')))
        return version, version_info

    version = None
    for p in __find_paths(dunder_name):
        if p.endswith('.dist-info'):
            version = re.search(r'\w+-(\d+\.\d+\.\d+)', p)
            if version:
                version = version.group(1)
                break

        if p.endswith('.dist-info/METADATA'):
            version = __get_version_from_metadata(p)
            if version:
                break

        if p.endswith('.egg-info/PKG-INFO'):
            version = __get_version_from_metadata(p)
            if version:
                break

    if version:
        version_info = tuple(map(int, version.split('.')))
    else:
        version_info = None

    # If nothing worked, I would rather return None than raise an exception
    # This could happen if the package is installed on python < 3.8
    return version, version_info


__version__, __version_info__ = get_version(__name__)


def _get_stacktrace(e):
    return ''.join(traceback.format_exception(None, e, e.__traceback__))


def _check(name, group):
    if group.endswith('*'):
        prefix = group.split('*')[0]
        return name.startswith(prefix)
    else:
        return name == group


def get_modules():
    """
    Get a list of importable modules within the package.

    Returns:
        list:
            A list of importable modules within the package, sorted by module name.

    """
    modules = []
    for item in Path(__file__).parent.iterdir():
        if item.stem == '__pycache__':
            continue

        module_name = f'{__package__}.{item.stem}'
        try:
            module = import_module(module_name)
        except Exception as e:  # pragma: no cover
            warnings.warn(f'Couldn\'t import {module_name!r}\n' + _get_stacktrace(e))
            continue

        modules.append(module)

    # find editable installs
    for item in Path(__file__).parent.parent.iterdir():  # pragma: no cover
        # no coverage: because I would have to create an editable install,
        # just to test this functionality
        if not re.search(__package__ + r'\..*\.pth', item.name):
            continue

        try:
            module = import_module(item.stem)
        except Exception as e:  # pragma: no cover
            warnings.warn(f'Couldn\'t import {item.stem!r}\n' + _get_stacktrace(e))
            continue

        modules.append(module)

    return sorted(modules, key=lambda m: m.__name__)


def find_functions_marked_with(group):
    """
    Get a list of functions within the package that belong to a specific group.

    Args:
        group (str):
            The name of the group.

    Returns:
        list:
            A list of tuples containing the function name, the function object, and the groups it belongs to.
            The list is sorted based on the function names.

    """
    functions = []
    for module in get_modules():
        for func_name in dir(module):
            f = getattr(module, func_name)
            groups = getattr(f, '__katalytic_marks__', [])
            groups = [g for g in groups if _check(g, group)]
            if groups:
                functions.append((func_name, f, groups))

    return sorted(functions)


def mark(label):
    """
    Decorator to mark a function with one or more labels.

    Args:
        label (str):
            The label to mark the function with.

    Returns:
        callable:
            The decorator to mark a function.

    Raises:
        TypeError:
            If the provided label is not a string.
        ValueError:
            If the provided label contains newline characters, tab characters, or consists only of whitespace characters.

    """
    if not isinstance(label, str):
        raise TypeError(f'Only strings are allowed. Got {label!r}')

    if '\n' in label or '\t' in label or re.search(r'^\s*$', label):
        raise ValueError(f'Choose a meaningful label. Got {label!r}')

    def decorator(func):
        func.__katalytic_marks__ = getattr(func, '__katalytic_marks__', ())
        # prepend to maintain the intuitive order (top to bottom)
        func.__katalytic_marks__ = (label, *func.__katalytic_marks__)
        return func

    return decorator


@mark('__test_1')
@mark('__test_2')
@mark('__test_300')
def __test(): pass


@mark('__test_3::a')
@mark('__test_3::b')
@mark('__test_2')
def __test_2(): pass
