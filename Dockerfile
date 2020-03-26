FROM alpine:3.10.2

RUN set -ex && \
    mkdir /client \
    && cd /tmp \
    && wget https://github.com/nzbget/nzbget/archive/v21.0.zip \
    && apk add --no-cache unrar p7zip \
    && apk add --no-cache --virtual .fetch-deps \
    build-base \
    openssl-dev \
    libxml2-dev \
    pkgconf \
    zlib-dev \
    && unzip v21.0.zip \
    && rm v21.0.zip \
    && cd nzb* \
    && ./configure --disable-curses \
    && make && strip nzbget \
    && cp nzbget /client/ \
    && cp nzbget.conf webui/ \
    && cp -r scripts/ /client/ \
    && cp -r webui/ /client/ \
    && cd .. \
    && rm -rf nzb* \
    && cd /usr/lib/ \
    && cp libxml2.so.2 libstdc++.so.6 libgcc_s.so.1 /tmp/ \
    && apk del .fetch-deps \
    && cp /tmp/lib* /usr/lib/ \
    && rm /tmp/lib* \
    && adduser -g '' -h /client -u 1000 -D -s /sbin/nologin nzbget \
    && chown -R nzbget:nzbget /client 

EXPOSE 6789

USER nzbget

VOLUME /config /downloads

ENTRYPOINT ["/client/nzbget","-s","-c","/config/nzbget.conf"]
