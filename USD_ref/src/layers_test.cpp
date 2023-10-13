#include "layers_test.h"
#include "generic.h"
#include <iostream>

PXR_NAMESPACE_OPEN_SCOPE
UsdStageRefPtr layers_test::create_reference()
{
	UsdStageRefPtr stage = generic_functions::spheres_test(std::string("sphere_ref_test"));
	SdfLayerHandle sphere_root = stage->GetRootLayer();
	UsdPrim prim = stage->GetPrimAtPath(SdfPath("/root"));
	std::string identifier = sphere_root->GetIdentifier();

	UsdStageRefPtr main_stage = generic_functions::get_stage("C://my_files//USD_Trainig//CPP//USD_ref//usda_files//main_file.usda");

	UsdPrim main_prim = main_stage->DefinePrim(SdfPath("/root"));

	generic_functions::create_xform(main_stage, SdfPath("/root/sphere_xform"));
	generic_functions::create_sphere(main_stage, SdfPath("/root/sphere_xform/sphere1"));

	UsdPrim ref_prim = main_stage->OverridePrim(SdfPath("/ref_prim"));

	ref_prim.GetReferences().AddReference(identifier, prim.GetPath());

	main_stage->Save();
	return stage;
}

// Create main_file.usda and add sphere_sublayer_test.usda as sub layer
UsdStageRefPtr layers_test::create_sublayer()
{
	UsdStageRefPtr stage = generic_functions::spheres_test(std::string("sphere_sublayer_test"));
	SdfLayerHandle sphere_root = stage->GetRootLayer();
	UsdPrim prim = stage->GetPrimAtPath(SdfPath("/root"));
	std::string identifier = sphere_root->GetIdentifier();



	UsdStageRefPtr main_stage = generic_functions::get_stage("C://my_files//USD_Trainig//CPP//USD_ref//usda_files//main_file.usda");

	UsdPrim main_prim = main_stage->DefinePrim(SdfPath("/root"));

	generic_functions::create_xform(main_stage, SdfPath("/root/sphere_xform"));
	generic_functions::create_sphere(main_stage, SdfPath("/root/sphere_xform/sphere1"));

	UsdPrim ref_prim = main_stage->OverridePrim(SdfPath("/ref_prim"));

	main_stage->GetRootLayer()->GetSubLayerPaths().push_back(identifier);


	//ref_prim.GetReferences().AddReference(identifier, prim.GetPath());

	main_stage->Save();
	return stage;
}

// Setting edit target to the sublayer in usda file
UsdStageRefPtr layers_test::sub_layer_edit_target_test()
{
	create_sublayer();

	UsdStageRefPtr stage = UsdStage::Open("C://my_files//USD_Trainig//CPP//USD_ref//usda_files//main_file.usda");

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
UsdStageRefPtr layers_test::ref_layer_edit_target_test()
{
	create_reference();

	UsdStageRefPtr stage = UsdStage::Open("C://my_files//USD_Trainig//CPP//USD_ref//usda_files//main_file.usda");

	UsdPrimRange prim_range = stage->Traverse();

	std::cout << "Edit Target: " << stage->GetEditTarget().GetLayer()->GetDisplayName() << "\n";

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
					if (flag)
					{
						break;
					}
				}
			}
		}
	}
	if (!flag)
	{
		std::cout << "edit target not set\n";
	}
	std::cout << "Edit Target: " << stage->GetEditTarget().GetLayer()->GetDisplayName() << "\n";
	return stage;
}

PXR_NAMESPACE_CLOSE_SCOPE