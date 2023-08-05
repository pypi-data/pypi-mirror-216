from typing import Optional

from pydantic import BaseSettings
from pydantic import Field


class GitLabCustomCommandConfig(BaseSettings):
    """Config parameters needed throughout the process read from the environment"""

    ci_job_image: str
    ci_pipeline_id: str
    ci_job_id: str
    ci_concurrent_id: str
    ci_concurrent_project_id: str
    ci_runner_short_token: str
    ci_project_name: str
    ci_registry: Optional[str]
    ci_registry_user: Optional[str]
    ci_registry_password: Optional[str]

    tart_registry_username: Optional[str]
    tart_registry_password: Optional[str]
    tart_registry: Optional[str]

    tart_ssh_username: Optional[str]
    tart_ssh_password: Optional[str]

    tart_max_vm_count: Optional[int] = Field(default=2)

    class Config:
        """Define the prefix used by GitLab for all environment variables passed to a custom driver.
        see https://docs.gitlab.com/runner/executors/custom.html#stages
        """

        env_prefix = "CUSTOM_ENV_"

    def vm_name(self):
        """Creates a unique name for a VM"""
        return f"{self.vm_name_prefix}-{self.ci_project_name}-{self.ci_pipeline_id}-{self.ci_job_id}-{self.ci_concurrent_id}"

    @property
    def vm_name_prefix(self):
        return "grtd"
