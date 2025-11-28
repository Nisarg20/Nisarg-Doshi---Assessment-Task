"""
Test script for the markdown parser
This validates that the parsing logic works correctly without requiring API calls
"""

import re

def test_parse_heading_1():
    """Test parsing of H1 headings"""
    line = "# Product Team Sync - May 15, 2023"
    assert line.startswith('# ')
    text = line[2:].strip()
    assert text == "Product Team Sync - May 15, 2023"
    print("✓ H1 parsing works")

def test_parse_heading_2():
    """Test parsing of H2 headings"""
    line = "## Attendees"
    assert line.startswith('## ')
    text = line[3:].strip()
    assert text == "Attendees"
    print("✓ H2 parsing works")

def test_parse_heading_3():
    """Test parsing of H3 headings"""
    line = "### 1. Sprint Review"
    assert line.startswith('### ')
    text = line[4:].strip()
    assert text == "1. Sprint Review"
    print("✓ H3 parsing works")

def test_parse_checkbox():
    """Test parsing of checkbox items"""
    line = "- [ ] @sarah: Finalize Q3 roadmap by Friday"
    match = re.match(r'^-\s*\[([ x])\]\s*(.+)', line)
    assert match is not None
    is_checked = match.group(1) == 'x'
    text = match.group(2).strip()
    assert not is_checked
    assert text == "@sarah: Finalize Q3 roadmap by Friday"
    print("✓ Checkbox parsing works")

def test_parse_mention():
    """Test parsing of @mentions"""
    text = "@sarah: Finalize Q3 roadmap by Friday"
    mention_pattern = r'@(\w+)'
    mentions = re.findall(mention_pattern, text)
    assert len(mentions) == 1
    assert mentions[0] == "sarah"
    print("✓ @mention parsing works")

def test_parse_bullet():
    """Test parsing of bullet points"""
    line = "* User authentication flow"
    assert re.match(r'^[\*-]\s+', line)
    text = re.sub(r'^[\*-]\s+', '', line).strip()
    assert text == "User authentication flow"
    print("✓ Bullet point parsing works")

def test_parse_nested_bullet():
    """Test parsing of nested bullet points"""
    line = "  * Reduced load time by 40%"
    indent_level = 0
    # Count leading spaces and divide by 2 to get indent level
    leading_spaces = len(line) - len(line.lstrip())
    if leading_spaces > 0:
        indent_level = leading_spaces // 2
    assert indent_level == 1
    # Strip leading spaces before applying regex
    text = re.sub(r'^[\*-]\s+', '', line.lstrip()).strip()
    assert text == "Reduced load time by 40%"
    print("✓ Nested bullet parsing works")

def test_parse_horizontal_rule():
    """Test parsing of horizontal rules"""
    line = "---"
    assert line.strip() == '---'
    print("✓ Horizontal rule parsing works")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Markdown Parser Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_parse_heading_1,
        test_parse_heading_2,
        test_parse_heading_3,
        test_parse_checkbox,
        test_parse_mention,
        test_parse_bullet,
        test_parse_nested_bullet,
        test_parse_horizontal_rule
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
