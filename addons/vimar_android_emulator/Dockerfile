ARG BUILD_FROM=budtmo/docker-android:emulator_13.0
FROM ${BUILD_FROM}

USER root

# The upstream budtmo/docker-android base image family is Debian-based and
# installs python3-pip in its base stage. Keep an explicit apt install here so
# this add-on remains self-contained and guarantees python availability.
RUN set -eux; \
    apt-get -qqy update; \
    apt-get -qqy install --no-install-recommends python3 python3-pip; \
    apt-get autoremove -y; \
    apt-get clean all; \
    rm -rf /var/lib/apt/lists/*; \
    python3 --version; \
    pip3 --version

# Restore the original non-root runtime user from the base image.
USER ${USERID}:${GROUPID}

ENV WEB_VNC=true \
    HOME=/data/android-home \
    ANDROID_EMULATOR_HOME=/data/.android \
    ANDROID_SDK_HOME=/data/.android \
    ANDROID_AVD_HOME=/data/.android/avd

COPY --chmod=755 run.sh /run.sh

EXPOSE 5555 6080

CMD ["/run.sh"]
