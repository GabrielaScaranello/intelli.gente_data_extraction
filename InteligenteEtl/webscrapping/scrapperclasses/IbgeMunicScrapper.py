from datastructures import BaseFileType
from .IbgePibCidadesScrapper import IbgePibCidadesScrapper
from datastructures import YearDataPoint

class IbgeBasesMunicScrapper(IbgePibCidadesScrapper):
   
   #a base MUNI de municípios do IBGE  tem um link diferente para os dados de cada ano, pelo menos isso é oq da pra ver no HTML da página
   URL_FOR_EACH_YEAR:dict[int,str] = {
      2019 : "https://www.ibge.gov.br/estatisticas/sociais/educacao/10586-pesquisa-de-informacoes-basicas-municipais.html?edicao=29466&t=downloads",
      2020 :  "https://www.ibge.gov.br/estatisticas/sociais/educacao/10586-pesquisa-de-informacoes-basicas-municipais.html?edicao=32141&t=downloads",
      2021 : "https://www.ibge.gov.br/estatisticas/sociais/educacao/10586-pesquisa-de-informacoes-basicas-municipais.html?edicao=35765&t=downloads",
   }

   file_type: BaseFileType
   priority_to_series_len: bool
   url: str #url colocado aqui para compatibilidade com a classe pai

   def __init__(self,file_type: BaseFileType,priority_to_series_len: bool = False) -> None:
      self.file_type = file_type
      self.priority_to_series_len = priority_to_series_len

   def extract_database(self)-> list[YearDataPoint]:
      """
      TODO
      como estamos falando de um arquivo EXCEL, ver se a sheet recuperada no dataframe por padrão é a sheet certa para a extração
      """
      file_links_by_year:dict[int,str] = self._get_all_files()
      print(file_links_by_year)

      data_list: list[YearDataPoint] = []
      for year,url in file_links_by_year.items():
         df = super()._dataframe_from_link(url,self.file_type,False)
         data_list.append(
             YearDataPoint(df,year)
         )
      
      return data_list
      
   def _get_all_files(self)->dict[int,str]:
      file_links_by_year:dict = {}
      
      for year,page_url in self.URL_FOR_EACH_YEAR.items():
          self.url = page_url
          file_link:str = super()._get_file_link()
          file_links_by_year[year] = file_link
      
      return file_links_by_year

