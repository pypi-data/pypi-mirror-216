#pragma once
#include <finance-enums/common.hpp>
#include <iostream>

namespace finance_enums {
ENUM(OptionType, Call, Put)
ENUM_FROM_STRING(OptionType)
ENUM_TO_STRING(OptionType)

ENUM(OptionExerciseType, American, European, Bermudan)
ENUM_FROM_STRING(OptionExerciseType)
ENUM_TO_STRING(OptionExerciseType)
}
