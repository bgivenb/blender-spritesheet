bl_info = {
    "name": "Spritesheet Renderer",
    "author": "Given Peace",
    "version": (1, 4),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Spritesheet",
    "description": "Render a spritesheet from a model and camera",
    "category": "Render",
}

import bpy
import math
import os
from mathutils import Euler
from bpy.props import (
    PointerProperty,
    StringProperty,
    IntProperty,
    FloatProperty,
    EnumProperty,
    BoolProperty,
)
from bpy.types import Panel, Operator, PropertyGroup

class SpritesheetProperties(PropertyGroup):
    model: PointerProperty(
        name="Model",
        type=bpy.types.Object,
        description="Select the model to render",
    )
    camera: PointerProperty(
        name="Camera",
        type=bpy.types.Object,
        description="Select the camera to render from",
    )
    output_path: StringProperty(
        name="Output Path",
        description="Directory to save the spritesheet",
        default="//",
        subtype='DIR_PATH',
    )
    image_width: IntProperty(
        name="Image Width",
        description="Width of the spritesheet (pixels)",
        default=1024,
        min=1,
    )
    image_height: IntProperty(
        name="Image Height",
        description="Height of the spritesheet (pixels)",
        default=1024,
        min=1,
    )
    frames_per_second: IntProperty(
        name="Frames Per Second",
        description="Number of frames rendered per second",
        default=24,
        min=1,
    )
    rotation_axis: EnumProperty(
        name="Rotation Axis",
        description="Axis to rotate the model around",
        items=[
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", ""),
        ],
        default='Z',
    )
    use_animation: BoolProperty(
        name="Use Animation",
        description="Render frames from the timeline animation instead of rotating the model",
        default=False,
    )
    start_frame: IntProperty(
        name="Start Frame",
        description="Start frame of the animation",
        default=1,
        min=1,
    )
    end_frame: IntProperty(
        name="End Frame",
        description="End frame of the animation",
        default=250,
        min=1,
    )
    render_360_animation: BoolProperty(
        name="Render 360 Animation",
        description="Render 360-degree animation with fixed settings",
        default=False,
    )

