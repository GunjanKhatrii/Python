#!/usr/bin/env python3
"""
Inter-Process Communication & File Processing System

A comprehensive system demonstrating various IPC mechanisms and file I/O operations.
Features include process pools, queues, pipes, shared memory, and advanced file handling.

Author: Gunjan Khatri
Date: 1 March 2025
"""

import os
import sys
import time
import json
import csv
import pickle
import mmap
import threading
import multiprocessing as mp
from multiprocessing import Process, Queue, Pipe, Value, Array, Lock
from multiprocessing import shared_memory, Pool, Manager
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from queue import Empty
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
import logging
from pathlib import Path
import hashlib
import shutil
from datetime import datetime
import signal
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ipc_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class FileTask:
    """Data class representing a file processing task"""
    task_id: str
    file_path: str
    operation: str  # 'read', 'write', 'process', 'analyze'
    parameters: Dict[str, Any]
    priority: int = 1
    timestamp: float = 0.0
    
    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ProcessingResult:
    """Data class for processing results"""
    task_id: str
    success: bool
    result: Any
    error_message: str = ""
    processing_time: float = 0.0
    worker_pid: int = 0

class FileProcessor:
    """Base class for file processing operations"""
    
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.processed_files = 0
        
    def read_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """Read text file content"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            raise IOError(f"Failed to read file {file_path}: {e}")
    
    def write_file(self, file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """Write content to text file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            raise IOError(f"Failed to write file {file_path}: {e}")
    
    def read_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """Read CSV file and return list of dictionaries"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            raise IOError(f"Failed to read CSV {file_path}: {e}")
    
    def write_csv(self, file_path: str, data: List[Dict[str, Any]]) -> bool:
        """Write data to CSV file"""
        try:
            if not data:
                return False
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            raise IOError(f"Failed to write CSV {file_path}: {e}")
    
    def read_json(self, file_path: str) -> Dict[str, Any]:
        """Read JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise IOError(f"Failed to read JSON {file_path}: {e}")
    
    def write_json(self, file_path: str, data: Dict[str, Any]) -> bool:
        """Write data to JSON file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            raise IOError(f"Failed to write JSON {file_path}: {e}")
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze file properties"""
        try:
            stat = os.stat(file_path)
            
            # Calculate file hash
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            
            # Count lines if text file
            line_count = 0
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    line_count = sum(1 for _ in f)
            except:
                line_count = -1  # Binary file
            
            return {
                'file_path': file_path,
                'size_bytes': stat.st_size,
                'size_mb': stat.st_size / (1024 * 1024),
                'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'md5_hash': hash_md5.hexdigest(),
                'line_count': line_count,
                'is_text': line_count > -1
            }
        except Exception as e:
            raise IOError(f"Failed to analyze file {file_path}: {e}")

