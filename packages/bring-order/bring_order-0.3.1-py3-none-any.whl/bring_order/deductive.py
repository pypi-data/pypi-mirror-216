"""Deductive class"""
from ipywidgets import widgets
from IPython.display import display, Javascript, clear_output

class Deductive:
    """Class that guides deductive analysis"""
    def __init__(self, bogui, boutils, start_new):
        """Class constructor
        
        Args:
            bogui (BOGui)
            boutils (BOUtils)
            start_new (function): Function to start new analysis with same data
        """
        self.cell_count = 0
        self.start_new = start_new
        self.bogui = bogui
        self.boutils = boutils
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.theory_desc = self.bogui.create_text_area()
        #List of hypotheses: 0 = hypothesis, 1 = null hypothesis
        self.hypotheses = [
            self.bogui.create_input_field(),
            self.bogui.create_input_field()
        ]
        self.add_cells_int = self.bogui.create_int_text()
        self.conclusion = None
        self.data_limitations = ['Data limitations missing']
        self.result_description = self.bogui.create_text_area()

    @property
    def button_list(self):
        """Buttons for deductive class.

        Returns:
            list of tuples in format (description: str, command: func, style: str)"""
        button_list = [('Open cells', self.open_cells, 'primary'),
                       ('Delete last cell', self.delete_last_cell, 'danger'),
                       ('Save', self.check_theory_and_hypotheses, 'success'),
                       ('Clear hypotheses', self.clear_hypotheses, 'warning'),
                       ('Yes', self.save_theory_and_hypotheses, 'success'),
                       ('No', self.bad_hypotheses, 'warning'),
                       ('Run cells', self.run_cells, 'warning'),
                       ('Clear cells', self.clear_cells, 'danger'),
                       ('New analysis', self.start_new_analysis, 'success'),
                       ('Prepare new data', self.start_analysis_with_new_data, 'success'),
                       ('All done', self.all_done, 'success'),
                       ('Export to pdf', self.export_to_pdf, 'success'),
                       ('Close BringOrder', self.no_export, 'success'),
                       ('Clear theory', self.clear_theory, 'warning')]

        return button_list

    def __create_hypotheses_grid(self, empty_hypo_error='', empty_null_error=''):
        """Creates the view for setting hypotheses
        
        Args:
            empty_hypo_error (str): error message for empty hypothesis, optional
            empty_null_error (str): error message for empty null hypothesis, optional
        """
        grid = widgets.AppLayout(
            header = self.bogui.create_message('Set the hypotheses:'),
            left_sidebar = widgets.VBox([
                self.bogui.create_label('Hypothesis (H1):'),
                self.bogui.create_label('Null hypothesis (H0):')
            ]),
            center = widgets.VBox([
                widgets.HBox([
                    self.hypotheses[0],
                    self.bogui.create_error_message(empty_hypo_error)
                ]),
                widgets.HBox([
                    self.hypotheses[1],
                    self.bogui.create_error_message(empty_null_error)
                ]),
                self.buttons['Clear hypotheses']
            ]),
            footer = self.buttons['Save'],
            pane_widths = [1, 6, 0],
            grid_gap = '18px'
        )

        return grid

    def __create_theory_grid(self, error=''):
        """Creates the view for summarizing theory
        
        Args:
            error (str): error message, optional
        """
        grid = widgets.AppLayout(
            header=self.bogui.create_message('Describe the theory and insights:'),
            center=widgets.VBox([
                self.theory_desc,
                self.bogui.create_error_message(error),
                self.buttons['Clear theory']
            ]),
            pane_widths=[1, 6, 0],
            grid_gap='12px'
        )

        return grid

    def start_deductive_analysis(self, _=None):
        """Button function for deductive analysis"""
        theory_grid = self.__create_theory_grid()
        hypotheses_grid = self.__create_hypotheses_grid()

        clear_output(wait=True)
        display(theory_grid)
        display(hypotheses_grid)
        self.theory_desc.focus()

    def clear_theory(self, _=None):
        """Function for clearing theory and insights"""
        self.theory_desc.value = ''
        self.theory_desc.focus()

    def focus_first_empty(self, input_list):
        """Sets focus to the first widget on the list that has empty value
        
        Args:
            input_list (list): list of input widgets

        Retruns:
            item (widget): the item that was focused (or None if no empty item on the list)
        """
        focused = None
        for item in input_list:
            if item.value == '':
                item.focus()
                focused = item
                break

        return focused

    def get_error_messages(self):
        """Returns error messages for empty theory, hypothesis, and null hypothesis
        
        Returns:
            errors (tuple)
        """
        empty_theory = 'You must describe your theory and insights'
        empty_hypo = 'Hypothesis missing'
        empty_null = 'Null hypothesis missing'

        theory_error = empty_theory if self.theory_desc.value == '' else ''
        empty_hypo_error = empty_hypo if self.hypotheses[0].value == '' else ''
        empty_null_error = empty_null if self.hypotheses[1].value == '' else ''

        return (theory_error, empty_hypo_error, empty_null_error)

    def __create_limitation_prompt(self):
        """Creates limitation prompt grid"""
       
        hypothesis_text = self.bogui.create_message(
            f'You have set hypothesis (H1): {self.hypotheses[0].value}'
        )
        null_text = self.bogui.create_message(
            f'You have set null hypothesis (H0): {self.hypotheses[1].value}'
        )

        limitations = "<ul>\n"
        limitations += "\n".join(["<li>" + limitation.value + "</li>" for limitation in self.data_limitations])
        limitations += "\n</ul>"

        limitation_prompt_text = widgets.HTML(
            '</br>'+ '<h4> Do the hypotheses fit within the limitations of the data set? </h4>' 
             + limitations)

        limitation_prompt = widgets.VBox([
            hypothesis_text,
            null_text,
            limitation_prompt_text,
            widgets.HBox([self.buttons['Yes'], self.buttons['No']])
        ])

        return limitation_prompt

    def check_theory_and_hypotheses(self, _=None):
        """Checks theory and hypotheses and displays the prompt for
        the check against data limitations
        
        Returns:
            True/False: True if theory, hypothesis, and null hypothesis are all filled
        """

        # Set error messages
        theory_error, empty_hypo_error, empty_null_error = self.get_error_messages()
        theory_grid = self.__create_theory_grid(theory_error)
        hypotheses_grid = self.__create_hypotheses_grid(empty_hypo_error, empty_null_error)

        # Show error messages if any of the required values are empty
        if len(theory_error + empty_hypo_error + empty_null_error) > 0:
            clear_output(wait=True)
            display(theory_grid)
            display(hypotheses_grid)
            self.focus_first_empty([self.theory_desc] + self.hypotheses)

            return False

        # Show limitation prompt if all values are ok
        limitation_prompt = self.__create_limitation_prompt()
        clear_output(wait=True)
        display(limitation_prompt)

        return True

    def bad_hypotheses(self, _=None):
        """Closes the data limitation check prompt and calls clear_hypotheses()"""
        theory_grid = self.__create_theory_grid()
        hypotheses_grid = self.__create_hypotheses_grid('Hypotheses must fit data limitations')
        clear_output(wait=True)
        display(theory_grid)
        display(hypotheses_grid)
        self.clear_hypotheses()

    def format_hypotheses_and_theory(self):
        """Formats hypotheses and theory for markdown
        
        Returns:
            formatted_text (str)
        """
        formatted_text = f'# Deductive analysis: {self.hypotheses[0].value}\\n'
        formatted_theory = '<br />'.join(self.theory_desc.value.split('\n'))
        formatted_text += f'## Theory and insights\\n{formatted_theory}\\n'
        hypotheses = f'- Hypothesis (H1): {self.hypotheses[0].value}\
        \\n- Null hypothesis (H0): {self.hypotheses[1].value}'
        formatted_text += f'## Hypotheses\\n{hypotheses}\\n## Data analysis'

        return formatted_text

    def save_theory_and_hypotheses(self, _=None):
        """Saves theory and hypotheses and displays buttons for running code"""
        text = self.format_hypotheses_and_theory()
        self.boutils.create_markdown_cells_above(1, text=text)
        cell_operations = self.__create_cell_operations_grid()
        clear_output(wait=True)
        display(cell_operations)
        self.add_cells_int.focus()

    def clear_hypotheses(self, _=None):
        """Button function for resetting hypothesis and null hypothesis inputs"""
        self.hypotheses[0].value = ''
        self.hypotheses[1].value = ''
        self.hypotheses[0].focus()

    def open_cells(self, _=None):
        """Button function for opening new code cells"""
        if self.add_cells_int.value > 0:
            self.cell_count += self.add_cells_int.value
            self.boutils.create_code_cells_above(self.add_cells_int.value)

    def delete_last_cell(self, _=None):
        """Button function for deleting the last code cell"""
        if self.cell_count > 0:
            self.boutils.delete_cell_above()
            self.cell_count -= 1

    def deactivate_cell_operations(self):
        """Deactivates buttons after runnig code block"""
        self.buttons['Open cells'].disabled = True
        self.buttons['Clear cells'].disabled = True
        self.buttons['Delete last cell'].disabled = True

    def __create_conclusion_grid(self):
        question = self.bogui.create_message(value='What happened?')
        conclusion_label = self.bogui.create_message(value='Accepted hypothesis:')
        self.conclusion = self.bogui.create_radiobuttons(
            options=[f'H1: {self.hypotheses[0].value}',
                     f'H0: {self.hypotheses[1].value}'])
        notes_label = self.bogui.create_message(value='Describe your results here:')

        grid = widgets.AppLayout(
            header=question,
            left_sidebar=conclusion_label,
            center=self.conclusion,
            footer=widgets.VBox([
                notes_label,
                self.result_description,
                widgets.HBox([
                    self.buttons['New analysis'],
                    self.buttons['Prepare new data'],
                    self.buttons['All done']
                ])
            ]),
            pane_widths=[1, 5, 0],
            pane_heights=['20px', '40px', 1],
            grid_gap='12px'
        )

        return grid

    def run_cells(self, _=None):
        """Runs code cells, deactivates cell operations, and shows radiobuttons"""
        self.boutils.run_cells_above(
            self.cell_count)
        self.deactivate_cell_operations()

        clear_output(wait=True)
        cell_operations = self.__create_cell_operations_grid()
        conclusion = self.__create_conclusion_grid()
        display(cell_operations)
        display(conclusion)
        conclusion.focus()

    def clear_cells(self, _=None):
        """Clear button function to clear cells above"""
        self.boutils.clear_code_cells_above(self.cell_count)

    def __create_cell_operations_grid(self):
        """Creates widget grid"""
        cell_number_label = self.bogui.create_label('Add code cells for your analysis:')

        grid = widgets.GridspecLayout(2, 2, justify_items='center', width='70%', align_items='center')
        grid[1, 0] = widgets.HBox([cell_number_label, self.add_cells_int])
        grid[1, 1] = widgets.TwoByTwoLayout(
            top_left=self.buttons['Open cells'],
            bottom_left=self.buttons['Run cells'],
            top_right=self.buttons['Delete last cell'],
            bottom_right=self.buttons['Clear cells'])

        return grid

    def save_results(self):
        """Prints results as markdown and hides widgets"""
        
        text = (f'## Conclusion\\n### Accepted hypothesis: {self.conclusion.value[4:]}\\n'
                f'The hypotheses were:\\n- Hypothesis (H1): {self.hypotheses[0].value}\\n'
                f'- Null hypothesis (H0): {self.hypotheses[1].value}\\n')
        
        if self.result_description.value:
            formatted_description = '<br />'.join(self.result_description.value.split('\n'))
            text += f'### Notes\\n {formatted_description}'
        
        self.boutils.create_markdown_cells_above(1, text=text)
        clear_output(wait=True)

    def start_new_analysis(self, _=None):
        """Button function to save results and star new analysis"""
        self.save_results()
        self.start_new()

    def start_analysis_with_new_data(self, _=None):
        """Button function to start over with new data"""
        self.save_results()
        self.boutils.execute_cell_from_current(1, 'BringOrder()')

    def all_done(self, _=None):
        """Button function to save results when ready."""
        self.save_results()
        export_view = widgets.HBox([
            self.buttons['Export to pdf'],
            self.buttons['Close BringOrder']
        ])
        display(export_view)

    def export_to_pdf(self, _=None):
        """Button function to export the notebook to pdf."""
        #os.system('jupyter nbconvert Untitled.ipynb --to pdf')
        clear_output(wait=False)
        display(Javascript('print()'))
        self.boutils.delete_cell_from_current(0)

    def no_export(self, _=None):
        """Button function to close widgets without exporting."""
        self.boutils.delete_cell_from_current(0)

    def __repr__(self):
        return ''
