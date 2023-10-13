#include <iostream>
#include<optional>

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


using namespace pxr;

// Create stage at given path
UsdStageRefPtr get_stage(const std::string& file_path)
{
	UsdStageRefPtr stage = UsdStage::CreateNew(file_path);
	return stage;
}

// Get UsdAttribute object if the attribute is found in the prim
UsdAttribute get_attr(UsdPrim prim, TfToken attr_name)
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
void set_attr(UsdPrim prim, TfToken attr_name, VtValue attr_val)
{
	UsdAttribute attr = get_attr(prim, attr_name);
	if (!attr)
	{
		return;
	}
	attr.Set(attr_val);
}

// Prim information from given stage
void inspect_stage(UsdStageRefPtr stage)
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
void add_documentation(UsdStageRefPtr stage, std::string doc_str)
{
	stage->GetRootLayer()->SetDocumentation(doc_str);
}
// Create Xform prim  
UsdGeomXform create_xform(UsdStageRefPtr stage, SdfPath xform_path)
{
	return UsdGeomXform::Define(stage, xform_path);
}

// Create Sphere Prim
UsdGeomSphere create_sphere(UsdStageRefPtr stage, SdfPath sphere_path)
{
	return UsdGeomSphere::Define(stage, sphere_path);
}

// Set given kind on given prim
template <class T>
void set_kind(T prim, TfToken kind_name)
{
	UsdModelAPI(prim).SetKind(kind_name);
}


void set_asset_info(UsdPrim prim, TfToken key, VtValue val)
{
	prim.SetAssetInfoByKey(key, val);
}


void add_user_property(UsdPrim prim, TfToken property_name, SdfValueTypeName type_name,  VtValue property_val)
{
	UsdAttribute user_attr = prim.CreateAttribute(property_name, type_name);
	user_attr.Set(property_val);
}

void add_purpose(UsdPrim prim, TfToken purpose)
{
	UsdGeomImageable(prim).CreatePurposeAttr().Set(purpose);
}

void resolve_info(UsdPrim prim, TfToken attr_name)
{
	std::cout << get_attr(prim, attr_name).GetResolveInfo().GetSource() << "\n";
}

