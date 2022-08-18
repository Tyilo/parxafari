import json

import xlsxwriter

TEAM_NAMES = [
    "dat1",
    "dat2",
    "dat3",
    "dat4",
    "dat5",
    "dat6",
    "dat7",
    "dav",
    "fys1",
    "fys2",
    "fys3",
    "fys4",
    "fys5",
    "mat1",
    "mat2",
    "mat3",
    "møk1",
    "møk2",
    "nano",
    "it1",
    "it2",
    "TK",
    "hold1",
    "hold2",
]

ACTIVITY_NAMES = [
    "Post 1",
    "Post 2",
    "Post 3",
    "Post 4",
    "Post 5",
    "Pause",
]

ROUND_NAMES = [
    "14:15-14:25",
    "14:35-14:45",
    "14:55-15:05",
    "15:15-15:25",
    "15:35-15:45",
    "15:55-16:05",
]

with open("solution.json") as f:
    solution = json.load(f)


with xlsxwriter.Workbook("timetable.xlsx") as workbook:
    worksheet = workbook.add_worksheet()

    round_name_format = workbook.add_format()
    round_name_format.set_bold()
    round_name_format.set_font_size(30)
    round_name_format.set_align("center")
    round_name_format.set_border()

    activity_name_format = workbook.add_format()
    activity_name_format.set_bold()
    activity_name_format.set_border()

    team_name_format = workbook.add_format()
    team_name_format.set_border()

    row = 0
    for round_name, round_activities in zip(ROUND_NAMES, solution):
        worksheet.merge_range(row, 0, row, 4, round_name, round_name_format)
        worksheet.set_row(row, height=30)
        row += 1
        for activity_name, teams in zip(ACTIVITY_NAMES, round_activities):
            worksheet.write(row, 0, activity_name, activity_name_format)
            for i, team in enumerate(teams):
                worksheet.write(row, i + 1, TEAM_NAMES[team], team_name_format)

            row += 1

        row += 2
