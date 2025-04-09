import numpy as np
from dataclasses import dataclass
from typing import List

@dataclass
class Propellant:
    name: str
    isp: float  # specific impulse in seconds

# Common propellant combinations
PROPELLANTS = {
    'RP-1/LOX': Propellant('RP-1/LOX', 263),  # First stage typical
    'LH2/LOX': Propellant('LH2/LOX', 421),      # Upper stages typical
    'N2O4/UDMH': Propellant('N2O4/UDMH', 320),  # Hypergolic
    'Solid': Propellant('Solid', 280),         # Solid rocket motor
}

@dataclass
class Stage:
    propellant: Propellant
    dry_mass: float  # kg
    propellant_mass: float  # kg
    payload_mass: float  # kg
    g0 = 9.81 # standard gravity in m/s²

    @property
    def total_mass(self) -> float:
        return self.dry_mass + self.propellant_mass + self.payload_mass

    @property
    def mass_ratio(self) -> float:
        return self.total_mass / (self.dry_mass + self.payload_mass)

    def delta_v(self) -> float:
        return self.g0 * self.propellant.isp * np.log(self.mass_ratio)

    def thrust(self) -> float:
        return np.gradient(self.g0*self.propellant.isp)

class Rocket:
    def __init__(self, stages: List[Stage]):
        self.stages = stages

    def total_delta_v(self) -> float:
        return sum(stage.delta_v() for stage in self.stages)

def calculate_stage_permutations(stages):
    



def main():
    # drymass, propellant mass, payload mass
    original_saturn_v_stages = [
        Stage(PROPELLANTS['RP-1/LOX'], 137000, 2214000 - 137000, 0),  # S-IC stage
        Stage(PROPELLANTS['LH2/LOX'], 40100, 496200 - 40100, 0),  # S-II stage
        Stage(PROPELLANTS['LH2/LOX'], 15200, 123000 - 15200, 0),  # S-IVB stage
    ]



    saturn_v_rocket = Rocket(original_saturn_v_stages)
    alternate_saturn_v_stages = [
        Stage(PROPELLANTS['RP-1/LOX'], 137000, 2214000 - 137000, 0),  # S-IC stage
        Stage(PROPELLANTS['LH2/LOX'], 40100, 496200 - 40100, 0),  # S-II stage
        Stage(PROPELLANTS['LH2/LOX'], 15200, 123000 - 15200, 0),  # S-IVB stage
    ]



    print(f"\nSaturn V-like configuration total Δv: {saturn_v_rocket.total_delta_v():.1f} m/s")



if __name__ == "__main__":
    main() 
