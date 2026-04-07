import requests
import time
import sys
from typing import Set, List

# Colors for console output (optional)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def get_headers(token: str) -> dict:
    """Returns headers for GitHub API requests"""
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Unfollow-Bot"
    }

def get_all_users(url: str, token: str, session: requests.Session) -> Set[str]:
    """
    Fetches all users from a paginated GitHub API endpoint.
    Returns a set of usernames.
    """
    users = set()
    page = 1
    per_page = 100
    
    while True:
        response = session.get(
            url,
            headers=get_headers(token),
            params={"per_page": per_page, "page": page}
        )
        
        if response.status_code != 200:
            print(f"{Colors.RED}❌ API Error: {response.status_code} - {response.text}{Colors.END}")
            break
        
        data = response.json()
        if not data:
            break
            
        for user in data:
            users.add(user["login"])
        
        # Check if there's a next page
        if len(data) < per_page:
            break
            
        page += 1
        
        # Small delay to avoid hitting API limits
        time.sleep(0.1)
    
    return users

def unfollow_user(username: str, token: str, session: requests.Session, dry_run: bool = False) -> bool:
    """Unfollows the specified user"""
    url = f"https://api.github.com/user/following/{username}"
    
    if dry_run:
        print(f"{Colors.YELLOW}🔍 [DRY RUN] Would unfollow: {username}{Colors.END}")
        return True
    
    response = session.delete(url, headers=get_headers(token))
    
    if response.status_code == 204:
        print(f"{Colors.GREEN}✅ Unfollowed: {username}{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}❌ Failed to unfollow {username}: {response.status_code}{Colors.END}")
        return False

def main():
    """Main function of the script"""
    print(f"{Colors.HEADER}{'='*60}{Colors.END}")
    print(f"{Colors.HEADER}🤖 GitHub Unfollow Manager - Clean up your following{Colors.END}")
    print(f"{Colors.HEADER}{'='*60}{Colors.END}\n")
    
    # Request token from user
    token = input(f"{Colors.BLUE}🔑 Enter your GitHub Personal Access Token: {Colors.END}").strip()
    
    if not token:
        print(f"{Colors.RED}❌ Token cannot be empty!{Colors.END}")
        sys.exit(1)
    
    # Check if user wants a dry run
    dry_run_input = input(f"{Colors.BLUE}🧪 Run in dry-run mode (show only, no actual unfollowing)? (y/n): {Colors.END}").strip().lower()
    dry_run = dry_run_input == 'y'
    
    # Create session for connection reuse
    session = requests.Session()
    
    print(f"\n{Colors.BLUE}📡 Fetching data from GitHub API...{Colors.END}\n")
    
    try:
        # Get list of users the current user is following
        print(f"{Colors.YELLOW}📋 Loading following list...{Colors.END}")
        following = get_all_users("https://api.github.com/user/following", token, session)
        print(f"{Colors.GREEN}✅ Found following: {len(following)}{Colors.END}\n")
        
        # Get list of followers of the current user
        print(f"{Colors.YELLOW}📋 Loading followers list...{Colors.END}")
        followers = get_all_users("https://api.github.com/user/followers", token, session)
        print(f"{Colors.GREEN}✅ Found followers: {len(followers)}{Colors.END}\n")
        
        # Find users who don't follow back
        non_follow_back = following - followers
        
        if not non_follow_back:
            print(f"{Colors.GREEN}🎉 Great news! Everyone you follow follows you back!{Colors.END}")
            return
        
        print(f"{Colors.YELLOW}⚠️ Found users who don't follow you back: {len(non_follow_back)}{Colors.END}\n")
        
        # Display the list
        print(f"{Colors.HEADER}📋 List of users to unfollow:{Colors.END}")
        for i, username in enumerate(sorted(non_follow_back), 1):
            print(f"  {i}. {username}")
        
        print(f"\n{Colors.YELLOW}⚠️ WARNING: GitHub may temporarily rate-limit your account for mass actions!{Colors.END}")
        
        if not dry_run:
            confirm = input(f"\n{Colors.RED}❓ Are you sure you want to unfollow {len(non_follow_back)} users? (yes/no): {Colors.END}").strip().lower()
            
            if confirm != 'yes':
                print(f"{Colors.YELLOW}❌ Operation cancelled.{Colors.END}")
                return
        
        # Unfollow users
        print(f"\n{Colors.BLUE}🔄 Starting unfollow process...{Colors.END}\n")
        
        success_count = 0
        for i, username in enumerate(sorted(non_follow_back), 1):
            print(f"[{i}/{len(non_follow_back)}] ", end="")
            if unfollow_user(username, token, session, dry_run):
                success_count += 1
            
            # Delay between requests to avoid rate limiting
            # Recommended 1-2 seconds for safety
            time.sleep(2)
        
        # Final report
        print(f"\n{Colors.HEADER}{'='*60}{Colors.END}")
        if dry_run:
            print(f"{Colors.GREEN}✅ Dry run completed! Would unfollow: {success_count} users{Colors.END}")
        else:
            print(f"{Colors.GREEN}✅ Done! Successfully unfollowed {success_count} out of {len(non_follow_back)} users{Colors.END}")
        print(f"{Colors.HEADER}{'='*60}{Colors.END}")
        
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}❌ Network error: {e}{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()