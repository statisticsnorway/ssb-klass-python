from nox_poetry import session


@session()
def run_coverage(session, cov_fail: int = 23):
    session.install(".")
    session.install("coverage[toml]")

    session.run("coverage", "report", f"--fail-under={cov_fail}")
