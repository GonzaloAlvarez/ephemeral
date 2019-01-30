#!/usr/bin/env python
#from ruamel.yaml import ryaml
import os
import __main__
import sys

class PackageManager(object):
    def __init__(self, context):
        cli = context.session.cli
        self.package_name = cli.package
        main_path = os.path.dirname(os.path.realpath(__main__.__file__))
        self.packages_path = os.path.join(main_path, 'packages')
        self.package_filename = os.path.join(self.packages_path, self.package_name + '.yaml')
        if os.path.isfile(self.package_filename):
            from jinja2 import Environment, FileSystemLoader
            import ruamel.yaml as ryaml
            env = Environment(loader = FileSystemLoader(self.packages_path), trim_blocks=True, lstrip_blocks=True)
            template = env.get_template(self.package_name + '.yaml')
            package_vars = {
                    'python': context.config.python_path,
                    'pip': context.config.pip_path,
                    'bin': os.path.join(context.epherstore.get_store_path(), 'bin'),
                    'args': context.session.cli.args if 'args' in context.session.cli else []
                    }
            self.package_obj = ryaml.safe_load(template.render(package_vars))


    def get_dependencies(self):
        if 'package_obj' in self.__dict__:
            return self.package_obj['package']['setup']['dependencies']
        return None

    def get_instructions(self):
        if 'package_obj' in self.__dict__:
            return self.package_obj['package']['run']['execution']
        return None

