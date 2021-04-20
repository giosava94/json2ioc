Second example IOC.

Create the IOC with the makeBaseApp.pl functionality provided by epics base.

```
mkdir example1
cd example1
makeBaseApp.pl -t example example1
makeBaseApp.pl -i -t example example1
```

Then we followed the main procedure, explained in the main `README.md` file, to correctly set up the environment to use `json2ioc`.