// Create .usda file with prim spheres for test
UsdStageRefPtr spheres_test(std::string sphere_file_name)
{
	std::string usd_file = "C://my_files//USD_Trainig//CPP//helloworld//usda_files//" + sphere_file_name + ".usda";
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

// Resolve info test, get the attribute's source
void resolve_info_test()
{
	UsdStageRefPtr stage = UsdStage::Open("C:\\my_files\\USD_Trainig\\CPP\\helloworld\\usda_files\\resolve_info\\usd_resolve_info.usda");

	UsdPrim prim = stage->GetPrimAtPath(SdfPath("/PrimWithValueClips"));
	UsdAttribute attr = get_attr(prim, TfToken("value_clipped_property"));
	UsdResolveInfo resolve_info = attr.GetResolveInfo();
	UsdResolveInfoSource resolve_src = resolve_info.GetSource();
	std::cout << resolve_src << "\n";
	std::cout << UsdResolveInfoSourceValueClips << "\n";
}

// Create a main_file.usda file and reference sphere_ref_test.usda file.
UsdStageRefPtr create_reference()
{
	UsdStageRefPtr stage = spheres_test(std::string("sphere_ref_test"));
	SdfLayerHandle sphere_root = stage->GetRootLayer();
	UsdPrim prim = stage->GetPrimAtPath(SdfPath("/root"));
	std::string identifier = sphere_root->GetIdentifier();

	UsdStageRefPtr main_stage = get_stage("C://my_files//USD_Trainig//CPP//helloworld//usda_files//main_file.usda");

	UsdPrim main_prim = main_stage->DefinePrim(SdfPath("/root"));

	create_xform(main_stage, SdfPath("/root/sphere_xform"));
	create_sphere(main_stage, SdfPath("/root/sphere_xform/sphere1"));

	UsdPrim ref_prim = main_stage->OverridePrim(SdfPath("/ref_prim"));

	ref_prim.GetReferences().AddReference(identifier, prim.GetPath());

	main_stage->Save();
	return stage;
}

// Create main_file.usda and add sphere_sublayer_test.usda as sub layer
UsdStageRefPtr create_sublayer()
{
	UsdStageRefPtr stage = spheres_test(std::string("sphere_sublayer_test"));
	SdfLayerHandle sphere_root = stage->GetRootLayer();
	UsdPrim prim = stage->GetPrimAtPath(SdfPath("/root"));
	std::string identifier = sphere_root->GetIdentifier();



	UsdStageRefPtr main_stage = get_stage("C://my_files//USD_Trainig//CPP//helloworld//usda_files//main_file.usda");

	UsdPrim main_prim = main_stage->DefinePrim(SdfPath("/root"));

	create_xform(main_stage, SdfPath("/root/sphere_xform"));
	create_sphere(main_stage, SdfPath("/root/sphere_xform/sphere1"));

	UsdPrim ref_prim = main_stage->OverridePrim(SdfPath("/ref_prim"));

	main_stage->GetRootLayer()->GetSubLayerPaths().push_back(identifier);


	//ref_prim.GetReferences().AddReference(identifier, prim.GetPath());

	main_stage->Save();
	return stage;
}

// Setting edit target to the sublayer in usda file
UsdStageRefPtr sub_layer_edit_target_test()
{
	create_sublayer();

	UsdStageRefPtr stage = UsdStage::Open("C://my_files//USD_Trainig//CPP//helloworld//usda_files//main_file.usda");

	std::cout << "EDIT TARGET: " << stage->GetEditTarget().GetLayer()->GetDisplayName() << "\n";

	SdfLayerHandleVector lyr_hdl = stage->GetUsedLayers();

	SdfLayerHandle new_edit_layer;
	for (SdfLayerHandle lyr : lyr_hdl)
	{
		//std::cout << lyr->GetDisplayName() << "\n";
		if (lyr->GetDisplayName() == std::string("sphere_sublayer_test.usda"))
		{
			new_edit_layer = lyr;
			break;
		}
	}
	UsdEditTarget new_edit_target = UsdEditTarget(new_edit_layer);

	stage->SetEditTarget(new_edit_target);

	std::cout << "EDITR TARGET: " << stage->GetEditTarget().GetLayer()->GetDisplayName() << "\n";
	return stage;
}


// Setting edit target to reference layer in usda file
UsdStageRefPtr ref_layer_edit_target_test()
{
	create_reference();

	UsdStageRefPtr stage = UsdStage::Open("C://my_files//USD_Trainig//CPP//helloworld//usda_files//main_file.usda");

	UsdPrimRange prim_range = stage->Traverse();

	std::cout <<"Edit Target: " << stage->GetEditTarget().GetLayer()->GetDisplayName() << "\n";

	bool flag = false;

	for (UsdPrim prim : prim_range)
	{
		if (prim.GetName() == "ref_prim")
		{
			PcpPrimIndex prim_ind = prim.GetPrimIndex();

			for (PcpNodeRef nd : prim_ind.GetNodeRange())
			{
				PcpLayerStackRefPtr lyr_stk = nd.GetLayerStack();

				for (SdfLayerRefPtr lyr : lyr_stk->GetLayers())
				{

					if (lyr->GetDisplayName() == "sphere_ref_test.usda")
					{
						UsdEditTarget edit_target = UsdEditTarget(lyr, nd);
						stage->SetEditTarget(edit_target);
						flag = true;
						break;
					}
					if(flag)
					{
						break;
					}
				}
			}
		}
	}
	std::cout <<"Edit Target: " << stage->GetEditTarget().GetLayer()->GetDisplayName() << "\n";
	return stage;
}

// Copied from https://github.com/ColinKennedy/USD-Cookbook to test
void change_block()
{
	auto layer = pxr::SdfLayer::CreateAnonymous();

	pxr::SdfPathSet paths{
		pxr::SdfPath {"/AndMore"},
		pxr::SdfPath {"/AnotherOne"},
		pxr::SdfPath {"/AnotherOne/AndAnother"},
		pxr::SdfPath {"/More"},
		pxr::SdfPath {"/OkayNoMore"},
		pxr::SdfPath {"/SomeSphere"},
		pxr::SdfPath {"/SomeSphere/InnerPrim"},
		pxr::SdfPath {"/SomeSphere/InnerPrim/LastOne"},
	};

	TfToken xform_type = UsdGeomTokensType().Xform;

	for (auto const& path : paths) {
		auto prefixes = path.GetPrefixes();
		paths.insert(std::begin(prefixes), std::end(prefixes));
	}

	{
		pxr::SdfChangeBlock batcher;

		for (auto const& path : paths) {
			auto prim_spec = pxr::SdfCreatePrimInLayer(layer, path);
			prim_spec->SetSpecifier(pxr::SdfSpecifierDef);
			prim_spec->SetTypeName(xform_type);
		}
	}

	auto* result = new std::string();
	layer->ExportToString(result);
	std::cout << *result << std::endl;
	delete result;
	result = nullptr;
}

// Adding information using SdfChangeBlock to sublayer or reference setting them as EditTargetLayer
void change_block_test()
{
	UsdStageRefPtr stage = ref_layer_edit_target_test();
	SdfLayerHandle lyr = stage->GetEditTarget().GetLayer();
	SdfPath new_path = SdfPath("/root/new_prim");
	TfToken xform_type = UsdGeomTokensType().Xform;
	{
		pxr::SdfChangeBlock batcher;
		auto prim_spec = pxr::SdfCreatePrimInLayer(lyr, new_path);
		prim_spec->SetSpecifier(pxr::SdfSpecifierDef);
		prim_spec->SetTypeName(xform_type);
	}
	stage->Save();
}

int main()
{
	change_block_test();
	return 0;
}