def worker_process_queue(worker_id: int, task_queue: Queue, result_queue: Queue, 
                        shared_counter: Value, lock: Lock):
    """Worker process that processes tasks from a queue"""
    processor = FileProcessor(f"Worker-{worker_id}")
    logger.info(f"Worker {worker_id} started (PID: {os.getpid()})")
    
    while True:
        try:
            # Get task from queue with timeout
            task = task_queue.get(timeout=5)
            
            if task is None:  # Poison pill to stop worker
                logger.info(f"Worker {worker_id} received stop signal")
                break
            
            start_time = time.time()
            
            try:
                # Process the task based on operation type
                if task.operation == 'read':
                    if task.file_path.endswith('.csv'):
                        result = processor.read_csv(task.file_path)
                    elif task.file_path.endswith('.json'):
                        result = processor.read_json(task.file_path)
                    else:
                        result = processor.read_file(task.file_path)
                
                elif task.operation == 'write':
                    content = task.parameters.get('content', '')
                    if task.file_path.endswith('.csv'):
                        result = processor.write_csv(task.file_path, content)
                    elif task.file_path.endswith('.json'):
                        result = processor.write_json(task.file_path, content)
                    else:
                        result = processor.write_file(task.file_path, content)
                
                elif task.operation == 'analyze':
                    result = processor.analyze_file(task.file_path)
                
                elif task.operation == 'process':
                    # Custom processing based on file type
                    if task.file_path.endswith('.txt'):
                        content = processor.read_file(task.file_path)
                        # Word count analysis
                        words = content.split()
                        result = {
                            'word_count': len(words),
                            'char_count': len(content),
                            'line_count': content.count('\n') + 1,
                            'unique_words': len(set(word.lower().strip('.,!?;:') for word in words))
                        }
                    else:
                        result = processor.analyze_file(task.file_path)
                
                else:
                    raise ValueError(f"Unknown operation: {task.operation}")
                
                processing_time = time.time() - start_time
                
                # Update shared counter
                with lock:
                    shared_counter.value += 1
                
                # Send result back
                processing_result = ProcessingResult(
                    task_id=task.task_id,
                    success=True,
                    result=result,
                    processing_time=processing_time,
                    worker_pid=os.getpid()
                )
                
                result_queue.put(processing_result)
                logger.info(f"Worker {worker_id} completed task {task.task_id} in {processing_time:.3f}s")
                
            except Exception as e:
                error_result = ProcessingResult(
                    task_id=task.task_id,
                    success=False,
                    result=None,
                    error_message=str(e),
                    worker_pid=os.getpid()
                )
                result_queue.put(error_result)
                logger.error(f"Worker {worker_id} failed task {task.task_id}: {e}")
        
        except Empty:
            # Timeout on getting task - continue loop
            continue
        except Exception as e:
            logger.error(f"Worker {worker_id} encountered error: {e}")
            break
    
    logger.info(f"Worker {worker_id} shutting down")

def pipe_worker(conn: mp.Connection, worker_id: int):
    """Worker that communicates via pipes"""
    processor = FileProcessor(f"PipeWorker-{worker_id}")
    logger.info(f"Pipe worker {worker_id} started (PID: {os.getpid()})")
    
    try:
        while True:
            # Receive task through pipe
            task_data = conn.recv()
            
            if task_data is None:
                break
            
            task = FileTask(**task_data)
            start_time = time.time()
            
            try:
                if task.operation == 'analyze':
                    result = processor.analyze_file(task.file_path)
                else:
                    result = f"Processed {task.file_path} with operation {task.operation}"
                
                processing_time = time.time() - start_time
                
                response = {
                    'task_id': task.task_id,
                    'success': True,
                    'result': result,
                    'processing_time': processing_time,
                    'worker_pid': os.getpid()
                }
                
                conn.send(response)
                logger.info(f"Pipe worker {worker_id} completed task {task.task_id}")
                
            except Exception as e:
                error_response = {
                    'task_id': task.task_id,
                    'success': False,
                    'error_message': str(e),
                    'worker_pid': os.getpid()
                }
                conn.send(error_response)
                logger.error(f"Pipe worker {worker_id} failed task {task.task_id}: {e}")
    
    except EOFError:
        logger.info(f"Pipe worker {worker_id} connection closed")
    except Exception as e:
        logger.error(f"Pipe worker {worker_id} error: {e}")
    finally:
        conn.close()
        logger.info(f"Pipe worker {worker_id} shutting down")

class SharedMemoryFileProcessor:
    """Processor that uses shared memory for large data operations"""
    
    def __init__(self, shared_data_name: str, data_size: int):
        self.shared_data_name = shared_data_name
        self.data_size = data_size
        self.shared_mem = None
    
    def create_shared_memory(self) -> bool:
        """Create shared memory block"""
        try:
            self.shared_mem = shared_memory.SharedMemory(
                create=True, 
                size=self.data_size,
                name=self.shared_data_name
            )
            logger.info(f"Created shared memory block: {self.shared_data_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create shared memory: {e}")
            return False
    
    def attach_shared_memory(self) -> bool:
        """Attach to existing shared memory block"""
        try:
            self.shared_mem = shared_memory.SharedMemory(
                name=self.shared_data_name
            )
            logger.info(f"Attached to shared memory block: {self.shared_data_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to attach to shared memory: {e}")
            return False
    
    def write_to_shared_memory(self, data: bytes, offset: int = 0) -> bool:
        """Write data to shared memory"""
        try:
            if not self.shared_mem:
                return False
            
            if len(data) + offset > self.data_size:
                raise ValueError("Data too large for shared memory block")
            
            self.shared_mem.buf[offset:offset + len(data)] = data
            return True
        except Exception as e:
            logger.error(f"Failed to write to shared memory: {e}")
            return False
    
    def read_from_shared_memory(self, size: int, offset: int = 0) -> bytes:
        """Read data from shared memory"""
        try:
            if not self.shared_mem:
                return b''
            
            return bytes(self.shared_mem.buf[offset:offset + size])
        except Exception as e:
            logger.error(f"Failed to read from shared memory: {e}")
            return b''
    
    def cleanup(self):
        """Clean up shared memory"""
        if self.shared_mem:
            try:
                self.shared_mem.close()
                self.shared_mem.unlink()
                logger.info(f"Cleaned up shared memory: {self.shared_data_name}")
            except Exception as e:
                logger.error(f"Failed to cleanup shared memory: {e}")

