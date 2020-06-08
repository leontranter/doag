from components.equippable import EquippableFactory
from item_factory import makeHealingPotion, makeFireballScroll, makeConfusionScroll, makeFireballBook, makeHealBook, makeLightningScroll, makePoisonPotion
from components.equippable import EquippableFactory

def item_generator2(item_choice, x, y):
	if item_choice == 'sword':
		item = EquippableFactory.makeBroadSword(x, y)
	elif item_choice == 'shield':
		item = EquippableFactory.makeShield(x, y) 
	elif item_choice == 'armor':
		item = EquippableFactory.makeLeatherArmor(x, y)
	elif item_choice == 'greatsword':
		item = EquippableFactory.makeGreatSword(x, y)
	elif item_choice == 'dagger':
		item = EquippableFactory.makeDagger(x, y)
	elif item_choice == 'axe':
		item = EquippableFactory.makeAxe(x, y)
	elif item_choice == 'bow':
		item = EquippableFactory.makeBow(x, y)
	elif item_choice == 'arrows':
		item = EquippableFactory.makeArrows(x, y)
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
	item_lookup = {'healing_potion': makeHealingPotion, 'poison_potion': makePoisonPotion, 'sword': EquippableFactory.makeBroadSword, 'shield': EquippableFactory.makeShield, 'armor': EquippableFactory.makeLeatherArmor, 'greatsword': EquippableFactory.makeGreatSword, 'dagger': EquippableFactory.makeDagger,
				'axe': EquippableFactory.makeAxe, 'bow': EquippableFactory.makeBow, 'arrows': EquippableFactory.makeArrows, 'fireball_scroll': makeFireballScroll, 'confusion_scroll': makeConfusionScroll, 'fireball_book': makeFireballBook, 'heal_book': makeHealBook,
				'lightning_scroll': makeLightningScroll}
	chosen_item = item_lookup[item_choice](x, y)
	return chosen_item