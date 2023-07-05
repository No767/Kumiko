# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "kumiko_dev"
  config.vm.box = "generic/ubuntu2204"
  config.vm.synced_folder ".", "/home/vagrant/Kumiko", create: true
  config.vm.network "private_network", ip: "192.168.40.0/21"
  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = "playbook.yml"
    ansible.ask_become_pass = true
  end

end