import pandas as pd
from pathlib import Path

# Columns in Master that are not to be included in population analysis
NOT_MASTER_DESCRIPTORS = set(
    [
        "Description",
        "Part Number",
        "Categories",
        "Category Names",
        "Enabled",
    ]
)

# Important symbols in master sheet
MASTER_NULL_SYMBOL = "$"
MASTER_CATEGORY_COLUMN = "Description"
UNIT_INDICATOR = "(Unit)"

# Important columns in Category_Descriptor sheet
CATEGORY_CODE = "CATEGORY_CODE"
CATEGORY_NAME = "CATEGORY_NAME"
DESCRIPTOR_NAME = "DESCRIPTOR_NAME"
DISP_SEQ = "DISP_SEQ"
FILTER_SEQ = "FILTER_SEQ"


class Solver:
    def __init__(self, masterSheet, cdSheet, destinationSheet):
        self.master = Master(masterSheet)
        self.cds = CategoryDescriptors(cdSheet)
        self.destination = Destination(destinationSheet)

    def formatMasterToCategoryDescriptors(self):
        # return df of descriptors, with associated UOM if there is one.
        # input_df columns included: CATEGORY_CODE, CATEGORY_NAME, DESCRIPTOR_NAME
        # rv columns included: CATEGORY_CODE, CATEGORY_NAME, DESCRIPTOR_NAME, DISP_SEQ (auto generated), FILTER_ENABLED, FILTER_SEQ
        topDescriptors = self.master.getTopDescriptors()
        self.cds.addDescriptors(topDescriptors)
        self.cds.exportToSheet()


class Master:
    def __init__(self, masterSheet) -> None:
        self.masterdf = pd.read_excel(masterSheet)

    def getGroupedCategories(self, column=MASTER_CATEGORY_COLUMN):
        return self.masterdf.groupby(column)

    def getSeriesPopulationData(df, column, char=MASTER_NULL_SYMBOL):
        # get the % not populated by '$' (with exceptions)
        percentPopulated = df[column].value_counts(normalize=True)
        if not ("$" in percentPopulated.index):
            return 100
        return (1 - percentPopulated[MASTER_NULL_SYMBOL]) * 100

    def getDescriptorColumns(df):
        # returns a list of only the descriptor columns

        # get a list of master_source columns
        allColumns = df.columns.values
        # filter that list to only include descriptors (so don't include the enum NOT_MASTER_DESCRIPTORS, or '(unit)' categories)
        descriptorColumns = filter(
            lambda x: not (x in NOT_MASTER_DESCRIPTORS or UNIT_INDICATOR in x),
            allColumns,
        )
        return list(descriptorColumns)

    # df containing only one category
    def getTopDescriptorsList(df):
        # get a list of the top categories in the dataframe
        columns = Master.getDescriptorColumns(df)
        cdData = {"names": [], "popPercent": []}
        for column in columns:
            percentPopulated = Master.getSeriesPopulationData(df, column)
            if percentPopulated > 0:
                cdData["names"].append(column)
                cdData["popPercent"].append(percentPopulated)

        topFiveDf = pd.DataFrame(cdData).nlargest(5, "popPercent")
        return topFiveDf["names"].values

    # df containing only one category
    def getTopDescriptorsInCategory(df):
        # return a df of CATEGORY_CODE, CATEGORY_NAME, DESCRIPTOR_NAME
        if not (MASTER_CATEGORY_COLUMN in df.columns):
            raise KeyError("{} not found in input df".format(MASTER_CATEGORY_COLUMN))

        topDescriptorsList = Master.getTopDescriptorsList(df)
        categoryWords = df[MASTER_CATEGORY_COLUMN].iloc[0].split(" ")
        categoryCode = categoryWords[0]
        categoryName = " ".join(categoryWords[1:])
        categoryCodeList = [categoryCode for x in topDescriptorsList]
        categoryNameList = [categoryName for x in topDescriptorsList]
        dispSeq = list(range(len(topDescriptorsList)))
        filterSeq = list(range(len(topDescriptorsList)))

        rvDf = pd.DataFrame(
            {
                CATEGORY_CODE: categoryCodeList,
                CATEGORY_NAME: categoryNameList,
                DESCRIPTOR_NAME: topDescriptorsList,
                DISP_SEQ: dispSeq,
                FILTER_SEQ: filterSeq,
            }
        )
        rvDf["FILTER_ENABLED"] = pd.Series(["Y"] * len(topDescriptorsList))

        return rvDf

    def getTopDescriptors(self):
        """Get the top descriptors and return as a dataframe"""
        groupedCategories = list(self.getGroupedCategories())
        frames = []

        # per each category
        for category in groupedCategories:
            categoryDf = category[1]
            frames.append(Master.getTopDescriptorsInCategory(categoryDf))
        # add all the dataframes together, return the df
        return pd.concat(frames, ignore_index=True)


