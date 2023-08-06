import docker, os, subprocess

# Define paths to data files
sql_test_data = os.path.join(os.path.dirname(__file__), 'datasets', 'sql_queries.csv')
bash_test_data = os.path.join(os.path.dirname(__file__), 'datasets', 'bash_queries.json')

# Define paths to docker files
sql_image_name = "docker-env-sql"
bash_image_name = "intercode-bash"

# Define methods to build docker images
def sql_build_docker():
    docker_sql_path = os.path.join(os.path.dirname(__file__), 'docker', 'sql-docker-compose.yml')
    subprocess.run(["docker-compose", "-f", docker_sql_path, "up", "-d"])

def bash_build_docker():
    client = docker.from_env()
    docker_bash_path = os.path.join(os.path.dirname(__file__), 'docker', 'bash.Dockerfile')
    image = client.images.build(build_context="", path=docker_bash_path, tag=bash_image_name)