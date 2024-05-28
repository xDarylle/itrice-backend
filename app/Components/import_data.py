from app.Models import Production
from datetime import datetime

def import_data(date, irrigated, rainfeed, seed_type):
    production = Production(
        irrigated=irrigated, 
        rainfeed=rainfeed, 
        seedType=seed_type,
        dateCreated=datetime.strptime(date, "%B %d %Y")
    )
    
    production.create()