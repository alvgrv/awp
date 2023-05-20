"""Installer for the `awp` command line utility.

Python scripts cannot set environment variables in the parent shell, so this script installs a function in the
    user's ~/.zshrc file which evaluates the output of the script awp.py and applies it to the parent shell

If the function already exists in ~/.zshrc, no action is taken.

The .zsh function is as follows:
```
function awp {
  eval `~/essentia/awp/awp.py $@`
}
```

"""

import os

user = os.environ["ESSENTIA_USERNAME"].split(".")[0].replace("_", ".")

file_path = f"/Users/{user}/.zshrc"
with open(file_path, "r+") as file:
    lines = file.readlines()

    line_1 = "function awp {\n"
    line_2 = "  eval `~/essentia/awp/awp.py $@`\n"
    line_3 = "}\n"

    found_line_1 = False
    for line in reversed(lines):
        if line.strip() == line_1.strip():
            found_line_1 = True
            break

    if not found_line_1:
        file.write("\n")
        file.write(line_1)
        file.write(line_2)
        file.write(line_3)
        file.write("\n")
        print("awp was successfully installed to your .zshrc file")
    else:
        print("awp is already installed in your .zshrc file")
