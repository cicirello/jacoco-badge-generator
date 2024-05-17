# Copyright (c) 2020-2024 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM ghcr.io/cicirello/pyaction:4.30.0
COPY src /
ENTRYPOINT ["/entrypoint.py"]
