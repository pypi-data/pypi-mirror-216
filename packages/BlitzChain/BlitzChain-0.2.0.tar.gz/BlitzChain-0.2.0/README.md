# Blitzchain


Retrieval-Augmented Generation For Powerful Results

## Installation

```
pip install -e git+https://github.com/mr-gpt/blitzchain.git#egg=blitzchain
```

Once you install, you can get your API key from https://app.twilix.io/

If you would like to then use this for your solutions, we recommend the following: 

## QuickStart

```python
import blitzchain

# Get API key from https://app.twilix.io
client = blitzchain.Client(api_key="XYZ")
collection = client.Collection()

# sample documents
handbook_example_1 = {
    "section": "Introduction",
    "content": "Welcome to ABC Corporation! This employee handbook provides you with important information about our company policies and procedures."
}

handbook_example_2 = {
    "section": "Employment",
    "content": "At ABC Corporation, we believe in equal opportunity employment. We hire based on qualifications, skills, and experience, without discrimination on the basis of race, gender, religion, or any other protected status."
}

handbook_example_3 = {
    "section": "Code of Conduct",
    "content": "We expect all employees to conduct themselves professionally and ethically at all times. Treat colleagues, customers, and partners with respect and courtesy."
}

handbook_example_4 = {
    "section": "Work Hours",
    "content": "Our regular work hours are from 9:00 AM to 5:00 PM, Monday to Friday. Be punctual and adhere to your assigned schedule. Notify your supervisor in advance for any planned time off."
}

handbook_example_5 = {
    "section": "Dress Code",
    "content": "We maintain a business casual dress code. Dress appropriately for your role, maintaining a clean and professional appearance."
}

handbook_example_6 = {
    "section": "Confidentiality",
    "content": "As an employee of ABC Corporation, you may come across confidential information. Safeguard and maintain the confidentiality of such information, both during and after your employment."
}

handbook_example_7 = {
    "section": "Performance Reviews",
    "content": "We conduct regular performance reviews to provide feedback and evaluate your work. This process helps identify areas of improvement and recognize outstanding performance."
}

handbook_example_8 = {
    "section": "Leave and Time Off",
    "content": "We offer various types of leave, including vacation, sick leave, and parental leave. Familiarize yourself with the procedures and guidelines outlined in our leave policy."
}

handbook_example_9 = {
    "section": "Technology Usage",
    "content": "Use company-provided technology resources responsibly and solely for work-related purposes. Follow our IT policies and guidelines to ensure the security and integrity of our systems."
}

handbook_example_10 = {
    "section": "Termination",
    "content": "In the event of termination, return all company property and ensure a smooth transition of responsibilities. Follow the procedures outlined in our termination policy."
}

objects = [
    handbook_example_1,
    handbook_example_2,
    handbook_example_3,
    handbook_example_4,
    handbook_example_5,
    handbook_example_6,
    handbook_example_7,
    handbook_example_8,
    handbook_example_9
]

collection.insert_objects(docs)

```

## Retrieving RAG Results

```python
collection.generative_qa(
    user_input="Why?",
    answer_fields=["content"],
)
```

# Documentation

If you would like to read more about how to use this - 
we recommend visiting [https://docs.twilix.io](https://docs.twilix.io)
