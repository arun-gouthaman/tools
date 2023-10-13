#pragma once
#include <pxr/usd/usdGeom/sphere.h>
#include <pxr/usd/usdGeom/xform.h>
#include <pxr/usd/usdGeom/xformable.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usd/prim.h>
#include <pxr/usd/usd/primRange.h>
#include <pxr/usd/usd/attribute.h>
#include <pxr/base/tf/token.h>
#include <pxr/usd/usd/modelAPI.h>
#include <pxr/usd/kind/registry.h>
#include <pxr/usd/usd/specializes.h>
#include <pxr/usd/sdf/valueTypeName.h>
#include <pxr/usd/usdGeom/primvar.h>
#include <pxr/usd/usdGeom/primvarsAPI.h>
#include <pxr/usd/usdGeom/imageable.h>
#include <pxr/usd/usd/schemaRegistry.h>
#include <pxr/usd/sdf/changeBlock.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/sdf/layer.h>
#include <pxr/usd/pcp/primIndex.h>
#include <pxr/usd/pcp/layerStack.h>

PXR_NAMESPACE_OPEN_SCOPE

namespace generic_functions
{

	UsdStageRefPtr get_stage(const std::string& file_path);

	UsdAttribute get_attr(UsdPrim prim, TfToken attr_name);

	void set_attr(UsdPrim prim, TfToken attr_name, VtValue attr_val);

	void inspect_stage(UsdStageRefPtr stage);

	void add_documentation(UsdStageRefPtr stage, std::string doc_str);

	UsdGeomXform create_xform(UsdStageRefPtr stage, SdfPath xform_path);

	UsdGeomSphere create_sphere(UsdStageRefPtr stage, SdfPath sphere_path);

	template <class T>
	void set_kind(T prim, TfToken kind_name);

	void set_asset_info(UsdPrim prim, TfToken key, VtValue val);

	void add_user_property(UsdPrim prim, TfToken property_name, SdfValueTypeName type_name, VtValue property_val);

	void add_purpose(UsdPrim prim, TfToken purpose);

	void resolve_info(UsdPrim prim, TfToken attr_name);

	UsdStageRefPtr spheres_test(std::string sphere_file_name);

}

PXR_NAMESPACE_CLOSE_SCOPE
