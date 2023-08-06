class WiseDataError(Exception):
  def __init__(self, msg):
    self.msg = msg
    super().__init__(f"Error: {self.msg}")

class WiseDataInternalError(WiseDataError):
  """
  Raised when an internal error occurs
  """
  def __init__(self, error_msg=""):
    super().__init__(error_msg)

class BadRequestError(WiseDataError):
  """
  Raised when a bad request happens
  """
  def __init__(self, error_msg=""):
    super().__init__(error_msg)

class AuthorizationError(WiseDataError):
  def __init__(self):
    super().__init__(f"Invalid authorization token.")

class TranslationError(WiseDataError):
  def __init__(self, error_msg=""):
    super().__init__(f"We couldn't translate your query. {error_msg}")