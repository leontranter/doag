from components.item import Item
from entity import Entity
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse, poison
import tcod as libtcod
from render_functions import RenderOrder
from game_messages import Message
from components.name import Name
from random import shuffle

def make_healing_potion(x=1, y=1):
	healing_component = Item(use_function=heal, amount=40)
	healing_name = Name(true_name="Healing Potion")
	tempItem = Entity(x, y, '!', libtcod.violet, render_order=RenderOrder.ITEM, item=healing_component, name=healing_name)
	return tempItem

def make_poison_potion(x=1, y=1):
	poison_component = Item(use_function=poison, amount=10)
	poison_name = Name(true_name="Poison Potion")
	tempItem = Entity(x, y, '!', libtcod.violet, render_order=RenderOrder.ITEM, item=poison_component, name=poison_name)
	return tempItem

def make_confusion_potion(x=1, y=1):
	confusion_component = Item(use_function=confusion, target_self=True)
	confusion_name = Name(true_name="Confusion Potion")
	tempItem = Entity(x, y, '!', libtcod.violet, render_order=RenderOrder.ITEM, item=poison_component, name=poison_name)

def make_lightning_scroll(x=1, y=1):
	lightning_scroll_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
	lightning_scroll_name = Name(true_name="Lightning Scroll")
	tempItem = Entity(x, y, '?', libtcod.yellow, render_order=RenderOrder.ITEM, item=lightning_scroll_component, name=lightning_scroll_name)
	return tempItem

def make_fireball_scroll(x=1, y=1):
	fireball_scroll_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=25, radius=3)
	fireball_scroll_name = Name(true_name="Fireball Scroll")
	tempItem = Entity(x, y, '?', libtcod.red, render_order=RenderOrder.ITEM, item=fireball_scroll_component, name=fireball_scroll_name)
	return tempItem

def make_confusion_scroll(x=1, y=1):
	confusion_scroll_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message('Left-click on an enemy to confuse it or right-click to cancel.', libtcod.light_cyan))
	confusion_scroll_name = Name(true_name="Confusion Scroll")
	tempItem = Entity(x, y, '?', libtcod.light_pink, render_order=RenderOrder.ITEM, item=confusion_scroll_component, name=confusion_scroll_name)
	return tempItem

def make_fireball_book(x=1, y=1):
	fireball_book_component = Item(use_function=learn_fireball, spell="Fireball")
	fireball_book_name = Name("Fireball spellbook")
	tempItem = Entity(x, y, '#', libtcod.red, render_order=RenderOrder.ITEM, item=fireball_book_component, name=fireball_book_name)
	return tempItem

def make_heal_book(x=1, y=1):
	heal_book_component = Item(use_function=learn_heal, spell="Heal")
	heal_book_name = Name("Heal spellbook")
	tempItem = Entity(x, y, '#', libtcod.red, render_order=RenderOrder.ITEM, item=heal_book_component, name=heal_book_name)
	return tempItem

def make_bless_book(x=1, y=1):
	heal_book_component = Item(use_function=learn_heal, spell="Heal")
	bless_book_name = Name("Bless spellbook")
	tempItem = Entity(x, y, '#', libtcod.red, render_order=RenderOrder.ITEM, item=heal_book_component, name=bless_book_name)
	return tempItem