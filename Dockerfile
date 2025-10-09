# Copyright (c) 2020-2025 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM ghcr.io/cicirello/pyaction:3.14.0-gh-2.81.0
COPY src /
ENTRYPOINT ["/entrypoint.py"]
