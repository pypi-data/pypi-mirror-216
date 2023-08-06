
#pragma once

#include <string>
#include <vector>
#include <unordered_map>

#define ENUM_TO_STRING(type)                                                                     \
  inline std::string type##_to_string(type& typ) { return type##_names[static_cast<int>(typ)]; } \
  inline std::string type##_to_repr(type& typ) { return std::string(#type) + std::string("<") + type##_names[static_cast<int>(typ)] + std::string(">"); }

#ifdef BUILD_PYTHON
#include <pybind11/pybind11.h>
#define ENUM_FROM_STRING(type)                                 \
  type inline type##_from_string(char* s) {                    \
    if(_##type##_mapping.find(s) == _##type##_mapping.end()) { \
      throw pybind11::value_error(s);                          \
    }                                                          \
    return _##type##_mapping[s];                               \
  };
#else
#define ENUM_FROM_STRING(type)                                 \
  type inline type##_from_string(char* s) {                    \
    if(_##type##_mapping.find(s) == _##type##_mapping.end()) { \
      throw FinanceEnumsCPPException(s);                       \
    }                                                          \
    return _##type##_mapping[s];                               \
  };
#endif

#define GET_ENUM_MACRO(_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _17, _18, _19, _20, _21, _22, _23, _24, _25, _26, _27, _28, _29, _30, _31, _32, _33, _34, _35, _36, _37, _38, _39, _40, _41, _42, _43, _44, _45, _46, _47, _48, _49, _50, _51, _52, _53, _54, _55, _56, _57, _58, _59, _60, _61, _62, _63, _64, _65, _66, _67, _68, _69, _70, _71, _72, _73, _74, _75, _76, _77, _78, _79, _80, _81, _82, _83, _84, _85, _86, _87, _88, _89, _90, _91, _92, _93, _94, _95, _96, _97, _98, _99, NAME, ...) NAME
#define ENUM(...) GET_ENUM_MACRO(__VA_ARGS__, ENUM99, ENUM98, ENUM97, ENUM96, ENUM95, ENUM94, ENUM93, ENUM92, ENUM91, ENUM90, ENUM89, ENUM88, ENUM87, ENUM86, ENUM85, ENUM84, ENUM83, ENUM82, ENUM81, ENUM80, ENUM79, ENUM78, ENUM77, ENUM76, ENUM75, ENUM74, ENUM73, ENUM72, ENUM71, ENUM70, ENUM69, ENUM68, ENUM67, ENUM66, ENUM65, ENUM64, ENUM63, ENUM62, ENUM61, ENUM60, ENUM59, ENUM58, ENUM57, ENUM56, ENUM55, ENUM54, ENUM53, ENUM52, ENUM51, ENUM50, ENUM49, ENUM48, ENUM47, ENUM46, ENUM45, ENUM44, ENUM43, ENUM42, ENUM41, ENUM40, ENUM39, ENUM38, ENUM37, ENUM36, ENUM35, ENUM34, ENUM33, ENUM32, ENUM31, ENUM30, ENUM29, ENUM28, ENUM27, ENUM26, ENUM25, ENUM24, ENUM23, ENUM22, ENUM21, ENUM20, ENUM19, ENUM18, ENUM17, ENUM16, ENUM15, ENUM14, ENUM13, ENUM12, ENUM11, ENUM10, ENUM9, ENUM8, ENUM7, ENUM6, ENUM5, ENUM4, ENUM3, ENUM2, ENUM1)(__VA_ARGS__)
#define GET_ENUM_NAMES_MACRO(_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _17, _18, _19, _20, _21, _22, _23, _24, _25, _26, _27, _28, _29, _30, _31, _32, _33, _34, _35, _36, _37, _38, _39, _40, _41, _42, _43, _44, _45, _46, _47, _48, _49, _50, _51, _52, _53, _54, _55, _56, _57, _58, _59, _60, _61, _62, _63, _64, _65, _66, _67, _68, _69, _70, _71, _72, _73, _74, _75, _76, _77, _78, _79, _80, _81, _82, _83, _84, _85, _86, _87, _88, _89, _90, _91, _92, _93, _94, _95, _96, _97, _98, _99, NAME, ...) NAME
#define ENUM_NAMES(...) GET_ENUM_NAMES_MACRO(__VA_ARGS__, ENUM_NAMES99, ENUM_NAMES98, ENUM_NAMES97, ENUM_NAMES96, ENUM_NAMES95, ENUM_NAMES94, ENUM_NAMES93, ENUM_NAMES92, ENUM_NAMES91, ENUM_NAMES90, ENUM_NAMES89, ENUM_NAMES88, ENUM_NAMES87, ENUM_NAMES86, ENUM_NAMES85, ENUM_NAMES84, ENUM_NAMES83, ENUM_NAMES82, ENUM_NAMES81, ENUM_NAMES80, ENUM_NAMES79, ENUM_NAMES78, ENUM_NAMES77, ENUM_NAMES76, ENUM_NAMES75, ENUM_NAMES74, ENUM_NAMES73, ENUM_NAMES72, ENUM_NAMES71, ENUM_NAMES70, ENUM_NAMES69, ENUM_NAMES68, ENUM_NAMES67, ENUM_NAMES66, ENUM_NAMES65, ENUM_NAMES64, ENUM_NAMES63, ENUM_NAMES62, ENUM_NAMES61, ENUM_NAMES60, ENUM_NAMES59, ENUM_NAMES58, ENUM_NAMES57, ENUM_NAMES56, ENUM_NAMES55, ENUM_NAMES54, ENUM_NAMES53, ENUM_NAMES52, ENUM_NAMES51, ENUM_NAMES50, ENUM_NAMES49, ENUM_NAMES48, ENUM_NAMES47, ENUM_NAMES46, ENUM_NAMES45, ENUM_NAMES44, ENUM_NAMES43, ENUM_NAMES42, ENUM_NAMES41, ENUM_NAMES40, ENUM_NAMES39, ENUM_NAMES38, ENUM_NAMES37, ENUM_NAMES36, ENUM_NAMES35, ENUM_NAMES34, ENUM_NAMES33, ENUM_NAMES32, ENUM_NAMES31, ENUM_NAMES30, ENUM_NAMES29, ENUM_NAMES28, ENUM_NAMES27, ENUM_NAMES26, ENUM_NAMES25, ENUM_NAMES24, ENUM_NAMES23, ENUM_NAMES22, ENUM_NAMES21, ENUM_NAMES20, ENUM_NAMES19, ENUM_NAMES18, ENUM_NAMES17, ENUM_NAMES16, ENUM_NAMES15, ENUM_NAMES14, ENUM_NAMES13, ENUM_NAMES12, ENUM_NAMES11, ENUM_NAMES10, ENUM_NAMES9, ENUM_NAMES8, ENUM_NAMES7, ENUM_NAMES6, ENUM_NAMES5, ENUM_NAMES4, ENUM_NAMES3, ENUM_NAMES2, ENUM_NAMES1)(__VA_ARGS__)
#define GET_ENUM_MAPPING_MACRO(_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _17, _18, _19, _20, _21, _22, _23, _24, _25, _26, _27, _28, _29, _30, _31, _32, _33, _34, _35, _36, _37, _38, _39, _40, _41, _42, _43, _44, _45, _46, _47, _48, _49, _50, _51, _52, _53, _54, _55, _56, _57, _58, _59, _60, _61, _62, _63, _64, _65, _66, _67, _68, _69, _70, _71, _72, _73, _74, _75, _76, _77, _78, _79, _80, _81, _82, _83, _84, _85, _86, _87, _88, _89, _90, _91, _92, _93, _94, _95, _96, _97, _98, _99, NAME, ...) NAME
#define ENUM_MAPPING(...) GET_ENUM_MAPPING_MACRO(__VA_ARGS__, ENUM_MAPPING99, ENUM_MAPPING98, ENUM_MAPPING97, ENUM_MAPPING96, ENUM_MAPPING95, ENUM_MAPPING94, ENUM_MAPPING93, ENUM_MAPPING92, ENUM_MAPPING91, ENUM_MAPPING90, ENUM_MAPPING89, ENUM_MAPPING88, ENUM_MAPPING87, ENUM_MAPPING86, ENUM_MAPPING85, ENUM_MAPPING84, ENUM_MAPPING83, ENUM_MAPPING82, ENUM_MAPPING81, ENUM_MAPPING80, ENUM_MAPPING79, ENUM_MAPPING78, ENUM_MAPPING77, ENUM_MAPPING76, ENUM_MAPPING75, ENUM_MAPPING74, ENUM_MAPPING73, ENUM_MAPPING72, ENUM_MAPPING71, ENUM_MAPPING70, ENUM_MAPPING69, ENUM_MAPPING68, ENUM_MAPPING67, ENUM_MAPPING66, ENUM_MAPPING65, ENUM_MAPPING64, ENUM_MAPPING63, ENUM_MAPPING62, ENUM_MAPPING61, ENUM_MAPPING60, ENUM_MAPPING59, ENUM_MAPPING58, ENUM_MAPPING57, ENUM_MAPPING56, ENUM_MAPPING55, ENUM_MAPPING54, ENUM_MAPPING53, ENUM_MAPPING52, ENUM_MAPPING51, ENUM_MAPPING50, ENUM_MAPPING49, ENUM_MAPPING48, ENUM_MAPPING47, ENUM_MAPPING46, ENUM_MAPPING45, ENUM_MAPPING44, ENUM_MAPPING43, ENUM_MAPPING42, ENUM_MAPPING41, ENUM_MAPPING40, ENUM_MAPPING39, ENUM_MAPPING38, ENUM_MAPPING37, ENUM_MAPPING36, ENUM_MAPPING35, ENUM_MAPPING34, ENUM_MAPPING33, ENUM_MAPPING32, ENUM_MAPPING31, ENUM_MAPPING30, ENUM_MAPPING29, ENUM_MAPPING28, ENUM_MAPPING27, ENUM_MAPPING26, ENUM_MAPPING25, ENUM_MAPPING24, ENUM_MAPPING23, ENUM_MAPPING22, ENUM_MAPPING21, ENUM_MAPPING20, ENUM_MAPPING19, ENUM_MAPPING18, ENUM_MAPPING17, ENUM_MAPPING16, ENUM_MAPPING15, ENUM_MAPPING14, ENUM_MAPPING13, ENUM_MAPPING12, ENUM_MAPPING11, ENUM_MAPPING10, ENUM_MAPPING9, ENUM_MAPPING8, ENUM_MAPPING7, ENUM_MAPPING6, ENUM_MAPPING5, ENUM_MAPPING4, ENUM_MAPPING3, ENUM_MAPPING2, ENUM_MAPPING1)(__VA_ARGS__)
#define GET_ENUM_MACRO(_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _17, _18, _19, _20, _21, _22, _23, _24, _25, _26, _27, _28, _29, _30, _31, _32, _33, _34, _35, _36, _37, _38, _39, _40, _41, _42, _43, _44, _45, _46, _47, _48, _49, _50, _51, _52, _53, _54, _55, _56, _57, _58, _59, _60, _61, _62, _63, _64, _65, _66, _67, _68, _69, _70, _71, _72, _73, _74, _75, _76, _77, _78, _79, _80, _81, _82, _83, _84, _85, _86, _87, _88, _89, _90, _91, _92, _93, _94, _95, _96, _97, _98, _99, NAME, ...) NAME
#define PYBIND_ENUM_VALUE(...) GET_ENUM_MACRO(__VA_ARGS__, PYBIND_ENUM_VALUE99, PYBIND_ENUM_VALUE98, PYBIND_ENUM_VALUE97, PYBIND_ENUM_VALUE96, PYBIND_ENUM_VALUE95, PYBIND_ENUM_VALUE94, PYBIND_ENUM_VALUE93, PYBIND_ENUM_VALUE92, PYBIND_ENUM_VALUE91, PYBIND_ENUM_VALUE90, PYBIND_ENUM_VALUE89, PYBIND_ENUM_VALUE88, PYBIND_ENUM_VALUE87, PYBIND_ENUM_VALUE86, PYBIND_ENUM_VALUE85, PYBIND_ENUM_VALUE84, PYBIND_ENUM_VALUE83, PYBIND_ENUM_VALUE82, PYBIND_ENUM_VALUE81, PYBIND_ENUM_VALUE80, PYBIND_ENUM_VALUE79, PYBIND_ENUM_VALUE78, PYBIND_ENUM_VALUE77, PYBIND_ENUM_VALUE76, PYBIND_ENUM_VALUE75, PYBIND_ENUM_VALUE74, PYBIND_ENUM_VALUE73, PYBIND_ENUM_VALUE72, PYBIND_ENUM_VALUE71, PYBIND_ENUM_VALUE70, PYBIND_ENUM_VALUE69, PYBIND_ENUM_VALUE68, PYBIND_ENUM_VALUE67, PYBIND_ENUM_VALUE66, PYBIND_ENUM_VALUE65, PYBIND_ENUM_VALUE64, PYBIND_ENUM_VALUE63, PYBIND_ENUM_VALUE62, PYBIND_ENUM_VALUE61, PYBIND_ENUM_VALUE60, PYBIND_ENUM_VALUE59, PYBIND_ENUM_VALUE58, PYBIND_ENUM_VALUE57, PYBIND_ENUM_VALUE56, PYBIND_ENUM_VALUE55, PYBIND_ENUM_VALUE54, PYBIND_ENUM_VALUE53, PYBIND_ENUM_VALUE52, PYBIND_ENUM_VALUE51, PYBIND_ENUM_VALUE50, PYBIND_ENUM_VALUE49, PYBIND_ENUM_VALUE48, PYBIND_ENUM_VALUE47, PYBIND_ENUM_VALUE46, PYBIND_ENUM_VALUE45, PYBIND_ENUM_VALUE44, PYBIND_ENUM_VALUE43, PYBIND_ENUM_VALUE42, PYBIND_ENUM_VALUE41, PYBIND_ENUM_VALUE40, PYBIND_ENUM_VALUE39, PYBIND_ENUM_VALUE38, PYBIND_ENUM_VALUE37, PYBIND_ENUM_VALUE36, PYBIND_ENUM_VALUE35, PYBIND_ENUM_VALUE34, PYBIND_ENUM_VALUE33, PYBIND_ENUM_VALUE32, PYBIND_ENUM_VALUE31, PYBIND_ENUM_VALUE30, PYBIND_ENUM_VALUE29, PYBIND_ENUM_VALUE28, PYBIND_ENUM_VALUE27, PYBIND_ENUM_VALUE26, PYBIND_ENUM_VALUE25, PYBIND_ENUM_VALUE24, PYBIND_ENUM_VALUE23, PYBIND_ENUM_VALUE22, PYBIND_ENUM_VALUE21, PYBIND_ENUM_VALUE20, PYBIND_ENUM_VALUE19, PYBIND_ENUM_VALUE18, PYBIND_ENUM_VALUE17, PYBIND_ENUM_VALUE16, PYBIND_ENUM_VALUE15, PYBIND_ENUM_VALUE14, PYBIND_ENUM_VALUE13, PYBIND_ENUM_VALUE12, PYBIND_ENUM_VALUE11, PYBIND_ENUM_VALUE10, PYBIND_ENUM_VALUE9, PYBIND_ENUM_VALUE8, PYBIND_ENUM_VALUE7, PYBIND_ENUM_VALUE6, PYBIND_ENUM_VALUE5, PYBIND_ENUM_VALUE4, PYBIND_ENUM_VALUE3, PYBIND_ENUM_VALUE2, PYBIND_ENUM_VALUE1)(__VA_ARGS__)

