import os

from .config import DevelopmentConfig, ProductionConfig

if os.getenv('TRAIL_ENV') in ['dev', 'development']:
    libconfig = DevelopmentConfig
    print('dev db')
else:
    libconfig = ProductionConfig
    print('prod db')
