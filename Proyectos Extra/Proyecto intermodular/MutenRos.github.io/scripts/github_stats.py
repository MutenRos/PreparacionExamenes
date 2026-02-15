#!/usr/bin/env python3
"""
==========================================================================
MUTENROS Portfolio - GitHub Stats Generator
==========================================================================

Python script for fetching and processing GitHub repository statistics.
Generates a JSON cache file for faster portfolio loading.

Author: Dario (MutenRos)
Version: 2.0.0
License: MIT

Features:
- Fetch all public repositories
- Calculate aggregate statistics
- Generate project thumbnails
- Cache results for performance
- Support for rate limiting

Usage:
    python github_stats.py                    # Fetch and display stats
    python github_stats.py --output cache.json  # Save to cache file
    python github_stats.py --verbose          # Verbose output

Requirements:
    pip install requests python-dotenv

==========================================================================
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' module not found. Install with: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# ==========================================================================
# CONFIGURATION
# ==========================================================================

# GitHub API Configuration
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'MutenRos')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)  # Optional: for higher rate limits
GITHUB_API_BASE = 'https://api.github.com'

# Cache Configuration
CACHE_DIR = Path(__file__).parent.parent / 'cache'
CACHE_FILE = CACHE_DIR / 'github_stats.json'
CACHE_MAX_AGE_HOURS = 1

# Repositories to exclude
EXCLUDE_REPOS = [
    f'{GITHUB_USERNAME}.github.io',  # Portfolio itself
]

# Exclude forks by default
EXCLUDE_FORKS = True

# ==========================================================================
# DATA CLASSES
# ==========================================================================

@dataclass
class Repository:
    """Repository data structure"""
    name: str
    description: Optional[str]
    language: Optional[str]
    html_url: str
    homepage: Optional[str]
    stars: int
    forks: int
    watchers: int
    open_issues: int
    is_fork: bool
    is_archived: bool
    has_pages: bool
    topics: List[str]
    created_at: str
    updated_at: str
    pushed_at: str
    size: int  # KB


@dataclass
class GitHubStats:
    """Aggregate GitHub statistics"""
    username: str
    total_repos: int
    total_stars: int
    total_forks: int
    total_watchers: int
    languages: Dict[str, int]
    most_starred: List[str]
    recently_updated: List[str]
    generated_at: str


# ==========================================================================
# LOGGING CONFIGURATION
# ==========================================================================

def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure logging"""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='[%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    return logging.getLogger(__name__)


# ==========================================================================
# GITHUB API CLIENT
# ==========================================================================

class GitHubClient:
    """GitHub API client with rate limiting and caching support"""
    
    def __init__(self, username: str, token: Optional[str] = None):
        """
        Initialize GitHub client
        
        Args:
            username: GitHub username
            token: Optional personal access token for higher rate limits
        """
        self.username = username
        self.token = token
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
        # Set up headers
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': f'{username}-portfolio-script'
        })
        
        if token:
            self.session.headers['Authorization'] = f'token {token}'
            self.logger.debug('Using authenticated requests')
    
    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """
        Make API request with error handling
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            Parsed JSON response
            
        Raises:
            requests.HTTPError: On API error
        """
        url = f'{GITHUB_API_BASE}{endpoint}'
        
        self.logger.debug(f'Requesting: {url}')
        
        response = self.session.get(url, params=params)
        
        # Check rate limiting
        remaining = response.headers.get('X-RateLimit-Remaining', 'unknown')
        self.logger.debug(f'Rate limit remaining: {remaining}')
        
        response.raise_for_status()
        return response.json()
    
    def get_user(self) -> Dict:
        """
        Get user profile information
        
        Returns:
            User profile data
        """
        return self._request(f'/users/{self.username}')
    
    def get_repositories(self, per_page: int = 100, sort: str = 'updated') -> List[Dict]:
        """
        Get all user repositories (handles pagination)
        
        Args:
            per_page: Results per page (max 100)
            sort: Sort order (created, updated, pushed, full_name)
            
        Returns:
            List of repository data
        """
        all_repos = []
        page = 1
        
        while True:
            self.logger.debug(f'Fetching page {page}...')
            
            repos = self._request(
                f'/users/{self.username}/repos',
                params={
                    'per_page': per_page,
                    'page': page,
                    'sort': sort,
                    'direction': 'desc'
                }
            )
            
            if not repos:
                break
            
            all_repos.extend(repos)
            
            if len(repos) < per_page:
                break
            
            page += 1
        
        self.logger.info(f'Fetched {len(all_repos)} repositories')
        return all_repos
    
    def get_rate_limit(self) -> Dict:
        """
        Get current rate limit status
        
        Returns:
            Rate limit information
        """
        return self._request('/rate_limit')


