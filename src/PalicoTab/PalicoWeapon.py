class PalicoWeapon:

	def __init__(self, dbRow):
		self.id = dbRow[0]
		self.rarity = dbRow[1]
		self.rank = dbRow[2]
		self.name = dbRow[3]
		self.setName = dbRow[4]
		self.attackMelee = dbRow[5]
		self.attackRanged = dbRow[6]
		self.attackType = dbRow[7]
		self.element = dbRow[8]
		self.elementAttack = dbRow[9]
		self.elderseal = dbRow[10]
		self.affinity = dbRow[11]
		self.defense = dbRow[12]
		self.price = dbRow[13]
		self.description = dbRow[14]


	def __repr__(self):
		return f"{self.__dict__!r}"