def shared_memory_worker(shared_mem_name: str, data_size: int, task_queue: Queue, result_queue: Queue):
    """Worker that uses shared memory for processing large files"""
    processor = SharedMemoryFileProcessor(shared_mem_name, data_size)
    
    if not processor.attach_shared_memory():
        logger.error("Failed to attach to shared memory")
        return
    
    logger.info(f"Shared memory worker started (PID: {os.getpid()})")
    
    while True:
        try:
            task = task_queue.get(timeout=5)
            
            if task is None:
                break
            
            try:
                if task.operation == 'process_large_file':
                    # Read file in chunks and process through shared memory
                    file_path = task.file_path
                    chunk_size = min(data_size, 1024 * 1024)  # 1MB chunks
                    
                    results = []
                    with open(file_path, 'rb') as f:
                        while True:
                            chunk = f.read(chunk_size)
                            if not chunk:
                                break
                            
                            # Write chunk to shared memory
                            processor.write_to_shared_memory(chunk)
                            
                            # Read back and process (simulate processing)
                            processed_chunk = processor.read_from_shared_memory(len(chunk))
                            
                            # Simple processing: count bytes
                            results.append(len(processed_chunk))
                    
                    result = {
                        'total_chunks': len(results),
                        'total_bytes': sum(results),
                        'file_path': file_path
                    }
                else:
                    result = f"Processed {task.file_path}"
                
                processing_result = ProcessingResult(
                    task_id=task.task_id,
                    success=True,
                    result=result,
                    worker_pid=os.getpid()
                )
                result_queue.put(processing_result)
                
            except Exception as e:
                error_result = ProcessingResult(
                    task_id=task.task_id,
                    success=False,
                    result=None,
                    error_message=str(e),
                    worker_pid=os.getpid()
                )
                result_queue.put(error_result)
        
        except Empty:
            continue
        except Exception as e:
            logger.error(f"Shared memory worker error: {e}")
            break
    
    logger.info("Shared memory worker shutting down")

