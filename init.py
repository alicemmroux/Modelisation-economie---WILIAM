import xarray as xr


_subscript_dict = {
    "HOUSEHOLDS_I": ["LowINC", "HighINC"],
    "REGIONS_I": ["FR", "IT"],
}

#taux de variation EXO
def depreciation_rate_real_estate_sp():
    return xr.DataArray(
        [0.5, 0.08],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def increase_in_households_capital_stock_due_to_investments():
    return xr.DataArray(
        [[0.05, 0.04], [0.03, 0.02]],  # 5%, 4% etc.
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def variation_in_households_capital_stock_due_to_revalorizations():
    return xr.DataArray(
        [[0.02, 0.01], [0.03, 0.01]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def decrease_in_households_capital_stock_due_to_depreciation():
    return xr.DataArray(
        [[0.01, 0.02], [0.01, 0.03]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def increase_in_households_capital_stock_due_to_investments():
    return xr.DataArray(
        [[50, 100], [40, 75]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def ratio_liabilities_to_disposable_income():
    return xr.DataArray(
        [[0.02, 0.025], [0.015, 0.025]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def adjustment_factor_labour_compensation():
    return xr.DataArray(
        [[0.03, 0.035], [0.025, 0.03]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def adjustment_factor_social_benefits():
    return xr.DataArray(
        [[0.035, 0.04], [0.02, 0.025]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def adjustment_factor_net_operating_surplus():
    return xr.DataArray(
        [[0.05, 0.06], [0.03, 0.04]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

#variables d'initialisation

def initial_households_capital_stock():
    return xr.DataArray(
        [[20000, 50000], [30000, 60000]],
        dims = _subscript_dict.keys(),
        coords=_subscript_dict,
    )

def base_number_of_households():
    return xr.DataArray(
        [[2, 3], [3, 6]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def initial_households_financial_assets():
    return xr.DataArray(
        [[5000, 6000], [4000, 5500]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def total_households_consumption_coicop():
    return xr.DataArray(
        [[5000, 9000], [4000, 7500]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def initial_households_financial_liabilities():
    return xr.DataArray(
        [[300, 500], [200, 400]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def initial_households_gross_labor_income():
    return xr.DataArray(
        [[25000, 35000], [20000, 30000]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def households_basic_income():
    return xr.DataArray(
        [[200, 200], [175, 175]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def initial_households_social_benefits():
    return xr.DataArray(
        [[150, 150], [125, 125]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def initial_households_net_operating_surplus():
    return xr.DataArray(
        [[600, 1200], [800, 1100]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def households_other_transfers_paid():
    return xr.DataArray(
        [[50, 40], [30, 25]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def households_other_transfers_received():
    return xr.DataArray(
        [[55, 45], [35, 25]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

#taux d'imposition et taux d'interet
def household_tax_rate_on_assets_to_finance_basic_income():
    return xr.DataArray(
        [[0.05, 0.06], [0.06, 0.07]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def interest_rate_for_households_liabilities():
    return xr.DataArray(
        [[0.02, 0.03], [0.02, 0.03]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def interest_rate_for_households_assets():
    return xr.DataArray(
        [[0.02, 0.03], [0.02, 0.03]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def wealth_tax_rate():
    return xr.DataArray(
        [[0, 0.1], [0.015, 0.12]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def households_social_security_rate():
    return xr.DataArray(
        [[0.02, 0.03], [0.025, 0.035]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

def income_tax_rate():
    return xr.DataArray(
        [[0.20, 0.30], [0.22, 0.35]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )