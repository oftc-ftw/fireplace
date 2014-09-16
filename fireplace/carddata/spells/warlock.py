import random
from fireplace.enums import Race, Zone
from ..card import *


# Drain Life
class CS2_061(Card):
	def action(self, target):
		target.damage(2)
		self.heal(2)


# Hellfire
class CS2_062(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_CHARACTERS):
			target.damage(3)


# Shadow Bolt
class CS2_057(Card):
	action = damageTarget(4)


# Mortal Coil
class EX1_302(Card):
	def action(self, target):
		target.damage(1)
		if target.zone == Zone.GRAVEYARD:
			self.controller.draw()


# Shadowflame
class EX1_303(Card):
	def action(self, target):
		for minion in self.controller.opponent.field:
			minion.damage(target.atk)
		target.destroy()


# Soulfire
class EX1_308(Card):
	def action(self, target):
		target.damage(4)
		if self.controller.hand:
			random.choice(self.controller.hand).discard()


# Siphon Soul
class EX1_309(Card):
	def action(self, target):
		self.controller.hero.heal(3)
		target.destroy()


# Twisting Nether
class EX1_312(Card):
	def action(self):
		for minion in self.controller.getTargets(TARGET_ALL_MINIONS):
			target.destroy()


# Power Overwhelming
class EX1_316(Card):
	action = buffTarget("EX1_316e")

class EX1_316e(Card):
	atk = 4
	health = 4
	def endTurn(self):
		self.owner.destroy()


# Bane of Doom
class EX1_320(Card):
	def action(self, target):
		target.damage(2)
		if target.zone == Zone.GRAVEYARD:
			self.controller.summon(random.choice(self.data.entourage))


# Demonfire
class EX1_596(Card):
	def action(self, target):
		if target.race == Race.DEMON and target.controller == self.controller:
			target.buff("EX1_596e")
		else:
			target.damage(2)

class EX1_596e(Card):
	atk = 2
	health = 2


# Sacrificial Pact
class NEW1_003(Card):
	def action(self, target):
		target.destroy()
		self.controller.hero.heal(5)