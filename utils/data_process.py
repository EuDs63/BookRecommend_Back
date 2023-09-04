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


# 对paginate_result进行处理
def Paginate_Process(data_pagination, current_page,fields):
    result = {}
    total_pages = data_pagination.pages # 获取总页数
    total_records = data_pagination.total  # 获取总记录数
    per_page = data_pagination.per_page
    if current_page > total_pages:
        result['code'] = -1
        result['msg'] = "请求的current_page已超出"
    else:
        result['books'] = Data_Process(data_pagination, fields, 0)
        result['code'] = 0
    result['total_records'] = total_records
    result['total_pages'] = total_pages
    result['per_page'] = per_page
    return result
