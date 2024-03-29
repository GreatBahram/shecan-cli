## 0.4.1 (2021-03-16)

- Use No Color ANSI code for ending color lines.

## 0.4.0 (2021-03-16)

- Remove extraneous third-party libraries
- Use urllib.request library instead of a third-party library such as requests
- Remove colorama library and use a custom approach for printing in color.

## 0.3.4 (2021-01-20)

- Copy current resolv file instead of moving it: Moving resolv file is not allowed in docker env.
- Improve error handling

## 0.3.3 (2020-01-23)

- Use `colorama` for printing colorful text

## 0.3.2 (2020-01-23)

- Bugfix (Showing debug message when no dns nameservers found.)

## 0.3.1 (2020-01-23)

- Bugfix (Prevent showing error when configfile doesn't exist.)

## 0.3.0 (2020-01-23)

- Get rid of tinydb dependency.
- Add pre-commit file and bumpversion to make it easier to maintaine.

## 0.2.4 (2019-01-??)

- Replace `os.path` with `pathlib` module.
- Remove `__version__` which was awkward, replace it via `setup.cfg`.

## 0.2.3 (2019-01-08)

- Add `--version` option.

## 0.2.2 (2018-12-14)

- Add `show` subcommand to print current DNS configuration.
- Make output of `verify` function colorful.
- Tabulate output of `list` and `show` commmand.

## 0.2.1 (2018-12-11)

- Add `restore` subcommand to restore previous `resolv` file.
- update `get_ips` function to work with new shecan website update.
- add more type hints.

## 0.2.0 (2018-12-10)

- Write all shecan dns name servers into /etc/resolv.conf by default.
- Raise notimplementationError for --permanent option.
- Refactor and check all modules code styles.
- Update `setup.py` file.

## 0.1.0 (2018-12-10)

- Initial release.
