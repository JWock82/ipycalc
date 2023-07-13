import os
import os.path

from traitlets.config import Config
from nbconvert.exporters.pdf import PDFExporter

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

class ipycalcExporter(PDFExporter):
    """
    An exporter for ipycalc
    """

    # If this custom exporter should add an entry to the
    # "File -> Download as" menu in the notebook, give it a name here in the
    # `export_from_notebook` class member
    export_from_notebook = "ipycalc"

    @property
    def template_paths(self):
        """
        We want to inherit from PDF template, and have templates under
        ``./templates/`` so append it to the search path. (see next section)

        Note: nbconvert 7.0 changed ``template_path`` to ``template_paths``
        """
        return super().template_paths + [os.path.join(os.path.dirname(__file__), "nbconvert_templates")]

    def _template_file_default(self):
        """
        We want to use the new template we ship with our library.
        """
        return os.path.join(os.path.dirname(__file__), 'nbconvert_templates\ipycalc.j2')  # full path to your PDF template file
