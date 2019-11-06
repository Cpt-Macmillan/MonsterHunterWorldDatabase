import wx
import sqlite3

import CustomGridRenderer as cgr
from Debug.debug import debug

class SearchWindow:

	def __init__(self, root):
		self.root = root
		self.init = True
		self.conn = sqlite3.connect("mhw.db")

		self.win = wx.Frame(root, title="Debug", style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
		self.win.SetIcon(wx.Icon("images/Nergigante.png"))
		self.win.SetSize(700, 700)
		self.win.Center()
		self.win.Bind(wx.EVT_CLOSE, self.onClose)

		panel = wx.Panel(self.win)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.search = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
		self.search.SetHint("  search by name")
		self.search.Bind(wx.EVT_TEXT_ENTER, self.onSearchTextEnter)
		sizer.Add(self.search, 1, wx.EXPAND)

		self.results = cgr.HeaderBitmapGrid(panel)
		self.results.EnableEditing(False)
		self.results.EnableDragRowSize(False)
		self.results.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onResultSelection)
		self.results.CreateGrid(1, 2)
		self.results.SetDefaultRowSize(27, resizeExistingRows=True)
		self.results.HideRowLabels()
		self.results.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
		self.results.SetColLabelValue(0, "Name")
		self.results.SetColSize(0, 660)
		self.results.SetColSize(1, 0)
		sizer.Add(self.results, 120, wx.EXPAND)

		panel.SetSizer(sizer)


		self.makeMenuBar()

		self.win.Show()

		self.init = False


	def onSearchTextEnter(self, event):
		self.searchText = self.search.GetValue()
		self.padding = " " * 8

		try:
			self.results.DeleteRows(0, self.results.GetNumberRows())
		except:
			pass

		self.loadMonsters()
		self.loadWeapons()
		self.loadArmor()
		self.loadCharms()
		self.loadDecorations()
		self.loadSkills()
		self.loadItems()
		self.loadLocations()

		
	def loadMonsters(self):
		sql = f"""
			SELECT m.id, mt.name
			FROM monster m
			JOIN monster_text mt
				ON m.id = mt.id
			WHERE mt.name LIKE '%{self.searchText}%'
				AND mt.lang_id = :langId
		"""

		data = self.conn.execute(sql, ("en",))
		data = data.fetchall()

		for row in data:
			self.results.AppendRows()
			r = self.results.GetNumberRows() - 1
			img = wx.Bitmap(f"images/monsters/24/{row[1]}.png")
			self.results.SetCellRenderer(r, 0, cgr.ImageTextCellRenderer(img, f"{self.padding}{row[1]}", hAlign=wx.ALIGN_LEFT, imageOffset=320))
			self.results.SetCellValue(r, 1, f"{row[0]}")

	
	def loadWeapons(self):
		sql = f"""
			SELECT w.id, w.weapon_type, w.rarity, wt.name
			FROM weapon w
				JOIN weapon_text wt USING (id)
			WHERE wt.lang_id = 'en'
				AND wt.name LIKE '%{self.searchText}%'
			ORDER BY w.id ASC
		"""

		data = self.conn.execute(sql,)
		data = data.fetchall()
		
		for row in data:
			self.results.AppendRows()
			r = self.results.GetNumberRows() - 1
			img = wx.Bitmap(f"images/weapons/{row[1]}/rarity-24/{row[2]}.png")
			self.results.SetCellRenderer(r, 0, cgr.ImageTextCellRenderer(img, f"{self.padding}{row[3]}", hAlign=wx.ALIGN_LEFT, imageOffset=320))
			self.results.SetCellValue(r, 1, f"{row[0]}")


	def loadArmor(self):
		# TODO prob add sets to search as well
		sql = f"""
			SELECT a.id, at.name, a.armor_type, a.rarity
			FROM armor a
				JOIN armor_text at USING (id)
			WHERE at.lang_id = 'en'
				AND at.name LIKE '%{self.searchText}%'
		"""

		data = self.conn.execute(sql,)
		data = data.fetchall()

		for row in data:
			self.results.AppendRows()
			r = self.results.GetNumberRows() - 1
			img = wx.Bitmap(f"images/armor/{row[2]}/rarity-24/{row[3]}.png")
			self.results.SetCellRenderer(r, 0, cgr.ImageTextCellRenderer(img, f"{self.padding}{row[1]}", hAlign=wx.ALIGN_LEFT, imageOffset=320))
			self.results.SetCellValue(r, 1, f"{row[0]}")


	def loadCharms(self):
		sql = f"""
			SELECT c.id, ct.name, c.rarity
			FROM charm c
				JOIN charm_text ct
					ON ct.id = c.id
					AND ct.lang_id = 'en'
					AND ct.name LIKE '%{self.searchText}%'
		"""

		data = self.conn.execute(sql,)
		data = data.fetchall()

		for row in data:
			self.results.AppendRows()
			r = self.results.GetNumberRows() - 1
			img = wx.Bitmap(f"images/charms-24/{row[2]}.png")
			self.results.SetCellRenderer(r, 0, cgr.ImageTextCellRenderer(img, f"{self.padding}{row[1]}", hAlign=wx.ALIGN_LEFT, imageOffset=320))
			self.results.SetCellValue(r, 1, f"{row[0]}")


	def loadDecorations(self):
		sql = f"""
			SELECT d.id, dt.name, d.icon_color
			FROM decoration d
				JOIN decoration_text dt
					ON dt.id = d.id
					AND dt.lang_id = 'en'
				WHERE dt.name LIKE '%{self.searchText}%'
		"""

		data = self.conn.execute(sql,)
		data = data.fetchall()

		for row in data:
			self.results.AppendRows()
			r = self.results.GetNumberRows() - 1
			img = wx.Bitmap(f"images/items-24/Feystone{row[2]}.png")
			self.results.SetCellRenderer(r, 0, cgr.ImageTextCellRenderer(img, f"{self.padding}{row[1]}", hAlign=wx.ALIGN_LEFT, imageOffset=320))
			self.results.SetCellValue(r, 1, f"{row[0]}")


	def loadSkills(self):
		sql = f"""
			SELECT id, name, icon_color
			FROM skilltree s join skilltree_text st USING (id)
			WHERE lang_id = 'en'
			AND name LIKE '%{self.searchText}%'
		"""

		data = self.conn.execute(sql,)
		data = data.fetchall()

		for row in data:
			self.results.AppendRows()
			r = self.results.GetNumberRows() - 1
			img = wx.Bitmap(f"images/skills-24/Skill{row[2]}.png")
			self.results.SetCellRenderer(r, 0, cgr.ImageTextCellRenderer(img, f"{self.padding}{row[1]}", hAlign=wx.ALIGN_LEFT, imageOffset=320))
			self.results.SetCellValue(r, 1, f"{row[0]}")


	def loadItems(self):
		sql = f"""
			SELECT i.id, it.name, i.category, i.icon_name, i.icon_color
			FROM item i
				JOIN item_text it
					ON it.id = i.id
					AND it.lang_id = 'en'
			WHERE i.category != 'hidden'
				AND it.name LIKE '%{self.searchText}%'
		"""

		data = self.conn.execute(sql,)
		data = data.fetchall()

		for row in data:
			self.results.AppendRows()
			r = self.results.GetNumberRows() - 1
			img = wx.Bitmap(f"images/items-24/{row[3]}{row[4]}.png")
			self.results.SetCellRenderer(r, 0, cgr.ImageTextCellRenderer(img, f"{self.padding}{row[1]}", hAlign=wx.ALIGN_LEFT, imageOffset=320))
			self.results.SetCellValue(r, 1, f"{row[0]}")


	def loadLocations(self):
		sql = f"""
			SELECT id, name
			FROM location_text t
			WHERE t.lang_id = 'en'
				AND name LIKE '%{self.searchText}%'
		"""

		data = self.conn.execute(sql,)
		data = data.fetchall()

		for row in data:
			self.results.AppendRows()
			r = self.results.GetNumberRows() - 1
			img = wx.Bitmap(f"images/locations-24/{row[1]}.png")
			self.results.SetCellRenderer(r, 0, cgr.ImageTextCellRenderer(img, f"{self.padding}{row[1]}", hAlign=wx.ALIGN_LEFT, imageOffset=320))
			self.results.SetCellValue(r, 1, f"{row[0]}")

	
	def onResultSelection(self, event):
		if not self.init:
			self.currentlySelectedID = self.results.GetCellValue(event.GetRow(), 1)
			if self.currentlySelectedID != "":
				print(self.currentlySelectedID)


	def makeMenuBar(self):
		fileMenu = wx.Menu()
		closeItem = fileMenu.Append(-1, "&Close\tCtrl-F", "Closes the debug window.")
		
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu, "&File")

		self.win.SetMenuBar(menuBar)

		self.win.Bind(wx.EVT_MENU, self.onClose, closeItem)


	def onClose(self, event):
		self.win.Destroy()