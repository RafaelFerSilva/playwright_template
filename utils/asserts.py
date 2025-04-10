import allure

class BaseAsserts:
  def __init__(self) -> None:
    pass
  
  @allure.step("Assert String Value")
  def assert_string_value(self, expected_value, value_to_validate):
    assert expected_value == value_to_validate, f"Expected '{expected_value}', but got '{value_to_validate}'"
  
