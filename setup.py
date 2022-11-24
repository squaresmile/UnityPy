import os
import re
import platform
from setuptools import setup, Extension, find_packages


INSTALL_DIR = os.path.dirname(os.path.realpath(__file__))
UNITYPYBOOST_DIR = os.path.join(INSTALL_DIR, "UnityPyBoost")

version = None
with open(os.path.join(INSTALL_DIR, "UnityPy", "__init__.py"), "rt") as f:
    version = re.search(r'__version__ = "([^"]+)"', f.read()).group(1)


def get_fmod_library():
    # determine system - Windows, Darwin, Linux, Android
    system = platform.system()
    if system == "Linux" and "ANDROID_BOOTLOGO" in os.environ:
        system = "Android"
    # determine architecture
    machine = platform.machine()
    arch = platform.architecture()[0]

    lib_name = ""
    if system in ["Windows", "Darwin"]:
        lib_name = "fmod.dll" if system == "Windows" else "libfmod.dylib"
        if arch == "32bit":
            arch = "x86"
        elif arch == "64bit":
            arch = "x64"
    elif system == "Linux":
        lib_name = "libfmod.so"
        # Raspberry Pi and Linux on arm projects
        if "arm" in machine:
            if arch == "32bit":
                arch = "armhf" if machine.endswith("l") else "arm"
            elif arch == "64bit":
                return None
        elif arch == "32bit":
            arch = "x86"
        elif arch == "64bit":
            arch = "x86_64"
    else:
        return None

    return f"lib/FMOD/{system}/{arch}/{lib_name}"


packages = find_packages()
packages += [
    "UnityPy.resources",
    "UnityPy.tools",
    "UnityPy.tools.libil2cpp_helper",
    "tests",
    "tests.samples",
]
unitypy_package_data = ["resources/uncompressed.tpk"]
fmod_lib = get_fmod_library()
if fmod_lib is not None:
    unitypy_package_data.append(fmod_lib)


setup(
    packages=packages,
    package_data={
        "UnityPy": unitypy_package_data,
        "": ["*.c", "*.h"],
    },
    version=version,
    ext_modules=[
        Extension(
            "UnityPy.UnityPyBoost",
            [
                f"UnityPyBoost/{f}"
                for f in os.listdir(UNITYPYBOOST_DIR)
                if f.endswith(".c")
            ],
            language="c",
            include_dirs=[UNITYPYBOOST_DIR],
        )
    ],
)
