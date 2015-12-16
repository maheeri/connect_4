from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import *
from functools import partial
from kivy.clock import Clock
import connect4
import mode_controller
import time


class ModeScreen(Screen):
	def __init__(self, game, **kwargs):
		super(ModeScreen, self).__init__(** kwargs)
		self.game = game

		mode_layout = BoxLayout(spacing=10, orientation="vertical")

		welcome_message = Label(text="Please choose Connect4 mode")

		btn1 = Button(text="CPU vs. CPU")
		btn1.bind(on_press=self.cpu_cpu_mode)
		btn2 = Button(text="Human vs. CPU")
		btn2.bind(on_press=self.human_cpu_mode)
		btn3 = Button(text="Human vs. Human")
		btn3.bind(on_press=self.human_human_mode)

		mode_layout.add_widget(welcome_message)
		mode_layout.add_widget(btn1)
		mode_layout.add_widget(btn2)
		mode_layout.add_widget(btn3)

		self.add_widget(mode_layout)

	def human_human_mode(self, *args):
		self.game.mode = 0
		self.manager.current = "game"

	def human_cpu_mode(self, *args):
		self.game.mode = 1
		self.manager.current = "game"

	def cpu_cpu_mode(self, *args):
		self.game.mode = 2
		self.manager.current = "game"



class GameScreen(Screen):

	def __init__(self, game, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
		self.game = game

		self.game_layout = GridLayout(cols=7, rows=7)

		for y in range(6):
			for x in range(7):
				self.game_layout.add_widget(Button(background_color=(255,255,255,1.0)))

		for i in range(7):
			self.game_layout.add_widget(Button(text=str(i), on_press=self.update_and_repaint))

		self.add_widget(self.game_layout)


	def repaint_board(self):
		self.game_layout.clear_widgets()

		for y in range(5,-1,-1):
			for x in range(7):
				if (self.game.board[x][y] == "red"):
					self.game_layout.add_widget(Button(background_color=(255,0,0,1.0)))
				elif (self.game.board[x][y] == "yellow"):
					self.game_layout.add_widget(Button(background_color=(255,255,0,1.0)))
				else:
					self.game_layout.add_widget(Button(background_color=(255,255,255,1.0)))

		for i in range(7):
			self.game_layout.add_widget(Button(text=str(i), on_press=self.update_and_repaint))


	def update_and_repaint(self, instance):
		self.game.updateBoard(int(instance.text))
		self.repaint_board()

		if (self.game.mode == 1):
			cpu_move_num = mode_controller.human_vs_cpu(self.game)
			self.game.updateBoard(cpu_move_num)
			self.repaint_board()

class Connect4GUI(App):

	def build(self):

		# memory representation of the board
		connect4_game = connect4.Connect4()
		# adding screens to the screen manager
		screen_manager = ScreenManager()
		mode_screen = ModeScreen(connect4_game, name="mode")
		game_screen = GameScreen(connect4_game, name="game")
		screen_manager.add_widget(mode_screen)
		screen_manager.add_widget(game_screen)
		return screen_manager


if __name__ == "__main__":
	Connect4GUI().run()