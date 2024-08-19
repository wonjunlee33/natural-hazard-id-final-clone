#!/usr/bin/env python
# coding: utf-8

# # Llama2 working on CS Cluster machines for increased speed (and accuracy)

# ## Step 0: Make sure Nvidia RTX is running.

# In[3]:


# ## Step 1: Assuming that folder "models" exists, set up Llama2 using ctransformers
# This version of Llama-13b-chat is quantised down to 5 bits for enhanced accuracy.

# In[4]:


# load ctransformers and set up parameters
from ctransformers import AutoModelForCausalLM

# try loading model
try:
    llm = AutoModelForCausalLM.from_pretrained(
        model_path_or_repo_id="./models/13B-chat-GGUF-q5_K_M.gguf",
        model_file="13B-chat-GGUF-q5_K_M.gguf",
        model_type="llama",
        max_new_tokens=75,
        repetition_penalty=1.2,
        temperature=0.25,
        top_p=0.95,
        top_k=150,
        threads=22,
        batch_size=40,
        gpu_layers=50,
    )
except ValueError as e:
    raise FileNotFoundError(
        "Model not found. Please ensure that the model is located in the correct folder."
    )

# ## Step 2: Load Excel Spreadsheet and make into a DataFrame.

# In[5]:


import pandas as pd
import os
import re
from itertools import product

# specify the path to Excel file
excel_file_path = "../data/hazard_definitions.xlsx"

# read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

# ## Step 3: Define some helper functions to output correct scores.

# In[7]:


def extract_score(response):
    """
    Extracts the likelihood score from the LLM's response.

    Parameters:
    response (str): The user's response.

    Returns:
    float: The extracted likelihood score if found, -1 otherwise.
    """
    user_input = response

    # use regular expression to extract the number between 0 and 5"
    likelihood_match = re.search(r"\b([0-5]|\([0-5]\))\b", user_input)

    # check if a match is found and print the extracted number
    if likelihood_match:
        extracted_likelihood = float(likelihood_match.group(1) or likelihood_match.group(2))
        print("Extracted Likelihood:", extracted_likelihood)
        return extracted_likelihood
    else:
        print("No likelihood score found.")
        return -1


# ## Step 4: Create ~ 303^2 combinations and feed through to LLM model.

# In[8]:

# extracting unique values from the desired column
unique_values = df["Hazard_Name"].unique()  # change to create AxA matrix, remove to make all
print(unique_values)

# create double-sided pairs without pairs with the same element
pairs = [(x, y) for x, y in product(unique_values, unique_values) if x != y]


# ## Step 5: Create new dataframes to store new data.

# In[9]:


# Check if the excel files already exist
if os.path.exists("./out/scores.xlsx") and os.path.exists("./out/justifications.xlsx"):
    # Load the existing excel files
    scores_df = pd.read_excel("./out/scores.xlsx", index_col=0, dtype=str)
    justification_df = pd.read_excel("./out/justifications.xlsx", index_col=0, dtype=str)
else:
    # Create new excel files
    # print("poo")
    scores_df = pd.DataFrame(index=unique_values, columns=unique_values)
    justification_df = pd.DataFrame(index=unique_values, columns=unique_values)

scores_df


# ### Step 5.5: Find the first pair which does not have a value stored

# In[10]:


def find_first_missing_pair(df):
    """
    Finds the first pair of row and column categories in a DataFrame where the corresponding element is missing.

    Parameters:
    - df (pd.DataFrame): The DataFrame to search for missing values.

    Returns:
    - tuple or None: If a missing value is found, returns a tuple containing the row and column categories of the missing element. If no missing values are found, returns None.
    """
    categories = df.columns  # Exclude the first column which contains row headers
    for i, row_category in enumerate(categories):
        for j, col_category in enumerate(categories):
            if i != j:  # Exclude pairs where both elements are the same
                value = df.iloc[i, j]  # j+1 to account for the row header column
                if pd.isna(value):  # Check if the value is NaN
                    print(i, j)
                    return (row_category, col_category)
    return None


missing_value = find_first_missing_pair(scores_df)


# ## Step 6: Run the LLM.

# In[11]:


