import os
from traitlets.config import Config
from nbconvert.exporters import WebPDFExporter

class ipycalcExporter(WebPDFExporter):
    """
    A custom PDF exporter for ipycalc.
    """

    export_from_notebook = 'ipycalc via webpdf'

    def _template_file_default(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'nbconvert_templates')
        return os.path.join(template_dir, 'ipycalc.j2')

    @property
    def template_file(self):
        if not hasattr(self, '_template_file'):
            self._template_file = self._template_file_default()
        return self._template_file
    