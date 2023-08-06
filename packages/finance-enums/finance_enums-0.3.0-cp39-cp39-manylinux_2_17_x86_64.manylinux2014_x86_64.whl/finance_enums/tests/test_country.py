from finance_enums import CountryCode, CountryCode3


class TestCountry:
    def test_country_basic(self):
        assert len(CountryCode.__members__) == 250
        assert CountryCode.US.country_name() == "United States of America"
        assert CountryCode.US.code3() == CountryCode3.USA
