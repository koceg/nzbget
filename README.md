### NzbGet Dockerfile

I have seen a lot of images for NzbGet that try to solve this problem but there is one thing I don't like about them, TRANSPARENCY and SIZE.

They all start from some wierd or self build image where you can't really see what is inside and hope for the best or they are too big to begin with. Even though 50-60 Mb is not too much in this day and age we can do it in less and that is the purpose of this repo with total build size ~20MB

### Prerequisite

- Docker CE on remote host
Optional:
	- python3 on working host
	- rsync on working host

### Installation 

Clone/Copy this repo on the machine where you intend to run NzbGet and from inside the repo issue the following command
```
docker build .
```
once done you should get a hash for your newly build image in the last line of our execution steps or just run
```
docker images
```
and note the first **IMAGE ID** hash value, then run
```
docker tag (IMAGE ID) nzbget:v21
```

### Container Start
**NOTE:** make sure that `/local/config/dir` **AND** `/local/media/dir` exist first    
*(these here are only placeholders and should be real paths )*
then copy `nzbget.conf` to `/local/config/dir` *(again placeholder should be real path)* and run 
```
docker create --name NzbGet -p 6789:6789 -e PUID=1000 -e PGID=1000 -e TZ=Europe/Berlin --restart=always -v (/local/config/dir):/config -v (/local/media/dir):/downloads nzbget:v21
```
```
docker start NzbGet
```
**NOTE:** our newly created NzbGet container is *always running* and will auto start when we bootup our machine. If for some reason the container need to be stopped run:
```
docker stop NzbGet
```

### Post installation
At this point our newly created container should be running and reachable on the IP of our host, to make sure everithing is working run:
```
docker ps 
```
we should get our container data. If we don't get any data it means that our container is not runnning and we should check what might be the problem by running:
```
docker logs NzbGet
```

Problem might be missing `nzbget.conf` file, the paths that our container is using are non existent or with the wrong **user:group** permissins

### Configuration
Now inspect `nzbget.conf` file to get yourself familiar with the variables and replace **CHANGE ME** values with real values to make it work.
This can also be done through the web gui.
There are two defined categories that give sudgestion how things can be organised and should be changed or expanded by desire.

### Extra automation step

Now with this setup and the way NzbGet is intended to run I'm guessing it would run on a machine that has nothing to do with your working machine (laptop/PC).

To save ourselfs from the husle to login manually to our NzbGet machine and upload our nzb files there are 2 extra scripts **nzbget.py** and **nzbget.sh**

**NOTE: the steps that follow are executed on our working machine (laptop/PC)**

if you haven't set up passwordless ssh login to your NzbGet remote host you should do that now

```
ssh-keygen -t rsa -b 4096 -C "NzbGet"
# you can put password as well but it's out of scope for this demonstration
ssh-copy-id -i ~/.ssh/id_rsa.pub remoteUser@remoteIp
# ssh key should be set up and you should be able to login without a password 
#TEST BEFORE CONTINUING
``` 

**nzbget.sh** is our main script that *pushes/rsyncs* our local nzb directory with our remote nzb directory and when successfull it removes our local nzb files to save space and reduce duplication.    
To use this script do the following
```
cd NzbGet/repo/path/here
chmod u+x nzbget.sh
chmod u+x nzbget.py
# edit nzbget.sh to reflect your setup before going further
pwd # to get the full path for the next step
crontab -e
# and once inside crontab editor enter the following
* * * * * cd /paste/NzbGet/repo/full/path/here && ./nzbget.sh 
# now write and quit
```
Now our cron job will run every minute and try to sync our new files to our remote host that need to be processed. The nice thing is we can queue up on new files if our remote host if offline.

**nzbget.py** removes *sample* files and if there are no files for download it pauses NzbGet download.

### Safety

**Never run this on publically accessible IP, and you must connect with TLS always.**   
This is already configured but in case you get connection/TLS error do the following

```
# TLS Cipher support test
for v in tls1 tls1_1 tls1_2
do 
for c in $(openssl ciphers 'ALL:eNULL' | tr ':' ' ')
do
openssl s_client -connect usenetProvider:usenetPort -cipher $c -$v < /dev/null > /dev/null 2>&1 && echo -e "$v:\t$c"
done
done
```

And select the strongest cipher available to you with comparison to this [table-of-ciphers-and-their-priority-from-high-1-to-low-eg-18](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/TLS_Cipher_String_Cheat_Sheet.md#table-of-the-ciphers-and-their-priority-from-high-1-to-low-eg-18)
If possible use a cipher with **Perfect Forward Secrecy (PFS)**.
