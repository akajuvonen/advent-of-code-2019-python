from advent_of_code_2019_python.day6 import calculate_orbits, populate_orbits, calculate_orbital_transfers


def test_calculate_orbits():
    orbit_list = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']
    univ_center_of_mass = populate_orbits(orbit_list)
    assert calculate_orbits(univ_center_of_mass) == 42


def test_orbital_transfers():
    orbit_list = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN']
    univ_center_of_mass = populate_orbits(orbit_list)
    orb_transfer_count = calculate_orbital_transfers('YOU', 'SAN', univ_center_of_mass)
    assert  orb_transfer_count == 4