class RENDER_OT_spritesheet(Operator):
    bl_idname = "render.spritesheet"
    bl_label = "Render Spritesheet"
    bl_description = "Render the spritesheet based on settings"

    def execute(self, context):
        props = context.scene.spritesheet_props
        model = props.model
        camera = props.camera

        if not model or not camera:
            self.report({'ERROR'}, "Please select both a model and a camera.")
            return {'CANCELLED'}

        scene = context.scene
        scene.camera = camera

        image_width = props.image_width
        image_height = props.image_height
        frames_per_second = props.frames_per_second
        output_path = bpy.path.abspath(props.output_path)

        # Set render settings
        scene.render.resolution_x = image_width
        scene.render.resolution_y = image_height
        scene.render.fps = frames_per_second
        scene.render.image_settings.file_format = 'PNG'
        scene.render.film_transparent = True

        # Spritesheet dimensions
        sprites_per_row = 8
        sprites_per_column = 8
        sprite_width = image_width // sprites_per_row
        sprite_height = image_height // sprites_per_column
        sheet_width = sprite_width * sprites_per_row
        sheet_height = sprite_height * sprites_per_column

        # Ensure output directory exists
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Create a new image for the spritesheet
        spritesheet_name = "spritesheet_image"
        spritesheet = bpy.data.images.new(
            spritesheet_name,
            width=sheet_width,
            height=sheet_height,
            alpha=True,
            float_buffer=False
        )

        # Initialize the spritesheet pixels to transparent
        blank_pixels = [0.0, 0.0, 0.0, 0.0] * (sheet_width * sheet_height)
        spritesheet.pixels = blank_pixels

        # Store original frame and rotation
        original_frame = scene.frame_current
        original_rotation = model.rotation_euler.copy()

        if props.render_360_animation:
            total_rotations = 8
            rotation_angle = 360 / total_rotations

            # Calculate frames to render for animation
            start_frame = props.start_frame
            end_frame = props.end_frame
            total_frames = end_frame - start_frame + 1

            if total_frames < sprites_per_row:
                self.report({'ERROR'}, "Animation frame range is smaller than the number of sprites per row.")
                return {'CANCELLED'}

            frame_numbers = [
                int(round(start_frame + i * (total_frames - 1) / (sprites_per_row - 1)))
                for i in range(sprites_per_row)
            ]

            sprite_index = 0
            for rotation_index in range(total_rotations):
                # Calculate the rotation angle for the current rotation
                rotation_angle_rad = math.radians(rotation_angle * rotation_index)

                # Apply rotation to the model
                model.rotation_euler = original_rotation.copy()
                axis_index = 'XYZ'.index(props.rotation_axis)
                model.rotation_euler[axis_index] += rotation_angle_rad

                # Update the scene
                context.view_layer.update()

                # Render each frame in the animation
                for i, frame_number in enumerate(frame_numbers):
                    scene.frame_set(frame_number)

                    # Update the scene
                    context.view_layer.update()

                    # Render to a temporary image
                    temp_image_name = f"sprite_{sprite_index:03d}"
                    scene.render.image_settings.file_format = 'OPEN_EXR'
                    scene.render.image_settings.color_mode = 'RGBA'
                    scene.render.image_settings.color_depth = '16'
                    scene.render.filepath = os.path.join(output_path, temp_image_name)
                    bpy.ops.render.render(write_still=True)

                    # Load the rendered image
                    temp_image_path = scene.render.filepath + ".exr"
                    temp_image = bpy.data.images.load(temp_image_path)

                    # Calculate position in the spritesheet
                    row = rotation_index  # Rows correspond to rotations
                    column = i  # Columns correspond to frames in animation
                    x = column * sprite_width
                    y = (sprites_per_column - 1 - row) * sprite_height  # Flip y-axis

                    # Copy pixels from temp image to spritesheet
                    temp_image.scale(sprite_width, sprite_height)
                    temp_pixels = list(temp_image.pixels)

                    for pixel_y in range(sprite_height):
                        for pixel_x in range(sprite_width):
                            src_index = ((pixel_y * sprite_width) + pixel_x) * 4
                            dest_x = x + pixel_x
                            dest_y = y + pixel_y
                            dest_index = ((dest_y * sheet_width) + dest_x) * 4
                            spritesheet.pixels[dest_index:dest_index+4] = temp_pixels[src_index:src_index+4]

                    # Remove temp image and file
                    bpy.data.images.remove(temp_image)
                    os.remove(temp_image_path)

                    sprite_index += 1

            # Restore original frame and rotation
            scene.frame_set(original_frame)
            model.rotation_euler = original_rotation

        else:
            # Existing logic for other modes can be placed here
            self.report({'ERROR'}, "Please enable 'Render 360 Animation' to use this feature.")
            return {'CANCELLED'}

        # Save the spritesheet
        spritesheet.filepath_raw = os.path.join(output_path, "spritesheet.png")
        spritesheet.file_format = 'PNG'
        spritesheet.save()

        # Report before removing the spritesheet
        self.report({'INFO'}, f"Spritesheet saved to {spritesheet.filepath_raw}")

        # Remove the spritesheet from memory
        bpy.data.images.remove(spritesheet)

        return {'FINISHED'}

class VIEW3D_PT_spritesheet_renderer(Panel):
    bl_label = "Spritesheet Renderer"
    bl_idname = "VIEW3D_PT_spritesheet_renderer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Spritesheet'

    def draw(self, context):
        layout = self.layout
        props = context.scene.spritesheet_props

        layout.prop(props, "model")
        layout.prop(props, "camera")
        layout.prop(props, "output_path")
        layout.prop(props, "image_width")
        layout.prop(props, "image_height")
        layout.prop(props, "frames_per_second")

        layout.prop(props, "render_360_animation")

        if props.render_360_animation:
            layout.prop(props, "rotation_axis")
            layout.prop(props, "start_frame")
            layout.prop(props, "end_frame")
        else:
            layout.label(text="Enable 'Render 360 Animation' to use this feature.")

        layout.operator("render.spritesheet", text="Render Spritesheet", icon='RENDER_STILL')

classes = (
    SpritesheetProperties,
    RENDER_OT_spritesheet,
    VIEW3D_PT_spritesheet_renderer,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.spritesheet_props = PointerProperty(type=SpritesheetProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.spritesheet_props

if __name__ == "__main__":
    register()
