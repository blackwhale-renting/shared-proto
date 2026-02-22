from setuptools import setup
from setuptools.command.build_py import build_py
import subprocess
import glob
import os
import sys

class BuildProto(build_py):
    def run(self):
        cwd = os.getcwd()
        proto_files = glob.glob(f"{cwd}/proto/**/*.proto", recursive=True)
        package_name = "src/blackwhale_proto"

        os.makedirs(package_name, exist_ok=True)

        with open(os.path.join(package_name, "__init__.py"), "w") as f:
            # f.write(f"from . import message_pb2, message_pb2_grpc\n")
            pass

        for proto in proto_files:
            subprocess.check_call([
                sys.executable,
                "-m",
                "grpc_tools.protoc",
                f"-I{cwd}/proto",
                f"--python_out={package_name}",
                f"--grpc_python_out={package_name}",
                proto,
            ])

        super().run()


setup(
    cmdclass={
        "build_py": BuildProto,
    },
)