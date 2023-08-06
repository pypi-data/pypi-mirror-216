# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'stubs'}

packages = \
['Boost-stubs', 'pxr-stubs']

package_data = \
{'': ['*'],
 'pxr-stubs': ['Ar/*',
               'CameraUtil/*',
               'Garch/*',
               'GeomUtil/*',
               'Gf/*',
               'Glf/*',
               'Kind/*',
               'Ndr/*',
               'Pcp/*',
               'Plug/*',
               'PxOsd/*',
               'Sdf/*',
               'Sdr/*',
               'SdrGlslfx/*',
               'Tf/*',
               'Tf/testenv/*',
               'Trace/*',
               'Usd/*',
               'UsdAppUtils/*',
               'UsdBakeMtlx/*',
               'UsdGeom/*',
               'UsdHydra/*',
               'UsdImagingGL/*',
               'UsdLux/*',
               'UsdMedia/*',
               'UsdMtlx/*',
               'UsdPhysics/*',
               'UsdProc/*',
               'UsdRender/*',
               'UsdResolverExample/*',
               'UsdRi/*',
               'UsdSchemaExamples/*',
               'UsdShade/*',
               'UsdShaders/*',
               'UsdSkel/*',
               'UsdUI/*',
               'UsdUtils/*',
               'UsdVol/*',
               'Usdviewq/*',
               'Vt/*',
               'Work/*']}

setup_kwargs = {
    'name': 'types-usd',
    'version': '23.5.0',
    'description': "Unofficial python stubs for Pixar's Universal Scene Description (USD)",
    'long_description': "# Unofficial python stubs for Pixar's Universal Scene Description (USD)\n\nThese stubs are designed to be used with a type checker like `mypy` to provide static type checking of USD python code, as well as to provide analysis and completion in IDEs like PyCharm and VSCode (with Pylance).\n\n## Installing\n\n```commandline\npip install types-usd\n```\n\nThe version of the package corresponds to the version of USD that it generated from,\nplus a suffix for the version of the stubs.\n\nThe stubs have been tested against a large USD codebase using `mypy`, however, there\nare still known issues that need to be resolved.\n\nUsing these stubs with `mypy` will produce erros within the stubs themselves, mostly about \nmissing/unknown types.  I've left these errors unsilenced as a reminder to fix them. \nI recommend adding the following config to your `mypy.ini` to silence these errors:\n\n```ini\n[mypy-pxr.*]\nignore_errors = true\n```\n\nIf you find any other issues, please report them on the [github issues page](https://github.com/LumaPictures/cg-stubs/issues).\n\n## Developing\n\nThe stubs are created using information extracted from python signatures generated\nby boost-python in each function's docstring, combined with data parsed as from the USD C++ docs.\n\nCurrently, creating the stubs requires custom forks of mypy and USD, but I hope to have\nmy changes merged into upstream soon.\n",
    'author': 'Chad Dombrova',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LumaPictures/cg-stubs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
