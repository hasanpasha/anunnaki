from cinemana import Cinemana

from requests import Session


def main():
    cinemana_source = Cinemana()
    cinemana_source.session = Session()
    cinemana_source.session.headers = cinemana_source.headers

    print(f"loaded {cinemana_source}")

    medias_page = cinemana_source.fetch_popular_media(page=1)
    # one_media = medias_page.medias[0]

    for m in medias_page.medias:
        if not m.is_movie:
            seasons = cinemana_source.get_season_list(m)
            f_episode = seasons[0].episodes[0]
            videos = cinemana_source.get_video_list(episode=f_episode)
            subtitles = cinemana_source.get_subtitle_list(episode=f_episode)
            print(videos)
            print(subtitles)
            break


if __name__ == '__main__':
    main()
