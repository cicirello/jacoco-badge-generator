# Copyright (c) 2020-2022 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM cicirello/pyaction-lite:3
COPY src /
ENTRYPOINT ["/JacocoBadgeGenerator.py"]
