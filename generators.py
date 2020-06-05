from components.equippable import EquippableFactory
from item_factory import makeHealingPotion, makeFireballScroll, makeConfusionScroll, makeFireballBook, makeHealBook, makeLightningScroll
from components.equippable import EquippableFactory

def item_generator(item_choice, x, y):
	if item_choice == 'healing_potion':
		item = makeHealingPotion()
	elif item_choice == 'sword':
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
		item = makeFireballScroll()
	elif item_choice == 'confusion_scroll':
		item = makeConfusionScroll()	
	elif item_choice == 'fireball_book':
		item_component = makeFireballBook()
	elif item_choice == 'heal_book':
		item_component = makeHealBook()
	elif item_choice == 'lightning_scroll':
		item = makeLightningScroll()
	return item

#def item_generator(item_choice):
#	item_lookup = {'healing_potion': makeHealingPotion, 'sword': makeBroadSword, 'shield': makeShield, 'armor': makeLeatherArmor, 'greatsword': makeGreatSword, 'dagger': makeDagger,
#				'axe': makeAxe, 'bow': makeBow, 'arrows': makeArrows, 'fireball_scroll': makeFireballScroll, 'confusion_scroll': makeConfusionScroll, 'fireball_book': makeFireballBook, 'heal_book': makeHealBook,
#				'lightning_scroll': makeLightningScroll}
#	chosen_item = item_lookup[item_choice]()
#	return chosen_item