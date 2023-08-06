import docker, os

# Define paths to data files
test_data_sql = os.path.join(os.path.dirname(__file__), 'datasets', 'sql_queries.csv')
test_data_bash = os.path.join(os.path.dirname(__file__), 'datasets', 'bash_queries.json')

# Define paths to docker files
docker_sql_image = "docker-env-sql"
docker_bash_image = "intercode-bash"

# Define methods to build docker images
def build_docker_sql():
    docker_sql_path = os.path.join(os.path.dirname(__file__), 'docker', 'sql-docker-compose.yml')
    base_path = os.getcwd()

    client = docker.from_env()
    compose_data = docker.types.services.load_yaml(filename=docker_sql_path, base_dir=base_path)
    services = client.services.create(configs=compose_data)

def build_docker_bash():
    client = docker.from_env()
    docker_bash_path = os.path.join(os.path.dirname(__file__), 'docker', 'bash.Dockerfile')
    image = client.images.build(build_content="", path=docker_bash_path, tag=docker_bash_image)