#define ENUM_NAMES2(name, v1, v2)\
static const std::vector<str_t> name##_names = {#v1, #v2};
#define ENUM_MAPPING2(name, v1, v2)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}};
#define ENUM2(name, v1, v2)\
enum class LIB_EXPORT name { v1, v2};\
ENUM_NAMES(name, v1, v2)\
ENUM_MAPPING(name, v1, v2)
#define PYBIND_ENUM_VALUE2(name, v1, v2)\
.value(#v1, name::v1).value(#v2, name::v2)

#define ENUM_NAMES3(name, v1, v2, v3)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3};
#define ENUM_MAPPING3(name, v1, v2, v3)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}};
#define ENUM3(name, v1, v2, v3)\
enum class LIB_EXPORT name { v1, v2, v3};\
ENUM_NAMES(name, v1, v2, v3)\
ENUM_MAPPING(name, v1, v2, v3)
#define PYBIND_ENUM_VALUE3(name, v1, v2, v3)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3)

#define ENUM_NAMES4(name, v1, v2, v3, v4)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4};
#define ENUM_MAPPING4(name, v1, v2, v3, v4)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}};
#define ENUM4(name, v1, v2, v3, v4)\
enum class LIB_EXPORT name { v1, v2, v3, v4};\
ENUM_NAMES(name, v1, v2, v3, v4)\
ENUM_MAPPING(name, v1, v2, v3, v4)
#define PYBIND_ENUM_VALUE4(name, v1, v2, v3, v4)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4)

#define ENUM_NAMES5(name, v1, v2, v3, v4, v5)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5};
#define ENUM_MAPPING5(name, v1, v2, v3, v4, v5)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}};
#define ENUM5(name, v1, v2, v3, v4, v5)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5};\
ENUM_NAMES(name, v1, v2, v3, v4, v5)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5)
#define PYBIND_ENUM_VALUE5(name, v1, v2, v3, v4, v5)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5)

