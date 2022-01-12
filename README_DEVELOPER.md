# naming-media-files-by-datetime README for developers

# Table of contents
1. [Git commit message best practices](#Git-commit-message-best-practices)
1. [Build executable (Windows)](#Build-executable-Windows)

# Git commit message best practices
Mainly following the conventions suggested by [kazupon/git-commit-message-convention](https://github.com/kazupon/git-commit-message-convention). Therefore, this section is copied and modified from [kazupon/git-commit-message-convention](https://github.com/kazupon/git-commit-message-convention), which is licensed under the [MIT License](https://github.com/kazupon/git-commit-message-convention/blob/master/LICENSE).

## Commit message format
```
<Type>[(<Scope>)]: <Subject>
<BLANK-LINE-IF-ADDING-MESSAGE-BODY>
[<Message Body>]
<BLANK-LINE-IF-ADDING-MESSAGE-FOOTER>
[<Message Footer>]


NOTE:
<...>: Replace it will relevant/required content
[...]: Optional fields
```

## Commit message types
| Type          | Description                                                  |
| ------------- | ------------------------------------------------------------ |
| `new`         | This commit contains new feature(s)                          |
| `bug`         | This commit fixes bug(s) (including missing semi-colon)      |
| `docs`        | This commit modifies documentations (readme, notes, etc.)    |
| `example`     | This commit adds/modifies example codes                      |
| `test`        | This commit adds/modifies test codes                         |
| `security`    | This commit fixes security issue(s)                          |
| `performance` | This commit improves system performance                      |
| `refactor`    | This commit refactors the codes, without change any feature (change code structures, change variables naming, etc.) |
| `wip`         | This commit is ADDING something, but has yet to be done. Changes to existing codes must be completed before committing. |
| `deprecated`  | This commit alters deprecated feature(s)                     |
| `revert`      | This commit reverts a previous commit. Message body should says: This reverts commit `hash-of-commit-being-reverted`. |
| `chore`       | This commit changes very minor things that does not fall into any type above |

## Scope
Specifying place or category of the commit change.

## Subject
- Use the imperative, present tense: "change" not "changed" nor "changes".
- Don't capitalize first letter.
- No dot (.) at the end.

## Message Body
- Same requirements as in Subject.
- Include the motivation for the change and contrast this with previous behaviour.

## Message Footer
- Refer to GitHub issue ID, such as `Issue #27`, `Fixes #1`, `Closes #2`, `Resolves #3`.

# Build executable (Windows)
1. Ensure bash emulator exists.
    - e.g. Installing [Git for Windows](https://gitforwindows.org/) should provide you with bash emulation.
1. Install `pyinstaller`
    - `pip install pyinstaller`
1. Add the directory of `pyinstaller` to user's *PATH* variable (if not already done).
    - Add `C:\Users\<User name>\AppData\Roaming\Python\<e.g. Python38>\Scripts` to *PATH*
    - [Tutorial](https://stackoverflow.com/a/45952113)
1. Ensure `pyinstaller` is recognized
    - `pyinstaller -v`
1. Run `bundle.sh` in bash emulator
    - `bundle.sh`
1. Obtain the built files in project's `export` directory.
    - The built files will be stored in a directory named by the date and time (`YYYYMMDD_HHMMSS` format) that the executables are built.
1. The built files can be distributed.
