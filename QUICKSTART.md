# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### For Google Colab Users (Easiest!)

1. **Open the notebook**
   - Upload `markdown_to_google_docs.ipynb` to [Google Colab](https://colab.research.google.com/)

2. **Run all cells** (Runtime → Run all)
   - Install dependencies
   - Authenticate (one click!)
   - See your Google Doc created

3. **Done!** 🎉
   - Click the generated link to view your document

### For Local Users

1. **Get Google Credentials**
   ```
   - Go to console.cloud.google.com
   - Enable Google Docs API
   - Create OAuth credentials
   - Download as credentials.json
   ```

2. **Install & Run**
   ```bash
   pip install -r requirements.txt
   python markdown_to_google_docs.py
   ```

3. **Authenticate**
   - Browser opens automatically
   - Grant permissions
   - Done!

## 📝 Test It Out

The script includes sample meeting notes. Just run it to see the magic happen!

## 🎯 What Gets Created

Your markdown meeting notes transform into a professional Google Doc with:

- ✨ Proper heading hierarchy
- ✨ Nested bullet points
- ✨ Interactive checkboxes
- ✨ Highlighted @mentions
- ✨ Clean formatting

## ❓ Need Help?

Check the full README.md for:
- Detailed setup instructions
- Troubleshooting tips
- API documentation links
- Code structure explanation

## 🔧 Common Issues

**"credentials.json not found"**
→ Download OAuth credentials from Google Cloud Console

**"API not enabled"**
→ Enable Google Docs API in your project

**"Authentication failed"**
→ Delete token.pickle and try again

## 📚 Next Steps

1. ✅ Run the sample
2. ✅ Try your own markdown
3. ✅ Customize the styling
4. ✅ Automate your workflow!

Happy converting! 🎊
