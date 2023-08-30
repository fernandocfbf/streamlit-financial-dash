import git
repository = git.Repo('.', search_parent_directories=True)
ROOT_PATH = repository.working_tree_dir.replace("\\",'/')
LOAD_DATA_PATH = f"{ROOT_PATH}/src/data/"