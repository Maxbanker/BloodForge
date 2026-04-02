"""
BloodForge Basic Fight Demo
Simple command-line example
"""

from bloodforge.sim import BloodForgeSim

# Example fighters
fighter_a = {
    "name": "Prison Yard Bully",
    "init_state": {"panic": 0.35, "omega": 0.78}
}

fighter_b = {
    "name": "Cornered Inmate",
    "init_state": {"panic": 0.45, "omega": 0.68}
}

# Run simulation with SPSM enabled
sim = BloodForgeSim(
    fighter_a_config=fighter_a,
    fighter_b_config=fighter_b,
    spsm_mode=True,      # Change to False for base mode
    seed=42
)

result = sim.run_fight()

print("\n=== BloodForge Fight Result ===")
print(f"Winner: {result.winner}")
print(f"Method: {result.method}")
print(f"Total Exchanges: {result.exchanges}")
print(f"Final Round: {result.round}")

print("\nFinal States:")
print(f"{fighter_a['name']}: Ω={result.final_state_a['omega']:.3f}, Γ={result.final_state_a['gamma']:.3f}, Veil={result.final_state_a['veil']:.3f}")
print(f"{fighter_b['name']}: Ω={result.final_state_b['omega']:.3f}, Γ={result.final_state_b['gamma']:.3f}, Veil={result.final_state_b['veil']:.3f}")

print(f"\nFull log saved to: bloodforge_{fighter_a['name'].replace(' ', '_')}_vs_{fighter_b['name'].replace(' ', '_')}.csv")