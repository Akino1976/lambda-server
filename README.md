# lambdaserver-python

> Ever wanted to easily system test your lambda function, or perhaps run it locally in a sane manner? All this without writing any weird hacks?
>
> Then let me tell you about `lambdaserver-python`!

## What is this?

This is a webserver to use for locally running lambda functions in a live-like environment while being able to easily test multiple scenarios in a containerized environment ([building upon the glorious lambci/docker-lambda](https://github.com/lambci/docker-lambda)).

What's neat is you can use your **regular testing suite for testing your lambda** by simply making requests with an event and maybe some environment variables and then get back any return values/errors and the logs outputted by the lambda function.

## So, how do I use it?

Check the [`/example` folder](https://github.com/bambora/lambdaserver-python/tree/master/example) for examples on how to use it in different scenarios. Or maybe check out how the system tests are set up? Or here below? Up to you.

Step by step:

1. [Package your lambda as usual](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) into a folder of your choice (you can also check out how this is done in the [`/example` folder](https://github.com/bambora/lambdaserver-python/tree/master/example))
2. Using docker mount in the folder with the `.zip` into the container when the container is running
3. Start making requests to `localhost:5000/invoke/<your_lambda_handler_here>`

The API specification for how to _make requests_ to the server can be found in [`./lambdaserver/api-specification.yaml`](https://github.com/bambora/lambdaserver-python/blob/master/lambdaserver/api-specification.yaml)

_In code please!_

```bash
# The path to the packaged .zip file is ./my-packages
# and the package name is lambda_package.zip
docker run \
  -v "${PWD}/my-packages:/packages" \
  -p 5000:80 \
  -e "PACKAGE_NAME=lambda_package.zip" \
  -it --rm bambora-dkr.jfrog.io/lambdaserver-python3.7
```

## Passing environment variables

### To the lambda function

To pass in environment variables to the lambda function, simply provide these as per the spec in the request body!

### To the lambda server

There are a couple different environment variables that might be interesting when using the lambda server though, they are the the following:

#### `${PACKAGE_FOLDER}=/packages`

The folder in which the lambda package(s) (.zip files) should be mounted in into.

Defaults to `/packages`

#### `${PACKAGE_NAME}=pkg.zip`

The name of the package that was passed in which should be run and unzipped.

Defaults to `pkg.zip`

#### `${RUN_IN_WATCH_MODE}="0"`

Boolean value for whether to _run in watch mode_, which basically means that the `.zip` file in `/packages` won't be unzipped.

This variable should be used when mounting in the application code straight into `/var/task` for a watch-mode like experience.

Defaults to "0"

#### `${EXEC_BEFORE}=""`

Bash script to run before starting the server. Example usage would be to install third-party dependencies into an external folder when running in test mode, since installing them next to the application code will completely ruin your local file tree.

See an example of this in the [`/example` folder](https://github.com/bambora/lambdaserver-python/tree/master/example).

## Any caveats?

Of course, it's code after all.

The biggest potential issue is that the code being run in this image is run as root instead of a low privilege user. Please submit a PR with a fix if this is something you want.

## Can I use this in production?

Please don't. The purpose of this tool is to use it for running your lambdas locally for black-box testing.
