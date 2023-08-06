import os, sys
import collections.abc
import shutil
import copy
import docker
import json
import tempfile
import uuid
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper



def dictionary_update( d, u ):
    for k, v in u.items():
        if isinstance( v, collections.abc.Mapping ):
            d[k] = dictionary_update( d.get(k, {}), v )
        else:
            d[k] = v
    return d



def prep_directory(dependencies):
    # create a filepath that does not already exist
    root_directory = os.path.join( tempfile.gettempdir(),f"ow-ci-helper-{str(uuid.uuid4())}" )
    while os.path.exists(root_directory):
        # check if rootdir exists, and if so, try again
        root_directory = os.path.join( tempfile.gettempdir(),  str(uuid.uuid4()) )

    # make a directory at the filepath
    os.mkdir(root_directory)

    # volume mounts maps from dependancy to the directory corresponding to that dependancy
    volume_mounts = {}
    for dependency in dependencies:
        # creates a directory at a file path off of root_directory, named after the dependancy
        dependency_dir = os.path.join( root_directory, dependency )
        os.mkdir(dependency_dir)
        if dependency in 'model-registry':
            # if the dependancy is a model-registry, add a sub-directory for models
            os.makedirs( os.path.join(dependency_dir, 'data-dir', 'models'), exist_ok=True)
        elif dependency in 'input-server':
            os.makedirs( os.path.join(dependency_dir, 'data-dir', 'inputs'), exist_ok=True)
            
        volume_mounts[dependency] = dependency_dir

    return root_directory, volume_mounts

def pull_image( client, image ):
    repo_name, tag = image.split(":")
    client.images.pull( repo_name, tag=tag )
    return

def make_mount_list(dependency, config, root_volume_directory):
    mounts = []
    config = copy.deepcopy(config)
    config.pop('docker')

    volume_path = os.path.join( root_volume_directory, dependency, 'config.yaml' )
    with open(volume_path, 'w') as f:
        f.write( yaml.dump(config, Dumper=Dumper) )

    mount_path = '/app/config.yaml'

    if dependency in ['input-server', 'overwatch-server' ]:
        # the directory on the host machine which will be mapped to a directory in the docker container
        host_dir = None

        if 'INPUT_SERVER_DATA_DIR' in os.environ:
            # if a bash variable has been set, use it for the data dir
            host_dir = os.environ['INPUT_SERVER_DATA_DIR']
        else:
            # if no data dir is set, use the temp dir
            host_dir = os.path.join( root_volume_directory, 'input-server', 'data-dir' )

        mounts.append(
            docker.types.Mount(
                '/data-dir',
                host_dir,
                type = 'bind'
            )
        )
    else:
        mounts.append(
            docker.types.Mount(
                '/data-dir',
                os.path.join( root_volume_directory, dependency, 'data-dir' ),
                type = 'bind'
            )
        )

    mounts.append(
        docker.types.Mount(mount_path, volume_path, read_only=True, type='bind')
    )

    return mounts

def cleanup(client, dependencies, config):
    all_containers = {}
    for container in client.containers.list(all=True):
        all_containers[container.name] = container

    for dependency in dependencies:
        if dependency in list(all_containers.keys()):
            print(f"Cleaning up {dependency}")
            container = all_containers[dependency]
            container.stop()
            container.wait()
            mounts = container.attrs['Mounts']
            for mount in mounts:
                if mount['Destination'] == '/root/.dcp':
                    continue
                if mount['Source'] == os.environ.get('INPUT_SERVER_DATA_DIR'):
                    # if the mount directory on the host machine is specified by CLI variable, do not delete it
                    continue
                if os.path.exists(mount['Source']) and os.path.isdir(mount['Source']):
                    shutil.rmtree(mount['Source'])
                elif os.path.exists(mount['Source']):
                    os.remove(mount['Source'])
            container.remove()
            print(f"Done cleaning up {dependency}")
    print("Finished cleaning up all dependencies")
    return


def satisfy_needs(client, dependencies, config, keystores):
    
    # check if the keystore exists
    assert os.path.exists(keystores), f"Given keystore path does not exist: {keystores}"

    # gets the running containers
    all_containers = {}
    for container in client.containers.list(all=True):
        all_containers[container.name] = container

    # creates temp directories for the containers to mount volumes on
    # root_volume_directory is the temp-dir that each of the dopendacy's volumes are contained within
    # volume_mounts is an object mapping from dependancy names to the dir within root_volume_directory for that specific dependancy
    root_volume_directory, volume_mounts = prep_directory(dependencies)

    for dependency in dependencies:
        # stops any running containers that are dependancies
        if dependency in list(all_containers.keys()):
            print(f"Stopping {dependency}")
            container = all_containers[dependency]
            container.stop()
            container.wait()
            container.remove()
            print(f"Stopped and removed {dependency}")

        # checks that the dependancy has a config
        assert dependency in config.keys(), f"No config entry for {dependency}"
        # gets the dependancy's config
        dependency_config = config[dependency]
        

        mounts = make_mount_list(
            dependency, 
            dependency_config, 
            root_volume_directory,
        )

        # if the dependancy is overwatchserver, mount a directory for the keystore
        if dependency in 'overwatch-server':
            mounts.append(
                docker.types.Mount(
                    '/root/.dcp',
                    keystores,
                    type='bind',
                    read_only=True,
                )
            )

        pull_image( client, dependency_config['docker']['image'] )
        
        container = client.containers.create(
            dependency_config['docker']['image'],
            mounts = mounts,
            network_mode = 'host',
        )
        container.rename(dependency)
        container.start()
    print(f"Finished deploying dependencies: {dependencies}")



# creates and caches a docker client
def setup_client():
    if hasattr(setup_client, "client"):
        return setup_client.client
    client = docker.from_env()
    pretty_client_info = json.dumps( client.version(), sort_keys=True, indent=2 )
    print(f"Connected to docker: \n{pretty_client_info}")
    setup_client.client = client
    return client


def _load_config(path):
    assert os.path.exists(path), f"Config provided does not exist: {path}"
    with open(path, 'r') as f:
        data = ''.join( f.readlines() )
    config = yaml.load(data, Loader=Loader)
    return config

def load_config(path):
    template_config = _load_config( os.path.join( os.path.dirname( __file__ ), 'template.config.yaml' ) )
    config = _load_config( path )

    out_config = copy.deepcopy( template_config )
    out_config = dictionary_update( out_config, config )

    return out_config



def write_config(path, data):
    with open(path, 'w') as f:
        f.write(
            yaml.dump( data, Dumper=Dumper )
        )
    return


def needs_cli(args = None):
    import argparse
    parser = argparse.ArgumentParser(description="A dependency satisfaction tool for overwatch using docker/python to simplify your CI setups!")
    parser.add_argument("dependencies", nargs="+", help="Dependencies to satisfy, must be any of 'overwatch-server', 'model-registry', 'input-server'")
    parser.add_argument("-c", "--config", type=str, help="Path to config.yaml for Overwatch CI Helper")
    parser.add_argument("--cleanup", action="store_true", help="Clean up all containers and remove from docker instance")
    parser.add_argument("--keystores", type=str, default="~/.dcp", help="Directory containing dcp keystores on host. Defaults to ~/.dcp")

    args = parser.parse_args(args)
    client = setup_client()
    config = load_config(args.config)

    print(json.dumps( config, sort_keys=True, indent=2 ))
    
    if args.cleanup:
        cleanup(client, args.dependencies, config)
    else:
        satisfy_needs(client, args.dependencies, config, os.path.expanduser(args.keystores))
