#pragma once
#include <finance-enums/common.hpp>
#include <finance-enums/country.hpp>
#include <finance-enums/helpers/enum.hpp>
#include <finance-enums/helpers/exports.hpp>
#include <iostream>
#include <vector>

namespace finance_enums {
// https://www.iso20022.org/market-identifier-codes
static str_t ExchangeStandard = "ISO10383";

str_t inline exchange_standard() { return ExchangeStandard; }

enum class LIB_EXPORT ExchangeCode {
  /*################# NYSE #################*/
  XNYS, // NYSE
  NYSD, // NYSE Dark
  XCIS, // NYSE National
  CISD, // NYSE National Dark
  XCHI, // NYSE Chicago
  ARCX, // ARCA
  ARCD, // ARCA Dark
  ARCO, // ARCA Options
  XASE, // AMEX
  AMXO, // AMEX Options
  // XNLI, // NYSE LIFFE

  /*################# NASDAQ #################*/
  XNAS, // NASDAQ
  XNGS, // NASDAQ Global Select
  XNCM, // NASDAQ Capital Markets
  XNMS, // NASDAQ Global Market
  NASD, // NASDAQ Dark
  XNDQ, // NASDAQ Options
  XBOS, // NASDAQ Boston
  BOSD, // NASDAQ Boston Dark
  XBXO, // NASDAQ Boston Options
  XPHL, // NASDAQ Philly
  XPSX, // NASDAQ PSX (also philly?)
  PSXD, // NASDAQ Philly Dark
  XPHO, // NASDAQ Philly Options
  XPBT, // PBOT
  XPOR, // NASDAQ Portal
  // XBRT, // BRUT ECN
  XNFI, // NASDAQ Fixed Income
  XISE, // ISE Equities (ISE)
  GMNI, // ISE Gemini Options (GEMX)
  MCRY, // ISE Mercury Options (MRX)
  // XISA, // ISE Alternative Markets
  // XISX, // ISE

  /*################# CBOE #################*/
  XCBO, // CBOE
  EDGA, // EDGA
  EDGD, // EDGA DARK
  EDGX, // EDGX
  EDDP, // EDGX DARK
  EDGO, // EDGX Options
  BATS, // BZX
  BZXD, // BZX DARK
  BATO, // BZX Options
  BATY, // BYX
  BYXD, // BYX DARK
  C2OX, // CBOE C2 Options
  // BHSF, // CBOE Swap Execution Facility
  // HSFX, // CBOE Hotspot FX
  // XCBF, // CBOE Futures
  // XCBD, // CBOE Digital
  // CFIM, // CBOE Fixed Income

  /*################# CME #################*/
  XCME, // CME
  FCME, // CME Floor
  // XIMM, // CME IMM (FX / IR)
  GLBX, // Globex
  // XIOM, // CME INDEX AND OPTIONS MARKET
  // CMES, // CME SWAPS MARKETS (CME)
  // CBTS, // CME SWAPS MARKETS (CBOT)
  // NYMS, // CME SWAPS MARKETS (NYMEX)
  // CECS, // CME SWAPS MARKETS (COMEX)
  XCBT, // CBOT
  FCBT, // CBOT Floor
  XKBT, // KANSAS CITY BOARD OF TRADE
  XNYM, // NYMEX
  // XCEC, // NYMEX COMMODITIES EXCHANGE CENTER
  // XNYE, // NYMEX - OTC MARKETS
  // XNYL, // NYMEX - ENERGY MARKETS

  /*################# MIAX #################*/
  MIHI, // MIAX
  MPRL, // MIAX Pearl
  EPRL, // MIAX Pearl
  EPRD, // MIAX Pearl Dark
  XMIO, // MIAX Options
  EMLD, // MIAX Emerald Options

  /*################# OTC Markets #################*/
  OTCM, // OTC Markets
  CAVE, // OTC CAVEAT EMPTOR
  OTCB, // OTCQB MARKETPLACE
  OTCQ, // OTCQX MARKETPLACE
  PINL, // OTC PINK LIMITED
  PINI, // OTC PINK NO INFORMATION
  PINX, // OTC PINK MARKETPLACE
  PSGM, // OTC GREY MARKET
  PINC, // OTC PINK CURRENT

  /*################# FINRA #################*/
  FINR, // FINRA
  FINN, // FINRA NASDAQ TRF (NJ)
  FINC, // FINRA NASDAQ TRF (Chicago)
  FINY, // FINRA NYSE TRF
  XADF, // FINRA ADF
  FINO, // FINRA ORF
  OOTC, // Other OTC

  /*################# OTHER US #################*/
  OPRA, // OPRA
  MEMX, // MEMX
  MEMD, // MEMX Dark
  MXOP, // MEMX Options
  // MEMM,MEMX,SGMT,MEMX LLC RETAIL MIDPOINT,MEMX LLC,254900ZJZM9RSYHE7D79,NSPD,,US
  IEXG, // IEX
  // IEXD, // IEX Dark
  LTSE, // Long Term Stock Exchange

  /*################# Canadian Securities Exchange CSE #################*/
  XCNQ, // CSE
  PURE, // CSE Pure
  CSE2, // CSE CSE2

  /*################# TMX Group  #################*/
  XTSE, // TSE
  XDRK, // TSX Dark
  VDRK, // TSX Venture Dark
  XTSX, // TSX Venture
  XTNX, // TSX Venture Nex
  XATS, // Alpha Exchange
  XATX, // Alpha X
  ADRK, // Alpha Dark
  XMOD, // Montreal
  XMOC, // Montreal Climate

