#!/usr/bin/env python3
"""
Data Serialization Manager

A comprehensive project demonstrating various data serialization techniques in Python.
Supports JSON, Pickle, CSV, XML, and Binary formats with performance benchmarking.

Author: Gunjan Khatri
Date: 12 July 2025
"""

import json
import pickle
import csv
import xml.etree.ElementTree as ET
import struct
import time
import os
import gzip
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Union
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Employee:
    """Sample data class for demonstration"""
    id: int
    name: str
    department: str
    salary: float
    hire_date: str
    is_active: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Employee':
        """Create instance from dictionary"""
        return cls(**data)

class SerializationError(Exception):
    """Custom exception for serialization errors"""
    pass

class BaseSerializer(ABC):
    """Abstract base class for all serializers"""
    
    @abstractmethod
    def serialize(self, data: Any, filepath: str) -> bool:
        """Serialize data to file"""
        pass
    
    @abstractmethod
    def deserialize(self, filepath: str) -> Any:
        """Deserialize data from file"""
        pass
    
    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Return appropriate file extension"""
        pass

class JSONSerializer(BaseSerializer):
    """JSON serialization implementation"""
    
    def serialize(self, data: Any, filepath: str) -> bool:
        """Serialize data to JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if isinstance(data, list) and all(isinstance(item, Employee) for item in data):
                    # Convert Employee objects to dictionaries
                    json_data = [emp.to_dict() for emp in data]
                else:
                    json_data = data
                
                json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Successfully serialized data to {filepath}")
            return True
        except Exception as e:
            logger.error(f"JSON serialization failed: {e}")
            raise SerializationError(f"Failed to serialize to JSON: {e}")
    
    def deserialize(self, filepath: str) -> Any:
        """Deserialize data from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Successfully deserialized data from {filepath}")
            return data
        except Exception as e:
            logger.error(f"JSON deserialization failed: {e}")
            raise SerializationError(f"Failed to deserialize from JSON: {e}")
    
    @property
    def file_extension(self) -> str:
        return ".json"

class PickleSerializer(BaseSerializer):
    """Pickle serialization implementation with compression support"""
    
    def __init__(self, use_compression: bool = False):
        self.use_compression = use_compression
    
    def serialize(self, data: Any, filepath: str) -> bool:
        """Serialize data to pickle file with optional compression"""
        try:
            mode = 'wb'
            open_func = gzip.open if self.use_compression else open
            
            with open_func(filepath, mode) as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            logger.info(f"Successfully pickled data to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Pickle serialization failed: {e}")
            raise SerializationError(f"Failed to pickle data: {e}")
    
    def deserialize(self, filepath: str) -> Any:
        """Deserialize data from pickle file"""
        try:
            mode = 'rb'
            open_func = gzip.open if self.use_compression else open
            
            with open_func(filepath, mode) as f:
                data = pickle.load(f)
            
            logger.info(f"Successfully unpickled data from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Pickle deserialization failed: {e}")
            raise SerializationError(f"Failed to unpickle data: {e}")
    
    @property
    def file_extension(self) -> str:
        return ".pkl.gz" if self.use_compression else ".pkl"

class CSVSerializer(BaseSerializer):
    """CSV serialization implementation"""
    
    def serialize(self, data: List[Employee], filepath: str) -> bool:
        """Serialize Employee list to CSV file"""
        try:
            if not isinstance(data, list) or not all(isinstance(item, Employee) for item in data):
                raise ValueError("CSV serialization requires a list of Employee objects")
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                if data:
                    fieldnames = data[0].to_dict().keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for emp in data:
                        writer.writerow(emp.to_dict())
            
            logger.info(f"Successfully serialized {len(data)} employees to CSV: {filepath}")
            return True
        except Exception as e:
            logger.error(f"CSV serialization failed: {e}")
            raise SerializationError(f"Failed to serialize to CSV: {e}")
    
    def deserialize(self, filepath: str) -> List[Employee]:
        """Deserialize Employee list from CSV file"""
        try:
            employees = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convert string values to appropriate types
                    row['id'] = int(row['id'])
                    row['salary'] = float(row['salary'])
                    row['is_active'] = row['is_active'].lower() == 'true'
                    employees.append(Employee.from_dict(row))
            
            logger.info(f"Successfully deserialized {len(employees)} employees from CSV: {filepath}")
            return employees
        except Exception as e:
            logger.error(f"CSV deserialization failed: {e}")
            raise SerializationError(f"Failed to deserialize from CSV: {e}")
    
    @property
    def file_extension(self) -> str:
        return ".csv"

class XMLSerializer(BaseSerializer):
    """XML serialization implementation"""
    
    def serialize(self, data: List[Employee], filepath: str) -> bool:
        """Serialize Employee list to XML file"""
        try:
            if not isinstance(data, list) or not all(isinstance(item, Employee) for item in data):
                raise ValueError("XML serialization requires a list of Employee objects")
            
            root = ET.Element("employees")
            
            for emp in data:
                emp_elem = ET.SubElement(root, "employee")
                emp_dict = emp.to_dict()
                
                for key, value in emp_dict.items():
                    child = ET.SubElement(emp_elem, key)
                    child.text = str(value)
            
            tree = ET.ElementTree(root)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            
            logger.info(f"Successfully serialized {len(data)} employees to XML: {filepath}")
            return True
        except Exception as e:
            logger.error(f"XML serialization failed: {e}")
            raise SerializationError(f"Failed to serialize to XML: {e}")
    
    def deserialize(self, filepath: str) -> List[Employee]:
        """Deserialize Employee list from XML file"""
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            employees = []
            
            for emp_elem in root.findall("employee"):
                emp_data = {}
                for child in emp_elem:
                    value = child.text
                    # Convert to appropriate types
                    if child.tag in ['id']:
                        value = int(value)
                    elif child.tag in ['salary']:
                        value = float(value)
                    elif child.tag in ['is_active']:
                        value = value.lower() == 'true'
                    
                    emp_data[child.tag] = value
                
                employees.append(Employee.from_dict(emp_data))
            
            logger.info(f"Successfully deserialized {len(employees)} employees from XML: {filepath}")
            return employees
        except Exception as e:
            logger.error(f"XML deserialization failed: {e}")
            raise SerializationError(f"Failed to deserialize from XML: {e}")
    
    @property
    def file_extension(self) -> str:
        return ".xml"

class BinarySerializer(BaseSerializer):
    """Custom binary serialization implementation"""
    
    def serialize(self, data: List[Employee], filepath: str) -> bool:
        """Serialize Employee list to binary file"""
        try:
            if not isinstance(data, list) or not all(isinstance(item, Employee) for item in data):
                raise ValueError("Binary serialization requires a list of Employee objects")
            
            with open(filepath, 'wb') as f:
                # Write number of employees
                f.write(struct.pack('I', len(data)))
                
                for emp in data:
                    # Pack employee data
                    name_bytes = emp.name.encode('utf-8')
                    dept_bytes = emp.department.encode('utf-8')
                    hire_date_bytes = emp.hire_date.encode('utf-8')
                    
                    # Write lengths and data
                    f.write(struct.pack('I', emp.id))
                    f.write(struct.pack('I', len(name_bytes)))
                    f.write(name_bytes)
                    f.write(struct.pack('I', len(dept_bytes)))
                    f.write(dept_bytes)
                    f.write(struct.pack('d', emp.salary))
                    f.write(struct.pack('I', len(hire_date_bytes)))
                    f.write(hire_date_bytes)
                    f.write(struct.pack('?', emp.is_active))
            
            logger.info(f"Successfully serialized {len(data)} employees to binary: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Binary serialization failed: {e}")
            raise SerializationError(f"Failed to serialize to binary: {e}")
    
    def deserialize(self, filepath: str) -> List[Employee]:
        """Deserialize Employee list from binary file"""
        try:
            employees = []
            with open(filepath, 'rb') as f:
                # Read number of employees
                num_employees = struct.unpack('I', f.read(4))[0]
                
                for _ in range(num_employees):
                    # Read employee data
                    emp_id = struct.unpack('I', f.read(4))[0]
                    
                    name_len = struct.unpack('I', f.read(4))[0]
                    name = f.read(name_len).decode('utf-8')
                    
                    dept_len = struct.unpack('I', f.read(4))[0]
                    department = f.read(dept_len).decode('utf-8')
                    
                    salary = struct.unpack('d', f.read(8))[0]
                    
                    date_len = struct.unpack('I', f.read(4))[0]
                    hire_date = f.read(date_len).decode('utf-8')
                    
                    is_active = struct.unpack('?', f.read(1))[0]
                    
                    employees.append(Employee(emp_id, name, department, salary, hire_date, is_active))
            
            logger.info(f"Successfully deserialized {len(employees)} employees from binary: {filepath}")
            return employees
        except Exception as e:
            logger.error(f"Binary deserialization failed: {e}")
            raise SerializationError(f"Failed to deserialize from binary: {e}")
    
    @property
    def file_extension(self) -> str:
        return ".bin"

class SerializationManager:
    """Main class to manage different serialization formats"""
    
    def __init__(self, output_dir: str = "serialized_data"):
        self.output_dir = output_dir
        self.serializers = {
            'json': JSONSerializer(),
            'pickle': PickleSerializer(),
            'pickle_compressed': PickleSerializer(use_compression=True),
            'csv': CSVSerializer(),
            'xml': XMLSerializer(),
            'binary': BinarySerializer()
        }
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Initialized SerializationManager with output directory: {output_dir}")
    
    def generate_sample_data(self, num_employees: int = 1000) -> List[Employee]:
        """Generate sample employee data"""
        departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
        employees = []
        
        for i in range(1, num_employees + 1):
            emp = Employee(
                id=i,
                name=f"Employee_{i:04d}",
                department=departments[i % len(departments)],
                salary=round(40000 + (i * 100) + (i % 1000), 2),
                hire_date=f"2020-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
                is_active=(i % 10) != 0  # 90% active
            )
            employees.append(emp)
        
        logger.info(f"Generated {num_employees} sample employees")
        return employees
    
    def benchmark_serialization(self, data: List[Employee]) -> Dict[str, Dict[str, float]]:
        """Benchmark all serialization methods"""
        results = {}
        
        logger.info("Starting serialization benchmarks...")
        
        for name, serializer in self.serializers.items():
            filepath = os.path.join(self.output_dir, f"employees_{name}{serializer.file_extension}")
            
            try:
                # Serialize
                start_time = time.time()
                serializer.serialize(data, filepath)
                serialize_time = time.time() - start_time
                
                # Get file size
                file_size = os.path.getsize(filepath)
                
                # Deserialize
                start_time = time.time()
                deserialized_data = serializer.deserialize(filepath)
                deserialize_time = time.time() - start_time
                
                # Verify data integrity (for list data)
                if isinstance(deserialized_data, list) and len(deserialized_data) > 0:
                    data_integrity = len(data) == len(deserialized_data)
                else:
                    data_integrity = True
                
                results[name] = {
                    'serialize_time': serialize_time,
                    'deserialize_time': deserialize_time,
                    'total_time': serialize_time + deserialize_time,
                    'file_size_bytes': file_size,
                    'file_size_mb': file_size / (1024 * 1024),
                    'data_integrity': data_integrity
                }
                
                logger.info(f"Completed benchmark for {name}: "
                          f"{serialize_time:.3f}s serialize, "
                          f"{deserialize_time:.3f}s deserialize, "
                          f"{file_size / 1024:.1f}KB")
                
            except Exception as e:
                logger.error(f"Benchmark failed for {name}: {e}")
                results[name] = {'error': str(e)}
        
        return results
    
    def print_benchmark_results(self, results: Dict[str, Dict[str, float]]):
        """Print formatted benchmark results"""
        print("\n" + "="*80)
        print("SERIALIZATION BENCHMARK RESULTS")
        print("="*80)
        
        # Sort by total time
        sorted_results = sorted(
            [(k, v) for k, v in results.items() if 'error' not in v],
            key=lambda x: x[1]['total_time']
        )
        
        print(f"{'Format':<20} {'Serialize':<12} {'Deserialize':<12} {'Total':<10} {'Size(MB)':<10} {'Integrity':<10}")
        print("-" * 80)
        
        for name, metrics in sorted_results:
            print(f"{name:<20} "
                  f"{metrics['serialize_time']:<12.3f} "
                  f"{metrics['deserialize_time']:<12.3f} "
                  f"{metrics['total_time']:<10.3f} "
                  f"{metrics['file_size_mb']:<10.2f} "
                  f"{'✓' if metrics['data_integrity'] else '✗':<10}")
        
        # Print errors
        errors = [(k, v) for k, v in results.items() if 'error' in v]
        if errors:
            print("\nErrors:")
            for name, error_info in errors:
                print(f"  {name}: {error_info['error']}")
    
    def demonstrate_features(self):
        """Demonstrate various serialization features"""
        print("\n" + "="*60)
        print("SERIALIZATION FEATURE DEMONSTRATION")
        print("="*60)
        
        # Generate sample data
        employees = self.generate_sample_data(100)
        
        # Demonstrate JSON serialization with custom objects
        json_serializer = self.serializers['json']
        json_path = os.path.join(self.output_dir, "demo_employees.json")
        json_serializer.serialize(employees[:5], json_path)
        
        # Load and display
        loaded_data = json_serializer.deserialize(json_path)
        print(f"JSON Demo: Loaded {len(loaded_data)} employees")
        print(f"First employee: {loaded_data[0]}")
        
        # Demonstrate pickle with custom objects
        pickle_serializer = self.serializers['pickle']
        pickle_path = os.path.join(self.output_dir, "demo_employees.pkl")
        pickle_serializer.serialize(employees[:5], pickle_path)
        
        loaded_employees = pickle_serializer.deserialize(pickle_path)
        print(f"\nPickle Demo: Loaded {len(loaded_employees)} Employee objects")
        print(f"First employee type: {type(loaded_employees[0])}")
        print(f"First employee: {loaded_employees[0]}")

def main():
    """Main function to demonstrate the serialization system"""
    print("Data Serialization Manager Demo")
    print("===============================")
    
    # Initialize manager
    manager = SerializationManager()
    
    # Generate sample data
    sample_data = manager.generate_sample_data(1000)
    
    # Run benchmarks
    results = manager.benchmark_serialization(sample_data)
    
    # Display results
    manager.print_benchmark_results(results)
    
    # Demonstrate features
    manager.demonstrate_features()
    
    print(f"\nAll serialized files saved to: {manager.output_dir}/")
    print("Demo completed successfully!")

if __name__ == "__main__":
    main()