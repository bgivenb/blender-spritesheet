Spritesheet Renderer for Blender by Given Borthwick

Spritesheet Renderer is a Blender addon designed to streamline the creation of spritesheets from your 3D models. Whether you're developing games, animations, or interactive applications, this tool simplifies the process of generating high-quality spritesheets by automating rendering tasks with customizable settings.
Features

    Model and Camera Selection: Easily choose the 3D model and camera from which to render your sprites.
    Image Settings: Define the resolution of your spritesheet to suit your project's needs.
        Render Modes:
        360 Animation Rendering: Automatically renders a full 360-degree rotation of your model, organizing sprites into an 8x8 grid.
        Animation Frame Rendering: Capture specific frames from your timeline animation and distribute them evenly across the spritesheet.
    Automated Spritesheet Assembly: Combines rendered images into a single, organized spritesheet without the need for external tools.
    User-Friendly Interface: Access all settings through a convenient panel in the Blender UI.

Installation

    Download the Addon:
        Save the spritesheet_renderer.py script to a convenient location on your computer.

    Install via Blender:
        Open Blender.
        Navigate to Edit > Preferences > Add-ons.
        Click on the Install... button at the top.
        Locate and select the spritesheet_renderer.py file you downloaded.
        After installation, enable the addon by checking the box next to Spritesheet Renderer.

Usage

    Access the Addon:
        In the 3D Viewport, press N to open the sidebar.
        Navigate to the Spritesheet tab.

    Configure Settings:
        Model: Select the 3D object you wish to render.
        Camera: Choose the camera from which the render will be captured.
        Output Path: Specify the directory where the spritesheet will be saved.
        Image Width & Height: Define the dimensions of the final spritesheet (in pixels).
        Frames Per Second: Set the rendering FPS (optional for certain modes).

    Choose Render Mode:

        Render 360 Animation:
            Enable: Check the Render 360 Animation box.
            Rotation Axis: Select the axis (X, Y, or Z) around which the model will rotate.
            Start Frame: Define the starting frame of your animation.
            End Frame: Define the ending frame of your animation.
            Description: The addon will render 8 sprites per row, rotating the model by 45 degrees after each row, completing a full 360-degree rotation with a total of 64 sprites (8 rows x 8 columns).

        Use Animation:
            Enable: Check the Use Animation box.
            Start Frame: Set the starting frame of the animation to capture.
            End Frame: Set the ending frame of the animation to capture.
            Description: The addon will evenly distribute the specified number of sprites across the selected frame range, capturing different animation states.

    Render Spritesheet:
        Click the Render Spritesheet button to initiate the rendering process.
        The addon will process each frame or rotation step, compile the sprites into a single image, and save it to the specified output directory.

Example
360 Animation Rendering

    Select Model and Camera.
    Enable Render 360 Animation.
    Set Rotation Axis to Z.
    Define Start Frame (1) and End Frame (250).
    Click Render Spritesheet.
    Result: A 1024x1024 pixels spritesheet with 64 sprites arranged in an 8x8 grid, each representing a 45-degree rotation of the model.

Animation Frame Rendering

    Select Model and Camera.
    Enable Use Animation.
    Set Start Frame (1) and End Frame (250).
    Click Render Spritesheet.
    Result: A spritesheet with sprites capturing the model at different animation frames, evenly distributed across the grid.

Requirements

    Blender: Version 3.6 or higher.
    Operating System: Compatible with Windows, macOS, and Linux.
    Permissions: Write permissions to the specified output directory.

Troubleshooting

    No Spritesheet Generated:
        Ensure that both a model and camera are selected.
        Verify that the output path is correct and writable.
        Check that the image dimensions are divisible by 8 for 360 animation rendering.

    Incorrect Rotation:
        Confirm that the correct rotation axis is selected.
        Ensure that the model's origin is appropriately set for rotation.
        Make sure you have selected the parent for rigged and animated models

    Error Messages:
        Review Blender's console for detailed error logs.
        Common errors include missing dependencies or incorrect frame ranges.

Customization

    Adjust Spritesheet Grid:
        Modify the number of sprites per row and column by editing the script variables sprites_per_row and sprites_per_column.

    Change Rotation Steps:
        Alter the rotation_angle calculation to achieve different rotation increments.

    Extend Render Modes:
        Add additional rendering options by expanding the UI panel and logic in the script.

Contribution

Contributions are welcome! If you encounter bugs, have feature requests, or want to contribute code, please open an issue or submit a pull request on the GitHub repository.
License

Acknowledgements

    Blender Foundation: For providing a powerful and versatile platform for 3D creation.
    Open Source Community: For inspiring and contributing to the development of Blender addons.
