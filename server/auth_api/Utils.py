from rest_framework_simplejwt.tokens import RefreshToken


class Utils:
    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    @staticmethod
    def get_leads (leads, leads_count, page=2):
        if (leads_count > 25):
            if (page == 1):
                return leads[: 25]
            else:
                x = (page-1) * 25
                try: 
                    new_leads = leads[x: x+25]
                except:
                    return leads[x:]
                else:
                    return new_leads
        else:
            return leads
    @staticmethod       
    def get_total_pages(count):
        if (count < 25):
            return 1
        if (count % 25 == 0):
            return count // 25
        return (count // 25) + 1

        