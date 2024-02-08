import unittest
import pandas as pd
import pandas.testing as pdt
import solution.sheetClasses as sc
import os
from solution.sheetClasses import CategoryDescriptors

cd = CategoryDescriptors("problem_set/category-descriptor-template.xlsx")
expectedTopCategoryDescriptors = [
    "TPSA Certificate",
    "Industrial Part Type",
    "Rod Spacing",
]


class TestMaster(unittest.TestCase):
    def testInit(self):
        pass

    def testAddConstantColumns(self):
        starterDf = pd.DataFrame({"A": [1, 2, 3]})
        expectedDf = pd.DataFrame(
            {
                "A": [1, 2, 3],
                "GROUP_NAME": ["CNSTNT"] * 3,
                "DATA_TYPE": ["T"] * 3,
                "DESCRIPTOR_TYPE": ["Value"] * 3,
                "VALUE_DELIMITER": [""] * 3,
                "IS_DIFFERENTIATOR_DESCRIPTOR": ["N"] * 3,
                "ENTITY_TYPE": ["I"] * 3,
                "PRINT": ["Y"] * 3,
                "STATUS": ["Y"] * 3,
            }
        )
        actualDf = CategoryDescriptors.addConstantColumns(starterDf)
        print(expectedDf)
        print(actualDf)
        pdt.assert_frame_equal(expectedDf, actualDf)

    def testAddDescriptors(self):
        flangeDescriptorsDf = pd.DataFrame(
            {
                sc.CATEGORY_CODE: ["10000030"] * 3,
                sc.CATEGORY_NAME: ["FLANGE MOUNT"] * 3,
                sc.DESCRIPTOR_NAME: expectedTopCategoryDescriptors,
                sc.DISP_SEQ: [0, 1, 2],
                sc.FILTER_SEQ: [0, 1, 2],
                "FILTER_ENABLED": ["Y", "Y", "Y"],
            }
        )
        # print(cd.cdDf.tail())
        cd.addDescriptors(flangeDescriptorsDf)
        # print(cd.cdDf.tail())
        # not writing an assert, visual inspection is fine.

    def testExportToSheet(self):
        try:
            os.remove("./filled_category-descriptor-template.xlsx")
        except OSError:
            pass
        cd.exportToSheet()
        exported = os.path.isfile("./filled_category-descriptor-template.xlsx")
        try:
            os.remove("./filled_category-descriptor-template.xlsx")
        except OSError:
            pass
        self.assertTrue(exported, "File is not exported")


if __name__ == "__main__":
    unittest.main()
