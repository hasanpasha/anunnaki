from dataclasses import dataclass
from anunnaki.extensions.models import RepoType


@dataclass
class Repo:
    base_url: str
    source_url: str
    index_url: str
    repo_type: RepoType
