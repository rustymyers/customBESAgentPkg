# customBESAgentPkg

Add actionsite.afxm to ModifiedFiles folder

Add stock BESAgent installer to root folder

Run ./customBESAgentPkg.py

If you want to include clientsettings.cfg in the custom pacakge, use the -s flag.

Adding a brand can be done by editing the "name" variable in the customBESAgentPkg.py script and using the -b flag.

```
usage: customBESAgentPkg.py [-h] [--brand CUSTOM_BRAND] [--settings]
                            [--package CUSTOM_PKG]

Build Custom BESAgent Installers.

optional arguments:
  -h, --help            show this help message and exit
  --brand CUSTOM_BRAND, -b CUSTOM_BRAND
                        add branding text to the BESAgent pacakge
  --settings, -s        add custom settings cfg to the BESAgent pacakge
  --package CUSTOM_PKG, -p CUSTOM_PKG
                        specify the BESAgent pacakge to use
```
