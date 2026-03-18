from .currency_checker import CurrencyChecker


def init_currency_checker(api: str, **kwargs) -> CurrencyChecker:
    if api == 'fixer':
        from .fixer import FixerCurrencyChecker
        return FixerCurrencyChecker(**kwargs)
    elif api == 'geoapi':
        from .geoapi import GeoCurrencyChecker
        return GeoCurrencyChecker(**kwargs)
    raise ValueError(f"Unknown currency API: {api!r}. Supported values: 'fixer', 'geoapi'")


__all__ = ['CurrencyChecker', 'init_currency_checker']
