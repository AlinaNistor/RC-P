
SET vbm="C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"


REM Node 1 
%vbm% clonevm base --name node1 --snapshot base --options link --register
%vbm% modifyvm node1 --cableconnected2 off
%vbm% modifyvm node1 --cableconnected3 off
%vbm% modifyvm node1 --nic2 intnet --intnet2 neta
%vbm% modifyvm node1 --cableconnected2 on
%vbm% modifyvm node1 --natpf1 delete ssh
%vbm% modifyvm node1 --natpf1 ssh,tcp,,2201,,22

REM Node 2 
%vbm% clonevm base --name node2 --snapshot base --options link --register
%vbm% modifyvm node2 --cableconnected2 off
%vbm% modifyvm node2 --cableconnected3 off
%vbm% modifyvm node2 --nic2 intnet --intnet2 neta
%vbm% modifyvm node2 --cableconnected2 on
%vbm% modifyvm node2 --natpf1 delete ssh
%vbm% modifyvm node2 --natpf1 ssh,tcp,,2202,,22

REM Node 3 
%vbm% clonevm base --name node3 --snapshot base --options link --register
%vbm% modifyvm node3 --cableconnected2 off
%vbm% modifyvm node3 --cableconnected3 off
%vbm% modifyvm node3 --nic2 intnet --intnet2 neta
%vbm% modifyvm node3 --nic3 intnet --intnet3 netb
%vbm% modifyvm node3 --cableconnected2 on
%vbm% modifyvm node3 --cableconnected3 on
%vbm% modifyvm node3 --natpf1 delete ssh
%vbm% modifyvm node3 --natpf1 ssh,tcp,,2203,,22

REM Node 4 
%vbm% clonevm base --name node4 --snapshot base --options link --register
%vbm% modifyvm node4 --cableconnected2 off
%vbm% modifyvm node4 --cableconnected3 off
%vbm% modifyvm node4 --nic2 intnet --intnet2 netb
%vbm% modifyvm node4 --cableconnected2 on
%vbm% modifyvm node4 --natpf1 delete ssh
%vbm% modifyvm node4 --natpf1 ssh,tcp,,2204,,22
