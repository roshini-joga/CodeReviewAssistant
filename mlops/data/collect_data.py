import os
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict
import subprocess
import sys

def initialize_dvc():
    """Initialize DVC if not already initialized"""
    try:
        # Check if .dvc directory exists
        if not os.path.exists('.dvc'):
            print("Initializing DVC...")
            subprocess.run(['dvc', 'init'], check=True)
            print("DVC initialized successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing DVC: {e}")
        return False
    except FileNotFoundError:
        print("DVC is not installed. Please install it using: pip install dvc")
        return False
    return True

def get_mock_samples() -> List[Dict]:
    """Generate mock code samples for testing"""
    return [
        {
            "code": """
def calculate_factorial(n):
    if n < 0:
        return None
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
            """,
            "language": "python",
            "quality_score": 0.85,
            "has_bugs": False,
            "complexity": "low"
        },
        {
            "code": """
function findDuplicates(arr) {
    let duplicates = [];
    for(let i = 0; i < arr.length; i++) {
        for(let j = i + 1; j < arr.length; j++) {
            if(arr[i] === arr[j]) {
                duplicates.push(arr[i]);
            }
        }
    }
    return duplicates;
}
            """,
            "language": "javascript",
            "quality_score": 0.75,
            "has_bugs": True,
            "complexity": "medium"
        },
        {
            "code": """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    public int subtract(int a, int b) {
        return a - b;
    }
    
    public int multiply(int a, int b) {
        return a * b;
    }
    
    public double divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Division by zero");
        }
        return (double) a / b;
    }
}
            """,
            "language": "java",
            "quality_score": 0.90,
            "has_bugs": False,
            "complexity": "low"
        },
        {
            "code": """
def process_data(data):
    try:
        result = []
        for item in data:
            if item > 0:
                result.append(item * 2)
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None
            """,
            "language": "python",
            "quality_score": 0.70,
            "has_bugs": True,
            "complexity": "medium"
        },
        {
            "code": """
class User {
    constructor(name, email) {
        this.name = name;
        this.email = email;
    }
    
    validateEmail() {
        return this.email.includes('@');
    }
    
    getInfo() {
        return `${this.name} (${this.email})`;
    }
}
            """,
            "language": "javascript",
            "quality_score": 0.80,
            "has_bugs": False,
            "complexity": "low"
        },
        {
            "code": """
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib
            """,
            "language": "python",
            "quality_score": 0.95,
            "has_bugs": False,
            "complexity": "medium"
        },
        {
            "code": """
function sortArray(arr) {
    return arr.sort((a, b) => a - b);
}

function findMedian(arr) {
    const sorted = sortArray(arr);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 === 0 
        ? (sorted[mid-1] + sorted[mid]) / 2 
        : sorted[mid];
}
            """,
            "language": "javascript",
            "quality_score": 0.85,
            "has_bugs": False,
            "complexity": "medium"
        },
        {
            "code": """
public class StringUtils {
    public static boolean isPalindrome(String str) {
        if (str == null) return false;
        str = str.toLowerCase().replaceAll("[^a-z0-9]", "");
        int left = 0;
        int right = str.length() - 1;
        while (left < right) {
            if (str.charAt(left) != str.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}
            """,
            "language": "java",
            "quality_score": 0.88,
            "has_bugs": False,
            "complexity": "medium"
        },
        {
            "code": """
def validate_password(password):
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit
            """,
            "language": "python",
            "quality_score": 0.82,
            "has_bugs": False,
            "complexity": "low"
        },
        {
            "code": """
class Queue {
    constructor() {
        this.items = [];
    }
    
    enqueue(item) {
        this.items.push(item);
    }
    
    dequeue() {
        if (this.isEmpty()) {
            throw new Error("Queue is empty");
        }
        return this.items.shift();
    }
    
    isEmpty() {
        return this.items.length === 0;
    }
}
            """,
            "language": "javascript",
            "quality_score": 0.87,
            "has_bugs": False,
            "complexity": "low"
        }
    ]

def process_samples(samples: List[Dict]) -> pd.DataFrame:
    """Process collected samples into a structured format"""
    df = pd.DataFrame(samples)
    
    # Add additional processing if needed
    df['timestamp'] = datetime.now()
    df['review_status'] = 'pending'
    
    return df

def save_data(df: pd.DataFrame, path: str):
    """Save processed data"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Save the data
    df.to_csv(path, index=False)
    print(f"Data saved to {path}")
    
    # Try to add to DVC if it's initialized
    if initialize_dvc():
        try:
            subprocess.run(['dvc', 'add', path], check=True)
            print(f"Added {path} to DVC")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not add {path} to DVC: {e}")

def main():
    # Create data directories if they don't exist
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # Get mock samples
    samples = get_mock_samples()

    # Process samples
    df = process_samples(samples)

    # Save raw data
    raw_path = f"data/raw/samples_{datetime.now().strftime('%Y%m%d')}.csv"
    save_data(df, raw_path)

    # Save processed data
    processed_path = f"data/processed/processed_{datetime.now().strftime('%Y%m%d')}.csv"
    save_data(df, processed_path)

    print(f"Successfully saved {len(samples)} mock samples")

if __name__ == "__main__":
    main() 