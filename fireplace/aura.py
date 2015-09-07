from .managers import CardManager
from .utils import fireplace_logger as logger


class AuraBuff:
	def __init__(self, source, entity):
		self.source = source
		self.entity = entity
		self.tags = CardManager(self)

	def __repr__(self):
		return "<AuraBuff %r -> %r>" % (self.source, self.entity)

	def update_tags(self, tags):
		self.tags.update(tags)
		self.tick = self.source.game.tick

	def destroy(self):
		logger.debug("Destroying %r", self)
		self.entity.slots.remove(self)
		self.source.game.active_aura_buffs.remove(self)

	def _getattr(self, attr, i):
		value = getattr(self, attr, 0)
		if callable(value):
			return value(self.entity, i)
		return i + value


class Refresh:
	"""
	Refresh a buff or a set of tags on an entity
	"""
	def __init__(self, selector, tags=None, buff=None, priority=50):
		self.selector = selector
		self.tags = tags
		self.buff = buff
		self.priority = priority

	def trigger(self, source):
		entities = self.selector.eval(source.game, source)
		for entity in entities:
			if self.buff:
				entity.refresh_buff(source, self.buff)
			else:
				tags = {}
				for tag, value in self.tags.items():
					if not isinstance(value, int) and not callable(value):
						value = value.evaluate(source)
					tags[tag] = value

				entity.refresh_tags(source, tags)


class TargetableByAuras:
	def refresh_buff(self, source, id):
		for slot in self.slots[:]:
			if slot.source is source:
				self.slots.remove(slot)
				self.slots.append(slot)
				slot.tick = source.game.tick
				break
		else:
			logger.debug("Aura from %r buffs %r with %r", source, self, id)
			buff = source.buff(self, id)
			buff.tick = source.game.tick
			source.game.active_aura_buffs.append(buff)

	def refresh_tags(self, source, tags):
		for slot in self.slots[:]:
			if slot.source is source:
				slot.update_tags(tags)
				# Move the buff position at the end again
				self.slots.remove(slot)
				self.slots.append(slot)
				break
		else:
			buff = AuraBuff(source, self)
			logger.debug("Creating %r", buff)
			buff.update_tags(tags)
			self.slots.append(buff)
			source.game.active_aura_buffs.append(buff)
