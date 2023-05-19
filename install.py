import os

user = os.environ["ESSENTIA_USERNAME"].split(".")[0].replace("_", ".")

file_path = f"/Users/{user}/.aws/config"
with open(file_path, "r+") as file:
    lines = file.readlines()

    line_1 = "function awp {\n"
    line_2 = "  eval `~/essentia/awp/main.py $@`\n"
    line_3 = "}\n"

    found_line_1 = False
    for line in reversed(lines):
        if line.strip() == line_1.strip():
            found_line_1 = True
            break

    if not found_line_1:
        file.write(line_1)
        file.write(line_2)
        file.write(line_3)
        print("Lines written to the file.")
    else:
        print("Line 1 already exists in the file.")
