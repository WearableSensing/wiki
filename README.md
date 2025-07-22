# Wearable Sensing Techincal Documentation 

## Install

- `pip install -r requirements.txt`

## Build

You can manually build the code from within the docs folder and then navidate to `index.html` using,
> `sphinx-build . _build`

A better approach is to use sphinx autobuild to spin up a server that re-builds everytime a file is added or changed in the docs directory.

```sh
sphinx-autobuild docs docs/_build/html
```

This should print several things to the terminal and if the build is scucceful a final message like this will appear where you can see the page,

> [sphinx-autobuild] Serving on http://127.0.0.1:8000