class IPCFileProcessingSystem:
    """Main system orchestrating IPC and file processing"""
    
    def __init__(self, num_workers: int = 4, output_dir: str = "output"):
        self.num_workers = num_workers
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # IPC components
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.shared_counter = Value('i', 0)
        self.lock = Lock()
        
        # Process management
        self.workers = []
        self.manager = Manager()
        self.shared_data = self.manager.dict()
        
        # Statistics
        self.stats = {
            'tasks_submitted': 0,
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_processing_time': 0.0
        }
        
        logger.info(f"Initialized IPC system with {num_workers} workers")
    
    def create_sample_files(self) -> List[str]:
        """Create sample files for testing"""
        sample_dir = self.output_dir / "samples"
        sample_dir.mkdir(exist_ok=True)
        
        files = []
        
        # Create text files
        for i in range(5):
            file_path = sample_dir / f"sample_{i}.txt"
            content = f"This is sample file {i}\n" * (100 * (i + 1))
            content += f"Created at: {datetime.now()}\n"
            content += f"File number: {i}\n"
            content += "Lorem ipsum " * 50
            
            with open(file_path, 'w') as f:
                f.write(content)
            files.append(str(file_path))
        
        # Create CSV file
        csv_path = sample_dir / "sample_data.csv"
        csv_data = [
            {'id': i, 'name': f'Item_{i}', 'value': i * 10, 'category': f'Cat_{i % 3}'}
            for i in range(100)
        ]
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name', 'value', 'category'])
            writer.writeheader()
            writer.writerows(csv_data)
        files.append(str(csv_path))
        
        # Create JSON file
        json_path = sample_dir / "sample_config.json"
        json_data = {
            'version': '1.0',
            'settings': {
                'debug': True,
                'max_workers': self.num_workers,
                'timeout': 30
            },
            'data': [{'id': i, 'value': i ** 2} for i in range(20)]
        }
        
        with open(json_path, 'w') as f:
            json.dump(json_data, f, indent=2)
        files.append(str(json_path))
        
        # Create large binary file for shared memory testing
        large_file_path = sample_dir / "large_file.bin"
        with open(large_file_path, 'wb') as f:
            # Write 5MB of random data
            for _ in range(5 * 1024):
                f.write(os.urandom(1024))
        files.append(str(large_file_path))
        
        logger.info(f"Created {len(files)} sample files")
        return files
    
    def start_workers(self):
        """Start worker processes"""
        for i in range(self.num_workers):
            worker = Process(
                target=worker_process_queue,
                args=(i, self.task_queue, self.result_queue, self.shared_counter, self.lock)
            )
            worker.start()
            self.workers.append(worker)
        
        logger.info(f"Started {len(self.workers)} worker processes")
    
    def stop_workers(self):
        """Stop all worker processes"""
        # Send poison pills
        for _ in self.workers:
            self.task_queue.put(None)
        
        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=5)
            if worker.is_alive():
                logger.warning(f"Force terminating worker {worker.pid}")
                worker.terminate()
        
        self.workers.clear()
        logger.info("All workers stopped")
    
    def submit_task(self, task: FileTask):
        """Submit a task for processing"""
        self.task_queue.put(task)
        self.stats['tasks_submitted'] += 1
        logger.debug(f"Submitted task {task.task_id}")
    
    def collect_results(self, expected_count: int, timeout: int = 60) -> List[ProcessingResult]:
        """Collect processing results"""
        results = []
        start_time = time.time()
        
        while len(results) < expected_count:
            if time.time() - start_time > timeout:
                logger.warning(f"Timeout waiting for results. Got {len(results)}/{expected_count}")
                break
            
            try:
                result = self.result_queue.get(timeout=1)
                results.append(result)
                
                if result.success:
                    self.stats['tasks_completed'] += 1
                    self.stats['total_processing_time'] += result.processing_time
                else:
                    self.stats['tasks_failed'] += 1
                
            except Empty:
                continue
        
        return results
    
    def demonstrate_queues(self, files: List[str]):
        """Demonstrate queue-based IPC"""
        logger.info("=== Demonstrating Queue-based IPC ===")
        
        self.start_workers()
        
        # Submit various tasks
        tasks = []
        for i, file_path in enumerate(files):
            if file_path.endswith('.txt'):
                task = FileTask(
                    task_id=f"process_{i}",
                    file_path=file_path,
                    operation='process',
                    parameters={}
                )
            else:
                task = FileTask(
                    task_id=f"analyze_{i}",
                    file_path=file_path,
                    operation='analyze',
                    parameters={}
                )
            
            tasks.append(task)
            self.submit_task(task)
        
        # Collect results
        results = self.collect_results(len(tasks))
        
        # Display results
        print(f"\nProcessed {len(results)} files using queue-based IPC:")
        for result in results:
            if result.success:
                print(f"✓ Task {result.task_id} (Worker PID: {result.worker_pid}) - "
                      f"Time: {result.processing_time:.3f}s")
            else:
                print(f"✗ Task {result.task_id} - Error: {result.error_message}")
        
        self.stop_workers()
        
        with self.lock:
            print(f"\nShared counter value: {self.shared_counter.value}")
    
    def demonstrate_pipes(self, files: List[str]):
        """Demonstrate pipe-based IPC"""
        logger.info("=== Demonstrating Pipe-based IPC ===")
        
        # Create pipe workers
        pipes = []
        workers = []
        
        for i in range(min(3, len(files))):
            parent_conn, child_conn = Pipe()
            worker = Process(target=pipe_worker, args=(child_conn, i))
            worker.start()
            
            pipes.append(parent_conn)
            workers.append(worker)
        
        # Send tasks through pipes
        results = []
        for i, (file_path, pipe) in enumerate(zip(files[:3], pipes)):
            task_data = {
                'task_id': f"pipe_task_{i}",
                'file_path': file_path,
                'operation': 'analyze',
                'parameters': {},
                'priority': 1,
                'timestamp': time.time()
            }
            
            pipe.send(task_data)
            result = pipe.recv()
            results.append(result)
        
        # Stop workers
        for pipe in pipes:
            pipe.send(None)
            pipe.close()
        
        for worker in workers:
            worker.join()
        
        # Display results
        print(f"\nProcessed {len(results)} files using pipe-based IPC:")
        for result in results:
            if result['success']:
                print(f"✓ Task {result['task_id']} (Worker PID: {result['worker_pid']}) - "
                      f"Time: {result['processing_time']:.3f}s")
            else:
                print(f"✗ Task {result['task_id']} - Error: {result['error_message']}")
    
    def demonstrate_shared_memory(self, large_file: str):
        """Demonstrate shared memory IPC"""
        logger.info("=== Demonstrating Shared Memory IPC ===")
        
        shared_mem_name = "file_processing_shared_mem"
        data_size = 2 * 1024 * 1024  # 2MB
        
        # Create shared memory
        processor = SharedMemoryFileProcessor(shared_mem_name, data_size)
        if not processor.create_shared_memory():
            logger.error("Failed to create shared memory")
            return
        
        try:
            # Start shared memory worker
            task_queue = Queue()
            result_queue = Queue()
            
            worker = Process(
                target=shared_memory_worker,
                args=(shared_mem_name, data_size, task_queue, result_queue)
            )
            worker.start()
            
            # Submit task
            task = FileTask(
                task_id="shared_mem_task",
                file_path=large_file,
                operation='process_large_file',
                parameters={}
            )
            
            start_time = time.time()
            task_queue.put(task)
            
            # Get result
            try:
                result = result_queue.get(timeout=30)
                processing_time = time.time() - start_time
                
                if result.success:
                    print(f"\n✓ Shared memory processing completed:")
                    print(f"  Worker PID: {result.worker_pid}")
                    print(f"  Total processing time: {processing_time:.3f}s")
                    if isinstance(result.result, dict):
                        for key, value in result.result.items():
                            print(f"  {key}: {value}")
                else:
                    print(f"✗ Shared memory processing failed: {result.error_message}")
                
            except Empty:
                print("Timeout waiting for shared memory result")
            
            # Stop worker
            task_queue.put(None)
            worker.join()
            
        finally:
            processor.cleanup()
    
    def demonstrate_process_pool(self, files: List[str]):
        """Demonstrate ProcessPoolExecutor"""
        logger.info("=== Demonstrating Process Pool Executor ===")
        
        def analyze_file_task(file_path: str) -> Dict[str, Any]:
            processor = FileProcessor("PoolWorker")
            return processor.analyze_file(file_path)
        
        # Use ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            start_time = time.time()
            
            # Submit all tasks
            future_to_file = {
                executor.submit(analyze_file_task, file_path): file_path 
                for file_path in files
            }
            
            results = []
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append((file_path, result, None))
                except Exception as e:
                    results.append((file_path, None, str(e)))
            
            total_time = time.time() - start_time
        
        # Display results
        print(f"\nProcessed {len(results)} files using ProcessPoolExecutor:")
        print(f"Total time: {total_time:.3f}s")
        
        for file_path, result, error in results:
            if error:
                print(f"✗ {os.path.basename(file_path)} - Error: {error}")
            else:
                print(f"✓ {os.path.basename(file_path)} - Size: {result['size_mb']:.2f}MB")
    
    def demonstrate_file_io_advanced(self):
        """Demonstrate advanced file I/O techniques"""
        logger.info("=== Demonstrating Advanced File I/O ===")
        
        # Memory-mapped file I/O
        test_file = self.output_dir / "mmap_test.txt"
        content = "This is a test for memory-mapped file I/O\n" * 1000
        
        # Write test file
        with open(test_file, 'w') as f:
            f.write(content)
        
        # Memory-mapped reading
        start_time = time.time()
        with open(test_file, 'r+') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                # Search in memory-mapped file
                line_count = mm[:].decode('utf-8').count('\n')
                word_count = len(mm[:].decode('utf-8').split())
        
        mmap_time = time.time() - start_time
        
        # Regular file reading for comparison
        start_time = time.time()
        with open(test_file, 'r') as f:
            content = f.read()
            line_count_regular = content.count('\n')
            word_count_regular = len(content.split())
        
        regular_time = time.time() - start_time
        
        print(f"\nMemory-mapped I/O vs Regular I/O:")
        print(f"Memory-mapped: {mmap_time:.4f}s - Lines: {line_count}, Words: {word_count}")
        print(f"Regular I/O:   {regular_time:.4f}s - Lines: {line_count_regular}, Words: {word_count_regular}")
        print(f"Speedup: {regular_time/mmap_time:.2f}x")
        
        # Atomic file operations
        atomic_file = self.output_dir / "atomic_test.json"
        temp_file = self.output_dir / "atomic_test.tmp"
        
        data = {'timestamp': datetime.now().isoformat(), 'data': list(range(100))}
        
        # Write to temporary file first, then rename (atomic operation)
        with open(temp_file, 'w') as f:
            json.dump(data, f)
        
        shutil.move(str(temp_file), str(atomic_file))
        print(f"✓ Atomic file write completed: {atomic_file}")
        
        # File locking demonstration
        lock_file = self.output_dir / "lock_test.txt"
        
        def write_with_lock(worker_id: int, shared_file: str, lock: threading.Lock):
            with lock:
                with open(shared_file, 'a') as f:
                    f.write(f"Worker {worker_id} wrote at {datetime.now()}\n")
                    time.sleep(0.1)  # Simulate processing
        
        # Multiple threads writing to same file with lock
        file_lock = threading.Lock()
        threads = []
        
        for i in range(5):
            thread = threading.Thread(
                target=write_with_lock,
                args=(i, str(lock_file), file_lock)
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        print(f"✓ File locking demonstration completed: {lock_file}")
    
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        report = {
            'system_info': {
                'cpu_count': mp.cpu_count(),
                'memory_gb': psutil.virtual_memory().total / (1024**3),
                'python_version': sys.version,
                'platform': sys.platform
            },
            'processing_stats': self.stats,
            'worker_performance': {
                'num_workers': self.num_workers,
                'avg_task_time': (
                    self.stats['total_processing_time'] / max(self.stats['tasks_completed'], 1)
                ),
                'success_rate': (
                    self.stats['tasks_completed'] / max(self.stats['tasks_submitted'], 1) * 100
                )
            }
        }
        
        # Save report
        report_file = self.output_dir / f"performance_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{'='*60}")
        print("PERFORMANCE REPORT")
        print(f"{'='*60}")
        print(f"Tasks submitted: {report['processing_stats']['tasks_submitted']}")
        print(f"Tasks completed: {report['processing_stats']['tasks_completed']}")
        print(f"Tasks failed: {report['processing_stats']['tasks_failed']}")
        print(f"Success rate: {report['worker_performance']['success_rate']:.1f}%")
        print(f"Average task time: {report['worker_performance']['avg_task_time']:.3f}s")
        print(f"Total processing time: {report['processing_stats']['total_processing_time']:.3f}s")
        print(f"Workers used: {report['worker_performance']['num_workers']}")
        print(f"CPU cores available: {report['system_info']['cpu_count']}")
        print(f"Memory available: {report['system_info']['memory_gb']:.1f} GB")
        print(f"Report saved: {report_file}")
        
        return report

