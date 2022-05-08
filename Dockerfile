FROM archlinux:latest AS install_python
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm python wget curl libffi gcc clang dos2unix
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.10 get-pip.py
RUN pip install --upgrade pip setuptools wheel pipenv

FROM install_python AS install_pm2
RUN pacman -S nodejs-lts-gallium npm --noconfirm
RUN npm install -g npm 
RUN npm install -g pnpm pm2

FROM install_pm2 AS prod_deployment
WORKDIR /Bot
COPY Pipfile ./ /Bot/
COPY Pipfile.lock ./ /Bot/
RUN pipenv run pip install --upgrade pip setuptools wheel
RUN pipenv install
RUN dos2unix /Bot/Bot/kumikobot.py
EXPOSE 4001
ARG PM2_PUBLIC_KEY_INGEST
ARG PM2_SECRET_KEY_INGEST
ENV PM2_PUBLIC_KEY=${PM2_PUBLIC_KEY_INGEST}
ENV PM2_SECRET_KEY=${PM2_SECRET_KEY_INGEST}
CMD ["pm2-runtime", "pipenv run /Bot/Bot/kumikobot.py"]