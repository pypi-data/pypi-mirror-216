import sys
import os
import json

from file_handler import FileManager, build_file_path
from args_manager import is_valid_args, get_argument_type
from diff_handler import OASDiffAnalyser, scan_all_paths, _summary
from utils import get_diff_mapping, get_src_tar_file_relative

def analyse(arg1, arg2):
    if is_valid_args(arg1, arg2):
        arg_type =get_argument_type(arg1)
        if arg_type == "Regular file":
            print(f"Processing {arg1} {arg2}, TYPE: {arg_type}")
            src_files, tar_files = [arg1],[arg2]     
            summary = _summary(src_files, tar_files)
            summary["arg1"] = summary['source_system'] = arg1
            summary["arg2"] = summary['target_system'] = arg2
            summary["fs_type"] = "OAS JSON File"
            return summary
        elif arg_type == "Zip file":
            print(f"Processing {arg1} {arg2}, TYPE: {arg_type}")
        elif arg_type == "Folder":
            print(f"Processing {arg1} {arg2}, TYPE: {arg_type}")  
            src_files, tar_files = get_src_tar_file_relative(arg1, arg2)      
            summary = _summary(src_files, tar_files)
            summary["arg1"] = summary['source_system'] = arg1
            summary["arg2"] = summary['target_system'] = arg2
            summary["fs_type"] = "Folder"
            return summary
        else:
            print(f"Unknown argument passed of type {arg_type}")
    else:
        print("Invalid arguments")


def render_template(summary):
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))))
    template = env.get_template('report_v3.html')
    rendered_template = template.render(summary)
    output_file_path = 'summary.html'
    with open(output_file_path, 'w') as file:
        file.write(rendered_template)
    print(f"Template rendered and saved to '{output_file_path}'.")

def generate_cli_report(summary):
    file_path = "summary.txt"

    with open(file_path, "w") as file:
        text = f"""Imperva API Security OAS file diff tool Version 0.1.
            Source FS type: {summary.get('fs_type')} (S): ./{summary.get('arg1')}
            Target FS type: {summary.get('fs_type')} (T): ./{summary.get('arg2')}
            Legend:
            + Present in target file and missing in source file
            - Missing in target file and present in source file
            ~ Similar in both target and source file but with minor differences \n"""
        text += f"\n Total {summary.get('count_src_files')} {summary.get('source_system')} files scanned\n"
        text += f"\n Total {summary.get('count_tar_files')} {summary.get('target_system')} files scanned\n"
        text += f"\n {summary.get('count_api_src_files')} APIs found at {summary.get('source_system')} \n"
        text += f"\n {summary.get('count_api_tar_files')} APIs found at {summary.get('target_system')} \n"
        text += f"\n {len(summary.get('diff_paths_methods'))} APIs path with mismatching methods \n"
        text += f"\n {len(summary.get('mismatch_param_list'))} APIs with mismatching parameters \n"

        text += "\n Whats's New?\n"
        text += f"\n{summary.get('count_whats_new')} APIs not found in {summary.get('target_system')} \n"
        for path in summary.get('whats_new'):
            text +=f"\n - {path}"
        text += "\n"
        text += "\n Whats's Missing?\n"
        text += f"\n{summary.get('count_whats_missing')} APIs not found in {summary.get('source_system')} \n"

        for path in summary.get('whats_missing'):
            text +=f"\n + {path}"
        text += "\n"
        text += "\n Whats's Changed?\n"
   
        for new in summary.get('diff_paths_methods'):
            text +=f"\n ~ {new[3][0]}: {new[2]} -> PRESENT in {new[0]} NOT PRESENT in {new[1]}"
        text += "\n\n"
        for new in summary.get('mismatch_param_list'):
            text +=f"\n ~ {new[1]} parameters mismatch between both systems for the API: {new[0]}" 
            for key, value in summary.get('src_methods_metadata_dict').get(new[0]).get('data_types').items():
                text +=f"\n \t(S) { value[0] } { key }"
                text +=f"\n { value[1:] }"
            text += "\n"
            for key, value in summary.get('tar_methods_metadata_dict').get(new[0]).get('data_types').items():
                text +=f"\n \t(T) { value[0] } { key }"
                text +=f"\n { value[1:] }"
            text += "\n\n"
        text += "\n"
        file.write(text)
        print(f"Summary file saved to '{file_path}'.")


def main():
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]  
    summary = analyse(arg1, arg2)
    render_template(summary)
    generate_cli_report(summary)

if __name__ == "__main__":
    main()