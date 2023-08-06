
import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="certora-cli-alpha-oz-cli-by-os",
        version="20230627.12.3.846810",
        author="Certora",
        author_email="support@certora.com",
        description="Runner for the Certora Prover",
        long_description="Commit a89e1a4. Build and Run scripts for executing the Certora Prover on Solidity smart contracts.",
        long_description_content_type="text/markdown",
        url="https://pypi.org/project/certora-cli-alpha-oz-cli-by-os",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=['click', 'json5', 'pycryptodome', 'requests', 'sly', 'tabulate', 'tqdm'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        entry_points={
            "console_scripts": [
                "certoraRun = certora_cli.certoraRun:entry_point",
                "certoraMutate = certora_cli.certoraMutate:ext_gambit_entry_point",
                "certoraEqCheck = certora_cli.certoraEqCheck:ext_equivcheck_entry_point"
            ]
        },
        python_requires='>=3.8',
    )
        