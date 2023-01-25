import nox


@nox.session(python="3.11")
def test311(session: nox.Session):
    session.run_always("poetry", "install", "--with", "test", external=True)
    session.run(
        "poetry",
        "run",
        "pytest",
        "--cov=Bot",
        "--cov-report=xml",
        "tests/redis",
        external=True,
    )


@nox.session(python="3.10")
def test310(session: nox.Session):
    session.run_always("poetry", "install", "--with", "test", external=True)
    session.run(
        "poetry",
        "run",
        "pytest",
        "--cov=Bot",
        "--cov-report=xml",
        "tests/redis",
        external=True,
    )


@nox.session(python="3.9")
def test39(session: nox.Session):
    session.run_always("poetry", "install", "--with", "test", external=True)
    session.run(
        "poetry",
        "run",
        "pytest",
        "--cov=Bot",
        "--cov-report=xml",
        "tests/redis",
        external=True,
    )


@nox.session(python="3.8")
def test38(session: nox.Session):
    session.run_always("poetry", "install", "--with", "test", external=True)
    session.run(
        "poetry",
        "run",
        "pytest",
        "--cov=Bot",
        "--cov-report=xml",
        "tests/redis",
        external=True,
    )
