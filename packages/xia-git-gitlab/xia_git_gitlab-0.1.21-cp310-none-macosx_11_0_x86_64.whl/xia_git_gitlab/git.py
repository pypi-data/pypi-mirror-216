import logging
import os
import json
import base64
import time
from datetime import datetime, timedelta
from itertools import chain
import requests
from git import Repo
from xia_git import Git


class GitlabGit(Git):
    PIPELINE_END_STATUS = ["success", "failed", "canceled", "skipped"]
    api_url = f'https://{os.environ.get("GITLAB_HOST")}/api/v4/'
    gitlab_token = os.environ.get("GITLAB_TOKEN")

    @classmethod
    def create_sub_group(cls, group_name: str, parent_id: int):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        group_payload = {'name': group_name, 'path': group_name, 'parent_id': parent_id}
        response = requests.post(cls.api_url + "groups", headers=headers, json=group_payload)
        if response.status_code == 201:
            print("Subgroup created successfully.")
            return True
        else:
            print("Failed to create subgroup. Response:", response.text)
            return False

    @classmethod
    def delete_sub_group(cls, group_name: str, parent_id: int):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        group_id = cls.get_sub_group_info(group_name, parent_id).get("id", None)
        if not group_id:
            print("Subgroup Not Found")
            return True
        response = requests.delete(cls.api_url + f"groups/{group_id}", headers=headers)
        if response.status_code == 202:
            print("Subgroup deleted successfully.")
            return True
        else:
            print("Failed to delete subgroup. Response:", response.text)
            return False

    @classmethod
    def get_sub_group_id(cls, group_name: str, parent_id: int, raise_error: bool = False):
        group_info = cls.get_sub_group_info(group_name, parent_id)
        if group_info:
            return group_info["id"]
        elif raise_error:
            raise ValueError(f"Group {group_name} can not be found")

    @classmethod
    def get_sub_group_info(cls, group_name: str, parent_id: int):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        response = requests.get(cls.api_url + f"groups/{parent_id}/subgroups", headers=headers)
        if response.status_code == 200:
            for group_info in response.json():
                if group_info["name"] == group_name:
                    return group_info

    @classmethod
    def create_repo_token(cls, user_id: int, token_name: str):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        token_url = cls.api_url + f"users/{user_id}/access_tokens"
        token_payload = {'name': token_name, 'scopes': ["read_api"]}
        response = requests.post(token_url, headers=headers, json=token_payload)
        if response.status_code == 201:
            return response.json()['token']
        else:
            print("Failed to create the access token. Response: ", response.text)

    @classmethod
    def create_group_access_token(cls, group_id: int, token_name: str):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        token_payload = {
            'name': token_name,
            'scopes': ["api", "read_api", "read_registry", "write_registry", "read_repository", "write_repository"],
            "access_level": 50  # Owner
        }
        response = requests.post(cls.api_url + f"groups/{group_id}/access_tokens", headers=headers, json=token_payload)
        if response.status_code == 201:
            return response.json()['token']
        else:
            print("Failed to create the access token. Response: ", response.text)

    @classmethod
    def get_access_token_info(cls, group_id: int, token_name: str):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        response = requests.get(cls.api_url + f"groups/{group_id}/access_tokens", headers=headers)
        if response.status_code == 200:
            for access_token_info in response.json():
                if access_token_info["name"] == token_name:
                    return access_token_info

    @classmethod
    def create_project(cls, project_name: str, group_id: int, **kwargs):
        headers = {
            'PRIVATE-TOKEN': cls.gitlab_token,
            'Content-Type': 'application/json',
        }
        data = {
            'name': project_name,
            'description': project_name,
            'path': project_name,
            'namespace_id': str(group_id),
            'visibility': 'internal'
        }
        response = requests.post(cls.api_url + "projects", headers=headers, json=data)
        if response.status_code == 201:
            print(f"Project {project_name} created successfully.")
        else:
            print("Failed to create the project. Response: ", response.text)
        # Create the first readme file
        cls.commit_file(project_name, group_id, "README.md", "Hello World")

    @classmethod
    def get_project_info(cls, project_name: str, group_id: int, **kwargs):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        response = requests.get(cls.api_url + "projects", headers=headers,
                                params={'search': project_name, 'simple': True})
        if response.status_code == 200:
            for project in response.json():
                if project['name'] == project_name and project["namespace"]["id"] == group_id:
                    return project

    @classmethod
    def delete_project(cls, project_name: str, group_id: int, **kwargs):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_info = cls.get_project_info(project_name, group_id)
        if not project_info:
            print(f"Project {project_name} doesn't exist")
            return
        response = requests.delete(cls.api_url + "projects" + f"/{project_info['id']}", headers=headers)
        if response.status_code == 202:
            print(f"Project {project_name} accepted deletion successfully.")
        else:
            print("Failed to delete the project. Response: ", response.text)

    @classmethod
    def get_branch_info(cls, project_name: str, group_id: int, branch_name: str):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        branch_url = f"{cls.api_url}projects/{project_id}/repository/branches/{branch_name}"
        response = requests.get(branch_url, headers=headers)
        if response.status_code == 200:
            return response.json()

    @classmethod
    def create_branch(cls, project_name: str, group_id: int, branch_name: str, ref: str = "master"):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        if not cls.get_branch_info(project_name, group_id, branch_name):
            branch_url = f"{cls.api_url}projects/{project_id}/repository/branches"
            data = {"id": project_id, "branch": branch_name, "ref": ref}
            response = requests.post(branch_url, headers=headers, json=data)
            if response.status_code == 201:
                return response.json()

    @classmethod
    def delete_branch(cls, project_name: str, group_id: int, branch_name: str):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        if cls.get_branch_info(project_name, group_id, branch_name):
            branch_url = f"{cls.api_url}projects/{project_id}/repository/branches/{branch_name}"
            response = requests.delete(branch_url, headers=headers)
            if response.status_code == 202:
                print(f"Project {project_name}/{branch_name} accepted deletion successfully.")
            else:
                print("Failed to delete the project. Response: ", response.text)

    @classmethod
    def clone_project(cls, repo_dir: str, project_name: str, group_id: int, overwrite: bool = True, branch: str = None,
                      **kwargs):
        if os.path.exists(repo_dir) and len(os.listdir(repo_dir)) > 0:
            if overwrite:
                cls.clean_workspace(repo_dir, destroy=True)
            else:
                raise ValueError(f"{repo_dir} is not empty!")
        repo_url = cls.get_project_info(project_name, group_id)["http_url_to_repo"]
        scheme, body = repo_url.split("://", 1)
        body = f"oauth2:{os.environ.get('GITLAB_TOKEN')}@" + body
        repo_url = "://".join([scheme, body])
        return Repo.clone_from(repo_url, repo_dir, branch=branch)

    @classmethod
    def commit_file(cls, project_name: str, group_id: int, filename: str, file_content):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        commit_url = f"{cls.api_url}projects/{project_id}/repository/files/{filename}"
        file_content_base64 = base64.b64encode(file_content.encode()).decode()
        data = {'branch': 'master', 'content': file_content_base64, 'commit_message': filename, 'encoding': 'base64'}
        response = requests.post(commit_url, headers=headers, json=data)
        # Check the response
        if response.status_code == 201:
            print(f'Successfully created {filename}')
        else:
            print(f'Failed to create {filename}:', response.text)

    @classmethod
    def commit_project(cls, repo_dir: str, commit_message: str,
                       project_name: str, remote_branch: str, group_id: int,
                       author_name: str = None, author_email: str = None, **kwargs):
        repo = Repo(repo_dir)
        origin = repo.remote('origin')
        origin.fetch()
        repo.git.merge(f'origin/{remote_branch}')
        # Switch to correct branch
        active_branch = repo.active_branch
        if active_branch.name != remote_branch:
            target_branch = repo.heads[remote_branch]
            target_branch.checkout()
        # Commit all changes
        repo.git.add(A=True)
        if not repo.index.diff(f'origin/{remote_branch}'):
            return  # Nothing is changed, so no need to continue
        repo.index.commit(commit_message)
        print(sum(1 for _ in repo.iter_commits()))
        # Get changes to be committed to Gitlab
        diff_index = repo.head.commit.diff(f'origin/{remote_branch}')
        actions = []
        # Case 1: Modification or Change File Type
        for diff in chain(diff_index.iter_change_type('M'), diff_index.iter_change_type('T')):
            file_path = os.path.join(repo_dir, diff.a_path)
            with open(file_path, 'rb') as f:
                file_content = f.read()
            file_content = base64.b64encode(file_content).decode('utf-8')
            action = {'action': 'update', 'file_path': diff.a_path, 'content': file_content, 'encoding': 'base64'}
            actions.append(action)
        # Case 2: Exists on local but not remotely, so we will create new file to remote
        for diff in diff_index.iter_change_type('D'):
            file_path = os.path.join(repo_dir, diff.a_path)
            with open(file_path, 'rb') as f:
                file_content = f.read()
            file_content = base64.b64encode(file_content).decode('utf-8')
            action = {'action': 'create', 'file_path': diff.a_path, 'content': file_content, 'encoding': 'base64'}
            actions.append(action)
        # Case 3: Exists on remote but not locally, so we will delete remote
        for diff in chain(diff_index.iter_change_type('A'), diff_index.iter_change_type('C')):
            action = {'action': 'delete', 'file_path': diff.a_path}
            actions.append(action)
        # Case 4: File Rename
        for diff in diff_index.iter_change_type('R'):
            file_path = os.path.join(repo_dir, diff.a_path)
            delete_action = {'action': 'delete', 'file_path': diff.b_path}
            with open(file_path, 'rb') as f:
                file_content = f.read()
            file_content = base64.b64encode(file_content).decode()
            create_action = {'action': 'create', 'file_path': diff.a_path, 'content': file_content, 'encoding': 'base64'}
            actions.extend([delete_action, create_action])
        # Commit to Gitlab
        project_id = cls.get_project_info(project_name, group_id)["id"]
        commit_url = f"{cls.api_url}projects/{project_id}/repository/commits"
        commit_payload = {'branch': remote_branch, 'commit_message': commit_message, 'actions': actions}
        if author_name and author_email:
            commit_payload.update({'author_name': author_name, 'author_email': author_email})
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        response = requests.post(commit_url, headers=headers, json=commit_payload)

        # Check the response
        if response.status_code == 201:
            print('Successfully committed')
            origin.fetch()
            repo.git.merge(f'origin/{remote_branch}')
        else:
            print('Failed to commit:', response.text)
            action_list = {action["file_path"]: action["action"] for action in actions}
            print(action_list)

    @classmethod
    def create_merge_request(cls, project_name: str, group_id: int, title: str,
                             source_branch: str, target_branch: str = "master"):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        merge_request_url = f"{cls.api_url}projects/{project_id}/merge_requests"
        data = {"title": title, "source_branch": source_branch, "target_branch": target_branch}
        response = requests.post(merge_request_url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            print(f'Failed to create merge request {project_name}:', response.text)

    @classmethod
    def perform_merge(cls, project_name: str, group_id: int, merge_request_id: int, title: str, timeout: int = 60):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        merge_request_url = f"{cls.api_url}projects/{project_id}/merge_requests/{merge_request_id}"
        done = False
        while timeout > 0:
            timeout -= 5
            time.sleep(5)
            response = requests.get(merge_request_url, headers=headers)
            if response.json()["merge_status"] == "checking":
                logging.info(f"{project_name}/{merge_request_id}: checking waiting 5 seconds")
                continue
            done = True
        if not done:
            raise RuntimeError(f"Merge Request Checking Timeout after {timeout} seconds")
        merge_url = f"{cls.api_url}projects/{project_id}/merge_requests/{merge_request_id}/merge"
        data = {"should_remove_source_branch": True, "merge_commit_message": title}
        response = requests.put(merge_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Failed to perform merge {project_name}/{merge_request_id}', response.text)

    @classmethod
    def get_commits_by_range(cls, start_ref: str, end_ref: str, project_name: str, group_id: int):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        tag_url = f"{cls.api_url}projects/{project_id}/repository/commits"
        params = {"ref_name": f"{start_ref}...{end_ref}"}
        response = requests.get(tag_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()

    @classmethod
    def get_commits_since(cls, since_date: str, project_name: str, group_id: int):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        tag_url = f"{cls.api_url}projects/{project_id}/repository/commits"
        params = {"since": f"{since_date}"}
        response = requests.get(tag_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()

    @classmethod
    def get_tag_list(cls, project_name: str, group_id: int):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        tag_url = f"{cls.api_url}projects/{project_id}/repository/tags"
        params = {"order_by": "version"}
        response = requests.get(tag_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()

    @classmethod
    def get_tag_info(cls, tag_name: str, project_name: str, group_id: int):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        tag_url = f"{cls.api_url}projects/{project_id}/repository/tags/{tag_name}"
        response = requests.get(tag_url, headers=headers)
        if response.status_code == 200:
            return response.json()

    @classmethod
    def tag_project(cls, tag_name: str, project_name: str, remote_branch: str, group_id: int):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        tag_info = cls.get_tag_info(tag_name, project_name, group_id)
        if not tag_info:
            tag_url = f"{cls.api_url}projects/{project_id}/repository/tags"
            tag_form = {'tag_name': tag_name, 'ref': remote_branch, 'message': tag_name}
            response = requests.post(tag_url, headers=headers, data=tag_form)
            if response.status_code == 201:
                print(f'Successfully tagged {tag_name}')
            else:
                print(f'Failed to tag {tag_name}:', response.text)

    @classmethod
    def get_project_variable(cls, project_name: str, key: str, group_id: int):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        key_url = cls.api_url + f"projects/{project_id}/variables/{key}"
        response = requests.get(key_url, headers=headers)
        if response.status_code == 200:
            return response.json()

    @classmethod
    def set_project_variable(cls, project_name: str, key: str, value: str, group_id: int,
                             is_file: bool = False, overwrite: bool = True):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        variable_payload = {
            "key": key,
            "value": value,
            "variable_type": "file" if is_file else "env_var",
            "protected": False,
            "masked": False if is_file or len(value) < 8 else True,
        }
        key_url = cls.api_url + f"projects/{project_id}/variables/{key}"
        create_url = cls.api_url + f"projects/{project_id}/variables"
        response = requests.get(key_url, headers=headers)
        if response.status_code == 200:
            if overwrite:
                response = requests.put(key_url, headers=headers, data={"value": value})
            else:
                print(f"Environment variable {key} exists and it is requested to not overwrite it")
                return
        else:
            response = requests.post(create_url, headers=headers, json=variable_payload)
        # Check the response
        if 200 <= response.status_code < 300:
            print(f"Environment variable {key} set successfully.")
        else:
            print(f"Failed to set environment variable {key}. Response:", response.text)

    @classmethod
    def get_group_variable(cls, group_id: int, key: str):
        key_url = cls.api_url + f"groups/{group_id}/variables/{key}"
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        response = requests.get(key_url, headers=headers)
        if response.status_code == 200:
            return response.json()

    @classmethod
    def set_group_variable(cls, group_id: int, key: str, value: str, is_file: bool = False, overwrite: bool = True):
        variable_payload = {
            "key": key,
            "value": value,
            "variable_type": "file" if is_file else "env_var",
            "protected": False,
            "masked": False if is_file else True,
        }
        key_url = cls.api_url + f"groups/{group_id}/variables/{key}"
        create_url = cls.api_url + f"groups/{group_id}/variables"
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        response = requests.get(key_url, headers=headers)
        if response.status_code == 200:
            if overwrite:
                response = requests.put(key_url, headers=headers, data={"value": value})
            else:
                print(f"Environment variable {key} exists and it is requested to not overwrite it")
                return
        else:
            response = requests.post(create_url, headers=headers, json=variable_payload)
        # Check the response
        if 200 <= response.status_code < 300:
            print(f"Environment variable {key} set successfully.")
        else:
            print(f"Failed to set environment variable {key}. Response:", response.text)

    @classmethod
    def get_pipeline_status(cls, project_name: str, group_id: int, ref: str = "master", last_minutes: int = 1440):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_info = cls.get_project_info(project_name, group_id)
        if not project_info:
            print(f"Project {project_name} doesn't exist")
            return
        pipeline_url = cls.api_url + f"projects/{project_info['id']}/pipelines"
        params = {"ref": ref, "updated_after": (datetime.utcnow() - timedelta(minutes=last_minutes)).isoformat() + 'Z'}
        response = requests.get(pipeline_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get pipeline status {project_name}/{ref}. Response:", response.text)

    @classmethod
    def get_single_pipeline_status(cls, project_id, pipeline_id):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        pipeline_url = cls.api_url + f"projects/{project_id}/pipelines/{pipeline_id}"
        response = requests.get(pipeline_url, headers=headers)
        if response.status_code == 200:
            return response.json()

    @classmethod
    def retry_single_pipeline(cls, project_id, pipeline_id):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        pipeline_url = cls.api_url + f"projects/{project_id}/pipelines/{pipeline_id}/retry"
        response = requests.post(pipeline_url, headers=headers)
        if response.status_code == 200:
            return response.json()

    @classmethod
    def create_issue(cls, project_name: str, group_id: int, title: str, issue_type: str, labels: list = None):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        issue_url = cls.api_url + f"projects/{project_id}/issues"
        labels = [] if not labels else labels
        params = {"title": title, "issue_type": issue_type, "labels": ",".join(labels)}
        response = requests.post(issue_url, headers=headers, params=params)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Failed to create issue {project_name}. Response:", response.text)

    @classmethod
    def close_issue(cls, project_name: str, group_id: int, issue_id: int):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        issue_url = cls.api_url + f"projects/{project_id}/issues/{issue_id}"
        params = {"state_event": "close"}
        response = requests.put(issue_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to close issue {project_name}/{issue_id}. Response:", response.text)

    @classmethod
    def create_note(cls, project_name: str, group_id: int, issue_id: int, note_body: str):
        headers = {'PRIVATE-TOKEN': cls.gitlab_token}
        project_id = cls.get_project_info(project_name, group_id)["id"]
        note_url = cls.api_url + f"projects/{project_id}/issues/{issue_id}/notes"
        params = {"body": note_body}
        response = requests.post(note_url, headers=headers, params=params)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Failed to create note {project_name}. Response:", response.text)
