FOLLOW LIMITS = 100
POST_LIKES = 50

Scraping Service = ss
Get Valid User Service = gvus
Connect User to a Profile Service = cups
Bot Service = bs
Storage Service = ss

gvus:

    args: username
    table: scraped_accounts, user_profile_links(foreign table)
    action1: get profile that the last_interaction_date is more than 1 week or is null
    action2: username, profile_id is not in the user_profile_links(foreign) table
    return: profile_link

cups: 

    args: username, profile_id
    table: scraped_accounts, user_profile_links(foreign)
    action: for the profile with this {profile_id}, add username to the user_profile_links table with the profile_id, then update the last_interaction_date to now


Services:
     
    Scraping service
    Get Valid User Service (get some user based on defined rules) a.k.a gvus


bs:
    
    Bot name: bot_mark (with mark being the creator account the bot is automating) 
    
    actions:
        1. bot_mark will call gvus and pass Mark username to it returning a valid profile to work with
        2. bot_mark will login into mark's account and follow profile and like latest post
        3. call the cups service and pass Mark's username to it

ss:

    Create a storage in supabase called Session
    3 Functions:
        1. get_session
        2. store_session
        3. check_session_is_available



1. Call check_session_is_available to confirm [Username].json
if not session:
    Login afresh
if session:
    Login with session

2. Follow Account
<!-- 3. Like lastest post -->

