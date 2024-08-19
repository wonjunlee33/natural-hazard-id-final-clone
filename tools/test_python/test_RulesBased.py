import unittest
import itertools
from unittest.mock import patch
import pandas as pd
from RulesBased.rules_based import HazardIdentifier


class TestHazardIdentifier(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.hazard_identifier = HazardIdentifier()

    def test_load_report_excel(self):
        self.hazard_identifier.load_report_excel("data/hazard_definitions.xlsx")
        self.assertIsNotNone(self.hazard_identifier.report_excel)

    # def test_load_hazard_definitions(self):
    #     self.hazard_identifier.load_hazard_definitions()
    #     self.assertIsNotNone(self.hazard_identifier.hazard_definitions_pd)

    def test_load_event_report(self):
        self.hazard_identifier.load_event_report()
        self.assertIsNotNone(self.hazard_identifier.report)

    def test_tokenize_report(self):
        self.hazard_identifier.load_event_report()
        self.hazard_identifier.tokenize_report()
        self.assertIsInstance(self.hazard_identifier.report, list)

    @patch("builtins.input", side_effect=itertools.cycle(["y"]))
    def test_identify_hazards(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [[], []],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.identified_hazards, {"H1"})

    @patch("builtins.input", side_effect=itertools.cycle(["d", "y"]))
    def test_define_hazards(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [[], []],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.identified_hazards, {"H1"})

    @patch("builtins.input", side_effect=itertools.cycle(["d", "n"]))
    def test_define_hazards_neg(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [[], []],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.rejected_hazards, {"H1"})

    @patch("builtins.input", side_effect=itertools.cycle(["n"]))
    def test_reject_hazards(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [[], []],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.rejected_hazards, {"H1"})

    @patch("builtins.input", side_effect=itertools.cycle(["r", "y"]))
    def test_reason_hazards(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [[], []],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.identified_hazards, {"H1"})

    @patch("builtins.input", side_effect=itertools.cycle(["r", "n"]))
    def test_reason_hazards_neg(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [[], []],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.rejected_hazards, {"H1"})

    @patch("builtins.input", side_effect=itertools.cycle(["y", "y"]))
    def test_upstream_hazards(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [[], ["H1"]],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.identified_hazards, {"H1", "H2"})

    @patch("builtins.input", side_effect=itertools.cycle(["y", "n"]))
    def test_upstream_hazards_neg(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [["H2"], []],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.identified_hazards, {"H1"})

    @patch("builtins.input", side_effect=itertools.cycle(["y", "d", "y"]))
    def test_upstream_hazards_define(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [[], ["H1"]],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.identified_hazards, {"H1", "H2"})

    @patch("builtins.input", side_effect=itertools.cycle(["y", "d", "n"]))
    def test_upstream_hazards_define_neg(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [["H2"], []],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.identified_hazards, {"H1"})

    @patch("builtins.input", side_effect=itertools.cycle(["y", "r", "y"]))
    def test_upstream_hazards_reason(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [[], ["H1"]],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.identified_hazards, {"H1", "H2"})

    @patch("builtins.input", side_effect=itertools.cycle(["y", "r", "n"]))
    def test_upstream_hazards_reason_neg(self, input):
        hazard_identifier = HazardIdentifier()
        hazard_identifier.hazard_definitions_pd = pd.DataFrame(
            {
                "Hazard_Code": ["H1", "H2"],
                "Upstream_Hazards": [["H2"], []],
                "Keywords": [["keyword1"], ["keyword2"]],
                "Questions": ["Question 1?", "Question 2?"],
                "Hazard_Name": ["Hazard 1", "Hazard 2"],
                "Hazard_Description": ["Description 1", "Description 2"],
            }
        )
        hazard_identifier.report = ["keyword1"]
        hazard_identifier.identify_hazards()
        self.assertEqual(hazard_identifier.identified_hazards, {"H1"})


# if __name__ == "__main__":
#     unittest.main()
