"""Spectral lines produced by DKIST instruments."""
import astropy.units as u

from dkist_spectral_lines.models import DiagnosticSpecies
from dkist_spectral_lines.models import SpectralLine


_SPECTRAL_LINES = sorted(
    [
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.CA_II_K,
            rest_wavelength_in_air=393.37 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.CA_II_H,
            rest_wavelength_in_air=396.85 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.H_EPSILON,
            rest_wavelength_in_air=397 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_I,
            rest_wavelength_in_air=404.58 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.H_DELTA,
            rest_wavelength_in_air=410.17 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.CA_I,
            rest_wavelength_in_air=422.67 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.H_GAMMA,
            rest_wavelength_in_air=434.05 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.TI_I,
            rest_wavelength_in_air=453.6 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.BA_II,
            rest_wavelength_in_air=455.4 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.SR_I,
            rest_wavelength_in_air=460.73 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.H_BETA,
            rest_wavelength_in_air=486.13 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.MG_I_B1,
            rest_wavelength_in_air=517.27 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.MG_I_B2,
            rest_wavelength_in_air=518.36 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_I,
            rest_wavelength_in_air=525.04 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_XIV,
            rest_wavelength_in_air=530.3 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.MN_I,
            rest_wavelength_in_air=553.78 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_I,
            rest_wavelength_in_air=557.6 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.HE_I,
            rest_wavelength_in_air=587.59 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.HE_I_D3,
            rest_wavelength_in_air=587.6 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.NA_I_D2,
            rest_wavelength_in_air=589 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.NA_I_D1,
            rest_wavelength_in_air=589.59 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_I,
            rest_wavelength_in_air=617.33 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_I,
            rest_wavelength_in_air=630.15 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_I,
            rest_wavelength_in_air=630.25 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.H_ALPHA,
            rest_wavelength_in_air=656.28 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.NI_I,
            rest_wavelength_in_air=676.78 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_I,
            rest_wavelength_in_air=709 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.CA_I,
            rest_wavelength_in_air=714.82 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_I,
            rest_wavelength_in_air=751.15 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.K_I,
            rest_wavelength_in_air=769.9 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_XI,
            rest_wavelength_in_air=789.2 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.NA_I,
            rest_wavelength_in_air=818.33 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.NA_I,
            rest_wavelength_in_air=819.48 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.CA_II,
            rest_wavelength_in_air=849.81 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.CA_II,
            rest_wavelength_in_air=854.21 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.CA_II,
            rest_wavelength_in_air=866.22 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.MN_I,
            rest_wavelength_in_air=874.1 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_XIII,
            rest_wavelength_in_air=1074.7 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_XIII,
            rest_wavelength_in_air=1079.8 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.HE_I,
            rest_wavelength_in_air=1083 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.SI_X,
            rest_wavelength_in_air=1430 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.FE_I,
            rest_wavelength_in_air=1565 * u.nm,
        ),
        SpectralLine(
            diagnostic_species=DiagnosticSpecies.SI_IX,
            rest_wavelength_in_air=3934 * u.nm,
        ),
    ]
)

SPECTRAL_LINES = tuple(_SPECTRAL_LINES)
