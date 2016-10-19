
# set the system folders of pycharm here
# if on ubuntu, a possible value is
pycharm_folders =  [
    "~/.PyCharm2016.1/system/tmp/",
    "~/.PyCharm2016.2/system/tmp/"
    ]

# set the default directory after ssh-ing into the virtual machine
default_dir_after_ssh = Dir.pwd
Vagrant.configure(2) do |config|

    config.vm.box = "phusion/ubuntu-14.04-amd64"
    config.vm.box_check_update = false

    config.vm.network "forwarded_port", guest: 2375, host: 2375
    config.vm.network "private_network", ip: "192.168.33.10"


    config.vm.synced_folder ".", "/vagrant", disabled: true 
    # this will sync the path of the current host folder
    # to a folder with the same path on the guest machine.
    # this is done to make PyCharm work
    config.vm.synced_folder ".", Dir.pwd,
        owner: 'vagrant',
        group: 'vagrant',
        mount_options: ["dmode=777", "fmode=777"]

    # this is done to enable pycharm connect to docker, when docker is in a vm.
    # synch pycharm's system folder 
    # to the same path on the virtual machine
    pycharm_folders.each do |pycharm_folder| 

        config.vm.synced_folder pycharm_folder, File.expand_path(pycharm_folder),
            owner: 'vagrant',
            group: 'vagrant',
            mount_options: ["dmode=777", "fmode=777"]
    end


    config.vm.provider "virtualbox" do |vb|
        vb.gui = false
        vb.memory = "1024"
    end


    # Provision the virtual machine
    provision_script_path = "#{Dir.pwd}/vagrant_setup.sh "

    provision_script = "chmod +x #{provision_script_path}; #{provision_script_path} #{default_dir_after_ssh}"
    config.vm.provision :shell, :inline => provision_script

    config.vm.provision "file", source: "~/.gitconfig", destination: "/home/vagrant/.gitconfig", run:"always"

end
