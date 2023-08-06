
class TestSessionValidator:
    @staticmethod
    def validate_project_name(project_name: str) -> str:
        if not project_name:
            raise ValueError("Project name is required.")
        
        # Check if project_name contains any special characters except "_"
        allowed_chars = set("._-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")

        if not set(project_name).issubset(allowed_chars):
            raise ValueError("Project name should only contain alphanumeric characters and '_', '.'.")
        # Additional validation logic specific to project id
        return project_name

    @staticmethod
    def validate_run_name(run_name: str) -> str:
        if not run_name:
            raise ValueError("Run name is required.")
        # Check if run_name contains any special characters except "_"
        allowed_chars = set("._-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")

        if not set(run_name).issubset(allowed_chars):
            raise ValueError("Run name should only contain alphanumeric characters and '_', '.'.")
        # Additional validation logic specific to run name
        return run_name


