import xarray as xr
from pysd.py_backend.statefuls import (
    SampleIfTrue,
    Smooth,
    Delay,
    DelayFixed,
    Initial,
    Integ,
)

_subscript_dict = {
    "HOUSEHOLDS_I": ["LowINC", "HighINC"],
    "REGIONS_I": ["FR", "IT"],
}

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

if __name__ == "__main__":
    years = list(range(2014, 2016))
    proj = households_capital_stock_over_time(years)
    print(proj)
    print("\nStock in 2025:")
    print(proj.sel(Year=2015))


