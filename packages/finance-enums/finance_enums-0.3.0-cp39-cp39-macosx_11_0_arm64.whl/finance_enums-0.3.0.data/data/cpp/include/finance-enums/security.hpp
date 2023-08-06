#pragma once
#include <finance-enums/common.hpp>
#include <finance-enums/helpers/exports.hpp>
#include <iostream>
#include <vector>

namespace finance_enums {
enum class LIB_EXPORT SecurityType {
  Equity,
  Option,
  Bond,
  Forward,
  Future,
  PerpetualFuture,
  Spread,
  Fund,
  Commodity,
  Currency,
  Pair,
  Index,
};

ENUM_NAMES(
  SecurityType, Equity, Option, Bond, Forward, Future, PerpetualFuture, Spread, Fund, Commodity, Currency, Pair, Index
)
ENUM_MAPPING(
  SecurityType, Equity, Option, Bond, Forward, Future, PerpetualFuture, Spread, Fund, Commodity, Currency, Pair, Index
)
ENUM_FROM_STRING(SecurityType)
ENUM_TO_STRING(SecurityType)

}
