# FilesUpDown
filemanager for syncing files from PL_office to Shipyard

FileUpDown.py - starts the app (Credentials loaded from Json outside this rep)

progressbar.py - dowlnloaded from https://github.com/anler/progressbar Thanks :)

to do:
- add logging (done. make more advanced :) )
- if file already exist in \Temp - delete. It means that something went wrong on previous download
- Error: 553 The file access permissions do not allow the specified action.
- large file warning - night transfer can exceed 2h! postpone to day transfer.
- cover 100% with tests
- refactor
- Syncing full tree
- folder Update and Upload
- outlook integration
- GUI + upload

Log for User should consist of:
- empty run should be mentioned only by "date - no files to import"
- list of rarfiles
- what was in rar files
- new/overwritten files
- errors: what was not copied
