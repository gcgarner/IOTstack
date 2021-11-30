# Download base image
FROM prom/prometheus:latest

USER root

# where IOTstack template files are stored
ENV IOTSTACK_DEFAULTS_DIR="iotstack_defaults"
ENV IOTSTACK_CONFIG_DIR="/prometheus/config/"

# copy template files to image
COPY --chown=nobody:nobody ${IOTSTACK_DEFAULTS_DIR} /${IOTSTACK_DEFAULTS_DIR}

# add default config from image to template
RUN cp /etc/prometheus/prometheus.yml /${IOTSTACK_DEFAULTS_DIR}

# replace the docker entry-point script
ENV IOTSTACK_ENTRY_POINT="docker-entrypoint.sh"
COPY ${IOTSTACK_ENTRY_POINT} /${IOTSTACK_ENTRY_POINT}
RUN chmod 755 /${IOTSTACK_ENTRY_POINT}
ENTRYPOINT ["/docker-entrypoint.sh"]
ENV IOTSTACK_ENTRY_POINT=

USER nobody

# EOF
