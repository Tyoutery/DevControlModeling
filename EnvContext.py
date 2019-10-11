import itertools

import xlsxwriter

workbook = xlsxwriter.Workbook('环境语境.xlsx')
worksheet = workbook.add_worksheet()

array = list(
    itertools.product(["机器人正常", "机器人异常"], ["清洁任务暂停", "急停", "清洁任务开始", "清洁任务进行", "清洁任务结束", "无清洁任务"],
                      ["导航", "不导航"], ["处于一米栏区域", "处于扶梯区域", "处于减速带区域", "处于窄道"],
                      ["处于不可清洁区域", "处于清洁区域"], ["处于围档区域", "处于电梯区域", "处于无遮挡区域"]
                      ))

array = [x for x in array if not (("机器人异常" in x) & ("清洁任务开始" in x))]
array = [x for x in array if not (("机器人异常" in x) & ("清洁任务进行" in x))]
array = [x for x in array if not (("机器人异常" in x) & ("清洁任务结束" in x))]
array = [x for x in array if not (("机器人异常" in x) & ("导航" in x))]
array = [x for x in array if not (("急停" in x) & ("导航" in x))]
array = [x for x in array if not (("清洁任务开始" in x) & ("导航" in x))]
array = [x for x in array if not (("清洁任务开始" in x) & ("处于扶梯区域" in x))]
array = [x for x in array if not (("清洁任务开始" in x) & ("处于减速带区域" in x))]
array = [x for x in array if not (("清洁任务开始" in x) & ("处于窄道" in x))]
array = [x for x in array if not (("清洁任务开始" in x) & ("处于不可清洁区域" in x))]
array = [x for x in array if not (("清洁任务开始" in x) & ("处于电梯区域" in x))]
array = [x for x in array if not (("清洁任务进行" in x) & ("导航" in x))]
array = [x for x in array if not (("清洁任务进行" in x) & ("处于不可清洁区域" in x))]
array = [x for x in array if not (("清洁任务进行" in x) & ("处于围挡区域" in x))]
array = [x for x in array if not (("清洁任务进行" in x) & ("处于电梯区域" in x))]
array = [x for x in array if not (("清洁任务结束" in x) & ("处于扶梯区域" in x))]
array = [x for x in array if not (("清洁任务结束" in x) & ("处于减速带区域" in x))]
array = [x for x in array if not (("清洁任务结束" in x) & ("处于窄道" in x))]
array = [x for x in array if not (("清洁任务结束" in x) & ("处于不可清洁区域" in x))]
array = [x for x in array if not (("清洁任务结束" in x) & ("处于电梯区域" in x))]
array = [x for x in array if not (("无清洁任务" in x) & ("处于不可清洁区域" in x))]
array = [x for x in array if not (("处于扶梯区域" in x) & ("处于可清洁区域" in x))]
array = [x for x in array if not (("处于扶梯区域" in x) & ("处于电梯区域" in x))]
array = [x for x in array if not (("处于扶梯区域" in x) & ("处于无遮挡区域" in x))]
array = [x for x in array if not (("处于减速带区域" in x) & ("处于可清洁区域" in x))]
array = [x for x in array if not (("处于减速带区域" in x) & ("处于电梯区域" in x))]
array = [x for x in array if not (("处于可清洁区域" in x) & ("处于电梯区域" in x))]

print(array)

col = 0

for row, data in enumerate(array):
    worksheet.write_row(row, col, data)

workbook.close()
