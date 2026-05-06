#!/usr/bin/env python3
"""
Script to remove rate_limit_service from all service and provider files.
"""
import re
import os

# List of service files to update
service_files = [
    'app/apps/counselling/service.py',
    'app/apps/feedback/service.py',
    'app/apps/withdrawal_limit/service.py',
    'app/apps/lending_borrowing/service.py',
    'app/apps/scholarship_tracker/service.py',
    'app/apps/subscription_manager/service.py',
    'app/apps/emergency_fund/service.py',
    'app/apps/expense_splitter/service.py',
    'app/apps/mpesa_integration/service.py',
    'app/apps/offline_sync/service.py',
    'app/apps/expenditure_analytics/service.py',
    'app/apps/budget_tracker/service.py',
    'app/apps/auth/service.py',
]

provider_files = [
    'app/apps/counselling/providers.py',
    'app/apps/feedback/providers.py',
    'app/apps/withdrawal_limit/providers.py',
    'app/apps/lending_borrowing/providers.py',
    'app/apps/scholarship_tracker/providers.py',
    'app/apps/subscription_manager/providers.py',
    'app/apps/emergency_fund/providers.py',
    'app/apps/expense_splitter/providers.py',
    'app/apps/mpesa_integration/providers.py',
    'app/apps/offline_sync/providers.py',
    'app/apps/expenditure_analytics/providers.py',
    'app/apps/budget_tracker/providers.py',
    'app/apps/auth/providers.py',
]

def remove_rate_limit_from_init(content):
    """Remove rate_limit_service parameter from __init__ method."""
    # Pattern to match the rate_limit_service line
    pattern = r',\s*rate_limit_service=None\n'
    content = re.sub(pattern, '\n', content)
    
    pattern = r'\s*self\.rate_limit_service = rate_limit_service\n'
    content = re.sub(pattern, '', content)
    
    return content

def remove_rate_limit_from_providers(content):
    """Remove rate_limit_service and related imports from provider files."""
    # Remove import line
    content = re.sub(r'from app\.apps\.rate_limiting\.providers import get_rate_limit_service\n', '', content)
    
    # Remove rate_limit_service parameter
    pattern = r',\s*rate_limit_service = Depends\(get_rate_limit_service, use_cache=True\)\n'
    content = re.sub(pattern, '\n', content)
    
    # Remove rate_limit_service argument to service constructor
    pattern = r',\s*rate_limit_service=rate_limit_service\n'
    content = re.sub(pattern, '\n', content)
    
    return content

# Process service files
for filepath in service_files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        content = remove_rate_limit_from_init(content)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f'✓ Updated {filepath}')

# Process provider files
for filepath in provider_files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        content = remove_rate_limit_from_providers(content)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f'✓ Updated {filepath}')

print('\nDone!')
