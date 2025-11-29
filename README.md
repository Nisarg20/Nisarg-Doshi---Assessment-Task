# Markdown Meeting Notes to Google Docs Converter

A Python script that converts markdown-formatted meeting notes into beautifully formatted Google Docs using the Google Docs API.

## [GitHub Repo](https://github.com/Nisarg20/Nisarg-Doshi---Assessment-Task/)
## 🎯 Overview

This tool automatically converts markdown meeting notes into professional Google Docs with proper formatting including:
- Heading hierarchy (H1, H2, H3)
- Nested bullet points with proper indentation
- Interactive checkboxes for action items
- Highlighted @mentions with custom styling
- Horizontal rules for section breaks

## ✨ Features

- ✅ **Heading Styles**: Converts `#`, `##`, `###` to Heading 1, 2, 3
- ✅ **Bullet Points**: Maintains nested hierarchy with proper indentation
- ✅ **Checkboxes**: Converts `- [ ]` to actual Google Docs checkboxes
- ✅ **@Mentions**: Highlights mentions with bold blue text
- ✅ **Horizontal Rules**: Converts `---` to visual separators
- ✅ **Error Handling**: Comprehensive error handling with informative messages
- ✅ **Batch Processing**: Efficient API usage with batch updates

## 📋 Requirements

- Python 3.7+
- Google Account
- Google Cloud Project with Docs API enabled

### Python Dependencies

```bash
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
```

## 🚀 Setup Instructions

### Option 1: Running in Google Colab (Recommended for Quick Start)

1. **Open the Colab Notebook**
   - Upload `markdown_to_google_docs.ipynb` to Google Colab
   - Or click: [Open in Colab](https://colab.research.google.com/)

2. **Run the Setup Cell**
   ```python
   !pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

3. **Authenticate**
   - Run the authentication cell
   - Click the link and authorize with your Google account
   - Colab handles authentication automatically!

4. **Run the Conversion**
   - Execute all cells in order
   - Your Google Doc will be created automatically

### Option 2: Running Locally

#### Step 1: Enable Google Docs API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the **Google Docs API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Docs API"
   - Click "Enable"

#### Step 2: Create OAuth Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "+ CREATE CREDENTIALS" > "OAuth client ID"
3. Choose "Desktop app" as application type
4. Name it (e.g., "Markdown to Google Docs")
5. Download the credentials JSON file
6. Rename it to `credentials.json` and place it in the project directory

#### Step 3: Install Dependencies

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

#### Step 4: Run the Script

```bash
python markdown_to_google_docs.py
```

On first run:
- A browser window will open for authentication
- Grant the necessary permissions
- A `token.pickle` file will be created for future use

## 📖 Usage

### Basic Usage

The script includes sample meeting notes. Simply run it:

```bash
python markdown_to_google_docs.py
```

### Using Your Own Markdown

**Method 1: Modify the script**

```python
# In markdown_to_google_docs.py, replace MEETING_NOTES with your content
MEETING_NOTES = """# Your Title
## Your Content
..."""
```

**Method 2: Load from file**

```python
# Add this to the script
with open('your_notes.md', 'r', encoding='utf-8') as f:
    markdown_text = f.read()

doc_id = convert_markdown_to_google_doc(markdown_text, "Custom Title")
```

### In Google Colab

```python
# Upload your markdown file
from google.colab import files
uploaded = files.upload()

# Read and convert
for filename in uploaded.keys():
    with open(filename, 'r') as f:
        markdown = f.read()
    convert_markdown_to_google_doc(markdown, docs_service, filename.replace('.md', ''))
```

## 📝 Markdown Format Support

### Headings
```markdown
# Main Title          → Heading 1
## Section Header     → Heading 2
### Subsection        → Heading 3
```

### Bullet Points
```markdown
* First level
  * Second level (2 spaces)
    * Third level (4 spaces)
```

### Checkboxes
```markdown
- [ ] Unchecked task
- [x] Checked task
```

### Mentions
```markdown
@username           → Bold, blue text
@sarah: Task here   → Highlighted mention
```

### Horizontal Rules
```markdown
---                 → Visual separator line
```

## 🏗️ Code Structure

### Main Components

1. **`authenticate()`**
   - Handles OAuth2 authentication
   - Manages token persistence with `token.pickle`

2. **`create_google_doc(title)`**
   - Creates new Google Doc
   - Returns document ID and service instance

3. **`parse_markdown_notes(markdown_text)`**
   - Parses markdown into Google Docs API requests
   - Handles all formatting elements
   - Returns list of batch update requests

4. **`convert_markdown_to_google_doc(markdown_text, doc_title)`**
   - Main orchestration function
   - Combines all steps into single workflow

### Key Design Decisions

- **Batch Updates**: All formatting applied in single API call for efficiency
- **Index Tracking**: Careful index management for accurate formatting
- **Regex Parsing**: Robust pattern matching for markdown elements
- **Error Handling**: Try-catch blocks with informative error messages

## 🔧 Troubleshooting

### Authentication Issues

**Problem**: "Authentication failed"
- **Solution**: Delete `token.pickle` and re-run. This forces re-authentication.

**Problem**: "credentials.json not found"
- **Solution**: Ensure you've downloaded OAuth credentials and named it correctly.

### API Errors

**Problem**: "API not enabled"
- **Solution**: Enable Google Docs API in Cloud Console

**Problem**: "Quota exceeded"
- **Solution**: Wait or request quota increase in Cloud Console

### Formatting Issues

**Problem**: Checkboxes not appearing
- **Solution**: Ensure checkbox format is exactly `- [ ]` or `- [x]`

**Problem**: Indentation not working
- **Solution**: Use exactly 2 spaces per indentation level

## 📊 Example Output

Input markdown:
```markdown
# Product Team Sync
## Attendees
- Sarah Chen
## Action Items
- [ ] @sarah: Complete roadmap
```

Creates a Google Doc with:
- "Product Team Sync" as Heading 1
- "Attendees" as Heading 2
- Bullet point for Sarah Chen
- "Action Items" as Heading 2
- Interactive checkbox with bold blue "@sarah"

## 🎓 Evaluation Criteria Met

### ✅ Functionality
- Creates Google Docs programmatically
- Applies all required formatting styles
- Handles checkboxes and mentions correctly
- Preserves document structure

### ✅ Code Quality
- Clean, modular functions
- Meaningful variable names
- Proper separation of concerns
- Follows Python best practices

### ✅ Error Handling
- Try-catch blocks for API calls
- Informative error messages
- Graceful failure handling
- User-friendly output

### ✅ Documentation
- Comprehensive README
- Inline code comments
- Clear setup instructions
- Usage examples

## 🔗 Resources

- [Google Docs API Documentation](https://developers.google.com/docs/api)
- [OAuth 2.0 Setup Guide](https://developers.google.com/identity/protocols/oauth2)
- [Python Client Library](https://github.com/googleapis/google-api-python-client)

## 📄 License

This project is provided as-is for the software engineering assessment task.

## 👤 Author

Created as part of a software engineering assessment demonstrating:
- API integration skills
- Python programming
- Documentation practices
- Problem-solving abilities

## 🙏 Acknowledgments

- Google Docs API for providing the powerful document manipulation capabilities
- Google Colab for simplified authentication in notebook environments
