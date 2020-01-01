#!/bin/sh

echo ${RUN_IN_WATCH_MODE}

if [ "${RUN_IN_WATCH_MODE}" == "1" ]; then
  echo "Assuming /var/task/ isn't empty, here's the file list:"

  ls /var/task/ -l
else
  echo "Unzipping package at ${PACKAGE_FOLDER}/${PACKAGE_NAME} into /var/task/"

  unzip -o ${PACKAGE_FOLDER}/${PACKAGE_NAME} -d /var/task/

  UNZIP_EXIT_CODE=$?

  if [[ ${UNZIP_EXIT_CODE} != 0 ]]; then
    echo "unzip command exited with non-zero exit code: ${UNZIP_EXIT_CODE}"

    exit ${UNZIP_EXIT_CODE}
  fi

  echo ""
  echo "Successfully unzipped ${PACKAGE_NAME} into /var/task/"
fi

if [[ ! -z "${EXEC_BEFORE}" ]]; then
  echo "Running the following command before start up:"
  echo "${EXEC_BEFORE}"

  eval "${EXEC_BEFORE}"
fi

echo ""
echo "Running: $@"
echo ""

exec "$@"
