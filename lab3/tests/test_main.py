import io
import os
import runpy
import sys
import unittest
from unittest.mock import patch

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import main
from Equation import Equation


class TestMain(unittest.TestCase):
    def test_print_equations_with_and_without_sdnf(self):
        equations = [Equation(name="E", sdnf="X1", minimized="X1")]

        with patch("sys.stdout", new_callable=io.StringIO) as captured:
            main._print_equations("Section", equations, include_sdnf=True)
            output = captured.getvalue()
        self.assertIn("Section", output)
        self.assertIn("SDNF: X1", output)
        self.assertIn("Minimized: X1", output)

        with patch("sys.stdout", new_callable=io.StringIO) as captured:
            main._print_equations("Section", equations, include_sdnf=False)
            output = captured.getvalue()
        self.assertIn("E = X1", output)

    def test_main_prints_all_sections(self):
        fake_equation = [Equation(name="N", sdnf="S", minimized="M")]
        with (
            patch.object(main.circuits, "get_adder_equations", return_value=fake_equation) as adder,
            patch.object(main.circuits, "get_decoder_5421_equations", return_value=fake_equation) as decoder,
            patch.object(main.circuits, "get_bcd_adder_equations", return_value=fake_equation) as bcd_adder,
            patch.object(main.circuits, "get_encoder_5421_equations_offset_n", return_value=fake_equation) as encoder,
            patch.object(main.circuits, "get_counter_equations", return_value=fake_equation) as counter,
            patch("sys.stdout", new_callable=io.StringIO) as captured,
        ):
            main.main()

        adder.assert_called_once()
        decoder.assert_called_once()
        bcd_adder.assert_called_once()
        encoder.assert_called_once()
        counter.assert_called_once()
        output = captured.getvalue()
        self.assertIn("SDNF:", output)
        self.assertIn("N = M", output)

    def test_module_executes_main_in_dunder_main_mode(self):
        module_path = os.path.join(ROOT, "main.py")
        fake_equation = [Equation(name="ScriptEq", sdnf="S", minimized="M")]
        with (
            patch("circuits.get_adder_equations", return_value=fake_equation),
            patch("circuits.get_decoder_5421_equations", return_value=fake_equation),
            patch("circuits.get_bcd_adder_equations", return_value=fake_equation),
            patch("circuits.get_encoder_5421_equations_offset_n", return_value=fake_equation),
            patch("circuits.get_counter_equations", return_value=fake_equation),
            patch("sys.stdout", new_callable=io.StringIO) as captured,
        ):
            runpy.run_path(module_path, run_name="__main__")

        self.assertIn("ScriptEq", captured.getvalue())

