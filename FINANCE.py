import xarray as xr

import K_stock
years = list(range(2014, 2016))
capitalstock_proj = K_stock.households_capital_stock_over_time(years)

_subscript_dict = {
    "REGIONS_I": ["FR", "IT"],
    "HOUSEHOLDS_I": ["LowINC", "HighINC"],
}

def base_number_of_households():
    return xr.DataArray(
        [[2, 3], [3, 6]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def household_tax_rate_on_assets_to_finance_basic_income():
    return xr.DataArray(
        [[0.05, 0.06], [0.06, 0.07]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def interest_rate_for_households_liabilities():
    return xr.DataArray(
        [[0.02, 0.03], [0.02, 0.03]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def interest_rate_for_households_assets():
    return xr.DataArray(
        [[0.02, 0.03], [0.02, 0.03]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )


def initial_households_financial_assets():
    return xr.DataArray(
        [[5000, 6000], [4000, 5500]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )


def households_disposable_income():
    return xr.DataArray(
        [[20000, 30000], [15000, 22000]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )


def total_households_consumption_coicop():
    return xr.DataArray(
        [[5000, 9000], [4000, 7500]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )


def increase_in_households_capital_stock_due_to_investments():
    return xr.DataArray(
        [[50, 100], [40, 75]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )


def households_gross_savings():
    return households_disposable_income() - total_households_consumption_coicop()


def households_net_lending():
    return households_gross_savings() - increase_in_households_capital_stock_due_to_investments()


def initial_households_financial_liabilities():
    return xr.DataArray(
        [[300, 500], [200, 400]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,

    )


def ratio_liabilities_to_disposable_income():
    return xr.DataArray(
        [[0.02, 0.025], [0.015, 0.025]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )


def wealth_tax_rate():
    return xr.DataArray(
        [[0, 0.1], [0.015, 0.12]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )


def variation_in_households_financial_liabilities(current_liabilities):
    return ratio_liabilities_to_disposable_income() * households_disposable_income() - current_liabilities


def households_financial_liabilities_over_time(years):
    stock = initial_households_financial_liabilities() / base_number_of_households()
    results = []

    for yr in years:
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = variation_in_households_financial_liabilities(stock)

        stock = stock + growth
        results.append(stock.copy())

    return xr.concat(results, dim="Year").assign_coords({"Year": years})


def variation_households_financial_assets(liabilities):
    return households_net_lending() + variation_in_households_financial_liabilities(liabilities)


def households_financial_assets_over_time(years, liabilities_by_year):
    stock = initial_households_financial_assets() / base_number_of_households()
    results = []

    for i, yr in enumerate(years):
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            liabilities = liabilities_by_year.sel(Year=yr)
            growth = variation_households_financial_assets(liabilities)

        stock = stock + growth
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})


def households_property_income_paid_over_time(years, liabilities_by_year):
    rate = interest_rate_for_households_liabilities()
    results = []

    for yr in years:
        liabilities = liabilities_by_year.sel(Year=yr)
        payment = liabilities * rate
        payment = payment.expand_dims(Year=[yr])  # Add year coordinate for concat
        results.append(payment)

    return xr.concat(results, dim="Year").assign_coords({"Year": years})


def compute_households_property_income_paid(years, liabilities_proj):
    return households_property_income_paid_over_time(years, liabilities_proj)


def households_property_income_received_over_time(years, assets_by_year, capitalstock_proj):
    rate = interest_rate_for_households_assets()
    results = []

    for yr in years:
        assets_t = assets_by_year.sel(Year=yr)
        capital_t = capitalstock_proj.sel(Year=yr)
        payment = (assets_t + capital_t) * rate
        results.append(payment.expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year")


def households_net_wealth_over_time(years, liabilities_by_year, assets_by_year, capitalstock_proj):
    results = []

    for yr in years:
        assets_t = assets_by_year.sel(Year=yr)
        capital_t = capitalstock_proj.sel(Year=yr)
        liabilities_t = liabilities_by_year.sel(Year=yr)
        payment = assets_t + capital_t - liabilities_t
        results.append(payment.expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year")


def households_wealth_tax_over_time(net_wealth_proj):
    return net_wealth_proj * wealth_tax_rate()

if __name__ == "__main__":
    years = list(range(2014, 2016))

    # Compute liabilities over time
    liabilities_proj = households_financial_liabilities_over_time(years)

    gross_savings_proj = households_gross_savings()

    # Compute assets over time using liabilities
    assets_proj = households_financial_assets_over_time(years, liabilities_proj)

    # Compute property income paid using liabilities
    property_income_paid = compute_households_property_income_paid(years, liabilities_proj)

    # Compute property income received using assets
    property_income_received = households_property_income_received_over_time(years, assets_proj, capitalstock_proj)

    net_wealth_proj = households_net_wealth_over_time(years, liabilities_proj, assets_proj, capitalstock_proj)

    wealth_tax_proj = households_wealth_tax_over_time(net_wealth_proj)

    # Output section
    #print("FINANCIAL LIABILITIES:")
    #print(liabilities_proj)

    #print("\nFINANCIAL ASSETS:")
    #print(assets_proj)

    #print("\nPROPERTY INCOME PAID:")
    #print(property_income_paid)

    #print("\nPROPERTY INCOME RECEIVED:")
    #print(property_income_received)

    print("\nAssets in 2015:")
    print(assets_proj.sel(Year=2015))

    print("\nLiabilities in 2015:")
    print(liabilities_proj.sel(Year=2015))

    print("\nCapital Stock in 2015:")
    print(capitalstock_proj.sel(Year=2015))

    print("\nProperty Income Paid in 2015:")
    print(property_income_paid.sel(Year=2015))

    print("\nProperty Income Received in 2015:")
    print(property_income_received.sel(Year=2015))

    print("\nNet Wealth in 2015:")
    print(net_wealth_proj.sel(Year=2015))

    print("\nWealth Tax in 2015:")
    print(wealth_tax_proj.sel(Year=2015))