def run_llm(hazard1, hazard2, def1, def2):
    """
    Run a likelihood assessment using a Language Model (LLM) to evaluate the likelihood that a given hazard1 causes hazard2.

    Parameters:
    - hazard1 (str): The first hazard in the assessment.
    - hazard2 (str): The second hazard in the assessment.
    - def1 (str): The definition of the first hazard.
    - def2 (str): The definition of the second hazard.

    Returns:
    tuple: A tuple containing the numerical score representing the likelihood assessment (ranging from 0 to 5) and the detailed response from the language model.
    """
    # cut definitions to be only first sentence
    def1 = def1.split(".")[0]
    def2 = def2.split(".")[0]

    # begin prompting
    prompt = f"""What is the likelihood that {hazard1} causes {hazard2}, bearing in mind:
    {hazard1}: {def1}
    {hazard2}: {def2}
    """

    super_prompt = f"""
    SYSTEM: We're evaluating the likelihood of various hazards causing specific outcomes. Your responses should be one number between 0 and 5, following the below scale. Include a short explanation for your score, as it helps understand the reasoning behind your assessment.
    
    - 0: Almost never
    - 1: Very Unlikely
    - 2: Unlikely
    - 3: Likely
    - 4: Very likely
    - 5: Almost always

    Given the above, consider the following query:

    USER: {prompt}
    
    ASSISTANT:
    """

    response = llm(super_prompt)
    print(f"Running: {hazard1}, {hazard2}")
    print(response)
    score = extract_score(response)
    print("====================================")
    return (score, response)


# ## Step 7: Record and update spreadsheets.

# In[13]:


# store the scores and justifications in the new dataframes
i = 0
# missing_value contains the first pair that does not have a value stored, slice the pairs list to start from there
pairs = pairs[pairs.index(missing_value) :]
length_pairs = len(pairs)

for pair in pairs:
    print(f"ITERATION {i} of {length_pairs}")
    data = run_llm(
        pair[0],
        pair[1],
        df[df["Hazard_Name"] == pair[0]]["Hazard_Description"].values[0],
        df[df["Hazard_Name"] == pair[1]]["Hazard_Description"].values[0],
    )
    scores_df.loc[pair[0], pair[1]] = data[0]
    justification_df.loc[pair[0], pair[1]] = data[1]
    if i % 20 == 0:
        scores_df.to_excel("./out/scores.xlsx")
        justification_df.to_excel("./out/justifications.xlsx")
    i += 1


# ## Step 8: Rerun all instances of -1, until there are no more -1's

# In[14]:


def find_invalid_pairs():
    """
    Finds pairs of row and column categories in the scores DataFrame where the corresponding element is -1

    Returns:
    - list: A list of tuples containing the row and column categories of the missing elements.
    """
    scores_df = pd.read_excel("./out/scores.xlsx", index_col=0, dtype=str)
    justification_df = pd.read_excel("./out/justifications.xlsx", index_col=0, dtype=str)

    # check which pairs are equal to -1
    invalid_pairs = []
    for i, row in scores_df.iterrows():
        for j, value in row.items():
            if value == "-1":
                invalid_pairs.append((i, j))

    return invalid_pairs


# In[15]:


# add the invalid pairs to update score_df
j = 0
invalid_pairs = find_invalid_pairs()
print(invalid_pairs)
length_invalid_pairs = len(invalid_pairs)

# until no more invalid pairs
while invalid_pairs:
    print("STARTING NEW INVALID CORRECTION ITERATION...........")
    for pair in invalid_pairs:
        print(f"ITERATION {j} of {length_invalid_pairs}")
        data = run_llm(
            pair[0],
            pair[1],
            df[df["Hazard_Name"] == pair[0]]["Hazard_Description"].values[0],
            df[df["Hazard_Name"] == pair[1]]["Hazard_Description"].values[0],
        )
        scores_df.loc[pair[0], pair[1]] = data[0]
        justification_df.loc[pair[0], pair[1]] = data[1]
        if j % 20 == 0:
            scores_df.to_excel("./out/scores.xlsx")
            justification_df.to_excel("./out/justifications.xlsx")
        j += 1
    # reset, and check again
    j = 0
    invalid_pairs = find_invalid_pairs()
    length_invalid_pairs = len(invalid_pairs)
