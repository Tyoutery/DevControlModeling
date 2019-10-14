import itertools
import xlsxwriter


def make_state(array, limits):
    ## step1 计算所有的设备状态
    dev_states = list(itertools.product(*array))
    ## step2 增加设备内部约束
    for key in limits.keys():
        for item in limits[key]:
            dev_states = [x for x in dev_states if not ((key in x) & (item in x))]
    return dev_states


class StateCreator:
    def __init__(self, devices, limits, name):
        name = name.lower().strip()
        assert name in ['device', 'context']

        self.devices = devices
        self.limits = limits
        self.name = name

    def make_sheet(self):
        workbook_device = xlsxwriter.Workbook(self.name + '.xlsx')
        worksheet_device = workbook_device.add_worksheet()

        dev_states = make_state(self.devices, self.limits)

        col = 0

        for row, data in enumerate(dev_states):
            worksheet_device.write_row(row, col, data)

        workbook_device.close()


class ContextDeviceStateCreator:
    def __init__(self, context_array, context_limits, dev_array, dev_limits, combined_limits):
        self.context_array = context_array
        self.context_limits = context_limits
        self.dev_array = dev_array
        self.dev_limits = dev_limits
        self.context_states = None
        self.dev_states = None

        self.limits = combined_limits
        self.workbook = xlsxwriter.Workbook('设备语境映射.xlsx')

    def make_device_sheet(self):
        worksheet_device = self.workbook.add_worksheet("设备状态")

        assert self.dev_states

        col = 0
        for row, data in enumerate(self.dev_states):
            worksheet_device.write_row(row, col, data)

    def make_context_sheet(self):
        worksheet_device = self.workbook.add_worksheet("语境状态")

        assert self.dev_states

        col = 0
        for row, data in enumerate(self.context_states):
            worksheet_device.write_row(row, col, data)

    def make_combined_sheet(self):
        worksheet_context_dev = self.workbook.add_worksheet("设备语境状态")

        ## step1 以语境状态数组为基础，创建一个一维数组作为映射的keys
        assert self.dev_states
        assert self.context_states

        context_dev_keys = []
        for array in self.context_states:
            context_dev_keys.append(",".join(array))
        # print(context_dev_keys)

        ## step2 创建一个字典，里面有所有语境状态组成的key，以及每个key对应的可能存在的设备状态空间
        context_dev_dict = dict()

        ## 根据key分解出来的元素，逐一去语境设备映射字典遍历所有的限制条件,以设备状态空间数组为池子过滤，加到字典对应的key里
        def func_filter(dic_key, states_array):
            context_dev_conflict_keys = dic_key.split(",")
            for conflict_key in context_dev_conflict_keys:
                if self.limits.get(conflict_key) is None:
                    continue
                for dic_item in self.limits.get(conflict_key):
                    states_array = [x for x in states_array if not (dic_item in x)]
            return states_array

        ## step3 组成语境——可能设备状态集合字典
        for context_key in context_dev_keys:
            if context_key in context_dev_dict:
                # 如果已经存在key，追加
                context_dev_dict[context_key] = func_filter(context_key, self.dev_states)
            else:
                context_dev_dict[context_key] = func_filter(context_key, self.dev_states)

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

        # workbook_context_dev.close()

    def build(self):
        self.context_states = make_state(self.context_array, self.context_limits)
        self.dev_states = make_state(self.dev_array, self.dev_limits)

        self.make_device_sheet()
        self.make_context_sheet()
        self.make_combined_sheet()

        self.workbook.close()

