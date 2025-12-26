"""
Microsoft Clarity Service
"""
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class ClarityService:
    """Microsoft Clarity integration service"""
    
    BASE_URL = "https://www.clarity.ms/api"
    
    def __init__(self, api_key: str):
        """
        Initialize Clarity service
        
        Args:
            api_key: Clarity API key
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.project_ids = []
    
    def set_project_ids(self, project_ids: List[str]):
        """Set Clarity project IDs"""
        self.project_ids = project_ids
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get list of available projects"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/projects",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return []
    
    def get_project_stats(self, project_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Get project statistics
        
        Args:
            project_id: Project ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            Project statistics
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/projects/{project_id}/stats",
                headers=self.headers,
                params={
                    "startDate": start_date,
                    "endDate": end_date
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching project stats: {e}")
            return {'error': str(e)}
    
    def get_heatmaps(self, project_id: str, page_url: str, days: int = 7) -> Dict[str, Any]:
        """
        Get heatmap data for a specific page
        
        Args:
            project_id: Project ID
            page_url: Page URL to get heatmap for
            days: Number of days of data
        
        Returns:
            Heatmap data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/projects/{project_id}/heatmaps",
                headers=self.headers,
                params={
                    "url": page_url,
                    "startDate": start_date.strftime('%Y-%m-%d'),
                    "endDate": end_date.strftime('%Y-%m-%d')
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching heatmaps: {e}")
            return {'error': str(e)}
    
    def get_session_recordings(self, project_id: str, limit: int = 50, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Get session recordings
        
        Args:
            project_id: Project ID
            limit: Maximum number of recordings to return
            filters: Optional filters for recordings
        
        Returns:
            List of session recordings
        """
        try:
            params = {"limit": limit}
            if filters:
                params.update(filters)
            
            response = requests.get(
                f"{self.BASE_URL}/projects/{project_id}/sessions",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching session recordings: {e}")
            return []
    
    def get_rage_clicks(self, project_id: str, days: int = 7) -> Dict[str, Any]:
        """
        Get rage click data
        
        Args:
            project_id: Project ID
            days: Number of days of data
        
        Returns:
            Rage click data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/projects/{project_id}/rage-clicks",
                headers=self.headers,
                params={
                    "startDate": start_date.strftime('%Y-%m-%d'),
                    "endDate": end_date.strftime('%Y-%m-%d')
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching rage clicks: {e}")
            return {'error': str(e)}
    
    def get_dead_clicks(self, project_id: str, days: int = 7) -> Dict[str, Any]:
        """
        Get dead click data
        
        Args:
            project_id: Project ID
            days: Number of days of data
        
        Returns:
            Dead click data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/projects/{project_id}/dead-clicks",
                headers=self.headers,
                params={
                    "startDate": start_date.strftime('%Y-%m-%d'),
                    "endDate": end_date.strftime('%Y-%m-%d')
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching dead clicks: {e}")
            return {'error': str(e)}
    
    def get_scroll_depth(self, project_id: str, page_url: str, days: int = 7) -> Dict[str, Any]:
        """
        Get scroll depth data for a specific page
        
        Args:
            project_id: Project ID
            page_url: Page URL
            days: Number of days of data
        
        Returns:
            Scroll depth data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/projects/{project_id}/scroll-depth",
                headers=self.headers,
                params={
                    "url": page_url,
                    "startDate": start_date.strftime('%Y-%m-%d'),
                    "endDate": end_date.strftime('%Y-%m-%d')
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching scroll depth: {e}")
            return {'error': str(e)}
    
    def get_user_insights(self, project_id: str, days: int = 7) -> Dict[str, Any]:
        """
        Get user behavior insights
        
        Args:
            project_id: Project ID
            days: Number of days of data
        
        Returns:
            User insights data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/projects/{project_id}/insights",
                headers=self.headers,
                params={
                    "startDate": start_date.strftime('%Y-%m-%d'),
                    "endDate": end_date.strftime('%Y-%m-%d')
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching user insights: {e}")
            return {'error': str(e)}
