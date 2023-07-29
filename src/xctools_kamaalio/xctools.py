import subprocess
from typing import Literal


class XcTools:
    @classmethod
    def archive(
        cls,
        scheme: str,
        configuration: Literal["Debug", "Release"],
        destination: str,
        sdk: Literal["macosx", "iphoneos"],
        archive_path: str,
        **kwargs,
    ):
        command = [
            "zsh",
            "-c",
            f'xcodebuild archive -scheme "{scheme}" -configuration {configuration}'
            + f'-destination "{destination}" -sdk {sdk} -archivePath "{archive_path}"',
        ]

        if project := kwargs.get("project"):
            command[-1] += f' -project "{project}"'
        elif workspace := kwargs.get("workspace"):
            command[-1] += f' -workspace "{workspace}"'
        else:
            raise XcToolsException("No workspace or project provided")
        cls.__run_command(command, "archive")

    @classmethod
    def upload(
        cls, target: Literal["ios", "macos"], file: str, username: str, password: str
    ):
        command = [
            "zsh",
            "-c",
            f'xcrun altool --upload-app -t {target} -f "{file}" -u {username} -p "{password}"',
        ]
        cls.__run_command(command, "upload")

    @staticmethod
    def __run_command(command: list[str], command_type: str):
        process = subprocess.Popen(command)
        status = process.wait()
        if status != 0:
            raise XcToolsException(f"Failed {command_type} with status='{status}'")


class XcToolsException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