#define ENUM_NAMES6(name, v1, v2, v3, v4, v5, v6)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6};
#define ENUM_MAPPING6(name, v1, v2, v3, v4, v5, v6)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}};
#define ENUM6(name, v1, v2, v3, v4, v5, v6)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6)
#define PYBIND_ENUM_VALUE6(name, v1, v2, v3, v4, v5, v6)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6)

#define ENUM_NAMES7(name, v1, v2, v3, v4, v5, v6, v7)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7};
#define ENUM_MAPPING7(name, v1, v2, v3, v4, v5, v6, v7)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}};
#define ENUM7(name, v1, v2, v3, v4, v5, v6, v7)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7)
#define PYBIND_ENUM_VALUE7(name, v1, v2, v3, v4, v5, v6, v7)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7)

#define ENUM_NAMES8(name, v1, v2, v3, v4, v5, v6, v7, v8)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8};
#define ENUM_MAPPING8(name, v1, v2, v3, v4, v5, v6, v7, v8)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}};
#define ENUM8(name, v1, v2, v3, v4, v5, v6, v7, v8)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8)
#define PYBIND_ENUM_VALUE8(name, v1, v2, v3, v4, v5, v6, v7, v8)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8)

#define ENUM_NAMES9(name, v1, v2, v3, v4, v5, v6, v7, v8, v9)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8, #v9};
#define ENUM_MAPPING9(name, v1, v2, v3, v4, v5, v6, v7, v8, v9)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}, {#v9, name::v9}};
#define ENUM9(name, v1, v2, v3, v4, v5, v6, v7, v8, v9)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8, v9};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8, v9)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8, v9)
#define PYBIND_ENUM_VALUE9(name, v1, v2, v3, v4, v5, v6, v7, v8, v9)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8).value(#v9, name::v9)

