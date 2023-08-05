"""Class for Inductive analysis"""
from ipywidgets import widgets
from IPython.display import display, clear_output, Javascript

class Inductive:
    """Class that guides inductive analysis"""
    def __init__(self, bogui, boutils, start_new):
        """Class constructor."""
        self.bogui = bogui
        self.utils = boutils
        self.start_new = start_new
        self.cell_count = 0
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.add_cells_int = self.bogui.create_int_text()
        self.notes = self.bogui.create_text_area()
        self.conclusion = None
        self.summary = self.bogui.create_text_area()
        self.empty_notes_error = self.bogui.create_error_message()
        self.observations = []
        self.new_analysis_view = widgets.HBox([
            self.buttons['New analysis'],
            self.buttons['Prepare new data'],
            self.buttons['All done']]
        )
        self.export_view = widgets.HBox([self.buttons['Export to pdf'],
                                         self.buttons['Close BringOrder']])

    @property
    def button_list(self):
        """Buttons for Inductive class.

        Returns:
            list of tuples in format (description: str, command: func, style: str) """
        button_list = [('Open cells', self.open_cells, 'warning'),
                   ('Delete last cell', self.delete_last_cell, 'danger'),
                   ('Clear cells', self.clear_cells, 'danger'),
                   ('Run cells', self.run_cells, 'primary'),
                   ('New analysis', self.start_new_analysis, 'success'),
                   ('Ready to summarize', self.execute_ready, 'primary'),
                   ('Submit observation', self.new_observation, 'warning'),
                   ('Submit summary', self.submit_summary, 'success'),
                   ('Prepare new data', self.prepare_new_data_pressed, 'success'),
                   ('All done', self.all_done, 'success'),
                   ('Export to pdf', self.export_to_pdf, 'success'),
                   ('Close BringOrder', self.no_export, 'success')]

        return button_list

    def open_cells(self, _=None):
        """Open cells button function that opens the selected
        number of code cells"""
        if self.add_cells_int.value > 0:
            self.cell_count += self.add_cells_int.value
            self.utils.create_code_cells_above(self.add_cells_int.value)

    def delete_last_cell(self, _=None):
        """Delete last cell-button function"""
        if self.cell_count > 0:
            self.utils.delete_cell_above()
            self.cell_count -= 1

    def clear_cells(self, _=None):
        """Clears all code cells above."""
        self.utils.clear_code_cells_above(self.cell_count)

    def buttons_disabled(self, disabled):
        """Activates/deactivates buttons
        
        Args:
            disbled (bool): True to disable, False to activate
        """

        self.buttons['Open cells'].disabled = disabled
        self.buttons['Clear cells'].disabled = disabled
        self.buttons['Delete last cell'].disabled = disabled
        self.buttons['Ready to summarize'].disabled = disabled

    def run_cells(self, _=None):
        """Executes cells above and displays text area for observations of analysis."""
        if self.cell_count == 0:
            return

        self.utils.run_cells_above(self.cell_count)
        if self.conclusion:
            self.conclusion.close()

        self.buttons_disabled(True)

        notes_label = self.bogui.create_label(value='Explain what you observed:')
        self.conclusion = widgets.VBox([
            widgets.HBox([notes_label, self.notes]),
            self.empty_notes_error,
            self.buttons['Submit observation']
        ])

        display(self.conclusion)

    def get_first_words(self, word_list):
        """Takes a word list and returns a string that has the first sentence or
        the first five words and three dots if the sentence is longer.
        
        Args:
            word_list (list)
            
        Returns:
            first_words (str)
        """
        first_words = f'{word_list[0]}'

        for word in word_list[1:5]:
            first_words += f' {word}'
            if any(mark in word for mark in ['.', '?', '!']):
                return first_words.strip('.')

        first_words.strip('.').strip(',')
        if len(word_list) > 5:
            first_words += '...'

        return first_words

    def format_observation(self):
        """Formats observation for markdown.
        
        Returns:
            formatted_obs (str)
        """
        formatted_obs = f'## Observation {len(self.observations)}: '

        notes_list = self.notes.value.split('\n')
        first_line_list = notes_list[0].split(' ')
        first_words = self.get_first_words(first_line_list)
        formatted_obs += f'{first_words}\\n'

        notes = '<br />'.join(notes_list)
        formatted_obs += notes

        return formatted_obs

    def new_observation(self, _=None):
        """Checks new observation, saves it, and resets cell count"""
        if self.check_notes():
            self.observations.append(self.notes.value)
            text = self.format_observation()
            self.utils.create_markdown_cells_above(1, text=text)
            self.buttons_disabled(False)
            self.empty_notes_error.value = ''
            self.conclusion.close()
            self.notes.value = ''
            self.cell_count = 0

        else:
            self.empty_notes_error.value = 'Observation field can not be empty'

    def start_new_analysis(self, _=None):
        """Starts new bringorder object with old data"""
        clear_output(wait=True)
        self.start_new()

    def prepare_new_data_pressed(self, _=None):
        '''Starts new analysis with importing new data'''
        self.utils.execute_cell_from_current(0, 'BringOrder()')

    def execute_ready(self, _=None):
        """Executes code cells after Get summary button is clicked."""
        clear_output(wait=True)
        self.display_summary()

    def display_summary(self, error=''):
        """Prints all observations and asks for summary"""
        clear_output(wait=True)

        observations = "<ul>\n"
        observations += "\n".join(["<li>" + observation + "</li>" for observation in self.observations])
        observations += "\n</ul>"

        observation_list = widgets.HTML(
            '</br>'+'<h4>All your observations from the data:</h4>'+observations)

        # observation_string = '\n'.join((f"Observation {i+1}: {observation}\n") for i, observation
        #          in enumerate(self.observations))
        # text = f'All your observations from the data:\n\n{observation_string}'
        # print(text)

        summary_label = self.bogui.create_label('What do these observations mean?')
        error_message = self.bogui.create_error_message(value=error)
        grid = widgets.VBox([
            observation_list,
            widgets.HBox([summary_label, self.summary]),
            error_message,
            self.buttons['Submit summary']
        ])
        display(grid)

    def format_summary(self):
        """Formats summary for markdown
        
        Returns:
            formatted_summary (str)
        """
        formatted_summary = '## Summary: '

        summary_list = self.summary.value.split('\n')
        first_line_list = summary_list[0].split(' ')
        first_words = self.get_first_words(first_line_list)
        formatted_summary += f'{first_words}\\n'

        summary = '<br />'.join(summary_list)
        formatted_summary += summary

        return formatted_summary

    def submit_summary(self, _=None):
        """Button function to submit summary"""
        if self.summary.value == '':
            self.display_summary(error='You must write some kind of summary')
            return

        text = self.format_summary()
        self.utils.create_markdown_cells_above(1, text=text)
        clear_output(wait=False)
        self.new_analysis()

    def check_notes(self):
        """Checks that text field was filled"""
        if self.notes.value == '':
            return False
        return True

    def create_cell_operations(self):
        """Displays buttons for operations in inductive analysis"""
        self.buttons['Ready to summarize'].disabled = True
        cell_number_label = self.bogui.create_label('Add code cells for your analysis:')

        cell_buttons = widgets.TwoByTwoLayout(
            top_left=self.buttons['Open cells'],
            bottom_left=self.buttons['Run cells'],
            top_right=self.buttons['Delete last cell'],
            bottom_right=self.buttons['Clear cells']
        )

        grid = widgets.GridspecLayout(2, 3, height='auto', width='100%')
        grid[0, 0] = widgets.HBox([cell_number_label, self.add_cells_int])
        grid[:, 1] = cell_buttons
        grid[1, 2] = self.buttons['Ready to summarize']

        return grid

    def start_inductive_analysis(self):
        """Starts inductive analysis"""
        self.utils.create_markdown_cells_above(1, '# Inductive analysis')
        display(self.create_cell_operations())

    def all_done(self, _=None):
        """Button function to display the export/close phase."""
        #self.boutils.delete_cell_from_current(1)
        self.new_analysis_view.close()
        display(self.export_view)

    def export_to_pdf(self, _=None):
        """Button function to export the notebook to pdf."""
        #os.system('jupyter nbconvert Untitled.ipynb --to pdf')
        self.export_view.close()
        display(Javascript('print()'))
        self.utils.delete_cell_from_current(0)

    def no_export(self, _=None):
        """Button function to close widgets without exporting."""
        self.utils.delete_cell_from_current(0)

    def new_analysis(self):
        """Display buttons to start a new analysis or prepare new data for analysis"""
        display(self.new_analysis_view)

    def __repr__(self):
        return ''
