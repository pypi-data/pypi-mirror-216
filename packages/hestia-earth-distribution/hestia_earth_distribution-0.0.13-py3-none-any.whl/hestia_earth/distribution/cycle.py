from functools import reduce
import pandas as pd
import numpy as np
from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import find_primary_product, filter_list_term_type
from hestia_earth.utils.tools import list_sum, list_average, flatten
from hestia_earth.utils.api import download_hestia
from .utils.cycle import INDEX_COLUMN, YIELD_COLUMN, FERTILISER_COLUMNS, PESTICIDE_COLUMN, IRRIGATION_COLUMN


FERTILISER_TERM_TYPES = [
    TermTermType.ORGANICFERTILISER,
    TermTermType.INORGANICFERTILISER
]

TYPE_TO_COLUMN = {
    TermTermType.PESTICIDEAI.value: PESTICIDE_COLUMN,
    TermTermType.PESTICIDEBRANDNAME.value: PESTICIDE_COLUMN,
    TermTermType.WATER.value: IRRIGATION_COLUMN
}


def _nansum(val1: float, val2: float):
    return np.nan if all([np.isnan(val1), np.isnan(val2)]) else np.nansum([val1, val2])


def _get_fert_group(input: dict):
    term_units = input.get('term', {}).get('units')
    return next((group for group in FERTILISER_COLUMNS if term_units in group), None)


def get_input_group(input: dict):
    term_type = input.get('term', {}).get('termType')
    return _get_fert_group(input) if 'Fertiliser' in term_type else TYPE_TO_COLUMN[term_type]


def group_inputs(inputs: list, convert_nan_to_zero: bool = False):
    def exec(group: dict, group_key: str):
        sum_inputs = list_sum(flatten([
            input.get('value', []) for input in inputs if get_input_group(input) == group_key
        ]), np.nan)
        sum_inputs = 0 if np.isnan(sum_inputs) and convert_nan_to_zero else sum_inputs
        return {**group, group_key: sum_inputs}
    return exec


def _sum_input_values(inputs: list, percentages: list = []):
    vals = flatten([input.get('value', []) for input in inputs])
    return list_sum(vals, np.nan) if not percentages else np.dot(vals, percentages)


def sum_fertilisers(cycle: dict):
    fertilisers = [
        i for i in filter_list_term_type(cycle.get('inputs', []), FERTILISER_TERM_TYPES) if all([
            list_sum(i.get('value', []), 0) > 0
        ])
    ]
    convert_nan_to_zero = cycle.get('completeness', {}).get('fertiliser', False)
    values = reduce(group_inputs(fertilisers, convert_nan_to_zero), FERTILISER_COLUMNS, {})
    return values


def _pct_activate_ingredients(brand_name: str):
    name = download_hestia(brand_name, 'Term')
    return list_sum([i.get('value') for i in name.get('defaultProperties', [])
                     if i.get('term', {}).get('@id') == 'activeIngredient'], np.nan)


def _pesticideBrandNames_per_cycle(cycle: dict):
    return [
            i for i in cycle.get('inputs', []) if all([
                i.get('term', {}).get('termType') == TermTermType.PESTICIDEBRANDNAME.value,
                list_sum(i.get('value', []), np.nan) >= 0  # default nan, instead of zero 0
            ])
    ]


def _pesticideBrandName_IDs_per_cycle(cycle: dict):
    brandnames = _pesticideBrandNames_per_cycle(cycle)
    return [i.get('term', {}).get('@id') for i in brandnames]


def _get_totalAI_of_brandnames(cycles: list):
    pestBrandNames = list(set(flatten([_pesticideBrandName_IDs_per_cycle(c) for c in cycles])))
    pct_ai = [_pct_activate_ingredients(brand) for brand in pestBrandNames]
    return {pestBrandNames[i]: pct_ai[i] for i in range(len(pestBrandNames))}


def sum_pesticides(cycle: dict, brandname_to_ai: dict = {}):
    pestAIs = [
        i for i in filter_list_term_type(cycle.get('inputs', []), TermTermType.PESTICIDEAI) if all([
            list_sum(i.get('value', []), np.nan) >= 0
        ])
    ]
    pestBrandNames = _pesticideBrandNames_per_cycle(cycle)
    brandname_to_ai = brandname_to_ai or _get_totalAI_of_brandnames([cycle])
    pestAI_percentages = [brandname_to_ai.get(brand_name.get('term', {}).get('@id')) for brand_name in pestBrandNames]
    value = _nansum(_sum_input_values(pestAIs), _sum_input_values(pestBrandNames, pestAI_percentages))
    return 0 if np.isnan(value) and cycle.get('completeness', {}).get('pesticidesAntibiotics', False) else value


def sum_water(cycle: dict):
    waters = [
        i for i in cycle.get('inputs', []) if all([
            i.get('term', {}).get('termType') == TermTermType.WATER.value,
            list_sum(i.get('value', []), 0) > 0
        ])
    ]
    value = _sum_input_values(waters)
    return 0 if np.isnan(value) and cycle.get('completeness', {}).get('water', False) else value


def group_cycle_inputs(cycle: dict, brandname_to_ai: dict = {}):
    fertilisers_values = sum_fertilisers(cycle)
    pesticides_value = sum_pesticides(cycle, brandname_to_ai)
    water_values = sum_water(cycle)

    return {
        INDEX_COLUMN: cycle.get('@id'),
        YIELD_COLUMN: list_average((find_primary_product(cycle) or {}).get('value', []), np.nan),
        'completeness.products': cycle.get('completeness', {}).get('products', False),
        **fertilisers_values,
        'completeness.fertiliser': cycle.get('completeness', {}).get('fertiliser', False),
        PESTICIDE_COLUMN: pesticides_value,
        'completeness.pesticidesAntibiotics': cycle.get('completeness', {}).get('pesticidesAntibiotics', False),
        IRRIGATION_COLUMN: water_values,
        'completeness.water': cycle.get('completeness', {}).get('water', False)
    }


def cycle_yield_distribution(cycles: list):
    dict_brandname_to_ai = _get_totalAI_of_brandnames(cycles)

    values = list(map(lambda c: group_cycle_inputs(c, dict_brandname_to_ai), cycles))
    # in case there are no values, we should still set the columns
    columns = group_cycle_inputs({}).keys()
    return pd.DataFrame.from_records(values, index=[INDEX_COLUMN], columns=columns)
