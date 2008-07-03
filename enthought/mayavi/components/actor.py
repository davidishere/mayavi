"""A simple actor component.

"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005, Enthought, Inc.
# License: BSD Style.

# Enthought library imports.
from enthought.traits.api import Instance
from enthought.traits.api import Bool
from enthought.tvtk.api import tvtk

# Local imports.
from enthought.mayavi.core.component import Component
from enthought.mayavi.core.source import Source


######################################################################
# `Actor` class.
######################################################################
class Actor(Component):
    # The version of this class.  Used for persistence.
    __version__ = 0

    # The mapper.
    mapper = Instance(tvtk.Mapper)

    # The actor.
    actor = Instance(tvtk.Actor)

    # The actor's property.
    property = Instance(tvtk.Property)

    # If texturing is enabled for the actor or not
    enable_texture = Bool(False, desc='if texturing is enabled')

    # the source of the texture's image
    texture_source_object = Instance(Source)

    # the actors texture
    texture = Instance(tvtk.Texture)

    
    ######################################################################
    # `object` interface
    ######################################################################
    def __get_pure_state__(self):
        d = super(Actor, self).__get_pure_state__()
        for attr in ('texture', 'texture_source_object', 'enable_texture'):
            d.pop(attr,None)
        return d            
    

    ######################################################################
    # `Component` interface
    ######################################################################
    def setup_pipeline(self):
        """Override this method so that it *creates* its tvtk
        pipeline.

        This method is invoked when the object is initialized via
        `__init__`.  Note that at the time this method is called, the
        tvtk data pipeline will *not* yet be setup.  So upstream data
        will not be available.  The idea is that you simply create the
        basic objects and setup those parts of the pipeline not
        dependent on upstream sources and filters.
        """
        self.mapper = tvtk.PolyDataMapper(use_lookup_table_scalar_range=1)
        self.actor = tvtk.Actor()
        self.property = self.actor.property
        self.texture = tvtk.Texture()
    
    def update_pipeline(self):
        """Override this method so that it *updates* the tvtk pipeline
        when data upstream is known to have changed.

        This method is invoked (automatically) when the input fires a
        `pipeline_changed` event.
        """
        if (len(self.inputs) == 0) or \
               (len(self.inputs[0].outputs) == 0):
            return
        self.mapper.input = self.inputs[0].outputs[0]
        self.render()

    def update_data(self):
        """Override this method to do what is necessary when upstream
        data changes.

        This method is invoked (automatically) when any of the inputs
        sends a `data_changed` event.
        """
        # Invoke render to update any changes.
        self.render()

    ######################################################################
    # `Actor` interface
    ######################################################################
    def set_lut(self, lut):
        """Set the Lookup table to use."""
        self.mapper.lookup_table = lut
    
    ######################################################################
    # Non-public interface.
    ######################################################################
    def _setup_handlers(self, old, new):
        if old is not None:
            old.on_trait_change(self.render, remove=True)
        new.on_trait_change(self.render)

    def _mapper_changed(self, old, new):
        # Setup the handlers.
        self._setup_handlers(old, new)
        # Setup the LUT.
        if old is not None:
            self.set_lut(old.lookup_table)
        # Setup the inputs to the mapper.
        if (len(self.inputs) > 0) and (len(self.inputs[0].outputs) > 0):
            new.input = self.inputs[0].outputs[0]
        # Setup the actor's mapper.
        actor = self.actor
        if actor is not None:
            actor.mapper = new
        self.render()

    def _actor_changed(self, old, new):
        # Setup the handlers.
        self._setup_handlers(old, new)
        # Set the mapper.
        mapper = self.mapper
        if mapper is not None:
            new.mapper = mapper
        # Set the property.
        prop = self.property
        if prop is not None:
            new.property = prop
        # Setup the `actors` trait.
        self.actors = [new]
        
    def _property_changed(self, old, new):
        # Setup the handlers.
        self._setup_handlers(old, new)
        # Setup the actor.
        actor = self.actor
        if new is not actor.property:
            actor.property = new

    def _foreground_changed_for_scene(self, old, new):
        # Change the default color for the actor.
        self.property.color = new
        self.render()
        
    def _scene_changed(self, old, new):
        super(Actor, self)._scene_changed(old, new)
        self._foreground_changed_for_scene(None, new.foreground)
        
    def _enable_texture_changed(self, value):
        if self.texture_source_object is None :
            self.actor.texture = None
            return
        if value:
            self.actor.texture = self.texture
        else:
            self.actor.texture = None

    def _can_object_give_image_data(self, source):
        if source is None:
            return False
        if not issubclass(source, Source):
            return False
        if source.outputs[0].is_a('vtkImageData'):
            return True
        return False

    def _change_texture_input(self):
        if self._can_object_give_image_data(self.texture_source_object):
            img_data = self.texture_source_object.outputs[0]
            self.texture.input = img_data
            self.actor.texture = self.texture
        else:
            self.texture_source_object = None

    def _texture_source_object_changed(self,old,new):
        if old is not None :
            old.on_trait_change(self._change_texture_input, 
                                'pipeline_changed', 
                                remove=True)
        if new is not None :
            new.on_trait_change(self._change_texture_input, 
                                'pipeline_changed' )

        if new is not None:
            self._change_texture_input()
        else:
            self.actor.texture = None
            self.texture.input = None
    
    def _texture_changed(self,value):
        # Setup the actor's texture.
        actor = self.actor
        if actor is not None:
            actor.texture = value
            self.texture.on_trait_change(self.render)

        self.render()
