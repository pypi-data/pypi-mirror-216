import logging
from typing import Tuple

from exasol_script_languages_container_tool.lib.api import export
from exasol_script_languages_container_tool.lib.tasks.export.export_containers import ExportContainerResult

from exasol_script_languages_container_ci.lib.ci_step_output_printer import CIStepOutputPrinterProtocol, \
    CIStepOutputPrinter


class CIExport:

    def __init__(self, printer: CIStepOutputPrinterProtocol = CIStepOutputPrinter(logging.info)):
        self._printer = printer

    def export(self,
               flavor_path: Tuple[str, ...],
               export_path: str):
        """
        Export the flavor as tar.gz file
        """

        logging.info(f"Running command 'push' with parameters: {locals()}")
        export_result = export(flavor_path=flavor_path,
                               export_path=export_path,
                               workers=7)
        self._printer.print_exasol_docker_images()
