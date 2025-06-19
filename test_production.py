#!/usr/bin/env python3
"""
Production Readiness Test Suite
Tests all critical functionality before deployment
"""

import sys
import traceback
import importlib.util

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    
    required_modules = [
        'streamlit',
        'yfinance', 
        'pandas',
        'numpy',
        'pytz',
        'ta',
        'psutil',
        'json',
        'os',
        'logging',
        'time',
        'datetime'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            if module in ['json', 'os', 'logging', 'time', 'datetime']:
                # Built-in modules
                __import__(module)
            else:
                # External modules
                importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0, failed_imports

def test_file_structure():
    """Test required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'working1.py',
        'stock_names.json',
        'requirements.txt',
        'Dockerfile',
        'runtime.txt'
    ]
    
    missing_files = []
    
    import os
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0, missing_files

def test_syntax():
    """Test Python syntax"""
    print("\n🐍 Testing Python syntax...")
    
    try:
        with open('working1.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, 'working1.py', 'exec')
        print("  ✅ working1.py syntax is valid")
        return True, None
    except SyntaxError as e:
        print(f"  ❌ Syntax error in working1.py: {e}")
        return False, str(e)
    except Exception as e:
        print(f"  ❌ Error reading working1.py: {e}")
        return False, str(e)

def test_json_format():
    """Test JSON file format"""
    print("\n📋 Testing JSON format...")
    
    try:
        import json
        with open('stock_names.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, dict) and len(data) > 0:
            print(f"  ✅ stock_names.json is valid ({len(data)} stocks)")
            return True, None
        else:
            print("  ❌ stock_names.json is empty or invalid format")
            return False, "Empty or invalid format"
    except Exception as e:
        print(f"  ❌ Error reading stock_names.json: {e}")
        return False, str(e)

def test_streamlit_config():
    """Test Streamlit configuration"""
    print("\n⚙️ Testing Streamlit configuration...")
    
    try:
        # Check if working1.py has proper st.set_page_config
        with open('working1.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'st.set_page_config' in content:
            print("  ✅ Streamlit page config found")
        else:
            print("  ⚠️ No Streamlit page config found")
        
        if '@st.cache_data' in content:
            print("  ✅ Caching decorators found")
        else:
            print("  ⚠️ No caching decorators found")
        
        return True, None
    except Exception as e:
        print(f"  ❌ Error checking Streamlit config: {e}")
        return False, str(e)

def main():
    """Run all tests"""
    print("🚀 Production Readiness Test Suite")
    print("="*50)
    
    all_passed = True
    failed_tests = []
    
    # Run tests
    tests = [
        ("Imports", test_imports),
        ("File Structure", test_file_structure), 
        ("Python Syntax", test_syntax),
        ("JSON Format", test_json_format),
        ("Streamlit Config", test_streamlit_config)
    ]
    
    for test_name, test_func in tests:
        try:
            passed, error = test_func()
            if not passed:
                all_passed = False
                failed_tests.append((test_name, error))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            all_passed = False
            failed_tests.append((test_name, f"Test crashed: {e}"))
    
    # Summary
    print("\n" + "="*50)
    if all_passed:
        print("🎉 ALL TESTS PASSED - Ready for Production!")
        print("\n✅ Your application is production-ready")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print(f"\n⚠️ {len(failed_tests)} issues found:")
        for test_name, error in failed_tests:
            print(f"  • {test_name}: {error}")
        print("\n🔧 Fix these issues before deploying")
        return 1

if __name__ == "__main__":
    sys.exit(main())
