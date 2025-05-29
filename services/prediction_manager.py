import docker
from docker import DockerClient
from docker.errors import DockerException
import pandas as pd
from sklearn.linear_model import LinearRegression
from models.docker_model import PredictionResult, ContainerStats


class ContainerMemoryManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except DockerException as e:
            print(f"[DockerClient] Docker is not available: {e}")
            self.client = None

        self.df = pd.DataFrame()
        self.model = LinearRegression()

    def get_client(self):
        if self.client is None:
            try:
                self.client = docker.from_env()
            except DockerException as e:
                print(f"[DockerClient] Docker is not available: {e}")
                return None
        return self.client

    def fetch_container_stats(self):
        client = self.get_client()
        if client is None:
            raise RuntimeError(
                "Docker client unavailable. Cannot fetch stats.")

        try:
            client.ping()
        except Exception as e:
            raise RuntimeError(
                "Docker is not running or not accessible.") from e

        containers = client.containers.list()
        data = []

        for container in containers:
            try:
                stats = container.stats(stream=False)
                memory_mb = stats["memory_stats"]["usage"] / (1024 ** 2)
                data.append({
                    "name": container.name,
                    "memory_usage": memory_mb
                })
            except Exception as e:
                print(
                    f"⚠️ Could not fetch stats for container {container.name}: {e}")

        self.df = pd.DataFrame(data)
        self.df['index'] = self.df.index

    def predict_memory_usage(self) -> PredictionResult:
        if self.df.empty:
            self.fetch_container_stats()

        container_data = [
            ContainerStats(name=row['name'], memory_usage=row['memory_usage'])
            for _, row in self.df.iterrows()
        ]

        predicted = max(0, self.df['memory_usage'].mean())

        summary_lines = [
            f"- Container **{row['name']}** is currently using {row['memory_usage']:.2f} MB of memory."
            for _, row in self.df.iterrows()
        ]

        summary_lines.append(
            f"\n🔮 Predicted memory usage for the next container or time step: **{predicted:.2f} MB**."
        )
        summary_lines.append(
            f"\n📢 Summary: Based on current average usage, next memory reading is estimated around {predicted:.1f} MB."
        )

        return PredictionResult(
            data=container_data,
            predicted_next=predicted,
            summary="\n".join(summary_lines)
        )
