MESSAGE = """
Use this command to install ci-secrets-cli:
python3 -m pip install ci-secrets-cli --index-url=https://artifactory.klarna.net/artifactory/api/pypi/r-pypi-pypi-org/simple --extra-index-url=https://artifactory.klarna.net/artifactory/api/pypi/v-pypi-production/simple
"""

def cli():
    print(MESSAGE)
