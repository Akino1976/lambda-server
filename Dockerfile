FROM lambci/lambda:build-python3.7 as build

RUN mkdir -p /lambdaserver
RUN mkdir -p /server-dependencies

COPY lambdaserver /lambdaserver

RUN pip install \
  --requirement /lambdaserver/requirements.txt \
  --target /server-dependencies

FROM lambci/lambda:python3.7

ENV PACKAGE_FOLDER=/packages
ENV PACKAGE_NAME=pkg.zip
ENV RUN_IN_WATCH_MODE="0"
ENV EXEC_BEFORE=""
ENV FLASK_APP=app.py
ENV PYTHONPATH=$PYTHONPATH:/server-dependencies
ENV PATH=$PATH:/server-dependencies/bin

WORKDIR /lambdaserver

COPY --from=build /server-dependencies /server-dependencies
COPY --from=build /lambdaserver /lambdaserver

USER root

EXPOSE 80

ENTRYPOINT [ "sh", "./entrypoint.sh" ]

CMD python -u app.py
