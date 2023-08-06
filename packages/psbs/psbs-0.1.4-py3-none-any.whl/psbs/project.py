from os import path
from shutil import rmtree

from .gister import Gister
from .config import Config
from .psparser import split_ps, get_engine
from .templatebuilder import make_template
from .utils import read_file, write_file, write_yaml, make_dir, run_in_browser
from .template import render_template
from .extension import Extension


class PSBSProject:
    def __init__(self, config_filename="config.yaml"):
        self.config = Config(config_filename)

    def build(self):
        # Check for target directory
        if not path.exists("bin"):
            print("bin directory does not exist, creating one")
            make_dir("bin")

        readme_path = path.join("bin", "readme.txt")
        script_path = path.join("bin", "script.txt")

        # Build the readme.txt
        print(f"Writing file {readme_path}")
        write_file(
            readme_path,
            "Play this game by pasting the script in "
            f"{self.config['engine']}editor.html",
        )

        # Build the script.txt
        print("Building script.txt")
        source = render_template(
            path.join("src", self.config["template"]), self.config
        )

        print(f"Writing file {script_path}")
        write_file(script_path, source)

    def upload(self):
        gist_id = self.config["gist_id"]
        if not self.config["gist_id"]:
            print("Error: Unable to upload without a gist_id in config file")
            raise SystemExit(1)

        print("Updating gist")
        gist = Gister(gist_id=gist_id)
        gist.write(path.join("bin", "readme.txt"))
        gist.write(path.join("bin", "script.txt"))

    def run(self, editor=False):
        print("Opening in browser")
        url = self.config["engine"]
        if editor:
            url += "editor.html?hack="
        else:
            url += "play.html?p="
        url += self.config["gist_id"]
        run_in_browser(url)

    @staticmethod
    def create(project_name, gist_id=None, file=None, new_gist=False):
        source = ""
        engine = "https://www.puzzlescript.net/"

        if gist_id:
            print("Downloading data from gist")
            gist = Gister(gist_id=gist_id)
            source = gist.read("script.txt")
            engine = get_engine(gist.read("readme.txt"))
        elif file:
            source = read_file(file)
        else:
            source = read_file(
                path.join(path.realpath(path.dirname(__file__)), "example.txt")
            )

        src_tree = split_ps(source)

        if new_gist:
            print("Creating new gist")
            gist = Gister()
            gist_id = gist.create(name=project_name)

        config_dict = {
            "gist_id": gist_id,
            "engine": engine,
            "template": "main.pss",
        }

        for extension in Extension.get_extensions():
            if extension.get_config():
                config_dict[extension.__name__] = extension.get_config()

        print("Building directory structure")
        make_dir(project_name)
        try:
            make_dir(path.join(project_name, "src"))
            make_dir(path.join(project_name, "bin"))

            print("Creating config file")
            write_yaml(path.join(project_name, "config.yaml"), config_dict)

            print("Creating template file")
            write_file(
                path.join(project_name, "src", "main.pss"),
                make_template(src_tree),
            )

            print("Creating source files")
            for section_name, src_blocks in src_tree.items():
                for index, src_content in enumerate(src_blocks):
                    index += 1
                    if len(src_blocks) == 1:
                        index = ""
                    src_filename = f"{section_name}{index}.pss"
                    write_file(
                        path.join(project_name, "src", src_filename),
                        src_content,
                    )
        except SystemExit as err:
            print("Cleaning up!")
            rmtree(project_name)
            raise SystemExit(1) from err
