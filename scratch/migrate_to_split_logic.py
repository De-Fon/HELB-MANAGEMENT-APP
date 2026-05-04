import os
import re

APPS_DIR = "app/apps"

REPLACEMENTS = {
    # Imports in routes.py and providers.py
    'from app.apps.request_control.dependencies import idempotent, rate_limit': 
        'from app.apps.idempotency.dependencies import idempotent\nfrom app.apps.rate_limiting.dependencies import rate_limit',
    
    'from app.apps.request_control.providers import get_request_control_service':
        'from app.apps.idempotency.providers import get_idempotency_service\nfrom app.apps.rate_limiting.providers import get_rate_limit_service',

    'from app.apps.request_control.providers import get_idempotency_service, get_rate_limit_service':
        'from app.apps.idempotency.providers import get_idempotency_service\nfrom app.apps.rate_limiting.providers import get_rate_limit_service',
    
    'from app.apps.request_control.service import RequestControlService':
        'from app.apps.idempotency.service import IdempotencyService\nfrom app.apps.rate_limiting.service import RateLimitService',

    # Dependency Injection in routes.py
    'rc_service: RequestControlService = Depends(get_request_control_service)':
        'idempotency_service: IdempotencyService = Depends(get_idempotency_service),\n    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)',
}

def migrate_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = content
    for old, new in REPLACEMENTS.items():
        new_content = new_content.replace(old, new)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Migrated: {filepath}")

def main():
    for root, dirs, files in os.walk(APPS_DIR):
        for file in files:
            if file.endswith(".py"):
                migrate_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
