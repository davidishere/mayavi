"""This module generates the tvtk (Traited VTK) wrapper classes for
VTK classes.

"""
# Author: Prabhu Ramachandran
# Copyright (c) 2004-2015, Enthought, Inc.
# License: BSD Style.

from __future__ import print_function

import sys
import vtk
import types
import textwrap
import keyword
import copy
from collections import Sequence
from itertools import chain

# Local imports (these are relative imports because the package is not
# installed when these modules are imported).
from .common import get_tvtk_name, camel2enthought, is_version_58

from . import vtk_parser
from . import indenter
from . import special_gen

PY_VER = sys.version_info[0]


def get_trait_type(value):
    """ Return the appropriate trait type for the given `value`

    If a sequence is given, traits.Array is returned instead of
    traits.Tuple or traits.List

    Parameter
    ---------
    value

    Returns
    -------
    str

    Example
    -------
    >>> get_trait_type([100., 200.])
    'traits.Array'
    >>> get_trait_type(100)
    'traits.Int'
    >>> get_trait_type(long(100))  # Python 2
    'traits.Long'
    >>> get_trait_type(u'something')
    'traits.Unicode'
    """

    type_ = type(value)

    number_map = {int: 'traits.Int',
                  float: 'traits.Float'}

    # In Python 2 there is long type
    if PY_VER < 3:
        number_map[long] = 'traits.Long'

    if type_ in number_map:
        return number_map[type_]

    elif type_ is str:
        return 'traits.String'

    elif PY_VER < 3 and type_ is unicode:
        return 'traits.Unicode'

    elif type_ in (tuple, list):
        return 'traits.Array'

    elif type_ is bool:
        return 'traits.Bool'

    else:
        raise TypeError("Could not understand type: {}".format(type_))


def get_array_meta(value):
    if not isinstance(value, Sequence):
        return ""
    else:
        shape = (len(value),)
        dtypes = set(type(element) for element in value)
        dtype = dtypes.pop().__name__ if len(dtypes) == 1 else None
        cols = len(value)
        return ('shape={shape}, dtype={dtype}, '
                'value={value!r}, cols={cols}, ').format(shape=shape,
                                                         dtype=dtype,
                                                         value=value,
                                                         cols=cols)


def patch_default(vtk_set_meth, default):
    """Patch the initial default value for an attribute of
    a VTK class that does not initialise it properly.

    Parameters
    ----------
    vtk_set_meth : Method for setting the position attribute

    default : initial default value

    Returns
    -------

    Examples
    --------
    >>> import vtk
    >>> vtk.vtkVersion.GetVTKVersion()
    '6.3.0'
    >>> obj = vtk.vtkXOpenGLRenderWindow()
    >>> obj.GetPosition()
    '_000000000351c458_p_void'

    >>> patch_default(vtk.vtkXOpenGLRenderWindow.SetPosition,
                      '_000000000351c458_p_void')
    (0, 0)
    """
    # We will attempt to guess the default by looking into the
    # arguments of the Set method
    # SetPosition(int, int) has a signature of ("int", "int")
    # SetPosition(int position[2]) has a signature of (["int", "int"],)
    # Some method even has a signature of (["int", "int"], "vtkInformation")
    arg_formats = []
    for sig in vtk_parser.VTKMethodParser.get_method_signature(vtk_set_meth):
        if sig[1] is None:
            continue
        if any(isinstance(arg_format, list) for arg_format in sig[1]):
            arg_formats.append(tuple(chain.from_iterable(sig[1])))
        else:
            arg_formats.append(sig[1])

    for arg_format in arg_formats:
        if all(type_ == "int" for type_ in arg_format):
            if len(arg_format) == 1:
                return 0
            else:
                return (0,)*len(arg_format)
        if all(type_ == "float" for type_ in arg_format):
            if len(arg_format) == 1:
                return 0.
            else:
                return (0.,)*len(arg_format)
        if all(type_ == "string" for type_ in arg_format):
            if len(arg_format) == 1:
                return "None"
            else:
                return ("None",)*len(arg_format)
    else:
        return default


######################################################################
# `WrapperGenerator` class.
######################################################################

