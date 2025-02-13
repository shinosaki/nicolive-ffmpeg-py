from pathlib import Path
import argparse
import utils
from ws import NicoLiveWS

def main(output_path: Path):
    if output_path.exists():
        raise ValueError('Exists output path', output_path)

    program_id = utils.extract_program_id(str(args.output))
    if not program_id:
        raise ValueError('program id is not contain of argument')

    try:
        NicoLiveWS(program_id, output_path)
    except ValueError as e:
        print(e)
        exit(1)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('output', type=Path)
    args, _ = p.parse_known_args()
    main(args.output)
