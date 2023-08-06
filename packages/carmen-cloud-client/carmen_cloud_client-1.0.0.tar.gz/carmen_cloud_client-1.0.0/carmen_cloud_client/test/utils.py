import re

def extract_api_version_from_readme(api_name: str) -> str:
    with open('README.md', 'r') as file:
        readme = file.read()
    regex = re.compile(f"- {api_name}: v([0-9]\\.[0-9])")
    match = regex.search(readme)
    return match.group(1) if match else ''
