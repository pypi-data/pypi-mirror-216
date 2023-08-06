from hicpnewman import config_manager, hicpnewman_helpers, hicpnewman_commands
import argparse
import os


def main():
    config = config_manager.load_config()

    parser = argparse.ArgumentParser(prog ='hicpnewman',
                                     description ='package for running newman collection')
    
    parser.add_argument('-d', '--debug', action='store_true', help ='display debugging log')

    subparsers = parser.add_subparsers(dest="command", required=True)

    # add subcommand
    subcommand_add_parser = subparsers.add_parser("add", 
                                                    help="...adding a new collection configuration...")
    subcommand_add_parser.add_argument('name',
                                            type = str, 
                                            help ='name for the collection')

    subcommand_add_parser.add_argument('-c', '--collection',
                                            dest ='collection_file_path', 
                                            type=hicpnewman_helpers.collection_file_type,
                                            default=None, 
                                            help ='postman collection json file path')
    
    subcommand_add_parser.add_argument('-g', '--globals',
                                            dest ='globals_file_path', 
                                            type=hicpnewman_helpers.globals_file_type,
                                            default=None, 
                                            help ='postman globals json file path')
    
    subcommand_add_parser.add_argument('-e', '--environment',
                                            dest ='environment_file_path', 
                                            type=hicpnewman_helpers.environment_file_type,
                                            default=None, 
                                            help ='postman environment json file path')
    
    subcommand_add_parser.add_argument('-d', '--data',
                                            dest ='data_file_path', 
                                            type=hicpnewman_helpers.csv_file_type,
                                            default=None, 
                                            help ='data file path')
    
    # remove subcommand
    subcommand_remove_parser = subparsers.add_parser("remove", 
                                                    help="...removing a collection configuration...")
    subcommand_remove_parser.add_argument('name',
                                            type = str, 
                                            choices = config.collections.keys(),
                                            help ='name of the collection')
    
    # list subcommand
    subcommand_list_parser = subparsers.add_parser("list", 
                                                    help="...listing collections configuration...")
    subcommand_list_parser.add_argument('-s', '--serialize', 
                                            dest='serialize', 
                                            action='store_true', 
                                            help ='serialize the current config file')
    
    # export subcommand
    subcommand_export_parser = subparsers.add_parser("export", 
                                                    help="...exporting a collection configuration...")
    subcommand_export_parser.add_argument('name',
                                            type = str, 
                                            choices = config.collections.keys(),
                                            help ='name of the collection')
    subcommand_export_parser.add_argument('-d', '--directory',
                                            dest ='export_directory_path', 
                                            type=hicpnewman_helpers.directory_type,
                                            default=None, 
                                            help ='directory export path')
    
    # load subcommand
    subcommand_load_parser = subparsers.add_parser("load", 
                                                    help="...load a new configuration (overwrite the existing one)...")
    subcommand_load_parser.add_argument('new_config_file_path',
                                            type=hicpnewman_helpers.json_file_type,
                                            help ='new config file path')
    subcommand_load_parser.add_argument('-b', '--backup',
                                            dest='do_backup', 
                                            action='store_true', 
                                            help ='create a backup')
    subcommand_load_parser.add_argument('--overwrite', 
                                            dest='overwrite', 
                                            action='store_true', 
                                            help ='will overwrite the current config file')
    
    # save subcommand
    subcommand_save_parser = subparsers.add_parser("save", 
                                                    help="...save the current configuration...")
    subcommand_save_parser.add_argument('-f', '--filepath',
                                            dest ='save_path', 
                                            type=hicpnewman_helpers.file_type,
                                            required=True,
                                            help ='save file path')
    
    # run subcommand
    subcommand_run_parser = subparsers.add_parser("run", 
                                                    help="...running a collection configuration...")
    subcommand_run_parser.add_argument('names',
                                            type = str, 
                                            nargs= '*',
                                            choices = list(config.collections.keys()) + ['all'],
                                            help ='name of the collection')
    subcommand_run_parser.add_argument('-s', '--server',
                                            dest='server',
                                            type = str, 
                                            required=True,
                                            choices = ['kmse-pcl5', 'babylonia.local'],
                                            help ='server on which to run the collection')
    subcommand_run_parser.add_argument('-p', '--port',
                                            dest='port',
                                            type = int, 
                                            required=True,
                                            help ='port on which to run the collection')
    subcommand_run_parser.add_argument('-r', '--reporters',
                                            dest='reporters',
                                            type = str, 
                                            nargs= '*',
                                            choices= [key for key in config.newman.reporters.keys() if key != 'allure'],
                                            default= [],
                                            help ='reporters used for the collection run')
    subcommand_run_parser.add_argument('-d', '--directory',
                                            dest ='result_directory_path', 
                                            type=hicpnewman_helpers.directory_type,
                                            required=True,
                                            help ='directory export path')
    subcommand_run_parser.add_argument('--allure', 
                                            dest='use_allure', 
                                            action='store_true', 
                                            help ='will generate an allure interface')
    subcommand_run_parser.add_argument('--merge', 
                                            dest='do_merge', 
                                            action='store_true', 
                                            help ='[WIP] will merge all resulting reports')

  
    args = parser.parse_args()

    if args.command == "add":       hicpnewman_commands.add(args, config)
    elif args.command == "remove":  hicpnewman_commands.remove(args, config)
    elif args.command == "list":    hicpnewman_commands.list(args, config)
    elif args.command == "export":  hicpnewman_commands.export(args, config)
    elif args.command == "load":    hicpnewman_commands.load(args, config)
    elif args.command == "save":    hicpnewman_commands.save(args, config)
    elif args.command == "run":

        # format_config
        format_config = {
            "dir": args.result_directory_path,  
            "timestamp": hicpnewman_helpers.get_timestamp(), 
            "hicpnewman_dir":  os.path.dirname(__file__)
        }
        
        if 'all' in args.names:
            collections_to_run = config.collections.keys()
        else:
            collections_to_run = args.names

        for collection_name in collections_to_run:
            hicpnewman_commands.run(args, config, collection_name, {**format_config, **{"collection_name": collection_name}})

        if args.do_merge:
             hicpnewman_commands.merge(args, config, {**format_config, **{"collection_name": "*"}})

        if args.use_allure:
            hicpnewman_commands.allure(args, config, format_config)

