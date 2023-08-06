#pragma once
#include <finance-enums/common.hpp>
#include <finance-enums/helpers/enum.hpp>

namespace finance_enums {
ENUM(BondType, Corporate, Government, Municipal)
ENUM_FROM_STRING(BondType)
ENUM_TO_STRING(BondType)
}
