'''Bring Order Data Import (and preparation). 
Creates code cells for importing and cleaning data and markdown cell to describe the limitations
and requirements of data. After code cells displays "ready to analyse" button. After button is 
pressed displays text field and "ready" button. Empty text field is not accepted.'''
from ipywidgets import widgets
from IPython.display import display, clear_output
from ipywidgets import GridspecLayout


class Bodi:
    '''Creates code cells for importing data and markdown cell(s) to describe data limitations'''
    def __init__(self, boutils, bogui, start_analysis):
        """Class constructor
        """
        self.start_analysis = start_analysis
        self.boutils = boutils
        self.bogui = bogui
        self.cell_count = 0
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.data_name = self.bogui.create_input_field()
        self.data_description = self.bogui.create_text_area()
        self.add_cells_int = self.bogui.create_int_text()
        self.import_grid = self.data_import_grid()
        self.data_limitations = []
        self.limitation_grid = None
        self.empty_limitations_error = self.bogui.create_error_message()

    @property
    def button_list(self):
        """Buttons for Bodi class.

        Returns:
            list of tuples in format (description: str, command: func, style: str) """
        button_list = [
            ('Save description', self.start_data_import, 'success'),
            ('Open cells', self.open_cells, 'warning'),
            ('Delete last cell', self.delete_last_cell, 'danger'),
            ('Run cells', self.run_cells, 'primary'),
            ('Add limitation', self.add_limitation, 'primary'),
            ('Start analysis', self.start_analysis_clicked, 'success')
        ]

        return button_list

    def data_import_grid(self):
        """Creates widget grid"""
        cell_number_label = self.bogui.create_label(
            'Add code cells for data preparation:')

        grid = widgets.HBox([
            cell_number_label,
            self.add_cells_int,
            self.buttons['Open cells'],
            self.buttons['Run cells'],
            self.buttons['Delete last cell']
        ])

        return grid

    def open_cells(self, _=None):
        """Button function that opens selected number of cells above widget cell"""
        if self.add_cells_int.value > 0:
            self.cell_count += self.add_cells_int.value
            self.boutils.create_code_cells_above(self.add_cells_int.value)

    def delete_last_cell(self, _=None):
        """Button function to delete the last data import code cell"""
        if self.cell_count > 1:
            self.boutils.delete_cell_above()
            self.cell_count -= 1

    def run_cells(self, _=None):
        """Button function that runs data import cells"""
        self.boutils.run_cells_above(self.cell_count)

        if self.limitation_grid:
            self.limitation_grid.close()

        self.display_limitations()

    def add_limitation(self, _=None):
        """Button function to add new limitation"""
        if self.limitation_grid:
            self.limitation_grid.close()

        self.data_limitations.append(self.bogui.create_text_area('',f'Limitation {len(self.data_limitations)+1}'))

        self.display_limitations()

    def display_limitations(self):
        """Shows text boxes and buttons for adding limitations"""
        limitations_label = self.bogui.create_message(
                value='Identify limitations to the data: what kind of questions cannot be answered with it?')

        rows = len(self.data_limitations)
        if rows == 0:
            self.data_limitations.append(self.bogui.create_text_area('', 'Limitation 1'))
            rows +=1

        grid = GridspecLayout(rows, 1)

        for i in range(rows):
            for j in range(1):
                grid[i, j] = self.data_limitations[i]

        self.limitation_grid = widgets.AppLayout(
            header=limitations_label,
            center=grid,
            footer=widgets.HBox([
                self.buttons['Start analysis'],
                self.empty_limitations_error,
                self.buttons['Add limitation']
            ])
        )

        display(self.limitation_grid)

    def check_limitations(self, item=''):
        """Checks that limitations have been given or commented"""
        if item == '':
            return False
        return True

    def call_check_limitation(self):
        """Checks that none of the limitations is empty"""
        for limitation in self.data_limitations:
            if not self.check_limitations(limitation.value):
                return False
        return True

    def format_limitations(self):
        """Formats limitations for markdown to prevent Javascript error
        
        Returns:
            formatted_limitations (str)
        """

        formatted_limitations = '## Limitations\\n'
        for item in self.data_limitations:
            limitation = '<br />'.join(item.value.split('\n'))
            limitation_text = f'- {limitation}\\n'
            formatted_limitations += limitation_text

        return formatted_limitations

    def start_analysis_clicked(self, _=None):
        """Button function to start analysis after data preparation"""
        if self.call_check_limitation():
            text = self.format_limitations()
            self.boutils.create_markdown_cells_above(1, text=text)
            clear_output(wait=True)
            self.start_analysis()
        else:
            self.empty_limitations_error.value = 'Data limitations cannot be empty'

    def format_data_description(self):
        """Formats data description for markdown
        
        Returns:
            formatted_text (str)
        """
        title = f'# Data: {self.data_name.value}'
        description = '<br />'.join(self.data_description.value.split('\n'))
        formatted_text = f'{title}\\n## Description\\n{description}\\n## Import and cleaning'

        return formatted_text

    def start_data_import(self, _=None):
        """Creates markdown for data description and shows buttons for data import"""
        if self.data_name.value == '':
            self.bodi(error='You must name the data set')
        elif self.data_description.value == '':
            self.bodi(error='You must give some description of the data')

        else:
            self.boutils.hide_current_input()
            clear_output(wait=True)
            display(self.import_grid)

            self.boutils.create_markdown_cells_above(1, text=self.format_data_description())
            self.cell_count += 1

    def bodi(self, error=''):
        """Main function"""
        clear_output(wait=True)

        title = self.bogui.create_message('What kind of data are you using?')
        data_title_label = self.bogui.create_label('Name of the data set:')
        description_label = self.bogui.create_label('Description of the data:')
        error_message = self.bogui.create_error_message(error)

        grid = widgets.AppLayout(
            header=title,
            left_sidebar=widgets.VBox([
                data_title_label,
                description_label
            ]),
            center=widgets.VBox([
                    self.data_name,
                    self.data_description
            ]),
            footer=widgets.HBox([
                self.buttons['Save description'],
                error_message,
            ]),
            pane_widths=[1, 5, 0],
            grid_gap='10px'
        )

        display(grid)

        if 'description' in error:
            self.data_description.focus()
        else:
            self.data_name.focus()
