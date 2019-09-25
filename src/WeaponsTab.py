import wx
import wx.grid
import wx.lib.gizmos as gizmos
import CustomGridRenderer as cgr
import wx.propgrid as wxpg
import sqlite3
import time


class WeaponsTab:

	def __init__(self, root, mainNotebook):
		self.root = root
		self.mainNotebook = mainNotebook

		self.testIcon = wx.Bitmap("cut24.png", wx.BITMAP_TYPE_ANY) # REMOVE since youll be using specific icons

		self.initWeaponsTab()


	def initWeaponsTab(self):
		self.weaponsPanel = wx.Panel(self.mainNotebook)
		self.mainNotebook.AddPage(self.weaponsPanel, "Weapons")
		self.weaponsSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.weaponsTreeSizer = wx.BoxSizer(wx.VERTICAL)
		self.weaponsTree = gizmos.TreeListCtrl(self.weaponsPanel, -1, style=0,
												agwStyle=
												  gizmos.TR_DEFAULT_STYLE
												#| gizmos.TR_TWIST_BUTTONS
												| gizmos.TR_ROW_LINES
												| gizmos.TR_COLUMN_LINES
												#| gizmos.TR_NO_LINES
												| gizmos.TR_FULL_ROW_HIGHLIGHT
												| gizmos.TR_HIDE_ROOT
												)
		self.weaponsTree.Bind(wx.EVT_TREE_SEL_CHANGED, self.onWeaponSelection)
		self.weaponsTreeSizer.Add(self.weaponsTree, 1, wx.EXPAND)
		
		self.weaponsDetailedSizer = wx.BoxSizer(wx.VERTICAL)
		self.weaponImage = wx.Bitmap("images/weapons/Diablos Tyrannis.png", wx.BITMAP_TYPE_ANY)
		self.weaponImageLabel = wx.StaticBitmap(self.weaponsPanel, bitmap=self.weaponImage)

		self.weaponDetailsNotebook = wx.Notebook(self.weaponsPanel)
		self.weaponDetailPanel = wx.Panel(self.weaponDetailsNotebook)
		self.weaponFamilyPanel = wx.Panel(self.weaponDetailsNotebook)
		
		self.weaponDetailSizer = wx.BoxSizer(wx.VERTICAL)
		self.weaponDetailsNotebook.AddPage(self.weaponDetailPanel, "Detail")
		
		self.weaponFamilySizer = wx.BoxSizer(wx.VERTICAL)
		self.weaponDetailsNotebook.AddPage(self.weaponFamilyPanel, "Family")
		
		self.weaponsDetailedSizer.Add(self.weaponImageLabel, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ADJUST_MINSIZE, 10)
		self.weaponsDetailedSizer.Add(self.weaponDetailsNotebook, 3, wx.EXPAND)

		self.weaponsSizer.Add(self.weaponsTreeSizer, 2, wx.EXPAND)
		self.weaponsSizer.Add(self.weaponsDetailedSizer, 1, wx.EXPAND)

		self.weaponsPanel.SetSizer(self.weaponsSizer)

		self.loadWeaponsTree()


	def loadWeaponsTree(self):
		isz = (24,24)
		il = wx.ImageList(isz[0], isz[1])
		self.nergidx = il.Add(self.testIcon)
		self.weaponsTree.SetImageList(il)

		self.weaponsTree.AddColumn("Name")
		self.weaponsTree.AddColumn("Physical")
		self.weaponsTree.AddColumn("Element/Status")
		self.weaponsTree.AddColumn("Affinity")
		self.weaponsTree.AddColumn("Defense")
		self.weaponsTree.AddColumn("Slots")
		
		self.weaponsTree.AddColumn("R")
		self.weaponsTree.AddColumn("O")
		self.weaponsTree.AddColumn("Y")
		self.weaponsTree.AddColumn("G")
		self.weaponsTree.AddColumn("B")
		self.weaponsTree.AddColumn("W")
		self.weaponsTree.AddColumn("P")
		
		self.weaponsTree.AddColumn("id")
		
		self.weaponsTree.SetMainColumn(0)
		self.weaponsTree.SetColumnWidth(0, 400)

		for num in range(1, 6):
			self.weaponsTree.SetColumnImage(num, self.nergidx)
			self.weaponsTree.SetColumnAlignment(num, wx.ALIGN_CENTER)
			self.weaponsTree.SetColumnWidth(num, 35)

		for num in range(6, 13):
			self.weaponsTree.SetColumnImage(num, self.nergidx)
			self.weaponsTree.SetColumnAlignment(num, wx.ALIGN_CENTER)
			self.weaponsTree.SetColumnWidth(num, 24)
		
		self.weaponsTree.SetColumnWidth(5, 50)
		self.weaponsTree.SetColumnWidth(13, 0)

		root = self.weaponsTree.AddRoot("Weapon")
		normalWeaponNode = self.weaponsTree.AppendItem(root, "Normal")
		kulveWeaponNode = self.weaponsTree.AppendItem(root, "Kulve")

		sql = """
			SELECT w.id, w.weapon_type, w.category, w.rarity, w.attack, w.attack_true, w.affinity, w.defense, w.slot_1, w.slot_2, w.slot_3, w.element1, w.element1_attack,
				w.element2, w.element2_attack, w.element_hidden, w.sharpness, w.sharpness_maxed, w.previous_weapon_id, w.craftable, w.kinsect_bonus,
				w.elderseal, w.phial, w.phial_power, w.shelling, w.shelling_level, w.coating_close, w.coating_power, w.coating_poison, w.coating_paralysis, w.coating_sleep, w.coating_blast,
				w.notes, wa.special_ammo, wt.name
			FROM weapon w
				JOIN weapon_text wt USING (id)
				LEFT JOIN weapon_ammo wa ON w.ammo_id = wa.id
			WHERE wt.lang_id = :langId
				AND w.weapon_type = :weaponType
			ORDER BY w.id ASC
			"""

		conn = sqlite3.connect("../MonsterHunterWorld/mhw.db")
		data = conn.execute(sql, ("en", "charge-blade", ))

		weaponNodes = {}
		rarityIcon = {
			1: "images/weapons/",
		}

		start = time.time()
		for row in data:
			if row[2] != "Kulve":
				if row[18] == None:
					print(row)
					self.populateWeaponsTree(normalWeaponNode, row, weaponNodes)
				else:
					self.populateWeaponsTree(weaponNodes[row[18]], row, weaponNodes)
			else:
				self.populateWeaponsTree(kulveWeaponNode, row, weaponNodes)
		end = time.time()
		print("load weapon tree time: " + str(end - start))

		# PREFERENCES again add this as a setting in the preferences window/tab/whatever
		self.weaponsTree.ExpandAll()
		#self.weaponsTree.Expand(normalWeaponNode)
		#self.weaponsTree.Expand(kulveWeaponNode)


	def populateWeaponsTree(self, weaponNode, row, weaponNodes):
		if bool(row[19]):
			# TODO maybe add rarity in a similar manner?? row[3]
			name = str(row[34]) + " 🔨" # TODO make this clearer that it means craftable
		else:
			name = str(row[34])
		weapon = self.weaponsTree.AppendItem(weaponNode,  name)
		self.weaponsTree.SetItemText(weapon, str(row[4]), 1)
		element = str(row[12])
		if row[15] == 0 and row[12] == None:
			element = ""
		elif row[15] == 1:
			element = "(" + str(row[12]) + ")"
			# special color for dual element?? or alternatively have two columns for elements
			if row[14] != None:
				element = str(row[12]) + "\n" + str(row[14])
		if row[6] == 0:
			affinity = ""
		else:
			affinity = str(row[6]) + "%"
		if row[7] == 0:
			defense = ""
		else:
			defense = "+" + str(row[7])
		self.weaponsTree.SetItemText(weapon, element, 2) 
		self.weaponsTree.SetItemText(weapon, affinity, 3)
		self.weaponsTree.SetItemText(weapon, defense, 4)
		self.weaponsTree.SetItemText(weapon, str(row[8:11]), 5)
		
		# sharpness
		sharpnessSplit = str(row[16]).replace("(", "").replace(")", "").replace(" ", "").split(",")
		self.weaponsTree.SetItemText(weapon, sharpnessSplit[0], 6)
		self.weaponsTree.SetItemText(weapon, sharpnessSplit[1], 7)
		self.weaponsTree.SetItemText(weapon, sharpnessSplit[2], 8)
		self.weaponsTree.SetItemText(weapon, sharpnessSplit[3], 9)
		self.weaponsTree.SetItemText(weapon, sharpnessSplit[4], 10)
		self.weaponsTree.SetItemText(weapon, sharpnessSplit[5], 11)
		self.weaponsTree.SetItemText(weapon, sharpnessSplit[6], 12)
		
		# id - hidden, icon
		self.weaponsTree.SetItemText(weapon, str(row[0]), 13)
		self.weaponsTree.SetItemImage(weapon, self.nergidx, which = wx.TreeItemIcon_Normal)
		weaponNodes[row[0]] = weapon

		
	def onWeaponSelection(self, event):
		print("on selection")
		# TODO load details based of the weapon id found in the hidden id column