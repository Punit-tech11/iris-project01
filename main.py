#!/usr/bin/env python3
"""
Iris Crop Prediction System - Setup Script
This script sets up the entire project environment.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, description):
    """Run a shell command with description"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_project_structure():
    """Create necessary directories"""
    directories = ['models', 'static', 'templates', 'data', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")

def install_requirements():
    """Install Python dependencies"""
    print("📚 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if Path('requirements.txt').exists():
        return run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements")
    else:
        # Install individual packages
        packages = ['flask', 'pandas', 'numpy', 'scikit-learn', 'joblib']
        for package in packages:
            if not run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}"):
                return False
    return True

def create_default_files():
    """Create default configuration files"""
    
    # Create .gitignore
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Models
models/*.pkl

# Logs
logs/*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Data
data/*.csv
data/*.json
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content.strip())
    
    print("📝 Created .gitignore file")
    
    # Create config.json
    config = {
        "app_name": "Iris Crop Prediction System",
        "version": "1.0.0",
        "debug": True,
        "host": "0.0.0.0",
        "port": 5000,
        "models_directory": "models",
        "templates_directory": "templates",
        "static_directory": "static",
        "log_level": "INFO",
        "max_prediction_requests": 1000,
        "rate_limit_window": 3600
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("⚙️ Created config.json file")

def validate_installation():
    """Validate the installation"""
    print("🔍 Validating installation...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        return False
    
    # Test imports
    test_imports = [
        ('flask', 'Flask'),
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('sklearn.ensemble', 'RandomForestRegressor'),
        ('joblib', 'joblib')
    ]
    
    for module, obj in test_imports:
        try:
            if '.' in module:
                parts = module.split('.')
                mod = __import__(module, fromlist=[obj])
            else:
                mod = __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {module}: {e}")
            return False
    
    return True

def run_validation():
    """Run the validation script"""
    if Path('validate.py').exists():
        print("🔍 Running validation script...")
        return run_command(f"{sys.executable} validate.py", "Running validation")
    return True

def main():
    """Main setup function"""
    print("🌸 Iris Crop Prediction System - Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('main.py').exists():
        print("❌ Error: main.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Create project structure
    create_project_structure()
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during requirements installation")
        sys.exit(1)
    
    # Create default files
    create_default_files()
    
    # Validate installation
    if not validate_installation():
        print("❌ Setup failed during validation")
        sys.exit(1)
    
    # Run validation script
    if not run_validation():
        print("❌ Setup failed during final validation")
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n🚀 To start the application:")
    print("   python main.py")
    print("\n📖 For more information, see README.md")
    print("\n🌐 Open your browser and navigate to: http://localhost:5000")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Iris Crop Prediction System - Validation and Error Checking Script
This script validates the project setup and checks for common issues.
"""

import os
import sys
import importlib.util
import subprocess
import json
from pathlib import Path

class ProjectValidator:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        self.successes = []
    
    def log_error(self, message):
        self.errors.append(f"❌ {message}")
        print(f"❌ {message}")
    
    def log_warning(self, message):
        self.warnings.append(f"⚠️  {message}")
        print(f"⚠️  {message}")
    
    def log_success(self, message):
        self.successes.append(f"✅ {message}")
        print(f"✅ {message}")
    
    def check_python_version(self):
        """Check Python version compatibility"""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 7:
            self.log_success(f"Python {version.major}.{version.minor}.{version.micro} is supported")
        else:
            self.log_error("Python 3.7+ is required")
    
    def check_file_structure(self):
        """Check if all required files exist"""
        required_files = [
            'main.py',
            'app.py',
            'requirements.txt',
            'templates/index.html'
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                self.log_success(f"Found {file_path}")
            else:
                self.log_error(f"Missing {file_path}")
    
    def check_dependencies(self):
        """Check if all required packages are installed"""
        required_packages = [
            'flask',
            'pandas',
            'numpy',
            'scikit-learn',
            'joblib'
        ]
        
        for package in required_packages:
            try:
                spec = importlib.util.find_spec(package)
                if spec is not None:
                    self.log_success(f"{package} is installed")
                else:
                    self.log_error(f"{package} is not installed")
            except ImportError:
                self.log_error(f"{package} is not available")
    
    def check_templates_directory(self):
        """Check templates directory and HTML file"""
        templates_dir = self.project_root / 'templates'
        if templates_dir.exists():
            self.log_success("Templates directory exists")
            
            index_file = templates_dir / 'index.html'
            if index_file.exists():
                self.log_success("index.html template found")
                
                # Check HTML file size and basic structure
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if len(content) > 1000:
                            self.log_success("HTML template appears to be substantial")
                        else:
                            self.log_warning("HTML template seems very short")
                        
                        # Check for essential HTML elements
                        essential_elements = ['<!DOCTYPE html>', '<html', '<head>', '<body>', '</html>']
                        missing_elements = [elem for elem in essential_elements if elem not in content]
                        if not missing_elements:
                            self.log_success("HTML template has essential structure")
                        else:
                            self.log_warning(f"HTML template missing: {missing_elements}")
                            
                except Exception as e:
                    self.log_error(f"Error reading HTML template: {e}")
            else:
                self.log_error("index.html template not found")
        else:
            self.log_error("Templates directory not found")
    
    def check_models_directory(self):
        """Check if models directory can be created"""
        models_dir = self.project_root / 'models'
        try:
            if not models_dir.exists():
                models_dir.mkdir(exist_ok=True)
                self.log_success("Models directory is accessible")
            else:
                self.log_success("Models directory exists")
        except Exception as e:
            self.log_error(f"Cannot create models directory: {e}")
    
    def test_flask_import(self):
        """Test if Flask can be imported and basic functionality"""
        try:
            from flask import Flask
            self.log_success("Flask can be imported")
            
            # Test basic Flask app creation
            app = Flask(__name__)
            if app:
                self.log_success("Basic Flask app can be created")
            else:
                self.log_error("Cannot create Flask app instance")
                \n        except ImportError as e:
            self.log_error(f"Flask import error: {e}")
        except Exception as e:
            self.log_error(f"Flask functionality error: {e}")
    
    def test_ml_imports(self):
        """Test machine learning library imports"""
        ml_packages = {
            'pandas': 'pd',
            'numpy': 'np',
            'sklearn.ensemble': 'RandomForestRegressor',
            'sklearn.preprocessing': 'StandardScaler, LabelEncoder',
            'joblib': 'joblib'
        }
        
        for package, imports in ml_packages.items():
            try:
                if package == 'sklearn.ensemble':
                    from sklearn.ensemble import RandomForestRegressor
                    self.log_success("scikit-learn ensemble imports work")
                elif package == 'sklearn.preprocessing':
                    from sklearn.preprocessing import StandardScaler, LabelEncoder
                    self.log_success("scikit-learn preprocessing imports work")
                elif package == 'joblib':
                    import joblib
                    self.log_success("joblib import works")
                else:
                    exec(f"import {package} as {imports.split(',')[0].strip()}")
                    self.log_success(f"{package} import works")
                    \n            except ImportError as e:
                self.log_error(f"{package} import error: {e}")
            except Exception as e:
                self.log_error(f"{package} functionality error: {e}")
    
    def check_port_availability(self, port=5000):
        """Check if the default port is available"""
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result == 0:
                self.log_warning(f"Port {port} is already in use")
            else:
                self.log_success(f"Port {port} is available")
        except Exception as e:
            self.log_warning(f"Could not check port availability: {e}")
    
    def validate_main_script(self):
        """Check if main.py has the essential components"""
        main_file = self.project_root / 'main.py'
        if main_file.exists():
            try:
                with open(main_file, 'r') as f:
                    content = f.read()
                    
                # Check for essential components
                essential_components = [
                    'Flask',
                    'CropPredictionSystem',
                    'app.route',
                    'predict',
                    'train_models'
                ]
                
                missing_components = [comp for comp in essential_components if comp not in content]
                if not missing_components:
                    self.log_success("main.py has essential Flask and ML components")
                else:
                    self.log_warning(f"main.py missing components: {missing_components}")
                    \n            except Exception as e:
                self.log_error(f"Error validating main.py: {e}")
    
    def run_comprehensive_check(self):
        """Run all validation checks"""
        print("🔍 Starting comprehensive project validation...")
        print("=" * 50)
        
        self.check_python_version()
        self.check_file_structure()
        self.check_dependencies()
        self.check_templates_directory()
        self.check_models_directory()
        self.test_flask_import()
        self.test_ml_imports()
        self.check_port_availability()
        self.validate_main_script()
        
        print("=" * 50)
        print("📊 Validation Summary:")
        print(f"✅ Successes: {len(self.successes)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.errors:
            print("\n🔧 Recommended fixes:")
            print("1. Install missing dependencies: pip install -r requirements.txt")
            print("2. Ensure all required files are present")
            print("3. Check Python version compatibility")
            print("4. Verify Flask and scikit-learn installations")
        
        if not self.errors:
            print("\n🎉 Project validation passed! Ready to run.")
            print("Start the application with: python main.py")
        else:
            print("\n⚠️  Please fix the errors above before running the application.")
        
        return len(self.errors) == 0

def main():
    """Main validation function"""
    validator = ProjectValidator()
    success = validator.run_comprehensive_check()
    
    # Return exit code based on validation result
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Iris Crop Prediction System - Startup Script
This script provides a simple way to start the application with different options.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    print("Requirements installed successfully!")

def start_server(debug=True, host='0.0.0.0', port=5000):
    """Start the Flask development server"""
    print(f"Starting Iris Crop Prediction Server...")
    print(f"Debug mode: {debug}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"URL: http://{host}:{port}")
    
    # Import and run the main app
    from main import app
    app.run(debug=debug, host=host, port=port)

def main():
    """Main function with command line options"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Iris Crop Prediction System')
    parser.add_argument('--install', action='store_true', help='Install requirements')
    parser.add_argument('--no-debug', action='store_true', help='Disable debug mode')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    
    args = parser.parse_args()
    
    if args.install:
        install_requirements()
    
    # Start the server
    start_server(
        debug=not args.no_debug,
        host=args.host,
        port=args.port
    )

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Iris Crop Prediction System - Validation and Error Checking Script
This script validates the project setup and checks for common issues.
"""

import os
import sys
import importlib.util
import subprocess
import json
from pathlib import Path

class ProjectValidator:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        self.successes = []
    
    def log_error(self, message):
        self.errors.append(f"❌ {message}")
        print(f"❌ {message}")
    
    def log_warning(self, message):
        self.warnings.append(f"⚠️  {message}")
        print(f"⚠️  {message}")
    
    def log_success(self, message):
        self.successes.append(f"✅ {message}")
        print(f"✅ {message}")
    
    def check_python_version(self):
        """Check Python version compatibility"""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 7:
            self.log_success(f"Python {version.major}.{version.minor}.{version.micro} is supported")
        else:
            self.log_error("Python 3.7+ is required")
    
    def check_file_structure(self):
        """Check if all required files exist"""
        required_files = [
            'main.py',
            'app.py',
            'requirements.txt',
            'templates/index.html'
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                self.log_success(f"Found {file_path}")
            else:
                self.log_error(f"Missing {file_path}")
    
    def check_dependencies(self):
        """Check if all required packages are installed"""
        required_packages = [
            'flask',
            'pandas',
            'numpy',
            'scikit-learn',
            'joblib'
        ]
        
        for package in required_packages:
            try:
                spec = importlib.util.find_spec(package)
                if spec is not None:
                    self.log_success(f"{package} is installed")
                else:
                    self.log_error(f"{package} is not installed")
            except ImportError:
                self.log_error(f"{package} is not available")
    
    def check_templates_directory(self):
        """Check templates directory and HTML file"""
        templates_dir = self.project_root / 'templates'
        if templates_dir.exists():
            self.log_success("Templates directory exists")
            
            index_file = templates_dir / 'index.html'
            if index_file.exists():
                self.log_success("index.html template found")
                
                # Check HTML file size and basic structure
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if len(content) > 1000:
                            self.log_success("HTML template appears to be substantial")
                        else:
                            self.log_warning("HTML template seems very short")
                        
                        # Check for essential HTML elements
                        essential_elements = ['<!DOCTYPE html>', '<html', '<head>', '<body>', '</html>']
                        missing_elements = [elem for elem in essential_elements if elem not in content]
                        if not missing_elements:
                            self.log_success("HTML template has essential structure")
                        else:
                            self.log_warning(f"HTML template missing: {missing_elements}")
                            
                except Exception as e:
                    self.log_error(f"Error reading HTML template: {e}")
            else:
                self.log_error("index.html template not found")
        else:
            self.log_error("Templates directory not found")
    
    def check_models_directory(self):
        """Check if models directory can be created"""
        models_dir = self.project_root / 'models'
        try:
            if not models_dir.exists():
                models_dir.mkdir(exist_ok=True)
                self.log_success("Models directory is accessible")
            else:
                self.log_success("Models directory exists")
        except Exception as e:
            self.log_error(f"Cannot create models directory: {e}")
    
    def test_flask_import(self):
        """Test if Flask can be imported and basic functionality"""
        try:
            from flask import Flask
            self.log_success("Flask can be imported")
            
            # Test basic Flask app creation
            app = Flask(__name__)
            if app:
                self.log_success("Basic Flask app can be created")
            else:
                self.log_error("Cannot create Flask app instance")
                \n        except ImportError as e:
            self.log_error(f"Flask import error: {e}")
        except Exception as e:
            self.log_error(f"Flask functionality error: {e}")
    
    def test_ml_imports(self):
        """Test machine learning library imports"""
        ml_packages = {
            'pandas': 'pd',
            'numpy': 'np',
            'sklearn.ensemble': 'RandomForestRegressor',
            'sklearn.preprocessing': 'StandardScaler, LabelEncoder',
            'joblib': 'joblib'
        }
        
        for package, imports in ml_packages.items():
            try:
                if package == 'sklearn.ensemble':
                    from sklearn.ensemble import RandomForestRegressor
                    self.log_success("scikit-learn ensemble imports work")
                elif package == 'sklearn.preprocessing':
                    from sklearn.preprocessing import StandardScaler, LabelEncoder
                    self.log_success("scikit-learn preprocessing imports work")
                elif package == 'joblib':
                    import joblib
                    self.log_success("joblib import works")
                else:
                    exec(f"import {package} as {imports.split(',')[0].strip()}")
                    self.log_success(f"{package} import works")
                    \n            except ImportError as e:
                self.log_error(f"{package} import error: {e}")
            except Exception as e:
                self.log_error(f"{package} functionality error: {e}")
    
    def check_port_availability(self, port=5000):
        """Check if the default port is available"""
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result == 0:
                self.log_warning(f"Port {port} is already in use")
            else:
                self.log_success(f"Port {port} is available")
        except Exception as e:
            self.log_warning(f"Could not check port availability: {e}")
    
    def validate_main_script(self):
        """Check if main.py has the essential components"""
        main_file = self.project_root / 'main.py'
        if main_file.exists():
            try:
                with open(main_file, 'r') as f:
                    content = f.read()
                    
                # Check for essential components
                essential_components = [
                    'Flask',
                    'CropPredictionSystem',
                    'app.route',
                    'predict',
                    'train_models'
                ]
                
                missing_components = [comp for comp in essential_components if comp not in content]
                if not missing_components:
                    self.log_success("main.py has essential Flask and ML components")
                else:
                    self.log_warning(f"main.py missing components: {missing_components}")
                    \n            except Exception as e:
                self.log_error(f"Error validating main.py: {e}")
    
    def run_comprehensive_check(self):
        """Run all validation checks"""
        print("🔍 Starting comprehensive project validation...")
        print("=" * 50)
        
        self.check_python_version()
        self.check_file_structure()
        self.check_dependencies()
        self.check_templates_directory()
        self.check_models_directory()
        self.test_flask_import()
        self.test_ml_imports()
        self.check_port_availability()
        self.validate_main_script()
        
        print("=" * 50)
        print("📊 Validation Summary:")
        print(f"✅ Successes: {len(self.successes)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.errors:
            print("\n🔧 Recommended fixes:")
            print("1. Install missing dependencies: pip install -r requirements.txt")
            print("2. Ensure all required files are present")
            print("3. Check Python version compatibility")
            print("4. Verify Flask and scikit-learn installations")
        
        if not self.errors:
            print("\n🎉 Project validation passed! Ready to run.")
            print("Start the application with: python main.py")
        else:
            print("\n⚠️  Please fix the errors above before running the application.")
        
        return len(self.errors) == 0

def main():
    """Main validation function"""
    validator = ProjectValidator()
    success = validator.run_comprehensive_check()
    
    # Return exit code based on validation result
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
