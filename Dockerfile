# You need to tag the backend_base build you want to use for the backend build you're going to use to do this build.
FROM betasmartz/backend_base:latest

ENV PYTHONUNBUFFERED 1
ENV TERM xterm

ADD . ./betasmartz

EXPOSE 80

# setup all the config files
RUN ln -s /betasmartz/devop/supervisor-app.conf /etc/supervisor/conf.d/
COPY ./docker-entrypoint.sh /
COPY /local_settings_docker.py /betasmartz/local_settings.py
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["backend"]
