from components.item import Item
from entity import Entity
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse
import tcod as libtcod
from render_functions import RenderOrder
from game_messages import Message
from components.name import Name

def make_healing_potion(x=1, y=1):
	healing_component = Item(use_function=heal, amount=40)
	healing_name = Name(display_name="Fizzy Potion", true_name="Healing Potion")
	tempItem = Entity(x, y, '!', libtcod.violet, render_order=RenderOrder.ITEM, item=healing_component, name=healing_name)
	return tempItem

def make_poison_potion(x=1, y=1):
	poison_component = Item(use_function=poison, amount=10)
	poison_name = Name(dipslay_name="Dark Potion", true_name="Poison Potion")
	tempItem = Entity(x, y, '!', libtcod.violet, render_order=RenderOrder.ITEM, item=poison_component, name=poison_name)
	return tempItem

def make_confusion_potion(x=1, y=1):
	confusion_component = Item(use_function=confusion, target_self=True)
	confusion_name = Name(dipslay_name="Clear Potion", true_name="Confusion Potion")
	tempItem = Entity(x, y, '!', libtcod.violet, )

def make_lightning_scroll(x=1, y=1):
	lightning_scroll_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
	tempItem = Entity(x, y, '?', libtcod.yellow, render_order=RenderOrder.ITEM, item=lightning_scroll_component)
	return tempItem

def make_fireball_scroll(x=1, y=1):
	fireball_scroll_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=25, radius=3)
	tempItem = Entity(x, y, '?', libtcod.red, render_order=RenderOrder.ITEM, item=fireball_scroll_component)
	return tempItem

def make_confusion_scroll(x=1, y=1):
	confusion_scroll_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message('Left-click on an enemy to confuse it or right-click to cancel.', libtcod.light_cyan))
	tempItem = Entity(x, y, '?', libtcod.light_pink, render_order=RenderOrder.ITEM, item=confusion_scroll_component)
	return tempItem

def make_fireball_book(x=1, y=1):
	fireball_book_component = Item(use_function=learn_fireball, spell="Fireball")
	tempItem = Entity(x, y, '#', libtcod.red, render_order=RenderOrder.ITEM, item=fireball_book_component)
	return tempItem

def make_heal_book(x=1, y=1):
	heal_book_component = Item(use_function=learn_heal, spell="Heal")
	tempItem = Entity(x, y, '#', libtcod.red, render_order=RenderOrder.ITEM, item=heal_book_component)
	return tempItem

identified_potions = {}
identified_scrolls = {}