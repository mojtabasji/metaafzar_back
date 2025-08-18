from my_scraper.models import IGPage
import requests


class IgApp:
    igApi = {
        "PageDetails": "https://graph.instagram.com/v23.0/me",
        "UsersMedia": "https://graph.instagram.com/v23.0/<IG_ID>/media",
    }

    def __init__(self):
        pass

    @staticmethod
    def update_ig_details(ig_page: IGPage):
        response = requests.get(
            IgApp.igApi["PageDetails"],
            params={
                "fields": "id,user_id,name,username,account_type,media_count,followers_count,follows_count,"
                          "profile_picture_url",
                "access_token": ig_page.access_token
            }
        )
        if response.status_code == 200:
            data = response.json()
            ig_page.ig_user_id = data.get("user_id")
            ig_page.username = data.get("username")
            ig_page.followers = data.get("followers_count", 0)
            ig_page.following = data.get("follows_count", 0)
            ig_page.posts = data.get("media_count", 0)
            ig_page.bio = data.get("name", "")
            ig_page.profile_picture = data.get("profile_picture_url", "")
            ig_page.save()
            return True
        else:
            return False

    @staticmethod
    def get_ig_media(ig_page: IGPage):
        response = requests.get(
            IgApp.igApi["UsersMedia"].replace("<IG_ID>", ig_page.ig_user_id),
            params={
                "fields": "id,caption,media_type,media_url,thumbnail_url,timestamp",
                "access_token": ig_page.access_token
            }
        )
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            return []



