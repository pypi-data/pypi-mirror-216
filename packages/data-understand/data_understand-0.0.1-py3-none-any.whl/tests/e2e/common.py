import os
import subprocess
import tempfile

import nbformat
import PyPDF2


class TestE2ECommon:
    def verify_pdf_file(self, pdf_file_name):
        pdf_reader = PyPDF2.PdfReader(pdf_file_name)
        assert len(pdf_reader.pages) > 0

    def verify_jupyter_notebook(self, jupyter_notebook_file_name):
        self._verify_jupyter_notebook_output_cells_are_empty(
            jupyter_notebook_file_name
        )
        # self._run_and_verify_jupyter_notebook_output_cells(
        #     jupyter_notebook_file_name
        # )

    def _verify_jupyter_notebook_output_cells_are_empty(
        self, jupyter_notebook_file_name
    ):
        with open(jupyter_notebook_file_name, "r") as file:
            # Parse the notebook file using nbformat
            notebook = nbformat.read(file, as_version=4)

        for cell in notebook.cells:
            if "outputs" in cell:
                assert (
                    len(cell["outputs"]) == 0
                ), "Output cell found in notebook. Please clean your notebook"

    def _run_and_verify_jupyter_notebook_output_cells(self, filepath):
        """Execute a notebook via nbconvert and collect output."""
        with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
            args = [
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "-y",
                "--no-prompt",
                "--output",
                fout.name,
                filepath,
            ]
            subprocess.check_call(args)

            fout.seek(0)
            nb = nbformat.read(fout, nbformat.current_nbformat)

        errors = [
            output
            for cell in nb.cells
            if "outputs" in cell
            for output in cell["outputs"]
            if output.output_type == "error"
        ]

        assert (
            errors == []
        ), "There shouldn't be any errors in the executed jupyter notebook"

    def verify_if_files_generated(
        self, csv_file_name, generate_jupyter_notebook, generate_pdf
    ):
        assert os.path.exists(csv_file_name)
        if generate_pdf:
            assert os.path.exists(csv_file_name + ".pdf")
        else:
            assert not os.path.exists(csv_file_name + ".pdf")
        if generate_jupyter_notebook:
            assert os.path.exists(csv_file_name + ".ipynb")
        else:
            assert not os.path.exists(csv_file_name + ".ipynb")

    def cleanup_generated_files(
        self, csv_file_name, generate_jupyter_notebook, generate_pdf
    ):
        os.remove(csv_file_name)
        if generate_pdf:
            os.remove(csv_file_name + ".pdf")
        if generate_jupyter_notebook:
            os.remove(csv_file_name + ".ipynb")

    def execute_and_verify_data_understand(
        self, csv_file_name, generate_jupyter_notebook, generate_pdf
    ):
        if generate_jupyter_notebook and generate_pdf:
            command = "data_understand -f {0} -t target -p -j".format(
                csv_file_name
            )
        elif generate_pdf:
            command = "data_understand -f {0} -t target -p".format(
                csv_file_name
            )
        elif generate_jupyter_notebook:
            command = "data_understand -f {0} -t target -j".format(
                csv_file_name
            )
        else:
            command = "data_understand -f {0} -t target".format(csv_file_name)
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )
        print(result.stdout)
        print(result.stderr)
        assert result.returncode == 0

        self.verify_if_files_generated(
            csv_file_name, generate_jupyter_notebook, generate_pdf
        )
        if generate_jupyter_notebook:
            self.verify_jupyter_notebook(csv_file_name + ".ipynb")
        if generate_pdf:
            self.verify_pdf_file(csv_file_name + ".pdf")

        # Clean up the temporary files
        self.cleanup_generated_files(
            csv_file_name, generate_jupyter_notebook, generate_pdf
        )
