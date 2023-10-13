#pragma once

#include <pxr/usd/usd/stage.h>

PXR_NAMESPACE_OPEN_SCOPE

namespace layers_test
{
	UsdStageRefPtr create_reference();

	UsdStageRefPtr create_sublayer();

	UsdStageRefPtr sub_layer_edit_target_test();

	UsdStageRefPtr ref_layer_edit_target_test();
}

PXR_NAMESPACE_CLOSE_SCOPE