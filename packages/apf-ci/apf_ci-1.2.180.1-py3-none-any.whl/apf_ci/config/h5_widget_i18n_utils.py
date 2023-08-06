from apf_ci.util.log_utils import logger


# 筛选H5颗粒需要做
def filter_h5_widget_uuid(widgets, defines_json, biz_comp_transform):
    #comps = init_widgets_tags_map(widgets)

    if len(biz_comp_transform.h5_widget_i18n_property_map) <= 0:
        biz_comp_transform.make_h5_widget_property_map(defines_json)
    params = filter_h5_widget_i18n_param(widgets, biz_comp_transform.h5_widget_i18n_property_map)
    return params


# 循环遍历颗粒列表，获取需要国际化的属性对应国际化key值
def filter_h5_widget_i18n_param(widgets, h5_widget_i18n_property_map):
    params = {}
    for key in widgets:
        widget = widgets[key]
        widget_key = widget['key'] + '.' + widget['widget_name']
        # 判断这个颗粒是否有需要国际化
        if widget_key in h5_widget_i18n_property_map.keys():
            i18n_property = h5_widget_i18n_property_map[widget_key]
            logger.debug('需要国际化的h5颗粒参数：'+widget_key+'.'+i18n_property)
            i18n_property_char = i18n_property.split('.')
            get_i18n_param(widget, params, i18n_property_char)
    return params

# 获取需要国际化的属性
def get_i18n_param(widget, params, i18n_property_char):
    item = widget
    i18n_property_char_length = len(i18n_property_char)
    for char_key in i18n_property_char:
        index = i18n_property_char.index(char_key)
        # 如果属性是列表，要做循环获取需要替换的i18n的key值
        if isinstance(item, list):
            i18n_property_char_item = i18n_property_char[index:]
            for list_item in item:
                get_i18n_param(list_item, params, i18n_property_char_item)
        if isinstance(item, dict):
            if char_key in item:
                item = item[char_key]
                if index == i18n_property_char_length - 1 and isinstance(item, str):
                    params[item] = ''
            else:
                break

