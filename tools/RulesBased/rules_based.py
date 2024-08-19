"""
Uses rules based matching to guide the user through identifying the hazards in the event report.
"""

import string
import nltk
import pandas as pd
import warnings

# remove redundant pandas warning
warnings.simplefilter(action="ignore", category=FutureWarning)


class HazardIdentifier:
    """
    Class for identifying hazards based on predefined definitions and a given event report.

    Attributes:
        hazard_definitions_pd (pandas.DataFrame): DataFrame containing hazard definitions.
        category_wordlist (dict): Dictionary containing category wordlists.
        report (str): Event report text.
        identified_categories (list): List of identified hazard categories.
        self.identified_hazards (list): List of identified hazards.

    Methods:
        load_hazard_definitions: Loads hazard definitions from a JSON file and an Excel file.
        load_category_wordlist: Loads category wordlists from a JSON file.
        load_event_report: Loads the event report from a text file.
        tokenize_report: Tokenizes the event report.
        identify_categories: Identifies hazard categories based on the category wordlists.
        identify_hazards: Identifies hazards based on the hazard definitions and user input.
        print_identified_hazards: Prints the identified hazards.
        run: Executes the hazard identification process.
    """

    def __init__(self):
        self.hazard_definitions_pd = None
        self.category_wordlist = None
        self.report = None
        self.report_excel = None
        self.identified_hazards = set()
        self.rejected_hazards = set()
        nltk.download('punkt')

    def load_report_excel(self, file_path):
        """
        Loads the report csv file.
        """
        self.report_excel = pd.read_excel(file_path)

    def load_hazard_definitions(self):
        """
        Loads hazard definitions from a JSON file and an Excel file.
        """
        self.hazard_definitions_pd = pd.read_excel("../data/hazard_definitions.xlsx")

        for i in range(len(self.hazard_definitions_pd)):
            if not pd.isna(self.hazard_definitions_pd["Keywords"][i]):
                self.hazard_definitions_pd["Keywords"][i] = nltk.word_tokenize(
                    self.hazard_definitions_pd["Keywords"][i]
                )
                self.hazard_definitions_pd["Keywords"][i] = [
                    word.lower() for word in self.hazard_definitions_pd["Keywords"][i]
                ]
                self.hazard_definitions_pd["Keywords"][i] = [
                    word
                    for word in self.hazard_definitions_pd["Keywords"][i]
                    if word not in string.punctuation
                ]
            else:
                self.hazard_definitions_pd["Keywords"][i] = []

            if not pd.isna(self.hazard_definitions_pd["Upstream_Hazards"][i]):
                self.hazard_definitions_pd["Upstream_Hazards"][i] = self.hazard_definitions_pd[
                    "Upstream_Hazards"
                ][i].split(", ")
            else:
                self.hazard_definitions_pd["Upstream_Hazards"][i] = []

    def load_event_report(self):
        """
        Loads the event report from a text file.
        """
        with open("data/eventReport.txt", "r", encoding="UTF-8") as f:
            self.report = f.read()

    def tokenize_report(self):
        """
        Tokenizes the event report.
        """
        self.report = nltk.word_tokenize(self.report)
        self.report = [word.lower() for word in self.report]

    def identify_hazards(self):
        """
        Identifies hazards based on the hazard definitions and user input.
        """
        try:
            print(
                "After being asked each question, you will be asked for an input of (y/n/d/r)\n\n - Yes (y / 1) will add the hazard to the identified hazards\n - No (n / 2) will skip the hazard\n - Define (d / 3) will print the hazard description and ask for an input of (y/n)\n - Reason (r / 4) will print the word that suggests a hazard is present\n"
            )
            for _ in range(3):
                for row in self.hazard_definitions_pd.itertuples():
                    for hazard in row.Upstream_Hazards:
                        if (
                            hazard in self.identified_hazards
                            and hazard not in self.rejected_hazards
                        ):
                            print(f"Upstream hazard {hazard} already identified")
                            print(f"{row.Questions} - {row.Hazard_Name}")
                            response = input("(y/n/d/r): ")
                            if response in ["yes", "y", "1"]:
                                self.identified_hazards.add(row.Hazard_Code)
                            elif response in ["define", "def", "d", "3"]:
                                print(row.Hazard_Description)
                                response = input("(y/n/r): ")
                                if response in ["yes", "y", "1"]:
                                    self.identified_hazards.add(row.Hazard_Code)
                            elif response in ["reason", "r", "4"]:
                                print(hazard)
                                response = input("(y/n/r): ")
                                if response in ["yes", "y", "1"]:
                                    self.identified_hazards.add(row.Hazard_Code)

                            if response in ["no", "n", "2", ""]:
                                self.rejected_hazards.add(row.Hazard_Code)
                            break

                    if (
                        row.Hazard_Code not in self.identified_hazards
                        and row.Hazard_Code not in self.rejected_hazards
                    ):
                        for word in row.Keywords:
                            if word.lower() in self.report:
                                print(word)
                                print(row.Questions)
                                response = input("(y/n/d/r): ")
                                if response in ["yes", "y", "1"]:
                                    self.identified_hazards.add(row.Hazard_Code)
                                elif response in ["define", "def", "d", "3"]:
                                    print(row.Hazard_Description)
                                    response = input("(y/n): ")
                                    if response == "y":
                                        self.identified_hazards.add(row.Hazard_Code)
                                elif response in ["reason", "r", "4"]:
                                    print(word)
                                    response = input("(y/n/r): ")
                                    if response in ["yes", "y", "1"]:
                                        self.identified_hazards.add(row.Hazard_Code)

                                if response in ["no", "n", "2", ""]:
                                    self.rejected_hazards.add(row.Hazard_Code)
                                break
            for hazard in self.identified_hazards:
                print(hazard, end=", ")
            input("\nPress enter to continue")
        except KeyboardInterrupt:
            pass

    # def run(self):
    #     """
    #     Executes the hazard identification process (ReliefWeb max tagging version)
    #     """
    #     self.load_hazard_definitions()
    #     self.load_report_excel("./data/disaster_data_even.xlsx")
    #     start_row = int(input("Which row to start with? "))
    #     end_row = int(input("Which row to end with? "))
    #     for i in range((start_row - 1), (end_row - 1)):
    #         self.report = self.report_excel["Report"][i]
    #         print(f"\n\nReport {i + 1}")
    #         print(self.report)
    #         valid_report = input("Is this a valid report? (y/n): ")
    #         if valid_report in ["no", "n", "2"]:
    #             continue
    #         self.tokenize_report()
    #         self.identify_hazards()

    def run(self):
        """
        Executes the hazard identification process (One report version)
        """
        self.load_hazard_definitions()
        # get input from user
        report = input("Enter the report:\n")
        if report == "":
            print("Running default report...")
            self.load_event_report()
        else:
            self.report = report
        print(self.report)
        self.tokenize_report()
        self.identify_hazards()


if __name__ == "__main__":
    hazard_identifier = HazardIdentifier()
    hazard_identifier.run()
