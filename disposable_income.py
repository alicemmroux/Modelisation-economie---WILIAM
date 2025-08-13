import xarray as xr
import math
import numpy as np


import K_stock
years = list(range(2014, 2017))
capitalstock_proj = K_stock.households_capital_stock_over_time(years)


import FINANCE
years = list(range(2014, 2017))
liabilities_proj = FINANCE.households_financial_liabilities_over_time(years)
assets_proj = FINANCE.households_financial_assets_over_time(years, liabilities_proj)
property_income_paid = FINANCE.households_property_income_paid_over_time(years, liabilities_proj)
property_income_received = FINANCE.households_property_income_received_over_time(years, assets_proj, capitalstock_proj)
net_wealth_proj = FINANCE.households_net_wealth_over_time(years, liabilities_proj, assets_proj, capitalstock_proj)
wealth_tax_proj = FINANCE.households_wealth_tax_over_time(net_wealth_proj)

_subscript_dict = {
    "HOUSEHOLDS_I": ["LowINC", "HighINC"],
    "REGIONS_I": ["FR", "IT"],
}

def households_social_security_rate():
    return xr.DataArray(
        [[0.02, 0.03], [0.025, 0.035]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def initial_households_gross_labor_income():
    return xr.DataArray(
        [[25000, 35000], [20000, 30000]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def adjustment_factor_labour_compensation():
    return xr.DataArray(
        [[0.03, 0.035], [0.025, 0.03]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )


def households_basic_income():
    return xr.DataArray(
        [[200, 200], [175, 175]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def adjustment_factor_social_benefits():
    return xr.DataArray(
        [[0.035, 0.04], [0.02, 0.025]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def initial_households_social_benefits():
    return xr.DataArray(
        [[150, 150], [125, 125]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def initial_households_net_operating_surplus():
    return xr.DataArray(
        [[600, 1200], [800, 1100]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def adjustment_factor_net_operating_surplus():
    return xr.DataArray(
        [[0.05, 0.06], [0.03, 0.04]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )


def households_other_transfers_paid():
    return xr.DataArray(
        [[50, 40], [30, 25]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def households_other_transfers_received():
    return xr.DataArray(
        [[55, 45], [35, 25]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def income_tax_rate():
    return xr.DataArray(
        [[0.20, 0.30], [0.22, 0.35]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def households_gross_labour_income_over_time(years):
    stock = initial_households_gross_labor_income()
    results = []

    for i, yr in enumerate(years):
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = adjustment_factor_labour_compensation()

        stock = stock * (1 + growth)
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})

def households_net_operating_surplus(years):
    stock = initial_households_net_operating_surplus()
    results = []

    for i, yr in enumerate(years):
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = adjustment_factor_net_operating_surplus()

        stock = stock * (1 + growth)
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})


def households_social_benefits(years):
    stock = initial_households_social_benefits()
    results = []

    for i, yr in enumerate(years):
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = adjustment_factor_social_benefits()

        stock = stock * (1 + growth)
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})


def households_social_security_payments(gross_labour_income_proj):
    return gross_labour_income_proj * households_social_security_rate()


def households_net_labour_income_over_time(gross_labour_income_proj, social_security_payments_proj):
    return gross_labour_income_proj - social_security_payments_proj

def taxable_income_over_time(net_labor_income_proj, social_security_payments_proj, net_operating_surplus_proj, property_income_received, social_benefits_proj):
    return net_labor_income_proj + social_security_payments_proj + net_operating_surplus_proj + property_income_received + social_benefits_proj + households_other_transfers_received()

def delayed_households_taxable_income_over_time(taxable_income_proj, delay=1):
    return taxable_income_proj.shift(Year=delay)

def households_income_tax():
    return delayed_taxable_income_proj * income_tax_rate()

def households_disposable_income(net_labor_income_proj, social_benefits_proj, income_tax_proj, property_income_paid, wealth_tax_proj):
    return (net_labor_income_proj + social_benefits_proj + households_other_transfers_received() + property_income_received + households_basic_income())- (income_tax_proj + households_other_transfers_paid() + property_income_paid + wealth_tax_proj)

#ENERGY CONSUMPTION

def income_elasticity_households_fuel_transport():
    return xr.DataArray(
        [[0.7, 0.7], [0.7, 0.7]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def income_elasticity_households_air_transport():
    return xr.DataArray(
        [[1.1, 1.1], [1.1, 1.1]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def price_elasticity_households_fuel_transport():
    return xr.DataArray(
        [[0.4, 0.4], [0.4, 0.4]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def price_elasticity_households_air_transport():
    return xr.DataArray(
        [[0.8, 0.8], [0.8, 0.8]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def price_households_air_transport():
    return xr.DataArray(
        [[215, 500], [150, 225]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )
def price_households_fuel_transport():
    return xr.DataArray(
        [[1100, 2000], [1500, 2500]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def consumption_households_air_transport(disposable_income_proj):
    return np.exp(np.log(disposable_income_proj)*income_elasticity_households_air_transport() - np.log(price_households_air_transport() )* price_elasticity_households_air_transport() )

def consumption_households_fuel_transport(disposable_income_proj):
    return np.exp(np.log(disposable_income_proj)*income_elasticity_households_fuel_transport() - np.log(price_households_fuel_transport() )* price_elasticity_households_fuel_transport() )


 #GOVERNMENT SUBMODULE

def interest_rate_government_debt():
    return xr.DataArray(
        [[0.034, 0.034], [0.036, 0.036]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def base_number_of_households_in_millions():
    return xr.DataArray(
        [[2, 3], [3, 6]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def government_spending_basic_income():
    return households_basic_income() * base_number_of_households_in_millions()

def climate_change_damage_rate_on_capital_stock():
    return xr.DataArray(
        [[0.15, 0.10], [0.12, 0.14]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def public_gfcf_to_replace_climate_damage_over_time():


def government_investment():
    return

if __name__ == "__main__":
    years = list(range(2014, 2017))

    gross_labour_income_proj = households_gross_labour_income_over_time(years)

    social_security_payments_proj = households_social_security_payments(gross_labour_income_proj)

    net_labor_income_proj = households_net_labour_income_over_time(gross_labour_income_proj, social_security_payments_proj)

    social_benefits_proj = households_social_benefits(years)

    net_operating_surplus_proj = households_net_operating_surplus(years)

    taxable_income_proj = taxable_income_over_time(net_labor_income_proj, social_security_payments_proj, net_operating_surplus_proj, property_income_received, social_benefits_proj)

    delayed_taxable_income_proj = delayed_households_taxable_income_over_time(taxable_income_proj)

    income_tax_proj = households_income_tax()

    disposable_income_proj= households_disposable_income(net_labor_income_proj, social_benefits_proj, income_tax_proj, property_income_paid,
                                 wealth_tax_proj)

    air_transport_consumption_proj = consumption_households_air_transport(disposable_income_proj)

    fuel_transport_consumption_proj = consumption_households_fuel_transport(disposable_income_proj)

    print("GROSS LABOUR INCOME:")
    print(gross_labour_income_proj)

    print("\nGross Labour Income in 2015:")
    print(gross_labour_income_proj.sel(Year=2015))

    print("\nSocial Security Payments in 2015:")
    print(social_security_payments_proj.sel(Year=2015))

    print("\nNet Labour Income in 2015:")
    print(net_labor_income_proj.sel(Year=2015))

    print("\nSocial Benefits in 2015:")
    print(social_benefits_proj.sel(Year=2015))

    print("\nNet Operating Surplus in 2015:")
    print(net_operating_surplus_proj.sel(Year=2015))

    print("\nTaxable Income in 2015:")
    print(taxable_income_proj.sel(Year=2015))

    print("\nTaxable Income in 2014:")
    print(delayed_taxable_income_proj.sel(Year=2015))

    print("\nIncome Tax in 2015:")
    print(income_tax_proj.sel(Year=2015))

    print("Disposable Income in 2015:")
    print(disposable_income_proj.sel(Year=2015))

    print("Consumption of air transport in 2015:")
    print(air_transport_consumption_proj.sel(Year=2015))

    print("Consumption of air transport in 2015:")
    print(fuel_transport_consumption_proj.sel(Year=2015))
