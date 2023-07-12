import os
from traitlets.config import Config
from nbconvert.exporters import WebPDFExporter

class ipycalcExporter(WebPDFExporter):
    """
    A custom PDF exporter for ipycalc.
    """

    export_from_notebook = 'ipycalc'

    @default("template_name")
    def _template_name_default(self):
        return 'ipycalc'

    @property
    def _template_paths(self):
        return super()._template_paths + [os.path.join(os.path.dirname(__file__), "nbconvert_templates")]
    