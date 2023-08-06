from typing import List, Optional, Dict, Iterable
import aspose.pycore
import aspose.pydrawing
import aspose.threed
import aspose.threed.animation
import aspose.threed.deformers
import aspose.threed.entities
import aspose.threed.formats
import aspose.threed.profiles
import aspose.threed.render
import aspose.threed.shading
import aspose.threed.utilities

class Box(Primitive):
    '''Box.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert current object to mesh
        
        :returns: The mesh.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def length_segments(self) -> int:
        ...
    
    @length_segments.setter
    def length_segments(self, value : int):
        ...
    
    @property
    def width_segments(self) -> int:
        ...
    
    @width_segments.setter
    def width_segments(self, value : int):
        ...
    
    @property
    def height_segments(self) -> int:
        ...
    
    @height_segments.setter
    def height_segments(self, value : int):
        ...
    
    @property
    def length(self) -> float:
        '''Gets the length of the box aligned in z-axis.'''
        ...
    
    @length.setter
    def length(self, value : float):
        '''Sets the length of the box aligned in z-axis.'''
        ...
    
    @property
    def width(self) -> float:
        '''Gets the width of the box aligned in x-axis.'''
        ...
    
    @width.setter
    def width(self, value : float):
        '''Sets the width of the box aligned in x-axis.'''
        ...
    
    @property
    def height(self) -> float:
        '''Gets the height of the box aligned in y-axis.'''
        ...
    
    @height.setter
    def height(self, value : float):
        '''Sets the height of the box aligned in y-axis.'''
        ...
    
    ...

class Camera(Frustum):
    '''The camera describes the eye point of the viewer looking at the scene.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def move_forward(self, distance : float):
        '''Move camera forward towards its direction or target.
        
        :param distance: How long to move forward'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def rotation_mode(self) -> aspose.threed.entities.RotationMode:
        ...
    
    @rotation_mode.setter
    def rotation_mode(self, value : aspose.threed.entities.RotationMode):
        ...
    
    @property
    def near_plane(self) -> float:
        ...
    
    @near_plane.setter
    def near_plane(self, value : float):
        ...
    
    @property
    def far_plane(self) -> float:
        ...
    
    @far_plane.setter
    def far_plane(self, value : float):
        ...
    
    @property
    def aspect(self) -> float:
        '''Gets the aspect ratio of the frustum'''
        ...
    
    @aspect.setter
    def aspect(self, value : float):
        '''Sets the aspect ratio of the frustum'''
        ...
    
    @property
    def ortho_height(self) -> float:
        ...
    
    @ortho_height.setter
    def ortho_height(self, value : float):
        ...
    
    @property
    def up(self) -> aspose.threed.utilities.Vector3:
        '''Gets the up direction of the camera'''
        ...
    
    @up.setter
    def up(self, value : aspose.threed.utilities.Vector3):
        '''Sets the up direction of the camera'''
        ...
    
    @property
    def look_at(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @look_at.setter
    def look_at(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def direction(self) -> aspose.threed.utilities.Vector3:
        '''Gets the direction that the camera is looking at.
        Changes on this property will also affects the :py:attr:`aspose.threed.entities.Frustum.look_at` and :py:attr:`aspose.threed.entities.Frustum.target`.'''
        ...
    
    @direction.setter
    def direction(self, value : aspose.threed.utilities.Vector3):
        '''Sets the direction that the camera is looking at.
        Changes on this property will also affects the :py:attr:`aspose.threed.entities.Frustum.look_at` and :py:attr:`aspose.threed.entities.Frustum.target`.'''
        ...
    
    @property
    def target(self) -> aspose.threed.Node:
        '''Gets the target that the camera is looking at.
        If the user supports this property, it should be prior to :py:attr:`aspose.threed.entities.Frustum.look_at` property.'''
        ...
    
    @target.setter
    def target(self, value : aspose.threed.Node):
        '''Sets the target that the camera is looking at.
        If the user supports this property, it should be prior to :py:attr:`aspose.threed.entities.Frustum.look_at` property.'''
        ...
    
    @property
    def aperture_mode(self) -> aspose.threed.entities.ApertureMode:
        ...
    
    @aperture_mode.setter
    def aperture_mode(self, value : aspose.threed.entities.ApertureMode):
        ...
    
    @property
    def field_of_view(self) -> float:
        ...
    
    @field_of_view.setter
    def field_of_view(self, value : float):
        ...
    
    @property
    def field_of_view_x(self) -> float:
        ...
    
    @field_of_view_x.setter
    def field_of_view_x(self, value : float):
        ...
    
    @property
    def field_of_view_y(self) -> float:
        ...
    
    @field_of_view_y.setter
    def field_of_view_y(self, value : float):
        ...
    
    @property
    def width(self) -> float:
        '''Gets the view plane's width measured in inches'''
        ...
    
    @width.setter
    def width(self, value : float):
        '''Sets the view plane's width measured in inches'''
        ...
    
    @property
    def height(self) -> float:
        '''Gets the view plane's height measured in inches'''
        ...
    
    @height.setter
    def height(self, value : float):
        '''Sets the view plane's height measured in inches'''
        ...
    
    @property
    def aspect_ratio(self) -> float:
        ...
    
    @aspect_ratio.setter
    def aspect_ratio(self, value : float):
        ...
    
    @property
    def magnification(self) -> aspose.threed.utilities.Vector2:
        '''Gets the magnification used in orthographic camera'''
        ...
    
    @magnification.setter
    def magnification(self, value : aspose.threed.utilities.Vector2):
        '''Sets the magnification used in orthographic camera'''
        ...
    
    @property
    def projection_type(self) -> aspose.threed.entities.ProjectionType:
        ...
    
    @projection_type.setter
    def projection_type(self, value : aspose.threed.entities.ProjectionType):
        ...
    
    ...

class Circle(Curve):
    '''A :py:class:`aspose.threed.entities.Circle` curve consists of a set of points in the edge of the circle shape.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def color(self) -> aspose.threed.utilities.Vector3:
        '''Gets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @color.setter
    def color(self, value : aspose.threed.utilities.Vector3):
        '''Sets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @property
    def radius(self) -> float:
        '''The radius of the circle curve, default value is 10'''
        ...
    
    @radius.setter
    def radius(self, value : float):
        '''The radius of the circle curve, default value is 10'''
        ...
    
    ...

class CompositeCurve(Curve):
    '''A :py:class:`aspose.threed.entities.CompositeCurve` is consisting of several curve segments.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def add_segment(self, curve : aspose.threed.entities.Curve, same_direction : bool):
        '''The'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def color(self) -> aspose.threed.utilities.Vector3:
        '''Gets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @color.setter
    def color(self, value : aspose.threed.utilities.Vector3):
        '''Sets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @property
    def segments(self) -> List[CompositeCurve.Segment]:
        '''The segments of the curve.'''
        ...
    
    ...

class Curve(aspose.threed.Entity):
    '''The base class of all curve implementations.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def color(self) -> aspose.threed.utilities.Vector3:
        '''Gets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @color.setter
    def color(self, value : aspose.threed.utilities.Vector3):
        '''Sets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    ...

class Cylinder(Primitive):
    '''Parameterized Cylinder.
    It can also be used to represent the cone when one of radiusTop/radiusBottom is zero.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert current object to mesh
        
        :returns: The mesh.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def offset_bottom(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @offset_bottom.setter
    def offset_bottom(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def offset_top(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @offset_top.setter
    def offset_top(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def generate_fan_cylinder(self) -> bool:
        ...
    
    @generate_fan_cylinder.setter
    def generate_fan_cylinder(self, value : bool):
        ...
    
    @property
    def shear_bottom(self) -> aspose.threed.utilities.Vector2:
        ...
    
    @shear_bottom.setter
    def shear_bottom(self, value : aspose.threed.utilities.Vector2):
        ...
    
    @property
    def shear_top(self) -> aspose.threed.utilities.Vector2:
        ...
    
    @shear_top.setter
    def shear_top(self, value : aspose.threed.utilities.Vector2):
        ...
    
    @property
    def radius_top(self) -> float:
        ...
    
    @radius_top.setter
    def radius_top(self, value : float):
        ...
    
    @property
    def radius_bottom(self) -> float:
        ...
    
    @radius_bottom.setter
    def radius_bottom(self, value : float):
        ...
    
    @property
    def height(self) -> float:
        '''Gets the height of the cylinder.'''
        ...
    
    @height.setter
    def height(self, value : float):
        '''Sets the height of the cylinder.'''
        ...
    
    @property
    def radial_segments(self) -> int:
        ...
    
    @radial_segments.setter
    def radial_segments(self, value : int):
        ...
    
    @property
    def height_segments(self) -> int:
        ...
    
    @height_segments.setter
    def height_segments(self, value : int):
        ...
    
    @property
    def open_ended(self) -> bool:
        ...
    
    @open_ended.setter
    def open_ended(self, value : bool):
        ...
    
    @property
    def theta_start(self) -> float:
        ...
    
    @theta_start.setter
    def theta_start(self, value : float):
        ...
    
    @property
    def theta_length(self) -> float:
        ...
    
    @theta_length.setter
    def theta_length(self, value : float):
        ...
    
    ...

class Dish(Primitive):
    '''Parameterized dish.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert current object to mesh
        
        :returns: The mesh.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def height(self) -> float:
        '''Height of the dish'''
        ...
    
    @height.setter
    def height(self, value : float):
        '''Height of the dish'''
        ...
    
    @property
    def radius(self) -> float:
        '''Radius of the dish'''
        ...
    
    @radius.setter
    def radius(self, value : float):
        '''Radius of the dish'''
        ...
    
    @property
    def width_segments(self) -> int:
        ...
    
    @width_segments.setter
    def width_segments(self, value : int):
        ...
    
    @property
    def height_segments(self) -> int:
        ...
    
    @height_segments.setter
    def height_segments(self, value : int):
        ...
    
    ...

