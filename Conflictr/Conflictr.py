import sublime, sublime_plugin

class ConflictrCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		conflicts = self.view.find_all('>{5,}')
		if len(conflicts) == 1:
			self.view.show(conflicts[0])
		elif len(conflicts) > 1:
			sublime.Window.show_quick_panel(range(len(conflicts)), self.view.show(conflicts[0]))