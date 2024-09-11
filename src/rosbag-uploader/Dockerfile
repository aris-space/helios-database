# This Dockerfile builds the rosbag uploader

FROM debian:12-slim AS builder
# Install `pipx` and `python-is-python3`, the latter is needed due to `poetry bundle` failing later otherwise, see #4 on GitHub
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes \
    pipx \
    python-is-python3

# Refresh path
ENV PATH="/root/.local/bin:${PATH}"

# Install poetry and related things
RUN pipx install poetry
RUN pipx inject poetry poetry-plugin-bundle

WORKDIR /src
COPY . .
RUN poetry bundle venv --python=/usr/bin/python3 --only=main,production /venv

# FROM debian:12-slim
# COPY --from=builder /venv /venv
# ENTRYPOINT ["source /venv/bin/activate"]
# CMD source /venv/bin/activate
# ENTRYPOINT ["/bin/bash", "-c", "source /venv/bin/activate"]
# ENTRYPOINT /bin/bash -c "source /venv/bin/activate"
ENTRYPOINT ["/bin/bash", "-c", "source /venv/bin/activate && exec \"$@\"", "--"]
# CMD ["python /venv/bin/helios_rosbag_uploader_poc/main.py"]

CMD python /venv/lib/python3.11/site-packages/rosbag_uploader/main.py
