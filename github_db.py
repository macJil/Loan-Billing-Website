import requests
import json
import base64
from datetime import datetime
import os

class GitHubDB:
    def __init__(self):
        # GitHub configuration
        self.repo_owner = os.environ.get('GITHUB_USERNAME', 'your_username')
        self.repo_name = os.environ.get('GITHUB_REPO', 'loan-data')
        self.github_token = os.environ.get('GITHUB_TOKEN', 'your_token')
        self.api_base = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def _get_file_sha(self, filename):
        """Get the SHA of a file if it exists"""
        try:
            response = requests.get(f"{self.api_base}/contents/{filename}", headers=self.headers)
            if response.status_code == 200:
                return response.json()['sha']
            return None
        except:
            return None
    
    def _create_file(self, filename, content, message="Add loan data"):
        """Create or update a file in GitHub"""
        data = {
            'message': message,
            'content': base64.b64encode(content.encode()).decode()
        }
        
        # Check if file exists to get SHA
        sha = self._get_file_sha(filename)
        if sha:
            data['sha'] = sha
        
        response = requests.put(f"{self.api_base}/contents/{filename}", 
                              headers=self.headers, json=data)
        return response.status_code in [200, 201]
    
    def _read_file(self, filename):
        """Read a file from GitHub"""
        try:
            response = requests.get(f"{self.api_base}/contents/{filename}", headers=self.headers)
            if response.status_code == 200:
                content = base64.b64decode(response.json()['content']).decode()
                return json.loads(content)
            return []
        except:
            return []
    
    def get_all_loans(self):
        """Get all loans from GitHub"""
        return self._read_file('loans.json')
    
    def add_loan(self, loan_data):
        """Add a new loan"""
        loans = self.get_all_loans()
        
        # Generate new ID
        if loans:
            new_id = max(loan['id'] for loan in loans) + 1
        else:
            new_id = 1
        
        # Add loan with metadata
        loan_data['id'] = new_id
        loan_data['created_at'] = datetime.now().isoformat()
        loan_data['updated_at'] = datetime.now().isoformat()
        
        loans.append(loan_data)
        
        # Save to GitHub
        content = json.dumps(loans, indent=2)
        success = self._create_file('loans.json', content, f"Add loan: {loan_data['name']}")
        
        return success, new_id
    
    def update_loan(self, loan_id, loan_data):
        """Update an existing loan"""
        loans = self.get_all_loans()
        
        for i, loan in enumerate(loans):
            if loan['id'] == loan_id:
                loan_data['id'] = loan_id
                loan_data['created_at'] = loan['created_at']
                loan_data['updated_at'] = datetime.now().isoformat()
                loans[i] = loan_data
                
                content = json.dumps(loans, indent=2)
                success = self._create_file('loans.json', content, f"Update loan: {loan_data['name']}")
                return success
        
        return False
    
    def delete_loan(self, loan_id):
        """Delete a loan"""
        loans = self.get_all_loans()
        
        for i, loan in enumerate(loans):
            if loan['id'] == loan_id:
                deleted_loan = loans.pop(i)
                content = json.dumps(loans, indent=2)
                success = self._create_file('loans.json', content, f"Delete loan: {deleted_loan['name']}")
                return success
        
        return False
    
    def get_loan_by_id(self, loan_id):
        """Get a specific loan by ID"""
        loans = self.get_all_loans()
        
        for loan in loans:
            if loan['id'] == loan_id:
                return loan
        
        return None
    
    def search_loans(self, query="", status_filter=""):
        """Search loans by query and status"""
        loans = self.get_all_loans()
        
        if query:
            query_lower = query.lower()
            loans = [loan for loan in loans 
                    if query_lower in loan['name'].lower() 
                    or (loan.get('description') and query_lower in loan['description'].lower())]
        
        if status_filter:
            loans = [loan for loan in loans if loan['status'] == status_filter]
        
        return loans

# Global instance
github_db = GitHubDB() 