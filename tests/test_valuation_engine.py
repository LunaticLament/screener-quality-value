import math
from valuation_engine import dcf_per_share, implied_irr, reverse_growth, calculate


def test_dcf_steady():
    x=dcf_per_share(5,0.02,0.1,0.02)
    assert math.isclose(x['value'], 63.75, rel_tol=1e-7)
    assert math.isclose(implied_irr(x['value'],x['annual_flows'],x['terminal_value']),0.1,rel_tol=1e-8)
    assert math.isclose(reverse_growth(x['value'],5,0.1,0.02),0.02,abs_tol=1e-8)


def test_invalid_terminal_and_loss():
    assert dcf_per_share(5,.03,.02,.025) is None
    assert dcf_per_share(-1,.03,.1,.02) is None


def test_sector_block():
    result=calculate({'ticker':'BNP.PA','name':'BNP','model':'bank','price':40,'currency':'EUR'}, {})
    assert result['status']=='modèle_sectoriel_requis' and not result['scenarios']


def test_three_years_preliminary_only():
    company={'ticker':'XYZ','name':'XYZ','model':'corporate','price':45.0,'currency':'USD','price_asof':'2026-11-11'}
    history={'currency':'USD','source_type':'secondary','annual':{
        '2022-12-31':{'cfo':1250,'capex':250,'diluted_shares':100},
        '2023-12-31':{'cfo':1300,'capex':240,'diluted_shares':100},
        '2024-12-31':{'cfo':1500,'capex':300,'diluted_shares':100}}}
    result=calculate(company,history)
    assert result['status']=='prévalorisation_indicative'
    assert result['validation']=='Aucune recommandation'
    assert result['coverage_years']==3
    assert result['scenarios']['central']['value']>0
    assert result['reverse_growth'] is not None
    assert any('cinq exercices' in w for w in result['warnings'])


def test_mismatched_currency_blocks():
    company={'ticker':'XYZ','name':'XYZ','model':'corporate','price':45,'currency':'EUR'}
    hist={'currency':'USD','annual':{'2022-12-31':{'cfo':100,'capex':10,'diluted_shares':10},
        '2023-12-31':{'cfo':105,'capex':10,'diluted_shares':10},
        '2024-12-31':{'cfo':115,'capex':10,'diluted_shares':10}}}
    assert calculate(company,hist)['status']=='non_modélisable'