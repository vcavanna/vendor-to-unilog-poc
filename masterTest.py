import unittest
import pandas as pd
import solution.sheetClasses as sc
from solution.sheetClasses import Master

m = Master("problem_set\\test_master_source_dummy.xlsx")
flangeMountSubset = m.getGroupedCategories().get_group("10000030 FLANGE MOUNT")
expectedTopCategoryDescriptors = [
    "TPSA Certificate",
    "Industrial Part Type",
    "Rod Spacing",
]


class TestMaster(unittest.TestCase):
    def testInit(self):
        assert (
            m.masterdf["Part Number"][0] == "10000001"
        ), "masterdf['Part Number'][0] == {}".format(m.masterdf["Part Number"][0])

    def testGetGroupedCategories(self):
        self.assertEqual(flangeMountSubset["Rod Spacing"][2], "Loosely Coupled")

    def testGetSeriesPopulationData(self):
        expectedPopulation = 60
        actualPopulation = Master.getSeriesPopulationData(m.masterdf, "Rod Spacing")
        self.assertEqual(actualPopulation, expectedPopulation)

    def testGetDescriptorColumns(self):
        actualDescriptorColumns = [
            "Actual Ratio",
            "ERPA Size",
            "Angular Offset",
            "TPSA Certificate",
            "Axial Offset",
            "Backstop Included",
            "Bearing Series",
            "Base to Center Height",
            "Base to Flange Center Height",
            "Industrial Component",
            "Industrial Part Type",
            "Industrial Part Height",
            "Industrial Part Length Datum",
            "Gear Circle",
            "Gear Diameter",
            "Gear to Gear (Max)",
            "Hole Diameter (Maximum)",
            "Hole Diameter (Minimum)",
            "Center Distance",
            "Center to End of Rod Distance",
            "Depth",
            "Rod Length Input",
            "Rod Length Output",
            "Rod Spacing",
        ]
        expectedDescriptorColumns = Master.getDescriptorColumns(m.masterdf)

        self.assertEqual(set(actualDescriptorColumns), set(expectedDescriptorColumns))

    def testGetTopDescriptorsList(self):
        actualTopDescriptors = Master.getTopDescriptorsList(flangeMountSubset)

        self.assertTrue((expectedTopCategoryDescriptors == actualTopDescriptors).all())

    def testGetTopDescriptorsInCategory(self):
        expectedTopDescriptorsDf = pd.DataFrame(
            {
                sc.CATEGORY_CODE: "10000030",
                sc.CATEGORY_NAME: "FLANGE MOUNT",
                sc.DESCRIPTOR_NAME: expectedTopCategoryDescriptors,
                sc.DISP_SEQ: [0, 1, 2],
            }
        )
        actualTopDescriptorsDf = Master.getTopDescriptorsInCategory(flangeMountSubset)

        for column in expectedTopDescriptorsDf.columns:
            self.assertTrue(
                (
                    expectedTopDescriptorsDf[column] == actualTopDescriptorsDf[column]
                ).all()
            )


if __name__ == "__main__":
    unittest.main()

# class TestCalculations(unittest.TestCase):

#     def test_sum(self):
#         calculation = Calculations(8, 2)
#         self.assertEqual(calculation.get_sum(), 10, 'The sum is wrong.')

# if __name__ == '__main__':
#     unittest.main()
