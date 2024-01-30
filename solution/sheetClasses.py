import pandas as pd

NOT_MASTER_DESCRIPTORS = set(
    [
        "Description",
        "Part Number",
        "Categories",
        "Category Names",
        "Enabled",
    ]
)

MASTER_NULL_SYMBOL = "$"
MASTER_CATEGORY_COLUMN = "Description"


class Solver:
    def __init__(self, masterSheet, cdSheet, destinationSheet):
        self.master = Master(masterSheet)
        self.cds = CategoryDescriptors(cdSheet)
        self.destination = Destination(destinationSheet)

    def formatMasterToCategoryDescriptors(self):
        # return df of descriptors, with associated UOM if there is one.
        # input_df columns included: CATEGORY_CODE, CATEGORY_NAME, DESCRIPTOR_NAME
        # rv columns included: CATEGORY_CODE, CATEGORY_NAME, DESCRIPTOR_NAME, DISP_SEQ (auto generated), FILTER_ENABLED, FILTER_SEQ

        pass


class Master:
    def __init__(self, masterSheet) -> None:
        self.masterdf = pd.read_excel(masterSheet)

    def getGroupedCategories(self, column=MASTER_CATEGORY_COLUMN):
        return self.masterdf.groupby(column)

    def getSeriesPopulationData(self, df, column, char=MASTER_NULL_SYMBOL):
        # get the % not populated by '$' (with exceptions)
        percentPopulated = df[column].value_counts(normalize=True)
        if not ("$" in percentPopulated.index):
            return 100
        return (1 - percentPopulated[MASTER_NULL_SYMBOL]) * 100

    def getDescriptorColumns(self):
        # returns a list of only the descriptor columns

        # get a list of master_source columns
        allColumns = self.masterdf.columns.values
        # filter that list to only include descriptors (so don't include the enum NOT_MASTER_DESCRIPTORS, or '(unit)' categories)
        descriptorColumns = filter(
            lambda x: not (x in NOT_MASTER_DESCRIPTORS or "(Unit)" in x), allColumns
        )
        return list(descriptorColumns)

    # df containing only one category
    def getTopCategoryDescriptors(self, df):
        # return a list of the top 5 category descriptors
        columns = self.getDescriptorColumns()
        cdData = {"names": [], "popPercent": []}
        for column in columns:
            percentPopulated = self.getSeriesPopulationData(df, column)
            if percentPopulated > 0:
                cdData["names"].append(column)
                cdData["popPercent"].append(percentPopulated)

        topFiveDf = pd.DataFrame(cdData).nlargest(5, "popPercent")
        return topFiveDf["names"].values

    def getTopDescriptors(self):
        # per each category
        #   getTopCategoryDescriptors
        #   get CATEGORY_CODE and CATEGORY_NAME
        # add all the dataframes together, return the df

        pass


class CategoryDescriptors:
    def __init__(self, cdSheet):
        self.cdDf = pd.read_excel(cdSheet)
        self.name = "filled_" + cdSheet

    def addConstantColumns(self):
        # adds the unchanging columns to the dataframe, then returns it
        # input is a dataframe
        self.cdDf["GROUP_NAME"] = pd.series("CNSTNT")
        self.cdDf["DATA_TYPE"] = pd.series("T")
        self.cdDf["DESCRIPTOR_TYPE"] = pd.series("Value")
        self.cdDf["VALUE_DELIMITER"] = pd.series("")
        self.cdDf["IS_DIFFERENTIATOR_DESCRIPTOR"] = pd.series("N")
        self.cdDf["ENTITY_TYPE"] = pd.series("I")
        self.cdDf["PRINT"] = pd.series("Y")
        self.cdDf["STATUS"] = pd.series("Y")

    def addDescriptors(self, addedDescriptors):
        # intakes a DF as from getTopDescriptors, modifies to the shape of CategoryDescriptors sheet, then adds to the sheet
        pass

    def exportToSheet(self):
        pass


class Destination:
    def __init__(self, destinationSheet) -> None:
        self.destinationDf = pd.read_excel(destinationSheet)
        self.name = "filled_" + destinationSheet

    def getOpenDescriptor(self) -> int:
        pass

    def addDescriptorName(self, name, value, uom="") -> None:
        pass

    def addDescriptors(self):
        # join descriptors from CategoryDescriptors to Destination on "category"

        pass

    def addValues(self):
        # for each row: get the matching master product entry
        # for each descriptor in row: add the corresponding value in the product entry
        pass

    def exportToSheet(self):
        pass
