# Copyright (c) 2020 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM cicirello/pyaction-lite:3.13.4
COPY JacocoBadgeGenerator.py /JacocoBadgeGenerator.py
ENTRYPOINT ["/JacocoBadgeGenerator.py"]
