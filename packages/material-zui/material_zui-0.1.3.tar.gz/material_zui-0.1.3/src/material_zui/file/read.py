from collections import defaultdict
import json
from typing import DefaultDict
from pyparsing import Any

from .write import write_to_last
from material_zui.list import get_diff
from material_zui.string import remove_all
from material_zui.utility import pipe_list


def read_file_to_list(filename: str) -> list[str]:
    with open(filename, "r") as f:
        lines = f.readlines()
    return pipe_list(remove_all('\n'))(lines)


def load_json_object(json_file_path: str) -> DefaultDict[str, str]:
    '''
    Load json file data to dict type
    @json_file_path: json file path
    @return: dict json data
    '''
    with open(json_file_path, encoding='utf-8') as json_data:
        return defaultdict(str, json.load(json_data))


def load_json_array(json_file_path: str) -> list[dict[Any, Any]]:
    '''
    Load json file data to list type
    @json_file_path: json file path
    @return: list json data
    '''
    with open(json_file_path, "r") as f:
        data = json.load(f)
    return list(data)


def read_json(json_file_path: str):
    '''
    Read json file and return content value
    @return: `dict` for json object, otherwise `list dict` for json array
    - ex: using: `data[0]` or `data['field_value']`
    '''
    return json.loads(open(json_file_path, encoding="utf-8").read())


def load_diff_line(file_urls_path: str, input_urls: list[str], is_write_file: bool = False) -> list[str]:
    saved_urls = read_file_to_list(file_urls_path)
    diff_urls = get_diff(input_urls, saved_urls)
    print("New lines", len(diff_urls))
    print("Duplicate lines", len(input_urls)-len(diff_urls))
    if is_write_file:
        write_to_last(file_urls_path, '\n---New lines---\n' +
                      "\n".join(diff_urls))
    return diff_urls
