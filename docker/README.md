# naturerecorderpy

The Nature Recorder is a personal widlife sightings logbook application implemented using Python.

The application provides facilities for recording and querying the following data:

- Locations, with the following details:
    - Unique name
    - Address details
    - Latitude and longitude
- Categories, with the following details:
    - Category name e.g. birds, mammals
- Species, with the following details:
    - The category to which the species belongs
    - Species name
- Species sightings, consisting of:
    - The species, and by implication the category the species belongs to
    - Location
    - Date
    - Gender of the animals seen
    - Number of animals seen (optional)
    - Whether or not they were seen with young
- Conservation status information, consisting of:
    - Conservation schemes, acting as containers for a set of rating values
    - Conservation status ratings, values for the conservation status within a scheme
    - Species conservation status ratings, status ratings for a species with effective start and end dates

The naturerecorderpy image contains a distribution of the application implementing a Flask-based web UI hosted on the Flask development server, for personal use only.

## Getting Started

### Prerequisities

In order to run this image you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)

### Usage

#### Container Parameters

The following "docker run" parameters are recommended when running the naturerecorderpy image:

| Parameter | Value | Purpose |
| --- | --- | --- |
| -d | - | Run as a background  process
| -v | /local:/var/opt/naturerecorderpy.api-1.0.11.0 | Mount the host folder containing the SQLite database |
| -p | 80:5000 | Expose the container's port 5000 as port 80 on the host |
| --rm | - | Remove the container automatically when it stops |

For example:

```shell
docker run -d -v /local:/var/opt/naturerecorderpy-1.0.11.0/ -p 80:5000 --rm davewalker5/naturerecorderpy:latest
```

The "/local" path given to the -v argument is described, below, and should be replaced with a value appropriate for the host running the container. Similarly, the port number "80" can be replaced with any available port on the host.

### Volumes

The description of the container parameters, above, specifies that a folder containing the SQLite database file for the application is mounted in the running container, using the "-v" parameter.

That folder should contain a SQLite database named "naturerecorder.db" containing the application schema.

#### Accessing the application the Image

To run the image, enter the following commands, substituting "/local" for the host folder containing the SQLite database, as described:

```shell
docker run -d -v /local:/var/opt/naturerecorderpy-1.0.11.0/ -p 80:5000 --rm davewalker5/naturerecorderpy:latest
```

Once the container is running, browse to the following URL on the host:

http://localhost:80

You should see the login page for the UI.

## Built With

The naturerecorderpy image was been built with the following:

| Aspect | Version |
| --- | --- |
| Python | 3.10.0 |
| Docker Desktop | 20.10.11 |

Other dependencies and their versions are listed in the project's [requirements.txt](https://github.com/davewalker5/NatureRecorderPy/blob/main/requirements.txt) file

## Find Us

* [NatureRecorderPy on GitHub](https://github.com/davewalker5/NatureRecorderPy)

## Versioning

For the versions available, see the [tags on this repository](https://github.com/davewalker5/NatureRecorderPy/tags).

## Authors

* **Dave Walker** - *Initial work* - [LinkedIn](https://www.linkedin.com/in/davewalker5/)

See also the list of [contributors](https://github.com/davewalker5/NatureRecorderPy/contributors) who 
participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/davewalker5/NatureRecorderPy/blob/master/LICENSE) file for details.
