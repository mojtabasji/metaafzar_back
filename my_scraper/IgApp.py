from my_scraper.models import IGPage
import requests

class IgApp:
    igApi = {
        "PageDetails": "https://graph.instagram.com/v23.0/me"
    }

    def __init__(self):
        pass

    @staticmethod
    def update_ig_details(ig_page: IGPage):
        response = requests.get(
            IgApp.igApi["PageDetails"],
            params={
                "fields": "id,user_id,name,username,account_type,media_count,followers_count,follows_count",
                "access_token": ig_page.access_token
            }
        )
        if response.status_code == 200:
            data = response.json()
            ig_page.ig_user_id = data.get("id")
            ig_page.username = data.get("username")
            ig_page.followers = data.get("followers_count", 0)
            ig_page.following = data.get("follows_count", 0)
            ig_page.posts = data.get("media_count", 0)
            ig_page.bio = data.get("name", "")
            ig_page.profile_picture = f"https://graph.instagram.com/{data.get('id')}/picture?access_token={ig_page.access_token}"
            ig_page.save()
            return True
        else:
            return False



