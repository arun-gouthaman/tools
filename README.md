# tools

collection of my works and references

For maya tools

maya tools collection All scripts created and tested with maya 2016

Copy all files to maya scripts folder and run below command to display menu

```import CustomMenu```

Menu - Object Creator - Custom tools - Motion path(loop) - Joint placement - Center (object) - Center (component) - Insert joints - Center aimed at vertex - Chain along edge loops - Loop from edge - Continue along loops - IK Spline setup - Curve through points - Delete display layers - Rearrange deformers - Rename deformer nodes - Controls - Create control - Manage shapes - replace instance nodes

Assign Checker Shaders: Please edit the file path in script

Spiral script not included in menu Will be included later with UI

Photoshop to maya textures, runs UI in photoshop to save individual layer groups as individual images and update texture in maya if maya is open and texture is present in scene

<span style="text-decoration:underline">
<B><I>USD Rreference file</I></B>
</span>

C++ file containing few basic USD codes as reference.

Build using cmake

Edit CMakeLists.txt file to point to right directories and run below commands

```mkdir build; cd build```

```cmake .. -G "Visual Studio 16 2019"```

Above commands will generate visual studio project, set the configuration to "RelWithDebInfo" and build.
