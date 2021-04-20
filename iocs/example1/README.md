First example IOC.

Create the IOC with the makeBaseApp.pl functionality provided by epics base and epicsmng.

```
mkdir example1
cd example1
makeBaseApp.pl -t ioc example1
makeBaseApp.pl -i -t ioc example1

echo 'base = R7.0.4.1' > mod.conf
epicsmng makemodules -j $(nproc) mod.conf
epicsmng configureioc mod.conf
```

Then we followed the main procedure, explained in the main `README.md` file, to correctly set up the environment to use `json2ioc`.
