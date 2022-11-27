from .fire_chicken.mouse_position import MousePosition
from talon import Module
import os
from .display import PositionNumberingDisplay
from .confirm_command.confirmation import confirmation
module = Module()

class IndexedPositionStorage:
    def __init__(self, file_location):
        self.positions = []
        self.file_location = file_location
        self.fetch_positions_from_file()
        self.display = PositionNumberingDisplay()
        self.show_display = False
    
    def fetch_positions_from_file(self):
        with open(self.file_location, 'r') as file:
            for line in file:
                if line != '':
                    line_without_new_line_character = line.rstrip()
                    position = get_position_from_storage_representation(line_without_new_line_character)
                    self.append_position_to_list(position)

    def get_position_indexed_from_one(self, index: int):
        position = self.positions[index - 1]
        return position
    
    def store_position(self, position: MousePosition):
        self.append_position_to_list(position)
        self.append_position_to_file(position)
        self.update_display_if_shown()
    
    def append_position_to_list(self, position: MousePosition):
        if position not in self.positions:
            self.positions.append(position)
    
    def append_position_to_file(self, position: MousePosition):
        with open(self.file_location, 'a') as file:
            representation = get_position_storage_representation(position)
            file.write(representation + '\n')
    
    def clear_positions(self):
        pass

    def get_positions(self):
        return self.positions

    def display_positions(self):
        self.show_display = True
        self.display.setup()
        self.display.show(self.positions)
    
    def update_display_if_shown(self):
        if self.show_display:
            self.display_positions()
    
    def hide_display(self):
        self.display.hide()
        self.show_display = False 


def get_position_storage_representation(position: MousePosition) -> str:
    representation = f'{position.get_horizontal()} {position.get_vertical()}'
    return representation

def get_position_from_storage_representation(representation: str) -> MousePosition:
    coordinates = representation.split(' ')
    horizontal = int(coordinates[0])
    vertical = int(coordinates[1])
    position = MousePosition(horizontal, vertical)
    return position

def compute_data_filepath(file_name: str):
    project_directory = os.path.dirname(os.path.realpath(__file__))
    data_directory_name = 'data'
    filepath = os.path.join(project_directory, data_directory_name, file_name)
    return filepath

main_position_storage = IndexedPositionStorage(compute_data_filepath('positions.txt'))

def store_position_in_main_storage(position: MousePosition):
    main_position_storage.store_position(position)

def store_current_position_in_main_storage():
    current_position = MousePosition.current()
    store_position_in_main_storage(current_position)

def store_line_in_main_storage(origin: MousePosition, destination: MousePosition):
    store_position_in_main_storage(origin)
    position_sum = origin + destination
    position_average = MousePosition(position_sum.get_horizontal()//2, position_sum.get_vertical()//2)
    store_position_in_main_storage(position_average)
    store_position_in_main_storage(destination)

@module.action_class
class Actions:
    def diagram_drawing_move_mouse_to_position(position_number: int):
        ''''''
        position = main_position_storage.get_position_indexed_from_one(position_number)
        position.go()
    
    def diagram_drawing_show_numbering():
        ''''''
        main_position_storage.display_positions()
    
    def diagram_drawing_hide_numbering():
        ''''''
        main_position_storage.hide_display()
    
    def diagram_drawing_clear_numbering():
        ''''''
        message = "Are you sure that you would like to clear the current numbering?"
        def on_confirmation():
            main_position_storage.clear_positions()
        def on_disconfirmation():
            pass
        confirmation.request_confirmation(message, on_confirmation, on_disconfirmation)
