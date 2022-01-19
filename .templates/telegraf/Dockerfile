# Download base image
FROM telegraf:latest

# Add support tool
RUN apt update && apt install -y rsync

# where IOTstack template files are stored
ENV IOTSTACK_DEFAULTS_DIR="iotstack_defaults"

# copy template files to image
COPY ${IOTSTACK_DEFAULTS_DIR} /${IOTSTACK_DEFAULTS_DIR}

# 1. copy the default configuration file that ships with the image as
#    a baseline reference for the user, and make it read-only.
# 2. strip comment lines and blank lines from the baseline reference to
#    use as the starting point for the IOTstack default configuration.
# 3. edit the IOTstack default configuration to insert an appropriate
#    URL for influxdb running in another container in the same stack.
ENV BASELINE_CONFIG=/${IOTSTACK_DEFAULTS_DIR}/telegraf-reference.conf
ENV IOTSTACK_CONFIG=/${IOTSTACK_DEFAULTS_DIR}/telegraf.conf
RUN cp /etc/telegraf/telegraf.conf ${BASELINE_CONFIG} && \
    cat /${IOTSTACK_DEFAULTS_DIR}/auto_include/*.conf >> ${BASELINE_CONFIG} && \
    rm -r /${IOTSTACK_DEFAULTS_DIR}/auto_include && \
    chmod 444 ${BASELINE_CONFIG} && \
    grep -v -e "^[ ]*#" -e "^[ ]*$" ${BASELINE_CONFIG} >${IOTSTACK_CONFIG} && \
    sed -i '/^\[\[outputs.influxdb\]\]/a\ \ urls = ["http://influxdb:8086"]' ${IOTSTACK_CONFIG}
ENV BASELINE_CONFIG=
ENV IOTSTACK_CONFIG=

# replace the docker entry-point script with a self-repairing version
ENV IOTSTACK_ENTRY_POINT="entrypoint.sh"
COPY ${IOTSTACK_ENTRY_POINT} /${IOTSTACK_ENTRY_POINT}
RUN chmod 755 /${IOTSTACK_ENTRY_POINT}
ENV IOTSTACK_ENTRY_POINT=

# IOTstack declares this path for persistent storage
VOLUME ["/etc/telegraf"]

# EOF
