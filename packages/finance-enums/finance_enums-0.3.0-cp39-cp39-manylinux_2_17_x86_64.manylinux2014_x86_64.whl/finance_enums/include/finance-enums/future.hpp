#pragma once
#include <finance-enums/common.hpp>
#include <iostream>
#include <vector>

namespace finance_enums {
ENUM(FutureType, Financial, Commodity)
ENUM_FROM_STRING(FutureType)
ENUM_TO_STRING(FutureType)

ENUM(FutureDeliveryType, Physical, Cash)
ENUM_FROM_STRING(FutureDeliveryType)
ENUM_TO_STRING(FutureDeliveryType)
}
