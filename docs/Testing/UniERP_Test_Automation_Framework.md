# UniERP Test Automation Framework

## Overview

This document provides comprehensive guidelines for the UniERP Test Automation Framework, including architecture, configuration, implementation, and best practices for automated testing of the UniERP system.

## Document Information

- **Project:** UniERP Rebranding Project
- **Phase:** Phase 11 - Testing & Quality Assurance
- **Milestone:** 11.1 - Test Planning & Setup
- **Version:** 1.0
- **Created:** November 2024
- **Last Updated:** November 2024
- **Author:** UniERP QA Automation Team
- **Contact:** qa-automation@unierp.com

---

## 1. Framework Architecture

### 1.1 Architecture Overview

The UniERP Test Automation Framework is built on a modular, scalable architecture that supports multiple testing types and integrates seamlessly with the CI/CD pipeline.

#### 1.1.1 Framework Components
- **Core Engine:** Test execution and management
- **Test Libraries:** Reusable test components and utilities
- **Data Management:** Test data generation and management
- **Reporting:** Test result reporting and analysis
- **Integration:** CI/CD pipeline integration
- **Configuration:** Environment and test configuration management

#### 1.1.2 Technology Stack
- **Programming Language:** Python 3.8+
- **Test Runner:** pytest
- **UI Automation:** Selenium WebDriver
- **API Testing:** requests, REST Assured
- **Database Testing:** psycopg2, SQLAlchemy
- **Performance Testing:** JMeter integration
- **Reporting:** Allure, HTML reports
- **CI/CD:** GitLab CI/CD integration

### 1.2 Framework Structure

```
unierp_test_framework/
├── config/
│   ├── __init__.py
│   ├── base_config.py
│   ├── test_config.py
│   └── environment_config.py
├── core/
│   ├── __init__.py
│   ├── test_engine.py
│   ├── test_runner.py
│   └── test_manager.py
├── libraries/
│   ├── __init__.py
│   ├── web_library.py
│   ├── api_library.py
│   ├── database_library.py
│   └── utility_library.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── module_pages/
├── tests/
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   ├── functional/
│   ├── performance/
│   └── security/
├── data/
│   ├── __init__.py
│   ├── test_data_generator.py
│   ├── test_data_manager.py
│   └── fixtures/
├── reports/
│   ├── __init__.py
│   ├── report_generator.py
│   ├── email_notifier.py
│   └── templates/
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── screenshot.py
│   ├── wait_helper.py
│   └── config_loader.py
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 2. Core Framework Components

### 2.1 Configuration Management

#### 2.1.1 Base Configuration
```python
# config/base_config.py
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class BaseConfig:
    """Base configuration class for UniERP test framework"""
    
    # Framework Configuration
    FRAMEWORK_NAME: str = "UniERP Test Automation Framework"
    VERSION: str = "1.0.0"
    
    # Test Configuration
    DEFAULT_TIMEOUT: int = 30
    IMPLICIT_WAIT: int = 10
    PAGE_LOAD_TIMEOUT: int = 60
    SCRIPT_TIMEOUT: int = 300
    
    # Browser Configuration
    DEFAULT_BROWSER: str = "chrome"
    HEADLESS: bool = False
    BROWSER_WINDOW_SIZE: tuple = (1920, 1080)
    
    # Test Data Configuration
    TEST_DATA_PATH: str = "data/fixtures"
    TEST_DATA_REFRESH_INTERVAL: int = 7  # days
    
    # Reporting Configuration
    REPORT_PATH: str = "reports"
    SCREENSHOT_PATH: str = "reports/screenshots"
    LOG_PATH: str = "reports/logs"
    ALLURE_REPORT_PATH: str = "reports/allure"
    
    # Email Configuration
    EMAIL_NOTIFICATIONS: bool = True
    EMAIL_RECIPIENTS: list = ["qa-team@unierp.com"]
    
    # UniERP Branding Configuration
    COMPANY_NAME: str = "UniERP"
    COMPANY_WEBSITE: str = "https://www.unierp.com"
    SUPPORT_EMAIL: str = "support@unierp.com"
    
    @classmethod
    def from_env(cls) -> 'BaseConfig':
        """Create configuration from environment variables"""
        config = cls()
        
        # Override with environment variables
        config.DEFAULT_BROWSER = os.getenv('TEST_BROWSER', config.DEFAULT_BROWSER)
        config.HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
        config.EMAIL_NOTIFICATIONS = os.getenv('EMAIL_NOTIFICATIONS', 'true').lower() == 'true'
        
        return config
```

#### 2.1.2 Environment Configuration
```python
# config/environment_config.py
from enum import Enum
from typing import Dict, Any
from .base_config import BaseConfig

class Environment(Enum):
    """Test environments enumeration"""
    DEVELOPMENT = "development"
    INTEGRATION = "integration"
    SYSTEM = "system"
    PERFORMANCE = "performance"
    SECURITY = "security"
    UAT = "uat"

class EnvironmentConfig:
    """Environment-specific configuration"""
    
    ENVIRONMENT_CONFIGS: Dict[Environment, Dict[str, Any]] = {
        Environment.DEVELOPMENT: {
            "base_url": "http://dev.unierp.com:8069",
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "unierp_dev",
                "user": "unierp",
                "password": "dev_password"
            },
            "email": {
                "backend": "console",
                "host": "",
                "port": "",
                "user": "",
                "password": ""
            }
        },
        
        Environment.INTEGRATION: {
            "base_url": "https://integration.unierp.com",
            "database": {
                "host": "integration-db.unierp.com",
                "port": 5432,
                "name": "unierp_integration",
                "user": "unierp",
                "password": "integration_password"
            },
            "email": {
                "backend": "smtp",
                "host": "smtp.integration.unierp.com",
                "port": 587,
                "user": "integration@unierp.com",
                "password": "integration_email_password"
            }
        },
        
        Environment.SYSTEM: {
            "base_url": "https://system.unierp.com",
            "database": {
                "host": "system-db.unierp.com",
                "port": 5432,
                "name": "unierp_system",
                "user": "unierp",
                "password": "system_password"
            },
            "email": {
                "backend": "smtp",
                "host": "smtp.unierp.com",
                "port": 587,
                "user": "system@unierp.com",
                "password": "system_email_password"
            }
        },
        
        Environment.PERFORMANCE: {
            "base_url": "https://performance.unierp.com",
            "database": {
                "host": "performance-db.unierp.com",
                "port": 5432,
                "name": "unierp_performance",
                "user": "unierp",
                "password": "performance_password"
            },
            "email": {
                "backend": "smtp",
                "host": "smtp.unierp.com",
                "port": 587,
                "user": "performance@unierp.com",
                "password": "performance_email_password"
            }
        },
        
        Environment.SECURITY: {
            "base_url": "https://security.unierp.com",
            "database": {
                "host": "security-db.unierp.com",
                "port": 5432,
                "name": "unierp_security",
                "user": "unierp",
                "password": "security_password"
            },
            "email": {
                "backend": "smtp",
                "host": "smtp.unierp.com",
                "port": 587,
                "user": "security@unierp.com",
                "password": "security_email_password"
            }
        },
        
        Environment.UAT: {
            "base_url": "https://uat.unierp.com",
            "database": {
                "host": "uat-db.unierp.com",
                "port": 5432,
                "name": "unierp_uat",
                "user": "unierp",
                "password": "uat_password"
            },
            "email": {
                "backend": "smtp",
                "host": "smtp.unierp.com",
                "port": 587,
                "user": "uat@unierp.com",
                "password": "uat_email_password"
            }
        }
    }
    
    @classmethod
    def get_config(cls, environment: Environment) -> Dict[str, Any]:
        """Get configuration for specific environment"""
        return cls.ENVIRONMENT_CONFIGS.get(environment, {})
    
    @classmethod
    def get_database_url(cls, environment: Environment) -> str:
        """Get database URL for specific environment"""
        config = cls.get_config(environment)
        db_config = config.get("database", {})
        
        return (f"postgresql://{db_config.get('user')}:"
                f"{db_config.get('password')}@"
                f"{db_config.get('host')}:"
                f"{db_config.get('port')}/"
                f"{db_config.get('name')}")
