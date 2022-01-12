# naming-media-files-by-datetime README

# Table of contents
- [Background](#background)
- [File naming](#File-naming)
- [Warnings](#Warnings)
- [Installation guide](#Installation-guide)
- [Usage](#Usage)
    - [Execute from Python](#Execute-from-python)
    - [Execute from executable](#Execute-from-executable)
    - [Execute from *cliAssistant.exe*](#Execute-from-cliassistantexe)
    - [Arguments](#Arguments)
- [Licensing](#Licensing)
- [Dependencies](#Dependencies)
- [Versioning](#Versioning)

# Background
If we possess multiple photo-taking devices (e.g. a mobile phone and a digital camera), we will find that each device may have its own file naming format for the media taken. When we transfer these files to computer and place them under the same folder, there will be a mess. One solution is to rename all the files so that they all follow the same naming convention, which is what this tool doing.

# File naming
    ```
    <Date>_<Time>_<Datetime type>_<Editing status>_<Serial number>
    ```
1. Date
    - The photo-taking date, or the recording date of video or audio.
    - If this information was not found in the file's metadata, alternative date information will be substituted. See *Datetime type* for details.
    - Represented as `YYYYMMDD`.
1. Time
    - The photo-taking time, or the recording time of video or audio.
    - If this information was not found in the file's metadata, alternative time information will be substituted. See *Datetime type* for details.
    - Represented as `HHMMSS`.
1. Datetime type
    - The date and time fields above may not represents the actual photo-taking time, or the recording time of video or audio, due to the fact that not all media files will store this information. 
    - This tool will set the *Date* and *Time* fields as the oldest time information found from time-related metadata, if the actual photo-taking time, or the recording time of video or audio cannot be found.
    - This single character *Datetime type* represented what type of time information was chosen for the *Date* and *Time* fields.
        | Type | Description |
        | ---- | ----------- |
        | A    | The actual photo-taking time, or the recording time of video or audio. |
        | B    | The oldest time information found in the file's metadata, which probably not representing the actual photo-taking time, or the recording time of video or audio. |
        | C    | A hard-coded date, provided by the user.  |
        | X    | No time information could be used. |
1. Editing status
    - This field represents whether the media file is an edited one or os the original copy. 
    - The file will be classified as edited if the word "edit" appears in the file name, or name of media file editing sotware exists in the files metadata. 
    - Noted that most video and audio files do not contain the name of editing sotware in their metadata, so video and audio files will be classified as edited only if the word "edit" appears in the file name.
        | Type | Description |
        | ---- | ----------- |
        | Orig | The file is the original copy, or at least no cues indicating that the file is edited. |
        | Edit | The file was edited. |
1. Serial number
    - A *5-digit* integer, starts from `00000`.
    - Under burst mode of cameras, it is possible that multiple photos are taken in one second. In this case, file name duplication will exist for two independent photos. A *Serial number* is therefore required to prevent this situation.
    - For a file being renamed, if the tool found file name duplication, it will incremend the *Serial number* of the current file until no duplication is found. 
    - It does not guarantee that a photo with smaller *Serial number* must be taken before a larger one.
    - There is no relationship between two files with same *Serial number* but different *Editing status*.

# Warnings
1. This file naming style may not suit all users' preferences. Customized file naming format is currently not supported. If you are not willing to rename your media files as descripted in Section [File naming](#File-naming), please do not consider this tool. 


# Installation guide
1. Download [exiftool](https://exiftool.org/).
    - [Official document](https://github.com/exiftool/exiftool)
    - Linux
        - Download the source.
    - Mac
        - Download the *MacOS Package*
    - Windows
        - Download the *Windows Executable*
1. Set up **exiftool**.
    - Linux
        - Unzip the downloaded file. 
        - `tar -xf archive.tar.gz` 
        - [Tutorial](https://linuxize.com/post/how-to-extract-unzip-tar-gz-file/)
        - Go to the unzipped directory.
        - Build the package
            ```
            perl Makefile.PL
            make
            make test
            make install
            ```
        - [Official tutorial](https://github.com/exiftool/exiftool)
    - Mac
        - I don't know.
    - Windows
        - Unzip the downloaded file to get `exiftool(-k).exe`.
        - Rename `exiftool(-k).exe` to `exiftool.exe`. (The stand-alone version ("exiftool(-k).exe") should be renamed to "exiftool.exe" to allow it to be run by typing "exiftool" at the command line. [Reference](https://exiftool.org/))
        - Move `exiftool.exe` to a folder you want. 
1. (Windows only) Add the location of **exiftool** to *PATH*.
    - Open the *Properties* window of `exiftool.exe`.
        - [Tutorial](https://www.howto-connect.com/open-file-properties-windows-10/)
    - Copy the *Location* value.
    - Open the *Environment Variables* window of the Windows system.
        - [Tutorial](https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/)
        - [Tutorial](https://www.computerhope.com/issues/ch000549.htm)
    - Edit the *Path* variable of *User variables* by double-clicking the row. 
    - Click the button *New* on the top-right.
    - Paste the *Location* value previously copied.
2. Download this tool.
    - Linux / Mac
        - Clone this repository to the host machine.
            - [Official tutorial](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
    - Windows
        - (If familiar with using Python) Clone this repository to the host machine.
        - (If want a standalone script) Download the compiled executables to the host machine.

# Usage
1. Go the the tool's directory.
2. Execute the tool
    - [Execute from Python](#Execute-from-Python)
    - [Execute from executable](#Execute-from-executable)
    - [Execute from *cliAssistant.exe*](#Execute-from-cliAssistantexe)

## Execute from Python
```
  python main.py --dir <directory> [--date <alternative date>] [-r]
```
- See Section [Arguments](#Arguments) for the usage of arguments.

## Execute from executable
```
  main --dir <directory> [--date <alternative date>] [-r]
```
- Applicable to Windows users only.
- See Section [Arguments](#Arguments) for the usage of arguments.

## Execute from *cliAssistant.exe*
- Applicable to Windows users only.
- Run the `cliAssistant.exe` by double-clicking it.

## Arguments
- `--dir <directory>`
    - Required 
    - Replace `<directory>` with the location of directory/folder which contains the media files you want to rename.
- `--date <alternative date>`
    - Optional
    - If you know the date that these media files were created, you may set this parameter.
    - If photo-taking time, or the recording time of video or audio, cannot be found in the media file's metadata, this tool may use the provided date for the *Date* field in [File naming](#File-naming).
    - Replace `<alternative date>` with a date in [ISO8601](https://www.iso.org/iso-8601-date-and-time-format.html) format. (e.g. 2021-12-31)
- `-r`
    - Optional
    - If set, this tool will search for media files recursively. Else, only media files at the specified directory will be renamed. 

# Licensing
This project is licensed under the MIT License. See [LICENSE](./LICENSE) for the full license text.

# Dependencies
This project is dependent on third-party libraries or other resources listed below.

1. exiftool
    - Phil Harvey
    - [Perl Licensing](https://dev.perl.org/licenses/)

# Versioning
This project follows the [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)
