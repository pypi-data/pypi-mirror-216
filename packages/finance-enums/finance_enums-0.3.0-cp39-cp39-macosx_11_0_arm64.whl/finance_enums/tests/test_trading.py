from finance_enums import OrderType, Side, TimeInForce, OrderFlag, TradingType


class TestCurrency:
    def test_order_type_basic(self):
        assert len(OrderType.__members__) == 3

    def test_side_basic(self):
        assert len(Side.__members__) == 3

    def test_time_in_force_basic(self):
        assert len(TimeInForce.__members__) == 3

    def test_order_flag_basic(self):
        assert len(OrderFlag.__members__) == 4

    def test_trading_type_basic(self):
        assert len(TradingType.__members__) == 4
