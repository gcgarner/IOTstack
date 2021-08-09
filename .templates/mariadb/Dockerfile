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

# EOF