#define ENUM_NAMES10(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8, #v9, #v10};
#define ENUM_MAPPING10(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}, {#v9, name::v9}, {#v10, name::v10}};
#define ENUM10(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8, v9, v10};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10)
#define PYBIND_ENUM_VALUE10(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8).value(#v9, name::v9).value(#v10, name::v10)

#define ENUM_NAMES11(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8, #v9, #v10, #v11};
#define ENUM_MAPPING11(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}, {#v9, name::v9}, {#v10, name::v10}, {#v11, name::v11}};
#define ENUM11(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)
#define PYBIND_ENUM_VALUE11(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8).value(#v9, name::v9).value(#v10, name::v10).value(#v11, name::v11)

#define ENUM_NAMES12(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8, #v9, #v10, #v11, #v12};
#define ENUM_MAPPING12(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}, {#v9, name::v9}, {#v10, name::v10}, {#v11, name::v11}, {#v12, name::v12}};
#define ENUM12(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12)
#define PYBIND_ENUM_VALUE12(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8).value(#v9, name::v9).value(#v10, name::v10).value(#v11, name::v11).value(#v12, name::v12)

#define ENUM_NAMES13(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8, #v9, #v10, #v11, #v12, #v13};
#define ENUM_MAPPING13(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}, {#v9, name::v9}, {#v10, name::v10}, {#v11, name::v11}, {#v12, name::v12}, {#v13, name::v13}};
#define ENUM13(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13)
#define PYBIND_ENUM_VALUE13(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8).value(#v9, name::v9).value(#v10, name::v10).value(#v11, name::v11).value(#v12, name::v12).value(#v13, name::v13)

