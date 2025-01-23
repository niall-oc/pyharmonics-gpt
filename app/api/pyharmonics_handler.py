from pyharmonics.marketdata import YahooCandleData, BinanceCandleData, YahooOptionData
from pyharmonics.technicals import OHLCTechnicals
from pyharmonics.search import HarmonicSearch, DivergenceSearch
from pyharmonics.positions import Position
from pyharmonics.plotter import HarmonicPlotter, PositionPlotter, OptionPlotter
import json


def play_position(hs, pattern, strike, dollar_amount):
    pos = Position(pattern, strike, dollar_amount)
    p = PositionPlotter(hs.td, pos)
    p.add_peaks()


def whats_new(cd, limit_to=-1):
    t = OHLCTechnicals(cd.df, cd.symbol, cd.interval)
    hs = HarmonicSearch(t)
    hs.search(limit_to=limit_to)
    p = HarmonicPlotter(t)
    d = DivergenceSearch(t)
    d.search(limit_to=limit_to)
    p.add_peaks()
    p.add_harmonic_plots(hs.get_patterns(family=hs.XABCD))
    p.add_harmonic_plots(hs.get_patterns(family=hs.ABCD))
    p.add_harmonic_plots(hs.get_patterns(family=hs.ABC))
    p.add_divergence_plots(d.get_patterns())
    return {
        # 'plot': p,
        'patterns': {family: [p.to_dict() for p in found] for family, found in hs.get_patterns().items()},
        'divergences': {family: [p.to_dict() for p in found] for family, found in d.get_patterns().items()},
    }


def whats_new_binance(symbol, interval, limit_to=-1, candles=1000):
    bc = BinanceCandleData()
    bc.get_candles(symbol, interval, candles)
    return whats_new(bc, limit_to=limit_to)


def whats_new_yahoo(symbol, interval, limit_to=-1, candles=1000):
    yc = YahooCandleData()
    yc.get_candles(symbol, interval, candles)
    return whats_new(yc, limit_to=limit_to)


def whats_forming(cd, limit_to=10, percent_complete=0.8):
    t = OHLCTechnicals(cd.df, cd.symbol, cd.interval)
    hs = HarmonicSearch(t)
    hs.forming(limit_to=limit_to, percent_c_to_d=percent_complete)
    p = HarmonicPlotter(t)
    d = DivergenceSearch(t)
    d.search(limit_to=limit_to)
    p.add_peaks()
    p.add_harmonic_plots(hs.get_patterns(family=hs.XABCD, formed=False))
    p.add_harmonic_plots(hs.get_patterns(family=hs.ABCD, formed=False))
    p.add_harmonic_plots(hs.get_patterns(family=hs.ABC, formed=False))
    p.add_divergence_plots(d.get_patterns())
    return {
        # 'plot': p,
        'patterns': {family: [p.to_dict() for p in found] for family, found in hs.get_patterns(formed=False).items()},
        'divergences': {family: [p.to_dict() for p in found[:3]] for family, found in d.get_patterns().items()},
    }


def whats_forming_binance(symbol, interval, limit_to=10, percent_complete=0.8, candles=1000):
    bc = BinanceCandleData()
    bc.get_candles(symbol, interval, candles)
    return whats_forming(bc, limit_to=limit_to, percent_complete=percent_complete)


def whats_forming_yahoo(symbol, interval, limit_to=10, percent_complete=0.8, candles=1000):
    yc = YahooCandleData()
    yc.get_candles(symbol, interval, candles)
    return whats_forming(yc, limit_to=limit_to, percent_complete=percent_complete)


def whats_options_volume(symbol):
    yo = YahooOptionData(symbol)
    yo.analyse_options(trend='volume')
    p = OptionPlotter(yo, yo.ticker.options[0])
    return p, yo


def whats_options_interest(symbol):
    yo = YahooOptionData(symbol)
    yo.analyse_options()
    p = OptionPlotter(yo, yo.ticker.options[0])
    return p. yo


def parse_args(string):
    """
        Parses the given string into Python variables.

        Args:
            string: The string to be parsed.

        Returns:
            A tuple containing the parsed args and kwargs.
    """
    try:
        data = json.loads(string)
        args = data.get('args', [])
        kwargs = data.get('kwargs', {})
        return args, kwargs
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON string: {string}")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None