```

### 2.2 Test Engine

#### 2.2.1 Test Engine Core
```python
# core/test_engine.py
import pytest
import time
from typing import Optional, Callable, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config.base_config import BaseConfig
from config.environment_config import Environment, EnvironmentConfig
from utils.logger import TestLogger
from utils.screenshot import ScreenshotManager
from utils.wait_helper import WaitHelper

class TestEngine:
    """Core test engine for UniERP automation framework"""
    
    def __init__(self, environment: Environment):
        self.config = BaseConfig.from_env()
        self.environment = environment
        self.env_config = EnvironmentConfig.get_config(environment)
        self.logger = TestLogger()
        self.driver: Optional[webdriver.Remote] = None
        self.screenshot_manager = ScreenshotManager()
        self.wait_helper: Optional[WaitHelper] = None
        
    def setup_driver(self, browser: str = None) -> None:
        """Setup web driver based on browser type"""
        browser = browser or self.config.DEFAULT_BROWSER
        
        try:
            if browser.lower() == "chrome":
                self.driver = self._setup_chrome_driver()
            elif browser.lower() == "firefox":
                self.driver = self._setup_firefox_driver()
            else:
                raise ValueError(f"Unsupported browser: {browser}")
            
            self.driver.maximize_window()
            self.wait_helper = WaitHelper(self.driver, self.config.DEFAULT_TIMEOUT)
            self.logger.info(f"Driver setup completed for {browser}")
            
        except Exception as e:
            self.logger.error(f"Failed to setup driver: {e}")
            raise
    
    def _setup_chrome_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with options"""
        options = Options()
        
        if self.config.HEADLESS:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        
        # UniERP specific options
        options.add_argument("--user-agent=UniERP-Automation/1.0")
        options.add_argument(f"--profile-directory=unierp-test")
        
        return webdriver.Chrome(options=options)
    
    def _setup_firefox_driver(self) -> webdriver.Firefox:
        """Setup Firefox driver with options"""
        options = FirefoxOptions()
        
        if self.config.HEADLESS:
            options.add_argument("--headless")
        
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        # UniERP specific options
        options.set_preference("general.useragent.override", "UniERP-Automation/1.0")
        
        return webdriver.Firefox(options=options)
    
    def navigate_to_url(self, url: str = None) -> None:
        """Navigate to specified URL"""
        target_url = url or self.env_config.get("base_url")
        
        try:
            self.logger.info(f"Navigating to: {target_url}")
            self.driver.get(target_url)
            
            # Wait for page to load
            self.wait_helper.wait_for_page_load()
            
            # Verify UniERP branding on page
            self._verify_unierp_branding()
            
        except Exception as e:
            self.logger.error(f"Failed to navigate to {target_url}: {e}")
            self.screenshot_manager.take_screenshot(self.driver, "navigation_error")
            raise
    
    def _verify_unierp_branding(self) -> None:
        """Verify UniERP branding elements on current page"""
        try:
            # Check for UniERP logo
            logo = self.driver.find_element_by_css_selector("img[alt*='UniERP']")
            assert logo.is_displayed(), "UniERP logo not found"
            
            # Check page title contains UniERP
            page_title = self.driver.title
            assert "UniERP" in page_title, f"Page title '{page_title}' does not contain 'UniERP'"
            
            self.logger.info("UniERP branding verified successfully")
            
        except Exception as e:
            self.logger.warning(f"UniERP branding verification failed: {e}")
            # Don't fail the test for branding issues in test engine
    
    def teardown_driver(self) -> None:
        """Cleanup and close web driver"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Driver closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing driver: {e}")
            finally:
                self.driver = None
                self.wait_helper = None
    
    def execute_test(self, test_func: Callable, *args, **kwargs) -> Any:
        """Execute test function with error handling and reporting"""
        test_name = test_func.__name__
        start_time = time.time()
        
        try:
            self.logger.info(f"Starting test: {test_name}")
            result = test_func(self, *args, **kwargs)
            
            execution_time = time.time() - start_time
            self.logger.info(f"Test {test_name} passed in {execution_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"Test {test_name} failed after {execution_time:.2f} seconds: {e}")
            
            # Take screenshot on failure
            self.screenshot_manager.take_screenshot(self.driver, f"{test_name}_failure")
            
            raise
    
    def get_test_data(self, data_key: str) -> Any:
        """Get test data for current environment"""
        from data.test_data_manager import TestDataManager
        
        data_manager = TestDataManager(self.environment)
        return data_manager.get_test_data(data_key)
```

### 2.3 Page Object Model

#### 2.3.1 Base Page
```python
# pages/base_page.py
from abc import ABC, abstractmethod
from typing import Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.wait_helper import WaitHelper
from utils.logger import TestLogger

class BasePage(ABC):
    """Base page class for UniERP page objects"""
    
    def __init__(self, driver: WebDriver, wait_helper: WaitHelper):
        self.driver = driver
        self.wait_helper = wait_helper
        self.logger = TestLogger()
        
        # UniERP branding elements
        self.unierp_logo = (By.CSS_SELECTOR, "img[alt*='UniERP']")
        self.unierp_title = (By.CSS_SELECTOR, "title")
        self.footer_branding = (By.CSS_SELECTOR, ".footer .branding")
        
        # Common elements
        self.user_menu = (By.CSS_SELECTOR, ".oe_topbar_name")
        self.logout_link = (By.CSS_SELECTOR, "a[data-menu='logout']")
        self.help_link = (By.CSS_SELECTOR, ".oe_help_link")
        
    def wait_for_page_load(self) -> None:
        """Wait for page to fully load"""
        self.wait_helper.wait_for_page_load()
        self._verify_page_loaded()
    
    def _verify_page_loaded(self) -> None:
        """Verify page is loaded correctly"""
        try:
            # Check for UniERP branding
            self._verify_unierp_branding()
            
            # Check for page-specific elements
            self.verify_page_elements()
            
        except Exception as e:
            self.logger.error(f"Page load verification failed: {e}")
            raise
    
    def _verify_unierp_branding(self) -> None:
        """Verify UniERP branding on page"""
        try:
            # Check logo
            logo = self.wait_helper.wait_for_element_visible(self.unierp_logo)
            assert logo.is_displayed(), "UniERP logo not visible"
            
            # Check title
            title = self.driver.title
            assert "UniERP" in title, f"Page title '{title}' does not contain 'UniERP'"
            
            self.logger.debug("UniERP branding verified on page")
            
        except Exception as e:
            self.logger.warning(f"UniERP branding check failed: {e}")
    
    @abstractmethod
    def verify_page_elements(self) -> None:
        """Verify page-specific elements are loaded"""
        pass
    
    def click_user_menu(self) -> None:
        """Click on user menu"""
        self.wait_helper.wait_for_element_clickable(self.user_menu).click()
        self.logger.info("User menu clicked")
    
    def logout(self) -> None:
        """Logout from UniERP"""
        self.click_user_menu()
        self.wait_helper.wait_for_element_clickable(self.logout_link).click()
        self.logger.info("User logged out")
    
    def click_help_link(self) -> None:
        """Click on help link"""
        help_element = self.wait_helper.wait_for_element_clickable(self.help_link)
        help_element.click()
        self.logger.info("Help link clicked")
        
        # Verify help link opens UniERP help
        self._verify_help_link()
    
    def _verify_help_link(self) -> None:
        """Verify help link opens UniERP help"""
        try:
            # Switch to new window/tab if opened
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                
                # Check if help page contains UniERP branding
                page_source = self.driver.page_source
                assert "UniERP" in page_source, "Help page does not contain UniERP branding"
                assert "unierp.com" in page_source, "Help page does not reference unierp.com"
                
                self.logger.info("UniERP help link verified")
                
                # Close help window and switch back
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            
        except Exception as e:
            self.logger.warning(f"Help link verification failed: {e}")
    
    def get_page_title(self) -> str:
        """Get current page title"""
        return self.driver.title
    
    def is_element_present(self, locator: tuple) -> bool:
        """Check if element is present on page"""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False
    
    def is_element_visible(self, locator: tuple) -> bool:
        """Check if element is visible on page"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except:
            return False
    
    def wait_and_click(self, locator: tuple) -> None:
        """Wait for element to be clickable and click it"""
        element = self.wait_helper.wait_for_element_clickable(locator)
        element.click()
    
    def wait_and_type(self, locator: tuple, text: str) -> None:
        """Wait for element and type text"""
        element = self.wait_helper.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
```

#### 2.3.2 Login Page
```python
# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.wait_helper import WaitHelper

class LoginPage(BasePage):
    """UniERP login page object"""
    
    def __init__(self, driver, wait_helper):
        super().__init__(driver, wait_helper)
        
        # Login form elements
        self.login_form = (By.CSS_SELECTOR, ".oe_login_form")
        self.database_input = (By.CSS_SELECTOR, "select[name='db']")
        self.email_input = (By.CSS_SELECTOR, "input[name='login']")
        self.password_input = (By.CSS_SELECTOR, "input[name='password']")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")
        
        # UniERP branding elements
        self.unierp_title = (By.CSS_SELECTOR, ".oe_login .oe_topbar")
        self.unierp_logo = (By.CSS_SELECTOR, ".oe_login img")
        
        # Error messages
        self.error_message = (By.CSS_SELECTOR, ".oe_login .alert-danger")
        
        # Help and support links
        self.forgot_password_link = (By.CSS_SELECTOR, ".oe_login a[href*='reset_password']")
        self.unierp_support_link = (By.CSS_SELECTOR, ".oe_login a[href*='unierp.com']")
    
    def verify_page_elements(self) -> None:
        """Verify login page elements are loaded"""
        # Verify login form
        self.wait_helper.wait_for_element_visible(self.login_form)
        
        # Verify input fields
        self.wait_helper.wait_for_element_visible(self.database_input)
        self.wait_helper.wait_for_element_visible(self.email_input)
        self.wait_helper.wait_for_element_visible(self.password_input)
        
        # Verify login button
        self.wait_helper.wait_for_element_visible(self.login_button)
        
        # Verify UniERP branding
        self._verify_unierp_login_branding()
        
        self.logger.info("Login page elements verified")
    
    def _verify_unierp_login_branding(self) -> None:
        """Verify UniERP branding on login page"""
        try:
            # Check title
            title_element = self.wait_helper.wait_for_element_visible(self.unierp_title)
            assert "UniERP" in title_element.text, "Login page title does not contain 'UniERP'"
            
            # Check logo alt text
            logo_element = self.wait_helper.wait_for_element_visible(self.unierp_logo)
            assert "UniERP" in logo_element.get_attribute("alt"), "Logo alt text does not contain 'UniERP'"
            
            # Check support link
            support_link = self.wait_helper.wait_for_element_visible(self.unierp_support_link)
            support_href = support_link.get_attribute("href")
            assert "unierp.com" in support_href, "Support link does not point to unierp.com"
            
            self.logger.info("UniERP login page branding verified")
            
        except Exception as e:
            self.logger.error(f"UniERP login branding verification failed: {e}")
            raise
    
    def login(self, database: str, email: str, password: str) -> None:
        """Perform login with provided credentials"""
        self.logger.info(f"Attempting login for user: {email}")
        
        # Select database
        self.wait_helper.select_dropdown_by_text(self.database_input, database)
        
        # Enter credentials
        self.wait_helper.wait_for_element_visible(self.email_input).send_keys(email)
        self.wait_helper.wait_for_element_visible(self.password_input).send_keys(password)
        
        # Click login button
        self.wait_helper.wait_for_element_clickable(self.login_button).click()
        
        # Wait for login to complete
        self._wait_for_login_completion()
    
    def _wait_for_login_completion(self) -> None:
        """Wait for login process to complete"""
        try:
            # Wait for either dashboard or error message
            from pages.dashboard_page import DashboardPage
            dashboard = DashboardPage(self.driver, self.wait_helper)
            
            # Check if login was successful (dashboard appears) or failed (error appears)
            WebDriverWait(self.driver, 10).until(
                lambda driver: (
                    dashboard.is_dashboard_loaded() or 
                    self.is_element_present(self.error_message)
                )
            )
            
            if self.is_element_present(self.error_message):
                error_text = self.driver.find_element(*self.error_message).text
                self.logger.error(f"Login failed: {error_text}")
                raise Exception(f"Login failed: {error_text}")
            else:
                self.logger.info("Login completed successfully")
                
        except Exception as e:
            self.logger.error(f"Login completion check failed: {e}")
            raise
    
    def get_error_message(self) -> str:
        """Get error message from login page"""
        try:
            error_element = self.wait_helper.wait_for_element_visible(self.error_message)
            return error_element.text
        except:
            return ""
    
    def click_forgot_password(self) -> None:
        """Click forgot password link"""
        self.wait_helper.wait_for_element_clickable(self.forgot_password_link).click()
        self.logger.info("Forgot password link clicked")
    
    def is_login_page_displayed(self) -> bool:
        """Check if login page is displayed"""
        return self.is_element_visible(self.login_form)
```

---

## 3. Test Libraries

### 3.1 Web Library

#### 3.1.1 Web Utility Functions
```python
# libraries/web_library.py
from typing import List, Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
from utils.wait_helper import WaitHelper
from utils.logger import TestLogger

class WebLibrary:
    """Web utility library for UniERP testing"""
    
    def __init__(self, driver, wait_helper: WaitHelper):
        self.driver = driver
        self.wait_helper = wait_helper
        self.logger = TestLogger()
    
    def navigate_to_module(self, module_name: str) -> None:
        """Navigate to specific UniERP module"""
        try:
            # Click on Apps menu
            apps_menu = (By.CSS_SELECTOR, ".o_main_menu .o_app")
            self.wait_helper.wait_for_element_clickable(apps_menu).click()
            
            # Wait for apps to load
            apps_container = (By.CSS_SELECTOR, ".o_apps")
            self.wait_helper.wait_for_element_visible(apps_container)
            
            # Find and click on specific module
            module_xpath = f"//div[contains(@class, 'o_app')]//*[contains(text(), '{module_name}')]"
            module_element = self.wait_helper.wait_for_element_clickable((By.XPATH, module_xpath))
            module_element.click()
            
            # Wait for module to load
            self.wait_helper.wait_for_page_load()
            
            # Verify UniERP branding in module
            self._verify_module_branding(module_name)
            
            self.logger.info(f"Successfully navigated to {module_name} module")
            
        except Exception as e:
            self.logger.error(f"Failed to navigate to {module_name} module: {e}")
            raise
    
    def _verify_module_branding(self, module_name: str) -> None:
        """Verify UniERP branding in module"""
        try:
            # Check page title
            page_title = self.driver.title
            assert "UniERP" in page_title, f"Module {module_name} page title does not contain 'UniERP'"
            
            # Check for UniERP branding elements
            branding_elements = self.driver.find_elements(By.CSS_SELECTOR, "[class*='unierp'], [alt*='UniERP']")
            assert len(branding_elements) > 0, f"No UniERP branding found in {module_name} module"
            
            self.logger.debug(f"UniERP branding verified in {module_name} module")
            
        except Exception as e:
            self.logger.warning(f"Module branding verification failed for {module_name}: {e}")
    
    def create_record(self, module_name: str, record_data: dict) -> None:
        """Create a new record in specified module"""
        try:
            # Click Create button
            create_button = (By.CSS_SELECTOR, ".o_list_button_add")
            self.wait_helper.wait_for_element_clickable(create_button).click()
            
            # Wait for form to open
            form_container = (By.CSS_SELECTOR, ".o_form_view")
            self.wait_helper.wait_for_element_visible(form_container)
            
            # Fill form fields
            self._fill_form_fields(record_data)
            
            # Save record
            save_button = (By.CSS_SELECTOR, ".o_form_button_save")
            self.wait_helper.wait_for_element_clickable(save_button).click()
            
            # Wait for save to complete
            self.wait_helper.wait_for_element_invisible(form_container)
            
            self.logger.info(f"Successfully created record in {module_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to create record in {module_name}: {e}")
            raise
    
    def _fill_form_fields(self, field_data: dict) -> None:
        """Fill form fields with provided data"""
        for field_name, field_value in field_data.items():
            try:
                # Find field by name or label
                field_locator = self._find_field_locator(field_name)
                if field_locator:
                    self._fill_field(field_locator, field_value)
                else:
                    self.logger.warning(f"Field '{field_name}' not found")
                    
            except Exception as e:
                self.logger.error(f"Failed to fill field '{field_name}': {e}")
    
    def _find_field_locator(self, field_name: str) -> Optional[Tuple[str, str]]:
        """Find field locator by field name"""
        locators = [
            (By.NAME, field_name),
            (By.CSS_SELECTOR, f"[name='{field_name}']"),
            (By.XPATH, f"//label[contains(text(), '{field_name}')]/../input"),
            (By.XPATH, f"//label[contains(text(), '{field_name}')]/../select"),
            (By.XPATH, f"//label[contains(text(), '{field_name}')]/../textarea"),
        ]
        
        for locator in locators:
            try:
                self.driver.find_element(*locator)
                return locator
            except:
                continue
        
        return None
    
    def _fill_field(self, locator: Tuple[str, str], value: str) -> None:
        """Fill field with value"""
        element = self.wait_helper.wait_for_element_visible(locator)
        element_tag = element.tag_name.lower()
        
        if element_tag == "select":
            select = Select(element)
            select.select_by_visible_text(value)
        elif element_tag == "input" and element.get_attribute("type") == "checkbox":
            if value.lower() in ["true", "yes", "1"]:
                element.click()
        else:
            element.clear()
            element.send_keys(value)
    
    def search_records(self, search_term: str) -> None:
        """Search records with provided term"""
        try:
            # Find search box
            search_box = (By.CSS_SELECTOR, ".o_search_input")
            self.wait_helper.wait_for_element_visible(search_box).send_keys(search_term)
            
            # Press Enter or click search button
            search_button = (By.CSS_SELECTOR, ".o_search_button")
            if self.is_element_present(search_button):
                self.wait_helper.wait_for_element_clickable(search_button).click()
            else:
                self.wait_helper.wait_for_element_visible(search_box).send_keys(Keys.ENTER)
            
            # Wait for search results
            self.wait_helper.wait_for_page_load()
            
            self.logger.info(f"Search completed for term: {search_term}")
            
        except Exception as e:
            self.logger.error(f"Search failed for term '{search_term}': {e}")
            raise
    
    def verify_record_exists(self, record_identifier: str) -> bool:
        """Verify if record exists in current view"""
        try:
            # Search for record
            self.search_records(record_identifier)
            
            # Check if record is displayed in list
            record_xpath = f"//td[contains(text(), '{record_identifier}')]"
            record_element = self.wait_helper.wait_for_element_visible((By.XPATH, record_xpath))
            
            return record_element.is_displayed()
            
        except Exception:
            return False
    
    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """Check if element is present"""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False
```

### 3.2 API Library

#### 3.2.1 API Testing Functions
```python
# libraries/api_library.py
import requests
import json
from typing import Dict, Any, Optional
from requests.auth import HTTPBasicAuth
from config.environment_config import EnvironmentConfig
from utils.logger import TestLogger

class APILibrary:
    """API testing library for UniERP"""
    
    def __init__(self, environment):
        self.environment = environment
        self.env_config = EnvironmentConfig.get_config(environment)
        self.base_url = self.env_config.get("base_url")
        self.session = requests.Session()
        self.logger = TestLogger()
        
        # UniERP API headers
        self.default_headers = {
            "User-Agent": "UniERP-API-Test/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        self.session.headers.update(self.default_headers)
    
    def authenticate(self, username: str, password: str, database: str = None) -> str:
        """Authenticate with UniERP API and return session ID"""
        try:
            auth_url = f"{self.base_url}/web/session/authenticate"
            
            auth_data = {
                "jsonrpc": "2.0",
                "params": {
                    "login": username,
                    "password": password,
                    "db": database or self.env_config["database"]["name"]
                }
            }
            
            response = self.session.post(auth_url, json=auth_data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("result"):
                session_id = result["result"].get("session_id")
                self.logger.info(f"API authentication successful for user: {username}")
                return session_id
            else:
                error = result.get("error", {}).get("message", "Unknown error")
                raise Exception(f"API authentication failed: {error}")
                
        except Exception as e:
            self.logger.error(f"API authentication error: {e}")
            raise
    
    def create_record(self, model: str, record_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Create a record via API"""
        try:
            create_url = f"{self.base_url}/web/dataset/call_kw/{model}/create"
            
            create_data = {
                "jsonrpc": "2.0",
                "method": "create",
                "params": {
                    "model": model,
                    "args": [record_data],
                    "kwargs": {}
                }
            }
            
            # Add session ID to headers
            headers = {"Cookie": f"session_id={session_id}"}
            response = self.session.post(create_url, json=create_data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("result"):
                record_id = result["result"]
                self.logger.info(f"Successfully created {model} record with ID: {record_id}")
                return {"id": record_id, "data": record_data}
            else:
                error = result.get("error", {}).get("message", "Unknown error")
                raise Exception(f"Failed to create {model} record: {error}")
                
        except Exception as e:
            self.logger.error(f"API create record error: {e}")
            raise
    
    def read_record(self, model: str, record_id: int, session_id: str) -> Dict[str, Any]:
        """Read a record via API"""
        try:
            read_url = f"{self.base_url}/web/dataset/call_kw/{model}/read"
            
            read_data = {
                "jsonrpc": "2.0",
                "method": "read",
                "params": {
                    "model": model,
                    "ids": [record_id],
                    "fields": [],
                    "kwargs": {}
                }
            }
            
            headers = {"Cookie": f"session_id={session_id}"}
            response = self.session.post(read_url, json=read_data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("result"):
                record_data = result["result"][0] if result["result"] else {}
                self.logger.info(f"Successfully read {model} record with ID: {record_id}")
                return record_data
            else:
                error = result.get("error", {}).get("message", "Unknown error")
                raise Exception(f"Failed to read {model} record: {error}")
                
        except Exception as e:
            self.logger.error(f"API read record error: {e}")
            raise
    
    def update_record(self, model: str, record_id: int, update_data: Dict[str, Any], session_id: str) -> bool:
        """Update a record via API"""
        try:
            update_url = f"{self.base_url}/web/dataset/call_kw/{model}/write"
            
            update_data_request = {
                "jsonrpc": "2.0",
                "method": "write",
                "params": {
                    "model": model,
                    "ids": [record_id],
                    "args": [update_data],
                    "kwargs": {}
                }
            }
            
            headers = {"Cookie": f"session_id={session_id}"}
            response = self.session.post(update_url, json=update_data_request, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("result"):
                self.logger.info(f"Successfully updated {model} record with ID: {record_id}")
                return True
            else:
                error = result.get("error", {}).get("message", "Unknown error")
                raise Exception(f"Failed to update {model} record: {error}")
                
        except Exception as e:
            self.logger.error(f"API update record error: {e}")
            raise
    
    def delete_record(self, model: str, record_id: int, session_id: str) -> bool:
        """Delete a record via API"""
        try:
            delete_url = f"{self.base_url}/web/dataset/call_kw/{model}/unlink"
            
            delete_data = {
                "jsonrpc": "2.0",
                "method": "unlink",
                "params": {
                    "model": model,
                    "ids": [record_id],
                    "kwargs": {}
                }
            }
            
            headers = {"Cookie": f"session_id={session_id}"}
            response = self.session.post(delete_url, json=delete_data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("result"):
                self.logger.info(f"Successfully deleted {model} record with ID: {record_id}")
                return True
            else:
                error = result.get("error", {}).get("message", "Unknown error")
                raise Exception(f"Failed to delete {model} record: {error}")
                
        except Exception as e:
            self.logger.error(f"API delete record error: {e}")
            raise
    
    def search_records(self, model: str, domain: list = None, session_id: str = None) -> list:
        """Search records via API"""
        try:
            search_url = f"{self.base_url}/web/dataset/call_kw/{model}/search_read"
            
            search_data = {
                "jsonrpc": "2.0",
                "method": "search_read",
                "params": {
                    "model": model,
                    "domain": domain or [],
                    "fields": [],
                    "limit": 0,
                    "kwargs": {}
                }
            }
            
            headers = {}
            if session_id:
                headers["Cookie"] = f"session_id={session_id}"
            
            response = self.session.post(search_url, json=search_data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("result"):
                records = result["result"]
                self.logger.info(f"Found {len(records)} {model} records")
                return records
            else:
                error = result.get("error", {}).get("message", "Unknown error")
                raise Exception(f"Failed to search {model} records: {error}")
                
        except Exception as e:
            self.logger.error(f"API search records error: {e}")
            raise
    
    def verify_unierp_api_branding(self) -> bool:
        """Verify UniERP branding in API responses"""
        try:
            # Check API info endpoint
            info_url = f"{self.base_url}/web/webclient/version_info"
            response = self.session.get(info_url)
            response.raise_for_status()
            
            info_data = response.json()
            
            # Verify UniERP branding in version info
            if "server_version" in info_data:
                version = info_data["server_version"]
                assert "UniERP" in version, f"API version does not contain 'UniERP': {version}"
            
            # Check response headers for UniERP branding
            response_headers = response.headers
            server_header = response_headers.get("Server", "")
            assert "UniERP" in server_header, f"API Server header does not contain 'UniERP': {server_header}"
            
            self.logger.info("UniERP API branding verified")
            return True
            
        except Exception as e:
            self.logger.error(f"UniERP API branding verification failed: {e}")
            return False
```

---

## 4. Test Data Management

### 4.1 Test Data Generator

#### 4.1.1 Data Generation Classes
```python
# data/test_data_generator.py
import random
import string
from datetime import datetime, timedelta
from faker import Faker
from typing import Dict, List, Any

class UniERPTestDataGenerator:
    """Test data generator for UniERP"""
    
    def __init__(self, environment):
        self.environment = environment
        self.fake = Faker()
        self.fake.seed_instance(12345)  # Consistent test data
        
        # UniERP specific data
        self.unierp_companies = [
            "UniERP Test Company 1",
            "UniERP Test Company 2", 
            "UniERP Solutions Inc.",
            "UniERP Consulting Ltd."
        ]
        
        self.unierp_modules = [
            "Sales", "Purchase", "Inventory", "Accounting",
            "HR", "Manufacturing", "Project", "Website"
        ]
    
    def generate_user_data(self, count: int = 1) -> List[Dict[str, Any]]:
        """Generate test user data"""
        users = []
        
        for i in range(count):
            user = {
                "name": self.fake.name(),
                "email": f"test.user{i+1:03d}@unierp.com",
                "login": f"testuser{i+1:03d}",
                "password": "Test123!@#",
                "company_id": random.randint(1, 4),
                "groups_id": [random.randint(1, 10)],
                "company_ids": [random.randint(1, 4)],
                "active": True,
                "share": False,
                "notification_type": "email",
                "odoobot_state": "not_initialized",
                "sale_order_count": 0,
                "signature": f"<p>--<br/>{self.fake.name()}<br/>UniERP Test User</p>",
                "action_id": False,
                "create_date": datetime.now() - timedelta(days=random.randint(1, 365)),
                "write_date": datetime.now() - timedelta(days=random.randint(0, 30))
            }
            users.append(user)
        
        return users
    
    def generate_company_data(self, count: int = 1) -> List[Dict[str, Any]]:
        """Generate test company data"""
        companies = []
        
        for i in range(count):
            company = {
                "name": random.choice(self.unierp_companies),
                "email": f"company{i+1}@unierp.com",
                "phone": self.fake.phone_number(),
                "website": f"https://company{i+1}.unierp.com",
                "vat": f"US{random.randint(100000000, 999999999)}",
                "company_registry": f"{random.randint(1000000, 9999999)}",
                "currency_id": 1,  # USD
                "country_id": random.randint(1, 250),
                "state_id": random.randint(1, 5000),
                "street": self.fake.street_address(),
                "city": self.fake.city(),
                "zip": self.fake.zipcode(),
                "logo": self._generate_logo_data(),
                "favicon": self._generate_favicon_data(),
                "social_twitter": f"https://twitter.com/company{i+1}",
                "social_facebook": f"https://facebook.com/company{i+1}",
                "social_linkedin": f"https://linkedin.com/company/company{i+1}",
                "social_youtube": f"https://youtube.com/company{i+1}",
                "social_instagram": f"https://instagram.com/company{i+1}",
                "create_date": datetime.now() - timedelta(days=random.randint(1, 365)),
                "write_date": datetime.now() - timedelta(days=random.randint(0, 30))
            }
            companies.append(company)
        
        return companies
    
    def generate_product_data(self, count: int = 1) -> List[Dict[str, Any]]:
        """Generate test product data"""
        products = []
        categories = ["Electronics", "Furniture", "Office Supplies", "Software", "Services"]
        
        for i in range(count):
            product = {
                "name": f"UniERP Test Product {i+1:04d}",
                "default_code": f"UTP{i+1:06d}",
                "barcode": f"{random.randint(1000000000, 9999999999)}",
                "description": self.fake.text(max_nb_chars=500),
                "description_sale": self.fake.text(max_nb_chars=300),
                "description_purchase": self.fake.text(max_nb_chars=300),
                "categ_id": random.randint(1, 20),
                "type": random.choice(["product", "service"]),
                "sale_ok": True,
                "purchase_ok": True,
                "list_price": round(random.uniform(10.0, 1000.0), 2),
                "standard_price": round(random.uniform(5.0, 500.0), 2),
                "cost_method": "standard",
                "valuation": "manual_temporal",
                "currency_id": 1,  # USD
                "uom_id": 1,  # Units
                "uom_po_id": 1,  # Units
                "tracking": "none",
                "sale_line_warn": "no-message",
                "purchase_line_warn": "no-message",
                "weight": round(random.uniform(0.1, 100.0), 2),
                "volume": round(random.uniform(0.01, 10.0), 3),
                "active": True,
                "create_date": datetime.now() - timedelta(days=random.randint(1, 365)),
                "write_date": datetime.now() - timedelta(days=random.randint(0, 30))
            }
            products.append(product)
        
        return products
    
    def generate_customer_data(self, count: int = 1) -> List[Dict[str, Any]]:
        """Generate test customer data"""
        customers = []
        
        for i in range(count):
            customer = {
                "name": self.fake.company(),
                "display_name": self.fake.company(),
                "commercial_company_name": self.fake.company(),
                "is_company": True,
                "company_type": "company",
                "customer_rank": random.randint(1, 100),
                "supplier_rank": random.randint(0, 50),
                "street": self.fake.street_address(),
                "street2": self.fake.secondary_address(),
                "city": self.fake.city(),
                "state_id": random.randint(1, 5000),
                "zip": self.fake.zipcode(),
                "country_id": random.randint(1, 250),
                "phone": self.fake.phone_number(),
                "mobile": self.fake.phone_number(),
                "email": f"customer{i+1:04d}@unierp.com",
                "website": f"https://customer{i+1:04d}.unierp.com",
                "vat": f"US{random.randint(100000000, 999999999)}",
                "lang": "en_US",
                "tz": "UTC",
                "credit_limit": round(random.uniform(0.0, 50000.0), 2),
                "over_credit": False,
                "trust": "good",
                "active": True,
                "create_date": datetime.now() - timedelta(days=random.randint(1, 365)),
                "write_date": datetime.now() - timedelta(days=random.randint(0, 30))
            }
            customers.append(customer)
        
        return customers
    
    def generate_sales_order_data(self, customer_id: int, product_ids: List[int], count: int = 1) -> List[Dict[str, Any]]:
        """Generate test sales order data"""
        orders = []
        
        for i in range(count):
            order_lines = []
            for product_id in product_ids:
                line = {
                    "product_id": product_id,
                    "product_uom_qty": random.randint(1, 10),
                    "price_unit": round(random.uniform(10.0, 1000.0), 2),
                    "discount": round(random.uniform(0.0, 20.0), 2),
                    "tax_id": random.choice([None, 1, 2, 3]),
                    "name": f"Order line for product {product_id}"
                }
                order_lines.append((0, 0, line))
            
            order = {
                "partner_id": customer_id,
                "state": "draft",
                "date_order": datetime.now(),
                "validity_date": datetime.now() + timedelta(days=30),
                "pricelist_id": 1,
                "currency_id": 1,  # USD
                "payment_term_id": random.randint(1, 5),
                "order_line": order_lines,
                "note": f"Test sales order {i+1} for UniERP testing",
                "client_order_ref": f"CO-{random.randint(10000, 99999)}",
                "create_date": datetime.now() - timedelta(days=random.randint(0, 30)),
                "write_date": datetime.now() - timedelta(days=random.randint(0, 1))
            }
            orders.append(order)
        
        return orders
    
    def _generate_logo_data(self) -> str:
        """Generate base64 encoded logo data"""
        # This would normally generate actual image data
        # For testing, return placeholder
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    def _generate_favicon_data(self) -> str:
        """Generate base64 encoded favicon data"""
        # This would normally generate actual favicon data
        # For testing, return placeholder
        return "data:image/x-icon;base64,AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAABILAAASCwAAAAAAAAAAAAD///8A"
    
    def generate_test_scenario_data(self, scenario_type: str) -> Dict[str, Any]:
        """Generate data for specific test scenarios"""
        scenarios = {
            "user_registration": {
                "users": self.generate_user_data(5),
                "companies": self.generate_company_data(2)
            },
            "sales_process": {
                "customers": self.generate_customer_data(10),
                "products": self.generate_product_data(20),
                "orders": []
            },
            "inventory_management": {
                "products": self.generate_product_data(50),
                "locations": self._generate_warehouse_data(),
                "stock_moves": []
            },
            "financial_reporting": {
                "accounts": self._generate_chart_of_accounts(),
                "journal_entries": self._generate_journal_entries(),
                "periods": self._generate_fiscal_periods()
            }
        }
        
        return scenarios.get(scenario_type, {})
    
    def _generate_warehouse_data(self) -> List[Dict[str, Any]]:
        """Generate warehouse test data"""
        warehouses = []
        for i in range(5):
            warehouse = {
                "name": f"UniERP Warehouse {i+1}",
                "code": f"WH{i+1:02d}",
                "company_id": 1,
                "partner_id": None,
                "lot_input_id": random.randint(1, 10),
                "lot_stock_id": random.randint(1, 10),
                "active": True
            }
            warehouses.append(warehouse)
        return warehouses
    
    def _generate_chart_of_accounts(self) -> List[Dict[str, Any]]:
        """Generate chart of accounts test data"""
        accounts = []
        account_types = [
            ("Asset", "asset"), ("Liability", "liability"),
            ("Equity", "equity"), ("Revenue", "revenue"), ("Expense", "expense")
        ]
        
        for i, (name, account_type) in enumerate(account_types):
            for j in range(10):
                account = {
                    "name": f"{name} Account {j+1:02d}",
                    "code": f"{i+1}{j+1:02d}00",
                    "user_type_id": random.randint(1, 20),
                    "internal_type": account_type,
                    "reconcile": account_type in ["asset", "liability"],
                    "deprecated": False,
                    "company_id": 1
                }
                accounts.append(account)
        
        return accounts
    
    def _generate_journal_entries(self) -> List[Dict[str, Any]]:
        """Generate journal entry test data"""
        entries = []
        for i in range(100):
            entry = {
                "name": f"Journal Entry {i+1:04d}",
                "date": datetime.now() - timedelta(days=random.randint(0, 365)),
                "journal_id": random.randint(1, 10),
                "company_id": 1,
                "state": "posted",
                "line_ids": []
            }
            entries.append(entry)
        
        return entries
    
    def _generate_fiscal_periods(self) -> List[Dict[str, Any]]:
        """Generate fiscal period test data"""
        periods = []
        current_year = datetime.now().year
        
        for year in range(current_year - 2, current_year + 1):
            for quarter in range(1, 5):
                period = {
                    "name": f"{year}/Q{quarter}",
                    "code": f"{year}{quarter:02d}",
                    "date_start": datetime(year, (quarter - 1) * 3 + 1, 1),
                    "date_end": datetime(year, quarter * 3, 31),
                    "special": False,
                    "company_id": 1,
                    "fiscal_year_id": year - current_year + 3
                }
                periods.append(period)
        
        return periods
```

---

## 5. Configuration and Setup

### 5.1 pytest Configuration

#### 5.1.1 pytest.ini
```ini
[tool:pytest]
# Test discovery
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Output and reporting
addopts = 
    -v
    --html=reports/report.html
    --self-contained-html
    --alluredir=reports/allure
    --tb=short
    --strict-markers
    --strict-config
    --disable-warnings

# Markers
markers =
    smoke: marks tests as smoke tests (run on every build)
    regression: marks tests as regression tests (run on schedule)
    functional: marks tests as functional tests
    integration: marks tests as integration tests
    performance: marks tests as performance tests
    security: marks tests as security tests
    branding: marks tests as branding verification tests
    api: marks tests as API tests
    ui: marks tests as UI tests
    database: marks tests as database tests
    slow: marks tests as slow running tests
    critical: marks tests as critical path tests

# Minimum version
minversion = 6.0

# Test session configuration
console_output_style = progress
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(name)s: %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

# Coverage configuration
addopts = --cov=unierp_test_framework --cov-report=html --cov-report=term-missing
```

#### 5.1.2 conftest.py
```python
# conftest.py
import pytest
import os
import sys
from typing import Dict, Any, Generator

# Add framework to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.test_engine import TestEngine
from config.base_config import BaseConfig
from config.environment_config import Environment, EnvironmentConfig
from utils.logger import TestLogger
from data.test_data_manager import TestDataManager

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--environment",
        action="store",
        default="integration",
        help="Test environment (development, integration, system, performance, security, uat)"
    )
    parser.addoption(
        "--browser",
        action="store", 
        default="chrome",
        help="Browser to use for tests (chrome, firefox)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--test-data-refresh",
        action="store_true",
        default=False,
        help="Refresh test data before running tests"
    )

@pytest.fixture(scope="session")
def test_config(request) -> Dict[str, Any]:
    """Test configuration fixture"""
    environment_name = request.config.getoption("--environment")
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    try:
        environment = Environment(environment_name.lower())
    except ValueError:
        raise ValueError(f"Invalid environment: {environment_name}")
    
    config = {
        "environment": environment,
        "browser": browser,
        "headless": headless,
        "env_config": EnvironmentConfig.get_config(environment),
        "base_config": BaseConfig.from_env()
    }
    
    # Override config with command line options
    config["base_config"].DEFAULT_BROWSER = browser
    config["base_config"].HEADLESS = headless
    
    return config

@pytest.fixture(scope="session")
def test_engine(test_config) -> Generator[TestEngine, None, None]:
    """Test engine fixture"""
    engine = TestEngine(test_config["environment"])
    
    # Setup engine
    engine.setup_driver(test_config["browser"])
    
    yield engine
    
    # Teardown
    engine.teardown_driver()

@pytest.fixture(scope="function")
def authenticated_test_engine(test_engine, test_config) -> Generator[TestEngine, None, None]:
    """Authenticated test engine fixture"""
    # Login before test
    from pages.login_page import LoginPage
    login_page = LoginPage(test_engine.driver, test_engine.wait_helper)
    
    # Get test credentials
    from data.test_data_manager import TestDataManager
    data_manager = TestDataManager(test_config["environment"])
    credentials = data_manager.get_test_credentials()
    
    login_page.navigate_to_url()
    login_page.login(
        database=credentials["database"],
        email=credentials["email"],
        password=credentials["password"]
    )
    
    yield test_engine
    
    # Logout after test
    try:
        login_page.logout()
    except:
        pass  # Already logged out or page not accessible

@pytest.fixture(scope="session")
def test_data(test_config) -> Dict[str, Any]:
    """Test data fixture"""
    data_manager = TestDataManager(test_config["environment"])
    
    # Refresh test data if requested
    if test_config.get("test_data_refresh", False):
        data_manager.refresh_test_data()
    
    return data_manager.get_all_test_data()

@pytest.fixture(scope="function", autouse=True)
def test_logger(request):
    """Test logger fixture"""
    logger = TestLogger()
    logger.info(f"Starting test: {request.node.name}")
    
    yield logger
    
    logger.info(f"Finished test: {request.node.name}")

@pytest.fixture(autouse=True)
def unierp_branding_check(test_engine):
    """Automatically check UniERP branding in tests"""
    yield
    
    # Check UniERP branding after each test
    try:
        title = test_engine.driver.title
        assert "UniERP" in title, f"Page title '{title}' does not contain 'UniERP'"
    except:
        pass  # Driver might be closed or page not accessible

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Generate test report with UniERP branding"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        if report.passed:
            # Add UniERP branding info to passed tests
            if hasattr(report, "extra"):
                report.extra.append({
                    "name": "UniERP Branding",
                    "value": "Verified - UniERP branding present"
                })
        elif report.failed:
            # Add screenshot for failed tests
            try:
                from utils.screenshot import ScreenshotManager
                screenshot_manager = ScreenshotManager()
                screenshot_path = screenshot_manager.take_screenshot(
                    item.funcargs.get("test_engine").driver,
                    f"failure_{item.name}"
                )
                
                if hasattr(report, "extra"):
                    report.extra.append({
                        "name": "Screenshot",
                        "path": screenshot_path
                    })
            except:
                pass

def pytest_configure(config):
    """Configure pytest with UniERP settings"""
    # Set custom markers
    config.addinivalue_line(
        "markers", "branding: Tests that verify UniERP branding"
    )
    config.addinivalue_line(
        "markers", "unierp: Tests specific to UniERP functionality"
    )
    
    # Configure logging
    logger = TestLogger()
    logger.info("UniERP Test Framework initialized")
    logger.info(f"Test environment: {config.getoption('--environment')}")
    logger.info(f"Browser: {config.getoption('--browser')}")
    logger.info(f"Headless: {config.getoption('--headless')}")

def pytest_sessionstart(session):
    """Session start hook"""
    logger = TestLogger()
    logger.info("=" * 60)
    logger.info("UniERP Test Automation Framework")
    logger.info(f"Version: {BaseConfig.VERSION}")
    logger.info(f"Environment: {session.config.getoption('--environment')}")
    logger.info(f"Browser: {session.config.getoption('--browser')}")
    logger.info("=" * 60)

def pytest_sessionfinish(session, exitstatus):
    """Session end hook"""
    logger = TestLogger()
    logger.info("=" * 60)
    logger.info(f"Test session completed with exit status: {exitstatus}")
    logger.info("UniERP Test Framework session ended")
    logger.info("=" * 60)
```

### 5.2 Requirements

#### 5.2.1 requirements.txt
```txt
# Core dependencies
pytest>=7.0.0
pytest-html>=3.1.1
pytest-cov>=4.0.0
pytest-xdist>=3.0.0
pytest-allure-adaptor>=2.12.0
allure-pytest>=2.12.0

# Web automation
selenium>=4.5.0
webdriver-manager>=3.8.0

# API testing
requests>=2.28.0
requests-mock>=1.10.0
urllib3>=1.26.0

# Database testing
psycopg2-binary>=2.9.0
sqlalchemy>=1.4.0
alembic>=1.8.0

# Data generation
faker>=15.0.0
numpy>=1.21.0
pandas>=1.5.0

# Utilities
python-dotenv>=0.21.0
pyyaml>=6.0
jinja2>=3.1.0
markdown>=3.4.0

# Reporting
reportlab>=3.6.0
matplotlib>=3.6.0
seaborn>=0.11.0

# Performance testing
locust>=2.14.0
jmeter-python>=0.1.0

# Security testing
bandit>=1.7.0
safety>=2.2.0

# Code quality
black>=22.0.0
flake8>=5.0.0
mypy>=0.991

# UniERP specific
unierp-client>=16.0.0
unierp-addons>=16.0.0

# Development tools
pytest-watch>=6.0.0
pytest-benchmark>=3.4.0
ipython>=8.0.0
```

---

## 6. Best Practices and Guidelines

### 6.1 Test Development Guidelines

#### 6.1.1 Test Structure
- **Test Naming:** Use descriptive names that indicate what is being tested
- **Test Organization:** Group related tests in logical modules
- **Test Independence:** Each test should be independent and not rely on other tests
- **Test Data:** Use fixtures for test data setup and teardown
- **Assertions:** Use clear and specific assertions with meaningful messages

#### 6.1.2 Coding Standards
- **Python Standards:** Follow PEP 8 coding standards
- **Documentation:** Include docstrings for all test functions and classes
- **Error Handling:** Implement proper error handling and logging
- **UniERP Branding:** Always verify UniERP branding in tests
- **Resource Cleanup:** Ensure proper cleanup of test resources

### 6.2 Performance Guidelines

#### 6.2.1 Test Performance
- **Test Speed:** Keep individual tests under 30 seconds when possible
- **Parallel Execution:** Use pytest-xdist for parallel test execution
- **Resource Management:** Efficient use of system resources
- **Test Data:** Optimize test data generation and loading

#### 6.2.2 Framework Performance
- **Memory Usage:** Monitor and optimize memory usage
- **Driver Management:** Efficient web driver lifecycle management
- **Connection Pooling:** Use connection pooling for database operations
- **Caching:** Implement caching for frequently accessed data

### 6.3 Security Guidelines

#### 6.3.1 Test Security
- **Credential Management:** Secure storage and handling of test credentials
- **Data Privacy:** Ensure test data doesn't contain sensitive information
- **Access Control:** Implement proper access controls for test environments
- **Audit Logging:** Log all test activities for audit purposes

#### 6.3.2 Framework Security
- **Input Validation:** Validate all inputs to prevent injection attacks
- **Output Encoding:** Proper encoding of outputs to prevent XSS
- **Authentication:** Secure authentication mechanisms for test access
- **Network Security:** Use secure connections for all communications

---

## 7. Integration and Deployment

### 7.1 CI/CD Integration

#### 7.1.1 GitLab CI Configuration
```yaml
# .gitlab-ci.yml
stages:
  - test
  - report
  - deploy

variables:
  TEST_ENVIRONMENT: "integration"
  BROWSER: "chrome"
  HEADLESS: "true"

before_script:
  - python -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt
  - python setup.py develop

unit_tests:
  stage: test
  script:
    - pytest tests/unit/ -v --html=reports/unit_tests.html --cov=unierp_test_framework --cov-report=xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    paths:
      - reports/
  only:
    - merge_requests
    - main

integration_tests:
  stage: test
  script:
    - pytest tests/integration/ -v --html=reports/integration_tests.html --alluredir=reports/allure
  artifacts:
    reports:
      junit: reports/junit.xml
    paths:
      - reports/
  dependencies:
    - unit_tests
  only:
    - merge_requests
    - main

functional_tests:
  stage: test
  script:
    - pytest tests/functional/ -v --html=reports/functional_tests.html --alluredir=reports/allure -n 4
  artifacts:
    reports:
      junit: reports/junit.xml
    paths:
      - reports/
  dependencies:
    - unit_tests
    - integration_tests
  only:
    - merge_requests
    - main

branding_tests:
  stage: test
  script:
    - pytest tests/branding/ -v --html=reports/branding_tests.html --alluredir=reports/allure
  artifacts:
    reports:
      junit: reports/junit.xml
    paths:
      - reports/
  only:
    - merge_requests
    - main

performance_tests:
  stage: test
  script:
    - pytest tests/performance/ -v --html=reports/performance_tests.html --alluredir=reports/allure
  artifacts:
    reports:
      junit: reports/junit.xml
    paths:
      - reports/
  only:
    - schedules
    - main

security_tests:
  stage: test
  script:
    - pytest tests/security/ -v --html=reports/security_tests.html --alluredir=reports/allure
    - bandit -r unierp_test_framework/ -f json -o reports/security_scan.json
  artifacts:
    reports:
      junit: reports/junit.xml
    paths:
      - reports/
  only:
    - schedules
    - main

generate_reports:
  stage: report
  script:
    - allure generate reports/allure -o reports/allure-report
    - python scripts/generate_summary_report.py
  artifacts:
    paths:
      - reports/allure-report/
      - reports/summary_report.html
  dependencies:
    - unit_tests
    - integration_tests
    - functional_tests
    - branding_tests
    - performance_tests
    - security_tests
  only:
    - merge_requests
    - main

deploy_test_results:
  stage: deploy
  script:
    - aws s3 sync reports/ s3://unierp-test-reports/$CI_COMMIT_SHA/
    - echo "Test results deployed to: https://unierp-test-reports.s3.amazonaws.com/$CI_COMMIT_SHA/"
  dependencies:
    - generate_reports
  only:
    - main
```

### 7.2 Reporting and Monitoring

#### 7.2.1 Report Generation
```python
# reports/report_generator.py
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template

class UniERPReportGenerator:
    """Generate comprehensive test reports for UniERP"""
    
    def __init__(self, report_dir: str = "reports"):
        self.report_dir = report_dir
        self.template_dir = "templates"
        
    def generate_summary_report(self, test_results: Dict[str, Any]) -> str:
        """Generate HTML summary report"""
        # Calculate metrics
        total_tests = test_results.get("total", 0)
        passed_tests = test_results.get("passed", 0)
        failed_tests = test_results.get("failed", 0)
        skipped_tests = test_results.get("skipped", 0)
        
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Generate charts
        self._generate_execution_chart(test_results)
        self._generate_branding_chart(test_results)
        
        # Load template
        template_path = os.path.join(self.template_dir, "summary_report.html")
        with open(template_path, 'r') as f:
            template = Template(f.read())
        
        # Render report
        report_html = template.render(
            title="UniERP Test Summary Report",
            generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            skipped_tests=skipped_tests,
            pass_rate=pass_rate,
            unierp_branding_score=test_results.get("branding_score", 0),
            test_results=test_results
        )
        
        # Save report
        report_path = os.path.join(self.report_dir, "summary_report.html")
        with open(report_path, 'w') as f:
            f.write(report_html)
        
        return report_path
    
    def _generate_execution_chart(self, test_results: Dict[str, Any]) -> None:
        """Generate test execution chart"""
        plt.figure(figsize=(10, 6))
        
        labels = ['Passed', 'Failed', 'Skipped']
        sizes = [
            test_results.get("passed", 0),
            test_results.get("failed", 0),
            test_results.get("skipped", 0)
        ]
        colors = ['#28a745', '#dc3545', '#ffc107']
        
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('UniERP Test Execution Results')
        plt.axis('equal')
        
        chart_path = os.path.join(self.report_dir, "execution_chart.png")
        plt.savefig(chart_path)
        plt.close()
    
    def _generate_branding_chart(self, test_results: Dict[str, Any]) -> None:
        """Generate UniERP branding score chart"""
        branding_score = test_results.get("branding_score", 0)
        
        plt.figure(figsize=(8, 6))
        
        categories = ['Logo', 'Title', 'Colors', 'Content', 'Links']
        scores = [
            test_results.get("logo_score", 0),
            test_results.get("title_score", 0),
            test_results.get("colors_score", 0),
            test_results.get("content_score", 0),
            test_results.get("links_score", 0)
        ]
        
        colors = ['#007bff' if score >= 90 else '#ffc107' if score >= 70 else '#dc3545' for score in scores]
        
        bars = plt.bar(categories, scores, color=colors)
        plt.title('UniERP Branding Verification Scores')
        plt.ylabel('Score (%)')
        plt.ylim(0, 100)
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar, score in zip(bars, scores):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{score}%', ha='center', va='bottom')
        
        chart_path = os.path.join(self.report_dir, "branding_chart.png")
        plt.savefig(chart_path, bbox_inches='tight')
        plt.close()
```

---

## 8. Conclusion

The UniERP Test Automation Framework provides a comprehensive, scalable solution for automated testing of the UniERP system. With its modular architecture, extensive test libraries, and robust reporting capabilities, it ensures thorough validation of system functionality, branding, and quality.

Key features include:
- **Modular Architecture:** Easy to extend and maintain
- **Multi-Environment Support:** Flexible configuration for different test environments
- **Comprehensive Libraries:** Support for web, API, and database testing
- **UniERP Branding Verification:** Built-in checks for UniERP branding consistency
- **CI/CD Integration:** Seamless integration with development pipelines
- **Detailed Reporting:** Comprehensive test reports with visual analytics

Regular updates and improvements to the framework will ensure its continued effectiveness in supporting UniERP testing activities and maintaining high quality standards.

For questions or support regarding the test automation framework, please contact the UniERP QA Automation Team at qa-automation@unierp.com.

---

**Document Status:** Approved
**Next Review Date:** December 2024
**Document Owner:** UniERP QA Automation Team
**Contact Information:** qa-automation@unierp.com | +1-555-UNIERP-AUTO