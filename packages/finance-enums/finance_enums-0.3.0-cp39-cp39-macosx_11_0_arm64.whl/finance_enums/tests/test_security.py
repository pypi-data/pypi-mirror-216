from finance_enums import (
    SecurityType,
    EquityType,
    OptionType,
    BondType,
    CommodityType,
    FundType,
    OptionExerciseType,
    FundSubType,
    MutualFundEndedness,
)


class TestSecurityType:
    def test_security_type_basic(self):
        assert len(SecurityType.__members__) == 12

    def test_equity_type_basic(self):
        assert len(EquityType.__members__) == 5

    def test_option_type_basic(self):
        assert len(OptionType.__members__) == 2

    def test_bond_type_basic(self):
        assert len(BondType.__members__) == 3

    def test_commodity_type_basic(self):
        assert len(CommodityType.__members__) == 3

    def test_fund_type_basic(self):
        assert len(FundType.__members__) == 3

    def test_option_exercise_type_basic(self):
        assert len(OptionExerciseType.__members__) == 3

    def test_fund_subtype_basic(self):
        assert len(FundSubType.__members__) == 4

    def test_mutual_fund_endedness_basic(self):
        assert len(MutualFundEndedness.__members__) == 2