#define ENUM_NAMES14(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8, #v9, #v10, #v11, #v12, #v13, #v14};
#define ENUM_MAPPING14(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}, {#v9, name::v9}, {#v10, name::v10}, {#v11, name::v11}, {#v12, name::v12}, {#v13, name::v13}, {#v14, name::v14}};
#define ENUM14(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14)
#define PYBIND_ENUM_VALUE14(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8).value(#v9, name::v9).value(#v10, name::v10).value(#v11, name::v11).value(#v12, name::v12).value(#v13, name::v13).value(#v14, name::v14)

#define ENUM_NAMES15(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8, #v9, #v10, #v11, #v12, #v13, #v14, #v15};
#define ENUM_MAPPING15(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}, {#v9, name::v9}, {#v10, name::v10}, {#v11, name::v11}, {#v12, name::v12}, {#v13, name::v13}, {#v14, name::v14}, {#v15, name::v15}};
#define ENUM15(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)
#define PYBIND_ENUM_VALUE15(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8).value(#v9, name::v9).value(#v10, name::v10).value(#v11, name::v11).value(#v12, name::v12).value(#v13, name::v13).value(#v14, name::v14).value(#v15, name::v15)

#define ENUM_NAMES16(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8, #v9, #v10, #v11, #v12, #v13, #v14, #v15, #v16};
#define ENUM_MAPPING16(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}, {#v9, name::v9}, {#v10, name::v10}, {#v11, name::v11}, {#v12, name::v12}, {#v13, name::v13}, {#v14, name::v14}, {#v15, name::v15}, {#v16, name::v16}};
#define ENUM16(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16)
#define PYBIND_ENUM_VALUE16(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8).value(#v9, name::v9).value(#v10, name::v10).value(#v11, name::v11).value(#v12, name::v12).value(#v13, name::v13).value(#v14, name::v14).value(#v15, name::v15).value(#v16, name::v16)

