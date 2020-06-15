from components.equippable import EquippableFactory
from item_factory import make_healing_potion, make_fireball_scroll, make_confusion_scroll, make_fireball_book, make_heal_book, make_lightning_scroll, make_poison_potion
from components.equippable import EquippableFactory


def item_generator(item_choice, x, y):
	item_lookup = {'healing_potion': make_healing_potion, 'poison_potion': make_poison_potion, 'sword': EquippableFactory.make_sword, 'shield': EquippableFactory.make_shield, 'armor': EquippableFactory.make_leather_armor, 'greatsword': EquippableFactory.make_greatsword, 'dagger': EquippableFactory.make_dagger,
				'axe': EquippableFactory.make_axe, 'bow': EquippableFactory.make_bow, 'arrows': EquippableFactory.make_arrows, 'fireball_scroll': make_fireball_scroll, 'confusion_scroll': make_confusion_scroll, 'fireball_book': make_fireball_book, 'heal_book': make_heal_book,
				'lightning_scroll': make_lightning_scroll}
	chosen_item = item_lookup[item_choice](x, y)
	return chosen_item