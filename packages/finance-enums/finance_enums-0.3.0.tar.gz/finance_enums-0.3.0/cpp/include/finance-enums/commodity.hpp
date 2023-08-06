#pragma once
#include <finance-enums/helpers/enum.hpp>

namespace finance_enums {
ENUM(CommodityType, Energy, Metals, Agriculture)
ENUM_FROM_STRING(CommodityType)
ENUM_TO_STRING(CommodityType)

ENUM(EnergyType, Crude, NaturalGas)
ENUM_FROM_STRING(EnergyType)
ENUM_TO_STRING(EnergyType)

ENUM(MetalsType, Gold, Silver, Copper, Platinum, Palladium)
ENUM_FROM_STRING(MetalsType)
ENUM_TO_STRING(MetalsType)

ENUM(AgricultureType, Corn, Wheat, Oats, Soybean, Cocoa, Coffee, Sugar, Cotten, OrangeJuice, Cattle, Hogs)
ENUM_FROM_STRING(AgricultureType)
ENUM_TO_STRING(AgricultureType)
}
