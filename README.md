
### A Python script that finds users you're following who don't follow you back, and then unfollows them

## 📊 How the Script Works
1. Fetches your following list - all users you're following
2. Fetches your followers list - all users following you
3. Finds the difference - users you follow who don't follow you back (following − followers)
4. Displays the list of found users
5. Asks for confirmation before unfollowing
6. Unfollows each user via the GitHub API

## 🧪 Dry Run Mode
The script supports a dry-run mode. When you run it, you can choose this option - the script will show which users would be unfollowed without actually performing any actions. This is useful for testing before actual execution.

## ⚠️ Important Warnings
1. **API Rate Limits** - GitHub limits the number of requests (up to 5000 per hour for authenticated users). The script handles pagination and won't exceed limits
2. **Account Suspension** - Mass actions can lead to temporary suspension. GitHub considers automated follows/unfollows as potential spam
3. **Recommendations**:
    - Don't run the script too frequently (once a week is enough)
    - Don't unfollow hundreds of users at once
    - Use dry-run mode for testing

## 🧩 Install Dependencies
The script only needs the `requests` library. Install it with:
```bash
pip install requests
```

## 🧰 Create a Personal Access Token
To use this script, you need a GitHub Personal Access Token:  
🔹Go to Settings → Developer settings → Personal access tokens → Tokens (classic)  
🔹Click Generate new token (classic)   
🔹Give it a name (e.g., unfollow-bot)  
🔹Set an expiration (recommended: 30 or 90 days)  
🔹Select the required scopes:
  - ***user:follow*** (required) - to manage follows/unfollows  
  - ***user:read*** (automatically added)  

🔹Click **Generate token** and copy the token  

⚠️ **Important:** The token is only shown once! Save it in a secure place.

## 🤖 Example Output

🔑 Enter your GitHub Personal Access Token: ****************************************  

🧪 Run in dry-run mode (show only, no actual unfollowing)? (y/n): n

📡 Fetching data from GitHub API...

📋 Loading following list...
✅ Found following: 150

📋 Loading followers list...
✅ Found followers: 89

⚠️ Found users who don't follow you back: 61

📋 List of users to unfollow:
  1. user1
  2. user2
  ...

⚠️ WARNING: GitHub may temporarily rate-limit your account for mass actions!   
❓ Are you sure you want to unfollow 61 users? (yes/no): yes

🔄 Starting unfollow process...

[1/61] ✅ Unfollowed: user1  
[2/61] ✅ Unfollowed: user2  
...

✅ Done! Successfully unfollowed 61 out of 61 users  

