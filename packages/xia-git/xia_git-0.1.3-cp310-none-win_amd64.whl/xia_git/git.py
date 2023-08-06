import logging
import os
import filecmp
import stat
import shutil
import git


class Git:
    @classmethod
    def destroy_workspace(cls, work_path):
        for current_path, directories, files in os.walk(work_path, topdown=False):
            # Delete all files in the current directory
            for file in files:
                file_path = os.path.join(current_path, file)
                try:
                    os.remove(file_path)
                except OSError as e:
                    os.chmod(file_path, stat.S_IWRITE)
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        logging.error(f"Cannot remove file: {file_path}")

            # Remove current directory if it is empty
            # Since we're iterating in reverse, subdirectories will be empty
            for directory in directories:
                dir_path = os.path.join(current_path, directory)
                try:
                    os.rmdir(dir_path)
                except OSError as e:
                    os.chmod(dir_path, stat.S_IWRITE)
                    try:
                        os.rmdir(dir_path)
                    except OSError as e:
                        logging.error(f"Cannot remove directory: {dir_path}")

    @classmethod
    def clean_workspace(cls, work_path, destroy: bool = False):
        """Clean Workspace

        Args:
            work_path: Path to be cleaned
            destroy: Removing The directory itself. When it is false, ./.git/ will be kept
        """
        if not os.path.exists(work_path):
            return
        if ".git" not in os.listdir(work_path):
            raise ValueError("Workspace is not a git repository")
        if destroy:
            return cls.destroy_workspace(work_path)
        for item in os.listdir(work_path):
            item_path = os.path.join(work_path, item)
            if item == ".git" and os.path.isdir(item_path):
                continue
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                shutil.rmtree(item_path)

    @classmethod
    def compare_directories_recursive(cls, dir_a, dir_b, relative_path=''):
        """Compare file content
        """
        dir_comparison = filecmp.dircmp(os.path.join(dir_a, relative_path), os.path.join(dir_b, relative_path))

        # List of added, modified and deleted files
        added = [os.path.join(relative_path, f) for f in dir_comparison.left_only]
        deleted = [os.path.join(relative_path, f) for f in dir_comparison.right_only]

        # List of potentially modified files (files that are in both directories)
        maybe_modified = dir_comparison.common_files

        # Actual modified files (files with different contents)
        modified = [os.path.join(relative_path, f) for f in maybe_modified if not filecmp.cmp(
            os.path.join(dir_a, relative_path, f), os.path.join(dir_b, relative_path, f), shallow=False)]

        # Recursively compare subdirectories
        for common_dir in dir_comparison.common_dirs:
            new_relative_path = os.path.join(relative_path, common_dir)
            sub_added, sub_modified, sub_deleted = cls.compare_directories_recursive(dir_a, dir_b, new_relative_path)
            added.extend(sub_added)
            modified.extend(sub_modified)
            deleted.extend(sub_deleted)

        return added, modified, deleted

    @classmethod
    def get_operation_list(cls, source_path, target_path):
        added, modified, deleted = cls.compare_directories_recursive(source_path, target_path)
        change_list = {}
        for add in added:
            change_list[add] = {"operation": "add"}
        for modify in modified:
            change_list[modify] = {"operation": "modify"}
        for delete in deleted:
            change_list[delete] = {"operation": "delete"}
        return change_list

    @classmethod
    def get_update_instruction(cls, source_path, target_path, work_path):
        shutil.copytree(source_path, work_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git'))
        repo = git.Repo.init(work_path)
        with repo.config_writer() as git_config:
            git_config.set_value("user", "name", "Local")
            git_config.set_value("user", "email", "local@x-i-a.com")
        repo.git.add('.')  # Staging all files
        repo.git.commit('-m', 'Initial commit')
        cls.clean_workspace(work_path)
        shutil.copytree(target_path, work_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git'))
        repo.git.add('-A')  # Staging all files
        changed_files = cls.get_operation_list(target_path, source_path)
        # Get detailed patch information
        for changed_file, change_content in changed_files.items():
            if change_content["operation"] == "modify":
                change_details = repo.git.diff('HEAD', changed_file, unified=99999)
                change_content["patch"] = "\n".join(change_details.split('\n')[5:])
                with open(os.path.join(source_path, changed_file), 'r') as fp:
                    change_content["line_nb_source"] = len(fp.readlines())
                with open(os.path.join(target_path, changed_file), 'r') as fp:
                    change_content["line_nb_target"] = len(fp.readlines())
        cls.clean_workspace(work_path, destroy=True)
        return changed_files

