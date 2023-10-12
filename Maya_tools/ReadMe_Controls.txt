Controls

Tool to manage control library and assign controls to objects
Controls resize based on object's bounding box size


Create Control
    -Skinning/Constraint
        Objects can either be skinned or constrained under controls
        if checked off, shapes are created but do not have control over object

    -Control name
        Mesh name can be used with replace text for control naming

        >Control name
            Check to enter control name
            Controls are named with number id and suffix text

        >Zero node
            Naming pattern for zero group node

        >Lock scale/visibility/Radius(for joints) attributes

        >Scale controls to match objects, uses bounding box sizes from objects

        >Control size offset value to make the control size scaled larger than object bounding box(for visibility)

    -Control at object pivot
        Options to create control at object pivot or top, bottom, front, back, right and left


    Existing shapes are displayed on the right, select objects and click the control shape needed.
    After createing new shape, close and reopen the window to refresh
    To have icond displayed, create icons with the same name as control name and place inside "Ctrl_icons" folder


Manage Shapes
    -Shape name
        Name to create the new shape with

    -Shape mel command
        Create shape manually in maya, use the mel command generated, copy from script editor window to text box in UI, with semicolon at the end.

    -Existing shapes
        Displays a list of existing shapes
        Existing shapes can be renamed or deleted if needed
        When a new shape is added, it appends to the list