  /*################# CBOE NEO #################*/
  NEOE, // NEO Exchange
  NEOD, // NEO Exchange Dark
  NEON, // NEO Exchange (MARKET BY
        // PRICE),,549300MILSKTNBLQ1L12,NSPD,NEO-N,CA,TORONTO,WWW.NEOSTOCKEXCHANGE.COM,ACTIVE,20180723,20190624,,,
  NEOC, // NEO Connect

  /*################# Other Canada / Canada ATS #################*/
  // XCX2,CHIC,SGMT,CX2,,,NSPD,,CA,TORONTO,WWW.CHI-X.COM/CA,ACTIVE
  // CHIC,CHIC,OPRT,CHI-X CANADA ATS,,,ATSS,,CA,TORONTO,WWW.CHI-XCANADA.COM,ACTIVE
  // EQCA,EQCA,OPRT,EQUILEND CANADA CORP.,EQUILEND CANADA
  // CORP.,213800MJ9CY4JWO58S26,NSPD,,CA,TORONTO,WWW.EQUILEND.COM,ACTIVE BNSX,BNSX,OPRT,THE BANK OF NOVA
  // SCOTIA,,L3I9ZG2KFGXZ61BMYR72,SINT,,CA,TORONTO,WWW.SCOTIABANK.COM,ACTIVE CAND,CAND,OPRT,CANDEAL.CA
  // INC,,549300QSD4O4FEHPDA44,NSPD,CANDEAL,CA,TORONTO,WWW.CANDEAL.COM,ACTIVE CANX,CANX,OPRT,CANNEX FINANCIAL EXCHANGE
  // LTS,,,NSPD,CANNEX,CA,TORONTO,WWW.CANNEX.COM,ACTIVE COTC,COTC,OPRT,BMO CAPITAL MARKETS - CAD OTC
  // TRADES,,L64HM9LHPDOS1B9HJC68,NSPD,,CA,TORONTO,WWW.BMOCM.COM,ACTIVE IVZX,IVZX,OPRT,INVESCO CANADA PTF
  // TRADES,,9F443AVI6KXI3MYCLS29,NSPD,,CA,TORONTO,WWW.INVESCO.CA,ACTIVE LICA,LICA,OPRT,LIQUIDNET CANADA
  // ATS,,21380031335M4LHQJ436,ATSS,,CA,TORONTO,WWW.LIQUIDNET.COM,ACTIVE MATN,MATN,OPRT,MATCH
  // NOW,,,NSPD,,CA,TORONTO,WWW.TRIACTCANADA.COM,ACTIVE NGXC,NGXC,OPRT,NATURAL GAS
  // EXCHANGE,,549300MZWLT9C8T4VI12,NSPD,NGX,CA,CALGARY,WWW.NGX.COM,ACTIVE OMGA,OMGA,OPRT,OMEGA
  // ATS,,,ATSS,,CA,TORONTO,WWW.OMEGAATS.COM,ACTIVE LYNX,OMGA,SGMT,LYNX ATS,,,ATSS,,CA,TORONTO,WWW.OMEGAATS.COM,ACTIVE
  // XBBK,XBBK,OPRT,PERIMETER FINANCIAL CORP. - BLOCKBOOK ATS,,,ATSS,,CA,TORONTO,WWW.PFIN.CA,ACTIVE
  // XCXD,XCXD,OPRT,NASDAQ CXD,,,NSPD,,CA,TORONTO,HTTP://BUSINESS.NASDAQ.COM/TRADE/CANADIAN-EQUITIES/OVERVIEW,ACTIVE
  // XICX,XICX,OPRT,INSTINET CANADA CROSS,,549300SU730FTQOKTE75,NSPD,,CA,TORONTO,WWW.INSTINET.COM,ACTIVE

  /*################# Other US based Equity ATS #################*/
  // https://www.finra.org/filing-reporting/otc-transparency/ats-equity-firms
  // https://www.sec.gov/foia/docs/atslist
  // ABEX, // 303 Alternatives LLC
  // BIDS, // Bids Trading LP
  // BNPC, // BNP Paribas Cortex
  // OCEA, // Blue Ocean ATS
  // CCMX, // Carta
  // ICBX, // Instinet
  // ONEC, // Citigroup One ATS
  // clearlist
  // CODA, // Coda Markets
  // CAES, // Credit Suisse Crossfinder
  // XSTM, // Fidelity Crossstream
  // dealerweb
  // EQX LLC
  // FNC AG STOCK
  // GOTC, // Global OTC
  // IATS, // Interactive Brokers ATS
  // IEOS, // Interactive Brokers EOS ATS
  // BAML, // BAML Instinct X ATS
  // INCR, // Intelligentcross ATS
  // INVESTX GEM
  // INX SECURITIES, LLC
  // JPBX, // JP Morgan Securities JPB-X
  // JPMX, // JP Morgan Securities JPM-X
  // LEVL, // Level ATS
  // LIUH, // Liquidnet H2O
  // LIQUIDNET NEGOTIATION ATS
  // lodas
  // LMNX, // Luminex ATS
  // MS POOL (ATS-4)	MSPL	MORGAN STANLEY & CO. LLC
  // MS RPOOL (ATS-6)	MSRP	MORGAN STANLEY & CO. LLC
  // MS TRAJECTORY CROSS (ATS-1)	MSTX	MORGAN STANLEY & CO. LLC
  // NFSTX, LLC	NFST	NFSTX, LLC
  // NORTH CAPITAL PRIVATE SECURITIES CORPORATION
  // OASIS PRO MARKETS LLC
  // CGXS, // ONECHRONOS
  // OTC Link
  // OTCN, // OTC Link ECN
  // OTCI, // OTC Link NQB IDQS
  // ITGI, // Virtu Posit
  // PROMETHEUM EMBER ATS INC.
  // STRM, // Purestream
  // SECURITIZE MARKETS ATS
  // SHARENETT ATS
  // SGMT, // Goldman Sigma X2
  // STARTENGINE SECONDARY
  // STFX, // Stifel, Nicolaus and Co STIFEL X ATS
  // TEXTURE ATS
  // BARX, // Barclays ATS
  // TOR ATS
  // UBSA, // UBS ATS
  // VARIABLE INVESTMENT ADVISORS, INC. ATS (VIAATS)
  // VCRS, // Virtu MATCHIT conditional room
  // VFMI, // Virtu Matchit
  // PJCX, // Piper Sandler and Co. ATS

