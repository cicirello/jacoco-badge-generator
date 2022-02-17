# Copyright (c) 2020-2021 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM cicirello/pyaction-lite:3
RUN pip install pybadges
COPY JacocoBadgeGenerator.py /JacocoBadgeGenerator.py
ENTRYPOINT ["/JacocoBadgeGenerator.py"]
