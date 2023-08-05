"""Configuration-related utilities"""
#%%
import os
import pathlib
# import glob
import configparser
# from dotenv import dotenv_values
import json
# import yaml
import re
# import io

#%%

def process_env_file(env_values):
    def parse_single_line(line):
        delimiters = [';', ',', '.', '|', ' ', '\t']
        pairs = [pair.strip() for pair in re.split('|'.join(map(re.escape, delimiters)), line) if pair.strip()]
        valid_pairs = []
        for pair in pairs:
            pair = pair.replace('"', '').replace("'", "")
            if "=" in pair or ":" in pair:
                valid_pairs.append(pair.split("=", 1) if "=" in pair else pair.split(":", 1))
        return valid_pairs
    
    def parse_multi_lines(lines):
        key_value_pairs = []
        for line in lines:
            if '=' in line or ':' in line:
                matches = re.findall(r'(?:"([^"]+)")|(?:([^=:]+)[=:](.+))', line)
                pairs = [pair[0] if pair[0] else f"{pair[1]}={pair[2]}" for pair in matches]
                for pair in pairs:
                    key_value = pair.split('=', 1)
                    if len(key_value) == 2:
                        key = key_value[0].strip()
                        value = key_value[1].strip()
                        key_value_pairs.append((key, value))
        return key_value_pairs

    # if os.path.exists(env_values):
    #     # If the input is a file path
    #     try:
    #         with open(env_values) as file:
    #             env_vars = {}
    #             for line in file:
    #                 line = line.strip()
    #                 if line and not line.startswith("#"):
    #                     key, value = line.split("=", 1)
    #                     env_vars[key.strip()] = value.strip()
    #     except Exception as e:
    #         return f"Invalid environment file: {env_values}. Reason: {str(e)}"
    if isinstance(env_values, str):
        if os.path.exists(env_values):
            try:
                with open(env_values) as file:
                    env_vars = {}
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            key, value = line.split("=", 1)
                            env_vars[key.strip()] = value.strip()
            except Exception as e:
                return f"Invalid environment file: {env_values}. Reason: {str(e)}"
        else:
            try:
                # Attempt JSON parsing first
                env_vars = json.loads(env_values)
            except Exception as e:
                # try:
                #     # Attempt YAML parsing next
                #     env_vars = yaml.safe_load(env_values)
                # except Exception as e:
                #     # If JSON and YAML parsing fail, perform custom string parsing
                lines = env_values.splitlines()
                if len(lines) == 1:
                    if any(char in env_values for char in ('/', '\\')):
                        return f'Invalid filepath provided: {env_values}'
                    # Single line with possible delimiters
                    key_value_pairs = parse_single_line(env_values)
                else:
                    # Multiple lines, treat each line as a separate key-value pair
                    key_value_pairs = parse_multi_lines(lines)

                env_vars = {}
                for pair in key_value_pairs:
                    key, value = pair
                    env_vars[key.strip()] = value.strip()
    elif isinstance(env_values, dict):
        env_vars = env_values
    else:
        return 'Invalid argument provided. Must be a string, dictionary, or valid file path'

    if not env_vars:
        # print(f'No valid key-value pairs could be identified in the argument: {env_values}')
        return f'No valid key-value pairs could be identified in the argument: {env_values}'
    
    set_keys = []
    failed_set_keys = []

    for key, value in env_vars.items():
        try:
            os.environ[key] = value
            set_keys.append(key)
            # print(f'key: {key}, value: {value}')
        except Exception as e:
            failed_set_keys.append(key)

    if set_keys:
        set_keys_print_str = "\n".join(set_keys)
        print_str = f"Environment variables set successfully:\n{set_keys_print_str}"
        if failed_set_keys:
            failed_set_keys_print_str = "\n".join(failed_set_keys)
            print_str += f'\nHowever, the following keys could not be set:\n{failed_set_keys_print_str}'
        print(print_str)

        set_keys_return_str = ", ".join(set_keys)
        return_str = f"Environment variables set successfully: {set_keys_return_str}"
        if failed_set_keys:
            failed_set_keys_return_str = ", ".join(failed_set_keys)
            return_str += f'; However, the following keys could not be set: {failed_set_keys_return_str}'
        return return_str
    else:
        return "No environment variables were set"

def read_config_file(config_filepath):
    """Read config .ini file at provided location, using '_local' version instead if found"""
    if isinstance(config_filepath, str):
        config_filepath = pathlib.Path(config_filepath)
    config = configparser.ConfigParser()
    break_out_flag = False
    # Locate local config file
    local_config_path = ''
    for root, dirs, files in os.walk(config_filepath.parent):
        if break_out_flag == True:
            break
        files = [file for file in files if file.endswith(('.ini'))]
        for file in files:
            if break_out_flag == True:
                break
            if file == config_filepath.stem + '_local.ini':
                # local_config_path = os.path.join(root, file)
                local_config_path = pathlib.Path(root) / file
                break_out_flag = True
                break
    config.read([config_filepath, local_config_path])#, encoding='utf-8-sig')
    return config

# %%

if __name__ == '__main__':
    
    # Test case: Non-existent file path
    # process_env_file('path/to/invalid_env_file.env')
    
    # process_env_file(r'C:\Data Projects\Development\projects\flat_file_loader\docker\local\docker.env')

    # process_env_file('key1=value1,key2=value2')

    # process_env_file('key1:value1,key2:value2')

    # process_env_file('key1,value1;key2|value2')

    # process_env_file('key1,value1;key2=value2')

    # process_env_file('key1=value1 key2=value2 key3=value3')

    # process_env_file('"key1"="value1" "key2"="value2" "key3"="value3"')

    # process_env_file('key1:value1   key2:value2 key3:value3')

    # process_env_file('key1,value1;key2|value2 key3:value3')

    # process_env_file('key1=value1\nkey2=value2\nkey3=value3')

    # process_env_file('key1:value1\nkey2:value2\nkey3:value3')

    # process_env_file('key1,value1;key2|value2\nkey3:value3')

    process_env_file('{"key1": "value1", "key2": "value2"}')

    env_dict = {'key1': 'value1', 'key2': 'value2'}
    process_env_file(env_dict)

    # Test case: Invalid input type
    process_env_file(123)

    #%%
