#pragma once
#include <finance-enums/common.hpp>
#include <iostream>
#include <vector>

namespace finance_enums {
ENUM(FundType, ETF, MutualFund, REIT)
ENUM_FROM_STRING(FundType)
ENUM_TO_STRING(FundType)

ENUM(FundSubType, Index, Sector, Active, Passive)
ENUM_FROM_STRING(FundSubType)
ENUM_TO_STRING(FundSubType)

ENUM(MutualFundEndedness, Open, Close)
ENUM_FROM_STRING(MutualFundEndedness)
ENUM_TO_STRING(MutualFundEndedness)
}
