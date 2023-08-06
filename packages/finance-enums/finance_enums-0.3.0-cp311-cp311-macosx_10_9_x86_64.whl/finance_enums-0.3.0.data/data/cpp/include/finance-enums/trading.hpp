#pragma once
#include <finance-enums/common.hpp>
#include <iostream>

namespace finance_enums {
ENUM(TradingType, Live, Simulation, Sandbox, Backtest)
ENUM_FROM_STRING(TradingType)
ENUM_TO_STRING(TradingType)

ENUM(Side, None, Buy, Sell)
ENUM_FROM_STRING(Side)
ENUM_TO_STRING(Side)

ENUM(OrderType, Limit, Market, Stop)
ENUM_FROM_STRING(OrderType)
ENUM_TO_STRING(OrderType)

ENUM(OrderFlag, None, FillOrKill, AllOrNone, ImmediateOrCancel)
ENUM_FROM_STRING(OrderFlag)
ENUM_TO_STRING(OrderFlag)

ENUM(TimeInForce, None, Day, GoodTillCanceled)
ENUM_FROM_STRING(TimeInForce)
ENUM_TO_STRING(TimeInForce)
}
