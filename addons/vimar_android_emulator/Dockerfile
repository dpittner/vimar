ARG BUILD_FROM=budtmo/docker-android:emulator_13.0
FROM ${BUILD_FROM}

ENV WEB_VNC=true

COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 5555 6080

CMD ["/run.sh"]
