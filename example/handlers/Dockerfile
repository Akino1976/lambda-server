FROM lambci/lambda:build-python3.7 as build

WORKDIR /handlers
COPY . /handlers

RUN mkdir -p /package; \
  pip install -t /handlers --requirement /handlers/requirements.txt; \
  zip -r /package/pkg.zip * -x requirements.txt

FROM alpine:3.4

WORKDIR /package

COPY --from=build /package /package

COPY copy_handlers.sh /package/copy_handlers.sh
