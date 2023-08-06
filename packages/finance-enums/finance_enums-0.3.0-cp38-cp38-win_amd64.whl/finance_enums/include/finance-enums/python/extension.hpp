#pragma once
#include <deque>
#include <iostream>
#include <memory>
#include <pybind11/chrono.h>
#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <string>
#include <vector>
// #include <pybind11_json/pybind11_json.hpp>

#include <finance-enums/common.hpp>
#include <finance-enums/bond.hpp>
#include <finance-enums/commodity.hpp>
#include <finance-enums/country.hpp>
#include <finance-enums/currency.hpp>
#include <finance-enums/equity.hpp>
#include <finance-enums/exchange.hpp>
#include <finance-enums/helpers/exports.hpp>
#include <finance-enums/fund.hpp>
#include <finance-enums/future.hpp>
#include <finance-enums/instrument.hpp>
#include <finance-enums/option.hpp>
#include <finance-enums/sector.hpp>
#include <finance-enums/sector-mappings.hpp>
#include <finance-enums/security.hpp>
#include <finance-enums/trading.hpp>

namespace py = pybind11;
using namespace finance_enums;

PYBIND11_MODULE(extension, m) {
  m.doc() = "C++ bindings to finance-enums library";

  // Bond
  py::enum_<BondType>(m, "BondType", py::arithmetic()) PYBIND_ENUM_VALUE(BondType, Corporate, Government, Municipal)
    .def("__str__", &BondType_to_string, py::prepend())
    .def("__repr__", &BondType_to_repr, py::prepend())
    .def(py::init(&BondType_from_string));

  // Commodity
  py::enum_<CommodityType>(m, "CommodityType", py::arithmetic())
    PYBIND_ENUM_VALUE(CommodityType, Energy, Metals, Agriculture)
      .def("__str__", &CommodityType_to_string, py::prepend())
      .def("__repr__", &CommodityType_to_repr, py::prepend())
      .def(py::init(&CommodityType_from_string));
  py::enum_<EnergyType>(m, "EnergyType", py::arithmetic()) PYBIND_ENUM_VALUE(EnergyType, Crude, NaturalGas)
    .def("__str__", &EnergyType_to_string, py::prepend())
    .def("__repr__", &EnergyType_to_repr, py::prepend())
    .def(py::init(&EnergyType_from_string));
  py::enum_<MetalsType>(m, "MetalsType", py::arithmetic())
    PYBIND_ENUM_VALUE(MetalsType, Gold, Silver, Copper, Platinum, Palladium)
      .def("__str__", &MetalsType_to_string, py::prepend())
      .def("__repr__", &MetalsType_to_repr, py::prepend())
      .def(py::init(&MetalsType_from_string));
  py::enum_<AgricultureType>(m, "AgricultureType", py::arithmetic()) PYBIND_ENUM_VALUE(
    AgricultureType, Corn, Wheat, Oats, Soybean, Cocoa, Coffee, Sugar, Cotten, OrangeJuice, Cattle, Hogs
  )
    .def("__str__", &AgricultureType_to_string, py::prepend())
    .def("__repr__", &AgricultureType_to_repr, py::prepend())
    .def(py::init(&AgricultureType_from_string));

  // Country in long enums

  // Currency in long enums

  // Equity
  py::enum_<EquityType>(m, "EquityType", py::arithmetic()) PYBIND_ENUM_VALUE(
    EquityType, Shares, PreferredShares, ConvertibleShares, PreferredConvertibleShares, DepositoryReceipt
  )
    .def("__str__", &EquityType_to_string, py::prepend())
    .def("__repr__", &EquityType_to_repr, py::prepend())
    .def(py::init(&EquityType_from_string));

  // Exchange
  py::enum_<ExchangeCode>(m, "ExchangeCode", py::arithmetic()) PYBIND_ENUM_VALUE(
    ExchangeCode, XNYS, NYSD, XCIS, CISD, XCHI, ARCX, ARCD, ARCO, XASE, AMXO, XNAS, XNGS, XNCM, XNMS, NASD, XNDQ, XBOS,
    BOSD, XBXO, XPHL, XPSX, PSXD, XPHO, XPBT, XPOR, XNFI, XISE, GMNI, MCRY, XCBO, EDGA, EDGD, EDGX, EDDP, EDGO, BATS,
    BZXD, BATO, BATY, BYXD, C2OX, XCME, FCME, GLBX, XCBT, FCBT, XKBT, XNYM, MIHI, MPRL, EPRL, EPRD, XMIO, EMLD, OTCM,
    CAVE, OTCB, OTCQ, PINL, PINI, PINX, PSGM, PINC, FINR, FINN, FINC, FINY, XADF, FINO, OOTC, OPRA, MEMX, MEMD, MXOP,
    IEXG, LTSE, XCNQ, PURE, CSE2, XTSE, XDRK, VDRK, XTSX, XTNX, XATS, XATX, ADRK, XMOD, XMOC, NEOE, NEOD, NEON, NEOC,
    XXXX, PYPR, SIMU
  )
    .def("__str__", &ExchangeCode_to_string, py::prepend())
    .def("__repr__", &ExchangeCode_to_repr, py::prepend())
    .def(py::init(&ExchangeCode_from_string))
    .def("operating_mic", &Exchange_to_OperatingMic)
    .def("exchange_name", &Exchange_to_Name)
    .def_property_readonly_static("standard", &exchange_standard);

  // Fund
  py::enum_<FundType>(m, "FundType", py::arithmetic()) PYBIND_ENUM_VALUE(FundType, ETF, MutualFund, REIT)
    .def("__str__", &FundType_to_string, py::prepend())
    .def("__repr__", &FundType_to_repr, py::prepend())
    .def(py::init(&FundType_from_string));
  py::enum_<FundSubType>(m, "FundSubType", py::arithmetic())
    PYBIND_ENUM_VALUE(FundSubType, Index, Sector, Active, Passive)
      .def("__str__", &FundSubType_to_string, py::prepend())
      .def("__repr__", &FundSubType_to_repr, py::prepend())
      .def(py::init(&FundSubType_from_string));
  py::enum_<MutualFundEndedness>(m, "MutualFundEndedness", py::arithmetic())
    PYBIND_ENUM_VALUE(MutualFundEndedness, Open, Close)
      .def("__str__", &MutualFundEndedness_to_string, py::prepend())
      .def("__repr__", &MutualFundEndedness_to_repr, py::prepend())
      .def(py::init(&MutualFundEndedness_from_string));

  // Future
  py::enum_<FutureType>(m, "FutureType", py::arithmetic()) PYBIND_ENUM_VALUE(FutureType, Financial, Commodity)
    .def("__str__", &FutureType_to_string, py::prepend())
    .def("__repr__", &FutureType_to_repr, py::prepend())
    .def(py::init(&FutureType_from_string));
  py::enum_<FutureDeliveryType>(m, "FutureDeliveryType", py::arithmetic())
    PYBIND_ENUM_VALUE(FutureDeliveryType, Physical, Cash)
      .def("__str__", &FutureDeliveryType_to_string, py::prepend())
      .def("__repr__", &FutureDeliveryType_to_repr, py::prepend())
      .def(py::init(&FutureDeliveryType_from_string));

  // Instrument
  py::enum_<InstrumentType>(m, "InstrumentType", py::arithmetic())
    PYBIND_ENUM_VALUE(InstrumentType, Spot, Option, Forward, Future, Right, Spread, Pair, Basket)
      .def("__str__", &InstrumentType_to_string, py::prepend())
      .def("__repr__", &InstrumentType_to_repr, py::prepend())
      .def(py::init(&InstrumentType_from_string));

  // Option
  py::enum_<OptionType>(m, "OptionType", py::arithmetic()) PYBIND_ENUM_VALUE(OptionType, Call, Put)
    .def("__str__", &OptionType_to_string, py::prepend())
    .def("__repr__", &OptionType_to_repr, py::prepend())
    .def(py::init(&OptionType_from_string));
  py::enum_<OptionExerciseType>(m, "OptionExerciseType", py::arithmetic())
    PYBIND_ENUM_VALUE(OptionExerciseType, American, European, Bermudan)
      .def("__str__", &OptionExerciseType_to_string, py::prepend())
      .def("__repr__", &OptionExerciseType_to_repr, py::prepend())
      .def(py::init(&OptionExerciseType_from_string));

  // Sector
  py::enum_<Sector>(m, "Sector", py::arithmetic()) PYBIND_ENUM_VALUE(
    Sector, Energy, Materials, Industrials, ConsumerDiscretionary, ConsumerStaples, HealthCare, Financials,
    InformationTechnology, CommunicationServices, Utilities, RealEstate
  )
    .def("__str__", &Sector_to_string, py::prepend())
    .def("__repr__", &Sector_to_repr, py::prepend())
    .def(py::init(&Sector_from_string))
    .def("industry_groups", &Sector_to_IndustryGroup);

  py::enum_<IndustryGroup>(m, "IndustryGroup", py::arithmetic()) PYBIND_ENUM_VALUE(
    IndustryGroup, Energy, Materials, CapitalGoods, CommercialAndProfessionalServices, Transportation,
    AutomobilesAndComponents, ConsumerDurablesAndApparel, ConsumerServices, ConsumerDiscretionaryDistributionAndRetail,
    ConsumerStaplesDistributionAndRetail, FoodBeverageAndTobacco, HouseholdAndPersonalProducts,
    HealthCareEquipmentAndServices, PharmaceuticalsBiotechnologyAndLifeSciences, Banks, FinancialServices, Insurance,
    SoftwareAndServices, TechnologyHardwareAndEquipment, SemiconductorsAndSemiconductorEquipment,
    TelecommunicationServices, MediaAndEntertainment, Utilities, EquityRealEstateInvestmentTrusts,
    RealEstateManagementAndDevelopment
  )
    .def("__str__", &IndustryGroup_to_string, py::prepend())
    .def("__repr__", &IndustryGroup_to_repr, py::prepend())
    .def(py::init(&IndustryGroup_from_string))
    .def("sector", &IndustryGroup_to_Sector)
    .def("industries", &IndustryGroup_to_Industry);

  py::enum_<Industry>(m, "Industry", py::arithmetic()) PYBIND_ENUM_VALUE(
    Industry, EnergyEquipmentAndServices, OilGasAndConsumeableFules, Chemicals, ConstructionMaterials,
    ContainersAndPackaging, MetalsAndMining, PaperAndForestProducts, AerospaceAndDefense, BuildingProducts,
    ConstructionAndEngineering, ElectricalEquipment, IndustrialConglomerates, Machinery,
    TradingCompaniesAndDistributors, CommercialServicesAndSupplies, ProfessionalServices, AirFreightAndLogistics,
    PassengerAirlines, MarineTransportation, GroundTransportation, TransportationInfrastructure, AutomobileComponents,
    Automobiles, HouseholdDurables, LeisureProducts, TextilesApparelAndLuxuryGoods, HotelsRestaurantsAndLeisure,
    DiversifiedConsumerServices, Distributors, BroadlineRetail, SpecialtyRetail, ConsumerStaplesDistributionAndRetail,
    Beverages, FoodProducts, Tobacco, HouseholdProducts, PersonalCareProducts, HealthCareEquipmentAndSupplies,
    HealthCareProvidersAndServices, HealthCareTechnology, Biotechnology, Pharmaceuticals, LifeSciencesToolsAndServices,
    Banks, FinancialServices, ConsumerFinance, CapitalMarkets, MortgageRealEstateInvestmentTrusts, Insurance,
    ITServices, Software, CommunicationsEquipment, TechnologyHardwareStorageAndPeripherals,
    ElectronicEquipmentInstrumentsAndComponents, SemiconductorsAndSemiconductorEquipment,
    DiversifiedTelecommunicationServices, WirelessTelecommunicationServices, Media, Entertainment,
    InteractiveMediaAndServices, ElectricUtilities, GasUtilities, MultiUtilities, WaterUtilities,
    IndependentPowerAndRenewableElectricityProducers, DiversifiedREITs, IndustrialREITs, HotelAndResortREITs,
    OfficeREITs, HealthCareREITs, ResidentialREITs, RetailREITs, SpecializedREITs, RealEstateManagementAndDevelopment
  )
    .def("__str__", &Industry_to_string, py::prepend())
    .def("__repr__", &Industry_to_repr, py::prepend())
    .def(py::init(&Industry_from_string))
    .def("industry_group", &Industry_to_IndustryGroup)
    .def("subindustries", &Industry_to_SubIndustry);

  // Subindustry in long enums

  // Security
  py::enum_<SecurityType>(m, "SecurityType", py::arithmetic()) PYBIND_ENUM_VALUE(
    SecurityType, Equity, Option, Bond, Forward, Future, PerpetualFuture, Spread, Fund, Commodity, Currency, Pair, Index
  )
    .def("__str__", &SecurityType_to_string, py::prepend())
    .def("__repr__", &SecurityType_to_repr, py::prepend())
    .def(py::init(&SecurityType_from_string));

  // Trading
  py::enum_<TradingType>(m, "TradingType", py::arithmetic())
    PYBIND_ENUM_VALUE(TradingType, Live, Simulation, Sandbox, Backtest)
      .def("__str__", &TradingType_to_string, py::prepend())
      .def("__repr__", &TradingType_to_repr, py::prepend())
      .def(py::init(&TradingType_from_string));
  py::enum_<Side>(m, "Side", py::arithmetic()) PYBIND_ENUM_VALUE(Side, None, Buy, Sell)
    .def("__str__", &Side_to_string, py::prepend())
    .def("__repr__", &Side_to_repr, py::prepend())
    .def(py::init(&Side_from_string));
  py::enum_<OrderType>(m, "OrderType", py::arithmetic()) PYBIND_ENUM_VALUE(OrderType, Limit, Market, Stop)
    .def("__str__", &OrderType_to_string, py::prepend())
    .def("__repr__", &OrderType_to_repr, py::prepend())
    .def(py::init(&OrderType_from_string));
  py::enum_<OrderFlag>(m, "OrderFlag", py::arithmetic())
    PYBIND_ENUM_VALUE(OrderFlag, None, FillOrKill, AllOrNone, ImmediateOrCancel)
      .def("__str__", &OrderFlag_to_string, py::prepend())
      .def("__repr__", &OrderFlag_to_repr, py::prepend())
      .def(py::init(&OrderFlag_from_string));
  py::enum_<TimeInForce>(m, "TimeInForce", py::arithmetic()) PYBIND_ENUM_VALUE(TimeInForce, None, Day, GoodTillCanceled)
    .def("__str__", &TimeInForce_to_string, py::prepend())
    .def("__repr__", &TimeInForce_to_repr, py::prepend())
    .def(py::init(&TimeInForce_from_string));

// Long Enums
#include <finance-enums/python/long-enums.hpp>
  /*******************************
   * Helpers
   ******************************/
  // NONE
};
