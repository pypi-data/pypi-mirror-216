from setuptools import Extension
from typing import Any, Dict

ext_modules=[
       Extension(
       name="libmi",   
       language="c",
       sources=["mi/mi1.c"], # all sources are compiled into a single binary file
       ),
]


def build(setup_kwargs: Dict[str, Any]) -> None:
    setup_kwargs.update(
       {
            "ext_modules": ext_modules
       }
    )

