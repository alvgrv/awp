# awp

The command line utility `awp` makes it easy to switch between AWS profiles on the command line.

```
`awp brown`  # activates the brown profile
`awp shared`  # activates the shared-services profile
`awp -a f100530`  # activates the admin version of the ab profile
```

## Installation

As Python command line scripts cannot set environment variables in their parent shell, a zsh function is required to be installed in the .zshrc file. This function passes the args to the awp.py script and executes the output in the parent shell.

* Clone this repo into your `~/essentia` directory
* Enter the awp directory that was created and run `python install.py`
* Now the `awp` command will be available to you in any terminal window

## Usage

```
usage: awp [-a] [profile_name]

positional arguments:
  profile_name  A short profile name e.g. ab, f100530, testres2, live-app, shared, legacy

optional arguments:
  -a, --admin   Switches to the admin version of the profile

example usage:
`awp`  # deactivates any profile that is active
`awp brown`  # activates the brown profile
`awp shared`  # activates the shared-services profile
`awp -a f100530`  # activates the admin version of the ab profile
```