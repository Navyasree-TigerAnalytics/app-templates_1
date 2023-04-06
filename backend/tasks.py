import os
import os.path as op
import platform
from contextlib import contextmanager
import shutil
import tempfile
import time
import yaml
from invoke import Collection, UnexpectedExit, task

# Some default values
PACKAGE_NAME = "discount-tool"
ENV_PREFIX = "django-rest"
NUM_RETRIES = 10
SLEEP_TIME = 1

OS = platform.system().lower()
ARCH = platform.architecture()[0][:2]
PLATFORM = f"{OS}-cpu-{ARCH}"
DEV_ENV = "dev"  # one of ['dev', 'run', 'test']

HERE = op.dirname(op.abspath(__file__))
SOURCE_FOLDER = op.join(HERE, "src", PACKAGE_NAME)
TESTS_FOLDER = op.join(HERE, "tests")
CONDA_ENV_FOLDER = op.join(HERE, "deploy", "conda_envs")
NOTEBOOK_FOLDER = op.join(HERE, "notebooks", "tests")

WEB_APP_FOLDER = op.join(HERE, "src", "discount_tool", "web_api")

_TASK_COLLECTIONS = []

# ---------
# Utilities
# ---------
def _get_env_name(platform, env):
    # FIXME: do we need platform ?
    # return f"{ENV_PREFIX}-{env}"
    return "djangorest"


def _change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for _dir in [os.path.join(root, d) for d in dirs]:
            os.chmod(_dir, mode)
        for _file in [os.path.join(root, f) for f in files]:
            os.chmod(_file, mode)


def _clean_rmtree(path):
    for _try in range(NUM_RETRIES):
        try:
            _change_permissions_recursive(path, 0o777)
            shutil.rmtree(path)
        except Exception as e:
            time.sleep(SLEEP_TIME)
            print(f"{path} Remove failed with error {e}:: Retrying ..")
            continue
        print(f"{path} Remove Success")
        break


@contextmanager
def py_env(c, env_name):
    """Activate a python env while the context is active."""

    # FIXME: This works but takes a few seconds. Perhaps find a few to robustly
    # find the python path and just set the PATH variable ?
    if OS == "windows":
        # we assume conda binary is in path
        cmd = f"conda activate {env_name}"
    else:
        cmd = f'eval "$(conda shell.bash hook)" && conda activate {env_name}'
    with c.prefix(cmd):
        yield


@contextmanager
def switch_path(c, path):
    orig_path = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(orig_path)


def _create_task_collection(name, *tasks):
    """Construct a Collection object."""
    coll = Collection(name)
    for task_ in tasks:
        coll.add_task(task_)
    _TASK_COLLECTIONS.append(coll)
    return coll


def _create_root_task_collection():
    return Collection(*_TASK_COLLECTIONS)


# -----------
# debug tasks
# -----------


@task(name="check-reqs")
def check_setup_prerequisites(c):
    _failed = []

    # check the folder has no spaces in the path
    if " " in HERE:
        raise RuntimeError("The path to the current folder has whitespaces in it.")

    for binary in ["git", "conda"]:
        try:
            out = c.run(f"{binary} --version", hide="out")
        except UnexpectedExit:
            print(
                f"ERROR: Failed to find `{binary}` in path. "
                "See `pre-requisites` section in `README.md` for some pointers."
            )
            _failed.append(binary)
        else:
            print(f"SUCCESS: Found `{binary}` in path : {out.stdout}")

    # FIXME: Figure out colored output (on windows) and make the output easier
    # to read/interpret.
    # for now, make a splash when failing and make it obvious.
    if _failed:
        raise RuntimeError(f"Failed to find the following binaries in path : {_failed}")


_create_task_collection("debug", check_setup_prerequisites)


