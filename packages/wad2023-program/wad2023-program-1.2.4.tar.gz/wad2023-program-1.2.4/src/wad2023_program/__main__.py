"""Main module.

Contains the main script for the WAD2023 applican.
"""

from enum import Enum

import typer
from rich import box
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel

from .program import get_program


class SortField(str, Enum):
    """The field to sort on.

    Specifies the field to sort on.

    Attributes:
        START_TIME: sort on the start time.
        END_TIME: sort on the end time.
        TITLE: sort on the title.
        SPEAKER: sort on the speakername.
        STAGE_NAME: sort on the stagename.
    """

    START_TIME = 'start'
    END_TIME = 'end'
    TITLE = 'title'
    SPEAKER = 'speaker'
    STAGE_NAME = 'stage'

    @property
    def field_name(self) -> str:
        """Return the name of the field.

        We have to add a underscore to the attributes so we can use the `title`
        attribute. This method returns the normalized name.

        Returns:
            The normalized name.
        """
        return self.name.lower()


class DataOutput(str, Enum):
    """Output specification.

    Specifies how to output data.

    Attributes:
        TABLE: display as table.
        CSV: display as CSV.
    """

    TABLE = 'table'
    CSV = 'csv'
    DETAILS = 'details'


def start(
        sort: SortField = SortField.START_TIME,
        in_title: str = '',
        in_speaker: str = '',
        in_description: str = '',
        find: str = '',
        stage: str = '',
        output: DataOutput = DataOutput.TABLE,
        cache: bool = True
) -> None:
    """Script function for the program.

    The function that gets called when starting the script.

    Args:
        sort: the field on what to sort.
        in_title: filter on words in the title.
        in_speaker: filter on words in the speakers.
        in_description: filter on words in the description.
        find: filter on words in the description _or_ in the title.
        stage: specify a specific stage.
        output: specifies what kind of output the user wants.
        cache: specifies if the cache has to be used.
    """
    # Get the program
    program = get_program(cache=cache)

    # Sort the program. We always sort on start time first, before sorting on
    # the column given by the user
    program.sort(key=lambda x: x.start_time)
    program.sort(key=lambda x: getattr(x, sort.field_name))

    # Filter
    if len(in_title) > 0:
        program = list(filter(lambda session: in_title.lower()
                              in session.title.lower(), program))
    if len(in_speaker) > 0:
        program = list(filter(lambda session: in_speaker.lower()
                              in session.speaker.lower(), program))
    if len(in_description) > 0:
        program = list(filter(lambda session: in_description.lower()
                              in session.description.lower(), program))
    if len(find) > 0:
        program = list(filter(lambda session:
                              find.lower() in session.description.lower() or
                              find.lower() in session.title.lower(),
                              program))
    if len(stage) > 0:
        program = list(filter(lambda session:
                              session.stage_name.lower() == stage.lower(),
                              program))

    # Create a Rich console for a beautiful display
    console = Console()

    # Create a table to display the program
    if output == DataOutput.TABLE:
        table = Table(box=box.HORIZONTALS)
        table.add_column('Date')
        table.add_column('Start')
        table.add_column('End')
        table.add_column('Stage')
        table.add_column('Title')
        table.add_column('Speakers')

        # Add the rows
        for item in program:
            table.add_row(
                f'{item.start_time_berlin:%Y-%m-%d}',
                f'{item.start_time_berlin:%H:%M}',
                f'{item.end_time_berlin:%H:%M}',
                item.stage_name,
                item.title,
                item.speaker
            )

        # Show the nice table
        console.print(table)

    if output == DataOutput.CSV:
        print(
            '"Date";"Start";"End";"Stage";"Title";"Description";"Speakers"')
        for item in program:
            description = item.description.replace('"', '\\"')
            print(
                f'"{item.start_time_berlin:%Y-%m-%d}";' +
                f'"{item.start_time_berlin:%H:%M:%S}";' +
                f'"{item.end_time_berlin:%H:%M:%S}";' +
                f'"{item.stage_name}";' +
                f'"{item.title}";' +
                f'"{description}";' +
                f'"{item.speaker}"')

    if output == DataOutput.DETAILS:
        for item in program:
            table = Table(box=box.MINIMAL, show_header=False)
            table.add_column('Field')
            table.add_column('Information')
            table.add_row('Title', item.title)
            table.add_row(
                'Date', (f'{item.start_time_berlin:%Y-%m-%d} ' +
                         f'({item.start_time_berlin:%H:%M} - ' +
                         f'{item.end_time_berlin:%H:%M})'))
            table.add_row('Stage', item.stage_name)
            table.add_row('Speakers', item.speaker)
            console.print(
                Panel(
                    Group(table, item.description)
                ))


def main() -> None:
    """Start the script as a Typer app."""
    typer.run(start)


if __name__ == '__main__':
    main()
