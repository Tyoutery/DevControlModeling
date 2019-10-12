import itertools

import xlsxwriter

############################ 创建输出文件 ######################################

workbook_device = xlsxwriter.Workbook('设备状态.xlsx')
worksheet_device = workbook_device.add_worksheet()

workbook_context = xlsxwriter.Workbook('环境语境.xlsx')
worksheet_context = workbook_context.add_worksheet()

workbook_context_dev = xlsxwriter.Workbook('语境设备映射.xlsx')
worksheet_context_dev = workbook_context_dev.add_worksheet()
################################################################################


############################# 设定设备状态,设备内部约束 ################################################################

## 设备状态
dev_array = [["运动到点", "运动到线", "运动到面", "停止"], ["边刷旋转", "边刷停转"], ["边刷上升", "边刷下降", "边刷不放", "边刷放下"], ["喷水", "不喷水"],
             ["吸水趴升", "吸水趴降", "吸水趴不放", "吸水趴放下"], ["吸风开", "吸风关"]]
## 设备内部约束
dev_limits_internal = {'停止': ["喷水"],
                       '边刷旋转': ["吸风关"],
                       '边刷停转': ["喷水"],
                       '边刷上升': ["喷水"],
                       '边刷下降': ["喷水"],
                       '边刷不放': ["喷水"],
                       '喷水': ["吸水趴升", "吸水趴降", "吸水趴不放", "吸风关"],
                       '吸水趴升': ["吸风开"],
                       '吸水趴降': ["吸风开"],
                       '吸水趴不放': ["吸风开"]}

#######################################################################################################################

################################# 设定语境，语境内部约束，语境设备映射 #################################################

## 语境
context_array = [["机器人正常", "机器人异常"], ["清洁任务暂停", "急停", "清洁任务开始", "清洁任务进行", "清洁任务结束", "无清洁任务"],
                 ["导航", "不导航"], ["可运动", "不可运动"],
                 ["不可清洁区域", "可清洁区域"]]
## 语境内部约束
context_limits_internal = {'机器人异常': ["清洁任务开始", "清洁任务进行", "清洁任务结束", "导航"],
                           '急停': ["清洁任务开始", "清洁任务进行", "导航"],
                           '清洁任务暂停': ["导航"],
                           '清洁任务开始': ["导航", "不可运动"],
                           '清洁任务进行': ["导航", "不可运动", "不可清洁区域"],
                           '清洁任务结束': ["不可运动", "不可清洁区域"],
                           '导航': ["不可运动"],
                           }
## 语境设备映射（排除规则）
context_dev_conflict_dictionary = {'机器人异常': ["运动到点", "运动到线", "运动到面", "边刷旋转", "喷水", "吸风开"],
                                   '急停': ["运动到点", "运动到线", "运动到面", "边刷旋转", "喷水", "吸风开"],
                                   '不可运动': ["运动到点", "运动到线", "运动到面", "边刷旋转", "喷水", "吸风开"],
                                   '清洁任务暂停': ["边刷旋转", "喷水", "吸风开"],
                                   '无清洁任务': ["边刷旋转", "喷水", "吸风开"],
                                   '不可清洁区域': ["边刷旋转", "喷水", "吸风开"],
                                   '清洁任务开始': ["运动到点", "运动到线", "运动到面", "边刷停转", "边刷上升", "边刷不放", "吸水趴升", "吸水趴不放", "吸风关"],
                                   '清洁任务进行': ["边刷停转", "边刷上升", "边刷下降", "边刷不放", "不喷水", "吸水趴升", "吸水趴降", "吸水趴不放", "吸风关"],
                                   '清洁任务结束': ["边刷旋转", "边刷上升", "边刷下降", "边刷放下", "喷水", "吸水趴升",
                                              "吸水趴降", "吸水趴放下", "吸风开"],
                                   '导航': ["停止", "边刷上升", "边刷下降", "吸水趴升", "吸水趴降"],
                                   }
#####################################################################################################################


################################# 计算设备状态空间及输出#############################################################


## step1 计算所有的设备状态
dev_states = list(itertools.product(*dev_array))
## step2 增加设备内部约束
for key in dev_limits_internal.keys():
    for item in dev_limits_internal.get(key):
        dev_states = [x for x in dev_states if not ((key in x) & (item in x))]

# print(dev_states)
## step3 输出到文件
col = 0

for row, data in enumerate(dev_states):
    worksheet_device.write_row(row, col, data)

workbook_device.close()
#####################################################################################################################


################################# 计算语境状态空间及输出#############################################################


## step1 计算所有的语境状态
context_array = list(itertools.product(*context_array))
## step2 增加语境内部约束
for key in context_limits_internal.keys():
    for item in context_limits_internal.get(key):
        context_array = [x for x in context_array if not ((key in x) & (item in x))]

# print(context_array)
## step3 输出到文件
col = 0

for row, data in enumerate(context_array):
    worksheet_context.write_row(row, col, data)

workbook_context.close()
#####################################################################################################################


################################# 计算语境设备映射并输出#############################################################

## step1 以语境状态数组为基础，创建一个一维数组作为映射的keys
context_dev_keys = []
for array in context_array:
    context_dev_keys.append(",".join(array))
# print(context_dev_keys)

## step2 创建一个字典，里面有所有语境状态组成的key，以及每个key对应的可能存在的设备状态空间
context_dev_dict = dict()


## 根据key分解出来的元素，逐一去语境设备映射字典遍历所有的限制条件,以设备状态空间数组为池子过滤，加到字典对应的key里
def func_filter(dic_key, states_array):
    context_dev_conflict_keys = dic_key.split(",")
    for conflict_key in context_dev_conflict_keys:
        if context_dev_conflict_dictionary.get(conflict_key) is None:
            continue
        for dic_item in context_dev_conflict_dictionary.get(conflict_key):
            states_array = [x for x in states_array if not (dic_item in x)]
    return states_array


## step3 组成语境——可能设备状态集合字典
for context_key in context_dev_keys:
    if context_key in context_dev_dict:
        # 如果已经存在key，追加
        context_dev_dict[context_key] = func_filter(context_key, dev_states)
    else:
        context_dev_dict[context_key] = func_filter(context_key, dev_states)

print(context_dev_dict)

## step4 输出到文件
row = 0
for key in context_dev_dict.keys():
    worksheet_context_dev.write(row, 0, key)
    col = 1
    for value in context_dev_dict[key]:
        state = "-".join(value)
        worksheet_context_dev.write(row, col, state)
        col += 1
    row += 1

workbook_context_dev.close()
#####################################################################################################################