# Dev tasks
# ---------
@task(
    help={
        "platform": (
            "Specifies the platform spec. Must be of the form "
            "``{windows|linux}-{cpu|gpu}-{64|32}``"
        ),
        "env": "Specifies the enviroment type. Must be one of ``{dev|test|run}``",
        "force": "If ``True``, any pre-existing environment with the same name will be overwritten",
    }
)
def setup_env(c, platform=PLATFORM, env=DEV_ENV, force=False):
    """Setup a new development environment.

    Creates a new conda environment with the dependencies specified in the file
    ``env/{platform}-{env}.yml``. To overwrite an existing environment with the
    same name, set the flag ``force`` to ``True``.
    """

    # run pre-checks
    check_setup_prerequisites(c)

    # FIXME: We might want to split the env.yml file into multiple
    # files: run.yml, build.yml, test.yml and support combining them for
    # different environments
    force_flag = "" if not force else "--force"

    env_file = op.abspath(op.join(CONDA_ENV_FOLDER, f"{platform}-{env}.lock"))
    req_file = op.abspath(
        op.join(CONDA_ENV_FOLDER, f"requirements-{platform}-{env}.txt")
    )
    req_flag = True
    if not op.isfile(env_file):
        raise ValueError(f"The conda env file is not found : {env_file}")
    if not op.isfile(req_file):
        req_flag = False
    env_name = _get_env_name(platform, env)

    out = c.run(f"conda create --name {env_name} --file {env_file}  {force_flag} -y")

    # check for jupyterlab
    with open(env_file, "r") as fp:
        env_cfg = fp.read()

    # installating jupyter lab extensions
    extensions_file = op.abspath(op.join(CONDA_ENV_FOLDER, "jupyterlab_extensions.yml"))
    with open(extensions_file) as fp:
        extensions = yaml.safe_load(fp)

    # install the code-template modules
    with py_env(c, env_name):

        # install pip requirements
        if req_flag:
            c.run(f"pip install -r {req_file} --no-deps")

        # install the current package
        c.run(f"pip install -e {HERE}")

        is_jupyter = False
        if "jupyterlab-" in env_cfg:
            is_jupyter = True

        if is_jupyter:
            # install jupyterlab extensions
            for extension in extensions["extensions"]:
                extn_name = "@{channel}/{name}@{version}".format(**extension)
                c.run(
                    f"jupyter labextension install --no-build {extn_name}",
                )

            out = c.run("jupyter lab build")

    # FIXME: create default folders that are expected. these need to be handled
    # when convering to cookiecutter templates
    os.makedirs(op.join(HERE, "logs"), exist_ok=True)
    os.makedirs(op.join(HERE, "docs", "build", "html"), exist_ok=True)
    os.makedirs(op.join(HERE, "mlruns"), exist_ok=True)
    os.makedirs(op.join(HERE, "data"), exist_ok=True)


@task(name="format-code")
def format_code(c, platform=PLATFORM, env=DEV_ENV, path="."):
    env_name = _get_env_name(platform, env)
    with py_env(c, env_name):
        c.run(f"black {path}", warn=True)
        c.run(f"isort -rc {path}")


@task(name="refresh-version")
def refresh_version(c, platform=PLATFORM, env=DEV_ENV):
    env_name = _get_env_name(platform, env)
    with py_env(c, env_name):
        pass
        # res = c.run(f"python {HERE}/setup.py --version")
    # return res.stdout


_create_task_collection(
    "dev",
    setup_env,
    format_code,
    refresh_version,
)


@task(name="run-server")
def run_server(c, platform=PLATFORM, env=DEV_ENV):
    env_name = _get_env_name(platform, env)
    with py_env(c, env_name):
        res = c.run(f"python {HERE}/src/discount_tool/web_api/manage.py runserver")
    # return res.stdout


@task(name="run-migration")
def run_migration(c, platform=PLATFORM, env=DEV_ENV):
    env_name = _get_env_name(platform, env)
    with py_env(c, env_name):
        with switch_path(c, WEB_APP_FOLDER):
            res = c.run(f"python manage.py migrate")


@task(name="make-migration")
def make_migration(c, app_name, platform=PLATFORM, env=DEV_ENV):
    env_name = _get_env_name(platform, env)
    with py_env(c, env_name):
        with switch_path(c, WEB_APP_FOLDER):
            # seems to somehow find from sub folders
            res = c.run(f"python manage.py makemigrations {app_name}")


