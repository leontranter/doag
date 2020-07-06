from entity import Entity
from components.identified import Identified
from item_factory import make_healing_potion
from loader_functions.constants import get_basic_damage, WeaponTypes, get_constants
from systems.name_system import get_display_name2
from loader_functions.initialize_new_game import get_game_variables, assign_potion_descriptions
import tcod as libtcod

constants = get_constants()
potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
test_identified_component = Identified(potion_description_links)
print(test_identified_component.identified_potions)
print(test_identified_component.potion_links)
test_potion = make_healing_potion()
print(test_identified_component.potion_links[test_potion.name.true_name])
test_player = Entity(1, 1, 'A', libtcod.white, identified=test_identified_component)

print(get_display_name2(test_player, test_potion))
