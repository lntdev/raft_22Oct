cd /home/fabric/sawtooth-ci/ansible/nucworks
ansible-playbook --extra-vars "@./configs/lrIndia.yaml" --inventory-file hosts.yaml start_sawtooth_sim.yaml