# ==========================================================================
# DATA PROCESSING
# ==========================================================================

def parse_repository(repo_data: Dict) -> Repository:
    """
    Parse raw API data into Repository object
    
    Args:
        repo_data: Raw repository data from API
        
    Returns:
        Parsed Repository object
    """
    return Repository(
        name=repo_data['name'],
        description=repo_data.get('description'),
        language=repo_data.get('language'),
        html_url=repo_data['html_url'],
        homepage=repo_data.get('homepage'),
        stars=repo_data.get('stargazers_count', 0),
        forks=repo_data.get('forks_count', 0),
        watchers=repo_data.get('watchers_count', 0),
        open_issues=repo_data.get('open_issues_count', 0),
        is_fork=repo_data.get('fork', False),
        is_archived=repo_data.get('archived', False),
        has_pages=repo_data.get('has_pages', False),
        topics=repo_data.get('topics', []),
        created_at=repo_data['created_at'],
        updated_at=repo_data['updated_at'],
        pushed_at=repo_data['pushed_at'],
        size=repo_data.get('size', 0)
    )


def filter_repositories(
    repos: List[Repository],
    exclude_names: List[str],
    exclude_forks: bool = True,
    exclude_archived: bool = True
) -> List[Repository]:
    """
    Filter repositories based on criteria
    
    Args:
        repos: List of Repository objects
        exclude_names: Repository names to exclude
        exclude_forks: Whether to exclude forked repos
        exclude_archived: Whether to exclude archived repos
        
    Returns:
        Filtered list of repositories
    """
    filtered = []
    
    for repo in repos:
        # Check exclusion criteria
        if repo.name in exclude_names:
            continue
        if exclude_forks and repo.is_fork:
            continue
        if exclude_archived and repo.is_archived:
            continue
        
        filtered.append(repo)
    
    return filtered


def calculate_stats(repos: List[Repository], username: str) -> GitHubStats:
    """
    Calculate aggregate statistics from repositories
    
    Args:
        repos: List of Repository objects
        username: GitHub username
        
    Returns:
        GitHubStats object with aggregated data
    """
    # Count languages
    languages: Dict[str, int] = {}
    for repo in repos:
        if repo.language:
            languages[repo.language] = languages.get(repo.language, 0) + 1
    
    # Sort languages by count
    languages = dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))
    
    # Top starred repos
    by_stars = sorted(repos, key=lambda r: r.stars, reverse=True)
    most_starred = [r.name for r in by_stars[:5]]
    
    # Recently updated repos
    by_updated = sorted(repos, key=lambda r: r.updated_at, reverse=True)
    recently_updated = [r.name for r in by_updated[:5]]
    
    return GitHubStats(
        username=username,
        total_repos=len(repos),
        total_stars=sum(r.stars for r in repos),
        total_forks=sum(r.forks for r in repos),
        total_watchers=sum(r.watchers for r in repos),
        languages=languages,
        most_starred=most_starred,
        recently_updated=recently_updated,
        generated_at=datetime.utcnow().isoformat() + 'Z'
    )


# ==========================================================================
# CACHE MANAGEMENT
# ==========================================================================

