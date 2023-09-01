# 目的： database data  =======>  dict data/array data

def Data_Process(data, fields, data_type=0):  # （数据源，哪些字段，数组0/对象1）
    if not data_type:  # data: [obj,obj,obj,obj,obj,...]
        # 声明新 空 数组
        result = []
        for u in data:
            # 空字典
            temp = {}
            for f in fields:
                temp[f] = getattr(u, f)
            result.append(temp)

    else:  # obj
        result = {}
        for f in fields:
            result[f] = getattr(data, f)

    return result
