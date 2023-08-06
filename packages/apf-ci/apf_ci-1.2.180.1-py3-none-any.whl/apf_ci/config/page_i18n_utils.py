import json
import urllib.request
import urllib.parse
import ssl
from apf_ci.util.log_utils import logger

def init_pages_tags_map(pages):
    pageTags = []
    for page in pages:
        if "__type" not in page:
            continue
        if page["__type"] != "plugin":
            continue
        if "_page_name" not in page:
            continue
        if "tag_name" not in page:
            continue
        pageTags.append({"page_name": page["_page_name"], "tag_name": page["tag_name"]})
    return pageTags


def http_post_json(url, data):
    if len(data) == 0:
        return {}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    body = json.dumps(data).encode("utf-8")
    request = urllib.request.Request(url, headers=headers, data=body)
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(request, context=context)
    return json.load(response)


def filter_i18n_properties_name(defines):
    i18n_name_map = {}
    for define in defines.values():
        if "pages" not in define.keys():
            continue
        for page_name, page in define["pages"].items():
            if "properties" not in page.keys():
                continue
            for key, value in page["properties"].items():
                if "_elementType" not in value.keys():
                    continue
                    #解析property
                if value["_elementType"] == "property":
                    if "_i18n" not in value.keys():
                        continue
                    if str(value["_i18n"]).lower() == "true":
                        if page_name not in i18n_name_map:
                            i18n_name_map[page_name] = set()
                        i18n_name_map[page_name].add(key)
                #解析group
                elif value["_elementType"] == "group":
                    if not isinstance(value, dict):
                        continue
                    for property_name, property in value.items():
                        if not isinstance(property, dict):
                            continue
                        if "_i18n" not in property.keys():
                            continue
                        if str(property["_i18n"]).lower() == "true":
                            if page_name not in i18n_name_map:
                                i18n_name_map[page_name] = set()
                            i18n_name_map[page_name].add(key + "." + property_name)
    return i18n_name_map


def filter_i18n_properties_uuid(pages, i18n_name_map):
    i18n_uuid_map = {}
    for page in pages:
        if "__type" not in page:
            continue
        if page["__type"] != "plugin":
            continue
        if "_page_name" not in page.keys():
            continue
        if "properties" not in page.keys():
            continue
        if page["_page_name"] not in i18n_name_map:
            continue
        i18n_name_set = i18n_name_map[page["_page_name"]]
        for key, value in page["properties"].items():
            #解析property
            if isinstance(value, str):
                if key in i18n_name_set:
                    if page["_page_name"] not in i18n_uuid_map:
                        i18n_uuid_map[page["_page_name"]] = set()
                    i18n_uuid_map[page["_page_name"]].add(value)
            #解析group
            elif isinstance(value, list):
                for group in value:
                    if not isinstance(group, dict):
                        continue
                    for property_name, property_value in group.items():
                        if key + "." + property_name in i18n_name_set:
                            if page["_page_name"] not in i18n_uuid_map:
                                i18n_uuid_map[page["_page_name"]] = set()
                            i18n_uuid_map[page["_page_name"]].add(property_value)
    return i18n_uuid_map

#重建UUID集合
def recreate_uuid_map(i18n_uuid_map):
    map = {}
    for set in i18n_uuid_map.values():
        for uuid in set:
            map[uuid] = ""
    return map


def filter_page_uuid(pages, url):
    logger.debug(pages)
    tags = init_pages_tags_map(pages)
    logger.debug(tags)
    defines = http_post_json(url, tags)
    logger.debug(defines)
    i18n_name_map = filter_i18n_properties_name(defines)
    logger.debug(i18n_name_map)
    i18n_uuid_map = filter_i18n_properties_uuid(pages, i18n_name_map)
    logger.debug(i18n_uuid_map)
    return recreate_uuid_map(i18n_uuid_map)
