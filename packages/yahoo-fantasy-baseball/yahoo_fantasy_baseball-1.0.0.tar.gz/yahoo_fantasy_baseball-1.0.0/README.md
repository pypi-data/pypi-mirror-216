
# Yahoo-Bantasy-Baseball

[![PyPI version](https://badge.fury.io/py/yahoo-fantasy-baseball.svg)](https://img.shields.io/badge/build-passing-green)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

yahoo-fantasy-baseball is a Python package that provides a function to fetch live standings for a fantasy baseball league from Yahoo.

## Installation

You can install Your Package Name using pip: pip install your-package-name

## Usage

To use Your Package Name, import the `get_live_standings` function and call it with the league ID as the argument:

```python
from yahoo-fantasy-baseball import get_live_standings

# Replace LEAGUE_ID with the league ID of your league
df = get_live_standings(LEAGUE_ID)
```


The get_live_standings function retrieves the live standings for the specified league from Yahoo and returns the standings data as a DataFrame. You can then perform various operations on the DataFrame to analyze and manipulate the data according to your requirements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.