# naming-media-files-by-datetime README

# Table of contents

# Background
If we possess multiple photo-taking devices (e.g. a mobile phone and a digital camera), we will find that each device may have its own file naming format for the media taken. When we transfer these files to computer and place them under the same folder, there will be a mess. One solution is to rename all the files so that they all follow the same naming convention, which is what this tool doing.

# File naming
```
<Date>_<Time>_<Datetime type>_<Photo type>_<serial number>
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
   - The date and time fields above may not represents the actual photo-taking time, or the recording time of video or audio, due to the fact that not all media file formats will have a field to store this information. 
   - This tool will find a time information that is closest to desired time, if the desired time information was not found.
   - This single character *Datetime type* represented what type of time information was chosen for the two fields above.
      | Type | Description |
      | ---- | ----------- |
      | T    | The exact time when the photo is taken. This information might be inserted to the image file's EXIF metadata by the photo-taking device. All supported video and audio recording formats do not contain this information, so you will not see this type in those files. |
      | M    | ... |
      | C    | ... |
      | X    | ... |

# Warnings
1. 


## Guide
1. Install `MediaInfo` and obtain `MediaInfoDLL3.py`
   1. [Tutorial](https://stackoverflow.com/a/15043503).
2. Run the program with `python MediaFilesAutoNaming/MediaFilesAutoNaming.py --dir "<directory of media files>"`