#define ENUM_NAMES25(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8, #v9, #v10, #v11, #v12, #v13, #v14, #v15, #v16, #v17, #v18, #v19, #v20, #v21, #v22, #v23, #v24, #v25};
#define ENUM_MAPPING25(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}, {#v9, name::v9}, {#v10, name::v10}, {#v11, name::v11}, {#v12, name::v12}, {#v13, name::v13}, {#v14, name::v14}, {#v15, name::v15}, {#v16, name::v16}, {#v17, name::v17}, {#v18, name::v18}, {#v19, name::v19}, {#v20, name::v20}, {#v21, name::v21}, {#v22, name::v22}, {#v23, name::v23}, {#v24, name::v24}, {#v25, name::v25}};
#define ENUM25(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25)
#define PYBIND_ENUM_VALUE25(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8).value(#v9, name::v9).value(#v10, name::v10).value(#v11, name::v11).value(#v12, name::v12).value(#v13, name::v13).value(#v14, name::v14).value(#v15, name::v15).value(#v16, name::v16).value(#v17, name::v17).value(#v18, name::v18).value(#v19, name::v19).value(#v20, name::v20).value(#v21, name::v21).value(#v22, name::v22).value(#v23, name::v23).value(#v24, name::v24).value(#v25, name::v25)

#define ENUM_NAMES74(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8, #v9, #v10, #v11, #v12, #v13, #v14, #v15, #v16, #v17, #v18, #v19, #v20, #v21, #v22, #v23, #v24, #v25, #v26, #v27, #v28, #v29, #v30, #v31, #v32, #v33, #v34, #v35, #v36, #v37, #v38, #v39, #v40, #v41, #v42, #v43, #v44, #v45, #v46, #v47, #v48, #v49, #v50, #v51, #v52, #v53, #v54, #v55, #v56, #v57, #v58, #v59, #v60, #v61, #v62, #v63, #v64, #v65, #v66, #v67, #v68, #v69, #v70, #v71, #v72, #v73, #v74};
#define ENUM_MAPPING74(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}, {#v9, name::v9}, {#v10, name::v10}, {#v11, name::v11}, {#v12, name::v12}, {#v13, name::v13}, {#v14, name::v14}, {#v15, name::v15}, {#v16, name::v16}, {#v17, name::v17}, {#v18, name::v18}, {#v19, name::v19}, {#v20, name::v20}, {#v21, name::v21}, {#v22, name::v22}, {#v23, name::v23}, {#v24, name::v24}, {#v25, name::v25}, {#v26, name::v26}, {#v27, name::v27}, {#v28, name::v28}, {#v29, name::v29}, {#v30, name::v30}, {#v31, name::v31}, {#v32, name::v32}, {#v33, name::v33}, {#v34, name::v34}, {#v35, name::v35}, {#v36, name::v36}, {#v37, name::v37}, {#v38, name::v38}, {#v39, name::v39}, {#v40, name::v40}, {#v41, name::v41}, {#v42, name::v42}, {#v43, name::v43}, {#v44, name::v44}, {#v45, name::v45}, {#v46, name::v46}, {#v47, name::v47}, {#v48, name::v48}, {#v49, name::v49}, {#v50, name::v50}, {#v51, name::v51}, {#v52, name::v52}, {#v53, name::v53}, {#v54, name::v54}, {#v55, name::v55}, {#v56, name::v56}, {#v57, name::v57}, {#v58, name::v58}, {#v59, name::v59}, {#v60, name::v60}, {#v61, name::v61}, {#v62, name::v62}, {#v63, name::v63}, {#v64, name::v64}, {#v65, name::v65}, {#v66, name::v66}, {#v67, name::v67}, {#v68, name::v68}, {#v69, name::v69}, {#v70, name::v70}, {#v71, name::v71}, {#v72, name::v72}, {#v73, name::v73}, {#v74, name::v74}};
#define ENUM74(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74)
#define PYBIND_ENUM_VALUE74(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8).value(#v9, name::v9).value(#v10, name::v10).value(#v11, name::v11).value(#v12, name::v12).value(#v13, name::v13).value(#v14, name::v14).value(#v15, name::v15).value(#v16, name::v16).value(#v17, name::v17).value(#v18, name::v18).value(#v19, name::v19).value(#v20, name::v20).value(#v21, name::v21).value(#v22, name::v22).value(#v23, name::v23).value(#v24, name::v24).value(#v25, name::v25).value(#v26, name::v26).value(#v27, name::v27).value(#v28, name::v28).value(#v29, name::v29).value(#v30, name::v30).value(#v31, name::v31).value(#v32, name::v32).value(#v33, name::v33).value(#v34, name::v34).value(#v35, name::v35).value(#v36, name::v36).value(#v37, name::v37).value(#v38, name::v38).value(#v39, name::v39).value(#v40, name::v40).value(#v41, name::v41).value(#v42, name::v42).value(#v43, name::v43).value(#v44, name::v44).value(#v45, name::v45).value(#v46, name::v46).value(#v47, name::v47).value(#v48, name::v48).value(#v49, name::v49).value(#v50, name::v50).value(#v51, name::v51).value(#v52, name::v52).value(#v53, name::v53).value(#v54, name::v54).value(#v55, name::v55).value(#v56, name::v56).value(#v57, name::v57).value(#v58, name::v58).value(#v59, name::v59).value(#v60, name::v60).value(#v61, name::v61).value(#v62, name::v62).value(#v63, name::v63).value(#v64, name::v64).value(#v65, name::v65).value(#v66, name::v66).value(#v67, name::v67).value(#v68, name::v68).value(#v69, name::v69).value(#v70, name::v70).value(#v71, name::v71).value(#v72, name::v72).value(#v73, name::v73).value(#v74, name::v74)

