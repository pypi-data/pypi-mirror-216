"""Tests for the SpectralLine data structure and validation"""
import random

import astropy.units as u
import pytest
from astropy.units import Unit
from pydantic import ValidationError

from dkist_spectral_lines.lines import DiagnosticSpecies
from dkist_spectral_lines.models import SpectralLine


@pytest.mark.parametrize("unit", [u.nm, u.angstrom])
@pytest.mark.parametrize("diagnostic_species", [l for l in DiagnosticSpecies])
def test_spectral_line_valid(diagnostic_species, unit):
    """
    :Given: Diagnostic species and wavelength
    :When: Instantiating a SpectralLine
    :Then: Instance created and name property renders
    """
    # Given
    wavelength = random.random() * 100 * unit
    # When
    spectral_line = SpectralLine(
        diagnostic_species=diagnostic_species, rest_wavelength_in_air=wavelength
    )
    # Then
    assert spectral_line.name
    assert spectral_line.rest_wavelength_in_air.unit == Unit("nm")
    assert str(spectral_line) == spectral_line.name


@pytest.mark.parametrize(
    "diagnostic_species, wavelength",
    [
        pytest.param("bad line", 1.1 * u.nm, id="diagnostic_species"),
        pytest.param(DiagnosticSpecies.CA_I, "a", id="wavelength"),
        pytest.param(DiagnosticSpecies.CA_I, 1.1, id="wavelength_no_units"),
        pytest.param("bad line", "a", id="diagnostic_species_and_wavelength"),
        pytest.param(None, 1.1 * u.nm, id="diagnostic_species_required"),
        pytest.param(DiagnosticSpecies.CA_I, None, id="wavelength_required"),
        pytest.param(DiagnosticSpecies.CA_I, 1.1 * u.s, id="wavelength_wrong_units"),
    ],
)
def test_spectral_line_invalid(diagnostic_species, wavelength):
    """
    :Given: Invalid diagnostic species and/or wavelength
    :When: Instantiating a SpectralLine
    :Then: Pydantic Validation error raised
    """
    with pytest.raises(ValidationError):
        SpectralLine(diagnostic_species=diagnostic_species, rest_wavelength_in_air=wavelength)
