import plissken


def test_version():
    """test plissken version"""

    assert plissken.__version__


def test_module_to_fqdn(directories):
    d = directories

    module = "test_module"
    files = [
        "test_module/test.py",
        "test_module/test1/test.py",
        "test_module/test2/test.py",
        "test_module/test3/test.py",
        "test_module/__init__.py",
        "test_module/test1/__init__.py",
        "test_module/test2/__init__.py",
        "test_module/test3/__init__.py",
    ]
    fqdns = [
        "test_module.test",
        "test_module.test1.test",
        "test_module.test2.test",
        "test_module.test3.test",
        "test_module",
        "test_module.test1",
        "test_module.test2",
        "test_module.test3",
    ]
    outputs = [
        "test_module/test",
        "test_module/test1/test",
        "test_module/test2/test",
        "test_module/test3/test",
        "test_module/index",
        "test_module/test1/index",
        "test_module/test2/index",
        "test_module/test3/index",
    ]

    return_struct = zip(files, fqdns)
    r_files, r_fqdns, r_outputs = plissken.module_to_fqdns("test_module")

    files.sort()
    fqdns.sort()
    r_fqdns.sort()
    r_files.sort()
    outputs.sort()
    r_outputs.sort()

    assert r_files == files
    assert r_fqdns == fqdns
    assert r_outputs == outputs
