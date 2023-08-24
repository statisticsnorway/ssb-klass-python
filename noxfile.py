from nox_poetry import session


@session(python=["3.8", "3.9", "3.10", "3.11"])
def run_pytest_klass_folder(session, cov_fail: int = 23):
    session.install(".")
    session.install("coverage[toml]")
    session.run(
        "coverage",
        "report",
        "--include=klass/*",
        "--omit=*__init__.py",
        f"--fail-under={cov_fail}",
    )
