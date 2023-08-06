import argparse
import convomerge.script


def cli():
    parser = argparse.ArgumentParser(
        prog='ConvoMerge',
        description='Allows to merge multiptle linear conversation files into single conversation tree'
    )
    parser.add_argument('inputs', nargs='+', help='Path(s) to input .txt or .yml linear conversation files')
    parser.add_argument('-o', '--output', help='Path to output .yml to store the result', required=True)
    parser.add_argument('-n', '--convo-name')
    parser.add_argument('-d', '--convo-description')
    parser.add_argument('-a', '--base-author', default='teacher')
    args = parser.parse_args()
    
    script_files = args.inputs
    output_file = args.output
    convo_name = args.convo_name
    convo_description = args.convo_description
    base_author = args.base_author

    base_script = None

    for script_file in script_files:
        script = convomerge.script.read_file(script_file, convo_name=convo_name, convo_description=convo_description, base_author=base_author)
        
        if base_script is None:
            base_script = script
        else:
            base_script = base_script.merge_script(script)
        
    base_script.to_yaml(output_file)
