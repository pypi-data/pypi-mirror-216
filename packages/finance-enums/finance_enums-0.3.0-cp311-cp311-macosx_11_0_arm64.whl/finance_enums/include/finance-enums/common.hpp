#pragma once

#include <chrono>
#include <exception>
#include <sstream>
#include <stdint.h>
#include <string>

#include <finance-enums/helpers/exports.hpp>

// #include <nlohmann/json.hpp>
// #include <date.h>

// using json = nlohmann::json;

namespace finance_enums {
class LIB_EXPORT FinanceEnumsCPPException : public std::exception {
private:
  std::string msg = "";

public:
  explicit FinanceEnumsCPPException(std::string msg)
    : msg(msg) {}

  const char* what() const noexcept override { return msg.c_str(); }
};

typedef std::uint64_t uint_t;
typedef std::string str_t;
typedef std::stringstream sstream_t;

typedef std::chrono::system_clock datetime;
typedef std::chrono::system_clock::time_point timestamp_t;

// inline str_t
// format_timestamp(timestamp_t t) {
//   return date::format("%F %T", t);
// }
}
