import selenium.webdriver
import re , os, zipfile, requests
import pandas as pd
from html_parser import MyHTMLParser
from enum import Enum

class BaseDataType(Enum):
   EXCEL = "xlsx"
   ODS = "ods"
   TXT = "txt"

class IbgeBasesScrapper():

   REGEX_BASES_DADOS_IBGE: str = r"Base \d{4}-\d{4}"
   OFFSET_STRING_BASES: int = 10 #quando achamos a string que representa a tag html com o link das bases, precisamos voltar 10 chars para pegar a tag que tem essa string
   EXTRACTED_FILES_DIR:str = "tempfiles"


   def extract_database(self, url: str, html_tag_bases:str ,data_type: BaseDataType)->pd.DataFrame:
      driver = selenium.webdriver.Chrome()
      driver.get(url)
      page_source:str = driver.page_source

      databases_match = re.finditer(self.REGEX_BASES_DADOS_IBGE, page_source) #matchs no HTML com a string que identifica as bases de dados do ibge
   
      most_recent_data = max(databases_match,key= lambda x : x.group()) #acha a data mais recente entre as matches de banco de dados, isso por que 2010 > 2000 na comparação

      html_parser = MyHTMLParser(html_tag_bases) #instancia um objeto de parser de html
      substr:str = page_source[ (most_recent_data.start()- self.OFFSET_STRING_BASES) : ]  #substr do html que começa um pouco antes (offset negativo) do match com a str que identifica
      #o banco de dados do ibge
      
      lista_links:list[str] = html_parser.get_all_links( html_parser.get_limited_html_block(substr) )  
      final_link:str = ""

      for link in lista_links:
         if data_type.value in link:
               final_link = link
         
      if not final_link:
         raise RuntimeError(f"não foi possível achar o link da base de dados com o tipo {data_type.value}")
         
      driver.quit() #fecha o webdriver 
      
      return self.__dataframe_from_link(final_link,data_type)
   
   def __download_extract_zipfile(self,url:str)->str:
      """Retorna o caminho para o arquivo que foi baixado e extraido"""

      #caso o diretório para guardar os arquivos extraidos não exista, vamos criar ele
      if not os.path.exists(self.EXTRACTED_FILES_DIR):
         os.makedirs(self.EXTRACTED_FILES_DIR)

      #baixando o arquivo zip
      response = requests.get(url)
      if response.status_code == 200:
         with open(os.path.join(self.EXTRACTED_FILES_DIR, "zip_file.zip"), "wb") as f:
            f.write(response.content)
      else:
         raise RuntimeError("Falhou em baixar o arquivo .zip, status code da resposta:", response.status_code)

      #extraindo o arquivo zip
      with zipfile.ZipFile(os.path.join(self.EXTRACTED_FILES_DIR, "zip_file.zip"), "r") as zip_ref:
            zip_ref.extractall(self.EXTRACTED_FILES_DIR)

      extracted_files:list[str] = os.listdir(self.EXTRACTED_FILES_DIR)
      
      data_file:str = ""
      for file in extracted_files:
         if ".zip" not in file:
            data_file = file
            break

      if not extracted_files or not data_file:
         raise RuntimeError("Extração do arquivo zip num diretório temporário falhou")
      
      return os.path.join(self.EXTRACTED_FILES_DIR, data_file) #retorna o caminho para o arquivo extraido

   def __dataframe_from_link(self, url:str , data_type: BaseDataType)->pd.DataFrame:
      file_path: str = self.__download_extract_zipfile(url)

      df:pd.DataFrame
      if data_type == BaseDataType.EXCEL:
         df:pd.DataFrame = pd.read_excel(file_path)

      if df is None:
         raise RuntimeError("não foi possível criar um dataframe a partir do link")
      
      return df
   
scrapper = IbgeBasesScrapper()
url = "https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html?t=downloads&c=1100023"
df:pd.DataFrame = scrapper.extract_database(url=url, html_tag_bases="li" , data_type=BaseDataType.EXCEL)

print(df.head())