# Download base image
FROM eclipse-mosquitto:latest

# Add support tools
RUN apk update && apk add --no-cache rsync tzdata

# where IOTstack template files are stored
ENV IOTSTACK_DEFAULTS_DIR="iotstack_defaults"

# copy template files to image
COPY --chown=mosquitto:mosquitto ${IOTSTACK_DEFAULTS_DIR} /${IOTSTACK_DEFAULTS_DIR}

# replace the docker entry-point script
ENV IOTSTACK_ENTRY_POINT="docker-entrypoint.sh"
COPY ${IOTSTACK_ENTRY_POINT} /${IOTSTACK_ENTRY_POINT}
RUN chmod 755 /${IOTSTACK_ENTRY_POINT}
ENV IOTSTACK_ENTRY_POINT=

# IOTstack also declares these paths
VOLUME ["/mosquitto/config", "/mosquitto/pwfile"]

# EOF
