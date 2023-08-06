#pragma once
#include <finance-enums/common.hpp>
#include <finance-enums/helpers/exports.hpp>
#include <iostream>
#include <vector>

namespace finance_enums {

enum class IndustryGroup;
enum class LIB_EXPORT Sector {
  Energy,
  Materials,
  Industrials,
  ConsumerDiscretionary,
  ConsumerStaples,
  HealthCare,
  Financials,
  InformationTechnology,
  CommunicationServices,
  Utilities,
  RealEstate
};

ENUM_NAMES(
  Sector, Energy, Materials, Industrials, ConsumerDiscretionary, ConsumerStaples, HealthCare, Financials,
  InformationTechnology, CommunicationServices, Utilities, RealEstate
)
ENUM_MAPPING(
  Sector, Energy, Materials, Industrials, ConsumerDiscretionary, ConsumerStaples, HealthCare, Financials,
  InformationTechnology, CommunicationServices, Utilities, RealEstate
)
ENUM_FROM_STRING(Sector)
ENUM_TO_STRING(Sector)

enum class LIB_EXPORT IndustryGroup {
  // Energy
  Energy,
  // Materials
  Materials,
  // Industrials
  CapitalGoods,
  CommercialAndProfessionalServices,
  Transportation,
  // Consumer Discretionary
  AutomobilesAndComponents,
  ConsumerDurablesAndApparel,
  ConsumerServices,
  ConsumerDiscretionaryDistributionAndRetail,
  // Consumer Staples
  ConsumerStaplesDistributionAndRetail,
  FoodBeverageAndTobacco,
  HouseholdAndPersonalProducts,
  // Health Care
  HealthCareEquipmentAndServices,
  PharmaceuticalsBiotechnologyAndLifeSciences,
  // Financials
  Banks,
  FinancialServices,
  Insurance,
  // Information Technology
  SoftwareAndServices,
  TechnologyHardwareAndEquipment,
  SemiconductorsAndSemiconductorEquipment,
  // Communication Services
  TelecommunicationServices,
  MediaAndEntertainment,
  // Utilities
  Utilities,
  // Real Estate
  EquityRealEstateInvestmentTrusts,
  RealEstateManagementAndDevelopment
};

ENUM_NAMES(
  IndustryGroup, Energy, Materials, CapitalGoods, CommercialAndProfessionalServices, Transportation,
  AutomobilesAndComponents, ConsumerDurablesAndApparel, ConsumerServices, ConsumerDiscretionaryDistributionAndRetail,
  ConsumerStaplesDistributionAndRetail, FoodBeverageAndTobacco, HouseholdAndPersonalProducts,
  HealthCareEquipmentAndServices, PharmaceuticalsBiotechnologyAndLifeSciences, Banks, FinancialServices, Insurance,
  SoftwareAndServices, TechnologyHardwareAndEquipment, SemiconductorsAndSemiconductorEquipment,
  TelecommunicationServices, MediaAndEntertainment, Utilities, EquityRealEstateInvestmentTrusts,
  RealEstateManagementAndDevelopment
)
ENUM_MAPPING(
  IndustryGroup, Energy, Materials, CapitalGoods, CommercialAndProfessionalServices, Transportation,
  AutomobilesAndComponents, ConsumerDurablesAndApparel, ConsumerServices, ConsumerDiscretionaryDistributionAndRetail,
  ConsumerStaplesDistributionAndRetail, FoodBeverageAndTobacco, HouseholdAndPersonalProducts,
  HealthCareEquipmentAndServices, PharmaceuticalsBiotechnologyAndLifeSciences, Banks, FinancialServices, Insurance,
  SoftwareAndServices, TechnologyHardwareAndEquipment, SemiconductorsAndSemiconductorEquipment,
  TelecommunicationServices, MediaAndEntertainment, Utilities, EquityRealEstateInvestmentTrusts,
  RealEstateManagementAndDevelopment
)
ENUM_FROM_STRING(IndustryGroup)
ENUM_TO_STRING(IndustryGroup)

enum class LIB_EXPORT Industry {
  // Energy
  EnergyEquipmentAndServices,
  OilGasAndConsumeableFules,
  // Materials,
  Chemicals,
  ConstructionMaterials,
  ContainersAndPackaging,
  MetalsAndMining,
  PaperAndForestProducts,
  // Industrials -> Capital Goods
  AerospaceAndDefense,
  BuildingProducts,
  ConstructionAndEngineering,
  ElectricalEquipment,
  IndustrialConglomerates,
  Machinery,
  TradingCompaniesAndDistributors,
  // Industrials -> Commercial and Professional Services
  CommercialServicesAndSupplies,
  ProfessionalServices,
  // Industrials -> Transportation
  AirFreightAndLogistics,
  PassengerAirlines,
  MarineTransportation,
  GroundTransportation,
  TransportationInfrastructure,
  // Consumer Discretionary -> Automobiles and Components
  AutomobileComponents,
  Automobiles,
  // Consumer Discretionary -> Consumer Durables and Apparel
  HouseholdDurables,
  LeisureProducts,
  TextilesApparelAndLuxuryGoods,
  // Consumer Discretionary -> Consumer Services
  HotelsRestaurantsAndLeisure,
  DiversifiedConsumerServices,
  // Consumer Discretionary -> Consumer Discretionary Distribution and Retail
  Distributors,
  BroadlineRetail,
  SpecialtyRetail,
  // Consumer Staples -> Consumer Staples Distribution And Retail
  ConsumerStaplesDistributionAndRetail,
  // Consumer Staples -> Food, Beverage, and Tobacco
  Beverages,
  FoodProducts,
  Tobacco,
  // Consumer Staples -> Household and Personal Products
  HouseholdProducts,
  PersonalCareProducts,
  // Health Care -> Health Care Equipment and Services
  HealthCareEquipmentAndSupplies,
  HealthCareProvidersAndServices,
  HealthCareTechnology,
  // Health Care -> Pharmaceuticals, Biotechnology, and Life Sciences
  Biotechnology,
  Pharmaceuticals,
  LifeSciencesToolsAndServices,
  // Financials -> Banks
  Banks,
  // Financials -> Financial Services
  FinancialServices,
  ConsumerFinance,
  CapitalMarkets,
  MortgageRealEstateInvestmentTrusts,
  // Financials -> Insurance
  Insurance,
  // Information Technology -> Software and Services
  ITServices,
  Software,
  // Information Technology -> Technology Equipment and Hardware
  CommunicationsEquipment,
  TechnologyHardwareStorageAndPeripherals,
  ElectronicEquipmentInstrumentsAndComponents,
  // Information Technology -> Semiconductors and Semiconductor Equipment
  SemiconductorsAndSemiconductorEquipment,
  // Communication Services -> Telecommunication Services
  DiversifiedTelecommunicationServices,
  WirelessTelecommunicationServices,
  // Communication Services -> Media and Entertainment
  Media,
  Entertainment,
  InteractiveMediaAndServices,
  // Utilities
  ElectricUtilities,
  GasUtilities,
  MultiUtilities,
  WaterUtilities,
  IndependentPowerAndRenewableElectricityProducers,
  // Real Estate -> Equity REITs
  DiversifiedREITs,
  IndustrialREITs,
  HotelAndResortREITs,
  OfficeREITs,
  HealthCareREITs,
  ResidentialREITs,
  RetailREITs,
  SpecializedREITs,
  // Real Estate -> Real Estate Management and Development
  RealEstateManagementAndDevelopment,
};

ENUM_NAMES(
  Industry, EnergyEquipmentAndServices, OilGasAndConsumeableFules, Chemicals, ConstructionMaterials,
  ContainersAndPackaging, MetalsAndMining, PaperAndForestProducts, AerospaceAndDefense, BuildingProducts,
  ConstructionAndEngineering, ElectricalEquipment, IndustrialConglomerates, Machinery, TradingCompaniesAndDistributors,
  CommercialServicesAndSupplies, ProfessionalServices, AirFreightAndLogistics, PassengerAirlines, MarineTransportation,
  GroundTransportation, TransportationInfrastructure, AutomobileComponents, Automobiles, HouseholdDurables,
  LeisureProducts, TextilesApparelAndLuxuryGoods, HotelsRestaurantsAndLeisure, DiversifiedConsumerServices,
  Distributors, BroadlineRetail, SpecialtyRetail, ConsumerStaplesDistributionAndRetail, Beverages, FoodProducts,
  Tobacco, HouseholdProducts, PersonalCareProducts, HealthCareEquipmentAndSupplies, HealthCareProvidersAndServices,
  HealthCareTechnology, Biotechnology, Pharmaceuticals, LifeSciencesToolsAndServices, Banks, FinancialServices,
  ConsumerFinance, CapitalMarkets, MortgageRealEstateInvestmentTrusts, Insurance, ITServices, Software,
  CommunicationsEquipment, TechnologyHardwareStorageAndPeripherals, ElectronicEquipmentInstrumentsAndComponents,
  SemiconductorsAndSemiconductorEquipment, DiversifiedTelecommunicationServices, WirelessTelecommunicationServices,
  Media, Entertainment, InteractiveMediaAndServices, ElectricUtilities, GasUtilities, MultiUtilities, WaterUtilities,
  IndependentPowerAndRenewableElectricityProducers, DiversifiedREITs, IndustrialREITs, HotelAndResortREITs, OfficeREITs,
  HealthCareREITs, ResidentialREITs, RetailREITs, SpecializedREITs, RealEstateManagementAndDevelopment
)
ENUM_MAPPING(
  Industry, EnergyEquipmentAndServices, OilGasAndConsumeableFules, Chemicals, ConstructionMaterials,
  ContainersAndPackaging, MetalsAndMining, PaperAndForestProducts, AerospaceAndDefense, BuildingProducts,
  ConstructionAndEngineering, ElectricalEquipment, IndustrialConglomerates, Machinery, TradingCompaniesAndDistributors,
  CommercialServicesAndSupplies, ProfessionalServices, AirFreightAndLogistics, PassengerAirlines, MarineTransportation,
  GroundTransportation, TransportationInfrastructure, AutomobileComponents, Automobiles, HouseholdDurables,
  LeisureProducts, TextilesApparelAndLuxuryGoods, HotelsRestaurantsAndLeisure, DiversifiedConsumerServices,
  Distributors, BroadlineRetail, SpecialtyRetail, ConsumerStaplesDistributionAndRetail, Beverages, FoodProducts,
  Tobacco, HouseholdProducts, PersonalCareProducts, HealthCareEquipmentAndSupplies, HealthCareProvidersAndServices,
  HealthCareTechnology, Biotechnology, Pharmaceuticals, LifeSciencesToolsAndServices, Banks, FinancialServices,
  ConsumerFinance, CapitalMarkets, MortgageRealEstateInvestmentTrusts, Insurance, ITServices, Software,
  CommunicationsEquipment, TechnologyHardwareStorageAndPeripherals, ElectronicEquipmentInstrumentsAndComponents,
  SemiconductorsAndSemiconductorEquipment, DiversifiedTelecommunicationServices, WirelessTelecommunicationServices,
  Media, Entertainment, InteractiveMediaAndServices, ElectricUtilities, GasUtilities, MultiUtilities, WaterUtilities,
  IndependentPowerAndRenewableElectricityProducers, DiversifiedREITs, IndustrialREITs, HotelAndResortREITs, OfficeREITs,
  HealthCareREITs, ResidentialREITs, RetailREITs, SpecializedREITs, RealEstateManagementAndDevelopment
)
ENUM_FROM_STRING(Industry)
ENUM_TO_STRING(Industry)

enum class LIB_EXPORT SubIndustry {
  // Energy -> Energy Equipment and Services
  OilAndGasDrilling,
  OilAndGasEquipmentAndServices,
  // Energy -> Oil, Gas, and Consumeable Fuels
  IntegratedOilAndGas,
  OilAndGasExplorationAndProduction,
  OilAndGasRefiningAndMarketing,
  OilAndGasStorageAndTransportation,
  CoalAndConsumeableFuels,
  // Materials -> Chemicals
  CommodityChemicals,
  DiversifiedChemicals,
  FertilizersAndAgriculturalChemicals,
  IndustrialGases,
  SpecialtyChemicals,
  // Materials -> Construction Materials
  ConstructionMaterials,
  // Materials -> Containers and Packaging
  MetalGlassAndPlasticContainers,
  PaperAndPlasticPackagingProductsAndMaterials,
  // Materials -> Metals and Mining
  Aluminum,
  DiversifiedMetalsAndMining,
  Copper,
  Gold,
  PreciousMetalsAndMinerals,
  Silver,
  Steel,
  // Materials -> Paper and Forest Products
  ForestProducts,
  PaperProducts,
  // Industrials -> Capital Goods -> AerospaceAndDefense
  AerospaceAndDefense,
  // Industrials -> Capital Goods -> BuildingProducts
  BuildingProducts,
  // Industrials -> Capital Goods -> ConstructionAndEngineering
  ConstructionAndEngineering,
  // Industrials -> Capital Goods -> ElectricalEquipment
  ElectricalComponentsAndEquipment,
  HeavyElectricalEquipment,
  // Industrials -> Capital Goods -> IndustrialConglomerates
  IndustrialConglomerates,
  // Industrials -> Capital Goods -> Machinery
  ConstructionMachineryAndHeavyTransportationEquipment,
  AgriculturalAndFarmMachinery,
  IndustrialMachinerySuppliesAndComponents,
  // Industrials -> Capital Goods -> TradingCompaniesAndDistributors
  TradingCompaniesAndDistributors,
  // Industrials -> Commercial and Professional Services -> CommercialServicesAndSupplies
  CommercialPrinting,
  EnvironmentalAndFacilitiesServices,
  OfficeServicesAndSupplies,
  DiviersifiedSupportServices,
  SecurityAndAlarmServices,
  // Industrials -> Commercial and Professional Services -> ProfessionalServices
  HumanResourcesAndEmploymentServices,
  ResearchAndConsultingServices,
  DataProcessingAndOutsourcedServices,
  // Industrials -> Transportation -> AirFreightAndLogistics
  AirFreightAndLogistics,
  // Industrials -> Transportation -> PassengerAirlines
  PassengerAirlines,
  // Industrials -> Transportation -> MarineTransportation
  MarineTransportation,
  // Industrials -> Transportation -> GroundTransportation
  RailTransportation,
  CargoGroundTransportation,
  PassengerGroundTransportation,
  // Industrials -> Transportation -> TransportationInfrastructure
  AirportServices,
  HighwaysAndRailtracks,
  MarinePortsAndServices,
  // Consumer Discretionary -> Automobiles and Components -> AutomobileComponents
  AutomotivePartsAndEquipment,
  TiresAndRubber,
  // Consumer Discretionary -> Automobiles and Components -> Automobiles
  AutomobileManufacturers,
  MotorcycleManufacturers,
  // Consumer Discretionary -> Consumer Durables and Apparel -> Household Durables
  ConsumerElectronics,
  HomeFurnishings,
  Homebuilding,
  HouseholdAppliances,
  HousewaresAndSpecialties,
  // Consumer Discretionary -> Consumer Durables and Apparel -> Leisure Products
  LeisureProducts,
  // Consumer Discretionary -> Consumer Durables and Apparel -> Textiles, Apprael, and Luxury Goods
  ApparelAccessoriesAndLuxuryGoods,
  Footwear,
  Textiles,
  // Consumer Discretionary -> Consumer Services -> Hotels, Restaurants, and Leisure
  CasinosAndGaming,
  HotelsResortsAndCruiseLines,
  LeisureFacilities,
  Restaurants,
  // Consumer Discretionary -> Consumer Services -> Diversified Consumer Services
  EducationServices,
  SpecializedConsumerServices,
  // Consumer Discretionary -> Consumer Discretionary Distribution and Retail -> Distributors
  Distributors,
  // Consumer Discretionary -> Consumer Discretionary Distribution and Retail -> Broadline Retail
  BroadlineRetail,
  // Consumer Discretionary -> Consumer Discretionary Distribution and Retail -> Specialty Retail
  ApparelRetail,
  ComputerAndElectronicsretail,
  HomeImprovementRetail,
  OtherSpecialtyRetail,
  AutomotiveRetail,
  HomefurnishingRetail,
  // Consumer Staples -> Consumer Staples Distribution And Retail -> Consumer Staples, Distribution, and Retail
  DrugRetail,
  FoodDistributors,
  FoodRetail,
  ConsumerStaplesMerchandiseRetail,
  // Consumer Staples -> Food, Beverage, and Tobacco -> Beverages
  Brewers,
  DistillersAndVintners,
  SoftDrinksAndNonAlcoholicBeverages,
  // Consumer Staples -> Food, Beverage, and Tobacco -> Food Products
  AgriculturalProductsAndServices,
  PackagedFoodsAndMeats,
  // Consumer Staples -> Food, Beverage, and Tobacco -> Tobacco
  Tobacco,
  // Consumer Staples -> Household and Personal Products -> Household Products
  HouseholdProducts,
  // Consumer Staples -> Household and Personal Products -> Personal Care Products
  PersonalCareProducts,
  // Health Care -> Health Care Equipment and Services -> Health Care Equipment and Supplies
  HealthCareEquipment,
  HealthCareSupplies,
  // Health Care -> Health Care Equipment and Services -> Health Care Providers and Services
  HealthCareDistributors,
  HealthCareServices,
  HealthCareFacilities,
  ManagedHealthCare,
  // Health Care -> Health Care Equipment and Services -> Health Care Technology
  HealthCareTechnology,
  // Health Care -> Pharmaceuticals, Biotechnology, and Life Sciences -> Biotechnology
  Biotechnology,
  // Health Care -> Pharmaceuticals, Biotechnology, and Life Sciences -> Pharmaceuticals
  Pharmaceuticals,
  // Health Care -> Pharmaceuticals, Biotechnology, and Life Sciences -> Life Sciences Tools and Services
  LifeSciencesToolsAndServices,
  // Financials -> Banks -> Banks
  DiversifiedBanks,
  RegionalBanks,
  // Financials -> Financial Services -> Financial Services
  DiversifiedFinancialServices,
  MultiSectorHoldings,
  SpecializedFinance,
  CommercialAndResidentialMortgageFinance,
  TransactionAndPaymentProcessingServices,
  // Financials -> Financial Services -> Consumer Finance
  ConsumerFinance,
  // Financials -> Financial Services -> Capital Markets
  AssetManagementAndCustodyBanks,
  InvestmentBankingAndBrokerage,
  DiversifiedCapitalMarkets,
  FinancialExchangesAndData,
  // Financials -> Financial Services -> Mortgage REITs,
  MortgageRealEstateInvestmentTrusts,
  // Financials -> Insurance -> Insurance
  InsuranceBrokers,
  LifeAndHealthInsurance,
  MultilineInsurance,
  PropertyAndCasualtyInsurance,
  Reinsurance,
  // Information Technology -> Software and Services -> ITServices
  ITConsultingAndOtherServices,
  InternetServicesAndInfrastructure,
  // Information Technology -> Software and Services -> Software
  ApplicationSoftware,
  SystemsSoftware,
  // Information Technology -> Technology Equipment and Hardware -> CommunicationsEquipment
  CommunicationsEquipment,
  // Information Technology -> Technology Equipment and Hardware -> TechnologyHardwareStorageAndPeripherals
  TechnologyHardwareStorageAndPeripherals,
  // Information Technology -> Technology Equipment and Hardware -> ElectronicEquipmentInstrumentsAndComponents
  ElectronicEquipmentAndInstruments,
  ElectronicComponents,
  ElectronicManufacturingServices,
  TechnologyDistributors,
  // Information Technology -> Semiconductors and Semiconductor Equipment -> SemiconductorsAndSemiconductorEquipmen
  SemiconductorMaterialsAndEquipment,
  Semiconductors,
  // Communication Services -> Telecommunication Services -> DiversifiedTelecommunicationServices
  AlternativeCarriers,
  IntegratedTelecommunicationServices,
  // Communication Services -> Telecommunication Services -> WirelessTelecommunicationServices
  WirelessTelecommunicationServices,
  // Communication Services -> Media and Entertainment -> Media
  Advertising,
  Broadcasting,
  CableAndSatellite,
  Publishing,
  // Communication Services -> Media and Entertainment -> Entertainment
  MoviesAndEntertainment,
  InteractiveHomeEntertainment,
  // Communication Services -> Media and Entertainment -> InteractiveMediaAndServices
  InteractiveMediaAndServices,
  // Utilities -> ElectricUtilities
  ElectricUtilities,
  // Utilities -> GasUtilities
  GasUtilities,
  // Utilities -> MultiUtilities
  MultiUtilities,
  // Utilities -> WaterUtilities
  WaterUtilities,
  // Utilities -> IndependentPowerAndRenewableElectricityProducers
  IndependentPowerProducersAndEnergyTraders,
  RenewableElectricity,
  // Real Estate -> Equity REITs -> DiversifiedREITs
  DiversifiedREITs,
  // Real Estate -> Equity REITs -> IndustrialREITs
  IndustrialREITs,
  // Real Estate -> Equity REITs -> HotelAndResortREITs
  HotelAndResortREITs,
  // Real Estate -> Equity REITs -> OfficeREITs
  OfficeREITs,
  // Real Estate -> Equity REITs -> HealthCareREITs
  HealthCareREITs,
  // Real Estate -> Equity REITs -> ResidentialREITs
  MultiFamilyResidentialREITs,
  SingleFamilyResidentialREITs,
  // Real Estate -> Equity REITs -> RetailREITs
  RetailREITs,
  // Real Estate -> Equity REITs -> SpecializedREITs
  OtherSpecializedREITs,
  SelfStorageREITs,
  TelecomTowerREITs,
  TimberREITs,
  DataCenterREITs,
  // Real Estate -> Real Estate Management and Development -> RealEstateManagementAndDevelopment
  DiversifiedRealEstateActivities,
  RealEstateOperatingCompanies,
  RealEstateDevelopment,
  RealEstateServices,
};

static const std::vector<str_t> SubIndustry_names = {
  "OilAndGasDrilling",
  "OilAndGasEquipmentAndServices",
  "IntegratedOilAndGas",
  "OilAndGasExplorationAndProduction",
  "OilAndGasRefiningAndMarketing",
  "OilAndGasStorageAndTransportation",
  "CoalAndConsumeableFuels",
  "CommodityChemicals",
  "DiversifiedChemicals",
  "FertilizersAndAgriculturalChemicals",
  "IndustrialGases",
  "SpecialtyChemicals",
  "ConstructionMaterials",
  "MetalGlassAndPlasticContainers",
  "PaperAndPlasticPackagingProductsAndMaterials",
  "Aluminum",
  "DiversifiedMetalsAndMining",
  "Copper",
  "Gold",
  "PreciousMetalsAndMinerals",
  "Silver",
  "Steel",
  "ForestProducts",
  "PaperProducts",
  "AerospaceAndDefense",
  "BuildingProducts",
  "ConstructionAndEngineering",
  "ElectricalComponentsAndEquipment",
  "HeavyElectricalEquipment",
  "IndustrialConglomerates",
  "ConstructionMachineryAndHeavyTransportationEquipment",
  "AgriculturalAndFarmMachinery",
  "IndustrialMachinerySuppliesAndComponents",
  "TradingCompaniesAndDistributors",
  "CommercialPrinting",
  "EnvironmentalAndFacilitiesServices",
  "OfficeServicesAndSupplies",
  "DiviersifiedSupportServices",
  "SecurityAndAlarmServices",
  "HumanResourcesAndEmploymentServices",
  "ResearchAndConsultingServices",
  "DataProcessingAndOutsourcedServices",
  "AirFreightAndLogistics",
  "PassengerAirlines",
  "MarineTransportation",
  "RailTransportation",
  "CargoGroundTransportation",
  "PassengerGroundTransportation",
  "AirportServices",
  "HighwaysAndRailtracks",
  "MarinePortsAndServices",
  "AutomotivePartsAndEquipment",
  "TiresAndRubber",
  "AutomobileManufacturers",
  "MotorcycleManufacturers",
  "ConsumerElectronics",
  "HomeFurnishings",
  "Homebuilding",
  "HouseholdAppliances",
  "HousewaresAndSpecialties",
  "LeisureProducts",
  "ApparelAccessoriesAndLuxuryGoods",
  "Footwear",
  "Textiles",
  "CasinosAndGaming",
  "HotelsResortsAndCruiseLines",
  "LeisureFacilities",
  "Restaurants",
  "EducationServices",
  "SpecializedConsumerServices",
  "Distributors",
  "BroadlineRetail",
  "ApparelRetail",
  "ComputerAndElectronicsretail",
  "HomeImprovementRetail",
  "OtherSpecialtyRetail",
  "AutomotiveRetail",
  "HomefurnishingRetail",
  "DrugRetail",
  "FoodDistributors",
  "FoodRetail",
  "ConsumerStaplesMerchandiseRetail",
  "Brewers",
  "DistillersAndVintners",
  "SoftDrinksAndNonAlcoholicBeverages",
  "AgriculturalProductsAndServices",
  "PackagedFoodsAndMeats",
  "Tobacco",
  "HouseholdProducts",
  "PersonalCareProducts",
  "HealthCareEquipment",
  "HealthCareSupplies",
  "HealthCareDistributors",
  "HealthCareServices",
  "HealthCareFacilities",
  "ManagedHealthCare",
  "HealthCareTechnology",
  "Biotechnology",
  "Pharmaceuticals",
  "LifeSciencesToolsAndServices",
  "DiversifiedBanks",
  "RegionalBanks",
  "DiversifiedFinancialServices",
  "MultiSectorHoldings",
  "SpecializedFinance",
  "CommercialAndResidentialMortgageFinance",
  "TransactionAndPaymentProcessingServices",
  "ConsumerFinance",
  "AssetManagementAndCustodyBanks",
  "InvestmentBankingAndBrokerage",
  "DiversifiedCapitalMarkets",
  "FinancialExchangesAndData",
  "MortgageRealEstateInvestmentTrusts",
  "InsuranceBrokers",
  "LifeAndHealthInsurance",
  "MultilineInsurance",
  "PropertyAndCasualtyInsurance",
  "Reinsurance",
  "ITConsultingAndOtherServices",
  "InternetServicesAndInfrastructure",
  "ApplicationSoftware",
  "SystemsSoftware",
  "CommunicationsEquipment",
  "TechnologyHardwareStorageAndPeripherals",
  "ElectronicEquipmentAndInstruments",
  "ElectronicComponents",
  "ElectronicManufacturingServices",
  "TechnologyDistributors",
  "SemiconductorMaterialsAndEquipment",
  "Semiconductors",
  "AlternativeCarriers",
  "IntegratedTelecommunicationServices",
  "WirelessTelecommunicationServices",
  "Advertising",
  "Broadcasting",
  "CableAndSatellite",
  "Publishing",
  "MoviesAndEntertainment",
  "InteractiveHomeEntertainment",
  "InteractiveMediaAndServices",
  "ElectricUtilities",
  "GasUtilities",
  "MultiUtilities",
  "WaterUtilities",
  "IndependentPowerProducersAndEnergyTraders",
  "RenewableElectricity",
  "DiversifiedREITs",
  "IndustrialREITs",
  "HotelAndResortREITs",
  "OfficeREITs",
  "HealthCareREITs",
  "MultiFamilyResidentialREITs",
  "SingleFamilyResidentialREITs",
  "RetailREITs",
  "OtherSpecializedREITs",
  "SelfStorageREITs",
  "TelecomTowerREITs",
  "TimberREITs",
  "DataCenterREITs",
  "DiversifiedRealEstateActivities",
  "RealEstateOperatingCompanies",
  "RealEstateDevelopment",
  "RealEstateServices",
};

static std::unordered_map<str_t, SubIndustry> _SubIndustry_mapping = {
  {"OilAndGasDrilling",                                    SubIndustry::OilAndGasDrilling                           },
  {"OilAndGasEquipmentAndServices",                        SubIndustry::OilAndGasEquipmentAndServices               },
  {"IntegratedOilAndGas",                                  SubIndustry::IntegratedOilAndGas                         },
  {"OilAndGasExplorationAndProduction",                    SubIndustry::OilAndGasExplorationAndProduction           },
  {"OilAndGasRefiningAndMarketing",                        SubIndustry::OilAndGasRefiningAndMarketing               },
  {"OilAndGasStorageAndTransportation",                    SubIndustry::OilAndGasStorageAndTransportation           },
  {"CoalAndConsumeableFuels",                              SubIndustry::CoalAndConsumeableFuels                     },
  {"CommodityChemicals",                                   SubIndustry::CommodityChemicals                          },
  {"DiversifiedChemicals",                                 SubIndustry::DiversifiedChemicals                        },
  {"FertilizersAndAgriculturalChemicals",                  SubIndustry::FertilizersAndAgriculturalChemicals         },
  {"IndustrialGases",                                      SubIndustry::IndustrialGases                             },
  {"SpecialtyChemicals",                                   SubIndustry::SpecialtyChemicals                          },
  {"ConstructionMaterials",                                SubIndustry::ConstructionMaterials                       },
  {"MetalGlassAndPlasticContainers",                       SubIndustry::MetalGlassAndPlasticContainers              },
  {"PaperAndPlasticPackagingProductsAndMaterials",         SubIndustry::PaperAndPlasticPackagingProductsAndMaterials},
  {"Aluminum",                                             SubIndustry::Aluminum                                    },
  {"DiversifiedMetalsAndMining",                           SubIndustry::DiversifiedMetalsAndMining                  },
  {"Copper",                                               SubIndustry::Copper                                      },
  {"Gold",                                                 SubIndustry::Gold                                        },
  {"PreciousMetalsAndMinerals",                            SubIndustry::PreciousMetalsAndMinerals                   },
  {"Silver",                                               SubIndustry::Silver                                      },
  {"Steel",                                                SubIndustry::Steel                                       },
  {"ForestProducts",                                       SubIndustry::ForestProducts                              },
  {"PaperProducts",                                        SubIndustry::PaperProducts                               },
  {"AerospaceAndDefense",                                  SubIndustry::AerospaceAndDefense                         },
  {"BuildingProducts",                                     SubIndustry::BuildingProducts                            },
  {"ConstructionAndEngineering",                           SubIndustry::ConstructionAndEngineering                  },
  {"ElectricalComponentsAndEquipment",                     SubIndustry::ElectricalComponentsAndEquipment            },
  {"HeavyElectricalEquipment",                             SubIndustry::HeavyElectricalEquipment                    },
  {"IndustrialConglomerates",                              SubIndustry::IndustrialConglomerates                     },
  {"ConstructionMachineryAndHeavyTransportationEquipment",
   SubIndustry::ConstructionMachineryAndHeavyTransportationEquipment                                                },
  {"AgriculturalAndFarmMachinery",                         SubIndustry::AgriculturalAndFarmMachinery                },
  {"IndustrialMachinerySuppliesAndComponents",             SubIndustry::IndustrialMachinerySuppliesAndComponents    },
  {"TradingCompaniesAndDistributors",                      SubIndustry::TradingCompaniesAndDistributors             },
  {"CommercialPrinting",                                   SubIndustry::CommercialPrinting                          },
  {"EnvironmentalAndFacilitiesServices",                   SubIndustry::EnvironmentalAndFacilitiesServices          },
  {"OfficeServicesAndSupplies",                            SubIndustry::OfficeServicesAndSupplies                   },
  {"DiviersifiedSupportServices",                          SubIndustry::DiviersifiedSupportServices                 },
  {"SecurityAndAlarmServices",                             SubIndustry::SecurityAndAlarmServices                    },
  {"HumanResourcesAndEmploymentServices",                  SubIndustry::HumanResourcesAndEmploymentServices         },
  {"ResearchAndConsultingServices",                        SubIndustry::ResearchAndConsultingServices               },
  {"DataProcessingAndOutsourcedServices",                  SubIndustry::DataProcessingAndOutsourcedServices         },
  {"AirFreightAndLogistics",                               SubIndustry::AirFreightAndLogistics                      },
  {"PassengerAirlines",                                    SubIndustry::PassengerAirlines                           },
  {"MarineTransportation",                                 SubIndustry::MarineTransportation                        },
  {"RailTransportation",                                   SubIndustry::RailTransportation                          },
  {"CargoGroundTransportation",                            SubIndustry::CargoGroundTransportation                   },
  {"PassengerGroundTransportation",                        SubIndustry::PassengerGroundTransportation               },
  {"AirportServices",                                      SubIndustry::AirportServices                             },
  {"HighwaysAndRailtracks",                                SubIndustry::HighwaysAndRailtracks                       },
  {"MarinePortsAndServices",                               SubIndustry::MarinePortsAndServices                      },
  {"AutomotivePartsAndEquipment",                          SubIndustry::AutomotivePartsAndEquipment                 },
  {"TiresAndRubber",                                       SubIndustry::TiresAndRubber                              },
  {"AutomobileManufacturers",                              SubIndustry::AutomobileManufacturers                     },
  {"MotorcycleManufacturers",                              SubIndustry::MotorcycleManufacturers                     },
  {"ConsumerElectronics",                                  SubIndustry::ConsumerElectronics                         },
  {"HomeFurnishings",                                      SubIndustry::HomeFurnishings                             },
  {"Homebuilding",                                         SubIndustry::Homebuilding                                },
  {"HouseholdAppliances",                                  SubIndustry::HouseholdAppliances                         },
  {"HousewaresAndSpecialties",                             SubIndustry::HousewaresAndSpecialties                    },
  {"LeisureProducts",                                      SubIndustry::LeisureProducts                             },
  {"ApparelAccessoriesAndLuxuryGoods",                     SubIndustry::ApparelAccessoriesAndLuxuryGoods            },
  {"Footwear",                                             SubIndustry::Footwear                                    },
  {"Textiles",                                             SubIndustry::Textiles                                    },
  {"CasinosAndGaming",                                     SubIndustry::CasinosAndGaming                            },
  {"HotelsResortsAndCruiseLines",                          SubIndustry::HotelsResortsAndCruiseLines                 },
  {"LeisureFacilities",                                    SubIndustry::LeisureFacilities                           },
  {"Restaurants",                                          SubIndustry::Restaurants                                 },
  {"EducationServices",                                    SubIndustry::EducationServices                           },
  {"SpecializedConsumerServices",                          SubIndustry::SpecializedConsumerServices                 },
  {"Distributors",                                         SubIndustry::Distributors                                },
  {"BroadlineRetail",                                      SubIndustry::BroadlineRetail                             },
  {"ApparelRetail",                                        SubIndustry::ApparelRetail                               },
  {"ComputerAndElectronicsretail",                         SubIndustry::ComputerAndElectronicsretail                },
  {"HomeImprovementRetail",                                SubIndustry::HomeImprovementRetail                       },
  {"OtherSpecialtyRetail",                                 SubIndustry::OtherSpecialtyRetail                        },
  {"AutomotiveRetail",                                     SubIndustry::AutomotiveRetail                            },
  {"HomefurnishingRetail",                                 SubIndustry::HomefurnishingRetail                        },
  {"DrugRetail",                                           SubIndustry::DrugRetail                                  },
  {"FoodDistributors",                                     SubIndustry::FoodDistributors                            },
  {"FoodRetail",                                           SubIndustry::FoodRetail                                  },
  {"ConsumerStaplesMerchandiseRetail",                     SubIndustry::ConsumerStaplesMerchandiseRetail            },
  {"Brewers",                                              SubIndustry::Brewers                                     },
  {"DistillersAndVintners",                                SubIndustry::DistillersAndVintners                       },
  {"SoftDrinksAndNonAlcoholicBeverages",                   SubIndustry::SoftDrinksAndNonAlcoholicBeverages          },
  {"AgriculturalProductsAndServices",                      SubIndustry::AgriculturalProductsAndServices             },
  {"PackagedFoodsAndMeats",                                SubIndustry::PackagedFoodsAndMeats                       },
  {"Tobacco",                                              SubIndustry::Tobacco                                     },
  {"HouseholdProducts",                                    SubIndustry::HouseholdProducts                           },
  {"PersonalCareProducts",                                 SubIndustry::PersonalCareProducts                        },
  {"HealthCareEquipment",                                  SubIndustry::HealthCareEquipment                         },
  {"HealthCareSupplies",                                   SubIndustry::HealthCareSupplies                          },
  {"HealthCareDistributors",                               SubIndustry::HealthCareDistributors                      },
  {"HealthCareServices",                                   SubIndustry::HealthCareServices                          },
  {"HealthCareFacilities",                                 SubIndustry::HealthCareFacilities                        },
  {"ManagedHealthCare",                                    SubIndustry::ManagedHealthCare                           },
  {"HealthCareTechnology",                                 SubIndustry::HealthCareTechnology                        },
  {"Biotechnology",                                        SubIndustry::Biotechnology                               },
  {"Pharmaceuticals",                                      SubIndustry::Pharmaceuticals                             },
  {"LifeSciencesToolsAndServices",                         SubIndustry::LifeSciencesToolsAndServices                },
  {"DiversifiedBanks",                                     SubIndustry::DiversifiedBanks                            },
  {"RegionalBanks",                                        SubIndustry::RegionalBanks                               },
  {"DiversifiedFinancialServices",                         SubIndustry::DiversifiedFinancialServices                },
  {"MultiSectorHoldings",                                  SubIndustry::MultiSectorHoldings                         },
  {"SpecializedFinance",                                   SubIndustry::SpecializedFinance                          },
  {"CommercialAndResidentialMortgageFinance",              SubIndustry::CommercialAndResidentialMortgageFinance     },
  {"TransactionAndPaymentProcessingServices",              SubIndustry::TransactionAndPaymentProcessingServices     },
  {"ConsumerFinance",                                      SubIndustry::ConsumerFinance                             },
  {"AssetManagementAndCustodyBanks",                       SubIndustry::AssetManagementAndCustodyBanks              },
  {"InvestmentBankingAndBrokerage",                        SubIndustry::InvestmentBankingAndBrokerage               },
  {"DiversifiedCapitalMarkets",                            SubIndustry::DiversifiedCapitalMarkets                   },
  {"FinancialExchangesAndData",                            SubIndustry::FinancialExchangesAndData                   },
  {"MortgageRealEstateInvestmentTrusts",                   SubIndustry::MortgageRealEstateInvestmentTrusts          },
  {"InsuranceBrokers",                                     SubIndustry::InsuranceBrokers                            },
  {"LifeAndHealthInsurance",                               SubIndustry::LifeAndHealthInsurance                      },
  {"MultilineInsurance",                                   SubIndustry::MultilineInsurance                          },
  {"PropertyAndCasualtyInsurance",                         SubIndustry::PropertyAndCasualtyInsurance                },
  {"Reinsurance",                                          SubIndustry::Reinsurance                                 },
  {"ITConsultingAndOtherServices",                         SubIndustry::ITConsultingAndOtherServices                },
  {"InternetServicesAndInfrastructure",                    SubIndustry::InternetServicesAndInfrastructure           },
  {"ApplicationSoftware",                                  SubIndustry::ApplicationSoftware                         },
  {"SystemsSoftware",                                      SubIndustry::SystemsSoftware                             },
  {"CommunicationsEquipment",                              SubIndustry::CommunicationsEquipment                     },
  {"TechnologyHardwareStorageAndPeripherals",              SubIndustry::TechnologyHardwareStorageAndPeripherals     },
  {"ElectronicEquipmentAndInstruments",                    SubIndustry::ElectronicEquipmentAndInstruments           },
  {"ElectronicComponents",                                 SubIndustry::ElectronicComponents                        },
  {"ElectronicManufacturingServices",                      SubIndustry::ElectronicManufacturingServices             },
  {"TechnologyDistributors",                               SubIndustry::TechnologyDistributors                      },
  {"SemiconductorMaterialsAndEquipment",                   SubIndustry::SemiconductorMaterialsAndEquipment          },
  {"Semiconductors",                                       SubIndustry::Semiconductors                              },
  {"AlternativeCarriers",                                  SubIndustry::AlternativeCarriers                         },
  {"IntegratedTelecommunicationServices",                  SubIndustry::IntegratedTelecommunicationServices         },
  {"WirelessTelecommunicationServices",                    SubIndustry::WirelessTelecommunicationServices           },
  {"Advertising",                                          SubIndustry::Advertising                                 },
  {"Broadcasting",                                         SubIndustry::Broadcasting                                },
  {"CableAndSatellite",                                    SubIndustry::CableAndSatellite                           },
  {"Publishing",                                           SubIndustry::Publishing                                  },
  {"MoviesAndEntertainment",                               SubIndustry::MoviesAndEntertainment                      },
  {"InteractiveHomeEntertainment",                         SubIndustry::InteractiveHomeEntertainment                },
  {"InteractiveMediaAndServices",                          SubIndustry::InteractiveMediaAndServices                 },
  {"ElectricUtilities",                                    SubIndustry::ElectricUtilities                           },
  {"GasUtilities",                                         SubIndustry::GasUtilities                                },
  {"MultiUtilities",                                       SubIndustry::MultiUtilities                              },
  {"WaterUtilities",                                       SubIndustry::WaterUtilities                              },
  {"IndependentPowerProducersAndEnergyTraders",            SubIndustry::IndependentPowerProducersAndEnergyTraders   },
  {"RenewableElectricity",                                 SubIndustry::RenewableElectricity                        },
  {"DiversifiedREITs",                                     SubIndustry::DiversifiedREITs                            },
  {"IndustrialREITs",                                      SubIndustry::IndustrialREITs                             },
  {"HotelAndResortREITs",                                  SubIndustry::HotelAndResortREITs                         },
  {"OfficeREITs",                                          SubIndustry::OfficeREITs                                 },
  {"HealthCareREITs",                                      SubIndustry::HealthCareREITs                             },
  {"MultiFamilyResidentialREITs",                          SubIndustry::MultiFamilyResidentialREITs                 },
  {"SingleFamilyResidentialREITs",                         SubIndustry::SingleFamilyResidentialREITs                },
  {"RetailREITs",                                          SubIndustry::RetailREITs                                 },
  {"OtherSpecializedREITs",                                SubIndustry::OtherSpecializedREITs                       },
  {"SelfStorageREITs",                                     SubIndustry::SelfStorageREITs                            },
  {"TelecomTowerREITs",                                    SubIndustry::TelecomTowerREITs                           },
  {"TimberREITs",                                          SubIndustry::TimberREITs                                 },
  {"DataCenterREITs",                                      SubIndustry::DataCenterREITs                             },
  {"DiversifiedRealEstateActivities",                      SubIndustry::DiversifiedRealEstateActivities             },
  {"RealEstateOperatingCompanies",                         SubIndustry::RealEstateOperatingCompanies                },
  {"RealEstateDevelopment",                                SubIndustry::RealEstateDevelopment                       },
  {"RealEstateServices",                                   SubIndustry::RealEstateServices                          },
};

ENUM_FROM_STRING(SubIndustry)
ENUM_TO_STRING(SubIndustry)

}