@task(name="start-app")
def start_app(c, app_name, platform=PLATFORM, env=DEV_ENV):
    env_name = _get_env_name(platform, env)
    with py_env(c, env_name):
        with switch_path(c, WEB_APP_FOLDER):
            os.makedirs(f"apps/{app_name}", exist_ok=True)
            res = c.run(f"python manage.py startapp {app_name} apps/{app_name}")


_create_task_collection(
    "dj",
    run_server,
    make_migration,
    run_migration,
    start_app,
)


# -------------
# Test/QC tasks
# --------------
@task(name="qc")
def run_qc_test(c, platform=PLATFORM, env=DEV_ENV, fail=False):
    env_name = _get_env_name(platform, env)
    with py_env(c, env_name):
        # This runs flake8, flake8-black, flake8-isort, flake8-bandit,
        # flake8-docstring
        c.run(f"python -m flake8 {SOURCE_FOLDER}", warn=(not fail))


@task(name="unittest")
def run_unit_tests(c, platform=PLATFORM, env=DEV_ENV, markers=None):
    env_name = _get_env_name(platform, env)
    markers = "" if markers is None else f"-m {markers}"
    with py_env(c, env_name):
        # FIXME: Add others, flake9-black, etc
        c.run(f"pytest -v {TESTS_FOLDER} {markers}")


@task(name="vuln")
def run_vulnerability_test(c, platform=PLATFORM, env=DEV_ENV):
    env_name = _get_env_name(platform, env)
    # FIXME: platform agnostic solution: get the output from conda and then munge in python
    with py_env(c, env_name):
        c.run(
            f'conda list | tail -n +4 | tr -s " " " " '
            '| cut -f 1,2 -d " " | sed "s/\ /==/g" '
            "| safety check --stdin",
        )


@task(name="all")
def run_all_tests(c):
    run_qc_test(c)
    run_vulnerability_test(c)
    run_unit_tests(c)


_create_task_collection(
    "test",
    run_qc_test,
    run_vulnerability_test,
    run_unit_tests,
    run_all_tests,
)


# -----------
# Build tasks
# -----------
@task(name="docs")
def build_docs(c, platform=PLATFORM, env=DEV_ENV, regen_api=True, update_credits=False):
    env_name = _get_env_name(platform, env)
    with py_env(c, env_name):
        if regen_api:
            code_path = op.join(HERE, "docs", "source", "_autosummary")
            if os.path.exists(code_path):
                _clean_rmtree(code_path)
            os.makedirs(code_path, exist_ok=True)

        # FIXME: Add others, flake9-black, etc
        if update_credits:
            credits_path = op.join(HERE, "docs", "source", "_credits")
            if os.path.exists(credits_path):
                _clean_rmtree(credits_path)
            os.makedirs(credits_path, exist_ok=True)
            authors_path = op.join(HERE, "docs")
            token = os.environ["GITHUB_OAUTH_TOKEN"]
            c.run(f"python {authors_path}/generate_authors_table.py {token} {token}")
        c.run(
            "cd docs/source && sphinx-build -T -E -W --keep-going -b html -d ../build/doctrees  . ../build/html"
        )


_create_task_collection("build", build_docs)


# -----------
# Launch stuff
# -----------
@task(name="docs")
def start_docs_server(c, ip="127.0.0.1", port=8081):
    # FIXME: run as a daemon and support start/stop using pidfile
    c.run(
        f"python -m http.server --bind 127.0.0.1 " f"--directory docs/build/html {port}"
    )


@task(name="ipython")
def start_ipython_shell(c, platform=PLATFORM, env=DEV_ENV):
    env_name = _get_env_name(platform, env)
    # FIXME: run as a daemon and support start/stop using pidfile
    startup_script = op.join(HERE, "deploy", "ipython", "default_startup.py")
    with py_env(c, env_name):
        c.run(f"ipython -i {startup_script}")


_create_task_collection(
    "launch",
    start_docs_server,
    start_ipython_shell,
)

# --------------
# Root namespace
# --------------
# override any configuration for the tasks here
# FIXME: refactor defaults (constants) and set them as config after
# auto-detecting them
ns = _create_root_task_collection()
config = dict(pty=True, echo=True)

if OS == "windows":
    config["pty"] = False

ns.configure(config)