  /*################# Other US based Options/Futures ATS #################*/
  // DASH, // DASH ATS
  // FNFT, // BGC Fenics Futures
  // BGCD, // BGC Derivatives
  // XBOX, // BOX

  /*################# Other US based Fixed Income ATS #################*/
  // https://www.finra.org/filing-reporting/otc-transparency/finra-equity-ats-firms-list
  // SCXA,SCXO,SGMT,SEED DIGITAL SECURITIES MARKET,,5493009JXYKN3NLOUE77,ATSS,,US
  // BNDS, // Bonds.com Bondspro
  // BTEQ, // BrokerTec
  // cboe fixed income (above)
  // CLARITY BIDRATE ALTERNATIVE TRADING SYSTEM
  // clearlist
  // CREDITMATCH
  // DWFI, // Dealerweb
  // FNCS, // BGCF Fenics
  // GSEF, // GFI Swaps Exchange
  // HTD-ATS
  // interactive broker ats (above)
  // ICSU, // ICAP SEF
  // VABD, // ICE Bondpoint
  // TMCC, // ICE TMC
  // IDXM, // IDX Markets
  // Kopen Tech Capital Markets
  // LESI, // LedgerEdge
  // LIFI, // Liquidnet Fixed Income ATS
  // MKAA, // Marketaxess ATS
  // LQED, // LIQUIDITYEDGE
  // MBS Source eTrading, Inc.
  // North Capital Private Securities Corporation
  // OASIS PRO MARKETS LLC
  // OTC Link (above)
  // SECURITIZE MARKETS ATS
  // SHARENETT ATS
  // TEXTURE ATS
  // TP ICAP Global Markets Americas LLC
  // TPCD, // TULLETT PREBON PLC - TP CREDITDEAL
  // BNDD, // TRADEWEB DIRECT
  // TRWB, // TRADEWEB LLC
  // TWSF,TRWB,SGMT,TW SEF LLC,,5493000G5QHJUY9ZWQ91,NSPD,TWSEF,US
  // DWSF,TRWB,SGMT,DW SEF LLC,,5493000G5QHJUY9ZWQ91,NSPD,DWSEF,US
  // TMID, // Trumid

  /*################# Other US based ATS #################*/
  // AATS, // Assent ATS
  // BLUE, // tZero / PRO SECURITIES ATS
  // CLST, // Clear Street
  // FNXB, // BGCF Fenicx Invitations
  // FNFX, // BGC Fenics FX
  // GFAM, // GFI
  // LATG, // GFI LATG
  // PRSE, // Pragma ATS
  // XAQS,XAQS,OPRT,AUTOMATED EQUITY FINANCE MARKETS,,,ATSS,AQS,US
  // XTXD, // XTX Direct

  /*################# US based options #################*/

  /*################# US based futures #################*/
  // SMFE, // Small Exchange

  /*################# US based fx #################*/

  /*################# US based crypto #################*/
  // BKKT, // BAKKT
  // FREX, // COINBASE DERIVATIVES
  // SFOX, // SFOX
  // XTRD, // XTRD

  /*################# OTHER PARENT ORGS #################*/
  // BGCF, // BGC Financial
  // BTEC, // ICAP Electronic Broking
  // GSCO, // Goldman Sachs
  // IBKR, // Interactive Brokers
  // JPMS, // JP Morgan Securities
  // LIUS, // Liquidnet US
  // MTXX, // Marketaxess
  // PIPR, // Piper Sandler and Co.
  // UBSS, // UBS Securities LLC
  // VUSA, // Virtu Americas
  // VFCM, // Virtu Financial Capital Markets
  // XTXM, // XTX Markets

  /*################# OTHER #################*/
  XXXX,

