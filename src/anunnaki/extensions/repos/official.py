
from anunnaki.extensions.models import Repo, RepoType

official_repo = Repo(
    base_url="https://github.com/hasanpasha/anunnaki-extensions",
    source_url="https://github.com/hasanpasha/anunnaki-extensions/trunk/",
    index_url="https://raw.githubusercontent.com/hasanpasha/anunnaki-extensions/master/index.json",
    repo_type=RepoType.GIT
)
