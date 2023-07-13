import os
from nbconvert.exporters import WebPDFExporter
from nbconvert.exporters.templateexporter import TemplateExporter

class ipycalcExporter(WebPDFExporter):
    """
    A custom PDF exporter for ipycalc.
    """

    custom_template_name = 'nbconvert_template'
    pkg_dir = os.path.dirname(__file__)
    template_dir = os.path.join(pkg_dir, custom_template_name)

    extra_template_paths = [
        os.path.join(TemplateExporter()._template_paths, 'lab'),
        template_dir
    ]

    @property
    def extra_template_basedirs(self):
        return super()._default_extra_template_basedirs() + [self.template_dir]

    def _template_name_default(self):
        return os.path.join(self.pkg_dir, self.custom_template_name)