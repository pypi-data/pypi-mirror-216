"""Tests for the search module"""
import astropy.units as u
import pytest

from dkist_spectral_lines import get_closest_spectral_line
from dkist_spectral_lines import get_spectral_lines
from dkist_spectral_lines.models import DiagnosticSpecies
from dkist_spectral_lines.models import SpectralLine


@pytest.fixture()
def fake_spectral_lines(
    mocker,
) -> dict[str, SpectralLine]:
    wavelength_min = 100.0 * u.nm
    wavelength_max = 1000.0 * u.nm
    wavelength_mean = (wavelength_max + wavelength_min) / 2
    min_line = SpectralLine(
        rest_wavelength_in_air=wavelength_min, diagnostic_species=DiagnosticSpecies.CA_I
    )
    max_line = SpectralLine(
        rest_wavelength_in_air=wavelength_max, diagnostic_species=DiagnosticSpecies.CA_II
    )
    mean_line = SpectralLine(
        rest_wavelength_in_air=wavelength_mean, diagnostic_species=DiagnosticSpecies.CA_II_H
    )
    fake_lines = (min_line, max_line, mean_line)
    mocker.patch("dkist_spectral_lines.search.SPECTRAL_LINES", new=fake_lines)
    return {
        "min_line": min_line,
        "max_line": max_line,
        "mean_line": mean_line,
    }


@pytest.mark.parametrize(
    "wavelength_min, wavelength_max, expected_spectral_line_hashes",
    [
        pytest.param(100.0, 600.0, ["min_line", "mean_line"], id="float_min"),
        pytest.param(100.0, 600.0, ["min_line", "mean_line"], id="float_min_edge"),
        pytest.param(500.0, 1001.0, ["max_line", "mean_line"], id="float_max"),
        pytest.param(500.0, 1000.0, ["max_line", "mean_line"], id="float_max_edge"),
        pytest.param(
            1.0,
            1001.0,
            ["max_line", "mean_line", "min_line"],
            id="float_all",
        ),
        pytest.param(
            1.0,
            2.0,
            [],
            id="float_none",
        ),
        pytest.param(200.0, 800.0, ["mean_line"], id="float_mean_only"),
        pytest.param(100.0 * u.nm, 600.0 * u.nm, ["min_line", "mean_line"], id="nm_min"),
        pytest.param(100.0 * u.nm, 600.0 * u.nm, ["min_line", "mean_line"], id="nm_min_edge"),
        pytest.param(500.0 * u.nm, 1001.0 * u.nm, ["max_line", "mean_line"], id="nm_max"),
        pytest.param(500.0 * u.nm, 1000.0 * u.nm, ["max_line", "mean_line"], id="nm_max_edge"),
        pytest.param(
            1.0 * u.nm,
            1001.0 * u.nm,
            ["max_line", "mean_line", "min_line"],
            id="nm_all",
        ),
        pytest.param(
            1.0 * u.nm,
            2.0 * u.nm,
            [],
            id="nm_none",
        ),
        pytest.param(200.0 * u.nm, 800.0 * u.nm, ["mean_line"], id="nm_mean_only"),
        pytest.param(
            100.0 * 10 * u.angstrom,
            600.0 * 10 * u.angstrom,
            ["min_line", "mean_line"],
            id="angstrom_min",
        ),
        pytest.param(
            100.0 * 10 * u.angstrom,
            600.0 * 10 * u.angstrom,
            ["min_line", "mean_line"],
            id="angstrom_min_edge",
        ),
        pytest.param(
            500.0 * 10 * u.angstrom,
            1001.0 * 10 * u.angstrom,
            ["max_line", "mean_line"],
            id="angstrom_max",
        ),
        pytest.param(
            500.0 * 10 * u.angstrom,
            1000.0 * 10 * u.angstrom,
            ["max_line", "mean_line"],
            id="angstrom_max_edge",
        ),
        pytest.param(
            1.0 * 10 * u.angstrom,
            1001.0 * 10 * u.angstrom,
            ["max_line", "mean_line", "min_line"],
            id="angstrom_all",
        ),
        pytest.param(
            1.0 * u.angstrom,
            2.0 * u.angstrom,
            [],
            id="angstrom_none",
        ),
        pytest.param(
            200.0 * 10 * u.angstrom, 800.0 * 10 * u.angstrom, ["mean_line"], id="angstrom_mean_only"
        ),
    ],
)
def test_get_spectral_lines(
    fake_spectral_lines: dict[str, SpectralLine],
    wavelength_min: float | u.Quantity,
    wavelength_max: float | u.Quantity,
    expected_spectral_line_hashes: list[str],
):
    """
    :Given: Spectral line data structures
    :When: searching by wavelength range
    :Then: expected wavelengths are returned
    """
    # When
    lines = get_spectral_lines(wavelength_min=wavelength_min, wavelength_max=wavelength_max)
    # Then
    expected_spectral_line_names: list[DiagnosticSpecies] = []
    for h in expected_spectral_line_hashes:
        expected_spectral_line_names.append(fake_spectral_lines[h].diagnostic_species)
    for expected in expected_spectral_line_names:
        assert expected in [l.diagnostic_species for l in lines]
    assert len(expected_spectral_line_names) == len(lines)


@pytest.mark.parametrize(
    "search_wavelength, expected_spectral_line_hash",
    [
        pytest.param(1.0, "min_line", id="float_less_than_list"),
        pytest.param(2000.0, "max_line", id="float_greater_than_list"),
        pytest.param(550.0, "mean_line", id="float_middle"),
        pytest.param(325.0, "min_line", id="float_equidistant"),
        pytest.param(1.0 * u.nm, "min_line", id="nm_less_than_list"),
        pytest.param(2000.0 * u.nm, "max_line", id="nm_greater_than_list"),
        pytest.param(550.0 * u.nm, "mean_line", id="nm_middle"),
        pytest.param(325.0 * u.nm, "min_line", id="nm_equidistant"),
        pytest.param(1.0 * 10 * u.angstrom, "min_line", id="angstrom_less_than_list"),
        pytest.param(2000.0 * 10 * u.angstrom, "max_line", id="angstrom_greater_than_list"),
        pytest.param(550.0 * 10 * u.angstrom, "mean_line", id="angstrom_middle"),
        pytest.param(325.0 * 10 * u.angstrom, "min_line", id="angstrom_equidistant"),
    ],
)
def test_get_closest_spectral_line(
    fake_spectral_lines: dict[str, SpectralLine],
    search_wavelength: float,
    expected_spectral_line_hash: str,
):
    """
    :Given: Spectral line data structures
    :When: searching for closest value to a wavelength
    :Then: expected line is returned
    """
    # When
    line = get_closest_spectral_line(wavelength=search_wavelength)
    # Then
    assert line == fake_spectral_lines[expected_spectral_line_hash]
