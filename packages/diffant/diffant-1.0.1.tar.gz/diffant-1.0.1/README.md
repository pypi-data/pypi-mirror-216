# `diffant`

`diffant` uses the structure of configuration files to do a more helpful comparison than standard diff.

`diffant` allows you to compare:

* ini
* json
* yaml



For example, for the purpose of comparing configuration, these two files are the same. There should be no diff:

| file_01.ini             | file_02.ini               |
| ----------------------- | ------------------------- |
| `[info]`                | `[info]`                  |
| `email=bob@example.com` | `phone=212-555-1212`      |
| `phone=212-555-1212`    | `email = bob@example.com` |

`diffant` can meaningfully compare a heavily commented original configuration file with many lines to a minimized comment-less  configuration file and find how the defaults have changed.

You are not limited to comparing 2 files, `diffant` can compare many files.

## SAMPLE OUTPUT
```code
fruit:  apple
          tests/sample_input.dirs/simple/file01.json
          tests/sample_input.dirs/simple/file03.json

        cherry
          tests/sample_input.dirs/simple/file02.json

        /*MISSING*/
          tests/sample_input.dirs/simple/file04.json

grain:  rice
          tests/sample_input.dirs/simple/file01.json

        /*MISSING*/
          tests/sample_input.dirs/simple/file02.json
          tests/sample_input.dirs/simple/file03.json
          tests/sample_input.dirs/simple/file04.json

inspiration:art:  Pablo Picasso
                    tests/sample_input.dirs/simple/file01.json
                    tests/sample_input.dirs/simple/file03.json

                  Frida Kahlo
                    tests/sample_input.dirs/simple/file02.json

                  /*MISSING*/
                    tests/sample_input.dirs/simple/file04.json

inspiration:music:  Dead Kennedys
                      tests/sample_input.dirs/simple/file01.json
                      tests/sample_input.dirs/simple/file02.json
                      tests/sample_input.dirs/simple/file03.json

                    /*MISSING*/
                      tests/sample_input.dirs/simple/file04.json

inspiration:tools:0:  hammer
                        tests/sample_input.dirs/simple/file02.json

                      /*MISSING*/
                        tests/sample_input.dirs/simple/file01.json
                        tests/sample_input.dirs/simple/file03.json
                        tests/sample_input.dirs/simple/file04.json

inspiration:tools:1:  rack
                        tests/sample_input.dirs/simple/file02.json

                      /*MISSING*/
                        tests/sample_input.dirs/simple/file01.json
                        tests/sample_input.dirs/simple/file03.json
                        tests/sample_input.dirs/simple/file04.json

vegetable:  spinach
              tests/sample_input.dirs/simple/file03.json

            /*MISSING*/
              tests/sample_input.dirs/simple/file01.json
              tests/sample_input.dirs/simple/file02.json
              tests/sample_input.dirs/simple/file04.json
```
## SAMPLE INPUT
### file01.json
```json
{
"grain": "rice",
"color": "red",
 "fruit": "apple",
 "inspiration": {"art":"Pablo Picasso","music":"Dead Kennedys"}
}
```
### file02.json
```json
  {
   "color": "red",
   "fruit": "cherry",
   "inspiration": {"art":"Frida Kahlo","music":"Dead Kennedys","tools":["hammer","rack"]}
  }
```

### file03.json
```json
 {
   "vegetable": "spinach",
   "color": "red",
   "fruit": "apple",
   "inspiration": {"art":"Pablo Picasso","music":"Dead Kennedys"}
  }
```
### file04.json
```json
{
   "color": "red"
  }
```
## REQUIREMENTS
* pip
* python >= 3.8

## LICENSE
GNU General Public License v3.0
## SETUP
    `pip3 install diffant`

## USAGE

```
diffant  <directory with files of same type>
```

## BUGS

1. The files you are comparing need to be  at the top level of a directory that you supply as a positional argument to `diffant`
1. The files need to have an extension that reflects their contents (ini,json.yaml)
1. You can't compare files of different types or have files of different types in your input directory.

##  SUPPORT
    email dan@omacneil.org
