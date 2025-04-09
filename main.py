import numpy as np
from dataclasses import dataclass
from typing import List

@dataclass
class Propellant:
    name: str
    isp: float  # specific impulse in seconds
    density: float # fuel density in kg/m^3

# Common propellant combinations
PROPELLANTS = {
    'RP-1/LOX': Propellant('RP-1/LOX', 263, 806),  # First stage typical
    'LH2/LOX': Propellant('LH2/LOX', 421, 71),      # Upper stages typical
    'N2O4/UDMH': Propellant('N2O4/UDMH', 320, 793),  # Hypergolic
    'Solid': Propellant('Solid', 280, 1500),         # Solid rocket motor
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
    
    @property
    def propellant_volume(self) -> float:
        # Volume in cubic meters
        return self.propellant_mass / self.propellant.density


class Rocket:
    def __init__(self, stages: List[Stage]):
        self.stages = stages

    def total_delta_v(self) -> float:
        return sum(stage.delta_v() for stage in self.stages)

    def __str__(self):
        result = f"highest delta v: {self.total_delta_v()}. \nrocket stages: "
        for stage in self.stages:
            result += stage.__str__() + "\n"
        return result

def calculate_stage_permutations(stages):
    stage_combinations = []
    MAX_VOLUMES = [2500, 1000, 300]  # example constraint per stage (m³)

    for prop1 in PROPELLANTS.values():
        for prop2 in PROPELLANTS.values():
            for prop3 in PROPELLANTS.values():
                new_stages = [
                    Stage(prop1, stages[0].dry_mass, stages[0].propellant_mass, stages[0].payload_mass),
                    Stage(prop2, stages[1].dry_mass, stages[1].propellant_mass, stages[1].payload_mass),
                    Stage(prop3, stages[2].dry_mass, stages[2].propellant_mass, stages[2].payload_mass),
                ]
                # Check volume constraint
                if all(s.propellant_volume <= MAX_VOLUMES[i] for i, s in enumerate(new_stages)):
                    stage_combinations.append(new_stages)
    return stage_combinations

def main():
    # drymass, propellant mass, payload mass
    original_saturn_v_stages = [
        Stage(PROPELLANTS['RP-1/LOX'], 137000, 2214000 - 137000, 0),  # S-IC stage
        Stage(PROPELLANTS['LH2/LOX'], 40100, 496200 - 40100, 0),  # S-II stage
        Stage(PROPELLANTS['LH2/LOX'], 15200, 123000 - 15200, 0),  # S-IVB stage
    ]

    permutations = calculate_stage_permutations(original_saturn_v_stages)
    highest_delta_v = -1
    best_rocket = Rocket(original_saturn_v_stages)
    for permutation in permutations:
        rocket = Rocket(permutation)
        deltaV = rocket.total_delta_v()
        if deltaV > highest_delta_v:
            highest_delta_v = deltaV
            best_rocket = rocket
    print(best_rocket)

    saturn_v_rocket = Rocket(original_saturn_v_stages)
    alternate_saturn_v_stages = [
        Stage(PROPELLANTS['RP-1/LOX'], 137000, 2214000 - 137000, 0),  # S-IC stage
        Stage(PROPELLANTS['LH2/LOX'], 40100, 496200 - 40100, 0),  # S-II stage
        Stage(PROPELLANTS['LH2/LOX'], 15200, 123000 - 15200, 0),  # S-IVB stage
    ]
    print(f"\nSaturn V-like configuration total Δv: {saturn_v_rocket.total_delta_v():.1f} m/s")


if __name__ == "__main__":
    main() 
