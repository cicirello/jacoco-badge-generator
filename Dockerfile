# Copyright (c) 2020-2021 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
#FROM cicirello/pyaction-lite:3
FROM redhat/ubi8:latest

RUN dnf update --nodocs -y \
 && dnf --setopt=tsflags=nodocs install  curl ca-certificates openssl python38 python38-pip patch -y \
 && dnf clean all

RUN pip3 install pybadges
COPY JacocoBadgeGenerator.py /JacocoBadgeGenerator.py
ENTRYPOINT ["/JacocoBadgeGenerator.py"]
