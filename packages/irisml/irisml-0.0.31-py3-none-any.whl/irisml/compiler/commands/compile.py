import argparse
import json
import pathlib
import re
from irisml.compiler import Compiler


def main():
    class KeyValuePairAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            k, v = values.split('=', 1)
            d = getattr(namespace, self.dest)
            d[k] = v

    parser = argparse.ArgumentParser()
    parser.add_argument('input_filepath', type=pathlib.Path)
    parser.add_argument('--output_filepath', '-o', type=pathlib.Path, required=True)
    parser.add_argument('-I', action='append', dest='include_paths', default=[])
    parser.add_argument('--build-arg', '-b', action=KeyValuePairAction, dest='build_args', default={})

    args = parser.parse_args()

    for key, value in args.build_args.items():
        if not re.match(r'^[a-z][a-z0-9_]*$', key):
            parser.error(f"Invalid build arg name: {key}. Must be a valid python variable name.")

    compiler = Compiler()
    job_description = compiler.compile(args.input_filepath, args.include_paths, args.build_args)
    args.output_filepath.parent.mkdir(parents=True, exist_ok=True)
    args.output_filepath.write_text(json.dumps(job_description.to_dict(), indent=4) + '\n')


if __name__ == '__main__':
    main()
