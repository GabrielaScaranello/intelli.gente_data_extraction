from enum import Enum
from typing import Any

class DataPointTypes(Enum): #Enum para os tipos de dados encontrados nas bases 
   INT = "int"
   FLOAT = "float"
   STRING = "str"
   BOOL = "bool"

class DataPoint(): #clase para um ponto de dado específico encontrado na tabela de dados brutos
   data_category:str
   data_name: str
   column_name:str
   data_type: DataPointTypes
   multiply_amount: int  #algumas vezes os dados vão vir em escala de 1 equivale a 1000 ou similares, então é necessário
   #guardar por quanto esse valor deve ser multiplicado

   def __init__(
      self,
      data_category:str,
      data_name:str,
      column_name:str,
      data_type:DataPointTypes, 
      multiply_amount: int | None = None
   )-> None:
      
      self.data_category = data_category
      self.data_name:str =  data_name
      self.column_name:str = column_name
      self.data_type: DataPointTypes = data_type
      multiply_amount: int | float | None = multiply_amount
     
      if multiply_amount is None:
         self.multiply_amount = 1
      else:
         if self.data_type not in [DataPointTypes.INT, DataPointTypes.FLOAT]:
            raise IOError("Valor de multiplicação não é valido para tipos que não sejam inteiros ou float")
         self.multiply_amount = multiply_amount

   def multiply_value(self, value:Any)-> int | float:
      if self.data_type not in [DataPointTypes.INT, DataPointTypes.FLOAT]:
         return value
      else:
         return value * self.multiply_amount
      
class TableDataPoints(): #classe para agregar todos os pontos de dados extraido de uma tabela de dados
   
   year_column_name: str #nome da coluna que tem a info do ano
   city_code_column:str #nome da coluna que tem a info do código do município
   data_point_list: list[DataPoint] #lista de pontos de dados específicos

   def __init__(self, year_column_name:str, city_code_column:str) -> None:
      self.year_column_name = year_column_name
      self.city_code_column = city_code_column
      self.data_point_list = []

   def add_data_point(
      self,
      data_category:str,
      data_name:str,
      column_name:str,
      data_type:DataPointTypes,
      multiply_amount: int | None = None
   )->None:
      self.data_point_list.append(DataPoint(data_category,data_name,column_name,data_type,multiply_amount))

   def add_data_point_dict(self,data_dict:dict[str, str|int])->None:
      data_category:str = data_dict["data_category"]
      data_name:str = data_dict["data_name"]
      column_name:str = data_dict["column_name"]
      data_type:DataPointTypes = data_dict["data_type"]
      multiply_amount: int | None = data_dict.get("multiply_amount")

      self.data_point_list.append(DataPoint(data_category,data_name,column_name,data_type,multiply_amount))

   def add_data_points_dicts(self, dict_list: list[dict[str, str|int]])->None:
      for data_point in dict_list:
          self.add_data_point_dict(data_point)