# Development Setup

## Local

1. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/Kumiko.git && cd Kumiko
    ```

    Or if you have the `gh` cli tool installed:

    ```sh
    gh repo clone [username]/Kumiko
    ```

2. Install all of the dependencies (including dev dependencies)

    ```sh
    poetry install --with=dev,test
    ```

3. Start the Docker Compose stack

    ```sh
    sudo docker compose -f docker-compose-dev.yml up -d
    ```

4. Run the database migrations

    ```sh
    poetry run prisma db push
    ```

## Vagrant

Kumiko also supports using Vagrant as a development environment. In order to use Vagrant, you will need Oracle VirtualBox or VMWare Workstation installed on your machine. Once installed and properly configured, you can just run `vagrant up` to provision and start it up, and connect to it by SSH or by VSCode. 

## Environment Variables
Kumiko v0.7+ includes an development mode feature, which will set up jishaku and a custom FS watcher. Later on, there may be more development features that will be included. Make sure you first install the dev dependencies first! And in order to enable it, set an environment variable called `DEV_MODE` to `True`.