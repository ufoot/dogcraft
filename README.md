# DogCraft

This is proof of concept project making a bridge between DataDog metrics and Minecraft.
It allows you to view some custom DataDog dashboards within Minecraft. They show the real stuff.

Current features:

- display any metric, as long as you can formulate what you want as a query that returns a row of data
- skin them the way you want, change color, size, position
- customizable through YAML files, describe your Dashboard in a file, feed the program with it and voilà, you have a new dashboards
- support multiple dashboards, each dashboard can obviously show several graphs
- support alert buttons (they turn red when everything is on fire !)
- primitive labeling of graphs, the top corner can show a few cubic letters to remind you what this item is
- no dirty artefacts left after you're done with it, programs cleans up all the blocks it did put in the first place
- you can freely move around and play minecraft as you wish, only there are a few blocks dedicated to you total awareness of what's going on in your systems
- graphs are updated on-the-fly, continuously, several times per minute
- ...

Caveats:

- requires a dedicated Minecraft server, one hosted by you, and patched. This should not be a show stopper, but setting this up can be tricky
- yes, the genuine DataDog web UI is faster than this hack
- not production ready, no packaging, and lacks heavy testing

# Getting started

## Dependencies

* [Install PyMinecraft first](setup/README.md)
* You might be interested by reading https://www.nostarch.com/programwithminecraft
* Additionnally, this program uses `freetype-py` https://github.com/rougier/freetype-py which you can simply install by `pip install freetype-py`.
* Install the datadog python library https://github.com/DataDog/datadogpy
* You also need a DataDog account, along with an `APP_KEY` and an `API_KEY`. Refer to http://docs.datadoghq.com/api/ for details

## Run the program

Once you are ready, the `./demo.sh` shows an example of a possible launcher.

Basically:

```
python3 main.py <mydashboard.yml>
```

The program will expect elements such as the font to be in some precise path, so don't try to launch it from anywhere. For now.

## Tuning

Most of the configuration options are available in the YAML file.

Some environnment vars matter:

- `DATADOG_API_KEY`: the API key
- `DATADOG_APP_KEY`: the APP key
- `DATADOG_API_HOST`: the API host (eg: https://app.datadoghq.com/ )
- `DATADOG_DEMO_DATA`: if set to `True`, the program won't query DataDog API and display random demo data instead instead of read-world data

## Enjoy

![A typical screen capture](media/capture.jpg?raw=true "DogCraft screen capture")

# TODO

- make it more interactive, so that the "player" can act on the graph, acknowledge alerts...
- implement a cute white and purple Puppy that shows up with a dashboard hanging on his neck (killer feature!)
- ...