#define ENUM_NAMES96(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74, v75, v76, v77, v78, v79, v80, v81, v82, v83, v84, v85, v86, v87, v88, v89, v90, v91, v92, v93, v94, v95, v96)\
static const std::vector<str_t> name##_names = {#v1, #v2, #v3, #v4, #v5, #v6, #v7, #v8, #v9, #v10, #v11, #v12, #v13, #v14, #v15, #v16, #v17, #v18, #v19, #v20, #v21, #v22, #v23, #v24, #v25, #v26, #v27, #v28, #v29, #v30, #v31, #v32, #v33, #v34, #v35, #v36, #v37, #v38, #v39, #v40, #v41, #v42, #v43, #v44, #v45, #v46, #v47, #v48, #v49, #v50, #v51, #v52, #v53, #v54, #v55, #v56, #v57, #v58, #v59, #v60, #v61, #v62, #v63, #v64, #v65, #v66, #v67, #v68, #v69, #v70, #v71, #v72, #v73, #v74, #v75, #v76, #v77, #v78, #v79, #v80, #v81, #v82, #v83, #v84, #v85, #v86, #v87, #v88, #v89, #v90, #v91, #v92, #v93, #v94, #v95, #v96};
#define ENUM_MAPPING96(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74, v75, v76, v77, v78, v79, v80, v81, v82, v83, v84, v85, v86, v87, v88, v89, v90, v91, v92, v93, v94, v95, v96)\
static std::unordered_map<str_t, name> _##name##_mapping = {{#v1, name::v1}, {#v2, name::v2}, {#v3, name::v3}, {#v4, name::v4}, {#v5, name::v5}, {#v6, name::v6}, {#v7, name::v7}, {#v8, name::v8}, {#v9, name::v9}, {#v10, name::v10}, {#v11, name::v11}, {#v12, name::v12}, {#v13, name::v13}, {#v14, name::v14}, {#v15, name::v15}, {#v16, name::v16}, {#v17, name::v17}, {#v18, name::v18}, {#v19, name::v19}, {#v20, name::v20}, {#v21, name::v21}, {#v22, name::v22}, {#v23, name::v23}, {#v24, name::v24}, {#v25, name::v25}, {#v26, name::v26}, {#v27, name::v27}, {#v28, name::v28}, {#v29, name::v29}, {#v30, name::v30}, {#v31, name::v31}, {#v32, name::v32}, {#v33, name::v33}, {#v34, name::v34}, {#v35, name::v35}, {#v36, name::v36}, {#v37, name::v37}, {#v38, name::v38}, {#v39, name::v39}, {#v40, name::v40}, {#v41, name::v41}, {#v42, name::v42}, {#v43, name::v43}, {#v44, name::v44}, {#v45, name::v45}, {#v46, name::v46}, {#v47, name::v47}, {#v48, name::v48}, {#v49, name::v49}, {#v50, name::v50}, {#v51, name::v51}, {#v52, name::v52}, {#v53, name::v53}, {#v54, name::v54}, {#v55, name::v55}, {#v56, name::v56}, {#v57, name::v57}, {#v58, name::v58}, {#v59, name::v59}, {#v60, name::v60}, {#v61, name::v61}, {#v62, name::v62}, {#v63, name::v63}, {#v64, name::v64}, {#v65, name::v65}, {#v66, name::v66}, {#v67, name::v67}, {#v68, name::v68}, {#v69, name::v69}, {#v70, name::v70}, {#v71, name::v71}, {#v72, name::v72}, {#v73, name::v73}, {#v74, name::v74}, {#v75, name::v75}, {#v76, name::v76}, {#v77, name::v77}, {#v78, name::v78}, {#v79, name::v79}, {#v80, name::v80}, {#v81, name::v81}, {#v82, name::v82}, {#v83, name::v83}, {#v84, name::v84}, {#v85, name::v85}, {#v86, name::v86}, {#v87, name::v87}, {#v88, name::v88}, {#v89, name::v89}, {#v90, name::v90}, {#v91, name::v91}, {#v92, name::v92}, {#v93, name::v93}, {#v94, name::v94}, {#v95, name::v95}, {#v96, name::v96}};
#define ENUM96(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74, v75, v76, v77, v78, v79, v80, v81, v82, v83, v84, v85, v86, v87, v88, v89, v90, v91, v92, v93, v94, v95, v96)\
enum class LIB_EXPORT name { v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74, v75, v76, v77, v78, v79, v80, v81, v82, v83, v84, v85, v86, v87, v88, v89, v90, v91, v92, v93, v94, v95, v96};\
ENUM_NAMES(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74, v75, v76, v77, v78, v79, v80, v81, v82, v83, v84, v85, v86, v87, v88, v89, v90, v91, v92, v93, v94, v95, v96)\
ENUM_MAPPING(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74, v75, v76, v77, v78, v79, v80, v81, v82, v83, v84, v85, v86, v87, v88, v89, v90, v91, v92, v93, v94, v95, v96)
#define PYBIND_ENUM_VALUE96(name, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40, v41, v42, v43, v44, v45, v46, v47, v48, v49, v50, v51, v52, v53, v54, v55, v56, v57, v58, v59, v60, v61, v62, v63, v64, v65, v66, v67, v68, v69, v70, v71, v72, v73, v74, v75, v76, v77, v78, v79, v80, v81, v82, v83, v84, v85, v86, v87, v88, v89, v90, v91, v92, v93, v94, v95, v96)\
.value(#v1, name::v1).value(#v2, name::v2).value(#v3, name::v3).value(#v4, name::v4).value(#v5, name::v5).value(#v6, name::v6).value(#v7, name::v7).value(#v8, name::v8).value(#v9, name::v9).value(#v10, name::v10).value(#v11, name::v11).value(#v12, name::v12).value(#v13, name::v13).value(#v14, name::v14).value(#v15, name::v15).value(#v16, name::v16).value(#v17, name::v17).value(#v18, name::v18).value(#v19, name::v19).value(#v20, name::v20).value(#v21, name::v21).value(#v22, name::v22).value(#v23, name::v23).value(#v24, name::v24).value(#v25, name::v25).value(#v26, name::v26).value(#v27, name::v27).value(#v28, name::v28).value(#v29, name::v29).value(#v30, name::v30).value(#v31, name::v31).value(#v32, name::v32).value(#v33, name::v33).value(#v34, name::v34).value(#v35, name::v35).value(#v36, name::v36).value(#v37, name::v37).value(#v38, name::v38).value(#v39, name::v39).value(#v40, name::v40).value(#v41, name::v41).value(#v42, name::v42).value(#v43, name::v43).value(#v44, name::v44).value(#v45, name::v45).value(#v46, name::v46).value(#v47, name::v47).value(#v48, name::v48).value(#v49, name::v49).value(#v50, name::v50).value(#v51, name::v51).value(#v52, name::v52).value(#v53, name::v53).value(#v54, name::v54).value(#v55, name::v55).value(#v56, name::v56).value(#v57, name::v57).value(#v58, name::v58).value(#v59, name::v59).value(#v60, name::v60).value(#v61, name::v61).value(#v62, name::v62).value(#v63, name::v63).value(#v64, name::v64).value(#v65, name::v65).value(#v66, name::v66).value(#v67, name::v67).value(#v68, name::v68).value(#v69, name::v69).value(#v70, name::v70).value(#v71, name::v71).value(#v72, name::v72).value(#v73, name::v73).value(#v74, name::v74).value(#v75, name::v75).value(#v76, name::v76).value(#v77, name::v77).value(#v78, name::v78).value(#v79, name::v79).value(#v80, name::v80).value(#v81, name::v81).value(#v82, name::v82).value(#v83, name::v83).value(#v84, name::v84).value(#v85, name::v85).value(#v86, name::v86).value(#v87, name::v87).value(#v88, name::v88).value(#v89, name::v89).value(#v90, name::v90).value(#v91, name::v91).value(#v92, name::v92).value(#v93, name::v93).value(#v94, name::v94).value(#v95, name::v95).value(#v96, name::v96)

