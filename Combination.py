import xarray as xr


_subscript_dict = {
    "HOUSEHOLDS_I": ["LowINC", "HighINC"],
    "REGIONS_I": ["FR", "IT"],
}

#K_stock

def depreciation_rate_real_estate_sp():
    return xr.DataArray(
        [0.5, 0.08],
        coords={"REGIONS_I": _subscript_dict["REGIONS_I"]},
        dims=["REGIONS_I"]
    )

def initial_households_capital_stock():
    return xr.DataArray(
        [[20000, 50000], [30000, 60000]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def base_number_of_households():
    return xr.DataArray(
        [[2, 3], [3, 6]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def increase_in_households_capital_stock_due_to_investments():
    return xr.DataArray(
        [[0.05, 0.04], [0.03, 0.02]],  # 5%, 4% etc.
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def variation_in_households_capital_stock_due_to_revalorizations():
    return xr.DataArray(
        [[0.02, 0.01], [0.03, 0.01]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )

def decrease_in_households_capital_stock_due_to_depreciation():
    return xr.DataArray(
        [[0.01, 0.02], [0.01, 0.03]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
    )


def households_capital_stock_over_time(years):
    # Initial value per household
    stock = initial_households_capital_stock() / base_number_of_households()
    results = []

    for yr in years:
        if yr < 2015:
            rate = xr.zeros_like(stock)
        else:
            growth_rate = (
                increase_in_households_capital_stock_due_to_investments()
                + variation_in_households_capital_stock_due_to_revalorizations()
                - decrease_in_households_capital_stock_due_to_depreciation()
            )
            rate = stock * growth_rate  # multiply initial by rate

        stock = stock + rate
        results.append(stock)

    return xr.concat(results, dim="Year").assign_coords({"Year": years})

#END OF K_STOCK

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


#def households_disposable_income():
 #   return xr.DataArray(
  #      [[20000, 30000], [15000, 22000]],
   #     coords={
    #        "REGIONS_I": _subscript_dict["REGIONS_I"],
     #       "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
      #  },
       # dims=["REGIONS_I", "HOUSEHOLDS_I"]
   # )


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


def households_gross_savings(disposable_income_proj):
    return disposable_income_proj - total_households_consumption_coicop()


def households_net_lending():
    return households_gross_savings() - increase_in_households_capital_stock_due_to_investments()


def initial_households_financial_liabilities():
    return xr.DataArray(
        [[300, 500], [200, 400]],
        coords={
            "REGIONS_I": _subscript_dict["REGIONS_I"],
            "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"]
        },
        dims=["REGIONS_I", "HOUSEHOLDS_I"]
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
    return ratio_liabilities_to_disposable_income() * households_disposable_income(net_labor_income_proj, social_benefits_proj, income_tax_proj, property_income_paid, wealth_tax_proj) - current_liabilities


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


#DISPOSABLE_INCOME FILE

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



#END OF DISPOSABLE_INCOME FILE


def run_model(years):
    capitalstock_proj = households_capital_stock_over_time(years)

    # from DISPOSABLE INCOME

    gross_labour_income_proj = households_gross_labour_income_over_time(years)
    social_security_payments_proj = households_social_security_payments(gross_labour_income_proj)
    net_labor_income_proj = households_net_labour_income_over_time(gross_labour_income_proj,
                                                                   social_security_payments_proj)
    net_wealth_proj = households_net_labour_income_over_time(gross_labour_income_proj, social_security_payments_proj)
    social_benefits_proj = households_social_benefits(years)
    net_operating_surplus_proj = households_net_operating_surplus(years)
    taxable_income_proj = taxable_income_over_time(net_labor_income_proj, social_security_payments_proj,
                                                   net_operating_surplus_proj, property_income_received,
                                                   social_benefits_proj)
    delayed_taxable_income_proj = delayed_households_taxable_income_over_time(taxable_income_proj)
    income_tax_proj = households_income_tax()
    disposable_income_proj = households_disposable_income(net_labor_income_proj, social_benefits_proj, income_tax_proj,
                                                          property_income_paid,
                                                          wealth_tax_proj)
    gross_savings_proj = households_gross_savings(disposable_income_proj)

    # from FINANCE

    liabilities_proj = households_financial_liabilities_over_time(years)

    assets_proj = households_financial_assets_over_time(years, liabilities_proj)
    property_income_paid = compute_households_property_income_paid(years, liabilities_proj)
    property_income_received = households_property_income_received_over_time(years, assets_proj, capitalstock_proj)
    net_wealth_proj = households_net_wealth_over_time(years, liabilities_proj, assets_proj, capitalstock_proj)
    wealth_tax_proj = households_wealth_tax_over_time(net_wealth_proj)

    return gross_savings_proj

if __name__ == "__main__":
    years = list(range(2014, 2016))

    #from K_stock

    result = run_model(years)


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

    print(gross_savings_proj.sel(Year=2015))

