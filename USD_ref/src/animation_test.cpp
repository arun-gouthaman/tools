#include "animation_test.h"

#include<pxr/usd/usd/stage.h>
#include<pxr/usd/usd/prim.h>
#include<pxr/usd/usdGeom/cube.h>
#include<pxr/usd/usdGeom/xform.h>
#include<pxr/usd/sdf/path.h>
#include<pxr/usd/usdGeom/tokens.h>
#include<pxr/usd/usdGeom/api.h>
#include<pxr/pxr.h>
#include <pxr/usd/sdf/valueTypeName.h>


void anim_test::anim_test_usd()
{
	std::string usd_file_path = "C://my_files//USD_Trainig//CPP//USD_ref//usda_files//";
	pxr::UsdStageRefPtr stage = pxr::UsdStage::CreateNew(usd_file_path + std::string("anim_test.usda"));
	stage->SetMetadata(pxr::UsdGeomTokens->upAxis, pxr::VtValue("Z"));
	pxr::UsdPrim root_prim = stage->DefinePrim(pxr::SdfPath("/root"));
	pxr::UsdGeomXform xform = pxr::UsdGeomXform::Define(stage, pxr::SdfPath("/root/xform_cube"));
	
	pxr::UsdGeomCube cube1 = pxr::UsdGeomCube::Define(stage, pxr::SdfPath("/root/xform_cube/cube"));

	pxr::UsdGeomXformOp Zrot = xform.AddRotateZOp();
	Zrot.Set(0.0f, 0);
	Zrot.Set(90.0f, 50);

	pxr::UsdGeomXformOp Xrot = xform.AddRotateXOp();
	Xrot.Set(0.0f, 0);
	Xrot.Set(45.0f, 25);
	Xrot.Set(0.0f, 50);

	stage->SetStartTimeCode(1);
	stage->SetEndTimeCode(50);

	stage->Save();
}
