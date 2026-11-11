import math
from valuation_engine import calculate, dcf_per_share


def model():
    periods = {str(y) + '-12-31': {'cfo': 150 + (y-2021)*5, 'capex': -50,
                                  'diluted_shares': 10, 'revenue': 300} for y in range(2021, 2026)}
    company = {'ticker':'TEST','name':'Exemple','model':'corporate',
               'currency':'EUR','price':120,'price_asof':'2026-11-11'}
    return calculate(company, {'annual':periods,'currency':'EUR','source_type':'secondary'})


def test_ten_year_projection_and_discounted_cashflow_bridge():
    m = model()
    assert m['status'] == 'prévalorisation_indicative'
    for scenario in m['scenarios'].values():
        rows = scenario['projection']
        assert len(rows) == 10
        assert [x['year'] for x in rows] == list(range(1,11))
        assert math.isclose(sum(x['pv_fcf_per_share'] for x in rows), scenario['pv_flows'],rel_tol=1e-12)
        assert math.isclose(rows[-1]['cumulative_pv'],scenario['pv_flows'],rel_tol=1e-12)
        assert math.isclose(scenario['value'],scenario['pv_flows']+scenario['pv_terminal'],rel_tol=1e-12)
        assert math.isclose(rows[-1]['fcf_per_share']*(1+scenario['terminal_growth'])/(scenario['discount']-scenario['terminal_growth']),scenario['terminal_value'],rel_tol=1e-12)


def test_anchor_bridge_explicitly_unverified():
    m = model()
    bridge = m['anchor_bridge']
    assert bridge['normalization_adjustments'] is None
    assert bridge['selected_fcfps'] == m['anchor_fcfps']
    assert bridge['selected_fcfps'] == min(bridge['latest_fcfps'],bridge['mean_last_three_fcfps'])