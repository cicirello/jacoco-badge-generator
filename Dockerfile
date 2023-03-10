# Copyright (c) 2020-2023 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM ghcr.io/cicirello/pyaction:4.17.0
COPY src /
ENTRYPOINT ["/entrypoint.py"]
