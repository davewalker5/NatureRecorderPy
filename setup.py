import os
import setuptools


def find_package_files(directory, remove_root):
    """
    Walk the filesystem from the specifed directory to get a recursive list of files. Remove the start of each
    if it matches the specified removal string to leave paths relative to their containing package

    :param directory: Path to the folder to walk
    :param remove_root: Remove this if it appears at the start of a file path
    :return: A list of file paths relative to a package folder
    """
    file_paths = []
    for (path, directories, filenames) in os.walk(directory):
        # Remove the start of the path to leave the path relative to the package folder
        if path.startswith(remove_root):
            path = path[len(remove_root):]

        for filename in filenames:
            file_paths.append(os.path.join(path, filename))

    return file_paths


# The package data for the web package includes the whole directory tree for the static files plus
# the Flask view templates
naturerec_web_package_data = find_package_files("src/naturerec_web/static", "src/naturerec_web/")
naturerec_web_package_data.append("templates/*.html")


setuptools.setup(
    name="nature_recorder",
    version="1.15.0",
    description="Wildlife sightings database",
    packages=setuptools.find_packages("src"),
    include_package_data=True,
    package_dir={"": "src"},
    package_data={
        "naturerec_web": naturerec_web_package_data,
        "naturerec_web.auth": ["templates/auth/*.html"],
        "naturerec_web.categories": ["templates/categories/*.html"],
        "naturerec_web.export": ["templates/export/*.html"],
        "naturerec_web.jobs": ["templates/jobs/*.html"],
        "naturerec_web.life_list": ["templates/life_list/*.html"],
        "naturerec_web.locations": ["templates/locations/*.html"],
        "naturerec_web.reports": ["templates/reports/*.html"],
        "naturerec_web.sightings": ["templates/sightings/*.html"],
        "naturerec_web.species": ["templates/species/*.html"],
        "naturerec_web.species_ratings": ["templates/species_ratings/*.html"],
        "naturerec_web.status": ["templates/status/*.html"],
    }
)
