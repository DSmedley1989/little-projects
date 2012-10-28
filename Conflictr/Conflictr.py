import sublime, sublime_plugin

class ConflictrCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.starts = self.view.find_all('<{5,}')
		self.middles = self.view.find_all('={5,}')
		self.ends = self.view.find_all('>{5,}')
		self.number_of_conflicts = len(self.starts)
		self.create_conflict_areas()
		self.visible_region = self.view.visible_region()
		self.view_index = self.find_view_position()
		self.menu = self.populate_menu_options()
		the_message = ("Conflictr has found %d Merge "
		"Conflicts in this file." % self.number_of_conflicts)
		self.many_options = ["First Conflict", "Next Conflict", "Previous Conflict"]
		sublime.status_message(the_message)
		self.view.window().show_quick_panel(self.menu['options'], self.parse_selection)
		return

	def scroll_to_conflict(self, conflict):
		self.view.show(conflict)
		return

	def find_view_position(self):
		view_start = self.visible_region.begin()
		view_end = self.visible_region.end()
		if view_end < self.conflicts[0]['start'].begin():
			return 0
		else:
			for n in range(self.number_of_conflicts - 1):
				if view_start > self.conflicts[n]['start'].end() and view_start < self.conflicts[n+1]['start'].begin():
					return n + 1
			return self.number_of_conflicts


	def create_conflict_areas(self):
		self.conflicts = []
		for n in range(self.number_of_conflicts):
			startline = self.view.line(self.starts[n])
			middleline = self.view.line(self.middles[n])
			endline = self.view.line(self.ends[n])
			self.conflicts.append({
				"start": startline,
				"middle": middleline,
				"end": endline
				})
		return

	def populate_menu_options(self):
		number = self.number_of_conflicts
		if number == 0:
			return {
			"type": 1,
			"options": ["No Conflicts Found."]
			}
		elif number == 1:
			return {
			"type": 2,
			"options": ["Go To Conflict"]
			}
		elif number > 1:
			if self.view == 0:
				return {
				"type": 3,
				"options": ["Go To First", "Go To Next"]
				}
			elif self.view_index >= 1 and self.view_index < self.number_of_conflicts:
				return {
				"type": 4,
				"options": ["Go To First", "Go To Next", "Go To Previous"]
				}
			elif self.view_index == self.number_of_conflicts:
				return {
				"type": 5,
				"options": ["Go To First", "Go To Previous"]
				}

	def parse_selection(self, choice):
		menutype = self.menu['type']
		position = self.view_index - 1
		if choice == -1:
			return
		elif choice == 0:
			if menutype == 1:
				return
			else:
				self.scroll_to_conflict(self.starts[0])
				return
		elif choice == 1:
			if menutype == 5:
				self.scroll_to_conflict(self.starts[position - 1])
			else:
				self.scroll_to_conflict(self.starts[position + 1])
		elif choice == 2:
			if menutype == 4:
				self.scroll_to_conflict(self.starts[position - 1])