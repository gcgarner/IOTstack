# Download base image
FROM ghcr.io/linuxserver/mariadb

# apply stability patches recommended in
#   
#   https://discord.com/channels/638610460567928832/638610461109256194/825049573520965703
#   https://stackoverflow.com/questions/61809270/how-to-discover-why-mariadb-crashes
RUN sed -i.bak \
  -e "s/^thread_cache_size/# thread_cache_size/" \
  -e "s/^read_buffer_size/# read_buffer_size/" \
  /defaults/my.cnf

# copy the health-check script into place
ENV HEALTHCHECK_SCRIPT "iotstack_healthcheck.sh"
COPY ${HEALTHCHECK_SCRIPT} /usr/local/bin/${HEALTHCHECK_SCRIPT}

# define the health check
HEALTHCHECK \
   --start-period=30s \
   --interval=30s \
   --timeout=10s \
   --retries=3 \
   CMD ${HEALTHCHECK_SCRIPT} || exit 1

# EOF
