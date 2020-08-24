from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from random import randint
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.clock import Clock


class AllInfo:
    def __init__(self, rows=4, cols=4):
        self.cols = cols
        self.rows = rows
        self.info_text = "das bin ich"

    def print_all_info(self, fromtext="direct"):
        print("All Info from: ", fromtext)
        print("Cols: ", self.cols)
        print("Rows: ", self.rows)


class TilesField(GridLayout):
    def __init__(self, information, **kwargs):
        self.info = information
        # make sure we aren't overriding any important functionality
        super(TilesField, self).__init__(**kwargs)

        # spacing = Space between tiles and padding = Space around all tiles
        self.spacing = 2
        self.padding = 10
        self.new_game = True

        # fixed number of cols and rows
        self.set_rows_cols(self.info.rows, self.info.cols)
        self.all_tiles = []
        self.place_new_tiles(self.new_shuffled_field(100))
        Clock.schedule_once(self.first_menu_popup, 1.0/20.0)

    def first_menu_popup(self, dt):
        self.menu_popup("New Game", (0,.4,0,1))
        return dt

    def make_label_and_slider(self):
        self.row_label = Label(text="Rows: ", id="labelrows")
        self.row_slider = Slider(value_track=True,
                                 value_track_color=[1, 0, 0, 1],
                                 min=2, max=6,
                                 id="rows",
                                 step=1,
                                 value=self.info.rows)
        self.row_slider.bind(value=self.slider_changed)
        self.col_label = Label(text="Cols: ", id="labelcols")
        self.col_slider = Slider(value_track=True,
                                 value_track_color=[1, 0, 0, 1],
                                 min=2, max=6,
                                 id="cols",
                                 step=1,
                                 value=self.info.cols)
        self.col_slider.bind(value=self.slider_changed)
        self.show.add_widget(self.row_label)
        self.show.add_widget(self.row_slider)
        self.show.add_widget(self.col_label)
        self.show.add_widget(self.col_slider)

    def slider_changed(self, instance=0, value=0):
        self.row_label.text = "Number of rows: " + str(self.row_slider.value)
        self.info.rows = self.row_slider.value
        self.col_label.text = "Number of columns: " + str(self.col_slider.value)
        self.info.cols = self.col_slider.value

    def make_popup_buttons(self):
        self.new_game_button = Button(text="Start new game", id="newgame", on_press=self.new_game_button_pressed)
        self.show.add_widget(self.new_game_button)
        if not self.new_game:
            self.resume_button = Button(text="Resume game", id="resume", on_press=self.resume_button_pressed)
            self.show.add_widget(self.resume_button)
        self.quit_button = Button(text="Quit", id="quit", on_press=self.quit_button_pressed)
        self.show.add_widget(self.quit_button)

    def menu_popup(self, menu_text="Have fun", color=(1,1,1,1)):
        self.show = BoxLayout(orientation="vertical")
        self.show.add_widget(Label(text=menu_text,
                                   font_size=32,
                                   color=color))
        self.make_label_and_slider()
        self.make_popup_buttons()
        self.popupWindow = Popup(title="Slider Puzzle by Johdal12(UM)",
                                 content=self.show,
                                 size_hint=(.8, .8))
        self.popupWindow.open()
        self.slider_changed()

    def new_game_button_pressed(self, instance):
        self.new_game = False
        self.remove_all_tiles()
        self.set_rows_cols(self.info.rows, self.info.cols)
        self.all_tiles = []
        self.place_new_tiles(self.new_shuffled_field(100))
        self.popupWindow.dismiss()

    def resume_button_pressed(self, instance):
        self.popupWindow.dismiss()

    def quit_button_pressed(self, instance):
        exit()

    def new_shuffled_field(self, number_of_random_moves=10):
        if number_of_random_moves < 2 or number_of_random_moves > 1000:
            number_of_random_moves = 10
        tile_field = self.get_a_new_shuffle_field()
        empty_x = self.cols-1
        empty_y = self.rows-1
        last_move = 0
        all_moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for shuffles in range(1, number_of_random_moves):
            legal_moves = self.get_legal_moves_for_empty_tile(empty_x, empty_y, last_move)
            # This new move is at the same time the next last_move
            last_move = legal_moves[randint(0, len(legal_moves)-1)]
            # Calculate the next position of empty tile
            new_empty_x = empty_x + all_moves[last_move][0]
            new_empty_y = empty_y + all_moves[last_move][1]
            # move the tile to the empty tile
            tile_field[empty_y][empty_x] = tile_field[new_empty_y][new_empty_x]
            tile_field[new_empty_y][new_empty_x] = 0
            empty_x = new_empty_x
            empty_y = new_empty_y
        return self.convert_tile_field_to_tile_list(tile_field)

    def convert_tile_field_to_tile_list(self, tile_field):
        tile_list = []
        for row in tile_field:
            for column_element in row:
                tile_list.append(column_element)
        return tile_list

    def get_a_new_shuffle_field(self):
        tile_field = []
        for y in range(1, self.rows+1):
            tile_row = []
            for x in range(1, self.cols+1):
                tile_row.append((y-1) * self.cols + x)
            tile_field.append(tile_row)
        tile_field[self.rows-1][self.cols-1] = 0
        return tile_field

    def get_legal_moves_for_empty_tile(self, empty_x, empty_y, last_move):
        # Welche legalen moves gibt es clockwise/3(12=0->0, 3->1, 6->2, 9->3)
        # nicht entlang des vorhergehenden moves zurück
        legal_moves = []
        # There is a tile at the top and the last move wasn't down.
        if empty_y > 0 and last_move != 2:
            legal_moves.append(0)
        # There is a tile to the right and the last move wasn't left.
        if empty_x < self.cols-1 and last_move != 3:
            legal_moves.append(1)
        # There is a tile at the bottom and the last move wasn't up.
        if empty_y < self.rows-1 and last_move != 0:
            legal_moves.append(2)
        # There is a tile to the left and the last move wasn't right.
        if empty_x > 0 and last_move != 1:
            legal_moves.append(3)
        return legal_moves

    def get_random_move_index(self, last_move):
        move_set = [0, 1, 2, 3]
        if 0 <= last_move < 4:
            move_set.pop(last_move)
        return move_set[randint(0, len(move_set)-1)]

    def place_new_tiles(self, order_of_tiles):
        self.all_tiles = list(range(0, self.cols*self.rows))
        # Let's add x * y buttons to this layout.
        for y in range(1, self.rows+1):
            for x in range(1, self.cols+1):
                if order_of_tiles[0] == 0:
                    new_button = Button(
                        text="Menu",
                        id="0",
                        color=(1, 1, 1, 1)
                    )
                else:
                    new_button = Button(
                        text=str(order_of_tiles[0]),
                        id=str(order_of_tiles[0]),
                        font_size=32,
                    )
                new_button.bind(on_press=self.tile_was_pressed)
                self.all_tiles[order_of_tiles[0]] = new_button
                self.add_widget(new_button)
                # Give the tiles the right or wrong color.
                if order_of_tiles[0] == (y-1) * self.cols + x:
                    self.tile_color_right_place(order_of_tiles[0])
                else:
                    self.tile_color_wrong_place(order_of_tiles[0])
                order_of_tiles.pop(0)

    def set_rows_cols(self, rows, cols):
        self.cols = cols
        self.rows = rows

    def tile_was_pressed(self, instance):
        tile_pressed = int(instance.id)
        if not self.legal_tile_number(tile_pressed):
            return

        # If empty_button was pressed quit game.
        if tile_pressed == 0:
            self.menu_button_pressed()
            return

        self.switch_with_empty_tile(tile_pressed)
        self.color_tile_for_position(tile_pressed)
        self.check_if_finished()

    def legal_tile_number(self, tile_number):
        if 0 <= tile_number < len(self.all_tiles):
            return True
        else:
            return False

    def print_tile_infos(self, tile_number):
        if not self.legal_tile_number(tile_number):
            return
        else:
            print("Tile_info No.: <", str(tile_number), "> coord:", self.tile_grid_coordinates(tile_number))
            print(self.tile_number_grid_coordinates(tile_number))
            print("-----------------------")
            for element_info in ["pos", "width", "height"]:
                print(element_info, " = ", eval("self.all_tiles[tile_number]." + element_info))

    # (1, 2) should be: x=1 from left to the right and y=2 from bottom up
    # (-1, -1) tile_number is not legal
    def tile_number_grid_coordinates(self, tile_number):
        if tile_number == 0:
            return self.cols-1, 0
        if not self.legal_tile_number(tile_number):
            return -1, -1
        else:
            grid_x = (tile_number - 1) % self.cols
            grid_y = self.rows - int((tile_number-grid_x - 1) / self.cols) - 1
            return grid_x, grid_y

    # (1, 2) x=1 from left to the right and y=2 from bottom up
    # (-1, -1) tile_number is not legal
    def tile_grid_coordinates(self, tile_number):
        if not self.legal_tile_number(tile_number):
            return -1, -1
        else:
            grid_x = (self.all_tiles[tile_number].x - self.padding[0])/\
                     (self.all_tiles[tile_number].width + self.spacing[0])
            grid_y = (self.all_tiles[tile_number].y - self.padding[0])/\
                     (self.all_tiles[tile_number].height + self.spacing[0])
            return int(grid_x), int(grid_y)

    def game_won(self):
        self.new_game = True
        self.menu_popup("You won!",(1,1,1,1))

    def menu_button_pressed(self):
        self.menu_popup("Menu", (1,0,0,1))

    def remove_all_tiles(self):
        if len(self.all_tiles) > 0:
            parent = self.all_tiles[0].parent
            for instance in self.all_tiles:
                parent.remove_widget(instance)

    def switch_with_empty_tile(self, tile_pressed):
        if not self.button_is_next_to_empty_tile(tile_pressed):
            return
        else:
            swap_pos = self.all_tiles[0].pos[:]
            self.all_tiles[0].pos = self.all_tiles[tile_pressed].pos[:]
            self.all_tiles[tile_pressed].pos = swap_pos[:]

    def check_if_finished(self):
        anzahl = 0
        for tile_number in range(1, len(self.all_tiles)+1):
            if self.check_tile_at_correct_position(tile_number):
                anzahl += 1
        if anzahl == self.rows * self.cols -1:
            self.game_won()

    def color_tile_for_position(self, tile_number):
        if self.check_tile_at_correct_position(tile_number):
            self.tile_color_right_place(tile_number)
        else:
            self.tile_color_wrong_place(tile_number)

    def check_tile_at_correct_position(self, tile_number):
        if not self.legal_tile_number(tile_number):
            return False
        else:
            delta_x = self.tile_grid_coordinates(tile_number)[0] - self.tile_number_grid_coordinates(tile_number)[0]
            delta_y = self.tile_grid_coordinates(tile_number)[1] - self.tile_number_grid_coordinates(tile_number)[1]
            if abs(delta_x) + abs(delta_y) == 0:
                return True
            else:
                return False

    def tile_color_wrong_place(self, tile_number):
        if self.legal_tile_number(tile_number):
            if tile_number == 0:
                self.all_tiles[tile_number].background_color = (0, 0, 0, 1)
            else:
                self.all_tiles[tile_number].background_color = (1, 0.1, 0.2, 1)

    def tile_color_right_place(self, tile_number):
        if self.legal_tile_number(tile_number):
            if tile_number == 0:
                self.all_tiles[tile_number].background_color = (0, 0, 0, 1)
            else:
                self.all_tiles[tile_number].background_color = (0.1, 1, 0.2, 1)

    def button_is_next_to_empty_tile(self, tile_pressed):
        if not self.legal_tile_number(tile_pressed):
            return False
        delta_x = self.tile_grid_coordinates(tile_pressed)[0] - self.tile_grid_coordinates(0)[0]
        delta_y = self.tile_grid_coordinates(tile_pressed)[1] - self.tile_grid_coordinates(0)[1]
        if abs(delta_x) + abs(delta_y) == 1:
            return True
        else:
            return False


class Slider_Puzzle(App):
    def build(self):
        self.info = AllInfo(4, 4)
        t = TilesField(self.info, size=Window.size)
        return t


if __name__ == '__main__':
    Slider_Puzzle().run()
