from typing import TypeAlias, Any

ZuiFile = dict[{'name': str, 'ext': str, 'file_name': str, 'dir_name': str}]

ZuiExcelColumn: TypeAlias = dict[
    {
        'field': str,
        'name': str,
        # 'type': Optional[str],
        # 'width': Optional[str],
        # 'format': Optional[str]
    }
]

ZuiExcelColumns: TypeAlias = list[ZuiExcelColumn]

ZuiExcelDataItem = dict[str, Any]

ZuiExcelData = list[ZuiExcelDataItem]
