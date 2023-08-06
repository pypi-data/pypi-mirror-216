from koldar_utils.setuptools_toolbox import library_setup


s = library_setup.LibraryScriptSetup(
    author="Massimo Bono",
    author_mail="massimobono1@gmail.com",
    description="Generates docx from docs Jinja2 templates",
    keywords=["docx", "template", "jinja2"],
    home_page="https://github.com/Koldar/django-koldar-common-apps",
    python_minimum_version="3.6",
    license_name="MIT",
    main_package="docx_word_instance_generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

if __name__ == "__main__":
    # introducted to handle the scenario: if we import thsi script only in order to fetch installation fields but not
    # for running the scripts (e.g., sphinx)
    s.perform_setup()
