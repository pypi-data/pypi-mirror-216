import docker, os

# Define paths to data files
sql_test_data = os.path.join(os.path.dirname(__file__), 'datasets', 'sql_queries.csv')
bash_test_data = os.path.join(os.path.dirname(__file__), 'datasets', 'bash_queries.json')

# Define paths to docker files
sql_image_name = "docker-env-sql"
bash_image_name = "intercode-bash"

# Define methods to build docker images
def sql_build_docker():
    docker_sql_path = os.path.join(os.path.dirname(__file__), 'docker', 'sql-docker-compose.yml')
    base_path = os.getcwd()

    client = docker.from_env()
    compose_data = docker.types.services.load_yaml(filename=docker_sql_path, base_dir=base_path)
    services = client.services.create(configs=compose_data)

def bash_build_docker():
    client = docker.from_env()
    docker_bash_path = os.path.join(os.path.dirname(__file__), 'docker', 'bash.Dockerfile')
    image = client.images.build(build_content="", path=docker_bash_path, tag=bash_image_name)