import json
import logging
import os
import requests

from .exceptions import AuthorizationError, BadRequestError, WiseDataInternalError, TranslationError
from dotenv import load_dotenv
from requests.exceptions import RequestException
from retry import retry


class WiseData:
  """Creates a new WiseData API client."""
  def __init__(
    self, 
    api_base="https://wisedata.vercel.app/api",
    api_key=None
  ):
    load_dotenv()
    self.api_base = api_base if api_base else os.getenv("WISEDATA_API_BASE")
    self.api_key = api_key if api_key else os.getenv("WISEDATA_API_KEY")
  
  def sql(self, query, dataframes, code=False):
    """
    Transforms given dataframes based on given SQL query.

    Parameters:
    -----------
    query: str
      SQL query to be executed.
    dataframes: dict
      Dictionary of dataframes to be transformed.
      The key is the dataframe name and the value is the dataframe itself.
      Example:
      {"customers_df": customers_df, "employees_df": employees_df}
    Code: bool
      Whether to print/log the pandas code used to transformed dataframes or not.
    """
    return self._sql(query, dataframes, code=code)

  @retry(exceptions=(RequestException, WiseDataInternalError), tries=3, delay=2)
  def _sql(self, query, dataframes, error=None, code=False, num_retries=0, prev_code=None):
    if not (type(dataframes) is dict): raise Exception("dataframes needs to be a dictionary with key being dataframe name and value being the dataframe.")
    if num_retries >= 2:
      logging.error(f"We couldn't translate your query. Here is python code we attempted to generate: \n{prev_code}")
      raise TranslationError()

    data = {
      "dataframe": "\n".join([f"{idx+1}. Dataframe named {key} with columns {value.columns.tolist()}" for idx, (key, value) in enumerate(dataframes.items())]),
      "sql": query,
      "error": error
    }

    response = requests.post(
      self.api_base + "/sql2pandas", 
      data=json.dumps(data), 
      headers={
        "Authorization": "Bearer " + self.api_key,
        "content-type": "application/json"
      }
    )

    if (response.status_code == 400): raise BadRequestError(response.text)
    if (response.status_code == 401): raise AuthorizationError()
    if (response.status_code >= 500): raise WiseDataInternalError()

    python_code = response.json()

    import pandas as pd
    import numpy as np
    globals = { "np": np, "pd": pd }
    locals = dataframes.copy()
    try:
      exec(python_code, globals, locals)
      if isinstance(locals["return_df"], pd.DataFrame):
        return_df=locals["return_df"].reset_index(drop=True)
        if code: logging.info(f"Given query: \n{query} \nOutput code: \n{python_code}\n")
      else:
        num_retries += 1
        data["error"] = "Is not a pandas dataframe. Please return dataframe."
        return_df = self._sql(query, dataframes, error=data["error"], code=code, num_retries=num_retries, prev_code=python_code)
    except Exception as e:
      num_retries += 1
      data["error"] = f"Threw exception: `{e}`"
      return_df = self._sql(query, dataframes, error=data["error"], code=code, num_retries=num_retries, prev_code=python_code)
    
    return return_df



  def transform(self, prompt, dataframes, code=False):
    """
    Transforms given dataframes based on based on given prompt.

    Parameters:
    -----------
    prompt: str
      Prompt to be used for transformation.
    dataframes: Pandas dataframes
      Dictionary of dataframes to be transformed.
      The key is the dataframe name and the value is the dataframe itself.
      Example:
      {"customers_df": customers_df, "employees_df": employees_df}
    Code: bool
      Whether to print/log the pandas code used to generate visualization or not.
    """
    return self._transform(prompt, dataframes, code=code)
  
  @retry(exceptions=(RequestException, WiseDataInternalError), tries=3, delay=2)
  def _transform(self, prompt, dataframes, code=False, error=None, num_retries=0, prev_code=None):
    if not (type(dataframes) is dict): raise Exception("dataframes needs to be a dictionary with key being dataframe name and value being the dataframe.")

    if num_retries >= 2:
      logging.error(f"We couldn't translate your prompt. Here is python code we attempted to generate: \n{prev_code}")
      raise TranslationError()
    
    data = {
      "dataframe": "\n".join([f"{idx+1}. Dataframe named {key} with columns={value.columns.tolist()} {'and index=[' + value.index.name + ']' if value.index.name else ''}." for idx, (key, value) in enumerate(dataframes.items())]),
      "nl": prompt,
      "error": error
    }

    response = requests.post(
      self.api_base + "/nl2pandas", 
      data=json.dumps(data), 
      headers={
        "Authorization": "Bearer " + self.api_key,
        "content-type": "application/json"
      }
    )

    if (response.status_code == 400): raise BadRequestError(response.text)
    if (response.status_code == 401): raise AuthorizationError()
    if (response.status_code >= 500): raise WiseDataInternalError()

    python_code = response.json()

    import pandas as pd
    import numpy as np
    globals = { "np": np, "pd": pd }
    locals = dataframes.copy()
    try:
      exec(python_code, globals, locals)
      if isinstance(locals["return_df"], pd.DataFrame):
        return_df=locals["return_df"]
        if code: logging.info(f"Given prompt: \n{prompt} \nOutput code: \n{python_code}\n")
      else:
        num_retries += 1
        data["error"] = "Is not a pandas dataframe. Please return dataframe."
        return_df = self._transform(prompt, dataframes, error=data["error"], code=code, num_retries=num_retries, prev_code=python_code)
    except Exception as e:
      num_retries += 1
      data["error"] = f"Threw exception: `{e}`"
      return_df = self._transform(prompt, dataframes, error=data["error"], code=code, num_retries=num_retries, prev_code=python_code)
    
    return return_df


  def viz(self, prompt, dataframes, code=False):
    """
    Creates visualization based on given prompt.

    Parameters:
    -----------
    prompt: str
      Prompt to be used for visualization.
    dataframes: Pandas dataframes
      Dictionary of dataframes to be transformed.
      The key is the dataframe name and the value is the dataframe itself.
      Example:
      {"customers_df": customers_df, "employees_df": employees_df}
    Code: bool
      Whether to print/log the pandas code used to generate visualization or not.
    """
    return self._viz(prompt, dataframes, code=code)

  @retry(exceptions=(RequestException, WiseDataInternalError), tries=3, delay=2)
  def _viz(self, prompt, dataframes, code=False, error=None, num_retries=0, prev_code=None):
    if not (type(dataframes) is dict): raise Exception("dataframes needs to be a dictionary with key being dataframe name and value being the dataframe.")

    if num_retries >= 2:
      logging.error(f"We couldn't translate your prompt into visualization. Here is python code we attempted to generate: \n{prev_code}")
      raise TranslationError()
    
    data = {
      "dataframe": "\n".join([f"{idx+1}. Dataframe named {key} with columns={value.columns.tolist()} {'and index=[' + value.index.name + ']' if value.index.name else ''}." for idx, (key, value) in enumerate(dataframes.items())]),
      "nl": prompt,
      "error": error
    }

    response = requests.post(
      self.api_base + "/nl2seaborn", 
      data=json.dumps(data), 
      headers={
        "Authorization": "Bearer " + self.api_key,
        "content-type": "application/json"
      }
    )

    if (response.status_code == 400): raise BadRequestError(response.text)
    if (response.status_code == 401): raise AuthorizationError()
    if (response.status_code >= 500): raise WiseDataInternalError()

    python_code = response.json()

    import matplotlib.pyplot as plt
    import seaborn as sns
    globals = { "plt": plt, "sns": sns }
    locals = dataframes.copy()
    try:
      exec(python_code, globals, locals)
      if code: logging.info(f"Given prompt: \n{prompt} \nOutput code: \n{python_code}\n")
    except Exception as e:
      num_retries += 1
      data["error"] = f"Threw exception: `{e}`"
      self._viz(prompt, dataframes, error=data["error"], code=code, num_retries=num_retries, prev_code=python_code)