def signal_handler(signum, frame):
    """Handle system signals gracefully"""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

def main():
    """Main function demonstrating all IPC and file I/O concepts"""
    print("Inter-Process Communication & File Processing System")
    print("="*60)
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize system
    system = IPCFileProcessingSystem(num_workers=4, output_dir="ipc_output")
    
    try:
        # Create sample files for testing
        print("Creating sample files...")
        sample_files = system.create_sample_files()
        print(f"Created {len(sample_files)} sample files")
        
        # Demonstrate different IPC mechanisms
        system.demonstrate_queues(sample_files)
        print("\n" + "="*60)
        
        system.demonstrate_pipes(sample_files)
        print("\n" + "="*60)
        
        # Find a large file for shared memory demo
        large_files = [f for f in sample_files if f.endswith('.bin')]
        if large_files:
            system.demonstrate_shared_memory(large_files[0])
            print("\n" + "="*60)
        
        system.demonstrate_process_pool(sample_files)
        print("\n" + "="*60)
        
        system.demonstrate_file_io_advanced()
        print("\n" + "="*60)
        
        # Generate performance report
        system.generate_performance_report()
        
        print(f"\nAll demonstrations completed successfully!")
        print(f"Check the output directory: {system.output_dir}")
        print(f"Check the log file: ipc_system.log")
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"System error: {e}")
        raise
    finally:
        # Cleanup
        system.stop_workers()
        logger.info("System shutdown completed")

