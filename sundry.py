from __future__ import print_function

import xlrd
import pprint


class Sundry():
    def __init__(self, fileName):
        self.fileName = fileName
        self.supplies = []
        self.equipment = []
        xl_workbook = xlrd.open_workbook(self.fileName)

        # List sheet names, and pull a sheet by name
        sheet_names = xl_workbook.sheet_names()

        xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])

        # Or grab the first sheet by index
        #  (sheets are zero-indexed)
        xl_sheet = xl_workbook.sheet_by_index(0)

        num_rows = xl_sheet.nrows

        # format and store in lists
        for i in range(0, num_rows):
            curr_cell_paint = str(xl_sheet.cell(i, 0))
            curr_cell_equip = str(xl_sheet.cell(i, 1))
            if 'empty' in curr_cell_paint or 'empty' in curr_cell_equip:
                break
            if "text:" in curr_cell_paint or "text:" in curr_cell_equip:
                self.supplies.append(curr_cell_paint.replace("text:", '').strip("'"))
                self.equipment.append(curr_cell_equip.replace("text:", '').strip("'"))

    def get_supplies(self):
        return self.supplies

    def get_equipment(self):
        return self.equipment
