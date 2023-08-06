"""Tests for the line definitions"""
from collections import Counter

import pytest

from dkist_spectral_lines import get_spectral_lines
from dkist_spectral_lines.models import SpectralLine


@pytest.fixture()
def spectral_lines() -> tuple[SpectralLine]:
    """Import of spectral lines to capture validation errors in test setup vs collection"""
    from dkist_spectral_lines.lines import SPECTRAL_LINES

    return SPECTRAL_LINES


def test_lines_are_valid(spectral_lines):
    """
    :Given: Spectral line data structures
    :When: Instantiating the data structures
    :Then: Validation doesn't raise s pydantic.ValidationError
    """
    # Then
    assert spectral_lines


def test_lines_are_sortable(spectral_lines):
    """
    :Given: Spectral line data structures
    :When: Sorting them
    :Then: They get sorted by rest_wavelength_in_air
    """
    sorted_lines = list(sorted(spectral_lines))
    # Then
    for idx in range(1, len(sorted_lines)):
        assert (
            sorted_lines[idx - 1].rest_wavelength_in_air < sorted_lines[idx].rest_wavelength_in_air
        )


def test_lines_are_uniquely_named(spectral_lines):
    """
    :Given: Spectral line data structures
    :When: Inspecting name_id
    :Then: All name ids are unique
    """
    names = [line.name for line in spectral_lines]
    name_counts = Counter(names)
    assert not ({k: v for k, v in name_counts.items() if v > 1})
