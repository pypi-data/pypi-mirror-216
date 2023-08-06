from finance_enums import ExchangeCode


class TestExchange:
    def test_exchange_basic(self):
        assert len(ExchangeCode.__members__) == 96
