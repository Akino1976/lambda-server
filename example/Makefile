extract-package:
	docker build -t lambdaserver-python-example-function handlers
	docker run -v "${PWD}/output":/output --rm lambdaserver-python-example-function	sh copy_handlers.sh

# Example of how to mount in packaged .zip file and run the server on local port 5000
run-local: extract-package
	docker run \
		-v "${PWD}/output":/packages \
		-p 5000:80 \
		-e "PACKAGE_NAME=pkg.zip" \
		-it --rm bambora-dkr.jfrog.io/lambdaserver-python3.7

# Example of how to mount in application code to run in _watch-mode_,
# install it's dependencies in /tmp/deps and not unzip any package in /packages.
# Try modifying the lambda code while the server is running and then call the server again!
run-watch:
	docker run \
		-v "${PWD}/handlers":/var/task \
		-p 5000:80 \
		-e "EXEC_BEFORE=mkdir -p /tmp/deps; \
			export PYTHONPATH=\$$PYTHONPATH:/tmp/deps; \
			pip install -t /tmp/deps --requirement /var/task/requirements.txt \
			" \
		-e "RUN_IN_WATCH_MODE=1" \
		-it --rm bambora-dkr.jfrog.io/lambdaserver-python3.7