class CategoryDescriptors:
    def __init__(self, cdSheet):
        self.cdDf = pd.read_excel(cdSheet)
        fileName = cdSheet.split("/")[-1]
        self.name = "filled_" + fileName

    def addConstantColumns(df):
        # adds the unchanging columns to the dataframe, then returns it
        # input is a dataframe
        numRows = len(df)
        constantColumns = [
            ("GROUP_NAME", "CNSTNT"),
            ("DATA_TYPE", "T"),
            ("DESCRIPTOR_TYPE", "Value"),
            ("VALUE_DELIMITER", ""),
            ("IS_DIFFERENTIATOR_DESCRIPTOR", "N"),
            ("ENTITY_TYPE", "I"),
            ("PRINT", "Y"),
            ("STATUS", "Y"),
        ]
        for column, constant in constantColumns:
            df[column] = pd.Series([constant] * numRows)
        return df

    def addDescriptors(self, addedDescriptors):
        # intakes a DF as from getTopDescriptors, modifies to the shape of CategoryDescriptors sheet, then adds to the sheet
        newDf = CategoryDescriptors.addConstantColumns(addedDescriptors)
        self.cdDf = pd.concat([self.cdDf, newDf], ignore_index=True)

    def exportToSheet(self):
        self.cdDf.to_excel(self.name)

    def getDfFormattedToDest(self):
        """returns a version of category descriptors formatted to the destination df style, so that it can be easily joined"""
        tempDict = {
            CATEGORY_NAME: [],
            "DESCRIPTOR NAME1": [],
            "DESCRIPTOR NAME2": [],
            "DESCRIPTOR NAME3": [],
            "DESCRIPTOR NAME4": [],
            "DESCRIPTOR NAME5": [],
        }
        for name, group in self.cdDf.groupby(CATEGORY_NAME):
            tempDict[CATEGORY_NAME].append(name)
            descNum = 1
            for idx, row in group.head().iterrows():
                column = "DESCRIPTOR NAME" + str(descNum)
                tempDict[column].append(row[DESCRIPTOR_NAME])
                descNum += 1
        numCat = len(tempDict[CATEGORY_NAME])
        # populate empty descriptors with null values
        for key in tempDict.keys():
            while len(tempDict[key]) < numCat:
                tempDict[key].append("")
        rv = pd.DataFrame(tempDict)
        return rv


class Destination:
    def __init__(self, destinationSheet) -> None:
        self.destinationDf = pd.read_excel(destinationSheet)
        fileName = destinationSheet.split("/")[-1]
        self.name = "filled_" + destinationSheet

    def getOpenDescriptor(self, idx) -> int:
        for descNum in range(1, 6):
            descName = self.destinationDf["DESCRIPTOR NAME" + str(descNum)][idx]
            if descName == "" or descName == MASTER_NULL_SYMBOL:
                return descNum
        return -1

    def addDescriptorName(self, idx, name, value, uom="") -> None:
        pass

    def addDescriptors(self):
        # join descriptors from CategoryDescriptors to Destination on "category"

        # for each row:
        # get category foreign key
        # get part_number
        # get category descriptor columns from category descriptor sheet by foreign key

        # for each descriptor column:
        # clear descriptor column

        # fill descriptor name column with category descriptor sheet

        # fill value and uom columns from master_source sheet

        pass

    def addValues(self):
        # for each row: get the matching master product entry
        # for each descriptor in row: add the corresponding value in the product entry
        pass

    def exportToSheet(self):
        pass


solver = Solver(
    "problem_set/test_master_source_dummy.xlsx",
    "problem_set/category-descriptor-template.xlsx",
    "problem_set/destination.xlsx",
)
solver.formatMasterToCategoryDescriptors()
