"""Spectral Line and Filter data structures."""
from enum import StrEnum
from enum import unique

import astropy.units as u
from pydantic import BaseModel
from pydantic import validator


@unique
class DiagnosticSpecies(StrEnum):
    """Controlled list of values for the prefix of a spectral line.  Diagnostic species values should NOT be changed after they have been released lest they produce duplicates in the set of processed dkist data."""

    H_GAMMA = "H gamma"
    H_DELTA = "H delta"
    FE_I = "Fe I"
    TI_I = "Ti I"
    FE_XIII = "Fe XIII"
    NI_I = "Ni I"
    CA_II_H = "Ca II H"
    H_BETA = "H beta"
    CA_II = "Ca II"
    K_I = "K I"
    CA_I = "Ca I"
    SR_I = "Sr I"
    HE_I_D3 = "He I D3"
    H_EPSILON = "H epsilon"
    SI_X = "Si X"
    MG_I_B2 = "Mg I b2"
    HE_I = "He I"
    MN_I = "Mn I"
    BA_II = "Ba II"
    NA_I_D2 = "Na I D2"
    FE_XIV = "Fe XIV"
    NA_I_D1 = "Na I D1"
    SI_IX = "Si IX"
    FE_XI = "Fe XI"
    H_ALPHA = "H alpha"
    CA_II_K = "Ca II K"
    NA_I = "Na I"
    MG_I_B1 = "Mg I b1"


class SpectralLine(BaseModel):
    """Spectral line data model."""

    diagnostic_species: DiagnosticSpecies
    rest_wavelength_in_air: u.Quantity

    @validator("rest_wavelength_in_air")
    def convert_to_nanometers(cls, v):
        """Validate wavelength unit is for distance and convert to nanometers."""
        return v.to(u.nm)

    class Config:
        """pydantic.BaseModel configuration."""

        arbitrary_types_allowed = True

    @property
    def name(self) -> str:
        """Return the name in a display friendly format."""
        return f"{self.diagnostic_species} ({self.rest_wavelength_in_air.value} {self.rest_wavelength_in_air.unit})"

    def __lt__(self, other):
        """Support sorting lines based on wavelength."""
        return self.rest_wavelength_in_air < other.rest_wavelength_in_air

    def __str__(self):
        """Represent the model as a string."""
        return self.name
