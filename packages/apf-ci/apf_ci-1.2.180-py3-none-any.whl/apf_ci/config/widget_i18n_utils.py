import json
import urllib.request
import urllib.parse
import ssl
from apf_ci.util.log_utils import logger
#创建widgets版本列表
def init_widgets_tags_map(widgets):
    widgetTags=[]
    for widget in widgets.values():
        if "widget_name" not in widget.keys():
            continue
        widget_name=widget["widget_name"]
        if "tag_name" not in widget.keys():
            continue
        tag_name=widget["tag_name"]
        widgetTags.append({"widget_name":widget_name,"tag_name":tag_name})
    return widgetTags

# 查询widgets define
def http_post_json(url,data):
    if len(data)==0:
        return {}
    headers={
        "Content-Type":"application/json",
        "Accept":"application/json"
    }
    body=json.dumps(data).encode("utf-8")
    request=urllib.request.Request(url,headers=headers,data=body)
    context = ssl._create_unverified_context()
    response= urllib.request.urlopen(request,context=context)
    return json.load(response)

#筛选国际化资源名字
def filter_i18n_properties_name(defines):
    i18n_name_map={}
    for define in defines.values():
        if "widgets" not in define.keys():
            continue
        for widget_name,widget in define["widgets"].items():
            if "properties" not in widget.keys():
                continue
            for key,value in widget["properties"].items():
                if "_elementType" not in value.keys():
                    continue
                #解析property
                if value["_elementType"]=="property":
                    if "_i18n" not in value.keys():
                        continue
                    if str(value["_i18n"]).lower()=="true":
                        if widget_name not in i18n_name_map:
                            i18n_name_map[widget_name]=set()
                        i18n_name_map[widget_name].add(key)
                #解析group
                elif value["_elementType"]=="group":
                    if not isinstance(value,dict):
                        continue
                    for property_name,property in value.items():
                        if not isinstance(property,dict):
                            continue
                        if "_i18n" not in property.keys():
                            continue
                        if str(property["_i18n"]).lower()=="true":
                            if widget_name not in i18n_name_map:
                                i18n_name_map[widget_name]=set()
                            i18n_name_map[widget_name].add(key+"."+property_name)
    return i18n_name_map

#筛选国际化资源UUID
def filter_i18n_properties_uuid(widgets,i18n_name_map):
    i18n_uuid_map={}
    for widget in widgets.values():
        if "widget_name" not in widget.keys():
            continue
        if "properties" not in widget.keys():
            continue
        if widget["widget_name"] not in i18n_name_map:
            continue;
        i18n_name_set=i18n_name_map[widget["widget_name"]]
        for key,value in widget["properties"].items():
            #解析property
            if isinstance(value,str):
                if key in i18n_name_set:
                    if widget["widget_name"] not in i18n_uuid_map:
                        i18n_uuid_map[widget["widget_name"]]=set()
                    i18n_uuid_map[widget["widget_name"]].add(value)
            #解析group
            elif isinstance(value,list):
                for group in value:
                    if not isinstance(group,dict):
                        continue
                    for property_name,property_value in group.items():
                        if key+"."+property_name in i18n_name_set:
                            if widget["widget_name"] not in i18n_uuid_map:
                                i18n_uuid_map[widget["widget_name"]]=set()
                            i18n_uuid_map[widget["widget_name"]].add(property_value)
    return i18n_uuid_map

#重建UUID集合
def recreate_uuid_map(i18n_uuid_map):
    map={}
    for set in i18n_uuid_map.values():
        for uuid in set:
            map[uuid]=""
    return map

#入口
def filter_widget_uuid(widgets,url):
    tags=init_widgets_tags_map(widgets)
    logger.debug("获取颗粒链接："+url)
    logger.debug("获取颗粒data：")
    logger.debug(tags)
    defines=http_post_json(url,tags)
    logger.debug("获取颗粒返回数据：")
    logger.debug(defines)
    i18n_name_map=filter_i18n_properties_name(defines)
    i18n_uuid_map=filter_i18n_properties_uuid(widgets,i18n_name_map)
    return recreate_uuid_map(i18n_uuid_map)






