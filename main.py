import numpy as np
from dataclasses import dataclass
from typing import List

@dataclass
class Propellant:
    name: str
    isp: float  # specific impulse in seconds
    density: float  # kg/m³

# Common propellant combinations
PROPELLANTS = {
    'RP-1/LOX': Propellant('RP-1/LOX', 311, 1000),  # First stage typical
    'LH2/LOX': Propellant('LH2/LOX', 450, 70),      # Upper stages typical
    'N2O4/UDMH': Propellant('N2O4/UDMH', 320, 1200),  # Hypergolic
    'Solid': Propellant('Solid', 280, 1800),         # Solid rocket motor
}

@dataclass
class Stage:
    propellant: Propellant
    dry_mass: float  # kg
    propellant_mass: float  # kg
    payload_mass: float  # kg

    @property
    def total_mass(self) -> float:
        return self.dry_mass + self.propellant_mass + self.payload_mass

    @property
    def mass_ratio(self) -> float:
        return self.total_mass / (self.dry_mass + self.payload_mass)

    def delta_v(self) -> float:
        g0 = 9.81  # standard gravity in m/s²
        return g0 * self.propellant.isp * np.log(self.mass_ratio)

class Rocket:
    def __init__(self, stages: List[Stage]):
        self.stages = stages

    def total_delta_v(self) -> float:
        return sum(stage.delta_v() for stage in self.stages)

def create_saturn_v_like_rocket():
    # Approximate Saturn V masses
    stages = [
        Stage(PROPELLANTS['RP-1/LOX'], 130000, 2000000, 0),  # S-IC stage
        Stage(PROPELLANTS['LH2/LOX'], 40000, 450000, 0),     # S-II stage
        Stage(PROPELLANTS['LH2/LOX'], 12000, 100000, 0),     # S-IVB stage
    ]
    return Rocket(stages)

def analyze_propellant_combinations():
    print("Analyzing different propellant combinations for a 3-stage rocket:")
    print("\nStage 1 (First Stage) Options:")
    for name, prop in PROPELLANTS.items():
        stage = Stage(prop, 130000, 2000000, 0)
        print(f"{name}: Δv = {stage.delta_v():.1f} m/s")

    print("\nStage 2 (Second Stage) Options:")
    for name, prop in PROPELLANTS.items():
        stage = Stage(prop, 40000, 450000, 0)
        print(f"{name}: Δv = {stage.delta_v():.1f} m/s")

    print("\nStage 3 (Third Stage) Options:")
    for name, prop in PROPELLANTS.items():
        stage = Stage(prop, 12000, 100000, 0)
        print(f"{name}: Δv = {stage.delta_v():.1f} m/s")

def main():
    # Create and analyze Saturn V-like rocket
    rocket = create_saturn_v_like_rocket()
    print(f"\nSaturn V-like configuration total Δv: {rocket.total_delta_v():.1f} m/s")
    
    # Analyze different propellant combinations
    analyze_propellant_combinations()

    print("\nRecommendations:")
    print("1. First Stage: RP-1/LOX is recommended due to:")
    print("   - High thrust-to-weight ratio")
    print("   - Good density (compact tanks)")
    print("   - Proven reliability")
    
    print("\n2. Second Stage: LH2/LOX is recommended due to:")
    print("   - High specific impulse")
    print("   - Good performance in vacuum")
    print("   - Efficient for orbital insertion")
    
    print("\n3. Third Stage: LH2/LOX is recommended due to:")
    print("   - Highest specific impulse")
    print("   - Excellent for final orbital maneuvers")
    print("   - Efficient for deep space missions")

if __name__ == "__main__":
    main() 
