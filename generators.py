from components.equippable import EquippableFactory
from item_factory import makeHealingPotion, makeFireballScroll, makeConfusionScroll, makeFireballBook, makeHealBook, makeLightningScroll, makePoisonPotion
from components.equippable import EquippableFactory

def item_generator2(item_choice, x, y):
	if item_choice == 'sword':
		item = EquippableFactory.make_sword(x, y)
	elif item_choice == 'shield':
		item = EquippableFactory.make_shield(x, y) 
	elif item_choice == 'armor':
		item = EquippableFactory.make_leather_armor(x, y)
	elif item_choice == 'greatsword':
		item = EquippableFactory.makeGreatSword(x, y)
	elif item_choice == 'dagger':
		item = EquippableFactory.make_dagger(x, y)
	elif item_choice == 'axe':
		item = EquippableFactory.makeAxe(x, y)
	elif item_choice == 'bow':
		item = EquippableFactory.make_bow(x, y)
	elif item_choice == 'arrows':
		item = EquippableFactory.make_arrows(x, y)
	elif item_choice == 'fireball_scroll':
		item = makeFireballScroll(x, y)
	elif item_choice == 'confusion_scroll':
		item = makeConfusionScroll(x, y)	
	elif item_choice == 'fireball_book':
		item_component = makeFireballBook(x, y)
	elif item_choice == 'heal_book':
		item_component = makeHealBook(x, y)
	elif item_choice == 'lightning_scroll':
		item = makeLightningScroll(x, y)
	elif item_choice == 'healing_potion':
		item = makeHealingPotion(x, y)
	elif item_choice == 'poison_potion':
		item = makePoisonPotion(x, y)
	return item

def item_generator(item_choice, x, y):
	item_lookup = {'healing_potion': makeHealingPotion, 'poison_potion': makePoisonPotion, 'sword': EquippableFactory.make_sword, 'shield': EquippableFactory.make_shield, 'armor': EquippableFactory.make_leather_armor, 'greatsword': EquippableFactory.make_greatsword, 'dagger': EquippableFactory.make_dagger,
				'axe': EquippableFactory.make_axe, 'bow': EquippableFactory.make_bow, 'arrows': EquippableFactory.make_arrows, 'fireball_scroll': makeFireballScroll, 'confusion_scroll': makeConfusionScroll, 'fireball_book': makeFireballBook, 'heal_book': makeHealBook,
				'lightning_scroll': makeLightningScroll}
	chosen_item = item_lookup[item_choice](x, y)
	return chosen_item