  /*################# NON ISO-10383 #################*/
  PYPR,
  SIMU,
};

ENUM_NAMES(
  ExchangeCode, XNYS, NYSD, XCIS, CISD, XCHI, ARCX, ARCD, ARCO, XASE, AMXO, XNAS, XNGS, XNCM, XNMS, NASD, XNDQ, XBOS,
  BOSD, XBXO, XPHL, XPSX, PSXD, XPHO, XPBT, XPOR, XNFI, XISE, GMNI, MCRY, XCBO, EDGA, EDGD, EDGX, EDDP, EDGO, BATS,
  BZXD, BATO, BATY, BYXD, C2OX, XCME, FCME, GLBX, XCBT, FCBT, XKBT, XNYM, MIHI, MPRL, EPRL, EPRD, XMIO, EMLD, OTCM,
  CAVE, OTCB, OTCQ, PINL, PINI, PINX, PSGM, PINC, FINR, FINN, FINC, FINY, XADF, FINO, OOTC, OPRA, MEMX, MEMD, MXOP,
  IEXG, LTSE, XCNQ, PURE, CSE2, XTSE, XDRK, VDRK, XTSX, XTNX, XATS, XATX, ADRK, XMOD, XMOC, NEOE, NEOD, NEON, NEOC,
  XXXX, PYPR, SIMU
)
ENUM_MAPPING(
  ExchangeCode, XNYS, NYSD, XCIS, CISD, XCHI, ARCX, ARCD, ARCO, XASE, AMXO, XNAS, XNGS, XNCM, XNMS, NASD, XNDQ, XBOS,
  BOSD, XBXO, XPHL, XPSX, PSXD, XPHO, XPBT, XPOR, XNFI, XISE, GMNI, MCRY, XCBO, EDGA, EDGD, EDGX, EDDP, EDGO, BATS,
  BZXD, BATO, BATY, BYXD, C2OX, XCME, FCME, GLBX, XCBT, FCBT, XKBT, XNYM, MIHI, MPRL, EPRL, EPRD, XMIO, EMLD, OTCM,
  CAVE, OTCB, OTCQ, PINL, PINI, PINX, PSGM, PINC, FINR, FINN, FINC, FINY, XADF, FINO, OOTC, OPRA, MEMX, MEMD, MXOP,
  IEXG, LTSE, XCNQ, PURE, CSE2, XTSE, XDRK, VDRK, XTSX, XTNX, XATS, XATX, ADRK, XMOD, XMOC, NEOE, NEOD, NEON, NEOC,
  XXXX, PYPR, SIMU
)
ENUM_FROM_STRING(ExchangeCode)
ENUM_TO_STRING(ExchangeCode)

static std::unordered_map<ExchangeCode, ExchangeCode> OperatingMic = {
  /*################# NYSE #################*/
  {ExchangeCode::XNYS, ExchangeCode::XNYS}, // NYSE
  {ExchangeCode::XCIS, ExchangeCode::XNYS}, // NYSE National
  {ExchangeCode::CISD, ExchangeCode::XNYS}, // NYSE National Dark
  {ExchangeCode::XCHI, ExchangeCode::XNYS}, // NYSE Chicago
  {ExchangeCode::ARCX, ExchangeCode::XNYS}, // ARCA
  {ExchangeCode::ARCD, ExchangeCode::XNYS}, // ARCA Dark
  {ExchangeCode::ARCO, ExchangeCode::XNYS}, // ARCA Options
  {ExchangeCode::XASE, ExchangeCode::XNYS}, // AMEX
  {ExchangeCode::AMXO, ExchangeCode::XNYS}, // AMEX Options
  {ExchangeCode::NYSD, ExchangeCode::XNYS}, // NYSE Dark
  /*################# NASDAQ #################*/
  {ExchangeCode::XNAS, ExchangeCode::XNAS}, // NASDAQ
  {ExchangeCode::XNGS, ExchangeCode::XNAS}, // NASDAQ Global Select
  {ExchangeCode::XNCM, ExchangeCode::XNAS}, // NASDAQ Capital Markets
  {ExchangeCode::XNMS, ExchangeCode::XNAS}, // NASDAQ Global Market
  {ExchangeCode::NASD, ExchangeCode::XNAS}, // NASDAQ Dark
  {ExchangeCode::XNDQ, ExchangeCode::XNAS}, // NASDAQ Options
  {ExchangeCode::XBOS, ExchangeCode::XNAS}, // NASDAQ Boston
  {ExchangeCode::BOSD, ExchangeCode::XNAS}, // NASDAQ Boston Dark
  {ExchangeCode::XBXO, ExchangeCode::XNAS}, // NASDAQ Boston Options
  {ExchangeCode::XPHL, ExchangeCode::XNAS}, // NASDAQ Philly
  {ExchangeCode::XPSX, ExchangeCode::XNAS}, // NASDAQ PSX (also philly?)
  {ExchangeCode::PSXD, ExchangeCode::XNAS}, // NASDAQ Philly Dark
  {ExchangeCode::XPHO, ExchangeCode::XNAS}, // NASDAQ Philly Options
  {ExchangeCode::XPBT, ExchangeCode::XNAS}, // PBOT
  {ExchangeCode::XPOR, ExchangeCode::XNAS}, // NASDAQ Portal
  {ExchangeCode::XNFI, ExchangeCode::XNAS}, // NASDAQ Fixed Income
  {ExchangeCode::XISE, ExchangeCode::XNAS}, // ISE Equities (ISE)
  {ExchangeCode::GMNI, ExchangeCode::XNAS}, // ISE Gemini Options (GEMX)
  {ExchangeCode::MCRY, ExchangeCode::XNAS}, // ISE Mercury Options (MRX)
  // ExchangeCode::XISA, ExchangeCode::XNAS, // ISE Alternative Markets
  // ExchangeCode::XISX, ExchangeCode::XNAS, // ISE
  /*################# CBOE #################*/
  {ExchangeCode::XCBO, ExchangeCode::XCBO}, // CBOE
  {ExchangeCode::EDGA, ExchangeCode::XCBO}, // EDGA
  {ExchangeCode::EDGD, ExchangeCode::XCBO}, // EDGA DARK
  {ExchangeCode::EDGX, ExchangeCode::XCBO}, // EDGX
  {ExchangeCode::EDDP, ExchangeCode::XCBO}, // EDGX DARK
  {ExchangeCode::EDGO, ExchangeCode::XCBO}, // EDGX Options
  {ExchangeCode::BATS, ExchangeCode::XCBO}, // BZX
  {ExchangeCode::BZXD, ExchangeCode::XCBO}, // BZX DARK
  {ExchangeCode::BATO, ExchangeCode::XCBO}, // BZX Options
  {ExchangeCode::BATY, ExchangeCode::XCBO}, // BYX
  {ExchangeCode::BYXD, ExchangeCode::XCBO}, // BYX DARK
  {ExchangeCode::C2OX, ExchangeCode::XCBO}, // CBOE C2 Options
  // ExchangeCode::BHSF, ExchangeCode::XCBO, // CBOE Swap Execution Facility
  // ExchangeCode::HSFX, ExchangeCode::XCBO, // CBOE Hotspot FX
  // ExchangeCode::XCBF, ExchangeCode::XCBO, // CBOE Futures
  // ExchangeCode::XCBD, ExchangeCode::XCBO, // CBOE Digital
  // ExchangeCode::CFIM, ExchangeCode::XCBO, // CBOE Fixed Income

  /*################# CME #################*/
  {ExchangeCode::XCME, ExchangeCode::XCME}, // CME
  {ExchangeCode::FCME, ExchangeCode::XCME}, // CME Floor
  // ExchangeCode::XIMM, ExchangeCode::XCME, // CME IMM (FX / IR)
  {ExchangeCode::GLBX, ExchangeCode::XCME}, // Globex
  // ExchangeCode::XIOM, ExchangeCode::XCME, // CME INDEX AND OPTIONS MARKET,,,NSPD,IOM,US
  // ExchangeCode::CMES, ExchangeCode::XCME, // CME SWAPS MARKETS (CME)
  // ExchangeCode::CBTS, ExchangeCode::XCME, // CME SWAPS MARKETS (CBOT)
  // ExchangeCode::NYMS, ExchangeCode::XCME, // CME SWAPS MARKETS (NYMEX)
  // ExchangeCode::CECS, ExchangeCode::XCME, // CME SWAPS MARKETS (COMEX)
  {ExchangeCode::XCBT, ExchangeCode::XCBT}, // CBOT
  {ExchangeCode::FCBT, ExchangeCode::XCBT}, // CBOT Floor
  {ExchangeCode::XKBT, ExchangeCode::XCBT}, // KANSAS CITY BOARD OF TRADE
  {ExchangeCode::XNYM, ExchangeCode::XNYM}, // NYMEX
  // ExchangeCode::XCEC, ExchangeCode::XNYM, // NYMEX COMMODITIES EXCHANGE CENTER
  // ExchangeCode::XNYE, ExchangeCode::XNYM, // NYMEX - OTC MARKETS
  // ExchangeCode::XNYL, ExchangeCode::XNYM, // NYMEX - ENERGY MARKETS

  /*################# MIAX #################*/
  {ExchangeCode::MIHI, ExchangeCode::MIHI}, // MIAX
  {ExchangeCode::MPRL, ExchangeCode::MIHI}, // MIAX Pearl
  {ExchangeCode::EPRL, ExchangeCode::MIHI}, // MIAX Pearl
  {ExchangeCode::EPRD, ExchangeCode::MIHI}, // MIAX Pearl Dark
  {ExchangeCode::XMIO, ExchangeCode::MIHI}, // MIAX Options
  {ExchangeCode::EMLD, ExchangeCode::MIHI}, // MIAX Emerald Options

  /*################# OTC Markets #################*/
  {ExchangeCode::OTCM, ExchangeCode::OTCM}, // OTC Markets
  {ExchangeCode::CAVE, ExchangeCode::OTCM}, // OTC CAVEAT EMPTOR
  {ExchangeCode::OTCB, ExchangeCode::OTCM}, // OTCQB MARKETPLACE
  {ExchangeCode::OTCQ, ExchangeCode::OTCM}, // OTCQX MARKETPLACE
  {ExchangeCode::PINL, ExchangeCode::OTCM}, // OTC PINK LIMITED
  {ExchangeCode::PINI, ExchangeCode::OTCM}, // OTC PINK NO INFORMATION
  {ExchangeCode::PINX, ExchangeCode::OTCM}, // OTC PINK MARKETPLACE
  {ExchangeCode::PSGM, ExchangeCode::OTCM}, // OTC GREY MARKET
  {ExchangeCode::PINC, ExchangeCode::OTCM}, // OTC PINK CURRENT

  /*################# FINRA #################*/
  {ExchangeCode::FINR, ExchangeCode::FINR}, // FINRA
  {ExchangeCode::FINN, ExchangeCode::FINR}, // FINRA NASDAQ TRF (NJ)
  {ExchangeCode::FINC, ExchangeCode::FINR}, // FINRA NASDAQ TRF (Chicago)
  {ExchangeCode::FINY, ExchangeCode::FINR}, // FINRA NYSE TRF
  {ExchangeCode::XADF, ExchangeCode::FINR}, // FINRA ADF
  {ExchangeCode::FINO, ExchangeCode::FINR}, // FINRA ORF
  {ExchangeCode::OOTC, ExchangeCode::FINR}, // Other OTC

  /*################# OTHER US #################*/
  {ExchangeCode::OPRA, ExchangeCode::OPRA}, // OPRA
  {ExchangeCode::MEMX, ExchangeCode::MEMX}, // MEMX
  {ExchangeCode::MEMD, ExchangeCode::MEMX}, // MEMX Dark
  {ExchangeCode::MXOP, ExchangeCode::MEMX}, // MEMX Options
  {ExchangeCode::IEXG, ExchangeCode::IEXG}, // IEX
  {ExchangeCode::LTSE, ExchangeCode::LTSE}, // Long Term Stock Exchange

  /*################# Canadian Securities Exchange CSE #################*/
  {ExchangeCode::XCNQ, ExchangeCode::XCNQ}, // CSE
  {ExchangeCode::PURE, ExchangeCode::XCNQ}, // CSE Pure
  {ExchangeCode::CSE2, ExchangeCode::XCNQ}, // CSE CSE2

  /*################# TMX Group  #################*/
  {ExchangeCode::XTSE, ExchangeCode::XTSE}, // TSE
  {ExchangeCode::XDRK, ExchangeCode::XTSE}, // TSX Dark
  {ExchangeCode::XTSX, ExchangeCode::XTSX}, // TSX Venture
  {ExchangeCode::VDRK, ExchangeCode::XTSX}, // TSX Venture Dark
  {ExchangeCode::XTNX, ExchangeCode::XTSX}, // TSX Venture Nex
  {ExchangeCode::XATS, ExchangeCode::XATS}, // Alpha Exchange
  {ExchangeCode::XATX, ExchangeCode::XATS}, // Alpha X
  {ExchangeCode::ADRK, ExchangeCode::XATS}, // Alpha Dark
  {ExchangeCode::XMOD, ExchangeCode::XMOD}, // Montreal
  {ExchangeCode::XMOC, ExchangeCode::XMOD}, // Montreal Climate

  /*################# CBOE NEO #################*/
  {ExchangeCode::NEOE, ExchangeCode::NEOE}, // NEO Exchange
  {ExchangeCode::NEOD, ExchangeCode::NEOE}, // NEO Exchange Dark
  {ExchangeCode::NEON, ExchangeCode::NEOE}, // NEO Exchange (MARKET BY
  // PRICE),,549300MILSKTNBLQ1L12,NSPD,NEO-N,CA,TORONTO,WWW.NEOSTOCKEXCHANGE.COM,ACTIVE,20180723,20190624,,,
  {ExchangeCode::NEOC, ExchangeCode::NEOE}, // NEO Connect

  /*################# OTHER #################*/
  {ExchangeCode::XXXX, ExchangeCode::XXXX},

 /*################# NON ISO-10383 #################*/
  {ExchangeCode::PYPR, ExchangeCode::PYPR},
  {ExchangeCode::SIMU, ExchangeCode::SIMU},
};

ExchangeCode inline Exchange_to_OperatingMic(ExchangeCode& code) { return OperatingMic[code]; }

static std::unordered_map<ExchangeCode, str_t> ExchangeName = {
  /*################# NYSE #################*/
  {ExchangeCode::XNYS, "New York Stock Exchange"          },
  {ExchangeCode::NYSD, "NYSE Dark"                        },
  {ExchangeCode::XCIS, "NYSE National"                    },
  {ExchangeCode::CISD, "NYSE National Dark"               },
  {ExchangeCode::XCHI, "NYSE Chicago"                     },
  {ExchangeCode::ARCX, "NYSE ARCA"                        },
  {ExchangeCode::ARCD, "NYSE ARCA Dark"                   },
  {ExchangeCode::ARCO, "NYSE ARCA Options"                },
  {ExchangeCode::XASE, "NYSE AMEX"                        },
  {ExchangeCode::AMXO, "NYSE AMEX Options"                },

 /*################# NASDAQ #################*/
  {ExchangeCode::XNAS, "Nasdaq"                           },
  {ExchangeCode::XNGS, "Nasdaq Global Select"             },
  {ExchangeCode::XNCM, "Nasdaq Capital Markets"           },
  {ExchangeCode::XNMS, "Nasdaq Global Markets"            },
  {ExchangeCode::NASD, "Nasdaq Dark"                      },
  {ExchangeCode::XNDQ, "Nasdaq Options"                   },
  {ExchangeCode::XBOS, "Nasdaq BX"                        },
  {ExchangeCode::BOSD, "Nasdaq BX Dark"                   },
  {ExchangeCode::XBXO, "Nasdaq BX Options"                },
  {ExchangeCode::XPHL, "Nasdaq PHLX"                      },
  {ExchangeCode::XPSX, "Nasdaq PSX"                       },
  {ExchangeCode::PSXD, "Nasdaq PSX Dark"                  },
  {ExchangeCode::XPHO, "Nasdaq PSX Options"               },
  {ExchangeCode::XPBT, "Philadelphia Board of Trade"      },
  {ExchangeCode::XPOR, "Nasdaq Portal"                    },
  {ExchangeCode::XNFI, "Nasdaq Fixed Income"              },
  {ExchangeCode::XISE, "ISE Equities"                     },
  {ExchangeCode::GMNI, "ISE Gemini Options"               },
  {ExchangeCode::MCRY, "ISE Mercury Options"              },

 /*################# CBOE #################*/
  {ExchangeCode::XCBO, "CBOE Global Markets"              },
  {ExchangeCode::EDGA, "CBOE EDGA"                        },
  {ExchangeCode::EDGD, "CBOE EDGA Dark"                   },
  {ExchangeCode::EDGX, "CBOE EDGX"                        },
  {ExchangeCode::EDDP, "CBOE EDGX Dark"                   },
  {ExchangeCode::EDGO, "CBOE EDGX Options"                },
  {ExchangeCode::BATS, "CBOE BZX"                         },
  {ExchangeCode::BZXD, "CBOE BZX Dark"                    },
  {ExchangeCode::BATO, "CBOE BZX Options"                 },
  {ExchangeCode::BATY, "CBOE BYX"                         },
  {ExchangeCode::BYXD, "CBOE BYX Dark"                    },
  {ExchangeCode::C2OX, "CBOE C2 Options"                  },

 /*################# CME #################*/
  {ExchangeCode::XCME, "Chicago Mercantile Exchange"      },
  {ExchangeCode::FCME, "CME Floor"                        },
  {ExchangeCode::GLBX, "Globex"                           },
  {ExchangeCode::XCBT, "Chicago Board of Trade"           },
  {ExchangeCode::FCBT, "CBOT Floor"                       },
  {ExchangeCode::XKBT, "Kansas City Board of Trade"       },
  {ExchangeCode::XNYM, "New York Mercantile Exchange"     },

 /*################# MIAX #################*/
  {ExchangeCode::MIHI, "MIAX"                             },
  {ExchangeCode::MPRL, "MIAX Pearl"                       },
  {ExchangeCode::EPRL, "MIAX Pearl"                       },
  {ExchangeCode::EPRD, "MIAX Pearl Dark"                  },
  {ExchangeCode::XMIO, "MIAX Options"                     },
  {ExchangeCode::EMLD, "MIAX Emerald"                     },

 /*################# OTC Markets #################*/
  {ExchangeCode::OTCM, "OTC Markets"                      },
  {ExchangeCode::CAVE, "OTC Caveat Emptor"                },
  {ExchangeCode::OTCB, "OTC QB Marketplace"               },
  {ExchangeCode::OTCQ, "OTC QX Marketplace"               },
  {ExchangeCode::PINL, "OTC Pink Limited"                 },
  {ExchangeCode::PINI, "OTC Pink No Information"          },
  {ExchangeCode::PINX, "OTC Pink Marketplace"             },
  {ExchangeCode::PSGM, "OTC Grey Market"                  },
  {ExchangeCode::PINC, "OTC Pink Current"                 },

 /*################# FINRA #################*/
  {ExchangeCode::FINR, "FINRA"                            },
  {ExchangeCode::FINN, "FINRA NASDAQ TRF (NJ)"            },
  {ExchangeCode::FINC, "FINRA NASDAQ TRF (Chicago)"       },
  {ExchangeCode::FINY, "FINRA NYSE TRF"                   },
  {ExchangeCode::XADF, "FINRA ADF"                        },
  {ExchangeCode::FINO, "FINRA ORF"                        },
  {ExchangeCode::OOTC, "FINRA Other OTC"                  },

 /*################# OTHER US #################*/
  {ExchangeCode::OPRA, "Options Price Reporting Authority"},
  {ExchangeCode::MEMX, "Members Exchange"                 },
  {ExchangeCode::MEMD, "MEMX Dark"                        },
  {ExchangeCode::MXOP, "MEMX Options"                     },
  {ExchangeCode::IEXG, "Investors Exchange"               },
  {ExchangeCode::LTSE, "Long-Term Stock Exchange"         },

 /*################# Canadian Securities Exchange CSE #################*/
  {ExchangeCode::XCNQ, "Canadian Securities Exchange"     },
  {ExchangeCode::PURE, "CSE Pure"                         },
  {ExchangeCode::CSE2, "CSE CSE2"                         },

 /*################# TMX Group  #################*/
  {ExchangeCode::XTSE, "Toronto Stock Exchange"           },
  {ExchangeCode::XDRK, "TSE Dark"                         },
  {ExchangeCode::XTSX, "TRX Venture Exchange"             },
  {ExchangeCode::VDRK, "TRX Venture Exchange Dark"        },
  {ExchangeCode::XTNX, "TRX Venture Nex"                  },
  {ExchangeCode::XATS, "Alpha Exchange"                   },
  {ExchangeCode::XATX, "Alpha Exchange X"                 },
  {ExchangeCode::ADRK, "Alpha Exchange Dark"              },
  {ExchangeCode::XMOD, "Montréal Exchange"               },
  {ExchangeCode::XMOC, "Montréal Climate Exchange"       },

 /*################# CBOE NEO #################*/
  {ExchangeCode::NEOE, "NEO Exchange"                     },
  {ExchangeCode::NEOD, "NEO Exchange Dark"                },
  {ExchangeCode::NEON, "NEO Exchange"                     },
  {ExchangeCode::NEOC, "NEO Connect"                      },

 /*################# OTHER #################*/
  {ExchangeCode::XXXX, "Uncategorized"                    },

 /*################# NON ISO-10383 #################*/
  {ExchangeCode::PYPR, "Paper"                            },
  {ExchangeCode::SIMU, "Simulation"                       },
};

str_t inline Exchange_to_Name(ExchangeCode& code) { return ExchangeName[code]; }

static std::unordered_map<ExchangeCode, CountryCode> ExchangeCountry = {
  /*################# NYSE #################*/
  {ExchangeCode::XNYS, CountryCode::US},
  {ExchangeCode::NYSD, CountryCode::US},
  {ExchangeCode::XCIS, CountryCode::US},
  {ExchangeCode::CISD, CountryCode::US},
  {ExchangeCode::XCHI, CountryCode::US},
  {ExchangeCode::ARCX, CountryCode::US},
  {ExchangeCode::ARCD, CountryCode::US},
  {ExchangeCode::ARCO, CountryCode::US},
  {ExchangeCode::XASE, CountryCode::US},
  {ExchangeCode::AMXO, CountryCode::US},
 /*################# NASDAQ #################*/
  {ExchangeCode::XNAS, CountryCode::US},
  {ExchangeCode::XNGS, CountryCode::US},
  {ExchangeCode::XNCM, CountryCode::US},
  {ExchangeCode::XNMS, CountryCode::US},
  {ExchangeCode::NASD, CountryCode::US},
  {ExchangeCode::XNDQ, CountryCode::US},
  {ExchangeCode::XBOS, CountryCode::US},
  {ExchangeCode::BOSD, CountryCode::US},
  {ExchangeCode::XBXO, CountryCode::US},
  {ExchangeCode::XPHL, CountryCode::US},
  {ExchangeCode::XPSX, CountryCode::US},
  {ExchangeCode::PSXD, CountryCode::US},
  {ExchangeCode::XPHO, CountryCode::US},
  {ExchangeCode::XPBT, CountryCode::US},
  {ExchangeCode::XPOR, CountryCode::US},
  {ExchangeCode::XNFI, CountryCode::US},
  {ExchangeCode::XISE, CountryCode::US},
  {ExchangeCode::GMNI, CountryCode::US},
  {ExchangeCode::MCRY, CountryCode::US},

 /*################# CBOE #################*/
  {ExchangeCode::XCBO, CountryCode::US},
  {ExchangeCode::EDGA, CountryCode::US},
  {ExchangeCode::EDGD, CountryCode::US},
  {ExchangeCode::EDGX, CountryCode::US},
  {ExchangeCode::EDDP, CountryCode::US},
  {ExchangeCode::EDGO, CountryCode::US},
  {ExchangeCode::BATS, CountryCode::US},
  {ExchangeCode::BZXD, CountryCode::US},
  {ExchangeCode::BATO, CountryCode::US},
  {ExchangeCode::BATY, CountryCode::US},
  {ExchangeCode::BYXD, CountryCode::US},
  {ExchangeCode::C2OX, CountryCode::US},

 /*################# CME #################*/
  {ExchangeCode::XCME, CountryCode::US},
  {ExchangeCode::FCME, CountryCode::US},
  {ExchangeCode::GLBX, CountryCode::US},
  {ExchangeCode::XCBT, CountryCode::US},
  {ExchangeCode::FCBT, CountryCode::US},
  {ExchangeCode::XKBT, CountryCode::US},
  {ExchangeCode::XNYM, CountryCode::US},

 /*################# MIAX #################*/
  {ExchangeCode::MIHI, CountryCode::US},
  {ExchangeCode::MPRL, CountryCode::US},
  {ExchangeCode::EPRL, CountryCode::US},
  {ExchangeCode::EPRD, CountryCode::US},
  {ExchangeCode::XMIO, CountryCode::US},
  {ExchangeCode::EMLD, CountryCode::US},

 /*################# OTC Markets #################*/
  {ExchangeCode::OTCM, CountryCode::US},
  {ExchangeCode::CAVE, CountryCode::US},
  {ExchangeCode::OTCB, CountryCode::US},
  {ExchangeCode::OTCQ, CountryCode::US},
  {ExchangeCode::PINL, CountryCode::US},
  {ExchangeCode::PINI, CountryCode::US},
  {ExchangeCode::PINX, CountryCode::US},
  {ExchangeCode::PSGM, CountryCode::US},
  {ExchangeCode::PINC, CountryCode::US},

 /*################# FINRA #################*/
  {ExchangeCode::FINR, CountryCode::US},
  {ExchangeCode::FINN, CountryCode::US},
  {ExchangeCode::FINC, CountryCode::US},
  {ExchangeCode::FINY, CountryCode::US},
  {ExchangeCode::XADF, CountryCode::US},
  {ExchangeCode::FINO, CountryCode::US},
  {ExchangeCode::OOTC, CountryCode::US},

 /*################# OTHER US #################*/
  {ExchangeCode::OPRA, CountryCode::US},
  {ExchangeCode::MEMX, CountryCode::US},
  {ExchangeCode::MEMD, CountryCode::US},
  {ExchangeCode::MXOP, CountryCode::US},
  {ExchangeCode::IEXG, CountryCode::US},
  {ExchangeCode::LTSE, CountryCode::US},

 /*################# Canadian Securities Exchange CSE #################*/
  {ExchangeCode::XCNQ, CountryCode::CA},
  {ExchangeCode::PURE, CountryCode::CA},
  {ExchangeCode::CSE2, CountryCode::CA},

 /*################# TMX Group  #################*/
  {ExchangeCode::XTSE, CountryCode::CA},
  {ExchangeCode::XDRK, CountryCode::CA},
  {ExchangeCode::XTSX, CountryCode::CA},
  {ExchangeCode::VDRK, CountryCode::CA},
  {ExchangeCode::XTNX, CountryCode::CA},
  {ExchangeCode::XATS, CountryCode::CA},
  {ExchangeCode::XATX, CountryCode::CA},
  {ExchangeCode::ADRK, CountryCode::CA},
  {ExchangeCode::XMOD, CountryCode::CA},
  {ExchangeCode::XMOC, CountryCode::CA},

 /*################# CBOE NEO #################*/
  {ExchangeCode::NEOE, CountryCode::CA},
  {ExchangeCode::NEOD, CountryCode::CA},
  {ExchangeCode::NEON, CountryCode::CA},
  {ExchangeCode::NEOC, CountryCode::CA},

 /*################# OTHER #################*/
  {ExchangeCode::XXXX, CountryCode::XX},

 /*################# NON ISO-10383 #################*/
  {ExchangeCode::PYPR, CountryCode::XX},
  {ExchangeCode::SIMU, CountryCode::XX},
};

CountryCode inline Exchange_to_Country(ExchangeCode& code) { return ExchangeCountry[code]; }

}
