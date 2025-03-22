import requests
import random
from enum import Enum, auto

class Department(Enum):
    EXECUTIVE_LEADERSHIP = auto()
    OPERATIONS = auto()
    FINANCE_ACCOUNTING = auto()
    HUMAN_RESOURCES = auto()
    LEGAL_COMPLIANCE = auto()
    MARKETING_SALES = auto()
    CUSTOMER_SERVICE_SUPPORT = auto()
    TECHNOLOGY_IT = auto()
    PRODUCT_RD = auto()
    SUPPLY_CHAIN_LOGISTICS = auto()
    OTHER = auto()

class Industry(Enum):
    TECHNOLOGY = auto()
    FINANCE = auto()
    HEALTHCARE = auto()
    MANUFACTURING = auto()
    RETAIL = auto()
    EDUCATION = auto()
    TRANSPORTATION = auto()
    ENERGY = auto()
    ENTERTAINMENT = auto()
    TELECOMMUNICATIONS = auto()
    CONSTRUCTION = auto()
    HOSPITALITY = auto()
    REAL_ESTATE = auto()
    AGRICULTURE = auto()
    PHARMACEUTICALS = auto()
    OTHER = auto()

companies = [
    "Google", "Apple", "Microsoft", "Amazon", "Facebook", "Tesla", "Samsung", "IBM", "Intel", "Oracle",
    "Sony", "Walmart", "Target", "Costco", "Home Depot", "Lowe's", "Best Buy", "Starbucks", "McDonald's", "Coca-Cola",
    "PepsiCo", "Nike", "Adidas", "Disney", "Netflix", "Hulu", "Spotify", "Uber", "Lyft", "Airbnb",
    "General Electric", "Ford", "General Motors", "Toyota", "Honda", "BMW", "Volkswagen", "Mercedes-Benz", "Audi", "Hyundai",
    "Siemens", "Bosch", "Panasonic", "LG", "HP", "Dell", "Lenovo", "Asus", "Acer", "Canon",
    "Nikon", "Sony", "Philips", "SAP", "Adobe", "Salesforce", "VMware", "Cisco", "Qualcomm", "Broadcom",
    "Nvidia", "AMD", "Texas Instruments", "AT&T", "Verizon", "T-Mobile", "Comcast", "Charter", "Dish Network", "Hulu",
    "Spotify", "Pandora", "Slack", "Zoom", "Dropbox", "Evernote", "Trello", "Asana", "GitHub", "GitLab",
    "Bitbucket", "Jira", "Confluence", "Figma", "Sketch", "InVision", "Adobe XD", "Zeplin", "Marvel", "Proto.io",
    "Axure", "Balsamiq", "Miro", "Mural", "Toptal", "Upwork", "Fiverr", "Freelancer", "99designs", "PeoplePerHour"
]

countries = [
    "United States", "Canada", "United Kingdom", "Germany", "France", "Italy", "Spain", "Japan", "China", "South Korea",
    "India", "Brazil", "Mexico", "Australia", "Russia", "Philippines", "Singapore", "Malaysia", "Thailand", "Vietnam"
]

url = "http://localhost:5000/api/companies/add"

def generate_company_data():
    company_name = random.choice(companies)
    company_size = random.randint(50, 100000)
    company_industry = random.choice(list(Industry)).name
    country = random.choice(countries)
    
    return {
        "company_name": company_name,
        "company_size": company_size,
        "company_industry": company_industry,
        "country": country
    }

def add_companies(num_companies):
    for _ in range(num_companies):
        data = generate_company_data()
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print(f"Added company: {data['company_name']}")
        else:
            print(f"Failed to add company: {data['company_name']}")

add_companies(100)