import io
import os
import pythonnet
from clr_loader import get_coreclr
from pythonnet import set_runtime
import clr
import pandas as pd
import time
import sys

filedir = os.path.dirname(os.path.abspath(__file__))
dllFolder = os.path.join(filedir, 'netcore')
rt = get_coreclr(runtime_config=os.path.join(dllFolder, "ProcessHost.runtimeconfig.json"))
set_runtime(rt)
sys.path.append(dllFolder)
# info = pythonnet.get_runtime_info()

clr.AddReference('System.Data.Common')
clr.AddReference('System.Data')

from System import Data, Decimal
from System.Data import DataSet
from System.Data import DataTable
from System.Data import DataColumn
from System.Data import DataRow
from System import DBNull
# from System.IO import MemoryStream


def TableToDataFrame(dt):
    ''' Convert DataTable type to DataFrame type '''

    colTempCount = 0
    dic = {}
    while (colTempCount < dt.Columns.Count):
        li = []
        rowTempCount = 0
        column = dt.Columns[colTempCount]
        colName = column.ColumnName
        typeName = column.DataType.Name
        while (rowTempCount < dt.Rows.Count):
            result = dt.Rows[rowTempCount][colTempCount]
            try:
                if typeName == 'Decimal' and DBNull.Value != result:
                    li.append(Decimal.ToDouble(result))
                else:
                    li.append(result)
            except Exception as err:
                print(err)

            rowTempCount = rowTempCount + 1

        colTempCount = colTempCount + 1
        dic.setdefault(colName, li)

    df = pd.DataFrame(dic)

    return (df)

def DataFrameToDic(df):
    ''' Convert DataFrame data type to dictionary type '''
    dic = df.to_dict(' list ')
    return dic

def TableToDataFrame2(dt):

    # 컬럼 이름 추출
    columns = [column.ColumnName for column in dt.Columns]
    decimal_cols = [column.ColumnName for column in dt.Columns if column.DataType.Name == "Decimal"]

    data = []
    for row in dt.Rows:
        data.append([row[column] for column in columns])

    df = pd.DataFrame(data, columns=columns)
    for dcol in decimal_cols:
        df[dcol] = pd.to_numeric(df[dcol], errors='ignore')
        print(df[dcol])

    return df

def TableToDataFrame_Test(dt):
    import System.Data
    # linq 사용하기 위해서는 다음 추가필요
    clr.AddReference("System.Core")

    sys.path.append(r'<path>')

    # 컬럼 이름 추출
    columns = [column.ColumnName for column in dt.Columns]

    # rows = dt.AsEumerable()
    rows = System.Data.DataTableExtensions.AsEnumerable(dt)
    df = pd.DataFrame.from_records(rows, columns=columns)
    return df