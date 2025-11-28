"""
Markdown Meeting Notes to Google Docs Converter

This script converts markdown-formatted meeting notes into a well-formatted Google Doc
using the Google Docs API. It handles various formatting elements including headings,
bullet points, checkboxes, and mentions.
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import pickle
import re

# Define the scopes for Google Docs API
SCOPES = ['https://www.googleapis.com/auth/documents']

def authenticate():
    """
    Authenticate with Google Docs API using OAuth2.
    Returns authenticated credentials.
    """
    creds = None
    
    # Check if token.pickle exists (saved credentials)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If credentials are invalid or don't exist, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def create_google_doc(title):
    """
    Create a new Google Doc and return its ID.
    """
    try:
        creds = authenticate()
        service = build('docs', 'v1', credentials=creds)
        
        document = service.documents().create(body={'title': title}).execute()
        doc_id = document.get('documentId')
        
        print(f"Created document with ID: {doc_id}")
        print(f"View at: https://docs.google.com/document/d/{doc_id}/edit")
        
        return doc_id, service
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None, None

def parse_markdown_notes(markdown_text):
    """
    Parse markdown text and generate Google Docs API requests.
    Returns a list of requests to batch update the document.
    """
    requests = []
    index = 1  # Start after the title
    
    lines = markdown_text.strip().split('\n')
    
    for i, line in enumerate(lines):
        if not line.strip():
            # Skip empty lines but add a paragraph break
            continue
        
        # Main title (# heading)
        if line.startswith('# '):
            text = line[2:].strip()
            requests.append({
                'insertText': {
                    'location': {'index': index},
                    'text': text + '\n'
                }
            })
            # Apply Heading 1 style
            requests.append({
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': index,
                        'endIndex': index + len(text) + 1
                    },
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_1'
                    },
                    'fields': 'namedStyleType'
                }
            })
            index += len(text) + 1
        
        # Section headers (## heading)
        elif line.startswith('## '):
            text = line[3:].strip()
            requests.append({
                'insertText': {
                    'location': {'index': index},
                    'text': text + '\n'
                }
            })
            # Apply Heading 2 style
            requests.append({
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': index,
                        'endIndex': index + len(text) + 1
                    },
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_2'
                    },
                    'fields': 'namedStyleType'
                }
            })
            index += len(text) + 1
        
        # Sub-section headers (### heading)
        elif line.startswith('### '):
            text = line[4:].strip()
            requests.append({
                'insertText': {
                    'location': {'index': index},
                    'text': text + '\n'
                }
            })
            # Apply Heading 3 style
            requests.append({
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': index,
                        'endIndex': index + len(text) + 1
                    },
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_3'
                    },
                    'fields': 'namedStyleType'
                }
            })
            index += len(text) + 1
        
        # Horizontal rule
        elif line.strip() == '---':
            # Insert a horizontal line using special characters
            requests.append({
                'insertText': {
                    'location': {'index': index},
                    'text': '─' * 50 + '\n'
                }
            })
            index += 51
        
        # Checkbox items (- [ ] or - [x])
        elif re.match(r'^-\s*\[([ x])\]', line):
            match = re.match(r'^-\s*\[([ x])\]\s*(.+)', line)
            if match:
                is_checked = match.group(1) == 'x'
                text = match.group(2).strip()
                
                # Handle @mentions
                mention_pattern = r'@(\w+)'
                mentions = re.findall(mention_pattern, text)
                
                # Insert the text
                requests.append({
                    'insertText': {
                        'location': {'index': index},
                        'text': text + '\n'
                    }
                })
                
                # Create a checkbox
                requests.append({
                    'createParagraphBullets': {
                        'range': {
                            'startIndex': index,
                            'endIndex': index + len(text) + 1
                        },
                        'bulletPreset': 'BULLET_CHECKBOX'
                    }
                })
                
                # Apply bold formatting to @mentions
                if mentions:
                    for mention in mentions:
                        mention_text = f'@{mention}'
                        mention_start = text.find(mention_text)
                        if mention_start != -1:
                            requests.append({
                                'updateTextStyle': {
                                    'range': {
                                        'startIndex': index + mention_start,
                                        'endIndex': index + mention_start + len(mention_text)
                                    },
                                    'textStyle': {
                                        'bold': True,
                                        'foregroundColor': {
                                            'color': {
                                                'rgbColor': {
                                                    'red': 0.2,
                                                    'green': 0.4,
                                                    'blue': 0.8
                                                }
                                            }
                                        }
                                    },
                                    'fields': 'bold,foregroundColor'
                                }
                            })
                
                index += len(text) + 1
        
        # Regular bullet points (* or -)
        elif re.match(r'^[\s]*[\*-]\s+', line):
            # Count indentation level based on leading spaces
            leading_spaces = len(line) - len(line.lstrip())
            indent_level = leading_spaces // 2
            
            # Remove leading spaces and bullet marker
            text = re.sub(r'^[\*-]\s+', '', line.lstrip()).strip()
            
            requests.append({
                'insertText': {
                    'location': {'index': index},
                    'text': text + '\n'
                }
            })
            
            # Apply bullet formatting
            requests.append({
                'createParagraphBullets': {
                    'range': {
                        'startIndex': index,
                        'endIndex': index + len(text) + 1
                    },
                    'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                }
            })
            
            # Apply indentation if needed
            if indent_level > 0:
                requests.append({
                    'updateParagraphStyle': {
                        'range': {
                            'startIndex': index,
                            'endIndex': index + len(text) + 1
                        },
                        'paragraphStyle': {
                            'indentStart': {
                                'magnitude': 36 * indent_level,
                                'unit': 'PT'
                            }
                        },
                        'fields': 'indentStart'
                    }
                })
            
            index += len(text) + 1
        
        # Regular text
        else:
            text = line.strip()
            if text:
                requests.append({
                    'insertText': {
                        'location': {'index': index},
                        'text': text + '\n'
                    }
                })
                index += len(text) + 1
    
    return requests

def convert_markdown_to_google_doc(markdown_text, doc_title="Product Team Sync"):
    """
    Main function to convert markdown text to a Google Doc.
    """
    try:
        # Create a new Google Doc
        doc_id, service = create_google_doc(doc_title)
        
        if not doc_id or not service:
            print("Failed to create document")
            return None
        
        # Parse markdown and generate requests
        requests = parse_markdown_notes(markdown_text)
        
        if requests:
            # Batch update the document
            result = service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"\nDocument updated successfully!")
            print(f"Total updates: {len(requests)}")
        
        return doc_id
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

# Sample markdown meeting notes
MEETING_NOTES = """# Product Team Sync - May 15, 2023
## Attendees
- Sarah Chen (Product Lead)
- Mike Johnson (Engineering)
- Anna Smith (Design)
- David Park (QA)
## Agenda
### 1. Sprint Review
* Completed Features
  * User authentication flow
  * Dashboard redesign
  * Performance optimization
    * Reduced load time by 40%
    * Implemented caching solution
