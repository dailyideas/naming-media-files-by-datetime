# naming-media-files-by-datetime README

# Table of contents

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
2. Time
   - The photo-taking time, or the recording time of video or audio.
   - If this information was not found in the file's metadata, alternative time information will be substituted. See *Datetime type* for details.
   - Represented as `HHMMSS`.
3. Datetime type
   - The date and time fields above may not represents the actual photo-taking time, or the recording time of video or audio, due to the fact that not all media files will store this information. 
   - This tool will set the *Date* and *Time* fields as the oldest time information found from time-related metadata, if the actual photo-taking time, or the recording time of video or audio cannot be found.
   - This single character *Datetime type* represented what type of time information was chosen for the *Date* and *Time* fields.
      | Type | Description |
      | ---- | ----------- |
      | A    | The actual photo-taking time, or the recording time of video or audio. |
      | B    | The oldest time information found in the file's metadata, which probably not representing the actual photo-taking time, or the recording time of video or audio. |
      | C    | A hard-coded date, provided by the user.  |
      | X    | No time information could be used. |
4. Editing status
   - This field represents whether the media file is an edited one or os the original copy. 
   - The file will be classified as edited if the word "edit" appears in the file name, or name of media file editing sotware exists in the files metadata. 
   - Noted that most video and audio files do not contain the name of editing sotware in their metadata, so video and audio files will be classified as edited only if the word "edit" appears in the file name.
      | Type | Description |
      | ---- | ----------- |
      | Orig | The file is the original copy, or at least no cues indicating that the file is edited. |
      | Edit | The file was edited. |
5. Serial number
   - A *5-digit* integer, starts from `00000`.
   - Under burst mode of cameras, it is possible that multiple photos are taken in one second. In this case, file name duplication will exist for two independent photos. A *Serial number* is therefore required to prevent this situation.
   - For a file being renamed, if the tool found file name duplication, it will incremend the *Serial number* of the current file until no duplication is found. 
   - It does not guarantee that a photo with smaller *Serial number* must be taken before a larger one.
   - There is no relationship between two files with same *Serial number* but different *Editing status*.

# Warnings
1. This file naming style may not suit all users' preferences. Customized file naming format is currently not supported. If you are not willing to rename your media files as descripted in Section [File naming](#File-naming), please do not consider this tool. 


## Guide
1. Download **exiftool**.
   - Windows
     - 
