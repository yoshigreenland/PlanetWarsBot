import sys
import logging
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):

    #list of planets that already being attacked
    targeted_planets = {fleet.destination_planet for fleet in state.my_fleets()}
    #limits available targets to only those that are not already being attacked
    available_targets = [p for p in state.enemy_planets() if p.ID not in targeted_planets]
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(available_targets, key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):

    #list of planets that already being attacked
    targeted_planets = {fleet.destination_planet for fleet in state.my_fleets()}
    #limits available targets to only those that are not already being attacked
    available_targets = [p for p in state.neutral_planets() if p.ID not in targeted_planets]

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(available_targets, key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet or strongest_planet.num_ships/2 < weakest_planet.num_ships:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest neutral planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, weakest_planet.num_ships + 1)
