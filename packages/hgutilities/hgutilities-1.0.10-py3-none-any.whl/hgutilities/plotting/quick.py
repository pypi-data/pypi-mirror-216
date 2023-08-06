import os
from copy import deepcopy

from .. import defaults
from .figures import Figures
from .datatypes.line import Line as line
from .datatypes.lines import Lines as lines
from ..utils import readwrite

class Quick():

    def __init__(self, path_input, **kwargs):
        self.kwargs = kwargs
        defaults.kwargs(self, kwargs)
        self.path_input = deepcopy(path_input)
        self.process_path_input()

    def process_path_input(self):
        if isinstance(self.path_input, str):
            self.process_path_input_string()
        else:
            self.process_path_input_non_string()

    def process_path_input_string(self):
        if os.path.isdir(self.path_input):
            self.process_path_input_string_dir()
        else:
            self.process_path_input_string_non_dir()

    def process_path_input_string_dir(self):
        if self.one_line_per_plot:
            print("A")
            self.paths = [[os.path.join(self.path_input, path)] for path in os.listdir(self.path_input)]
        else:
            print("B")
            self.paths = [[os.path.join(self.path_input, path) for path in os.listdir(self.path_input)]]
        print(self.paths)

    def process_path_input_string_non_dir(self):
        if os.path.isfile(self.path_input):
            self.paths = [[self.path_input]]
        else:
            self.bad_path_exception(self.path_input)

    def bad_path_exception(self, path_input):
        message = (f"The following is not a valid path to a file or directory:\n"
                   f"{path_input}\n\n"
                   f"Original input:\n"
                   f"{self.path_input}")
        raise ValueError(message)

    def process_path_input_non_string(self):
        if hasattr(self.path_input, "__iter__"):
            self.process_path_input_iterable()
        else:
            self.non_iterable_non_string_exception(self.path_input)

    def process_path_input_iterable(self):
        if isinstance(self.path_input, dict):
            self.path_input = list(self.path_input.values())
        self.paths = [self.get_path(element) for element in self.path_input]
        self.ensure_two_dimensional_paths()

    def non_iterable_non_string_exception(self, path_input):
        message = (f"Input must be a string or iterable of strings\n"
                   f"Your input is of type {type(path_input)}")
        raise ValueError(message)

    def get_path(self, element):
        if isinstance(element, str):
            return self.get_path_string(element)
        else:
            return self.get_path_non_string(element)

    def get_path_string(self, element):
        if os.path.isdir(element):
            return [os.path.join(element, path) for path in os.path.listdir(element)]
        else:
            return self.get_path_string_non_dir(element)

    def get_path_string_non_dir(self, element):
        if self.one_line_per_plot:
            return [element]
        else:
            return element

    def get_path_non_string(self, element):
        if hasattr(element, "__iter__"):
            return self.get_path_non_string_iterable(element)
        else:
            return self.non_iterable_non_string_exception(element)

    def get_path_non_string_iterable(element):
        if isinstance(element, dict):
            element = list(element.values())
        return element

    def ensure_two_dimensional_paths(self):
        if not isinstance(self.paths, list):
            self.paths = [self.paths]
    
    def create_figures(self, **kwargs):
        lines_objects = [self.get_lines_obj(paths_list) for paths_list in self.paths]
        figures_obj = Figures(lines_objects, **kwargs)
        figures_obj.create_figures(**kwargs)

    def get_lines_obj(self, paths_list):
        line_objects = [self.get_line_obj(path) for path in paths_list]
        lines_obj = lines(line_objects, x_label=self.independent,
                          y_label=self.dependent, **self.kwargs)
        return lines_obj

    def get_line_obj(self, path):
        data_dict = readwrite.read_from_path(path)
        keys = list(data_dict.keys())
        x_values = self.get_x_values(data_dict, keys)
        y_values = self.get_y_values(data_dict, keys)
        line_obj = line(x_values, y_values)
        return line_obj

    def get_x_values(self, data_dict, keys):
        self.independent = keys[self.x]
        x_values = data_dict[self.independent][self.ignore_first:]
        return x_values

    def get_y_values(self, data_dict, keys):
        self.dependent = keys[self.y]
        y_values = data_dict[self.dependent][self.ignore_first:]
        return y_values
        
defaults.load(Quick)
