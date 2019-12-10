import pandas as pd
from StateCreater import ContextDeviceStateCreator


def get_matrix(filename, sheetname):
    matrix_dframe = pd.read_excel(filename, sheetname=sheetname)
    matrix = [list(values.dropna()) for _, values in matrix_dframe.items()]
    return matrix


def get_constraint(filename, sheetname):
    constraint_dframe = pd.read_excel(filename, sheetname=sheetname)
    limits = {title: list(values.dropna()) for title, values in constraint_dframe.items()}
    return limits


if __name__ == '__main__':
    name = "配置.xlsx"
    sheet1 = '设备控制'
    sheet2 = '设备约束'
    sheet3 = '语境'
    sheet4 = '语境约束'
    sheet5 = '映射约束'

    device_array = get_matrix(name, sheet1)
    device_limits = get_constraint(name, sheet2)
    context_array = get_matrix(name, sheet3)
    context_limits = get_constraint(name, sheet4)
    combined_limits = get_constraint(name, sheet5)

    context_device_state = ContextDeviceStateCreator(context_array, context_limits,
                                                     device_array, device_limits,
                                                     combined_limits)

    context_device_state.build()



