import docker, os, subprocess, time

# Paths to InterCode test data
sql_test_data = os.path.join(os.path.dirname(__file__), 'datasets', 'sql_queries.csv')
bash_test_data = os.path.join(os.path.dirname(__file__), 'datasets', 'bash_queries.json')

# Names of InterCode docker images
sql_image_name = "docker-env-sql"
bash_image_name = "intercode-bash"

def sql_build_docker():
    """
    Build the docker image for the InterCode SQL environment. If the image already exists, do nothing.
    """
    client = docker.from_env()
    available_images = [y for x in client.images.list() for y in x.tags]
    if f"{sql_image_name}:latest" in available_images:
        return

    docker_sql_path = os.path.join(os.path.dirname(__file__), 'docker', 'sql-docker-compose.yml')
    subprocess.run(["docker-compose", "-f", docker_sql_path, "up", "-d"])

    # Give some time for SQL server to start
    time.sleep(5)

def bash_build_docker():
    """
    Build the docker image for the InterCode Bash environment. If the image already exists, do nothing.
    """
    client = docker.from_env()
    available_images = [y for x in client.images.list() for y in x.tags]
    if f"{bash_image_name}:latest" in available_images:
        return
    
    docker_bash_path = os.path.join(os.path.dirname(__file__), 'docker', 'bash.Dockerfile')
    image = client.images.build(build_context="", path=docker_bash_path, tag=bash_image_name)

    # Give some time for Bash server to start
    time.sleep(5)