"""Helpful Javascript methods"""
from IPython.display import display, Javascript


class BOUtils:
    """Helpful Javascript methods"""
    def __init__(self):
        """Class constructor"""

    def create_code_cells_above(self, how_many):
        """Creates code cells above the current cell
        
        Args:
            how_many (int): the number of cells to be created
        """
        for _ in range(how_many):
            command = 'IPython.notebook.insert_cell_above("code")'
            display(Javascript(command))

    def create_markdown_cells_above(self, how_many, text='', run_cell=True):
        """Creates markdown cells above the current cell
        
        Args:
            how_many (int): the number of cells to be created
            text (str): default contents of the created cells
            run_cell (bool): should the cell be run after creation
        """
        if run_cell:
            run_cell_str = 'true'
        else:
            run_cell_str = 'false'

        for _ in range(how_many):
            command = f'''
                var cell = IPython.notebook.insert_cell_above("markdown");
                cell.set_text("{text}");
                if ({run_cell_str}) {{
                    var new_index = IPython.notebook.get_selected_index()-1;
                    IPython.notebook.execute_cells([new_index]);
                }}
            '''
            display(Javascript(command))

    def clear_code_cells_above(self, how_many):
        """Clears code cells above the active cell
        
        Args:
            how_many (int): the number of cells to be cleared
        """
        for _ in range(how_many):
            self.delete_cell_above()
        self.create_code_cells_above(how_many)

    def create_code_cells_below(self, how_many):
        """Creates the given number of code cells below the current cell"""
        for _ in range(how_many):
            command = 'IPython.notebook.insert_cell_below("code")'
            display(Javascript(command))

    def create_markdown_cells_below(self, how_many):
        """Creates the given number of code cells below the current cell"""
        for _ in range(how_many):
            command = 'IPython.notebook.insert_cell_below("markdown")'
            display(Javascript(command))

    def create_code_cells_at_bottom(self, how_many):
        """Creates the given number of code cells at the bottom of notebook"""
        for _ in range(how_many):
            command = 'IPython.notebook.insert_cell_at_bottom("code")'
            display(Javascript(command))

    def create_markdown_cells_at_bottom(self, how_many, text=''):
        """Creates the given number of markdown cells at the bottom of notebook
        
        Args:
            how_many (int): the number of cells to be opened
            text (str): default text to be shown in the new cells
        """
        for _ in range(how_many):
            command = f'''
            var cell = IPython.notebook.insert_cell_at_bottom("markdown");
            cell.set_text("{text}");
            '''
            display(Javascript(command))

    def create_code_and_observation_cells(self, how_many):
        """Creates new code and markdown cells on top of each other.
        
        Args:
            how_many (int): the number of cell pairs to be opened
        """
        for _ in range(how_many):
            command = '''
            IPython.notebook.insert_cell_at_bottom("code");
            var markdown = IPython.notebook.insert_cell_at_bottom("markdown");
            markdown.set_text("### Observations");
            '''
            display(Javascript(command))

    def clear_code_and_observation_cells(self, how_many):
        """Clears the given number of code and observation cells below the active cell"""
        command = f'''
        var first_cell = IPython.notebook.get_selected_index() + 1;
        var cells = IPython.notebook.get_cells().reverse();
        cells.forEach(function(cell) {{
                var index = IPython.notebook.find_cell_index(cell);
                if(index >= first_cell && index < first_cell + {how_many}) {{
                    IPython.notebook.delete_cell(index);
                }}
        }});
        '''
        display(Javascript(command))

        self.create_code_and_observation_cells(how_many//2)

    def clear_code_cells_below(self, how_many):
        """Clears the given number of code cells below the active cell"""
        command = f'''
        var first_cell = IPython.notebook.get_selected_index() + 1;
        var cells = IPython.notebook.get_cells().reverse();
        cells.forEach(function(cell) {{
                var index = IPython.notebook.find_cell_index(cell);
                if(index >= first_cell && index < first_cell + {how_many}) {{
                    IPython.notebook.delete_cell(index);
                }}
        }});
        '''
        display(Javascript(command))
        self.create_code_cells_at_bottom(how_many)

    def delete_cell_above(self):
        """Deletes the cell above the current cell"""
        command = '''
        var above_index = IPython.notebook.get_selected_index() - 1;
        IPython.notebook.delete_cell(above_index);
        '''
        display(Javascript(command))

    # Refactoring note: delete_cell_above could be deleted
    # and delete_cell_from_current could be used instead with distance=-1
    # This can also replace delete_cell with distance=cell_count
    # if that method is still needed after inductive has been changed to cells above version
    def delete_cell_from_current(self, distance):
        """Deletes a cell that has the index of the active cell index + distance
        
        Args:
            distance (int): target cell index with respect to active cell
        """
        command = f'''
        var index = IPython.notebook.get_selected_index() + {distance};
        IPython.notebook.delete_cell(index);
        '''
        display(Javascript(command))

    def delete_cell(self, cell_count):
        """Deletes the last analysis cell"""
        command = f'''
        var first_index = IPython.notebook.get_selected_index();
        var last_index = first_index + {cell_count};
        const cells = IPython.notebook.get_cells();
        IPython.notebook.delete_cell(last_index);
        '''
        display(Javascript(command))

    def run_cells_above(self, cell_count):
        """Runs cells above the active cell.
        
        Args:
            cell_count (int): the number of cells to be run
        """

        command = f'''
        var current_index = IPython.notebook.get_selected_index();
        var first_index = current_index - {cell_count};
        IPython.notebook.execute_cell_range(first_index, current_index);
        '''
        display(Javascript(command))

    def run_cells(self, cell_count):
        """Runs cells below the active cell.
        
        Args:
            cell_count (int): the number of cells to be run
        """
        command = f'''
        var first_index = IPython.notebook.get_selected_index() + 1;
        var last_index = first_index + {cell_count};
        IPython.notebook.execute_cell_range(first_index, last_index);
        '''
        display(Javascript(command))

    def create_and_execute_code_cell(self, code='', hide_input=True):
        """Creates a new cell at the bottom with given code and runs it.
        
        Args:
            code (str): Python code to be executed
            hide_input (boolean): hides input of the executed cell, defaults to True 
        """
        if hide_input:
            hide_input_string = 'true'
        else:
            hide_input_string = 'false'
        command = f'''
        var code = IPython.notebook.insert_cell_at_bottom("code");
        code.set_text('{code}');
        Jupyter.notebook.execute_cells([-1]);
        if ({hide_input_string}) (code.input.hide());
        '''
        display(Javascript(command))

    def execute_cell_from_current(self, distance, code='', hide_input=True):
        """Executes code in cell that has the index of the active cell index + distance
        
        Args:
            distance (int): target cell index with respect to active cell
            code (str): Python code to be executed
            hide_input (boolean): hides input of the executed cell, defaults to True 
        """
        if hide_input:
            hide_input_string = 'true'
        else:
            hide_input_string = 'false'
        command = f'''
        var index = IPython.notebook.get_selected_index() + {distance};
        var cell = IPython.notebook.get_cell(index);
        cell.set_text("{code}");
        IPython.notebook.execute_cells([index]);
        if ({hide_input_string}) (cell.input.hide());
        '''
        display(Javascript(command))

    def hide_current_input(self):
        """Hides the input of current cell"""
        command = '''
        var cell_index = IPython.notebook.get_selected_index();
        var cells = IPython.notebook.get_cells();
        cells[cell_index].input.hide();
        '''
        display(Javascript(command))
