import git
from git import Repo, Remote
from git import RemoteProgress
import os
from tqdm import tqdm
import json
import pathlib


class GitGrammarDownloader:

    def __init__(self, grammars_folder):
        self.grammars_folder = grammars_folder

    def _setup_git_folder(self, tokenizer_name, repo_url)-> Remote:
        grammar_folder = f"tree-sitter-{tokenizer_name}"
        full_grammar_path = os.path.join(self.grammars_folder, grammar_folder)
        empty_repo = git.Repo.init(full_grammar_path)

        try:
            origin = empty_repo.remote("origin")
        except ValueError:
            origin = empty_repo.create_remote("origin", repo_url)

        origin.fetch(progress=GenericProgress(f"Fetching '{tokenizer_name}': "))
        self._track_master_branch(empty_repo, origin)

        return origin

    def _track_master_branch(self, repo: Repo, origin: Remote):
        # Setup a local tracking branch of a remote branch
        if not repo.head.is_valid():
            repo.create_head("master", origin.refs.master, force=True)\
                .set_tracking_branch(origin.refs.master).checkout()

    def pull_grammars(self, repositories_urls):
        # repositories_urls = {
        #                     'c-master': "https://github.com/tree-sitter/tree-sitter-c",
        #                     'cpp-master': "https://github.com/tree-sitter/tree-sitter-cpp",
        #                     'java-master': "https://github.com/tree-sitter/tree-sitter-java",
        #                     'php-master': "https://github.com/tree-sitter/tree-sitter-php",
        #                     'c_sharp-master': "https://github.com/tree-sitter/tree-sitter-c-sharp",
        #                     'rust-master': "https://github.com/tree-sitter/tree-sitter-rust",
        #                      }

        for tokenizer_name in repositories_urls:
            repository_origin = self._setup_git_folder(tokenizer_name, repositories_urls[tokenizer_name])
            repository_origin.pull(progress=GenericProgress(f"Pulling '{tokenizer_name}': "))


    def get_repositories(self):
        json_file = os.path.join(pathlib.Path(__file__).parent, 'grammar_repositories.json')
        with open(json_file, 'r') as repository_file:
            return json.load(repository_file)


class GenericProgress(RemoteProgress):
    def __init__(self, description="Progress: "):
        super().__init__()
        self.pbar = tqdm()
        self.pbar.desc = description

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


#
# if __name__ == "__main__":
# Test
#     gg = GitGrammarDownloader('/tmp/test-console')
#     repo = {
#         "console-utils": "https://github.com/carlosap256/console_utils/"
#     }
#     gg.pull_grammars(repo)