# conservative_documents = [
#     "r_askconservatives_output.txt",
#     "r_asktrumpsupporters_output.txt",
#     "r_capitalism_output.txt",
#     "r_conservative_output.txt",
#     "r_conservatives_output.txt",
#     "r_progun_output.txt",
#     "r_prolife_output.txt",
#     "r_republican_output.txt",
#     "r_walkaway_output.txt",
# ]

# liberal_documents = [
#     "r_askaliberal.txt",
#     "r_democrats.txt",
#     "r_dsa.txt",
#     "r_esist.txt",
#     "r_joebiden.txt",
#     "r_liberal.txt",
#     "r_murderedbyaoc.txt",
#     "r_progressive.txt",
#     "r_wayofthebern.txt",
# ]
# liberal_dict = {}
# conservative_dict = {}

# for i in range(9):
#     with open(
#         f"conservative_outputs/{conservative_documents[i]}", encoding="utf8"
#     ) as f:
#         conservative_dict[f"conservative_{i}"] = f.read().replace("\n", " ")

# for i in range(9):
#     with open(f"liberal_outputs/{liberal_documents[i]}", encoding="utf8") as f:
#         liberal_dict[f"liberal_{i}"] = f.read().replace("\n", " ")

# liberal_list = [value for key, value in liberal_dict.items()]
# print(liberal_list)


import pandas as pd

# test_docs_df = pd.read_csv("corpus.csv")
# test_text_series = test_docs_df.text

# test_doc = [item for item in test_text_series]
# print(test_doc)


df = pd.read_excel("RedditExcelOutput.xlsx")

conservative_texts = df[df["Political Leaning"] == "Conservative"]["Comment Text"]
