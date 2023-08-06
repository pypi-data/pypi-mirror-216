from finance_enums import Currency


class TestCurrency:
    def test_currency_basic(self):
        assert len(Currency.__members__) == 183
        assert str(Currency.USD) == "USD"
        assert Currency.USD.currency_name() == "United States dollar"
    
    def test_noniso_currency_pennies(self):
        assert Currency("EUr") == Currency.EUX
        assert Currency("GBp") == Currency.GBX
        assert Currency("USd") == Currency.USX
