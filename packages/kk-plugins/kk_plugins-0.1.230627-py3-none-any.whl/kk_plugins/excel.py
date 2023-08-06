import pandas
import pandas as pd


class Excel(object):
    def __init__(self, file, header=0, sheet_name=0, usecols=None):
        self.__pd_header = header
        self.file = None
        self.__file_path = file
        self.__sheet_name = sheet_name
        self.__usecols = usecols
        self.__read_file()

    @property
    def data(self) -> pd.DataFrame:
        return self.file

    @property
    def items(self):
        return self.data_to_dict.values()

    @property
    def sheet_names(self):
        """
        获取所有表格名称
        :return:
        """
        file = self.__file_path
        if isinstance(file, str):
            # support file : xls,xlsx,csv
            if file.endswith('xls'):
                pass
            elif file.endswith('xlsx'):
                pass
            elif file.endswith('csv'):
                pass
            else:
                print('file type is not support')
                return

        return list(pd.read_excel(file, sheet_name=None).keys())

    @property
    def data_to_dict(self) -> dict:
        data = self.file.fillna("").values.tolist()
        if not isinstance(data, list):
            return {}
        result = {}
        for index, item in enumerate(data):
            result[index] = item
        return result

    @property
    def headers(self) -> list:
        return self.file.columns.values.tolist()

    def add_after(self, row, data):
        p_data = self.file[:row]
        n_data = self.file[row:]
        if not isinstance(data, list):
            self.file = pandas.concat([p_data, pandas.DataFrame([data]), n_data])
        elif isinstance(data, list):
            self.file = pandas.concat([p_data, pandas.DataFrame(data), n_data])

    def delete(self, row):
        p_data = self.file[:row]
        n_data = self.file[row + 1:]
        self.file = pandas.concat([p_data, n_data])

    def save(self, file_name: str = None):
        if file_name is None:
            pass
        self.file.to_excel(file_name)

    def items_fillnan(self, method="ffill", axis=0):
        """
        返回补全空格后的items

        :param method: ffill:前一个值   bfill:后一个值

        :param axis: 0:上一行  1:左边

        :return:
        """
        data = self.file.fillna(method=method, axis=axis).values.tolist()
        if not isinstance(data, list):
            return {}
        result = {}
        for index, item in enumerate(data):
            result[index] = item
        return result.values()

    def __read_file(self):
        file = self.__file_path
        if isinstance(file, str):
            # support file : xls,xlsx,csv
            if file.endswith('xls'):
                pass
            elif file.endswith('xlsx'):
                pass
            elif file.endswith('csv'):
                pass
            else:
                print('file type is not support')
                return

            self.file = pd.read_excel(file, header=self.__pd_header, sheet_name=self.__sheet_name,
                                      usecols=self.__usecols)

    def __str__(self):
        tmp = self.data_to_dict
        result = ''
        for key in tmp.keys():
            result += str(key) + ':' + str(tmp[key]) + '\n'
        return result


class ExcelItem:
    def __init__(self):
        self.__item = []

    def add(self, data):
        self.__item.append(data)

    def save(self, file_name="result.xlsx"):
        pd.DataFrame(self.__item).to_excel(file_name)
