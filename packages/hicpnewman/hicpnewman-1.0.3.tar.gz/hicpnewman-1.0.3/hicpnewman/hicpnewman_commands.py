from hicpnewman import config_manager, hicpnewman_helpers
import json
import os

def add(args, config):
    print(f"HICPNEWMAN | ADD | {args.name}")
    if args.name in config.collections.keys():
        print(f"collection {args.name} already exist in the config")
        return 2

    if args.collection_file_path:
        collection = config_manager.ContextJson(status=hicpnewman_helpers.get_file_name(args.collection_file_path), content=hicpnewman_helpers.json_file_path_to_dict(args.collection_file_path))
    else:
        collection = config.default.collection

    if args.environment_file_path:
        environment = config_manager.ContextJson(status=hicpnewman_helpers.get_file_name(args.environment_file_path), content=hicpnewman_helpers.json_file_path_to_dict(args.environment_file_path))
    else:
        environment = config.default.environment

    if args.globals_file_path:
        globals = config_manager.ContextJson(status=hicpnewman_helpers.get_file_name(args.globals_file_path), content=hicpnewman_helpers.json_file_path_to_dict(args.globals_file_path))
    else:
        globals = config.default.globals

    if args.data_file_path:
        data = config_manager.ContextCsv(status=hicpnewman_helpers.get_file_name(args.data_file_path), content=hicpnewman_helpers.csv_file_path_to_list_list_str(args.data_file_path))
    else:
        data = config.default.data


    config.collections[args.name] = config_manager.Collection(collection, environment, globals, data)

    config_manager.save_config(config)

    return 0

def remove(args, config):
    print(f"HICPNEWMAN | REMOVE | {args.name}")
    
    config.collections.pop(args.name)

    config_manager.save_config(config)

    return 0

def list(args, config):
    print(f"HICPNEWMAN | LIST")
    if args.serialize:
        print(json.dumps(config.to_dict(), indent=4))
    else:
        print(f"{len(config.collections)} loaded collections | {config.collections.keys()}")
        for name, col in config.collections.items():
            print(f"{name} | collection : {col.collection.status} | environment : {col.environment.status} | globals : {col.globals.status} | data : {col.data.status}")
    return 0

def export(args, config):
    print(f"HICPNEWMAN | EXPORT | {args.export_directory_path}")
    col = config.collections[args.name]
    if args.export_directory_path:
        hicpnewman_helpers.export_collection(col, args.name, args.export_directory_path)
    else:
        print(f"{args.name} | collection : {col.collection.status} | environment : {col.environment.status} | globals : {col.globals.status} | data : {col.data.status}")
        print("collection :")
        print(col.collection.content)
        print("environment :")
        print(col.environment.content)
        print("globals :")
        print(col.globals.content)
        print("data :")
        print(col.data.content)
        return 0

def load(args, config):
    print(f"HICPNEWMAN | LOAD | {args.new_config_file_path}")
    with open(args.new_config_file_path, "r") as file:
        data = json.load(file)
    new_config = config_manager.Config.from_dict(data)
    if args.do_backup:
        backup_path = hicpnewman_helpers.create_backup_path(args.new_config_file_path)
        print(f"creating backup of current config at {backup_path}")
        with open(backup_path, 'w') as backup_config_file:
            json.dump(config.to_dict(), backup_config_file, indent=4)
    if args.overwrite:
        print("overwriting old config")
        config_manager.save_config(new_config)
    else:
        print("add the flag --overwrite if you wish to overwrite the current configuration")
    return 0

def save(args, config):
    print(f"HICPNEWMAN | SAVE | {args.save_path}")
    with open(args.save_path, 'w') as save_file:
            json.dump(config.to_dict(), save_file, indent=4)
    return 0

def run(args, config, collection_name, format_config):
    print(f"HICPNEWMAN | RUN | {collection_name}")
    col = config.collections[collection_name]

    col_fp = hicpnewman_helpers.dict_to_json_temp_file_path(col.collection.content)
    env_fp = hicpnewman_helpers.dict_to_json_temp_file_path(col.environment.content)
    glo_fp = hicpnewman_helpers.dict_to_json_temp_file_path(col.globals.content)
    newman_command = f"{config.newman.command} run '{col_fp}' --environment {env_fp} --globals {glo_fp} --env-var \"url=http://{args.server}:{args.port}/hicp/rs\""

    if col.data.content:
        data_fp = hicpnewman_helpers.list_list_str_to_csv_temp_file_path(col.data.content)
        newman_command += f" --iteration-data '{data_fp}'"

    for flag in config.newman.flags:
        if flag.active:
            command = flag.command.format(**format_config)
            print(f"adding flag {command}")
            newman_command += " " + command

    
    reporters_command = " --reporters cli"
    reporters_export_command = ""
    reporters_flags_command = ""
    for reporter in args.reporters:

        print(f"adding reporter {reporter}")
        reporters_command += f",{reporter}"

        export_path = config.newman.reporters[reporter].export_path.format(**format_config)
        print(f"setting reporter {reporter} export to {export_path}")
        reporters_export_command += f" --reporter-{reporter}-export {export_path}"

        for flag in config.newman.reporters[reporter].flags:
            if flag.active:
                command = flag.command.format(**format_config)
                print(f"adding flag {command}")
                reporters_flags_command += " " + command

    if args.use_allure:
        reporters_command += f",allure"
        reporters_export_command += f" --reporter-allure-export {config.newman.reporters['allure'].export_path.format(**format_config)}"
        for flag in config.newman.reporters['allure'].flags:
            if flag.active:
                command = flag.command.format(**format_config)
                print(f"adding flag {command}")
                reporters_flags_command += " " + command

    newman_command += reporters_command + reporters_export_command + reporters_flags_command

    newman_result = hicpnewman_helpers.execute_command(newman_command)

    return 0

def merge(args, config, format_config):
    for reporter in [key for key in args.reporters if key not in ['csv', 'allure']]:
        print(f"merging reports from reporter {reporter}")

        export_path = config.newman.reporters[reporter].export_path.format(**format_config)[1:-1]
        print(f"export path for this reporter is {export_path}")

        merge_file_path = ("{dir}/merged/" + reporter + "/{timestamp}/merged_" + reporter + "_reports_{timestamp}.html").format(**format_config)
        os.makedirs(hicpnewman_helpers.get_path(merge_file_path))
        
        merge_command = f"cat {export_path} > {merge_file_path}"
        merge_result = hicpnewman_helpers.execute_command(merge_command)

    return 0

def allure(args, config, format_config):
    allure_export_path = config.newman.reporters['allure'].export_path.format(**format_config)

    allure_generate_command = f"npx allure generate {allure_export_path} --clean -o {allure_export_path}/allure-report"
    allure_generate_result = hicpnewman_helpers.execute_command(allure_generate_command)

    allure_open_command = f"npx allure open {allure_export_path}/allure-report &"
    allure_open_result = hicpnewman_helpers.execute_command(allure_open_command)

    return 0