def load_cache(cache_path: Path) -> Optional[Dict]:
    """
    Load cached data if valid
    
    Args:
        cache_path: Path to cache file
        
    Returns:
        Cached data or None if invalid/expired
    """
    if not cache_path.exists():
        return None
    
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check cache age
        generated_at = datetime.fromisoformat(
            data.get('stats', {}).get('generated_at', '').replace('Z', '+00:00')
        )
        age = datetime.utcnow() - generated_at.replace(tzinfo=None)
        
        if age.total_seconds() > CACHE_MAX_AGE_HOURS * 3600:
            return None
        
        return data
        
    except (json.JSONDecodeError, ValueError, KeyError):
        return None


def save_cache(cache_path: Path, data: Dict) -> None:
    """
    Save data to cache file
    
    Args:
        cache_path: Path to cache file
        data: Data to cache
    """
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ==========================================================================
# MAIN FUNCTIONS
# ==========================================================================

def fetch_github_data(
    username: str = GITHUB_USERNAME,
    token: Optional[str] = GITHUB_TOKEN,
    use_cache: bool = True
) -> Dict:
    """
    Fetch and process GitHub data
    
    Args:
        username: GitHub username
        token: Optional API token
        use_cache: Whether to use caching
        
    Returns:
        Dictionary with repos and stats
    """
    logger = logging.getLogger(__name__)
    
    # Try cache first
    if use_cache:
        cached = load_cache(CACHE_FILE)
        if cached:
            logger.info('Using cached data')
            return cached
    
    # Fetch from API
    client = GitHubClient(username, token)
    
    logger.info(f'Fetching repositories for {username}...')
    raw_repos = client.get_repositories()
    
    # Parse and filter
    repos = [parse_repository(r) for r in raw_repos]
    repos = filter_repositories(repos, EXCLUDE_REPOS, EXCLUDE_FORKS)
    
    logger.info(f'Processing {len(repos)} repositories...')
    
    # Calculate stats
    stats = calculate_stats(repos, username)
    
    # Prepare output
    result = {
        'stats': asdict(stats),
        'repositories': [asdict(r) for r in repos]
    }
    
    # Save to cache
    if use_cache:
        save_cache(CACHE_FILE, result)
        logger.info(f'Saved cache to {CACHE_FILE}')
    
    return result


def print_stats(data: Dict) -> None:
    """Print formatted statistics to console"""
    stats = data['stats']
    
    print('\n' + '=' * 50)
    print(f"  GITHUB STATS: {stats['username']}")
    print('=' * 50)
    print(f"\n  📊 Total Repositories: {stats['total_repos']}")
    print(f"  ⭐ Total Stars: {stats['total_stars']}")
    print(f"  🍴 Total Forks: {stats['total_forks']}")
    
    print('\n  📝 Top Languages:')
    for lang, count in list(stats['languages'].items())[:5]:
        print(f"     • {lang}: {count} repos")
    
    print('\n  🌟 Most Starred:')
    for repo in stats['most_starred']:
        print(f"     • {repo}")
    
    print('\n  🕐 Recently Updated:')
    for repo in stats['recently_updated']:
        print(f"     • {repo}")
    
    print('\n' + '=' * 50)
    print(f"  Generated: {stats['generated_at']}")
    print('=' * 50 + '\n')


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Fetch GitHub repository statistics for portfolio'
    )
    parser.add_argument(
        '-u', '--username',
        default=GITHUB_USERNAME,
        help='GitHub username'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output JSON file path'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Skip cache and fetch fresh data'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.verbose)
    
    try:
        # Fetch data
        data = fetch_github_data(
            username=args.username,
            use_cache=not args.no_cache
        )
        
        # Output
        if args.output:
            save_cache(args.output, data)
            logger.info(f'Saved to {args.output}')
        else:
            print_stats(data)
        
    except requests.HTTPError as e:
        logger.error(f'API Error: {e}')
        sys.exit(1)
    except Exception as e:
        logger.error(f'Error: {e}')
        if args.verbose:
            raise
        sys.exit(1)


if __name__ == '__main__':
    main()
