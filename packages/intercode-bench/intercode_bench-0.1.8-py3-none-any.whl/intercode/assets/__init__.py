import os 

# Define paths to data files
test_data_sql = os.path.join(os.path.dirname(__file__), 'datasets', 'sql_queries.csv')
test_data_bash = os.path.join(os.path.dirname(__file__), 'datasets', 'bash_queries.json')

# Define paths to docker files
# test_docker_sql = os.path.join(current_directory, 'docker', 'sql.Dockerfile')
# test_docker_sql_compose = os.path.join(current_directory, 'docker', 'sql.docker-compose.yml')
# test_docker_bash = os.path.join(current_directory, 'docker', 'bash.Dockerfile')