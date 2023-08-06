
# use case example 
## Adding a collection
```bash
# Add a collection named my-collection with a postman collection file and csv data
user@server1 % hicpnewman add my-collection --collection /path/to/my/collection.postman.collection.json --data /path/to/my/data.csv
```
```bash
# You can run my-collection
user@server1 % hicpnewman run my-collection --server kmse-pcl5 --port 1111
```

## Run some/all collections
```bash
# Add a collection named my-collection
user@server1 % hicpnewman add my-collection --collection /path/to/my/collection.postman.collection.json
```
```bash
# Add a collection named my-collection2
user@server1 % hicpnewman add my-collection2 --collection /path/to/my/collection2.postman.collection.json
```
```bash
# You can run specific collections
user@server1 % hicpnewman run my-collection my-collection2 --server kmse-pcl5 --port 1111
```
```bash
# You can run all collections
user@server1 % hicpnewman run all --server kmse-pcl5 --port 1111
```

## Sharing a config file
```bash
# Save your current config file
user@server1 % hicpnewman save --filepath /path/to/my/config_save.json
```
```bash
# Load the saved config file (--backup to create a backup of your current config)
user@server2 % hicpnewman load /path/to/my/config_save.json --backup --overwrite 
```
```bash
# You can run my-collection that was imported within the new config
user@server2 % hicpnewman run my-collection --server kmse-pcl5 --port 1111
```

## Creating reports
```bash
# You can run my-collection with differents reporters
user@server1 % hicpnewman run my-collection --server kmse-pcl5 --port 1111 --reporters htmlextra html --directory ../results
```
```bash
# You can see your report results
user@server1 % ls -l ../results
```

## Allure webapp report
```bash
# You can run collections using allure, this is very usefull for multi collection runs
user@server1 % hicpnewman run all --server kmse-pcl5 --port 1111 --directory ../results --allure
```

## BETA Work In Progress : Merge reports
```bash
# You can run collections and merge the reports, this do not work very well
user@server1 % hicpnewman run all --server kmse-pcl5 --port 1111 --directory ../results --merge
```
  
# hicpnewman v0.4.0 commands
```bash  
hicpnewman [-d,--debug] {add,remove,list,export,load,save,run} ...  
```  
package for running newman collection  
  
* positional arguments:  
  * {add,remove,list,export,load,save,run}  
    * add                 *...adding a new collection configuration...*  
    * remove              *...removing a collection configuration...*  
    * list                *...listing collections configuration...*  
    * export              *...exporting a collection configuration...*  
    * load                *...load a new configuration (overwrite the existing one)...*  
    * save                *...save the current configuration...*  
    * run                 *...running a collection configuration...*  
  
* options:  
  * -h, --help            show this help message and exit  
  * -d, --debug           display debugging log  
  
## add command  
**adding a new collection configuration**
```bash   
hicpnewman add name \
  [-c,--collection COLLECTION_FILE_PATH] \
  [-g,--globals GLOBALS_FILE_PATH] \
  [-e,--environment ENVIRONMENT_FILE_PATH] \
  [-d,--data DATA_FILE_PATH]  
```  
* positional arguments:  
  * name                  name for the collection  
  
* options:  
  * -h, --help                              *show this help message and exit*  
  * -c, --collection COLLECTION_FILE_PATH   *postman collection json file path*  
  * -g, --globals GLOBALS_FILE_PATH         *postman globals json file path*  
  * -e, --environment ENVIRONMENT_FILE_PATH *postman environment json file path*  
  * -d, --data DATA_FILE_PATH                *data file path*  
  
## remove command  
**removing a collection configuration**
```bash   
hicpnewman remove name  
```  
* positional arguments:  
  * name *name of the collection*  
  
* options:  
  * -h, --help            *show this help message and exit*  
  
## list command  
**listing collections configuration**
```bash   
hicpnewman list \
  [-s,--serialize]  
```  
* options:  
  * -h, --help       *show this help message and exit*  
  * -s, --serialize  *serialize the current config file*  
  
## export command  
**exporting a collection configuration**
```bash   
hicpnewman export name \
  [-d,--directory EXPORT_DIRECTORY_PATH]   
```  
* positional arguments:  
  * name *name of the collectio*n  
  
* options:  
  * -h, --help            *show this help message and exit*  
  * -d, --directory EXPORT_DIRECTORY_PATH *directory export path*  
  
## load command  
**load a new configuration (overwrite the existing one)**
```bash   
hicpnewman load new_config_file_path \
  [-b,--backup] \
  [--overwrite]  
```  
* positional arguments:  
  * new_config_file_path  *new config file path*  
  
* options:  
  * -h, --help            *show this help message and exit*  
  * -b, --backup          *create a backup*  
  * --overwrite           *will overwrite the current config file*  
  
## save command  
**save the current configuration**
```bash   
hicpnewman save \
  -f,--filepath SAVE_PATH  
```  
* options:  
  * -h, --help            *show this help message and exit*  
  * -f, --filepath SAVE_PATH *save file path*  
  
## run command 
**running a collection configuration**   
```bash   
hicpnewman run [**names_of_loaded_collections,all] \
  -s,--server {kmse-pcl5,babylonia.local} \
  -p,-port PORT \
  -d,--directory RESULT_DIRECTORY_PATH \
  [-r,--reporters [html,csv,htmlfull,htmlextra]] \
  [--allure] \
  [--merge]    
```  
* positional arguments:    
  * {names_of_loaded_collections,all} *name of the collection*    
  