class Ellipse(Curve):
    '''An :py:class:`aspose.threed.entities.Ellipse` defines a set of points that form the shape of ellipse.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def color(self) -> aspose.threed.utilities.Vector3:
        '''Gets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @color.setter
    def color(self, value : aspose.threed.utilities.Vector3):
        '''Sets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @property
    def semi_axis1(self) -> float:
        ...
    
    @semi_axis1.setter
    def semi_axis1(self, value : float):
        ...
    
    @property
    def semi_axis2(self) -> float:
        ...
    
    @semi_axis2.setter
    def semi_axis2(self, value : float):
        ...
    
    ...

class EndPoint:
    '''The end point to trim the curve, can be a parameter value or a Cartesian point.'''
    
    @staticmethod
    def from_degree(degree : float) -> aspose.threed.entities.EndPoint:
        '''Create an end point measured in degree.'''
        ...
    
    @staticmethod
    def from_radian(degree : float) -> aspose.threed.entities.EndPoint:
        '''Create an end point measured in radian.'''
        ...
    
    @property
    def is_cartesian_point(self) -> bool:
        ...
    
    @property
    def as_point(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @property
    def as_value(self) -> float:
        ...
    
    ...

class Frustum(aspose.threed.Entity):
    '''The base class of :py:class:`aspose.threed.entities.Camera` and :py:class:`aspose.threed.entities.Light`'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def rotation_mode(self) -> aspose.threed.entities.RotationMode:
        ...
    
    @rotation_mode.setter
    def rotation_mode(self, value : aspose.threed.entities.RotationMode):
        ...
    
    @property
    def near_plane(self) -> float:
        ...
    
    @near_plane.setter
    def near_plane(self, value : float):
        ...
    
    @property
    def far_plane(self) -> float:
        ...
    
    @far_plane.setter
    def far_plane(self, value : float):
        ...
    
    @property
    def aspect(self) -> float:
        '''Gets the aspect ratio of the frustum'''
        ...
    
    @aspect.setter
    def aspect(self, value : float):
        '''Sets the aspect ratio of the frustum'''
        ...
    
    @property
    def ortho_height(self) -> float:
        ...
    
    @ortho_height.setter
    def ortho_height(self, value : float):
        ...
    
    @property
    def up(self) -> aspose.threed.utilities.Vector3:
        '''Gets the up direction of the camera'''
        ...
    
    @up.setter
    def up(self, value : aspose.threed.utilities.Vector3):
        '''Sets the up direction of the camera'''
        ...
    
    @property
    def look_at(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @look_at.setter
    def look_at(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def direction(self) -> aspose.threed.utilities.Vector3:
        '''Gets the direction that the camera is looking at.
        Changes on this property will also affects the :py:attr:`aspose.threed.entities.Frustum.look_at` and :py:attr:`aspose.threed.entities.Frustum.target`.'''
        ...
    
    @direction.setter
    def direction(self, value : aspose.threed.utilities.Vector3):
        '''Sets the direction that the camera is looking at.
        Changes on this property will also affects the :py:attr:`aspose.threed.entities.Frustum.look_at` and :py:attr:`aspose.threed.entities.Frustum.target`.'''
        ...
    
    @property
    def target(self) -> aspose.threed.Node:
        '''Gets the target that the camera is looking at.
        If the user supports this property, it should be prior to :py:attr:`aspose.threed.entities.Frustum.look_at` property.'''
        ...
    
    @target.setter
    def target(self, value : aspose.threed.Node):
        '''Sets the target that the camera is looking at.
        If the user supports this property, it should be prior to :py:attr:`aspose.threed.entities.Frustum.look_at` property.'''
        ...
    
    ...

class Geometry(aspose.threed.Entity):
    '''The base class of all renderable geometric objects (like :py:class:`aspose.threed.entities.Mesh`, :py:class:`aspose.threed.entities.NurbsSurface`, :py:class:`aspose.threed.entities.Patch` and etc.).
    
    
    
    The :py:class:`aspose.threed.entities.Geometry` base class supports:
    
    *
    
    *
    
    *'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :returns: Created element.'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element.'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :returns: Created element uv'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element uv'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def get_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Gets a vertex element with specified type
        
        :param type: which vertex element type to find
        :returns: :py:class:`aspose.threed.entities.VertexElement` instance if found, otherwise null will be returned.'''
        ...
    
    def get_vertex_element_of_uv(self, texture_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Gets a :py:class:`aspose.threed.entities.VertexElementUV` instance with given texture mapping type
        
        :returns: VertexElementUV with the texture mapping type'''
        ...
    
    def add_element(self, element : aspose.threed.entities.VertexElement):
        '''Adds an existing vertex element to current geometry
        
        :param element: The vertex element to add'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def visible(self) -> bool:
        '''Gets if the geometry is visible'''
        ...
    
    @visible.setter
    def visible(self, value : bool):
        '''Sets if the geometry is visible'''
        ...
    
    @property
    def deformers(self) -> List[aspose.threed.deformers.Deformer]:
        '''Gets all deformers associated with this geometry.'''
        ...
    
    @property
    def control_points(self) -> List[aspose.threed.utilities.Vector4]:
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def vertex_elements(self) -> List[aspose.threed.entities.VertexElement]:
        ...
    
    ...

class IIndexedVertexElement:
    '''VertexElement with indices data.'''
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    ...

class IMeshConvertible:
    '''Entities that implemented this interface can be converted to :py:class:`aspose.threed.entities.Mesh`'''
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert current object to mesh
        
        :returns: The mesh.'''
        ...
    
    ...

class IOrientable:
    '''Orientable entities shall implement this interface.'''
    
    @property
    def direction(self) -> aspose.threed.utilities.Vector3:
        '''Gets the direction that the entity is looking at.'''
        ...
    
    @direction.setter
    def direction(self, value : aspose.threed.utilities.Vector3):
        '''Sets the direction that the entity is looking at.'''
        ...
    
    @property
    def target(self) -> aspose.threed.Node:
        '''Gets the target that the entity is looking at.'''
        ...
    
    @target.setter
    def target(self, value : aspose.threed.Node):
        '''Sets the target that the entity is looking at.'''
        ...
    
    ...

class Light(Frustum):
    '''The light illuminates the scene.
    
    
    
    The formula to calculate the total attenuation of light is:
    ``A = ConstantAttenuation + (Dist * LinearAttenuation) + ((Dist^2) * QuadraticAttenuation)``'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def rotation_mode(self) -> aspose.threed.entities.RotationMode:
        ...
    
    @rotation_mode.setter
    def rotation_mode(self, value : aspose.threed.entities.RotationMode):
        ...
    
    @property
    def near_plane(self) -> float:
        ...
    
    @near_plane.setter
    def near_plane(self, value : float):
        ...
    
    @property
    def far_plane(self) -> float:
        ...
    
    @far_plane.setter
    def far_plane(self, value : float):
        ...
    
    @property
    def aspect(self) -> float:
        '''Gets the aspect ratio of the frustum'''
        ...
    
    @aspect.setter
    def aspect(self, value : float):
        '''Sets the aspect ratio of the frustum'''
        ...
    
    @property
    def ortho_height(self) -> float:
        ...
    
    @ortho_height.setter
    def ortho_height(self, value : float):
        ...
    
    @property
    def up(self) -> aspose.threed.utilities.Vector3:
        '''Gets the up direction of the camera'''
        ...
    
    @up.setter
    def up(self, value : aspose.threed.utilities.Vector3):
        '''Sets the up direction of the camera'''
        ...
    
    @property
    def look_at(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @look_at.setter
    def look_at(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def direction(self) -> aspose.threed.utilities.Vector3:
        '''Gets the direction that the camera is looking at.
        Changes on this property will also affects the :py:attr:`aspose.threed.entities.Frustum.look_at` and :py:attr:`aspose.threed.entities.Frustum.target`.'''
        ...
    
    @direction.setter
    def direction(self, value : aspose.threed.utilities.Vector3):
        '''Sets the direction that the camera is looking at.
        Changes on this property will also affects the :py:attr:`aspose.threed.entities.Frustum.look_at` and :py:attr:`aspose.threed.entities.Frustum.target`.'''
        ...
    
    @property
    def target(self) -> aspose.threed.Node:
        '''Gets the target that the camera is looking at.
        If the user supports this property, it should be prior to :py:attr:`aspose.threed.entities.Frustum.look_at` property.'''
        ...
    
    @target.setter
    def target(self, value : aspose.threed.Node):
        '''Sets the target that the camera is looking at.
        If the user supports this property, it should be prior to :py:attr:`aspose.threed.entities.Frustum.look_at` property.'''
        ...
    
    @property
    def color(self) -> aspose.threed.utilities.Vector3:
        '''Gets the light's color'''
        ...
    
    @color.setter
    def color(self, value : aspose.threed.utilities.Vector3):
        '''Sets the light's color'''
        ...
    
    @property
    def light_type(self) -> aspose.threed.entities.LightType:
        ...
    
    @light_type.setter
    def light_type(self, value : aspose.threed.entities.LightType):
        ...
    
    @property
    def cast_light(self) -> bool:
        ...
    
    @cast_light.setter
    def cast_light(self, value : bool):
        ...
    
    @property
    def intensity(self) -> float:
        '''Gets the light's intensity, default value is 100'''
        ...
    
    @intensity.setter
    def intensity(self, value : float):
        '''Sets the light's intensity, default value is 100'''
        ...
    
    @property
    def hot_spot(self) -> float:
        ...
    
    @hot_spot.setter
    def hot_spot(self, value : float):
        ...
    
    @property
    def falloff(self) -> float:
        '''Gets the falloff cone angle (in degrees).'''
        ...
    
    @falloff.setter
    def falloff(self, value : float):
        '''Sets the falloff cone angle (in degrees).'''
        ...
    
    @property
    def constant_attenuation(self) -> float:
        ...
    
    @constant_attenuation.setter
    def constant_attenuation(self, value : float):
        ...
    
    @property
    def linear_attenuation(self) -> float:
        ...
    
    @linear_attenuation.setter
    def linear_attenuation(self, value : float):
        ...
    
    @property
    def quadratic_attenuation(self) -> float:
        ...
    
    @quadratic_attenuation.setter
    def quadratic_attenuation(self, value : float):
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def shadow_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @shadow_color.setter
    def shadow_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    ...

class Line(Curve):
    '''A polyline is a path defined by a set of points with :py:attr:`aspose.threed.entities.Geometry.control_points`, and connected by :py:attr:`aspose.threed.entities.Line.segments`,
    which means it can also be a set of connected line segments.
    The line is usually a linear object, which means it cannot be used to represent a curve, in order to represent a curve, uses :py:class:`aspose.threed.entities.NurbsCurve`.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    @staticmethod
    def from_points(points : List[aspose.threed.utilities.Vector3]) -> aspose.threed.entities.Line:
        '''Construct a :py:class:`aspose.threed.entities.Line` instance from a set of points.'''
        ...
    
    def make_default_indices(self):
        '''Generate the sequence 0,1,2,3....:py:attr:`aspose.threed.entities.Geometry.control_points`.Length-1 to :py:attr:`aspose.threed.entities.Line.segments` so the ControlPoints can be used as a single line'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def color(self) -> aspose.threed.utilities.Vector3:
        '''Gets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @color.setter
    def color(self, value : aspose.threed.utilities.Vector3):
        '''Sets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @property
    def visible(self) -> bool:
        '''Gets if the geometry is visible'''
        ...
    
    @visible.setter
    def visible(self, value : bool):
        '''Sets if the geometry is visible'''
        ...
    
    @property
    def segments(self) -> List[List[int]]:
        '''Gets the segments of the line'''
        ...
    
    ...

class LinearExtrusion(aspose.threed.Entity):
    '''Linear extrusion takes a 2D shape as input and extends the shape in the 3rd dimension.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert the extrusion to mesh.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def shape(self) -> aspose.threed.profiles.Profile:
        '''The base shape to be extruded.'''
        ...
    
    @shape.setter
    def shape(self, value : aspose.threed.profiles.Profile):
        '''The base shape to be extruded.'''
        ...
    
    @property
    def direction(self) -> aspose.threed.utilities.Vector3:
        '''The direction of extrusion, default value is (0, 0, 1)'''
        ...
    
    @direction.setter
    def direction(self, value : aspose.threed.utilities.Vector3):
        '''The direction of extrusion, default value is (0, 0, 1)'''
        ...
    
    @property
    def height(self) -> float:
        '''The height of the extruded geometry, default value is 1.0'''
        ...
    
    @height.setter
    def height(self, value : float):
        '''The height of the extruded geometry, default value is 1.0'''
        ...
    
    @property
    def slices(self) -> int:
        '''The slices of the twisted extruded geometry, default value is 1.'''
        ...
    
    @slices.setter
    def slices(self, value : int):
        '''The slices of the twisted extruded geometry, default value is 1.'''
        ...
    
    @property
    def center(self) -> bool:
        '''If this value is false, the linear extrusion Z range is from 0 to height, otherwise the range is from -height/2 to height/2.'''
        ...
    
    @center.setter
    def center(self, value : bool):
        '''If this value is false, the linear extrusion Z range is from 0 to height, otherwise the range is from -height/2 to height/2.'''
        ...
    
    @property
    def twist_offset(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @twist_offset.setter
    def twist_offset(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def twist(self) -> float:
        '''The number of degrees of through which the shape is extruded.'''
        ...
    
    @twist.setter
    def twist(self, value : float):
        '''The number of degrees of through which the shape is extruded.'''
        ...
    
    ...

class Mesh(Geometry):
    '''A mesh is made of many n-sided polygons.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :returns: Created element.'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element.'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :returns: Created element uv'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element uv'''
        ...
    
    @overload
    def create_polygon(self, indices : List[int], offset : int, length : int):
        '''Creates a new polygon with all vertices defined in ``indices``.
        To create polygon vertex by vertex, please use :py:class:`aspose.threed.entities.PolygonBuilder`.
        
        :param indices: Array of the polygon indices, each index points to a control point that forms the polygon.
        :param offset: The offset of the first polygon index
        :param length: The length of the indices'''
        ...
    
    @overload
    def create_polygon(self, indices : List[int]):
        '''Creates a new polygon with all vertices defined in ``indices``.
        To create polygon vertex by vertex, please use :py:class:`aspose.threed.entities.PolygonBuilder`.
        
        :param indices: Array of the polygon indices, each index points to a control point that forms the polygon.'''
        ...
    
    @overload
    def create_polygon(self, v1 : int, v2 : int, v3 : int, v4 : int):
        '''Create a polygon with 4 vertices(quad)
        
        :param v1: Index of the first vertex
        :param v2: Index of the second vertex
        :param v3: Index of the third vertex
        :param v4: Index of the fourth vertex'''
        ...
    
    @overload
    def create_polygon(self, v1 : int, v2 : int, v3 : int):
        '''Create a polygon with 3 vertices(triangle)
        
        :param v1: Index of the first vertex
        :param v2: Index of the second vertex
        :param v3: Index of the third vertex'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def get_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Gets a vertex element with specified type
        
        :param type: which vertex element type to find
        :returns: :py:class:`aspose.threed.entities.VertexElement` instance if found, otherwise null will be returned.'''
        ...
    
    def get_vertex_element_of_uv(self, texture_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Gets a :py:class:`aspose.threed.entities.VertexElementUV` instance with given texture mapping type
        
        :returns: VertexElementUV with the texture mapping type'''
        ...
    
    def add_element(self, element : aspose.threed.entities.VertexElement):
        '''Adds an existing vertex element to current geometry
        
        :param element: The vertex element to add'''
        ...
    
    def get_polygon_size(self, index : int) -> int:
        '''Gets the vertex count of the specified polygon.
        
        :param index: Index.
        :returns: The polygon size.'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Gets the Mesh instance from current entity.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def visible(self) -> bool:
        '''Gets if the geometry is visible'''
        ...
    
    @visible.setter
    def visible(self, value : bool):
        '''Sets if the geometry is visible'''
        ...
    
    @property
    def deformers(self) -> List[aspose.threed.deformers.Deformer]:
        '''Gets all deformers associated with this geometry.'''
        ...
    
    @property
    def control_points(self) -> List[aspose.threed.utilities.Vector4]:
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def vertex_elements(self) -> List[aspose.threed.entities.VertexElement]:
        ...
    
    @property
    def edges(self) -> List[int]:
        '''Gets edges of the Mesh.  Edge is optional in mesh, so it can be empty.'''
        ...
    
    @property
    def polygon_count(self) -> int:
        ...
    
    @property
    def polygons(self) -> List[List[int]]:
        '''Gets the polygons definition of the mesh'''
        ...
    
    ...

class NurbsCurve(Curve):
    '''`NURBS curve <https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline>` is a curve represented by NURBS(Non-uniform rational basis spline),
    A NURBS curve is defined by its :py:attr:`aspose.threed.entities.NurbsCurve.order`, a set of weighted :py:attr:`aspose.threed.entities.Geometry.control_points` and a :py:attr:`aspose.threed.entities.NurbsCurve.KnotVectors`
    The w component in control point is used as control point's weight, whatever it is a :py:attr:`aspose.threed.entities.CurveDimension.TWO_DIMENSIONAL` or :py:attr:`aspose.threed.entities.CurveDimension.THREE_DIMENSIONAL`'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def evaluate(self, steps : int) -> List[aspose.threed.utilities.Vector4]:
        '''Evaluate the NURBS curve
        
        :param steps: The evaluation frequency between two neighbor knots, default value is 20
        :returns: Points in the curve'''
        ...
    
    def evaluate_at(self, u : float) -> aspose.threed.utilities.Vector4:
        '''Evaluate the curve's point at specified position
        
        :param u: The position in the curve, between 0 and 1'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def color(self) -> aspose.threed.utilities.Vector3:
        '''Gets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @color.setter
    def color(self, value : aspose.threed.utilities.Vector3):
        '''Sets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @property
    def order(self) -> int:
        '''Gets the order of a NURBS curve, it defines the number of nearby control points that influence any given point on the curve.'''
        ...
    
    @order.setter
    def order(self, value : int):
        '''Sets the order of a NURBS curve, it defines the number of nearby control points that influence any given point on the curve.'''
        ...
    
    @property
    def dimension(self) -> aspose.threed.entities.CurveDimension:
        '''Gets the curve's dimension.'''
        ...
    
    @dimension.setter
    def dimension(self, value : aspose.threed.entities.CurveDimension):
        '''Sets the curve's dimension.'''
        ...
    
    @property
    def curve_type(self) -> aspose.threed.entities.NurbsType:
        ...
    
    @curve_type.setter
    def curve_type(self, value : aspose.threed.entities.NurbsType):
        ...
    
    @property
    def rational(self) -> bool:
        '''Gets whether it is rational, this value indicates whether this :py:class:`aspose.threed.entities.NurbsCurve` is rational spline or non-rational spline.
        Non-rational B-spline is a special case of rational B-splines.'''
        ...
    
    @rational.setter
    def rational(self, value : bool):
        '''Sets whether it is rational, this value indicates whether this :py:class:`aspose.threed.entities.NurbsCurve` is rational spline or non-rational spline.
        Non-rational B-spline is a special case of rational B-splines.'''
        ...
    
    ...

class NurbsDirection:
    '''A 3D :py:class:`aspose.threed.entities.NurbsSurface` has two direction, the :py:attr:`aspose.threed.entities.NurbsSurface.u` and :py:attr:`aspose.threed.entities.NurbsSurface.v`, the :py:class:`aspose.threed.entities.NurbsDirection` defines data for each direction.
    A direction is actually a NURBS curve, that means it's also defined by its :py:attr:`aspose.threed.entities.NurbsDirection.order`, a :py:attr:`aspose.threed.entities.NurbsDirection.KnotVectors`, and a set of weighted control points(defined in :py:class:`aspose.threed.entities.NurbsSurface`).'''
    
    @property
    def order(self) -> int:
        '''Gets the order of a NURBS curve, it defines the number of nearby control points that influence any given point on the curve.'''
        ...
    
    @order.setter
    def order(self, value : int):
        '''Sets the order of a NURBS curve, it defines the number of nearby control points that influence any given point on the curve.'''
        ...
    
    @property
    def divisions(self) -> int:
        '''Gets the number of divisions between adjacent control points in current direction.'''
        ...
    
    @divisions.setter
    def divisions(self, value : int):
        '''Sets the number of divisions between adjacent control points in current direction.'''
        ...
    
    @property
    def type(self) -> aspose.threed.entities.NurbsType:
        '''Gets the type of the current direction.'''
        ...
    
    @type.setter
    def type(self, value : aspose.threed.entities.NurbsType):
        '''Sets the type of the current direction.'''
        ...
    
    @property
    def count(self) -> int:
        '''Gets the count of control points in current direction.'''
        ...
    
    @count.setter
    def count(self, value : int):
        '''Sets the count of control points in current direction.'''
        ...
    
    ...

class NurbsSurface(Geometry):
    ''':py:class:`aspose.threed.entities.NurbsSurface` is a surface represented by `NURBS(Non-uniform rational basis spline) <https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline>`,
    A :py:class:`aspose.threed.entities.NurbsSurface` is defined by two :py:class:`aspose.threed.entities.NurbsDirection`:py:attr:`aspose.threed.entities.NurbsSurface.u` and :py:attr:`aspose.threed.entities.NurbsSurface.v`.
    The w component in control point is used as control point's weight whatever the direction's type is a :py:attr:`aspose.threed.entities.CurveDimension.TWO_DIMENSIONAL` or :py:attr:`aspose.threed.entities.CurveDimension.THREE_DIMENSIONAL`'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :returns: Created element.'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element.'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :returns: Created element uv'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element uv'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def get_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Gets a vertex element with specified type
        
        :param type: which vertex element type to find
        :returns: :py:class:`aspose.threed.entities.VertexElement` instance if found, otherwise null will be returned.'''
        ...
    
    def get_vertex_element_of_uv(self, texture_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Gets a :py:class:`aspose.threed.entities.VertexElementUV` instance with given texture mapping type
        
        :returns: VertexElementUV with the texture mapping type'''
        ...
    
    def add_element(self, element : aspose.threed.entities.VertexElement):
        '''Adds an existing vertex element to current geometry
        
        :param element: The vertex element to add'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert the NURBS surface to the mesh'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def visible(self) -> bool:
        '''Gets if the geometry is visible'''
        ...
    
    @visible.setter
    def visible(self, value : bool):
        '''Sets if the geometry is visible'''
        ...
    
    @property
    def deformers(self) -> List[aspose.threed.deformers.Deformer]:
        '''Gets all deformers associated with this geometry.'''
        ...
    
    @property
    def control_points(self) -> List[aspose.threed.utilities.Vector4]:
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def vertex_elements(self) -> List[aspose.threed.entities.VertexElement]:
        ...
    
    @property
    def u(self) -> aspose.threed.entities.NurbsDirection:
        '''Gets the NURBS surface's U direction'''
        ...
    
    @property
    def v(self) -> aspose.threed.entities.NurbsDirection:
        '''Gets the NURBS surface's V direction'''
        ...
    
    ...

class Patch(Geometry):
    '''A :py:class:`aspose.threed.entities.Patch` is a parametric modeling surface, similar to :py:class:`aspose.threed.entities.NurbsSurface`, it's also defined by two
    :py:class:`aspose.threed.entities.PatchDirection`, the :py:attr:`aspose.threed.entities.Patch.u` and :py:attr:`aspose.threed.entities.Patch.v`.
    
    But difference between :py:class:`aspose.threed.entities.Patch` and :py:class:`aspose.threed.entities.NurbsSurface` is that the :py:class:`aspose.threed.entities.PatchDirection` curve
    can be one of :py:attr:`aspose.threed.entities.PatchDirectionType.BEZIER`, :py:attr:`aspose.threed.entities.PatchDirectionType.QUADRATIC_BEZIER`, :py:attr:`aspose.threed.entities.PatchDirectionType.BASIS_SPLINE`, :py:attr:`aspose.threed.entities.PatchDirectionType.CARDINAL_SPLINE` and :py:attr:`aspose.threed.entities.PatchDirectionType.LINEAR`'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :returns: Created element.'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element.'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :returns: Created element uv'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element uv'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def get_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Gets a vertex element with specified type
        
        :param type: which vertex element type to find
        :returns: :py:class:`aspose.threed.entities.VertexElement` instance if found, otherwise null will be returned.'''
        ...
    
    def get_vertex_element_of_uv(self, texture_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Gets a :py:class:`aspose.threed.entities.VertexElementUV` instance with given texture mapping type
        
        :returns: VertexElementUV with the texture mapping type'''
        ...
    
    def add_element(self, element : aspose.threed.entities.VertexElement):
        '''Adds an existing vertex element to current geometry
        
        :param element: The vertex element to add'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def visible(self) -> bool:
        '''Gets if the geometry is visible'''
        ...
    
    @visible.setter
    def visible(self, value : bool):
        '''Sets if the geometry is visible'''
        ...
    
    @property
    def deformers(self) -> List[aspose.threed.deformers.Deformer]:
        '''Gets all deformers associated with this geometry.'''
        ...
    
    @property
    def control_points(self) -> List[aspose.threed.utilities.Vector4]:
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def vertex_elements(self) -> List[aspose.threed.entities.VertexElement]:
        ...
    
    @property
    def u(self) -> aspose.threed.entities.PatchDirection:
        '''Gets the u direction.'''
        ...
    
    @property
    def v(self) -> aspose.threed.entities.PatchDirection:
        '''Gets the v direction.'''
        ...
    
    ...

class PatchDirection:
    '''Patch's U and V direction.'''
    
    @property
    def type(self) -> aspose.threed.entities.PatchDirectionType:
        '''Gets the patch's type.'''
        ...
    
    @type.setter
    def type(self, value : aspose.threed.entities.PatchDirectionType):
        '''Sets the patch's type.'''
        ...
    
    @property
    def divisions(self) -> int:
        '''Gets the number of divisions between adjacent control points.'''
        ...
    
    @divisions.setter
    def divisions(self, value : int):
        '''Sets the number of divisions between adjacent control points.'''
        ...
    
    @property
    def control_points(self) -> int:
        ...
    
    @control_points.setter
    def control_points(self, value : int):
        ...
    
    @property
    def closed(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.threed.entities.PatchDirection` is a closed curve.'''
        ...
    
    @closed.setter
    def closed(self, value : bool):
        '''Sets a value indicating whether this :py:class:`aspose.threed.entities.PatchDirection` is a closed curve.'''
        ...
    
    ...

class Plane(Primitive):
    '''Parameterized plane.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert current object to mesh
        
        :returns: The mesh.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def up(self) -> aspose.threed.utilities.Vector3:
        '''Gets the up vector of the plane, default value is (0, 1, 0), this affects the generation of the plane'''
        ...
    
    @up.setter
    def up(self, value : aspose.threed.utilities.Vector3):
        '''Sets the up vector of the plane, default value is (0, 1, 0), this affects the generation of the plane'''
        ...
    
    @property
    def length(self) -> float:
        '''Gets the length of the plane.'''
        ...
    
    @length.setter
    def length(self, value : float):
        '''Sets the length of the plane.'''
        ...
    
    @property
    def width(self) -> float:
        '''Gets the width of the plane.'''
        ...
    
    @width.setter
    def width(self, value : float):
        '''Sets the width of the plane.'''
        ...
    
    @property
    def length_segments(self) -> int:
        ...
    
    @length_segments.setter
    def length_segments(self, value : int):
        ...
    
    @property
    def width_segments(self) -> int:
        ...
    
    @width_segments.setter
    def width_segments(self, value : int):
        ...
    
    ...

class PointCloud(Geometry):
    '''The point cloud contains no topology information but only the control points and the vertex elements.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :returns: Created element.'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element.'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :returns: Created element uv'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element uv'''
        ...
    
    @overload
    @staticmethod
    def from_geometry(g : aspose.threed.entities.Geometry) -> aspose.threed.entities.PointCloud:
        '''Create a new PointCloud instance from a geometry object'''
        ...
    
    @overload
    @staticmethod
    def from_geometry(g : aspose.threed.entities.Geometrydensity : int) -> aspose.threed.entities.PointCloud:
        '''Create a new point cloud instance from a geometry object.
        Density is the number of points per unit triangle(Unit triangle are the triangle with maximum surface area from the mesh)
        
        :param g: Mesh or other geometry instance
        :param density: Number of points per unit triangle'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def get_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Gets a vertex element with specified type
        
        :param type: which vertex element type to find
        :returns: :py:class:`aspose.threed.entities.VertexElement` instance if found, otherwise null will be returned.'''
        ...
    
    def get_vertex_element_of_uv(self, texture_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Gets a :py:class:`aspose.threed.entities.VertexElementUV` instance with given texture mapping type
        
        :returns: VertexElementUV with the texture mapping type'''
        ...
    
    def add_element(self, element : aspose.threed.entities.VertexElement):
        '''Adds an existing vertex element to current geometry
        
        :param element: The vertex element to add'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def visible(self) -> bool:
        '''Gets if the geometry is visible'''
        ...
    
    @visible.setter
    def visible(self, value : bool):
        '''Sets if the geometry is visible'''
        ...
    
    @property
    def deformers(self) -> List[aspose.threed.deformers.Deformer]:
        '''Gets all deformers associated with this geometry.'''
        ...
    
    @property
    def control_points(self) -> List[aspose.threed.utilities.Vector4]:
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def vertex_elements(self) -> List[aspose.threed.entities.VertexElement]:
        ...
    
    ...

class PolygonBuilder:
    '''A helper class to build polygon for :py:class:`aspose.threed.entities.Mesh`'''
    
    def begin(self):
        '''Begins to add a new polygon'''
        ...
    
    def add_vertex(self, index : int):
        '''Adds a vertex index to the polygon'''
        ...
    
    def end(self):
        '''Finishes the polygon creation'''
        ...
    
    ...

class PolygonModifier:
    '''Utilities to modify polygons'''
    
    @overload
    @staticmethod
    def triangulate(scene : aspose.threed.Scene):
        '''Convert all polygon-based meshes into full triangle mesh
        
        :param scene: The scene to process'''
        ...
    
    @overload
    @staticmethod
    def triangulate(mesh : aspose.threed.entities.Mesh) -> aspose.threed.entities.Mesh:
        '''Convert a polygon-based mesh into full triangle mesh
        
        :param mesh: The original non-triangle mesh
        :returns: The generated new triangle mesh'''
        ...
    
    @overload
    @staticmethod
    def triangulate(control_points : List[aspose.threed.utilities.Vector4]polygons : List[List[int]], generate_normals : bool, nor_out : Any) -> List[List[int]]:
        ...
    
    @overload
    @staticmethod
    def triangulate(control_points : List[aspose.threed.utilities.Vector4]polygons : List[List[int]]) -> List[List[int]]:
        ...
    
    @overload
    @staticmethod
    def triangulate(control_points : List[aspose.threed.utilities.Vector4]polygon : List[int]) -> List[List[int]]:
        ...
    
    @overload
    @staticmethod
    def triangulate(control_points : List[aspose.threed.utilities.Vector4]) -> List[List[int]]:
        ...
    
    @overload
    @staticmethod
    def merge_mesh(scene : aspose.threed.Scene) -> aspose.threed.entities.Mesh:
        '''Convert a whole scene to a single transformed mesh
        Vertex elements like normal/texture coordinates are not supported yet
        
        :param scene: The scene to merge
        :returns: The merged mesh'''
        ...
    
    @overload
    @staticmethod
    def merge_mesh(nodes : List[aspose.threed.Node]) -> aspose.threed.entities.Mesh:
        ...
    
    @overload
    @staticmethod
    def merge_mesh(node : aspose.threed.Node) -> aspose.threed.entities.Mesh:
        '''Convert a whole node to a single transformed mesh
        Vertex elements like normal/texture coordinates are not supported yet
        
        :param node: The node to merge
        :returns: Merged mesh'''
        ...
    
    @overload
    @staticmethod
    def scale(scene : aspose.threed.Scenescale : aspose.threed.utilities.Vector3) -> aspose.threed.Scene:
        '''Scale all geometries(Scale the control points not the transformation matrix) in this scene
        
        :param scene: The scene to scale
        :param scale: The scale factor'''
        ...
    
    @overload
    @staticmethod
    def scale(node : aspose.threed.Nodescale : aspose.threed.utilities.Vector3):
        '''Scale all geometries(Scale the control points not the transformation matrix) in this node
        
        :param node: The node to scale
        :param scale: The scale factor'''
        ...
    
    @overload
    @staticmethod
    def generate_uv(mesh : aspose.threed.entities.Meshnormals : aspose.threed.entities.VertexElementNormal) -> aspose.threed.entities.VertexElementUV:
        '''Generate UV data from the given input mesh and specified normal data.
        
        :param mesh: The input mesh
        :param normals: The normal data
        :returns: Generated UV data'''
        ...
    
    @overload
    @staticmethod
    def generate_uv(mesh : aspose.threed.entities.Mesh) -> aspose.threed.entities.VertexElementUV:
        '''Generate UV data from the given input mesh
        
        :param mesh: The input mesh
        :returns: Generated UV data'''
        ...
    
    @overload
    @staticmethod
    def split_mesh(node : aspose.threed.Nodepolicy : aspose.threed.entities.SplitMeshPolicy, create_child_nodes : bool, remove_old_mesh : bool):
        '''Split mesh into sub-meshes by :py:class:`aspose.threed.entities.VertexElementMaterial`.
        Each sub-mesh will use only one material.
        Perform mesh splitting on a node
        
        :param create_child_nodes: Create child nodes for each sub-mesh.
        :param remove_old_mesh: Remove the old mesh after split, if this parameter is false, the old and new meshes will co-exists.'''
        ...
    
    @overload
    @staticmethod
    def split_mesh(scene : aspose.threed.Scenepolicy : aspose.threed.entities.SplitMeshPolicy, remove_old_mesh : bool):
        '''Split mesh into sub-meshes by :py:class:`aspose.threed.entities.VertexElementMaterial`.
        Each sub-mesh will use only one material.
        Perform mesh splitting on all nodes of the scene.'''
        ...
    
    @overload
    @staticmethod
    def split_mesh(mesh : aspose.threed.entities.Meshpolicy : aspose.threed.entities.SplitMeshPolicy) -> List[aspose.threed.entities.Mesh]:
        '''Split mesh into sub-meshes by :py:class:`aspose.threed.entities.VertexElementMaterial`.
        Each sub-mesh will use only one material.
        The original mesh will not get changed.'''
        ...
    
    @overload
    @staticmethod
    def build_tangent_binormal(scene : aspose.threed.Scene):
        '''This will create tangent and binormal on all meshes of the scene
        Normal is required, if normal is not existing on the mesh, it will also create the normal data from position.
        UV is also required, the mesh will be ignored if no UV is defined.'''
        ...
    
    @overload
    @staticmethod
    def build_tangent_binormal(mesh : aspose.threed.entities.Mesh):
        '''This will create tangent and binormal on the mesh
        Normal is required, if normal is not existing on the mesh, it will also create the normal data from position.
        UV is also required, an exception will be raised if no UV found.'''
        ...
    
    @staticmethod
    def generate_normal(mesh : aspose.threed.entities.Mesh) -> aspose.threed.entities.VertexElementNormal:
        '''Generate normal data from Mesh definition'''
        ...
    
    ...

class Primitive(aspose.threed.Entity):
    '''Base class for all primitives'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert current object to mesh
        
        :returns: The mesh.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    ...

class Pyramid(Primitive):
    '''Parameterized pyramid.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert current object to mesh
        
        :returns: The mesh.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def bottom_area(self) -> aspose.threed.utilities.Vector2:
        ...
    
    @bottom_area.setter
    def bottom_area(self, value : aspose.threed.utilities.Vector2):
        ...
    
    @property
    def top_area(self) -> aspose.threed.utilities.Vector2:
        ...
    
    @top_area.setter
    def top_area(self, value : aspose.threed.utilities.Vector2):
        ...
    
    @property
    def bottom_offset(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @bottom_offset.setter
    def bottom_offset(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def height(self) -> float:
        '''Height of the pyramid'''
        ...
    
    @height.setter
    def height(self, value : float):
        '''Height of the pyramid'''
        ...
    
    ...

class RectangularTorus(Primitive):
    '''Parameterized rectangular torus.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert this primitive to :py:class:`aspose.threed.entities.Mesh`'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def inner_radius(self) -> float:
        ...
    
    @inner_radius.setter
    def inner_radius(self, value : float):
        ...
    
    @property
    def outer_radius(self) -> float:
        ...
    
    @outer_radius.setter
    def outer_radius(self, value : float):
        ...
    
    @property
    def height(self) -> float:
        '''The height of the rectangular torus.
        Default value is 20'''
        ...
    
    @height.setter
    def height(self, value : float):
        '''The height of the rectangular torus.
        Default value is 20'''
        ...
    
    @property
    def arc(self) -> float:
        '''The total angle of the arc, measured in radian.
        Default value is PI'''
        ...
    
    @arc.setter
    def arc(self, value : float):
        '''The total angle of the arc, measured in radian.
        Default value is PI'''
        ...
    
    @property
    def angle_start(self) -> float:
        ...
    
    @angle_start.setter
    def angle_start(self, value : float):
        ...
    
    @property
    def radial_segments(self) -> int:
        ...
    
    @radial_segments.setter
    def radial_segments(self, value : int):
        ...
    
    ...

class RevolvedAreaSolid(aspose.threed.Entity):
    '''This class represents a solid model by revolving a cross section provided by a profile about an axis.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert the :py:class:`aspose.threed.entities.RevolvedAreaSolid` into a mesh.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def angle_start(self) -> float:
        ...
    
    @angle_start.setter
    def angle_start(self, value : float):
        ...
    
    @property
    def angle_end(self) -> float:
        ...
    
    @angle_end.setter
    def angle_end(self, value : float):
        ...
    
    @property
    def axis(self) -> aspose.threed.utilities.Vector3:
        '''Gets the axis direction, default value is (0, 1, 0).'''
        ...
    
    @axis.setter
    def axis(self, value : aspose.threed.utilities.Vector3):
        '''Sets the axis direction, default value is (0, 1, 0).'''
        ...
    
    @property
    def origin(self) -> aspose.threed.utilities.Vector3:
        '''Gets the origin point of the revolving, default value is (0, 0, 0).'''
        ...
    
    @origin.setter
    def origin(self, value : aspose.threed.utilities.Vector3):
        '''Sets the origin point of the revolving, default value is (0, 0, 0).'''
        ...
    
    @property
    def shape(self) -> aspose.threed.profiles.Profile:
        '''Gets the base profile used to revolve.'''
        ...
    
    @shape.setter
    def shape(self, value : aspose.threed.profiles.Profile):
        '''Sets the base profile used to revolve.'''
        ...
    
    ...

class Shape(Geometry):
    '''The shape describes the deformation on a set of control points, which is similar to the cluster deformer in Maya.
    For example, we can add a shape to a created geometry.
    And the shape and the geometry have the same topological information but different position of the control points.
    With varying amounts of influence, the geometry performs a deformation effect.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :returns: Created element.'''
        ...
    
    @overload
    def create_element(self, type : aspose.threed.entities.VertexElementType, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElement:
        '''Creates a vertex element with specified type and add it to the geometry.
        
        :param type: Vertex element type
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element.'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :returns: Created element uv'''
        ...
    
    @overload
    def create_element_uv(self, uv_mapping : aspose.threed.entities.TextureMapping, mapping_mode : aspose.threed.entities.MappingMode, reference_mode : aspose.threed.entities.ReferenceMode) -> aspose.threed.entities.VertexElementUV:
        '''Creates a :py:class:`aspose.threed.entities.VertexElementUV` with given texture mapping type.
        
        :param uv_mapping: Which texture mapping type to create
        :param mapping_mode: Default mapping mode
        :param reference_mode: Default reference mode
        :returns: Created element uv'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def get_element(self, type : aspose.threed.entities.VertexElementType) -> aspose.threed.entities.VertexElement:
        '''Gets a vertex element with specified type
        
        :param type: which vertex element type to find
        :returns: :py:class:`aspose.threed.entities.VertexElement` instance if found, otherwise null will be returned.'''
        ...
    
    def get_vertex_element_of_uv(self, texture_mapping : aspose.threed.entities.TextureMapping) -> aspose.threed.entities.VertexElementUV:
        '''Gets a :py:class:`aspose.threed.entities.VertexElementUV` instance with given texture mapping type
        
        :returns: VertexElementUV with the texture mapping type'''
        ...
    
    def add_element(self, element : aspose.threed.entities.VertexElement):
        '''Adds an existing vertex element to current geometry
        
        :param element: The vertex element to add'''
        ...
    
    @staticmethod
    def from_control_points(control_points : List[aspose.threed.utilities.Vector3]) -> aspose.threed.entities.Shape:
        '''Create a shape with specified control points with a default indices.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def visible(self) -> bool:
        '''Gets if the geometry is visible'''
        ...
    
    @visible.setter
    def visible(self, value : bool):
        '''Sets if the geometry is visible'''
        ...
    
    @property
    def deformers(self) -> List[aspose.threed.deformers.Deformer]:
        '''Gets all deformers associated with this geometry.'''
        ...
    
    @property
    def control_points(self) -> List[aspose.threed.utilities.Vector4]:
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def vertex_elements(self) -> List[aspose.threed.entities.VertexElement]:
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices.'''
        ...
    
    ...

class Skeleton(aspose.threed.Entity):
    '''The :py:class:`aspose.threed.entities.Skeleton` is mainly used by CAD software to help designer to manipulate the transformation of skeletal structure, it's usually useless outside the CAD softwares.
    To make the skeleton hierarchy acts like one object in CAD software, it's necessary to mark the top :py:class:`aspose.threed.entities.Skeleton` node as the root one by setting :py:attr:`aspose.threed.entities.Skeleton.type` to :py:attr:`aspose.threed.entities.SkeletonType.SKELETON`,
    and all children set to :py:attr:`aspose.threed.entities.SkeletonType.BONE`'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def size(self) -> float:
        '''Gets the limb node size that used in CAD software to represent the size of the bone.'''
        ...
    
    @size.setter
    def size(self, value : float):
        '''Sets the limb node size that used in CAD software to represent the size of the bone.'''
        ...
    
    @property
    def type(self) -> aspose.threed.entities.SkeletonType:
        '''Gets the type of the skeleton.'''
        ...
    
    @type.setter
    def type(self, value : aspose.threed.entities.SkeletonType):
        '''Sets the type of the skeleton.'''
        ...
    
    ...

class Sphere(Primitive):
    '''Parameterized sphere.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert current object to mesh
        
        :returns: The mesh.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def width_segments(self) -> int:
        ...
    
    @width_segments.setter
    def width_segments(self, value : int):
        ...
    
    @property
    def height_segments(self) -> int:
        ...
    
    @height_segments.setter
    def height_segments(self, value : int):
        ...
    
    @property
    def phi_start(self) -> float:
        ...
    
    @phi_start.setter
    def phi_start(self, value : float):
        ...
    
    @property
    def phi_length(self) -> float:
        ...
    
    @phi_length.setter
    def phi_length(self, value : float):
        ...
    
    @property
    def theta_start(self) -> float:
        ...
    
    @theta_start.setter
    def theta_start(self, value : float):
        ...
    
    @property
    def theta_length(self) -> float:
        ...
    
    @theta_length.setter
    def theta_length(self, value : float):
        ...
    
    @property
    def radius(self) -> float:
        '''Gets the radius of the sphere.'''
        ...
    
    @radius.setter
    def radius(self, value : float):
        '''Sets the radius of the sphere.'''
        ...
    
    ...

class SweptAreaSolid(aspose.threed.Entity):
    '''A :py:class:`aspose.threed.entities.SweptAreaSolid` constructs a geometry by sweeping a profile along a directrix.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert current object to mesh
        
        :returns: The mesh.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def shape(self) -> aspose.threed.profiles.Profile:
        '''The base profile to construct the geometry.'''
        ...
    
    @shape.setter
    def shape(self, value : aspose.threed.profiles.Profile):
        '''The base profile to construct the geometry.'''
        ...
    
    @property
    def directrix(self) -> aspose.threed.entities.Curve:
        '''The directrix that the swept area sweeping along with.'''
        ...
    
    @directrix.setter
    def directrix(self, value : aspose.threed.entities.Curve):
        '''The directrix that the swept area sweeping along with.'''
        ...
    
    @property
    def start_point(self) -> aspose.threed.entities.EndPoint:
        ...
    
    @start_point.setter
    def start_point(self, value : aspose.threed.entities.EndPoint):
        ...
    
    @property
    def end_point(self) -> aspose.threed.entities.EndPoint:
        ...
    
    @end_point.setter
    def end_point(self, value : aspose.threed.entities.EndPoint):
        ...
    
    ...

class Torus(Primitive):
    '''Parameterized torus.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    def to_mesh(self) -> aspose.threed.entities.Mesh:
        '''Convert current object to mesh
        
        :returns: The mesh.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def cast_shadows(self) -> bool:
        ...
    
    @cast_shadows.setter
    def cast_shadows(self, value : bool):
        ...
    
    @property
    def receive_shadows(self) -> bool:
        ...
    
    @receive_shadows.setter
    def receive_shadows(self, value : bool):
        ...
    
    @property
    def radius(self) -> float:
        '''Gets the radius of the torus.'''
        ...
    
    @radius.setter
    def radius(self, value : float):
        '''Sets the radius of the torus.'''
        ...
    
    @property
    def tube(self) -> float:
        '''Gets the radius of the tube.'''
        ...
    
    @tube.setter
    def tube(self, value : float):
        '''Sets the radius of the tube.'''
        ...
    
    @property
    def radial_segments(self) -> int:
        ...
    
    @radial_segments.setter
    def radial_segments(self, value : int):
        ...
    
    @property
    def tubular_segments(self) -> int:
        ...
    
    @tubular_segments.setter
    def tubular_segments(self, value : int):
        ...
    
    @property
    def arc(self) -> float:
        '''Gets the arc.'''
        ...
    
    @arc.setter
    def arc(self, value : float):
        '''Sets the arc.'''
        ...
    
    ...

class TransformedCurve(Curve):
    '''A :py:class:`aspose.threed.entities.TransformedCurve` gives a curve a placement by using a transformation matrix.
    This allows to perform a transformation inside a :py:class:`aspose.threed.entities.TrimmedCurve` or :py:class:`aspose.threed.entities.CompositeCurve`.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def color(self) -> aspose.threed.utilities.Vector3:
        '''Gets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @color.setter
    def color(self, value : aspose.threed.utilities.Vector3):
        '''Sets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @property
    def transform_matrix(self) -> aspose.threed.utilities.Matrix4:
        ...
    
    @transform_matrix.setter
    def transform_matrix(self, value : aspose.threed.utilities.Matrix4):
        ...
    
    @property
    def basis_curve(self) -> aspose.threed.entities.Curve:
        ...
    
    @basis_curve.setter
    def basis_curve(self, value : aspose.threed.entities.Curve):
        ...
    
    ...

class TriMesh(aspose.threed.Entity):
    '''A TriMesh contains raw data that can be used by GPU directly.
    This class is a utility to help to construct a mesh that only contains per-vertex data.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    @overload
    @staticmethod
    def from_mesh(declaration : aspose.threed.utilities.VertexDeclarationmesh : aspose.threed.entities.Mesh) -> aspose.threed.entities.TriMesh:
        '''Create a TriMesh from given mesh object with given vertex layout.'''
        ...
    
    @overload
    @staticmethod
    def from_mesh(mesh : aspose.threed.entities.Meshuse_float : bool) -> aspose.threed.entities.TriMesh:
        '''Create a TriMesh from given mesh object, the vertex declaration are based on the input mesh's structure.
        
        :param use_float: Use float type instead of double type for each vertex element component.
        :returns: The :py:class:`aspose.threed.entities.TriMesh` generated from given :py:class:`aspose.threed.entities.Mesh`'''
        ...
    
    @overload
    def indices_to_array(self, result : Any):
        ...
    
    @overload
    def indices_to_array(self, result : Any):
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    @staticmethod
    def copy_from(input : aspose.threed.entities.TriMeshvd : aspose.threed.utilities.VertexDeclaration) -> aspose.threed.entities.TriMesh:
        '''Copy the :py:class:`aspose.threed.entities.TriMesh` from input with new vertex layout
        
        :param input: The input TriMesh for copying
        :param vd: The new vertex declaration of the output TriMesh
        :returns: A new TriMesh instance with new vertex declaration.'''
        ...
    
    def begin_vertex(self) -> aspose.threed.utilities.Vertex:
        '''Begin adding vertex
        
        :returns: The reference of internal vertex object in type :py:class:`aspose.threed.utilities.Vertex`'''
        ...
    
    def end_vertex(self):
        '''End adding vertex'''
        ...
    
    def write_vertices_to(self, stream : io.RawIOBase):
        '''Write vertices data to the specified stream
        
        :param stream: The stream that the vertices data will be written to'''
        ...
    
    def write_16b_indices_to(self, stream : io.RawIOBase):
        '''Write the indices data as 16bit integer to the stream'''
        ...
    
    def write_32b_indices_to(self, stream : io.RawIOBase):
        '''Write the indices data as 32bit integer to the stream'''
        ...
    
    def vertices_to_array(self) -> bytes:
        '''Convert the vertices data to byte array'''
        ...
    
    @staticmethod
    def from_raw_data(vd : aspose.threed.utilities.VertexDeclarationvertices : bytes, indices : List[int], generate_vertex_mapping : bool) -> aspose.threed.entities.TriMesh:
        '''Create TriMesh from raw data
        
        :param vd: Vertex declaration, must contains at least one field.
        :param vertices: The input vertex data, the minimum length of the vertices must be greater or equal to vertex declaration's size
        :param indices: The triangle indices
        :param generate_vertex_mapping: Generate :py:class:`aspose.threed.utilities.Vertex` for each vertex, which is not necessary for just serialization/deserialization.
        :returns: The :py:class:`aspose.threed.entities.TriMesh` instance that encapsulated the input byte array.'''
        ...
    
    def load_vertices_from_bytes(self, vertices_in_bytes : bytes):
        '''Load vertices from bytes, the length of bytes must be an integer multiple of vertex size.'''
        ...
    
    def read_vector4(self, idx : int, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.Vector4:
        '''Read the vector4 field
        
        :param idx: The index of vertex to read
        :param field: The field with a Vector4/FVector4 data type'''
        ...
    
    def read_f_vector4(self, idx : int, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.FVector4:
        '''Read the vector4 field
        
        :param idx: The index of vertex to read
        :param field: The field with a Vector4/FVector4 data type'''
        ...
    
    def read_vector3(self, idx : int, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.Vector3:
        '''Read the vector3 field
        
        :param idx: The index of vertex to read
        :param field: The field with a Vector3/FVector3 data type'''
        ...
    
    def read_f_vector3(self, idx : int, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.FVector3:
        '''Read the vector3 field
        
        :param idx: The index of vertex to read
        :param field: The field with a Vector3/FVector3 data type'''
        ...
    
    def read_vector2(self, idx : int, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.Vector2:
        '''Read the vector2 field
        
        :param idx: The index of vertex to read
        :param field: The field with a Vector2/FVector2 data type'''
        ...
    
    def read_f_vector2(self, idx : int, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.FVector2:
        '''Read the vector2 field
        
        :param idx: The index of vertex to read
        :param field: The field with a Vector2/FVector2 data type'''
        ...
    
    def read_double(self, idx : int, field : aspose.threed.utilities.VertexField) -> float:
        '''Read the double field
        
        :param idx: The index of vertex to read
        :param field: The field with a float/double compatible data type'''
        ...
    
    def read_float(self, idx : int, field : aspose.threed.utilities.VertexField) -> float:
        '''Read the float field
        
        :param idx: The index of vertex to read
        :param field: The field with a float/double compatible data type'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def vertex_declaration(self) -> aspose.threed.utilities.VertexDeclaration:
        ...
    
    @property
    def vertices_count(self) -> int:
        ...
    
    @property
    def indices_count(self) -> int:
        ...
    
    @property
    def unmerged_vertices_count(self) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        '''The capacity of pre-allocated vertices.'''
        ...
    
    @property
    def vertices_size_in_bytes(self) -> int:
        ...
    
    ...

class TrimmedCurve(Curve):
    '''A bounded curve that trimmed the basis curve at both ends.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def color(self) -> aspose.threed.utilities.Vector3:
        '''Gets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @color.setter
    def color(self, value : aspose.threed.utilities.Vector3):
        '''Sets the color of the line, default value is white(1, 1, 1)'''
        ...
    
    @property
    def basis_curve(self) -> aspose.threed.entities.Curve:
        ...
    
    @basis_curve.setter
    def basis_curve(self, value : aspose.threed.entities.Curve):
        ...
    
    @property
    def first(self) -> aspose.threed.entities.EndPoint:
        '''The first end point to trim, can be a Cartesian point or a real parameter.'''
        ...
    
    @first.setter
    def first(self, value : aspose.threed.entities.EndPoint):
        '''The first end point to trim, can be a Cartesian point or a real parameter.'''
        ...
    
    @property
    def second(self) -> aspose.threed.entities.EndPoint:
        '''The second end point to trim, can be a Cartesian point or a real parameter.'''
        ...
    
    @second.setter
    def second(self, value : aspose.threed.entities.EndPoint):
        '''The second end point to trim, can be a Cartesian point or a real parameter.'''
        ...
    
    @property
    def same_direction(self) -> bool:
        ...
    
    @same_direction.setter
    def same_direction(self, value : bool):
        ...
    
    ...

class VertexElement(IIndexedVertexElement):
    '''Base class of vertex elements.
    A vertex element type is identified by VertexElementType.
    A VertexElement describes how the vertex element is mapped to a geometry surface and how the mapping information is arranged in memory.
    A VertexElement contains Normals, UVs or other kind of information.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Clears all the data from this vertex element.'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    ...

class VertexElementBinormal(VertexElementVector4):
    '''Defines the binormal vectors for specified components.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementVector4):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[aspose.threed.utilities.Vector4]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    @property
    def data(self) -> List[aspose.threed.utilities.Vector4]:
        '''Gets the vertex data'''
        ...
    
    ...

class VertexElementDoublesTemplate(VertexElement):
    '''A helper class for defining concrete :py:class:`aspose.threed.entities.VertexElement` implementations.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementDoublesTemplate):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[float]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    ...

class VertexElementEdgeCrease(VertexElementDoublesTemplate):
    '''Defines the edge crease for specified components'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementDoublesTemplate):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[float]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    ...

class VertexElementHole(VertexElement):
    '''Defines if specified polygon is hole'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Clears all the data from this vertex element.'''
        ...
    
    def set_data(self, data : List[bool]):
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    ...

class VertexElementIntsTemplate(VertexElement):
    '''A helper class for defining concrete :py:class:`aspose.threed.entities.VertexElement` implementations.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementIntsTemplate):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[int]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    @property
    def data(self) -> List[int]:
        '''Gets the vertex data'''
        ...
    
    ...

class VertexElementMaterial(VertexElement):
    '''Defines material index for specified components.
    
    A node can have multiple materials, the :py:class:`aspose.threed.entities.VertexElementMaterial` is used to render different part of the geometry in different materials.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    ...

class VertexElementNormal(VertexElementVector4):
    '''Defines normal vectors for specified components.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementVector4):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[aspose.threed.utilities.Vector4]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    @property
    def data(self) -> List[aspose.threed.utilities.Vector4]:
        '''Gets the vertex data'''
        ...
    
    ...

class VertexElementPolygonGroup(VertexElementIntsTemplate):
    '''Defines polygon group for specified components to group related polygons together.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementIntsTemplate):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[int]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    @property
    def data(self) -> List[int]:
        '''Gets the vertex data'''
        ...
    
    ...

class VertexElementSmoothingGroup(VertexElementIntsTemplate):
    '''A smoothing group is a group of polygons in a polygon mesh which should appear to form a smooth surface.
    Some early 3d modeling software like 3D studio max for DOS used smoothing group to void storing normal vector for each mesh vertex.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementIntsTemplate):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[int]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    @property
    def data(self) -> List[int]:
        '''Gets the vertex data'''
        ...
    
    ...

class VertexElementSpecular(VertexElementVector4):
    '''Defines specular color for specified components.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementVector4):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[aspose.threed.utilities.Vector4]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    @property
    def data(self) -> List[aspose.threed.utilities.Vector4]:
        '''Gets the vertex data'''
        ...
    
    ...

class VertexElementTangent(VertexElementVector4):
    '''Defines tangent vectors for specified components.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementVector4):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[aspose.threed.utilities.Vector4]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    @property
    def data(self) -> List[aspose.threed.utilities.Vector4]:
        '''Gets the vertex data'''
        ...
    
    ...

class VertexElementUV(VertexElementVector4):
    '''Defines the UV coordinates for specified components.
    A geometry can have multiple :py:class:`aspose.threed.entities.VertexElementUV` elements, and each one have different :py:class:`aspose.threed.entities.TextureMapping`s.'''
    
    @overload
    def add_data(self, data : Iterable[aspose.threed.utilities.Vector2]):
        ...
    
    @overload
    def add_data(self, data : Iterable[aspose.threed.utilities.Vector3]):
        ...
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementVector4):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[aspose.threed.utilities.Vector4]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    @property
    def data(self) -> List[aspose.threed.utilities.Vector4]:
        '''Gets the vertex data'''
        ...
    
    ...

class VertexElementUserData(VertexElement):
    '''Defines custom user data for specified components.
    Usually it's application-specific data for special purpose.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Clears all the data from this vertex element.'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    @property
    def data(self) -> any:
        '''The user data attached in this element'''
        ...
    
    @data.setter
    def data(self, value : any):
        '''The user data attached in this element'''
        ...
    
    ...

class VertexElementVector4(VertexElement):
    '''A helper class for defining concrete :py:class:`aspose.threed.entities.VertexElement` implementations.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementVector4):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[aspose.threed.utilities.Vector4]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    @property
    def data(self) -> List[aspose.threed.utilities.Vector4]:
        '''Gets the vertex data'''
        ...
    
    ...

class VertexElementVertexColor(VertexElementVector4):
    '''Defines the vertex color for specified components'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementVector4):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[aspose.threed.utilities.Vector4]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    @property
    def data(self) -> List[aspose.threed.utilities.Vector4]:
        '''Gets the vertex data'''
        ...
    
    ...

class VertexElementVertexCrease(VertexElementDoublesTemplate):
    '''Defines the vertex crease for specified components'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementDoublesTemplate):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[float]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    ...

class VertexElementVisibility(VertexElement):
    '''Defines if specified components is visible'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Clears all the data from this vertex element.'''
        ...
    
    def set_data(self, data : List[bool]):
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    ...

class VertexElementWeight(VertexElementDoublesTemplate):
    '''Defines blend weight for specified components.'''
    
    def set_indices(self, data : List[int]):
        '''Load indices'''
        ...
    
    def clear(self):
        '''Removes all elements from the direct and the index arrays.'''
        ...
    
    def copy_to(self, target : aspose.threed.entities.VertexElementDoublesTemplate):
        '''Copies data to specified element
        
        :param target: Target.'''
        ...
    
    def set_data(self, data : List[float]):
        '''Load data'''
        ...
    
    @property
    def vertex_element_type(self) -> aspose.threed.entities.VertexElementType:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def mapping_mode(self) -> aspose.threed.entities.MappingMode:
        ...
    
    @mapping_mode.setter
    def mapping_mode(self, value : aspose.threed.entities.MappingMode):
        ...
    
    @property
    def reference_mode(self) -> aspose.threed.entities.ReferenceMode:
        ...
    
    @reference_mode.setter
    def reference_mode(self, value : aspose.threed.entities.ReferenceMode):
        ...
    
    @property
    def indices(self) -> List[int]:
        '''Gets the indices data'''
        ...
    
    ...

class ApertureMode:
    '''Camera aperture modes.
    The aperture mode determines which values drive the camera aperture.
    If the aperture mode is HorizAndVert, Horizontal, or Vertical, then the field of view is used.
    If the aperture mode is FocalLength, then the focal length is used.'''
    
    @classmethod
    @property
    def HORIZ_AND_VERT(cls) -> ApertureMode:
        '''Set the angle values for both the horizontal and vertical settings.'''
        ...
    
    @classmethod
    @property
    def HORIZONTAL(cls) -> ApertureMode:
        '''Set only the horizontal angle.'''
        ...
    
    @classmethod
    @property
    def VERTICAL(cls) -> ApertureMode:
        '''Set only the vertical angle.'''
        ...
    
    @classmethod
    @property
    def FOCAL_LENGTH(cls) -> ApertureMode:
        '''Use focal length directly.'''
        ...
    
    ...

class CurveDimension:
    '''The dimension of the curves.'''
    
    @classmethod
    @property
    def TWO_DIMENSIONAL(cls) -> CurveDimension:
        '''The curves are two dimensional points.'''
        ...
    
    @classmethod
    @property
    def THREE_DIMENSIONAL(cls) -> CurveDimension:
        '''The curves are three dimensional points.'''
        ...
    
    ...

class LightType:
    '''Light types.'''
    
    @classmethod
    @property
    def POINT(cls) -> LightType:
        '''The point light.'''
        ...
    
    @classmethod
    @property
    def DIRECTIONAL(cls) -> LightType:
        '''The directional light.'''
        ...
    
    @classmethod
    @property
    def SPOT(cls) -> LightType:
        '''The spot light.'''
        ...
    
    @classmethod
    @property
    def AREA(cls) -> LightType:
        '''The area light.'''
        ...
    
    @classmethod
    @property
    def VOLUME(cls) -> LightType:
        '''The volume light.'''
        ...
    
    ...

class MappingMode:
    '''Determines how the element is mapped to a surface.
    The :py:class:`aspose.threed.entities.MappingMode` defined how :py:class:`aspose.threed.entities.VertexElement` is mapped to the surface of geometry.'''
    
    @classmethod
    @property
    def CONTROL_POINT(cls) -> MappingMode:
        '''Each data is mapped to the control point of the geometry.'''
        ...
    
    @classmethod
    @property
    def POLYGON_VERTEX(cls) -> MappingMode:
        '''The data is mapped to the polygon's vertex
        When a control point is shared by multiple polygons, and the data is mapped as :py:attr:`aspose.threed.entities.MappingMode.POLYGON_VERTEX`, the control point as different polygon vertex will have their own data'''
        ...
    
    @classmethod
    @property
    def POLYGON(cls) -> MappingMode:
        '''The data is mapped to the polygon.
        Each polygon vertex shares the same data when mapping mode is :py:attr:`aspose.threed.entities.MappingMode.POLYGON`.'''
        ...
    
    @classmethod
    @property
    def EDGE(cls) -> MappingMode:
        '''The data is mapped to the edge.
        Each edge end point shares the same data when mapping is :py:attr:`aspose.threed.entities.MappingMode.EDGE`.'''
        ...
    
    @classmethod
    @property
    def ALL_SAME(cls) -> MappingMode:
        '''One data mapped to the whole surface.
        What ever data is interpreted as control point/polygon vertex/edge endpoints, the data is always the same as it defined by :py:attr:`aspose.threed.entities.MappingMode.ALL_SAME`.'''
        ...
    
    ...

class NurbsType:
    '''NURBS types.'''
    
    @classmethod
    @property
    def OPEN(cls) -> NurbsType:
        '''The :py:class:`aspose.threed.entities.NurbsCurve` is an open curve.'''
        ...
    
    @classmethod
    @property
    def CLOSED(cls) -> NurbsType:
        '''The :py:class:`aspose.threed.entities.NurbsCurve` is a closed curve has its last control point equals to its first one.'''
        ...
    
    @classmethod
    @property
    def PERIODIC(cls) -> NurbsType:
        '''The :py:class:`aspose.threed.entities.NurbsCurve` is a periodic curve.'''
        ...
    
    ...

class PatchDirectionType:
    '''Patch direction's types.'''
    
    @classmethod
    @property
    def BEZIER(cls) -> PatchDirectionType:
        '''`The patch direction is a Bezier curve. <https://en.wikipedia.org/wiki/B%C3%A9zier_curve>`'''
        ...
    
    @classmethod
    @property
    def QUADRATIC_BEZIER(cls) -> PatchDirectionType:
        '''The quadratic bezier patch.
        `The patch direction is a quadratic curve. <https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Quadratic_curves>`'''
        ...
    
    @classmethod
    @property
    def CARDINAL_SPLINE(cls) -> PatchDirectionType:
        '''cardinal patch.
        `The patch direction is a cardinal spline. <https://en.wikipedia.org/wiki/Cubic_Hermite_spline#Cardinal_spline>`'''
        ...
    
    @classmethod
    @property
    def BASIS_SPLINE(cls) -> PatchDirectionType:
        '''`The patch direction is a basis spline. <https://en.wikipedia.org/wiki/B-spline>`'''
        ...
    
    @classmethod
    @property
    def LINEAR(cls) -> PatchDirectionType:
        '''`The patch direction is a linear curve. <https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Linear_curves>`'''
        ...
    
    ...

class ProjectionType:
    '''Camera's projection types.'''
    
    @classmethod
    @property
    def PERSPECTIVE(cls) -> ProjectionType:
        '''The camera uses perspective projection.'''
        ...
    
    @classmethod
    @property
    def ORTHOGRAPHIC(cls) -> ProjectionType:
        '''The camera uses orthographic projection.'''
        ...
    
    ...

class ReferenceMode:
    ''':py:class:`aspose.threed.entities.ReferenceMode` defines how mapping information is stored and referenced by.'''
    
    @classmethod
    @property
    def DIRECT(cls) -> ReferenceMode:
        '''Data is directly referenced'''
        ...
    
    @classmethod
    @property
    def INDEX(cls) -> ReferenceMode:
        '''Data is referenced by index'''
        ...
    
    @classmethod
    @property
    def INDEX_TO_DIRECT(cls) -> ReferenceMode:
        '''Data is referenced by index, then accessed by index in :py:class:`aspose.threed.entities.VertexElement`'s data list.'''
        ...
    
    ...

class RotationMode:
    '''The frustum's rotation mode'''
    
    @classmethod
    @property
    def FIXED_TARGET(cls) -> RotationMode:
        '''Target is fixed, direction is calculated by the look at target'''
        ...
    
    @classmethod
    @property
    def FIXED_DIRECTION(cls) -> RotationMode:
        '''Direction is fixed, look at is calculated by the direction'''
        ...
    
    ...

class SkeletonType:
    ''':py:class:`aspose.threed.entities.Skeleton`'s types.'''
    
    @classmethod
    @property
    def SKELETON(cls) -> SkeletonType:
        '''The :py:class:`aspose.threed.entities.Skeleton` is a skeleton entity, which means the associated node is the root node of the whole skeletal hierarchy.'''
        ...
    
    @classmethod
    @property
    def BONE(cls) -> SkeletonType:
        '''The :py:class:`aspose.threed.entities.Skeleton` is a bone entity.'''
        ...
    
    ...

class SplitMeshPolicy:
    '''Share vertex/control point data between sub-meshes or each sub-mesh has its own compacted data.'''
    
    @classmethod
    @property
    def CLONE_DATA(cls) -> SplitMeshPolicy:
        '''Control points and vertex elements data will be cloned'''
        ...
    
    @classmethod
    @property
    def COMPACT_DATA(cls) -> SplitMeshPolicy:
        '''Only used control points and vertex elements data will be copied to the sub-mesh'''
        ...
    
    ...

class TextureMapping:
    '''The texture mapping type for :py:class:`aspose.threed.entities.VertexElementUV`
    Describes which kind of texture mapping is used.'''
    
    @classmethod
    @property
    def AMBIENT(cls) -> TextureMapping:
        '''Ambient maps'''
        ...
    
    @classmethod
    @property
    def EMISSIVE(cls) -> TextureMapping:
        '''Emissive maps'''
        ...
    
    @classmethod
    @property
    def DIFFUSE(cls) -> TextureMapping:
        '''Diffuse maps'''
        ...
    
    @classmethod
    @property
    def OPACITY(cls) -> TextureMapping:
        '''Opacity maps'''
        ...
    
    @classmethod
    @property
    def BUMP(cls) -> TextureMapping:
        '''Bump maps'''
        ...
    
    @classmethod
    @property
    def NORMAL(cls) -> TextureMapping:
        '''Normal maps'''
        ...
    
    @classmethod
    @property
    def SPECULAR(cls) -> TextureMapping:
        '''Specular maps'''
        ...
    
    @classmethod
    @property
    def GLOW(cls) -> TextureMapping:
        '''Glow maps'''
        ...
    
    @classmethod
    @property
    def REFLECTION(cls) -> TextureMapping:
        '''Reflection maps'''
        ...
    
    @classmethod
    @property
    def SHADOW(cls) -> TextureMapping:
        '''Shadow maps'''
        ...
    
    @classmethod
    @property
    def SHININESS(cls) -> TextureMapping:
        '''Shininess maps'''
        ...
    
    @classmethod
    @property
    def DISPLACEMENT(cls) -> TextureMapping:
        '''Displacement maps'''
        ...
    
    ...

class VertexElementType:
    '''The type of the vertex element, defined how it will be used in modeling.'''
    
    @classmethod
    @property
    def BINORMAL(cls) -> VertexElementType:
        '''Binormal vector, see :py:class:`aspose.threed.entities.VertexElementBinormal`'''
        ...
    
    @classmethod
    @property
    def NORMAL(cls) -> VertexElementType:
        '''Normal vector, see :py:class:`aspose.threed.entities.VertexElementNormal`'''
        ...
    
    @classmethod
    @property
    def TANGENT(cls) -> VertexElementType:
        '''Tangent vector, see :py:class:`aspose.threed.entities.VertexElementTangent`'''
        ...
    
    @classmethod
    @property
    def MATERIAL(cls) -> VertexElementType:
        '''Material index, see :py:class:`aspose.threed.entities.VertexElementMaterial`'''
        ...
    
    @classmethod
    @property
    def POLYGON_GROUP(cls) -> VertexElementType:
        '''Polygon group index, see :py:class:`aspose.threed.entities.VertexElementPolygonGroup`'''
        ...
    
    @classmethod
    @property
    def UV(cls) -> VertexElementType:
        '''Texture UV coordinate, see :py:class:`aspose.threed.entities.VertexElementUV`'''
        ...
    
    @classmethod
    @property
    def VERTEX_COLOR(cls) -> VertexElementType:
        '''Vertex color, see :py:class:`aspose.threed.entities.VertexElementVertexColor`'''
        ...
    
    @classmethod
    @property
    def SMOOTHING_GROUP(cls) -> VertexElementType:
        '''Smoothing group, See :py:class:`aspose.threed.entities.VertexElementSmoothingGroup`'''
        ...
    
    @classmethod
    @property
    def VERTEX_CREASE(cls) -> VertexElementType:
        '''Vertex crease, See :py:class:`aspose.threed.entities.VertexElementVertexCrease`'''
        ...
    
    @classmethod
    @property
    def EDGE_CREASE(cls) -> VertexElementType:
        '''Edge crease, :py:class:`aspose.threed.entities.VertexElementEdgeCrease`'''
        ...
    
    @classmethod
    @property
    def USER_DATA(cls) -> VertexElementType:
        '''User data, usually for application-specific purpose, See :py:class:`aspose.threed.entities.VertexElementUserData`'''
        ...
    
    @classmethod
    @property
    def VISIBILITY(cls) -> VertexElementType:
        '''Visibility for components, see :py:class:`aspose.threed.entities.VertexElementVisibility`'''
        ...
    
    @classmethod
    @property
    def SPECULAR(cls) -> VertexElementType:
        '''Specular colors, see :py:class:`aspose.threed.entities.VertexElementSpecular`'''
        ...
    
    @classmethod
    @property
    def WEIGHT(cls) -> VertexElementType:
        '''Blend weights, see :py:class:`aspose.threed.entities.VertexElementWeight`'''
        ...
    
    @classmethod
    @property
    def HOLE(cls) -> VertexElementType:
        '''Holes, see :py:class:`aspose.threed.entities.VertexElementHole`'''
        ...
    
    ...

