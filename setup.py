setup(
    name="mycopernicus",
    version="1.0.0",
    description="",
    author="Santiago Basañes",
    author_email='santi.basanes@gmail.com',
    url='https://github.com/tiagobasagh/mycopernicus',
    packages=find_packages(include=["mycopernicus", "mymarinecopernicus", "mycopernicus.*"]),
    install_requires=[
        "pydap",
        "xarray", 
    ],
    setup_requires=["flake8", "black"],
)