Vagrant.configure("2") do |config|

  # Configurazione VMware Fusion (Apple Silicon / Intel Mac)
  config.vm.provider "vmware_desktop" do |v|
    v.gui = false     # Disabilita l'interfaccia grafica
    v.allowlist_verified = true
    v.vmx["memsize"] = "4096"  # 4GB di RAM
    v.vmx["numvcpus"] = "2"    # 2 CPU
  end

  # Selezione automatica Box
  if RUBY_PLATFORM =~ /arm64/ || RUBY_PLATFORM =~ /aarch64/
    config.vm.box = "bento/rockylinux-9-arm64"
  else
    config.vm.box = "bento/rockylinux-9"
  end

  config.vm.synced_folder ".", "/vagrant"

  config.vm.define "macchina" do |macchina|
    macchina.vm.hostname = "macchina"
  end

  # Porte (Aggiornate per evitare conflitti su Mac)
  config.vm.network "forwarded_port", guest: 8080, host: 8081
  config.vm.network "forwarded_port", guest: 50000, host: 50001

  # --- FIX IMPORTANTE QUI SOTTO ---
  config.vm.provision "shell", inline: <<-SHELL
    # 1. Installa Ansible e Pip
    dnf install -y epel-release
    dnf install -y ansible-core python3-pip
    
    # 2. Installa la collezione Docker in un percorso GLOBALE
    # L'opzione -p /usr/share/ansible/collections rende la collezione visibile a tutti gli utenti
    mkdir -p /usr/share/ansible/collections
    ansible-galaxy collection install community.docker -p /usr/share/ansible/collections
  SHELL

  # Esecuzione Playbook
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.verbose = true
    ansible.install_mode = "none"
  end
end