class WrapperGenerator:
    """Generates the wrapper code for all the TVTK classes.

    """
    def __init__(self):
        self.indent = indenter.Indent()
        self.parser = vtk_parser.VTKMethodParser()
        self.special = special_gen.SpecialGenerator(self.indent)
        self.dm = indenter.VTKDocMassager()

    #################################################################
    # `WrapperGenerator` interface.
    #################################################################

    def get_tree(self):
        """Returns the parser's class tree."""
        return self.parser.get_tree()

    def generate_code(self, node, out):
        """Generates the code for the given node in the parse tree
        along with an opened file-like object.

        Parameters
        ----------

        - node

          A node in the ClassTree.

        - out :  file-like object.

          Must support a `write` method.  Code is written to it.

        """
        self.indent.reset()

        self._write_prelims(node, out)

        # Write the class decl and __init__
        self._gen_class_init(node, out)

        # Write the other methods.
        self._gen_methods(node, out)

        # Write any special code if available.
        self.special.generate_code(node, out)

        out.write('\n')

    #################################################################
    # Non-public interface.
    #################################################################

    def _write_prelims(self, node, out):
        """Write preliminary information given the node in the class
        tree, `node`, and output file-like object, `out`.

        """
        prelim = """
        # Automatically generated code: EDIT AT YOUR OWN RISK
        from traits import api as traits
        from traitsui.item import Item, spring
        from traitsui.group import HGroup
        from traitsui.view import View

        from tvtk import vtk_module as vtk
        from tvtk import tvtk_base
        from tvtk.tvtk_base_handler import TVTKBaseHandler
        from tvtk import messenger
        from tvtk.tvtk_base import deref_vtk
        from tvtk import array_handler
        from tvtk.array_handler import deref_array
        from tvtk.tvtk_classes.tvtk_helper import wrap_vtk


        def InstanceEditor(*args, **kw):
            from traitsui.editors.api import InstanceEditor as Editor
            return Editor(view_name="handler.view")

        try:
            long
        except NameError:
            # Silly workaround for Python3.
            long = int

        """
        out.write(self.indent.format(prelim))

    def _gen_class_init(self, node, out):
        indent = self.indent
        klass = self.get_tree().get_class(node.name)
        vtk_class_name = klass.__name__
        class_name = self._get_class_name(klass)

        if node.level == 0 or node.name == 'vtkObjectBase':
            base_name = 'tvtk_base.TVTKBase'
        else:
            base_name = self._get_class_name(klass.__bases__)[0]
            if base_name != 'object':
                # Import the base class.
                base_fname = camel2enthought(base_name)
                _imp = "from tvtk.tvtk_classes.%(base_fname)s import %(base_name)s"%locals()
                out.write(indent.format(_imp))
                out.write('\n\n')

        # Write the class declaration.
        cdef = """
        class %(class_name)s(%(base_name)s):
        """%locals()
        out.write(indent.format(cdef))

        self.dm.write_class_doc(klass.__doc__, out, indent)
        indent.incr()

        # Write __init__
        decl = """
        def __init__(self, obj=None, update=True, **traits):
            tvtk_base.TVTKBase.__init__(self, vtk.%(vtk_class_name)s, obj, update, **traits)

        """%locals()
        out.write(indent.format(decl))

        if 'vtk3DWidget' in [x.name for x in node.get_ancestors()]:
            # In this case we also update the traits on the
            # EndInteractionEvent.  Note that we don't need to change
            decl = '''
            def setup_observers(self):
                """Setup the observers for the object."""
                super(%(class_name)s, self).setup_observers()
                tvtk_base._object_cache.setup_observers(self._vtk_obj,
                                              'EndInteractionEvent',
                                              self.update_traits)
            '''%locals()
            out.write(indent.format(decl))

    def _gen_methods(self, node, out):
        klass = self.get_tree().get_class(node.name)
        self.parser.parse(klass)

        if klass.__name__ == 'vtkCamera':
            # 'vtkCamera.Roll' has conflicting signatures --
            # Get/SetRoll() plus an additional Roll() method.  So we
            # wrap all of them as methods and not as traits.
            p = self.parser
            p.get_set_meths.pop('Roll')
            p.other_meths.extend(['GetRoll', 'SetRoll'])

        # ----------------------------------------
        # Generate the code.

        # The return values are editable traits.
        toggle = self._gen_toggle_methods(klass, out)
        state = self._gen_state_methods(klass, out)

        # The first return value contains updateable traits
        # the second return value contains dubious traits that
        # are initialised by VTK on init
        get_set, allow_update_failure = self._gen_get_set_methods(klass, out)

        # These do not produce editable traits.
        self._gen_get_methods(klass, out)
        self._gen_other_methods(klass, out)

        # ----------------------------------------
        # Now write out the _updateable_traits_ and View related code.

        # Store the data in the node after updating from parents.
        # Note that this data is generated and stored at run
        # time. This is the reason why the wrapper code for the
        # classes are generated in the reverse order of their depth in
        # the inheritance tree.
        data = {'toggle':toggle, 'state':state, 'get_set':get_set,
                'allow_update_failure': allow_update_failure}
        if node.level != 0 and node.parents[0].name != 'object':
            pd = node.parents[0].data
            for i in data.keys():
                data[i].update(pd[i])
        node.data = data

        # ----------------------------------------
        # Write out the updateable traits, this is used by
        # the `update_traits` method.
        ut = {}
        for i in (data['toggle'], data['state'], data['get_set']):
            ut.update(i)
        junk = textwrap.fill(repr(tuple(ut.items())))
        code = "\n_updateable_traits_ = \\" + "\n%s\n\n"%junk
        out.write(self.indent.format(code))

        # ----------------------------------------
        # Write out the allow_update_failure traits, this is used by
        # the `update_traits` method.
        junk = textwrap.fill(repr(tuple(data['allow_update_failure'])))
        code = "\n_allow_update_failure_ = \\" + "\n%s\n\n"%junk
        out.write(self.indent.format(code))

        # ----------------------------------------
        # Write out the full_traits_view and the more compact
        # traits_view

        # First copy the data over (we're going to edit it and don't
        # want the node's version to be changed).
        d = copy.deepcopy(data)

        # Add support for property trait delegation.
        #Commented out because of problems.
        #self._generate_delegates(node, d, out)

        toggle, state, get_set = d['toggle'], d['state'], d['get_set']

        # Remove unwanted stuff.
        def _safe_remove(d, keys):
            for key in keys:
                try:
                    del d[key]
                except KeyError:
                    pass

        # No point having these in the GUI.
        _safe_remove(get_set, ['reference_count', 'progress'])

        class_name = get_tvtk_name(node.name)
        title = 'Edit %s properties'%class_name

        # Write the full_traits_view.
        # The full traits view displays all of the relevant traits in a table
        # editor. For this, we first write out the _full_traitnames_list: this
        # is used by the TVTKBaseHandler to build a TableEditor for all of
        # the (relevant) traits in the tvtk object.
        t_g = sorted(toggle.keys())
        s_g = sorted(state.keys())
        gs_g = sorted(get_set.keys())

        junk = textwrap.fill("(%s)" % (t_g + s_g + gs_g))
        code = "\n_full_traitnames_list_ = \\" + "\n%s\n\n"%junk
        out.write(self.indent.format(code))

        # Start the trait_view() method.
        code = "\ndef trait_view(self, name=None, view_element=None):"
        out.write(self.indent.format(code))
        self.indent.incr()
        code = "\nif view_element is not None or name not in (None, '', 'traits_view', 'full_traits_view', 'view'):"
        out.write(self.indent.format(code))
        self.indent.incr()
        code = "\nreturn super(%s, self).trait_view(name, view_element)" % class_name
        out.write(self.indent.format(code))
        self.indent.decr()

        # Now write the full traits view.
        code = "\nif name == 'full_traits_view':"
        out.write(self.indent.format(code))
        self.indent.incr()
        item_contents = (
              'Item("handler._full_traits_list",show_label=False)')
        junk = 'View((%s),'% item_contents
        code = "\nfull_traits_view = \\" + \
               "\n%s\ntitle=\'%s\', scrollable=True, resizable=True,"\
               "\nhandler=TVTKBaseHandler,"\
               "\nbuttons=['OK', 'Cancel'])"\
               "\nreturn full_traits_view"%(junk, title)
        out.write(self.indent.format(code))
        self.indent.decr()

        # Next, we write a compact traits_view (which we call 'view'), which
        # removes some generally unused items.
        code = "\nelif name == 'view':"
        out.write(self.indent.format(code))
        self.indent.incr()
        _safe_remove(get_set, ['progress_text'])
        _safe_remove(toggle, ['abort_execute', 'release_data_flag',
                              'dragable', 'pickable',
                              'debug', 'global_warning_display'])
        t_g = sorted(toggle.keys())
        s_g = sorted(state.keys())
        gs_g = sorted(get_set.keys())
        junk = textwrap.fill('View((%s, %s, %s),'%(t_g, s_g, gs_g))
        code = "\nview = \\" + \
               "\n%s\ntitle=\'%s\', scrollable=True, resizable=True,"\
               "\nhandler=TVTKBaseHandler,"\
               "\nbuttons=['OK', 'Cancel'])"\
               "\nreturn view"%(junk, title)
        out.write(self.indent.format(code))
        self.indent.decr()

        # Finally, we write the default traits_view which includes a field
        # for specifying the view type (basic or advanced) and the
        # corresponding view (basic->view and advanced->full_traits_view)
        code = "\nelif name in (None, 'traits_view'):"
        out.write(self.indent.format(code))
        self.indent.incr()
        viewtype_contents = (
            'HGroup(spring, "handler.view_type", ' +\
                             'show_border=True)')
        view_contents = (
            '\nItem("handler.info.object", ' +\
            'editor = InstanceEditor(view_name="handler.view"), ' +\
            'style = "custom", show_label=False)')
        junk = 'View((%s, %s),'% (viewtype_contents, view_contents)
        code = "\ntraits_view = \\" + \
               "\n%s\ntitle=\'%s\', scrollable=True, resizable=True,"\
               "\nhandler=TVTKBaseHandler,"\
               "\nbuttons=['OK', 'Cancel'])"\
               "\nreturn traits_view\n\n"%(junk, title)
        out.write(self.indent.format(code))
        self.indent.decr()

        self.indent.decr()

    def _generate_delegates(self, node, n_data, out):
        """This method generates delegates for specific classes.  It
        modifies the n_data dictionary."""
        prop_name = {'vtkActor': 'vtkProperty',
                     'vtkActor2D': 'vtkProperty2D',
                     'vtkVolume': 'vtkVolumeProperty'}
        if node.name in prop_name:
            prop_node = self.get_tree().get_node(prop_name[node.name])
            prop_data = prop_node.data
            # Update the data of the node so the view includes the
            # property traits.
            code = ''
            for key in n_data:
                props = prop_data[key]
                n_data[key].update(props)
                # Write the delegates.
                for p in props:
                    code += '%s = tvtk_base.vtk_property_delegate\n'%p
            code += '\n'
            out.write(self.indent.format(code))

    def _gen_toggle_methods(self, klass, out):
        meths = self.parser.get_toggle_methods()
        updateable_traits = {}
        for m in meths:
            name = self._reform_name(m)
            updateable_traits[name] = 'Get' + m
            t_def = 'tvtk_base.false_bool_trait'
            if meths[m]:
                t_def = 'tvtk_base.true_bool_trait'
            try:
                vtk_set_meth = getattr(klass, 'Set' + m)
            except AttributeError:
                # Broken VTK API (4.2) where sometimes GetProp and
                # PropOn/Off exist but no SetProp method is available.
                vtk_get_meth = getattr(klass, 'Get' + m)
                self._write_trait(out, name, t_def, vtk_get_meth,
                                  mapped=True, broken_bool=True)
            else:
                self._write_trait(out, name, t_def, vtk_set_meth,
                                  mapped=True)
        return updateable_traits

    def _gen_state_methods(self, klass, out):
        parser = self.parser
        indent = self.indent
        meths = parser.get_state_methods()
        updateable_traits = {}

        for m in meths:
            name = self._reform_name(m)
            updateable_traits[name] = 'Get' + m
            d = {}
            vtk_val = 0
            for key, val in meths[m]:
                d[self._reform_name(key)] = val
                if isinstance(val, vtk.vtkObjectBase):
                    vtk_val = 1

            # Setting the default value of the traits of these classes
            # Else they are not instantiable
            if klass.__name__ == 'vtkCellQuality' \
                    and m == 'QualityMeasure':
                vtk_val = 1
            if klass.__name__ == 'vtkRenderView' \
                    and m == 'InteractionMode':
                vtk_val = 1
            if klass.__name__ == 'vtkMatrixMathFilter' \
                    and m == 'Operation':
                vtk_val = 1
            if klass.__name__ == 'vtkResliceImageViewer' \
                    and m == 'ResliceMode':
                vtk_val = 'axis_aligned'
            if  klass.__name__ == 'vtkThreshold' \
                   and m == 'PointsDataType':
                vtk_val = 10

            if (not hasattr(klass, 'Set' + m)):
                # Sometimes (very rarely) the VTK method is
                # inconsistent.  For example in VTK-4.4
                # vtkExtentTranslator::SetSplitMode does not exist.
                # In this case wrap it specially.
                vtk_val = 1
            if  vtk_val == 0 and m in ['DataScalarType', 'OutputScalarType',
                                       'UpdateExtent']:
                vtk_val = 2

            # Sometimes, some methods have default values that are
            # outside the specified choices.  This is to special case
            # these.
            extra_val = None
            if vtk_val == 0 and klass.__name__ == 'vtkGenericEnSightReader' \
                   and m == 'ByteOrder':
                extra_val = 2
            if vtk_val == 0 and klass.__name__ == 'vtkImageData' \
                   and m == 'ScalarType':
                extra_val = list(range(0, 22))
            if vtk_val == 0 and klass.__name__ == 'vtkImagePlaneWidget' \
                   and m == 'PlaneOrientation':
                extra_val = 3
            if (vtk_val == 0) and (klass.__name__ == 'vtkThreshold') \
                   and (m == 'AttributeMode'):
                extra_val = -1
            if (sys.platform == 'darwin') and (vtk_val == 0) \
                   and (klass.__name__ == 'vtkRenderWindow') \
                   and (m == 'StereoType'):
                extra_val = 0

            if not vtk_val:
                default = self._reform_name(meths[m][0][0])
                if extra_val is None:
                    t_def = """traits.Trait('%(default)s',
                                       tvtk_base.TraitRevPrefixMap(%(d)s))"""\
                    %locals()
                elif hasattr(extra_val, '__iter__'):
                    extra_val = str(extra_val)[1:-1]

            if (not hasattr(klass, 'Set' + m)):
                # Sometimes (very rarely) the VTK method is
                # inconsistent.  For example in VTK-4.4
                # vtkExtentTranslator::SetSplitMode does not exist.
                # In this case wrap it specially.
                vtk_val = 1
            if  vtk_val == 0 and m in ['DataScalarType', 'OutputScalarType',
                                       'UpdateExtent']:
                vtk_val = 2

            # Sometimes, some methods have default values that are
            # outside the specified choices.  This is to special case
            # these.
            extra_val = None
            if vtk_val == 0 and klass.__name__ == 'vtkGenericEnSightReader' \
                   and m == 'ByteOrder':
                extra_val = 2
            if vtk_val == 0 and klass.__name__ == 'vtkImageData' \
                   and m == 'ScalarType':
                extra_val = list(range(0, 22))
            if vtk_val == 0 and klass.__name__ == 'vtkImagePlaneWidget' \
                   and m == 'PlaneOrientation':
                extra_val = 3
            if (vtk_val == 0) and (klass.__name__ == 'vtkThreshold') \
                   and (m == 'AttributeMode'):
                extra_val = -1
            if (sys.platform == 'darwin') and (vtk_val == 0) \
                   and (klass.__name__ == 'vtkRenderWindow') \
                   and (m == 'StereoType'):
                extra_val = 0

            if not vtk_val:
                default = self._reform_name(meths[m][0][0])
                if extra_val is None:
                    t_def = """traits.Trait('%(default)s',
                                       tvtk_base.TraitRevPrefixMap(%(d)s))"""\
                    %locals()
                elif hasattr(extra_val, '__iter__'):
                    extra_val = str(extra_val)[1:-1]
                    t_def = """traits.Trait('%(default)s', %(extra_val)s,
                                       tvtk_base.TraitRevPrefixMap(%(d)s))"""\
                    %locals()
                else:
                    t_def = """traits.Trait('%(default)s', %(extra_val)s,
                                       tvtk_base.TraitRevPrefixMap(%(d)s))"""\
                    %locals()
                vtk_set_meth = getattr(klass, 'Set' + m)
                self._write_trait(out, name, t_def, vtk_set_meth,
                                  mapped=True)
            else:
                del updateable_traits[name]
                vtk_meth = getattr(klass, 'Get' + m)
                self._write_tvtk_method(klass, out, vtk_meth)
                if vtk_val == 2:
                    vtk_meth = getattr(klass, 'Set' + m)
                    self._write_tvtk_method(klass, out, vtk_meth)
                for key, val in meths[m][1:]:
                    x = self._reform_name(key)
                    vtk_meth = getattr(klass, 'Set%sTo%s'%(m, key))
                    decl = 'def set_%s_to_%s(self):'%(name, x)
                    body = 'self._vtk_obj.Set%(m)sTo%(key)s()\n'%locals()
                    self._write_generic_method(out, decl, vtk_meth, body)

        return updateable_traits

    def _gen_get_set_methods(self, klass, out):
        parser = self.parser
        meths = parser.get_get_set_methods()
        updateable_traits = {}
        allow_update_failure = set()
        for m in meths:
            name = self._reform_name(m)
            updateable_traits[name] = 'Get' + m
            vtk_get_meth = getattr(klass, 'Get' + m)
            vtk_set_meth = getattr(klass, 'Set' + m)

            if meths[m]:
                default, rng = meths[m]
            else:
                # In this case we could not get the defaults and range
                # since class has no known concrete subclass.  This
                # happens in very rare circumstances and while the
                # below look like hacks, they are the best we can do.
                sig = parser.get_method_signature(vtk_get_meth)
                if sig[0][1] is None:
                    ret = sig[0][0][0]
                    if ret[:3] == 'vtk':
                        default, rng = None, None
                    elif ret == 'int':
                        default, rng = 0, None
                    elif ret == 'float':
                        default, rng = 0.0, None
                    elif ret == 'string':
                        default, rng = '', None
                    else:
                        default, rng = None, None
                else:
                    self._write_tvtk_method(klass, out, vtk_get_meth, sig)
                    self._write_tvtk_method(klass, out, vtk_set_meth)
                    continue

            if m == 'Output':
                self._write_get_output_method(klass, out, set=True)
                del updateable_traits['output']

            elif m == 'Source':
                # Special cased because vtkGlyph3D.GetSource/SetSource
                # etc. have a special structure to support multiple
                # sources.
                del updateable_traits['source']
                self._write_get_source_method(klass, out)

            elif m == 'ScalarType':
                del updateable_traits['scalar_type']

            elif m == 'Input':
                # In VTK > 4.5, Set/GetInput have multiple signatures.
                del updateable_traits['input']
                self._write_get_input_method(klass, out)

            elif m == 'InputConnection':
                del updateable_traits['input_connection']
                self._write_get_input_connection_method(klass, out)

            elif m.endswith('FileName'):
                t_def = 'tvtk_base.vtk_file_name("")'
                self._write_trait(out, name, t_def, vtk_set_meth, mapped=False)

            elif m.endswith('FilePrefix'):
                t_def = 'tvtk_base.vtk_file_prefix("")'
                self._write_trait(out, name, t_def, vtk_set_meth, mapped=False)

            elif klass.__name__ == 'vtkImageReader2' and m == 'HeaderSize':
                # The documentation of vtkImageReader2.GetHeaderSize says
                # it returns `int`, but really the API meant `long`
                # matters for Python 2
                if PY_VER < 3:
                    default = long(default)
                    t_def = ('traits.Long({default}, '
                             'enter_set=True, auto_set=False)').format(default=default)
                else:
                    t_def = ('traits.Int({default}, '
                             'enter_set=True, auto_set=False)').format(default=default)
                self._write_trait(out, name, t_def, vtk_set_meth, mapped=False)

            elif klass.__name__ == 'vtkHardwareSelector' and name == 'prop_color_value':
                # The VTK GetPropColorValue method returns an uninitialised value
                # that is not a valid color, we will still try to update it but
                # we allow the update for this trait to fail
                allow_update_failure.add(name)

                t_def = ('tvtk_base.vtk_color_trait('
                         '(traits.Undefined, traits.Undefined, traits.Undefined))')
                self._write_trait(out, name, t_def, vtk_set_meth, mapped=False,
                                  force_update='False')

            elif (is_version_58() and klass.__name__ == 'vtkAxesTransformRepresentation' and
                      name == 'tolerance'):
                # e.g. The range of the tolerance is 1-100 but the value initialised by
                # VTK is zero, clearly not right
                allow_update_failure.add(name)
                message = ("vtkAxesTransformRepresentation: "
                           "tolerance not updatable "
                           "(VTK 5.8 bug - value not properly initialized)")
                print(message)
                default = rng[0]
                t_def = ('traits.Trait({default}, traits.Range{rng}, '
                         'enter_set=True, auto_set=False)').format(default=default,
                                                                   rng=rng)
                self._write_trait(out, name, t_def, vtk_set_meth, mapped=False)

            elif isinstance(default, str) and default.endswith('_p_void'):
                # The VTK Get method for the attribute does not return
                # a sensible value. We will still try to update it (i.e.
                # not removing `name` from `updateable_traits`) but we allow
                # it to fail
                allow_update_failure.add(name)

                message = '{klass}.Get{name} gives an initial value of {default}.'
                print(message.format(klass=klass.__name__,
                                     name=m, default=default))

                # `patch_default` use the Set method to find an appropriate default.
                # `new_default` is then passed to `get_trait_type` for finding
                # the trait type. When writing the code, `new_default` is replaced
                # with traits.Undefined (or a tuple of Undefined) so that we don't
                # pretend we know the value in the VTK object.
                new_default = patch_default(vtk_set_meth, default)

                if isinstance(new_default, str) and new_default.endswith('_p_void'):
                    # Still undefined, we give up, the trait can be anything
                    t_def = 'traits.Trait(enter_set=True, auto_set=False)'
                    self._write_trait(out, name, t_def, vtk_set_meth, mapped=False)
                    print('We could not determine the appropriate type, '
                          'it can be anything')
                else:
                    # Overwrite the default with Undefined's
                    if type(new_default) in (tuple, list):
                        default = "({})".format(", ".join(
                            ("traits.Undefined",)*len(new_default)))
                    else:
                        default = "traits.Undefined"

                    trait_type = get_trait_type(new_default)
                    t_def = ('traits.Trait({default}, '  # traits.Undefined
                             '{trait_type}({meta}), '    # the new default trait
                             'enter_set=True, auto_set=False)').format(
                                 default=default,
                                 trait_type=trait_type,
                                 meta=get_array_meta(new_default))
                    self._write_trait(out, name, t_def, vtk_set_meth, mapped=False)
                    print('We found a type from the Set method:', trait_type,
                          'It may be undefined upon initialisation.')

            elif (default is None or
                      isinstance(default, vtk.vtkObjectBase)):
                g_sig = parser.get_method_signature(vtk_get_meth)
                s_sig = parser.get_method_signature(vtk_set_meth)
                # Bunch of hacks to work around issues.
                #print g_sig, vtk_get_meth, klass.__name__
                if len(g_sig) == 0:
                    g_sig = [([None], None)]

                if len(s_sig) == 0:
                    s_sig = [([None], [None])]
                    g_sig = [([None], None)]

                elif s_sig[0][1] is None or s_sig[0][1] == '':
                    s_sig[0] = list(s_sig[0])
                    s_sig[0][1] = [None]

                if g_sig[0][0][0] == 'string':
                    # If the get method really returns a string
                    # wrap it as such.
                    t_def = 'traits.Trait(None, None, '\
                            'traits.String(enter_set=True, auto_set=False))'
                    self._write_trait(out, name, t_def, vtk_set_meth,
                                      mapped=False)
                else:
                    if (g_sig[0][1] is None) and (len(s_sig[0][1]) == 1):
                        # Get needs no args and Set needs one arg
                        self._write_property(out, name, vtk_get_meth,
                                             vtk_set_meth)
                    else: # Get has args or Set needs many args.
                        self._write_tvtk_method(klass, out, vtk_get_meth, g_sig)
                        self._write_tvtk_method(klass, out, vtk_set_meth, s_sig)
                    del updateable_traits[name]

            elif (isinstance(default, tuple) and len(default) == 3 and
                      (name.find('color') > -1 or name.find('bond_color') > -1 or
                       name.find('background') > -1)):
                # This is a color
                force = 'False'
                # 'vtkProperty' and 'vtkLight' are special because if you change
                # one color the GetColor changes value so we must force an
                # update.
                if klass.__name__ in ['vtkProperty', 'vtkLight']:
                    force = 'True'

                t_def = 'tvtk_base.vtk_color_trait({default})'.format(default=default)
                self._write_trait(out, name, t_def, vtk_set_meth,
                                  mapped=False, force_update=force)

            elif rng:    # Has a specified range of valid values.

                # If the default is just a little off from the range
                # then extend the range.
                if (default < rng[0]) and (rng[0] - default) < 2:
                    rng = (default, rng[1])
                if (default > rng[1]) and (default - rng[1]) < 2:
                    rng = (rng[0], default)
                # Sometimes the default is not in the valid range to
                # perhaps indicate that the class is not initialized
                if (default < rng[0]) or (default > rng[1]):
                    t_def = 'traits.Trait(%(default)s, %(default)s, '\
                            'traits.Range%(rng)s'%locals()
                    t_def = t_def[:-1] + ', enter_set=True, auto_set=False))'
                else:
                    t_def = 'traits.Trait(%(default)s, '\
                            'traits.Range%(rng)s'%locals()
                    t_def = t_def[:-1] + ', enter_set=True, auto_set=False))'
                self._write_trait(out, name, t_def, vtk_set_meth,
                                  mapped=False)

            else:
                try:
                    t_def = ('{trait_type}('
                             '{meta}'
                             'enter_set=True, auto_set=False)').format(
                                 trait_type=get_trait_type(default),
                                 meta=get_array_meta(default))
                except Exception:
                    print("%s:"%klass.__name__, end=' ')
                    print("Ignoring method: Get/Set%s"%m)
                    print("default: %s, range: None"%default)
                    del updateable_traits[name]
                else:
                    self._write_trait(out, name, t_def, vtk_set_meth,
                                      mapped=False)

        return updateable_traits, allow_update_failure

    def _gen_get_methods(self, klass, out):
        parser = self.parser
        meths = parser.get_get_methods()
        for m in meths:
            vtk_get_meth = getattr(klass, m)
            if m == 'GetOutput': # GetOutput is special.
                self._write_get_output_method(klass, out, set=False)
            elif m == 'GetInput': # GetInput is special.
                self._write_pure_get_input_method(klass, out)
            elif m == 'GetOutputPort':
                # This method sometimes prints warnings so we handle
                # it specially.GetInput is special.
                self._write_pure_get_output_port_method(klass, out)
            else:
                name = self._reform_name(m[3:])
                sig = parser.get_method_signature(vtk_get_meth)
                simple_get = 0
                if len(sig) == 1 and sig[0][1] is None:
                    simple_get = 1
                elif len(sig) > 1:
                    for i in sig:
                        if i[1] is None:
                            simple_get = 1
                            break
                if simple_get:
                    self._write_property(out, name, vtk_get_meth, None)
                else:
                    # Cannot be represented as a simple property,
                    # so we wrap it as a plain old method.
                    self._write_tvtk_method(klass, out, vtk_get_meth, sig)

    def _gen_other_methods(self, klass, out):
        parser = self.parser
        meths = parser.get_other_methods()
        for m in meths:
            vtk_meth = getattr(klass, m)
            self._write_tvtk_method(klass, out, vtk_meth)


    #################################################################
    # Private utility methods.
    #################################################################

    def _reform_name(self, name, method=False):
        """Converts a VTK name to an Enthought style one.  If `method`
        is True it does not touch names that are all upper case."""
        if name == 'TeX':
            # Special case for some of the names.  TeX occurs in the
            # vtkGL2PSExporter class.
            return 'tex'
        if name.isupper() and method:
            # All upper case names should remain the same since they
            # are usually special methods.
            return name

        res = camel2enthought(name)
        if keyword.iskeyword(res):
            return res + '_'
        else:
            return res

    def _get_class_name(self, klasses):
        """Returns renamed VTK classes as per TVTK naming style."""
        ret = []
        if type(klasses) in (list, tuple):
            return  [get_tvtk_name(x.__name__) \
                     for x in klasses]
        else:
            return get_tvtk_name(klasses.__name__)

    def _find_type(self, val):
        """Given `val` which is extracted from the method call
        signature, this returns the type of the value.  Right now this
        is in ['vtk', 'array', 'basic'].  'vtk' refers to a VTK type,
        'array' to a vtkDataArray/vtkCellArray/vtkPoints/vtkIdList,
        'basic' refers to a non-VTK, basic Python type.
        """
        _arr_types = ['Array', 'vtkPoints', 'vtkIdList']
        s = repr(val)
        if s.find('vtk') > -1:
            for i in _arr_types:
                if s.find(i) > -1:
                    return 'array'
            return 'vtk'
        else:
            return 'basic'

    def _find_arg_type(self, sig):
        """Given a method signature `sig`, this finds the argument
        types.  It uses the `_find_type` method to obtain its result.
        If no arguments are present in *all* of the signatures, then
        it returns `None`.

        """
        if len(sig) == 1:
            if sig[0][1] is None:
                return None
        args = [s[1] for s in sig]
        return self._find_type(args)

    def _find_return_type(self, sig):
        """Given a method signature `sig`, this finds the return
        types.
        """
        rets = [s[0] for s in sig]
        return self._find_type(rets)

    def _find_sig_type(self, sig):
        """Given a method signature `sig`, this finds the return and
        argument types using.  This is a convenience type and returns
        a tuple containing (ret_type, arg_type).
        """
        return self._find_return_type(sig), self._find_arg_type(sig)

    def _find_array_arg_sig(self, sig):
        """Returns a list of argument signatures from the signature
        information for a method.
        """
        return [s[1] for s in sig]

    #################################################################
    # The following methods do the writing.
    #################################################################

    def _write_get_output_method(self, klass, out, set=False):
        """Write the get_output method.  This method is special and
        needs special care.  `klass` is the class for which the method
        is being wrapped, `out` is the output file.  If `set` is True,
        a set_output method is also wrapped.  This defaults to False.
        """
        vtk_get_meth = getattr(klass, 'GetOutput')
        sig = self.parser.get_method_signature(vtk_get_meth)

        # First write out a property.
        doc = "Output of this source, i.e. the result of `get_output()`."
        if set:
            trait_def = """
            def _get_output(self):
                return wrap_vtk(self._vtk_obj.GetOutput())

            def _set_output(self, obj):
                old_val = self._get_output()
                self._wrap_call(self._vtk_obj.SetOutput, deref_vtk(obj))
                self.trait_property_changed('output', old_val, obj)
            output = traits.Property(_get_output, _set_output,
                                     help=\"%(doc)s\")

            """%locals()
        else:
            trait_def = """
            def _get_output(self):
                return wrap_vtk(self._vtk_obj.GetOutput())
            output = traits.Property(_get_output,
                                     help=\"%(doc)s\")

            """%locals()
        out.write(self.indent.format(trait_def))

        # Now write the generic method.
        if len(sig) == 1:
            decl = "def get_output(self):"
            body = "return wrap_vtk(self._vtk_obj.GetOutput())"
        else:
            decl = "def get_output(self, idx=None):"
            body = """
            if idx is None:
                return wrap_vtk(self._vtk_obj.GetOutput())
            else:
                return wrap_vtk(self._vtk_obj.GetOutput(idx))
            """
        self._write_generic_method(out, decl, vtk_get_meth, body)

        if set:
            decl = "def set_output(self, obj):"
            body = "old_val = self._get_output()\n"
            body += "self._wrap_call(self._vtk_obj.SetOutput, deref_vtk(obj))\n"
            body += "self.trait_property_changed('output', old_val, obj)\n"
            vtk_set_meth = getattr(klass, 'SetOutput')
            self._write_generic_method(out, decl,
                                       vtk_set_meth, body)

    def _write_get_source_method(self, klass, out):
        """Write the set/get_source method.  This method needs special
        care.  `klass` is the class for which the method is being
        wrapped, `out` is the output file.
        """
        vtk_get_meth = getattr(klass, 'GetSource')
        vtk_set_meth = getattr(klass, 'SetSource')
        set_sig = self.parser.get_method_signature(vtk_set_meth)
        if len(set_sig) > 1:
            # Special case.  First write the property for the first source.
            doc = "The first source of this object, i.e. the result of `get_source(0)`."
            trait_def = """
            def _get_source(self):
                return wrap_vtk(self._vtk_obj.GetSource(0))

            def _set_source(self, obj):
                old_val = self._get_source()
                self._wrap_call(self._vtk_obj.SetSource, deref_vtk(obj))
                self.trait_property_changed('source', old_val, obj)
            source = traits.Property(_get_source, _set_source,
                                     help=\"%(doc)s\")

            """%locals()
            out.write(self.indent.format(trait_def))
            # Now wrap the set_source and get_source.
            self._write_tvtk_method(klass, out, vtk_get_meth)
            self._write_tvtk_method(klass, out, vtk_set_meth, set_sig)
        else:
            self._write_property(out, 'source', vtk_get_meth, vtk_set_meth)

    def _write_pure_get_output_port_method(self, klass, out):
        """Handle the GetOutputPort method so that it does not print
        unnecessary warning messages.  `klass` is the class for which
        the method is being wrapped, `out` is the output file.
        """
        vtk_get_meth = getattr(klass, 'GetOutputPort')
        t_def = """
        def _get_output_port(self):
            if self._vtk_obj.GetNumberOfOutputPorts():
                return wrap_vtk(self._vtk_obj.GetOutputPort())
            else:
                return None
        """%locals()
        indent = self.indent
        out.write(indent.format(t_def))
        t_def = """output_port = traits.Property(_get_output_port, help=\\"""
        out.write(indent.format(t_def))
        doc = vtk_get_meth.__doc__
        self.dm.write_trait_doc(doc, out, indent)
        # Close the function definition.
        out.write(indent.format(')'))
        out.write('\n')

    def _write_pure_get_input_method(self, klass, out):
        """Write the get_input method when the class only has the
        getter and no setter.  `klass` is the class for which the
        method is being wrapped, `out` is the output file.
        """
        vtk_get_meth = getattr(klass, 'GetInput')
        get_sig = self.parser.get_method_signature(vtk_get_meth)
        if len(get_sig) > 1:
            # Special case.  First write the property for the first input.
            doc = "The first input of this object, i.e. the result of `get_input(0)`."
            trait_def = """
            def _get_input(self):
                try:
                    return wrap_vtk(self._vtk_obj.GetInput(0))
                except TypeError:
                    return wrap_vtk(self._vtk_obj.GetInput())
            input = traits.Property(_get_input,
                                    help=\"%(doc)s\")

            """%locals()
            out.write(self.indent.format(trait_def))
            # Now wrap the get_input with args.
            self._write_tvtk_method(klass, out, vtk_get_meth)
        else:
            self._write_property(out, 'input', vtk_get_meth, None)

    def _write_get_input_method(self, klass, out):
        """Write the set/get_input method.  This method needs special
        care.  `klass` is the class for which the method is being
        wrapped, `out` is the output file.
        """
        vtk_get_meth = getattr(klass, 'GetInput')
        vtk_set_meth = getattr(klass, 'SetInput')
        set_sig = self.parser.get_method_signature(vtk_set_meth)
        if len(set_sig) > 1:
            # Special case.  First write the property for the first input.
            doc = "The first input of this object, i.e. the result of `get_input(0)`."
            trait_def = """
            def _get_input(self):
                try:
                    return wrap_vtk(self._vtk_obj.GetInput(0))
                except TypeError:
                    return wrap_vtk(self._vtk_obj.GetInput())

            def _set_input(self, obj):
                old_val = self._get_input()
                self._wrap_call(self._vtk_obj.SetInput, deref_vtk(obj))
                self.trait_property_changed('input', old_val, obj)
            input = traits.Property(_get_input, _set_input,
                                    help=\"%(doc)s\")

            """%locals()
            out.write(self.indent.format(trait_def))
            # Now wrap the set_input and get_input.
            self._write_tvtk_method(klass, out, vtk_get_meth)
            self._write_tvtk_method(klass, out, vtk_set_meth, set_sig)
        else:
            self._write_property(out, 'input', vtk_get_meth, vtk_set_meth)

    def _write_get_input_connection_method(self, klass, out):
        """Write the set/get_input_connection method.  This method
        needs needs to be wrapped as a property and a method for
        convenience.  `klass` is the class for which the method is
        being wrapped, `out` is the output file.
        """
        vtk_get_meth = getattr(klass, 'GetInputConnection')
        vtk_set_meth = getattr(klass, 'SetInputConnection')
        doc = "The first input connection for this object, i.e. the result of `get_input_connection(0, 0)`."
        trait_def = """
        def _get_input_connection(self):
            if self._vtk_obj.GetTotalNumberOfInputConnections():
                return wrap_vtk(self._vtk_obj.GetInputConnection(0, 0))
            else:
                return None

        def _set_input_connection(self, obj):
            old_val = self._get_input_connection()
            self._wrap_call(self._vtk_obj.SetInputConnection, deref_vtk(obj))
            self.trait_property_changed('input_connection', old_val, obj)
        input_connection = traits.Property(_get_input_connection,
                                           _set_input_connection,
                                           help=\"%(doc)s\")

        """%locals()
        out.write(self.indent.format(trait_def))
        # Now wrap the set_input_connection and get_input_connection.
        self._write_tvtk_method(klass, out, vtk_get_meth)
        self._write_tvtk_method(klass, out, vtk_set_meth)

    def _write_tvtk_method(self, klass, out, vtk_meth, sig=None):
        """Write a generic tvtk_method to `out`.

        Parameters
        ----------

        - out : file like object

        - vtk_meth : VTK method

          The VTK method to wrap.  A docstring is extracted from
          this.

        - sig : Signature of vtk_method (default: None)

          If None, this is computed.  If not, the passed signature
          information is used.
        """
        if sig is None:
            sig = self.parser.get_method_signature(vtk_meth)

        # VTK 6.2: There exists no method signature for false built in
        # functions/methods
        if sig is None:
            return

        # Figure out if we really need to wrap the return and deref
        # the args.
        ret_type, arg_type = self._find_sig_type(sig)

        vtk_m_name = vtk_meth.__name__
        name = self._reform_name(vtk_m_name, method=True)
        if keyword.iskeyword(name):
            name = name + '_'
        method_affects_input = vtk_m_name in ['AddInput', 'RemoveInput',
                                              'RemoveAllInputs',
                                              'SetInputByNumber']
        method_needs_update = (vtk_m_name in ['InsertNextCell'] and
                               klass.__name__ in ['vtkCellArray'])

        if arg_type is None:
            decl = 'def %s(self):'%name
            body = ""
            if method_affects_input:
                body += "old_val = self._get_input()\n"
            if ret_type in ['vtk', 'array']:
                body += "ret = wrap_vtk(self._vtk_obj.%s())\n"\
                        %vtk_m_name
            else:
                body += "ret = self._vtk_obj.%s()\n"\
                        %vtk_m_name
            if method_affects_input:
                body += "self.trait_property_changed('input', old_val, self._get_input())\n"
            body += "return ret\n\n"

        else:
            decl = 'def %s(self, *args):'%name
            if arg_type == 'vtk':
                body = ""
                if method_affects_input:
                    body += "old_val = self._get_input()\n"
                body += "my_args = [deref_vtk(x) for x in args]\n"\
                        "ret = self._wrap_call(self._vtk_obj.%s, *my_args)\n"\
                        %vtk_m_name
                if method_affects_input:
                    body += "self.trait_property_changed('input', old_val, self._get_input())\n"

            elif arg_type == 'array':
                arr_sig = self._find_array_arg_sig(sig)
                body = "my_args = deref_array(args, %s)\n"\
                       "ret = self._wrap_call(self._vtk_obj.%s, *my_args)\n"\
                       %(arr_sig, vtk_m_name)
                ##########################################################
                # When a cell is inserted, number of cells is not updated.
                # Fixes GH Issue 178.
                ##########################################################
                if method_needs_update:
                    body += "self.update_traits()\n"
            else:
                body = "ret = self._wrap_call(self._vtk_obj.%s, *args)\n"\
                       %vtk_m_name
            if ret_type in ['vtk', 'array']:
                body += "return wrap_vtk(ret)\n"
            else:
                body += "return ret\n"

        self._write_generic_method(out, decl, vtk_meth, body)

    def _write_generic_method(self, out, decl, vtk_doc_meth, body):
        """Write out a method given the declaration, `decl`, the VTK
        method, `vtk_doc_meth`, from which the docstring is to be
        extracted and the code body, `body`.  Each of these is set as
        per the current indentation level.  output is written to the
        `out` object.

        `vtk_doc_meth` could also be a string, in which case the
        string is used directly.

        """
        if type(vtk_doc_meth) is str:
            doc = vtk_doc_meth
        else: # Must be a method so get the docstring.
            doc = self.dm.get_method_doc(vtk_doc_meth.__doc__)
        indent = self.indent
        out.write(indent.format(decl))
        indent.incr()
        if doc:
            out.write(indent.format('"""\n' + doc + '"""\n'))
        out.write(indent.format(body))
        out.write('\n')
        indent.decr()

    def _write_trait(self, out, t_name, t_def, vtk_set_meth,
                     mapped, force_update=None, broken_bool=False):
        """Write out a complete trait definition to `out`.

        Parameters
        ----------
        - out : File like object.

        - t_name : `string`: Name of the trait.

        - t_def : `string` : Trait definition.

        - vtk_set_meth : VTK setter method.

        - mapped : `bool` : Specifies if the trait is mapped.

        - force_update : `string` or `None` : force_update argument.

        - broken_bool : `bool` (default: `False`)

          If `True` the bool method does not have a 'Set' method and
          must be handled specially.  In this case make sure that the
          vtk_set_meth points to the 'Get' method.

        """
        changed = '_%s_changed'%t_name
        vtk_m_name = vtk_set_meth.__name__
        map_str = ''
        if mapped:
            map_str = '_'
        force_str = ''
        if force_update is not None:
            force_str = ', %s'%force_update

        # Fixing the trait definition in order to handle the help trait.
        if t_def.endswith(')'):
            t_def = t_def[:-1] + ', help=\\'
        else:
            t_def += '(help=\\'
        trait_def = '%(t_name)s = %(t_def)s'%locals()

        if broken_bool:
            msg = "If broken_bool is true, make sure vtk_set_meth "\
                  "is of form 'GetProp'"
            assert vtk_m_name[:3] == 'Get', msg
            vtk_on_name = vtk_m_name[3:] + 'On'
            vtk_off_name = vtk_m_name[3:] + 'Off'
            changed_def = """
            def %(changed)s(self, old_val, new_val):
                def _bool_change(val, obj=self._vtk_obj):
                    if val:
                        obj.%(vtk_on_name)s()
                    else:
                        obj.%(vtk_off_name)s()
                self._do_change(_bool_change, self.%(t_name)s%(map_str)s%(force_str)s)
            """%locals()
        else:
            changed_def = """
            def %(changed)s(self, old_val, new_val):
                self._do_change(self._vtk_obj.%(vtk_m_name)s,
                                self.%(t_name)s%(map_str)s%(force_str)s)
            """%locals()

        indent = self.indent
        # First write the trait definition.
        out.write(indent.format(trait_def))
        # Write the help docs.
        doc = vtk_set_meth.__doc__
        self.dm.write_trait_doc(doc, out, indent)
        # End the function definition.
        out.write(indent.format(')'))
        out.write('\n')
        # Write the handler method.
        out.write(indent.format(changed_def))
        out.write('\n')

    def _write_property(self, out, t_name, vtk_get_meth, vtk_set_meth,
                        multi_arg=False):
        """Writes out a traited property to `out` given the trait
        name, `t_name`, the VTK get method, `vtk_get_meth` an optional
        VTK set method for read-write traits as, `vtk_set_meth` plus a
        boolean value for `multi_arg`.  If `multi_arg` is True, the
        setter is treated as if it accepts a list of parameters.  If
        not the setter is treated as if it accepts a single parameter.
        """
        indent = self.indent
        getter = '_get_%s'%t_name
        vtk_get_name = vtk_get_meth.__name__
        sig = self.parser.get_method_signature(vtk_get_meth)
        ret_type = self._find_return_type(sig)

        if ret_type in ['vtk', 'array']:
            trait_def = """
            def %(getter)s(self):
                return wrap_vtk(self._vtk_obj.%(vtk_get_name)s())
            """%locals()
        else:
            trait_def = """
            def %(getter)s(self):
                return self._vtk_obj.%(vtk_get_name)s()
            """%locals()
        out.write(indent.format(trait_def))

        if vtk_set_meth:
            setter = '_set_%s'%t_name
            vtk_set_name = vtk_set_meth.__name__
            sig = self.parser.get_method_signature(vtk_set_meth)
            arg_type = self._find_arg_type(sig)
            if multi_arg:
                if arg_type == 'vtk':
                    trait_def = """
                    def %(setter)s(self, *args):
                        old_val = self.%(getter)s()
                        my_args = [deref_vtk(x) for x in args]
                        self._wrap_call(self._vtk_obj.%(vtk_set_name)s,
                                        *my_args)
                        self.trait_property_changed('%(t_name)s', old_val, args)
                    """%locals()
                elif arg_type == 'array':
                    arr_sig = self._find_array_arg_sig(sig)
                    trait_def = """
                    def %(setter)s(self, *args):
                        old_val = self.%(getter)s()
                        my_args = deref_array(args, %(arr_sig)s)
                        self._wrap_call(self._vtk_obj.%(vtk_set_name)s,
                                        *my_args)
                        self.trait_property_changed('%(t_name)s', old_val, args)
                    """%locals()

                else:
                    trait_def = """
                    def %(setter)s(self, *args):
                        old_val = self.%(getter)s()
                        self._wrap_call(self._vtk_obj.%(vtk_set_name)s,
                                        *args)
                        self.trait_property_changed('%(t_name)s', old_val, args)
                    """%locals()
            else:
                if arg_type == 'vtk':
                    trait_def = """
                    def %(setter)s(self, arg):
                        old_val = self.%(getter)s()
                        self._wrap_call(self._vtk_obj.%(vtk_set_name)s,
                                        deref_vtk(arg))
                        self.trait_property_changed('%(t_name)s', old_val, arg)
                    """%locals()
                elif arg_type == 'array':
                    arr_sig = self._find_array_arg_sig(sig)
                    trait_def = """
                    def %(setter)s(self, arg):
                        old_val = self.%(getter)s()
                        my_arg = deref_array([arg], %(arr_sig)s)
                        self._wrap_call(self._vtk_obj.%(vtk_set_name)s,
                                        my_arg[0])
                        self.trait_property_changed('%(t_name)s', old_val, arg)
                    """%locals()

                else:
                    trait_def = """
                    def %(setter)s(self, arg):
                        old_val = self.%(getter)s()
                        self._wrap_call(self._vtk_obj.%(vtk_set_name)s,
                                        arg)
                        self.trait_property_changed('%(t_name)s', old_val, arg)
                    """%locals()
            out.write(indent.format(trait_def))
            t_def = "traits.Property(%(getter)s, %(setter)s, help=\\"%locals()
        else:
            t_def = "traits.Property(%(getter)s, help=\\"%locals()

        trait_def = """%(t_name)s = %(t_def)s"""%locals()
        out.write(indent.format(trait_def))
        doc = vtk_get_meth.__doc__
        self.dm.write_trait_doc(doc, out, indent)
        # Close the function definition.
        out.write(indent.format(')'))
        out.write('\n')
