I've been taking a look to understand the problem. Here's my recap, please look it over to confirm that I have the right understanding:

# Context:
1) The `category-descriptor` sheet contains the descriptor for each product in that category. The `destination` table populates those expected measurements with the actual values.
    - If descriptor A is in the `category-descriptor` sheet but not in the `destination` sheet, that field is shown as blank on the website.
    - If descriptor A is in the `destination` sheet but not in the `category-descriptor` sheet, that field isn't shown at all on the website.
    - If descriptor A is found in both sheets, then the field is shown on the website with a measurement.
2) As a regular part of your work, you need to upload this `destination` and `category-descriptor` sheets to the ecommerce website Unilog. If I understand correctly, the status quo solution is to populate all 5000 of the items in Excel, rather than automation, so a lot of filtering and copying and pasting.

# Problem:
1) You need to populate the descriptor columns in the `destination` sheet, where the set of descriptors `A` is a subset of the set of descriptors for that product's category.
2) You need to add a number of descriptors to the `category-descriptor` sheet, where the set of descriptors `A` are actually measured by most of that category's items
    - I would need some input on how many unique descriptors to select. For example, should categories be populated with every unique descriptor that is found in, say, 70% of that category's items? Or should the categories have 5 unique descriptors, to match the 5 categories in the `destination` sheet?

# The product you want from me:
A script that produces the following:
1) A list of the most dominant descriptors grouped by category, ideally added as rows to the `category-descriptor` sheet.
    - This is sourced from the `master_source` sheet and an unknown map of vendor category to ecommerce category.
    - If I understand correctly, you've already mapped the `categories` column in the `master_source` sheet to your own ecommerce categories, so you really just need the descriptors grouped by the vendor categories.
2) A modified `destination` sheet with the `descriptor` columns populated. This is sourced from `category-descriptor` and values from `master_source`
    - For each row, the script would fetch descriptors for that item's category from `category-descriptor`.
    - For each descriptor, the script would then find the values for that part number (which I'm assuming is unique) in the `master_source` sheet.
    - As an example, here's the first descriptor to the first row

| Descriptor Name1 | Descriptor Value1 | Descriptor UOM1
|--------------|-----------|------------|
| Base to Center Height | 2.500 | INCHES |