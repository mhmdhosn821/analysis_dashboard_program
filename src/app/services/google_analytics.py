"""
Google Analytics 4 Service
"""
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
import pickle
from pathlib import Path


class GoogleAnalyticsService:
    """Google Analytics 4 integration service"""
    
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    
    def __init__(self, credentials_file: Optional[str] = None):
        """
        Initialize Google Analytics service
        
        Args:
            credentials_file: Path to OAuth2 credentials file
        """
        self.credentials_file = credentials_file
        self.credentials = None
        self.service = None
        self.property_ids = []
    
    def authenticate(self, client_id: str, client_secret: str, redirect_uri: str = "http://localhost:8080/") -> str:
        """
        Start OAuth2 authentication flow
        
        Returns:
            Authorization URL for user to visit
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            scopes=self.SCOPES,
            redirect_uri=redirect_uri
        )
        
        auth_url, _ = flow.authorization_url(prompt='consent')
        return auth_url
    
    def complete_authentication(self, authorization_response: str, client_id: str, client_secret: str):
        """
        Complete OAuth2 authentication with authorization code
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=self.SCOPES,
            redirect_uri="http://localhost:8080/"
        )
        
        flow.fetch_token(authorization_response=authorization_response)
        self.credentials = flow.credentials
        self._save_credentials()
        self._build_service()
    
    def load_credentials(self, token_file: str) -> bool:
        """Load credentials from file"""
        token_path = Path(token_file)
        if token_path.exists():
            with open(token_path, 'rb') as token:
                self.credentials = pickle.load(token)
            
            # Refresh if expired
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
                self._save_credentials()
            
            self._build_service()
            return True
        return False
    
    def _save_credentials(self):
        """Save credentials to file"""
        if self.credentials_file:
            with open(self.credentials_file, 'wb') as token:
                pickle.dump(self.credentials, token)
    
    def _build_service(self):
        """Build Analytics service"""
        if self.credentials:
            self.service = build('analyticsdata', 'v1beta', credentials=self.credentials)
    
    def set_property_ids(self, property_ids: List[str]):
        """Set GA4 property IDs"""
        self.property_ids = property_ids
    
    def get_properties(self) -> List[Dict[str, str]]:
        """Get list of available properties"""
        if not self.service:
            return []
        
        try:
            admin_service = build('analyticsadmin', 'v1beta', credentials=self.credentials)
            accounts = admin_service.accounts().list().execute()
            
            properties = []
            for account in accounts.get('accounts', []):
                account_id = account['name']
                props = admin_service.properties().list(filter=f"parent:{account_id}").execute()
                for prop in props.get('properties', []):
                    properties.append({
                        'id': prop['name'].split('/')[-1],
                        'display_name': prop.get('displayName', ''),
                        'account': account.get('displayName', '')
                    })
            
            return properties
        except Exception as e:
            print(f"Error fetching properties: {e}")
            return []
    
    def run_report(self, property_id: str, metrics: List[str], dimensions: List[str], 
                   start_date: str, end_date: str, **kwargs) -> Dict[str, Any]:
        """
        Run a GA4 report
        
        Args:
            property_id: GA4 property ID
            metrics: List of metrics (e.g., ['activeUsers', 'sessions'])
            dimensions: List of dimensions (e.g., ['date', 'city'])
            start_date: Start date (YYYY-MM-DD or 'NdaysAgo')
            end_date: End date (YYYY-MM-DD or 'today')
            **kwargs: Additional parameters
        
        Returns:
            Report data dictionary
        """
        if not self.service:
            raise Exception("Service not initialized. Please authenticate first.")
        
        request_body = {
            'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
            'metrics': [{'name': m} for m in metrics],
            'dimensions': [{'name': d} for d in dimensions],
        }
        
        # Add optional parameters
        if 'dimension_filter' in kwargs:
            request_body['dimensionFilter'] = kwargs['dimension_filter']
        if 'metric_filter' in kwargs:
            request_body['metricFilter'] = kwargs['metric_filter']
        if 'order_bys' in kwargs:
            request_body['orderBys'] = kwargs['order_bys']
        if 'limit' in kwargs:
            request_body['limit'] = kwargs['limit']
        
        try:
            response = self.service.properties().runReport(
                property=f'properties/{property_id}',
                body=request_body
            ).execute()
            
            return self._parse_report_response(response)
        except Exception as e:
            print(f"Error running report: {e}")
            return {'error': str(e)}
    
    def _parse_report_response(self, response: Dict) -> Dict[str, Any]:
        """Parse GA4 report response"""
        rows = []
        dimension_headers = [h['name'] for h in response.get('dimensionHeaders', [])]
        metric_headers = [h['name'] for h in response.get('metricHeaders', [])]
        
        for row in response.get('rows', []):
            row_data = {}
            
            # Parse dimensions
            for i, value in enumerate(row.get('dimensionValues', [])):
                row_data[dimension_headers[i]] = value.get('value', '')
            
            # Parse metrics
            for i, value in enumerate(row.get('metricValues', [])):
                row_data[metric_headers[i]] = value.get('value', '')
            
            rows.append(row_data)
        
        return {
            'rows': rows,
            'row_count': response.get('rowCount', 0),
            'metadata': response.get('metadata', {}),
            'dimension_headers': dimension_headers,
            'metric_headers': metric_headers
        }
    
    # High-level methods for specific data
    
    def get_performance_overview(self, property_id: str, days: int = 7) -> Dict[str, Any]:
        """Get performance overview data"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        metrics = ['activeUsers', 'newUsers', 'sessions', 'averageSessionDuration', 
                   'bounceRate', 'engagementRate']
        dimensions = ['date']
        
        return self.run_report(
            property_id, metrics, dimensions,
            start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
        )
    
    def get_top_cities(self, property_id: str, days: int = 7, limit: int = 10) -> Dict[str, Any]:
        """Get top cities by active users"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.run_report(
            property_id, ['activeUsers'], ['city'],
            start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'),
            order_bys=[{'metric': {'metricName': 'activeUsers'}, 'desc': True}],
            limit=limit
        )
    
    def get_device_breakdown(self, property_id: str, days: int = 7) -> Dict[str, Any]:
        """Get device category breakdown"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.run_report(
            property_id, ['activeUsers', 'sessions'], ['deviceCategory'],
            start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
        )
    
    def get_conversion_funnel(self, property_id: str, days: int = 7) -> Dict[str, Any]:
        """Get conversion funnel data"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        metrics = ['eventCount']
        dimensions = ['eventName']
        
        return self.run_report(
            property_id, metrics, dimensions,
            start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
        )
    
    def get_ecommerce_metrics(self, property_id: str, days: int = 7) -> Dict[str, Any]:
        """Get e-commerce metrics"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        metrics = ['totalRevenue', 'transactions', 'averagePurchaseRevenue', 
                   'itemsViewed', 'itemsAddedToCart', 'itemsPurchased']
        dimensions = ['date']
        
        return self.run_report(
            property_id, metrics, dimensions,
            start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
        )
