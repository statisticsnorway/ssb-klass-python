from nox_poetry import session


@session()
def run_coverage(session, cov_fail: int = 23):
    session.install(".")
    session.install("coverage[toml]", "pytest")

    session.run("coverage", "run", "-m", "pytest")
    session.run("coverage", "report", "--skip-empty", f"--fail-under={cov_fail}")
