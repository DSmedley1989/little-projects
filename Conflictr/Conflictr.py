import sublime, sublime_plugin

class ConflictrCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.conflicts =self.view.find_all('<{5,}')
		self.number_of_conflicts = len(self.conflicts)
		the_message = ("Conflictr has found %d Merge "
		"Conflicts in this file." % self.number_of_conflicts)
		self.many_options = ["First Conflict", "Next Conflict", "Previous Conflict"]
		sublime.status_message(the_message)
		self.view_index = 0
		if len(self.conflicts) == 1:
			self.view.show(conflicts[0])
		elif len(self.conflicts) > 1:
			self.view.window().show_quick_panel(self.many_options, self.scroll_to_conflict)
		return

	def scroll_to_conflict(self, choice):
		if choice == -1:
			return
		elif choice == 1:
			self.view.show(self.conflicts[0])
			self.view_index = 0
		elif choice == 2:
			self.view.show(self.conflicts)
		return