"""
IKA AI v3
Scanner Controller

Runs the original IKA AI scanner in its own Python process
so the original project environment cannot conflict with v3.
"""

from pathlib import Path
import subprocess
import sys
import json


class ScannerController:

    def __init__(self):

        # ====================================================
        # Project locations
        # ====================================================

        self.v3_root = Path(__file__).resolve().parents[1]

        self.project_root = self.v3_root.parent

        self.last_results = []

    # ========================================================
    # Scan markets
    # ========================================================

    def scan_markets(self):

        print("\n================================")
        print("IKA AI V3 SCANNER")
        print("================================")
        print("Starting original scanner...\n")

        # ----------------------------------------------------
        # Python code that will run INSIDE the original
        # IKA_AI project.
        # ----------------------------------------------------

        scanner_code = r"""
import json
from analysis.market_scanner import scan_markets

results = scan_markets()

print(
    "\n__IKA_V3_RESULTS_START__"
)

print(
    json.dumps(
        results,
        default=str
    )
)

print(
    "__IKA_V3_RESULTS_END__"
)
"""

        # ----------------------------------------------------
        # Run original scanner
        # ----------------------------------------------------

        try:

            process = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    scanner_code
                ],

                cwd=str(self.project_root),

                capture_output=True,

                text=True,

                timeout=120
            )

        except subprocess.TimeoutExpired:

            raise RuntimeError(
                "The original market scanner "
                "timed out after 120 seconds."
            )

        # ----------------------------------------------------
        # Show original scanner output
        # ----------------------------------------------------

        if process.stdout:

            print(process.stdout)

        if process.stderr:

            print(
                "\nOriginal scanner errors:\n"
            )

            print(process.stderr)

        # ----------------------------------------------------
        # Check process result
        # ----------------------------------------------------

        if process.returncode != 0:

            raise RuntimeError(
                "Original scanner failed.\n\n"
                + process.stderr
            )

        # ----------------------------------------------------
        # Extract results
        # ----------------------------------------------------

        output = process.stdout

        start_marker = (
            "__IKA_V3_RESULTS_START__"
        )

        end_marker = (
            "__IKA_V3_RESULTS_END__"
        )

        start = output.find(
            start_marker
        )

        end = output.find(
            end_marker
        )

        if start == -1 or end == -1:

            raise RuntimeError(
                "The original scanner ran, "
                "but no results were returned."
            )

        # Move past start marker
        start += len(start_marker)

        json_text = output[
            start:end
        ].strip()

        # ----------------------------------------------------
        # Convert JSON back into Python
        # ----------------------------------------------------

        try:

            results = json.loads(
                json_text
            )

        except json.JSONDecodeError as error:

            raise RuntimeError(
                "Could not decode scanner results.\n\n"
                f"{error}\n\n"
                f"Returned data:\n{json_text}"
            )

        # ----------------------------------------------------
        # Store results
        # ----------------------------------------------------

        self.last_results = results

        print(
            "\n================================"
        )

        print(
            f"V3 RECEIVED: {len(results)} RESULTS"
        )

        print(
            "================================\n"
        )

        return results

    # ========================================================
    # Get previous results
    # ========================================================

    def get_results(self):

        return self.last_results
        