* options:    
  * -h, --help            *show this help message and exit*    
  * -s, --server {kmse-pcl5,babylonia.local} *server on which to run the collection*    
  * -p, --port PORT *port on which to run the collection*  
  * -r, --reporters [html,csv,htmlfull,htmlextra] *reporters used for the collection run*  
  * -d, --directory RESULT_DIRECTORY_PATH *directory export path*  
  * --allure              *will generate an allure interface*  
  * --merge               *[WIP] will merge all resulting reports*

# hicpnewman dev toolkit

## files
* newman-runner-package
  * hicpnewman
    * config
      * ...
    * templates
      * ...
    * \_\_init__.py
    * config_manager.py
    * hicpnewman_argparser.py
    * hicpnewman_commands.py
    * hicpnewman_helpers.py
  * DESCRIPTION.txt
  * LICENSE.txt
  * README.md
  * setup.py

**setup.py** : describe the package : what is exported, package version, entrypoints  

**config_manager.py** : describe the config dataclass, imports and exports  

**hicpnewman_argparser.py** : entrypoint with commands/subcommands/params/flags  

**hicpnewman_commands.py** : implementation of the commands  

**hicpnewman_helpers.py** : helper functions  

**config/*** : default configs  

**templates/*** : templates for reporters

## config
The config possess 3 main elements :
```json
{
  "collections": {},
  "newman": {},
  "default": {}
}
```
### collections: {}
Here are stored the collections to run. Each collection is composed of the postman collection, the environment, the globals and the iteration-data. If you do not specify all the elements, default: {} will fill the rest.
```json
{
  "collections": {
    "tarification_vitivolume": { #collection name
            "collection": { # postman collection
                "status": "tarification-vitivolume.postman_collection.json",
                "content": {...} #json of the postman collection
            },
            "environment": { # postman environment
                "status": "default",
                "content": {...} # json of the postman environment
            },
            "globals": { # postman globals
                "status": "default",
                "content": {...} # json of the postman globals
            },
            "data": { # postman-ready csv file
                "status": "tarification-vitivolume.csv",
                "content": [[...]] # cells of the csv file
            }
        },
  },
  "newman": {},
  "default": {}
}
```

### newman: {}
Here is the newman configuration and its reporters. These will affect the command executed to run newman.
```json
{
  "collections": {},
  "newman": {
    "command": "newman", #command of newman (a path can be specified if newman if installed locally)
    "flags": [ # newman flags
      {
        "active": true,
        "command": "--color auto"
      },
      {
        "active": false,
        "command": "--verbose"
      }
    ],
    "reporters": { # reporters allowed to be used
      "html": { # simple html reporter
        "package": "newman-reporter-html", # name of the package
        "export_path": "'{dir}/{collection_name}/{timestamp}/{collection_name}_html_{timestamp}.html'", # report export path
        "flags": [ # reporter flags
          {
            "active": true,
            "command": "--reporter-html-template '{hicpnewman_dir}/templates/original/template-default-colored.hbs'"
          }
        ]
      },
      "allure": { # webapp reporter (perfect for multiple collection runs)
        "package": "newman-reporter-allure",
        "export_path": "'{dir}/allure_aggregate/{timestamp}/'",
        "flags": [
          {
            "active": true,
            "command": "--reporter-allure-collection-as-parent-suite"
          }
        ]
      },
      "htmlextra": { # beautifull html reporter
        "package": "newman-reporter-htmlextra",
        "export_path": "'{dir}/{collection_name}/{timestamp}/{collection_name}_htmlextra_{timestamp}.html'",
        "flags": [
          {
            "active": true,
            "command": "--reporter-htmlextra-title '{collection_name} report [{timestamp}]'"
          }
        ]
      },
      "csv": {...}, # simple csv reporter
      "htmlfull": {...} # custom html reporter
    }
  },
  "default": {}
}
```

### default: {}
Here are stored the default collections element is they are not specified at the creation of a collection.
```json
{
  "collections": {},
  "newman": {},
  "default": {
    "collection": { # default postman collection
      "status": "default",
      "content": {...} #json of the default postman collection
    },
    "environment": { # default postman environment
      "status": "default",
      "content": {...} # json of the default postman environment
    },
    "globals": { # default postman globals
      "status": "default",
      "content": {...} # json of the default postman globals
    },
    "data": { # empty postman-ready csv file
      "status": "empty",
      "content": null
    }
  }
}
```

## reporters
[newman-reporter-html](https://www.npmjs.com/package/newman-reporter-html) : simple reporter, can be improved with templates   
[newman-reporter-htmlfull](https://www.npmjs.com/package/newman-reporter-htmlfull) : html with templates  
[newman-reporter-htmlextra](https://www.npmjs.com/package/newman-reporter-htmlextra) : beautifull html reports  
[newman-reporter-csv](https://www.npmjs.com/package/newman-reporter-csv) : simplest reporter, can be easier to process automatically   
[newman-reporter-allure](https://www.npmjs.com/package/newman-reporter-allure) : webapp reporter, perfect for multi collection runs  

  
## improving/fixing hicpnewman  
1. Change the hicpnewman version in setup.py
1. In the folder where setup.py is located
    ```bash
    python -m build
    ```
1. Local install 
    ```bash
    pip install dist/hicpnewman-**hicpnewman_version**.tar.gz
    ```
1. Reload terminal
    ```bash
    source ~/.zshrc
    ```    
1. Use hicpnewman
   ```bash
    hicpnewman --help
    ```

## Publishing / Installing
If everything is working well, you can publish a new version to pypi or pypitest :
* test build
  * publish : 
    ```bash 
    twine upload -r pypitest dist/*
    ```
  * install :
    ```bash 
    pip install -i https://test.pypi.org/simple/ hicpnewman  
    ```
* official build
  * publish : 
    ```bash 
    twine upload dist/*
    ```
  * install :
    ```bash 
    pip install hicpnewman  
    ```