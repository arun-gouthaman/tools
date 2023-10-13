#include <iostream>
#include<optional>
#include<filesystem>

#include "generic.h"


PXR_NAMESPACE_OPEN_SCOPE

// Create stage at given path
UsdStageRefPtr generic_functions::get_stage(const std::string& file_path)
{
	UsdStageRefPtr stage = UsdStage::CreateNew(file_path);
	return stage;
}

// Get UsdAttribute object if the attribute is found in the prim
UsdAttribute generic_functions::get_attr(UsdPrim prim, TfToken attr_name)
{
	UsdAttribute attr = prim.GetAttribute(attr_name);
	if (attr.IsValid())
	{
		return attr;
	}
	std::cout << prim.GetName().GetString() << " " << attr_name.GetString() << " not found";
	return UsdAttribute();
}

// Set attribute on given prim and attribute name
void generic_functions::set_attr(UsdPrim prim, TfToken attr_name, VtValue attr_val)
{
	UsdAttribute attr = get_attr(prim, attr_name);
	if (!attr)
	{
		return;
	}
	attr.Set(attr_val);
}

// Prim information from given stage
void generic_functions::inspect_stage(UsdStageRefPtr stage)
{
	std::cout << "Inspecting Stage\n";
	UsdPrimRange prim_range = stage->Traverse();
	for(UsdPrim prim : prim_range)
	{
		if (prim.IsA<UsdGeomXform>())
		{
			std::cout << "\t" << "xform type\n";
		}

		if (prim.IsA<UsdGeomSphere>())
		{
			std::cout << "\t" << "sphere type\n";
		}
		std::cout << prim.GetPath() << "\n";
		std::cout << "\t" << prim.GetName() << "\n";
		UsdAttributeVector attr_vec = prim.GetAttributes();
		for (UsdAttribute attr : attr_vec)
		{
			
			std::string attr_name = attr.GetName().GetString();
			std::cout << "\t\t" << attr_name;
			prim.GetAttribute(TfToken(attr_name));
			VtValue val;
			attr.Get(&val);
			std::cout << " : " << val << "\n";
		}
	}
}

// Set document string on root layer
void generic_functions::add_documentation(UsdStageRefPtr stage, std::string doc_str)
{
	stage->GetRootLayer()->SetDocumentation(doc_str);
}
// Create Xform prim  
UsdGeomXform generic_functions::create_xform(UsdStageRefPtr stage, SdfPath xform_path)
{
	return UsdGeomXform::Define(stage, xform_path);
}

// Create Sphere Prim
UsdGeomSphere generic_functions::create_sphere(UsdStageRefPtr stage, SdfPath sphere_path)
{
	return UsdGeomSphere::Define(stage, sphere_path);
}

// Set given kind on given prim
template <class T>
void generic_functions::set_kind(T prim, TfToken kind_name)
{
	UsdModelAPI(prim).SetKind(kind_name);
}

void generic_functions::set_asset_info(UsdPrim prim, TfToken key, VtValue val)
{
	prim.SetAssetInfoByKey(key, val);
}

void generic_functions::add_user_property(UsdPrim prim, TfToken property_name, SdfValueTypeName type_name,  VtValue property_val)
{
	UsdAttribute user_attr = prim.CreateAttribute(property_name, type_name);
	user_attr.Set(property_val);
}

void generic_functions::add_purpose(UsdPrim prim, TfToken purpose)
{
	UsdGeomImageable(prim).CreatePurposeAttr().Set(purpose);
}

void generic_functions::resolve_info(UsdPrim prim, TfToken attr_name)
{
	std::cout << get_attr(prim, attr_name).GetResolveInfo().GetSource() << "\n";
}

// Create .usda file with prim spheres for test
UsdStageRefPtr generic_functions::spheres_test(std::string sphere_file_name)
{
	std::string usd_files_base_path = "C://my_files//USD_Trainig//CPP//USD_ref//usda_files//";
	std::string usd_file = usd_files_base_path + sphere_file_name + ".usda";
	UsdStageRefPtr stage = get_stage(usd_file);
	UsdPrim root_prim = stage->DefinePrim(SdfPath("/root"));
	UsdGeomXform xform_sphere1 = create_xform(stage, SdfPath("/root/sphere1"));
	SdfPath sphere1_path = SdfPath(xform_sphere1.GetPath().GetAsString() + "/sphere1");
	UsdGeomSphere sphere1 = create_sphere(stage, sphere1_path);

	UsdGeomXform xform_sphere2 = create_xform(stage, SdfPath("/root/sphere2"));
	SdfPath sphere2_path = SdfPath(xform_sphere2.GetPath().GetAsString() + "/sphere2");
	UsdGeomSphere sphere2 = create_sphere(stage, sphere2_path);

	UsdGeomXform xform_sphere3 = create_xform(stage, SdfPath("/root/sphere3"));
	SdfPath sphere3_path = SdfPath(xform_sphere3.GetPath().GetAsString() + "/sphere3");
	UsdGeomSphere sphere3 = create_sphere(stage, sphere3_path);
	UsdPrim sphere3_prim = sphere3.GetPrim();
	set_asset_info(sphere3_prim, UsdModelAPIAssetInfoKeys->name, VtValue("sphere3_asset"));
	set_asset_info(sphere3_prim, UsdModelAPIAssetInfoKeys->version, VtValue("V1"));

	add_user_property(sphere3_prim, TfToken("UserProperty:custom_property"), SdfValueTypeNames->Bool, VtValue(true));
	set_attr(sphere3_prim, TfToken("UserProperty:custom_property"), VtValue(false));


	set_kind(sphere1, KindTokens->component);
	set_kind(sphere2, KindTokens->component);
	set_kind(sphere3, TfToken("custom_kind"));

	add_purpose(sphere2.GetPrim(), UsdGeomTokens->Sphere);

	add_documentation(stage, "Root layer doc string goes here");

	set_attr(sphere1.GetPrim(), TfToken("radius"), VtValue(2.0));

	UsdPrim specialize_prim = stage->DefinePrim(SdfPath("/specialize_prim"));
	specialize_prim.GetSpecializes().AddSpecialize(sphere1.GetPath());
	set_attr(specialize_prim, TfToken("radius"), VtValue(3.0));

	stage->Save();

	return stage;
}

// Create a main_file.usda file and reference sphere_ref_test.usda file.

PXR_NAMESPACE_CLOSE_SCOPE