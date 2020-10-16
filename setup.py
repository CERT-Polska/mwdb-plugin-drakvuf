from setuptools import setup

setup(name="mwdb-plugin-drakvuf",
      version="0.1.0",
      description="MWDB Drakvuf Sandbox plugin",
      author="CERT Polska",
      author_email="info@cert.pl",
      packages=["mwdb_plugin_drakvuf"],
      install_requires=[
          "mwdb-core",
          "requests"
      ])
