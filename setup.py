from setuptools import setup

setup(name="mwdb-drakvuf-plugin",
      version="0.1.0",
      description="MWDB Drakvuf Sandbox plugin",
      author="CERT Polska",
      author_email="info@cert.pl",
      packages=["mwdb_drakvuf_plugin"],
      install_requires=[
          "mwdb-core",
          "requests"
      ])
