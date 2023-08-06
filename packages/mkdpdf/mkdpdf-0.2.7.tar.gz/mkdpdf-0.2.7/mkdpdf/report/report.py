import datetime

from mkdpdf import configuration
from mkdpdf.document.document import Document

class Report(Document):
    """
    Report is a time-bound document.
    """

    def __init__(self, date_publish:str = configuration.DATE_PUBLISH, format: str = configuration.FORMAT, filename: str = configuration.FILENAME, directory_path_output: str = configuration.DIRECTORY_PATH_OUTPUT, directory_path_templates: str = None):
        """
        Args:
            date_publish (string): 8601 date value
            directory_path_output (string): path of output directory
            directory_path_templates (string): path of template directory
            filename (string): name of output file
            format (enum): md || pdf
        """
        # update self
        self.date_publish = date_publish

        # initialize inheritance
        super(Report, self).__init__(
            directory_path_output=directory_path_output,
            directory_path_templates=directory_path_templates,
            filename=filename,
            format=format
        )

    def default_date_format(self, date_iso: str) -> str:
        """
        Default human legible date formats.

        Args:
            date_iso (string): iso 8601 date value

        Returns:
            A string representing a date.
        """

        return datetime.datetime.strftime(datetime.datetime.strptime(date_iso, "%Y-%m-%d"), "%B %d, %Y")

    def format_key_event(self, title: str, date: str = None, description: str = None) -> str:
        """
        Format key event for report template.

        Args:
            date (string): 8601 date value
            description (string): event description
            title (string): title of event

        Returns:
            A string representing a key event.
        """

        # format in markdown
        return "**%s**%s: %s" % (
            title,
            " (%s)" % self.default_date_format(date) if date else str(),
            description if description else str()
        )
