import pandas as pd
import os
import json
from tests.utils import fixtures_path, round_df_column

from hestia_earth.distribution.cycle import (
    INDEX_COLUMN, PESTICIDE_COLUMN, IRRIGATION_COLUMN,
    cycle_yield_distribution, group_cycle_inputs, get_input_group
)

fixtures_folder = os.path.join(fixtures_path, 'cycle_yield')


def test_cycle_yield_distribution():
    with open(f"{fixtures_folder}/cycles.jsonld", encoding='utf-8') as f:
        cycles = json.load(f)

    expected = pd.read_csv(os.path.join(fixtures_folder, 'distribution.csv'), index_col=INDEX_COLUMN)
    result = cycle_yield_distribution(cycles)
    round_df_column(result, 'Grain yield (kg/ha)')
    round_df_column(result, 'Nitrogen (kg N)')
    assert result.to_csv() == expected.to_csv()


def test_group_cycle_inputs():
    with open(f"{fixtures_folder}/cycles.jsonld", encoding='utf-8') as f:
        cycles = json.load(f)
    results = group_cycle_inputs(cycles[0])
    assert results.get('Nitrogen (kg N)') == 192


def test_get_input_group():
    assert get_input_group({'term': {'termType': 'organicFertiliser', 'units': 'kg N'}}) == 'Nitrogen (kg N)'
    assert get_input_group({'term': {'termType': 'organicFertiliser', 'units': 'kg K2O'}}) == 'Potassium (kg K2O)'
    assert get_input_group({'term': {'termType': 'organicFertiliser', 'units': 'kg CaCO3'}}) is None
    assert get_input_group({'term': {'termType': 'pesticideAI', 'units': 'kg active ingredient'}}) == PESTICIDE_COLUMN
    assert get_input_group({'term': {'termType': 'water', 'units': 'm3'}}) == IRRIGATION_COLUMN
