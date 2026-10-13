from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    container_hostname: str = "py-container"
    cgroup_dir: str = "/sys/fs/cgroup"
    cgroup_config: str = "cgroup.json"
    fs_root: str = "fs"
    fs_dir: str = "/"

    @property
    def process_cgroup_dir(self) -> str:
        return f"{self.cgroup_dir}/{self.container_hostname}"

settings = Settings()
