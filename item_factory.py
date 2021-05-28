from components.item import Item
from entity import Entity
from magic_functions import heal, cast_fireball, cast_confuse, poison, learn_spell_from_book, apply_confuse
import tcod as libtcod
from render_functions import RenderOrder
from game_messages import Message
from components.name import Name
from random import shuffle
from components.consumable import Consumable, ConsumableTypes

def make_healing_potion(x=1, y=1):
	healing_component = Consumable(ConsumableTypes.POTION, use_function=heal, amount=40)
	healing_name = Name(true_name="Healing Potion")
	healing_item = Item(1, 1)
	temp_entity = Entity(x, y, '!', libtcod.violet, render_order=RenderOrder.ITEM, item=healing_item, consumable=healing_component, name=healing_name)
	return temp_entity

def make_poison_potion(x=1, y=1):
	poison_consumable = Consumable(ConsumableTypes.POTION, use_function=poison, amount=3)
	poison_name = Name(true_name="Poison Potion")
	poison_item = Item(1, 1)
	temp_entity = Entity(x, y, '!', libtcod.violet, render_order=RenderOrder.ITEM, item=poison_item, name=poison_name, consumable=poison_consumable)
	return temp_entity

def make_confusion_potion(x=1, y=1):
	confusion_consumable = Consumable(ConsumableTypes.POTION, use_function=apply_confuse, target_self=True)
	confusion_name = Name(true_name="Confusion Potion")
	confusion_item = Item(1, 1)
	temp_entity = Entity(x, y, '!', libtcod.violet, render_order=RenderOrder.ITEM, item=confusion_item, name=confusion_name, consumable=confusion_consumable)
	return temp_entity

def make_fireball_scroll(x=1, y=1):
	fireball_scroll_consumable = Consumable(ConsumableTypes.SCROLL, use_function=cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=25, radius=3)
	fireball_scroll_name = Name(true_name="Fireball Scroll")
	fireball_scroll_item = Item(1, 1)
	temp_entity = Entity(x, y, '?', libtcod.red, render_order=RenderOrder.ITEM, item=fireball_scroll_item, name=fireball_scroll_name, consumable=fireball_scroll_consumable)
	return temp_entity

def make_confusion_scroll(x=1, y=1):
	confusion_scroll_consumable = Consumable(ConsumableTypes.SCROLL, use_function=cast_confuse, targeting=True, targeting_message=Message('Left-click on an enemy to confuse it or right-click to cancel.', libtcod.light_cyan))
	confusion_scroll_name = Name(true_name="Confusion Scroll")
	confusion_scroll_item = Item(1, 1)
	temp_entity = Entity(x, y, '?', libtcod.light_pink, render_order=RenderOrder.ITEM, item=confusion_scroll_item, name=confusion_scroll_name, consumable=confusion_scroll_consumable)
	return temp_entity

def make_fireball_book(x=1, y=1):
	fireball_book_consumable = Consumable(ConsumableTypes.SPELLBOOK, use_function=learn_spell_from_book, spell_name="fireball")
	fireball_book_name = Name("Fireball spellbook")
	fireball_book_item = Item(1, 1)
	temp_entity = Entity(x, y, '#', libtcod.red, render_order=RenderOrder.ITEM, item=fireball_book_item, name=fireball_book_name, consumable=fireball_book_consumable)
	return temp_entity

def make_heal_book(x=1, y=1):
	heal_book_consumable = Consumable(ConsumableTypes.SPELLBOOK, use_function=learn_spell_from_book, spell_name="heal")
	heal_book_name = Name("Heal spellbook")
	heal_book_item = Item(1, 1)
	temp_entity = Entity(x, y, '#', libtcod.red, render_order=RenderOrder.ITEM, item=heal_book_component, name=heal_book_name, consumable=heal_book_consumable)
	return temp_entity

def make_bless_book(x=1, y=1):
	bless_book_consumable = Consumable(ConsumableTypes.SPELLBOOK, use_function=learn_spell_from_book, spell_name="bless")
	bless_book_name = Name("Bless spellbook")
	bless_book_item = Item(1, 1)
	temp_entity = Entity(x, y, '#', libtcod.red, render_order=RenderOrder.ITEM, item=bless_book_item, name=bless_book_name, consumable=bless_book_consumable)
	return temp_entity
