# FilesUpDown
filemanager for syncing files from PL_office to Shipyard

FileUpDown.py - starts the app (Credentials loaded from Json outside this rep)

progressbar.py - dowlnloaded from https://github.com/anler/progressbar Thanks :)

to do:
- add logging (done. make more advanced :) )
- Error: 553 The file access permissions do not allow the specified action.
- cover 100% with tests
- refactor
- Syncing full tree
- folder Update and Upload
- outlook integration
- GUI + upload

Log for User should consist of:
- list of rarfiles
- what was in rar files
- new/overwritten files
- errors: what was not copied