* Pending Items
  * Mobile responsive fixes
  * Beta testing feedback integration
### 2. Current Challenges
* Resource constraints in QA team
* Third-party API integration delays
* User feedback on new UI
  * Navigation confusion
  * Color contrast issues
### 3. Next Sprint Planning
* Priority Features
  * Payment gateway integration
  * User profile enhancement
  * Analytics dashboard
* Technical Debt
  * Code refactoring
  * Documentation updates
## Action Items
- [ ] @sarah: Finalize Q3 roadmap by Friday
- [ ] @mike: Schedule technical review for payment integration
- [ ] @anna: Share updated design system documentation
- [ ] @david: Prepare QA resource allocation proposal
## Next Steps
* Schedule individual team reviews
* Update sprint board
* Share meeting summary with stakeholders
## Notes
* Next sync scheduled for May 22, 2023
* Platform demo for stakeholders on May 25
* Remember to update JIRA tickets
---
Meeting recorded by: Sarah Chen
Duration: 45 minutes"""

if __name__ == "__main__":
    print("=" * 60)
    print("Markdown to Google Docs Converter")
    print("=" * 60)
    print("\nStarting conversion process...\n")
    
    doc_id = convert_markdown_to_google_doc(MEETING_NOTES)
    
    if doc_id:
        print("\n" + "=" * 60)
        print("Conversion completed successfully!")
        print(f"Document URL: https://docs.google.com/document/d/{doc_id}/edit")
        print("=" * 60)
    else:
        print("\nConversion failed. Please check the errors above.")
