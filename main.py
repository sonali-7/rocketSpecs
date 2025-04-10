import numpy as np
from dataclasses import dataclass
from typing import List


@dataclass
class Propellant:
    name: str
    isp: float  # specific impulse in seconds
    density: float  # fuel density in kg/m^3


# Common propellants
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


def find_all_stage_combinations(stages) -> List[List[Stage]]:
    stage_combinations = []
    # MAX_VOLUMES = [2500, 1000, 300]  # example constraint per stage (m³)

    combinations = generate_combinations(PROPELLANTS.values(), len(stages))
    for combination in combinations:
        new_stages = []
        for i in range(len(stages)):
            stage = Stage(combination[i], stages[i].dry_mass, stages[i].propellant_mass, stages[i].payload_mass)
            new_stages.append(stage)
        # if all(s.propellant_volume <= MAX_VOLUMES[i] for i, s in enumerate(new_stages)):
        stage_combinations.append(new_stages)

    return stage_combinations


def generate_combinations(possible_options, n) -> List[List[any]]:
    """
    :param possible_options: a list of options to  pull from
    :param n: how long each list should be
    :return: A list of lists, of all possible ordered combinations, drawn from possible_options, for a list length n
    """
    result = []

    def recursive_generate_combinations(current_combo, depth):
        if depth == n:
            result.append(current_combo)
            return
        for prop in possible_options:
            recursive_generate_combinations(current_combo + [prop], depth + 1)
    recursive_generate_combinations([], 0)
    return result


def find_best_rocket(combinations: List[List[Stage]]) -> Rocket:
    highest_delta_v = -1
    best_rocket = Rocket(combinations[0])
    for combination in combinations:
        rocket = Rocket(combination)
        delta_v = rocket.total_delta_v()
        if delta_v > highest_delta_v:
            highest_delta_v = delta_v
            best_rocket = rocket
    return best_rocket


def main():
    # drymass, propellant mass, payload mass
    original_saturn_v_stages = [
        Stage(PROPELLANTS['RP-1/LOX'], 137000, 2214000 - 137000, 0),  # S-IC stage
        Stage(PROPELLANTS['LH2/LOX'], 40100, 496200 - 40100, 0),  # S-II stage
        Stage(PROPELLANTS['LH2/LOX'], 15200, 123000 - 15200, 0),  # S-IVB stage
    ]

    print(f"Originally, saturn v has a total Δv of {Rocket(original_saturn_v_stages).total_delta_v()}")
    combinations = find_all_stage_combinations(original_saturn_v_stages)
    best_rocket = find_best_rocket(combinations)
    print(f"Using different fuel combinations in the saturn v rocket, the best combinations can have a Δv{best_rocket.total_delta_v()}")


if __name__ == "__main__":
    main()
