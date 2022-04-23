class Headers:
    @staticmethod
    def get_headers() -> list:
        return [
            "Date",
            "Amount",
            "Type",
            "Transaction ID",
            "Description",
            "Tax Deductible",
            "Category"
        ]


class Tags:
    @staticmethod
    def get_tax_deductible_tags() -> list:
        return ['Business Advertising', 'Business Expense', 'Business Phone', 'Business Software',
                'Business Uniforms', 'Car Payment', 'Car Service', 'Donation', 'Education',
                'Entertainment', 'Food & Dining', 'Gift', 'Medical', "Mortgage Payment",
                'Home Improvement', 'Hotel & Lodging', 'Insurance', 'Investment', 'Moving Expense',
                'Parking', 'Pharmacy', 'Postage & Shipping', 'Rent', 'Savings', 'Shopping', 'Subscription',
                'Transportation Air', 'Transportation Public', 'Transportation Rental', 'Transportation Service',
                'Transportation Train', 'Travel', 'Utilities', "Legal Services"]

    @staticmethod
    def get_all_tags() -> dict:
        return {
            "acorns": "Investment",
            "royal farms": "Gas",
            "taco": "Food",
            "eyez": "Medical",
            "suntrust": "Car Payment",
            "redzone blitz": "Food",
            "instacart": "Groceries",
            "cleaners": "Business Uniforms",
            "matchbox": "Food",
            "exxon": "Gas",
            "restaurant": "Food",
            "safeway": "Groceries",
            "usps": "Postage & Shipping",
            "food lion": "Groceries",
            "whip clean": "Business Uniforms",
            "metro": "Transportation Public",
            "gates hudson": "Rent",
            "ascend apollo": "Rent",
            "USAA P&C": "Insurance",
            "tight n up": "Haircut",
            "kfc": "Food",
            "dd/br": "Food",
            "heroku": "Business Advertising",
            "google fi": "Business Phone",
            "google apps": "Business Software",
            "zipcar": "Transportation Rental",
            "grill": "Food",
            "popeyes": "Fast Food",
            "fedex": "Postage & Shipping",
            "uber": "Transportation Service",
            "lyft": "Transportation Service",
            "mcdonald": "Food",
            "dunkin": "Food",
            "amtrak": "Transportation Train",
            "rite aid": "Pharmacy",
            "vre": "Transportation Train",
            "cox": "Business Expense",
            "winn dixie": "Groceries",
            "marathon": "Gas",
            "spotify": "Subscription",
            "peabodys": "Food and Dining",
            "grand prix": "Entertainment",
            "budget": "Transportation Rental",
            "seafood": "Food & Dining",
            "speedway": "Gas",
            "digit": "Savings",
            "cigar": "Entertainment",
            "roadhouse": "Food & Dining",
            "eleven": "Misc",
            "stash": "Savings",
            "grubhub": "Food & Dining",
            "sunoco": "Misc",
            "potomac": "Utilities",
            "fuel": "Gas",
            "amazon prime": "Subscription",
            "five guys": "Fast Food",
            "shell oil": "Gas",
            "haagen": "Fast Food",
            "citi": "Credit Card",
            "julia": "Gift",
            "discover": "Credit Card",
            "shoppers": "Groceries",
            "liquor": "Misc",
            "GoFndMe": "Donation",
            "pizza": "Food & Dining",
            "sling": "Utilities",
            "uszoom": "Postage & Shipping",
            "snack": "Food & Dining",
            "zelle": "Gift",
            "pro wash": "Car Service",
            "chase": "Credit Card",
            "ups store": "Postage & Shipping",
            "ruby tuesday": "Food & Dining",
            "amzn mktp": "Misc",
            "amzn.com": "Misc",
            "comcast": "Utilities",
            "taste": "Food & Dining",
            "venmo": "Gift",
            "transferwise": "Savings",
            "home depot": "Home Improvement",
            "united": "Transportation Air",
            "puyallu": "Gift",
            "walmart": "Misc",
            "qdoba": "Food & Dining",
            "toyota": "Car Service",
            "marc": "Transportation Train",
            "alaska air": "Transportation Air",
            "walgreens": "Pharmacy",
            "food": "Food & Dining",
            "va abc": "Misc",
            "oyster": "Food & Dining",
            "oxon hill": "Entertainment",
            "garage": "Parking",
            "clini": "Medical",
            "lounge": "Alcohol & Bars",
            "wendys": "Fast Food",
            "ftd": "Gift",
            "robinhood": "Investment",
            "target": "Shopping",
            "wine": "Alcohol & Bars",
            "publix": "Groceries",
            "car wash": "Car Service",
            "american air": "Transportation Air",
            "auto parts": "Car Service",
            "synchrony": "Credit Card",
            "ethiopi": "Food & Dining",
            "longhorn": "Food & Dining",
            "ivy city": "Misc",
            "zippy": "Moving Expense",
            "ourisman": "Car Service",
            "groupon": "Gift",
            "lowes": "Home Improvement",
            "carolina kitchen": "Food & Dining",
            "parking": "Parking",
            "stogie": "Alcohol & Bars",
            "washington gas": "Utilities",
            "improv": "Entertainment",
            "lucky strike": "Entertainment",
            "dirty habit": "Alcohol & Bars",
            "decades": "Entertainment",
            "pharm": "Pharmacy",
            "CHRYSLER": "Car Service",
            "paypal inst xfer": "Misc",
            "office depot": "Business Expense",
            "car was": "Car Service",
            "xfinity": "Utilities",
            "donate": "Donation",
            "wayfair": "Home Improvement",
            "couchsurfing": "Hotel & Lodging",
            "famvibe": "Gift",
            "coffe": "Fast Food",
            "shang hai": "Food & Dining",
            "dhsmv": "Car Service",
            "noodles": "Food & Dining",
            "spirit air": "Transportation Air",
            "ggc": "Entertainment",
            "mandu": "Food & Dining",
            "m street": "Entertainment",
            "yardi": "Rent",
            "rewind": "Food & Dining",
            "the smith": "Food & Dining",
            "etsy": "Misc",
            "new meaning": "Clothing",
            "calm": "Medical",
            "lasani": "Food & Dining",
            "expression tees": "Clothing",
            "bozzelli": "Food & Dining",
            "clothing": "Clothing",
            "allianz": "Travel",
            "fashion": "Clothing",
            "boredwalk": "Clothing",
            "blissy": "Home Improvement",
            "deli": "Food & Dining",
            "moxy": "Entertainment",
            "sugarcane": "Food & Dining",
            "flight deck": "Entertainment",
            "station 4": "Food & Dining",
            "testing": "Education",
            "chipotle": "Food & Dining",
            "edible arrangements": "Gift",
            "fl dept": "Business Expense",
            "florida dept": "Business Expense",
            "notarize": "Business Expense",
            "jimmy johns": "Fast Food",
            "shirt": "Clothing",
            "forman mills": "Clothing",
            "secure finger": "Business Expense",
            "las vegas": "Entertainment",
            "fort belvoir": "Groceries",
            "cafe": "Food & Dining",
            "pusserslanding": "Food & Dining",
            "market basket": "Food & Dining",
            "golf": "Entertainment",
            "javed iqbal": "Medical",
            "jomashop": "Gift",
            "xi an ao peng": "Clothing",
            "speed deals": "Clothing",
            "the grove": "Misc",
            "crain mitchell": "Misc",
            "bowie bowie": "Misc",
            "stevie p": "Misc",
            "JBM": "Misc",
            "flyer": "Misc",
            "hotel": "Hotel & Lodging",
            "aircanada": "Transportation Air",
            "hopper": "Transportation Air",
            "delta": "Transportation Air",
            "jetblue": "Transportation Air",
            "doordash": "Food",
            "pack-rat": "Moving Expense",
            "wellex": "Medical",
            "agoda": "Hotel & Lodging",
            "marriott": "Hotel & Lodging",
            "legal": "Legal Services",
            "law firm": "Legal Services",
            "GARY M GILBERT": "Legal Services",
            "southwes": "Transportation Air",
            "best buy": "Business Expense",
            "apple.com": "Business Expense",
            "homedepot.com": "Home Improvement",
            "carpets": "Home Improvement",
            "gift": "Gift",
            "ANNUAL MEMBERSHIP FEE": "Business Expense",
            "UA INFLT": "Transportation Air",
            "HARBOR FREIGHT": "Home Improvement",
            "MCMASTER-CARR": "Home Improvement",
            "HUBITAT": "Home Improvement",
            "u haul": "Moving Expense",
            "resort": "Hotel & Lodging",
            "appraisal fee": "Home Improvement",
            "getitdone": "Home Improvement",
            "etags": "Transportation Service",
            "hilton": "Hotel & Lodging",
            "vrbo": "Hotel & Lodging",
            "jewel box": "Gift",
            "TRIPINSURA": "Travel",
            "Porsche": "Gift",
            "TOPBACHELOR": "Hotel & Lodging",
            "TURNKEY": "Hotel & Lodging"
        }

