import pandas as pd


def getTopDescriptors():
    # group master_source data by category

    # per column:
    # get the % not populated by '$' (with exceptions)

    # select the top 5 most populated columns, or as many as possible, whichever is lesser

    # return the top 5 as a dataframe
    pass


def addConstantColumns(input_df):
    # adds the unchanging columns to the dataframe, then returns it
    # input is a dataframe
    df = input_df
    df["GROUP_NAME"] = pd.series("CNSTNT")
    df["DATA_TYPE"] = pd.series("T")
    df["DESCRIPTOR_TYPE"] = pd.series("Value")
    df["VALUE_DELIMITER"] = pd.series("")
    df["IS_DIFFERENTIATOR_DESCRIPTOR"] = pd.series("N")
    df["ENTITY_TYPE"] = pd.series("I")
    df["PRINT"] = pd.series("Y")
    df["STATUS"] = pd.series("Y")
    return df


master = pd.read_excel("problem_set\small_master_set.xlsx")
categories = master.groupby("Description")

print(master.shape)
