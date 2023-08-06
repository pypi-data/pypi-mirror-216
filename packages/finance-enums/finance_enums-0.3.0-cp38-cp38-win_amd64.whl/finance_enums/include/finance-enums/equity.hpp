#pragma once
#include <finance-enums/common.hpp>
#include <iostream>
#include <vector>

namespace finance_enums {
ENUM(EquityType, Shares, PreferredShares, ConvertibleShares, PreferredConvertibleShares, DepositoryReceipt)
ENUM_FROM_STRING(EquityType)
ENUM_TO_STRING(EquityType)
}
