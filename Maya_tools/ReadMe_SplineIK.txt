Spline IK tool

Tool to create spline IK with stretch and squash effects

-input setup name

-input base joint

-dense joint
    if selected creates a new dense chain that acts as spline joints
    divisions takes input for number of joints to be created between 2 joints

-Auto Curve/ Use Curve
    curve for spline ik can be created by the tool or existing curve can be assigned

-Simplify curve used in spline IK
    recreate a simplified curve with lesser control points for ease of control

-Turn on stretch function

-Connect scale
    used to enable thnning and thickening of object by scaling the joints during stretch and squash

-Global scale
    input the global scale attribute to connect the setup to scaling
    input format: <object>.<attribute>
        example: cube1.globalScale (attribute globalScale should be created before running the tool)

-Number of control joints:
    total number of joints to be used as control for the spline chain,
    spline nurbs curve gets skinned to these joints
