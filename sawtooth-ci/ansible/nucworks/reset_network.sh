cd /home/fabric/sawtooth-ci/ansible/nucworks
ansible-playbook --extra-vars "@./configs/lrIndia.yaml" --inventory-file hosts.yaml stop_sawtooth.yaml
ansible-playbook --extra-vars "@./configs/lrIndia.yaml" --inventory-file hosts.yaml reset_sawtooth.yaml 
ansible-playbook --extra-vars "@./configs/lrIndia.yaml" --inventory-file hosts.yaml reboot_hosts.yaml
ansible-playbook --extra-vars "@./configs/lrIndia.yaml" --inventory-file hosts.yaml ping_check.yaml 
sleep 30
ansible-playbook --extra-vars "@./configs/lrIndia.yaml" --inventory-file hosts.yaml start_sawtooth_sim.yaml


