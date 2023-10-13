#include <pxr/usd/usdGeom/primvarsAPI.h>

#include <iostream>

#include "block_change_test.h"
#include "layers_test.h"


PXR_NAMESPACE_OPEN_SCOPE

// Copied from https://github.com/ColinKennedy/USD-Cookbook to test
void block_test::change_block()
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
void block_test::change_block_test()
{
	UsdStageRefPtr stage = layers_test::ref_layer_edit_target_test();
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

PXR_NAMESPACE_CLOSE_SCOPE