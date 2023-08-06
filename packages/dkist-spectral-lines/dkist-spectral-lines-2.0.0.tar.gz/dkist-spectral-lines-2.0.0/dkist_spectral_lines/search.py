"""Search for spectral lines."""
from warnings import warn

import astropy.units as u

from dkist_spectral_lines.lines import SPECTRAL_LINES
from dkist_spectral_lines.models import SpectralLine


def _to_nanometers(wavelength: float | u.Quantity) -> u.Quantity:
    if not isinstance(wavelength, u.Quantity):
        warn(
            f"The wavelength provided does not indicate a unit. "
            f"Nanometers (nm) is being assumed. "
            f"To pass in a unit use an astropy.units.Quantity.",
            category=UserWarning,
        )
        return wavelength * u.nm
    return wavelength.to(u.nm)


def get_spectral_lines(
    wavelength_min: float | u.Quantity, wavelength_max: float | u.Quantity
) -> list[SpectralLine]:
    """Get all spectral lines found in the wavelength range inclusive of the extremes.  Wavelengths are assumed to be in nm unless specified otherwise as a astropy.units.Quantity."""
    wavelength_min = _to_nanometers(wavelength_min)
    wavelength_max = _to_nanometers(wavelength_max)

    result = [
        line
        for line in SPECTRAL_LINES
        if wavelength_min <= line.rest_wavelength_in_air <= wavelength_max
    ]
    return result


def get_closest_spectral_line(wavelength: float | u.Quantity) -> SpectralLine:
    """Get the spectral line that is closest to reference wavelength."""
    wavelength = _to_nanometers(wavelength)
    return min(SPECTRAL_LINES, key=lambda x: abs(x.rest_wavelength_in_air - wavelength))
