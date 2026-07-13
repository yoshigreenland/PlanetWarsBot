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
    

def attack_ideal_enemy_planet(state):

    #list of planets that already being attacked
    targeted_planets = {fleet.destination_planet for fleet in state.my_fleets()}
    #limits available targets to only those that are not already being attacked
    available_targets = [p for p in state.enemy_planets() if p.ID not in targeted_planets]
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the ideal enemy planet.
    ideal_planet = None
    ideal_planet_score = -1
    
    for planet in available_targets:
        dist = state.distance(strongest_planet.ID,planet.ID)
        ships_to_take = 1 + planet.num_ships + (planet.growth_rate * dist)
        if ships_to_take > (strongest_planet.num_ships/2):
            continue
        else:
            planet_score = planet.growth_rate / ships_to_take
        
        if planet_score > ideal_planet_score:
            ideal_planet_score = planet_score
            ideal_planet = planet

    if not strongest_planet or not ideal_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the ideal enemy planet.
        return issue_order(state, strongest_planet.ID, ideal_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):

    #list of planets that already being attacked
    targeted_planets = {fleet.destination_planet for fleet in state.my_fleets()}
    #limits available targets to only those that are not already being attacked
    available_targets = [p for p in state.neutral_planets() if p.ID not in targeted_planets]

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    ideal_target = max(available_targets, key=lambda p: p.growth_rate / (max(p.num_ships, 1) * max(state.distance(strongest_planet.ID, p.ID), 1)), default=None)

    if not strongest_planet or not ideal_target or strongest_planet.num_ships/2 < ideal_target.num_ships:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest neutral planet.
        return issue_order(state, strongest_planet.ID, ideal_target.ID, ideal_target.num_ships + 1)
