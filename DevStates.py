import itertools

import xlsxwriter

workbook = xlsxwriter.Workbook('设备状态.xlsx')
worksheet = workbook.add_worksheet()

array = list(
    itertools.product(["运动到点", "运动到线", "运动到面", "停止"], ["边刷旋转", "边刷停转"], ["边刷上升", "边刷下降", "边刷不放", "边刷放下"], ["喷水", "不喷水"],
                      ["吸水趴升", "吸水趴降", "吸水趴不放", "吸水趴放下"], ["吸风开", "吸风关"], ["过滤开", "过滤关"]))

array = [x for x in array if not (("停止" in x) & ("喷水" in x))]
array = [x for x in array if not (("停止" in x) & ("边刷旋转" in x))]
array = [x for x in array if not (("边刷旋转" in x) & ("吸风关" in x))]
array = [x for x in array if not (("边刷停转" in x) & ("喷水" in x))]
array = [x for x in array if not (("边刷上升" in x) & ("喷水" in x))]
array = [x for x in array if not (("边刷下降" in x) & ("喷水" in x))]
array = [x for x in array if not (("边刷不放" in x) & ("喷水" in x))]
array = [x for x in array if not (("喷水" in x) & ("吸水趴升" in x))]
array = [x for x in array if not (("喷水" in x) & ("吸水趴降" in x))]
array = [x for x in array if not (("喷水" in x) & ("吸水趴不放" in x))]
array = [x for x in array if not (("喷水" in x) & ("吸风关" in x))]
array = [x for x in array if not (("吸水趴升" in x) & ("吸风开" in x))]
array = [x for x in array if not (("吸水趴降" in x) & ("吸风开" in x))]
array = [x for x in array if not (("吸水趴不放" in x) & ("吸风开" in x))]

print(array)

col = 0

for row, data in enumerate(array):
    worksheet.write_row(row, col, data)

workbook.close()
