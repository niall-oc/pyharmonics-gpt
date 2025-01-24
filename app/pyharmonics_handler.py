from pyharmonics.marketdata import YahooCandleData, BinanceCandleData, YahooOptionData
from pyharmonics.technicals import OHLCTechnicals
from pyharmonics.search import HarmonicSearch, DivergenceSearch
from pyharmonics.positions import Position
from pyharmonics.plotter import HarmonicPlotter, PositionPlotter, OptionPlotter
import base64
import logging

logging.basicConfig(level=logging.DEBUG)


def outcome(t, hs, d, p):
    assesment = {
        'patterns': hs.get_patterns(formed=False),
        'divergences': {family: [p.to_dict() for p in found[:1]] for family, found in d.get_patterns().items()},
    }
    logging.debug(f"XABCD: {len(assesment['patterns']['XABCD'])} ABCD: {len(assesment['patterns']['ABCD'])} ABC: {len(assesment['patterns']['ABC'])}")
    if assesment['patterns']['XABCD']:
        pattern = assesment['patterns']['XABCD'][0]
    elif assesment['patterns']['ABCD']:
        pattern = assesment['patterns']['ABCD'][0]
    elif assesment['patterns']['ABC']:
        pattern = assesment['patterns']['ABC'][0]
    else:
        pattern = None

    if pattern:
        logging.debug(f"Pattern: {pattern}")
        strike = (pattern.completion_min_price + pattern.completion_max_price) / 2
        position = Position(pattern, strike=strike, dollar_amount=100)
        logging.debug(f"Position: {position}")
        pos_plot = PositionPlotter(t, position)
        pos_plot.add_divergence_plots(d.get_patterns())
        logging.debug(f"Position plot built: {pos_plot}")
        encoded_img = base64.b64encode(pos_plot.to_image(dpi=600)).decode('utf-8')
        assesment['plot'] = f'{encoded_img}'
        assesment['position'] = position
    else:
        encoded_img = base64.b64encode(p.to_image(dpi=600)).decode('utf-8')
        assesment['plot'] = f'{encoded_img}'
    return assesment

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
    return outcome(t, hs, d, p)


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
    return outcome(t, hs, d, p)


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


if __name__ == "__main__":
    whats_forming_binance('STORJUSDT', '1d')
