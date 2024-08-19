import pandas as pd
import numpy as np
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go


class ConfusionMatrixGenerator:
    """
    A class to generate a confusion matrix based on a sentence transformer model.

    Attributes:
        hazard_df (pandas.DataFrame): The DataFrame containing hazard information.
        output_folder (str): The folder path where the output files will be saved.
        model (str): The name or path of the sentence transformer model.
        unique_categories (List[str]): A list of unique hazard categories.
        cumulative_counts (List[int]): A list of cumulative counts for each hazard category.
        confusion_df (pandas.DataFrame): The DataFrame containing the confused hazards.

    Methods:
        find_category_lines: Finds the positions of category boundaries in the similarity matrix.
        visualize_heatmap: Visualizes the similarity matrix as a heatmap with ordered category lines.
        save_similarity_matrix: Saves the similarity matrix as an Excel file.
        generate_similarity_pairs: Generate pairs of hazard codes along with their similarity scores based on a similarity matrix.
        filter_similarity_pairs: Filters the similarity pairs based on the similarity score.
        generate_confused_hazards: Creates a dataframe with the most similar hazards for each hazard.
        save_confused_pairs: Saves the confused pairs as Excel and JSON files.
        add_confused_to_definitions: Adds the confused hazards to the hazard definitions.
        show_plotly_heatmap: Visualizes the similarity matrix as an interactive heatmap using Plotly.
        run_plotly_heatmap: Runs the ConfusionMatrixGenerator to generate and display an interactive heatmap using Plotly.
        run: Runs the ConfusionMatrixGenerator to generate and save the confusion matrix and other outputs.
    """

    def __init__(self, model: str, data_file_path: str, output_folder: str) -> None:
        """
        Initializes the ConfusionMatrixGenerator class.

        Args:
            model (str): The name or path of the sentence transformer model.
            data_file_path (str): The file path of the data file containing hazard information.
            output_folder (str): The folder path where the output files will be saved.
        """
        self.hazard_df = pd.read_excel(data_file_path)
        self.output_folder = output_folder
        self.model = SentenceTransformer(model)
        self.unique_categories = None
        self.cumulative_counts = None
        self.confusion_df = None

    def find_category_lines(self, categories: pd.Series) -> List[int]:
        """
        Finds the positions of category boundaries in the similarity matrix.

        Args:
            categories (pd.Series): The series containing hazard categories.

        Returns:
            List[int]: A list of line positions representing the category boundaries.
        """
        unique_categories = categories.drop_duplicates().tolist()

        cumulative_counts = []
        count = 0
        for category in unique_categories:
            count += (categories == category).sum()
            cumulative_counts.append(count)

        return cumulative_counts[:-1]

    def visualize_heatmap(
        self, similarity_matrix: np.ndarray, line_positions_ordered: List[int]
    ) -> None:
        """
        Visualizes the similarity matrix as a heatmap with ordered category lines.

        Args:
            similarity_matrix (np.ndarray): The similarity matrix to be visualized.
            line_positions_ordered (List[int]): The ordered line positions representing the category boundaries.
        """
        plt.figure(figsize=(12, 10))
        sns.heatmap(similarity_matrix, cmap="viridis", xticklabels=False, yticklabels=False)

        for position in line_positions_ordered:
            plt.axhline(position, color="white", linewidth=1.5)
            plt.axvline(position, color="white", linewidth=1.5)

        plt.title("Similarity Matrix Heatmap (BERT with Ordered Category Lines)")
        plt.savefig(f"{self.output_folder}/heatmap.png")
        plt.close()

    def save_similarity_matrix(self, similarity_matrix: np.ndarray) -> None:
        """
        Saves the similarity matrix as an Excel file.

        Args:
            similarity_matrix (np.ndarray): The similarity matrix to be saved.
        """
        similarity_df = pd.DataFrame(
            similarity_matrix,
            columns=self.hazard_df["Hazard_Description"],
            index=self.hazard_df["Hazard_Description"],
        )
        similarity_df.to_excel(f"{self.output_folder}/confusion_matrix.xlsx")

    def generate_similarity_pairs(self, similarity_matrix: np.ndarray) -> pd.DataFrame:
        """
        Generate pairs of hazard codes along with their similarity scores based on a similarity matrix.

        Args:
            similarity_matrix (numpy.ndarray): The similarity matrix representing the pairwise similarity scores.

        Returns:
            pandas.DataFrame: A DataFrame containing the pairs of hazard codes and their similarity scores.

        """
        pairs = []
        for i in range(similarity_matrix.shape[0]):
            for j in range(similarity_matrix.shape[1]):
                pairs.append(
                    {
                        "Hazard_Code_1": self.hazard_df["Hazard_Code"].iloc[i],
                        "Hazard_Code_2": self.hazard_df["Hazard_Code"].iloc[j],
                        "Similarity_Score": similarity_matrix[i, j],
                    }
                )
        return pd.DataFrame(pairs)

    def filter_similarity_pairs(self, similarity_pairs_df: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the similarity pairs based on the similarity score.

        Args:
            similarity_pairs_df (pandas.DataFrame): The DataFrame containing the similarity pairs.

        Returns:
            pandas.DataFrame: The filtered DataFrame containing the similarity pairs.
        """
        similarity_pairs_df = similarity_pairs_df[
            (similarity_pairs_df["Similarity_Score"] < 1)
            & (similarity_pairs_df["Similarity_Score"] > 0.5)
        ]
        return similarity_pairs_df

    def generate_confused_hazards(
        self, similarity_matrix: np.ndarray, similarity_pairs_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Creates a dataframe with the most similar hazards for each hazard.

        Args:
            similarity_matrix (numpy.ndarray): The similarity matrix representing the pairwise similarity scores.
            similarity_pairs_df (pandas.DataFrame): The DataFrame containing the similarity pairs.

        Returns:
            pandas.DataFrame: A DataFrame containing the hazard codes and their most similar hazards.
        """
        confused_hazards = []
        for i in range(similarity_matrix.shape[0]):
            most_similar_hazards = (
                similarity_pairs_df[
                    similarity_pairs_df["Hazard_Code_1"] == self.hazard_df["Hazard_Code"].iloc[i]
                ]
                .nlargest(3, "Similarity_Score")["Hazard_Code_2"]
                .tolist()
            )
            confused_hazards.append(", ".join(most_similar_hazards))

        confusion_df = pd.DataFrame(
            {
                "Hazard_Code": self.hazard_df["Hazard_Code"],
                "Confused_Hazards": confused_hazards,
            }
        )

        return confusion_df

    def save_confused_pairs(self, confused_pairs_df: pd.DataFrame) -> None:
        """
        Saves the confused pairs as Excel and JSON files.

        Args:
            confused_pairs_df (pandas.DataFrame): The DataFrame containing the confused pairs.
        """
        confused_pairs_df.to_excel(f"{self.output_folder}/confusion_list.xlsx")
        confused_pairs_df.to_json(f"{self.output_folder}/confusion_list.json", orient="records")

    def add_confused_to_definitions(
        self, confusion_df: pd.DataFrame, hazard_definitions: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Adds the confused hazards to the hazard definitions.

        Args:
            confusion_df (pandas.DataFrame): The DataFrame containing the confused pairs.
            hazard_definitions (pandas.DataFrame): The DataFrame containing the hazard definitions.

        Returns:
            pandas.DataFrame: The DataFrame containing the hazard definitions with the confused hazards.
        """
        return hazard_definitions.merge(confusion_df, on="Hazard_Code")

    def show_plotly_heatmap(self, similarity_matrix: np.ndarray, labels_list: List[str]) -> None:
        """
        Visualizes the similarity matrix as an interactive heatmap using Plotly.

        Args:
            similarity_matrix (np.ndarray): The similarity matrix to be visualized.
            labels_list (List[str]): The list of labels for the heatmap.
        """
        # Mask the upper half of the similarity matrix
        mask = np.triu(np.ones_like(similarity_matrix, dtype=bool))
        similarity_matrix[mask] = None

        fig = go.Figure(
            data=go.Heatmap(
                z=similarity_matrix,
                x=labels_list,
                y=labels_list,
                colorscale="Viridis",
                hoverongaps=False,
            )
        )

        fig.update_layout(
            title="Hazard Confusion Likelihood Heatmap (Lower Half)",
            xaxis=dict(title="Hazard", tickangle=45),
            yaxis=dict(title="Hazard", tickangle=-45),
        )

        fig.show()

    def run_plotly_heatmap(self) -> None:
        """
        Runs the ConfusionMatrixGenerator to generate and display an interactive heatmap using Plotly.
        """
        # Use cosine similarity to compare each hazard description pair
        embeddings = self.model.encode(self.hazard_df["Hazard_Description"].tolist())
        similarity_matrix = cosine_similarity(embeddings)

        # Create the labels for the heatmap (Hazard Code and Hazard Name)
        labels_list = (
            self.hazard_df["Hazard_Code"] + " - " + self.hazard_df["Hazard_Name"]
        ).tolist()

        # Create the interactive heatmap using plotly.graph_objects
        self.show_plotly_heatmap(similarity_matrix, labels_list)

    def run(self) -> None:
        """
        Runs the ConfusionMatrixGenerator to generate and save the confusion matrix and other outputs.
        """
        # Use cosine similarity to compare each hazard description pair
        embeddings = self.model.encode(self.hazard_df["Hazard_Description"].tolist())
        similarity_matrix = cosine_similarity(embeddings)

        line_positions_ordered = self.find_category_lines(self.hazard_df["Hazard_Category"])

        self.visualize_heatmap(similarity_matrix, line_positions_ordered)
        self.save_similarity_matrix(similarity_matrix)

        # Create pairs of hazard codes and their similarity scores
        pairs_df = self.generate_similarity_pairs(similarity_matrix)
        filtered_pairs_df = self.filter_similarity_pairs(pairs_df)
        confusion_df = self.generate_confused_hazards(similarity_matrix, filtered_pairs_df)
        # self.save_confused_pairs(confusion_df)

        updated_hazard_definitions = self.hazard_df.merge(confusion_df, on="Hazard_Code")

        updated_hazard_definitions.to_excel(
            f"{self.output_folder}/hazard_definitions.xlsx", index=False
        )


data_file = "../data/hazard_definitions.xlsx"
output_folder = "data"
confusion_matrix_generator = ConfusionMatrixGenerator("all-mpnet-base-v2", data_file, output_folder)

# Generate and save the confusion matrix and other outputs
# confusion_matrix_generator.run()

# Generate and display an interactive heatmap using Plotly
confusion_matrix_generator.run_plotly_heatmap()
