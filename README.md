# spacy-pl-utils
Utilities for development polish language support for Spacy.

## Folders
Use separated folders for every module pipeline.

## Using DVC
We store all artifacts in folders `data` and `models`.
### Adding new step
To add new step to pipeline use 

```dvc run [-d <dependencies>] [-o <result_artifacts>] (-f <step_name>.dvc) <command>```

in main folder.
### Reproduce artifact
When something in pipeline changed and you want to run all steps again, use 

`dvc repro <step_name>`

with `<step_name>` to which you want to rerun pipeline.

### Synchronization
Synchronization always works with in connection with current branch and commit.
```dvc push```
Send all tracked artifacts to remote.
```dvc pull```
Get all tracked arfitfacts from remote.
### Print pipeline
```dvc pipeline show -c --ascii```


