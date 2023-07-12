import os
from traitlets.config import Config
from nbconvert.exporters import WebPDFExporter

class ipycalcExporter(WebPDFExporter):
    """
    A custom PDF exporter for ipycalc.
    """

    export_from_notebook = 'ipycalc via webpdf'

    @property
    def template_paths(self):
        return super().template_paths + [os.path.join(os.path.dirname(__file__), "nbconvert_templates")]
    
    def _template_file_default(self):
        """
        We want to use the new template we ship with our library.
        """
        return 'ipycalc.tpl'
    