Feature: Call handlers in lambdaserver that fail to execute

  Scenario: Call lambdaserver which raises an error inside the handler
    Given the request body:
      event:
        word: kitten
    When I make a POST request to http://lambdaserver/invoke/error_function.error_on_call_handler
    Then the HTTP status code should be INTERNAL_SERVER_ERROR
    And the JSON response body should contain:
      error:
        errorMessage: Oh no
        errorType: Exception
        stackTrace:
          - - File "/var/task/error_function.py", line 8, in error_on_call_handler
            - raise Exception('Oh no')
      logLines: !Exists

  Scenario: Call lambdaserver which cannot read the function
    Given the request body:
      event:
        word: kitten
    When I make a POST request to http://lambdaserver/invoke/erroneus_function.typo_handler
    Then the HTTP status code should be INTERNAL_SERVER_ERROR
    And the JSON response body should contain:
      error:
        errorMessage: name 'rpint' is not defined
      logLines: !Exists
