#pragma once
#include <finance-enums/common.hpp>
#include <finance-enums/helpers/exports.hpp>
#include <iostream>
#include <vector>

namespace finance_enums {
// TODO
// https://en.wikipedia.org/wiki/ISO_10962

enum class LIB_EXPORT InstrumentType {
  Spot,    // single instrument
  Option,  // underlying + date
  Forward, // underlying + date
  Future,  // underlying + date
  Right,   // underlying
  Spread,  // left / right legs
  Pair,    // left / right legs
  Basket,  // components
};

ENUM_NAMES(InstrumentType, Spot, Option, Forward, Future, Right, Spread, Pair, Basket)
ENUM_MAPPING(InstrumentType, Spot, Option, Forward, Future, Right, Spread, Pair, Basket)
ENUM_FROM_STRING(InstrumentType)
ENUM_TO_STRING(InstrumentType)

}
