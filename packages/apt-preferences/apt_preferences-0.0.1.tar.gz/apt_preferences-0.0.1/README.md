# Apt Preferences

## Description

Python package to modify apt preferences files in line with https://manpages.debian.org/buster/apt/apt_preferences.5.en.html.

I don't like using awk and sed for updating preferences cause it's got messier the bigger amount of preferences is connected to a package.
If regexes are used in packages names then it's even harder. This package along with `re` should make more complex preferences scenarios easy to automate. 

And I wanted to learn `LARK` so that is also a big pron of the project.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)

## Installation

Create virtual environment
```
make venv
```

Activate virtual environment
```
. .venv/bin/activate
```

Install package
```
make install
```

## Usage

```
from apt_preferences.data_structures import AptPreference
from apt_preferences.render_preferences_files import render_preferences_files

# lets assume this is a parsed preferences file
my_prefs_l = [AptPreference(package="*", pin="release n=jammy", pin_priority=700, file_path="/etc/apt/preferences", explanations={})]

# we would like to change pin priority for one of file preferences
my_pref = my_prefs_l[0]

# pin priority is modified
my_pref.pin_priority = 100

# preference with modified pin priority is saved to the file
render_preferences_files(my_prefs_l)
```

For more examples look into `/examples` directory.

Run example
```
python examples/read_preferences.py
```

### Features:
   - Parse apt preferences' files into Python objects list.
   - Generate new apt preferences' files based on Python objects list.

### Planned features:
   - Support multiple pins in single preference.
   - Comment out objects via AptPreference method.

### Limitations:

   - If a line starts with `#` it will be ignored by the parser.
   - The generator doesn't allow creating lines starting with `#`.


## Credits

Me, Myself and I.


## License

```
MIT License

Copyright (c) [2023] [Jakub Buczyński]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
---




