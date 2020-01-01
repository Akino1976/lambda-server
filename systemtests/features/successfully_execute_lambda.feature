Feature: Call handlers in lambdaserver that successfully execute

  Scenario: Successfully call the lambdaserver with a handler that returns JSON
    Given the request body:
      event:
        word: kitten
    When I make a POST request to http://lambdaserver/invoke/lambda_function.json_handler
    Then the HTTP status code should be OK
    And the JSON response body should contain:
      returnValue:
        singular: kitten
        plural: kittens
      logLines: !Exists

  Scenario: Successfully call the lambdaserver with a handler that returns a JSON array
    Given the request body:
      event:
        word: kitten
    When I make a POST request to http://lambdaserver/invoke/lambda_function.array_handler
    Then the HTTP status code should be OK
    And the JSON response body should contain:
      returnValue:
        - kitten
        - kittens
      logLines: !Exists

  Scenario: Successfully call the lambdaserver with a handler that returns a string
    Given the request body:
      event:
        word: kitten
    When I make a POST request to http://lambdaserver/invoke/lambda_function.text_handler
    Then the HTTP status code should be OK
    And the JSON response body should contain:
      returnValue: kitten in plural is kittens
      logLines: !Exists


  Scenario: Successfully call the lambdaserver with a handler that returns null
    Given the request body:
      event:
        word: kitten
    When I make a POST request to http://lambdaserver/invoke/lambda_function.null_handler
    Then the HTTP status code should be OK
    And the JSON response body should contain:
      returnValue: null
      logLines: !Exists


  Scenario: Successfully call the lambdaserver with a handler that uses its environment parameters
    Given the request body:
      event:
        variables:
          - SOME_ENVIRONMENT_VARIABLE
          - SOME_OTHER_ENVIRONMENT_VARIABLE
          - SOME_UNSET_VARIABLE
      environment:
        SOME_ENVIRONMENT_VARIABLE: The value of the environment variable here
        SOME_OTHER_ENVIRONMENT_VARIABLE: "123"
    When I make a POST request to http://lambdaserver/invoke/lambda_function.environment_handler
    Then the HTTP status code should be OK
    And the JSON response body should contain:
      returnValue:
        SOME_ENVIRONMENT_VARIABLE: The value of the environment variable here
        SOME_OTHER_ENVIRONMENT_VARIABLE: "123"
        SOME_UNSET_VARIABLE: null
      logLines: !Exists
