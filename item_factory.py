from components.item import Item
from entity import Entity
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse
	
def makeHealingPotion():
	healing_component = Item(use_function=heal, amount=40)
	tempItem = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM, item=healing_component)
	return tempItem

def makeLightningScroll():
	lightning_scroll_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
	tempItem = Entity(x, y, '?', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM, item=lightning_scroll_component)
	return tempItem

def makeFireballScroll():
	fireball_scroll_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=25, radius=3)
	tempItem = Entity(x, y, '?', libtcod.red, 'Fireball scroll', render_order=RenderOrder.ITEM, item=fireball_scroll_component)
	return tempItem

def makeConfusionScroll():
	confusion_scroll_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message('Left-click on an enemy to confuse it or right-click to cancel.', libtcod.light_cyan))
	tempItem = Entity(x, y, '?', libtcod.light_pink, 'Confusion scroll', render_order=RenderOrder.ITEM, item=confusion_scroll_component)
	return tempItem

def makeFireballBook():
	fireball_book_component = Item(use_function=learn_fireball, spell="Fireball")
	tempItem = Entity(x, y, '#', libtcod.red, 'Fireball spellbook', render_order=RenderOrder.ITEM, item=fireball_book_component)
	return tempItem

def makeHealBook():
	heal_book_component = Item(use_function=learn_heal, spell="Heal")
	tempItem = Entity(x, y, '#', libtcod.red, 'Heal spellbook', render_order=RenderOrder.ITEM, item=heal_book_component)
	return tempItem
