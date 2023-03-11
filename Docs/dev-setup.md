## Development Setup

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