if __name__ == "__main__":
    # Additional examples and utilities
    class AdvancedFileOperations:
        """Additional advanced file operations"""
        
        @staticmethod
        def batch_file_processor(file_paths: List[str], operation: str, 
                               max_workers: int = 4) -> Dict[str, Any]:
            """Process multiple files in batches"""
            results = {'success': [], 'failed': []}
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_file = {}
                
                for file_path in file_paths:
                    if operation == 'hash':
                        future = executor.submit(AdvancedFileOperations.calculate_hash, file_path)
                    elif operation == 'compress':
                        future = executor.submit(AdvancedFileOperations.compress_file, file_path)
                    elif operation == 'analyze':
                        future = executor.submit(AdvancedFileOperations.deep_analysis, file_path)
                    else:
                        continue
                    
                    future_to_file[future] = file_path
                
                for future in as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        result = future.result()
                        results['success'].append({'file': file_path, 'result': result})
                    except Exception as e:
                        results['failed'].append({'file': file_path, 'error': str(e)})
            
            return results
        
        @staticmethod
        def calculate_hash(file_path: str, algorithm: str = 'md5') -> str:
            """Calculate file hash using specified algorithm"""
            hash_func = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
        
        @staticmethod
        def compress_file(file_path: str, compression_level: int = 6) -> Dict[str, Any]:
            """Compress file and return compression statistics"""
            import gzip
            
            original_size = os.path.getsize(file_path)
            compressed_path = f"{file_path}.gz"
            
            with open(file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb', compresslevel=compression_level) as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            compressed_size = os.path.getsize(compressed_path)
            
            return {
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compressed_size / original_size,
                'space_saved': original_size - compressed_size,
                'compressed_path': compressed_path
            }
        
        @staticmethod
        def deep_analysis(file_path: str) -> Dict[str, Any]:
            """Perform deep file analysis"""
            stat = os.stat(file_path)
            
            analysis = {
                'path': file_path,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'permissions': oct(stat.st_mode)[-3:],
                'is_executable': os.access(file_path, os.X_OK),
                'file_type': 'unknown'
            }
            
            # Determine file type
            try:
                with open(file_path, 'rb') as f:
                    header = f.read(16)
                    
                    if header.startswith(b'PK'):
                        analysis['file_type'] = 'zip/office'
                    elif header.startswith(b'\x89PNG'):
                        analysis['file_type'] = 'png'
                    elif header.startswith(b'\xff\xd8\xff'):
                        analysis['file_type'] = 'jpeg'
                    elif header.startswith(b'GIF'):
                        analysis['file_type'] = 'gif'
                    elif header.startswith(b'%PDF'):
                        analysis['file_type'] = 'pdf'
                    elif b'\x00' not in header[:8]:
                        analysis['file_type'] = 'text'
                    else:
                        analysis['file_type'] = 'binary'
            except:
                pass
            
            # Text file analysis
            if analysis['file_type'] == 'text':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(10000)  # First 10KB
                        analysis['lines'] = content.count('\n')
                        analysis['words'] = len(content.split())
                        analysis['chars'] = len(content)
                except:
                    analysis['file_type'] = 'binary'
            
            return analysis
    
    # Run the main demonstration
    main()