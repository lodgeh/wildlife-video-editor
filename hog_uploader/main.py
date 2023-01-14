import os

from file_utils import (
    concatenate_videos_and_save_to_output,
    get_file_metadata,
    get_unique_dates,
    groups_files_into_days,
    move_file,
)

from yt_upload_utils import (
    get_authenticated_service,
    create_video_upload_request,
    start_video_upload,
    add_video_to_playlist,
)

PLAYLIST_ID = "PLtZv6jHN_L88JZmqB7yhdxAtm3MEn3CQH"


def main():
    youtube_secret_path = "../youtube_secrets.json"
    youtube = get_authenticated_service(youtube_secret_path)

    input_directory = os.listdir("../input")
    file_dict = get_file_metadata(input_directory)
    unique_dates = get_unique_dates(file_dict)
    groups = groups_files_into_days(file_dict, unique_dates)
    concatenate_videos_and_save_to_output(groups)

    for file in input_directory:
        file_path = os.path.join("../input", file)
        archive_file_path = os.path.join("../archive/raw/")
        move_file(file_path, archive_file_path)

    output_directory = os.listdir("../output")
    for file in output_directory:
        file_name = file.split(".mp4")[0]
        file_path = f"../output/{file}"
        archive_file_path = f"../archive/concatenated/"
        video_id = upload_youtube_video(youtube, file_name, file_path)
        add_video_to_playlist(youtube, PLAYLIST_ID, video_id)
        move_file(file_path, archive_file_path)


def upload_youtube_video(youtube, video_title, file_path):
    video_upload_request = create_video_upload_request(youtube, video_title, file_path)
    video_id = start_video_upload(video_upload_request)
    return video_id


if __name__ == "__main__":
    main()
