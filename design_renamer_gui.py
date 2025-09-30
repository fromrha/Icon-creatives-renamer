import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import re
from pathlib import Path

class DesignRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Design File Renamer")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.folder_path = tk.StringVar()
        self.company_name = tk.StringVar()
        self.start_number = tk.StringVar(value="1")  # Add this line with default value of "1"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Folder selection
        ttk.Label(main_frame, text="Folder:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(0, weight=1)
        
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).grid(row=0, column=1)
        
        # Company name input
        ttk.Label(main_frame, text="Company Name:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.company_entry = ttk.Entry(main_frame, textvariable=self.company_name, width=30)
        self.company_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        
        # Start number input
        ttk.Label(main_frame, text="Start Hook Number:").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        self.start_number_entry = ttk.Entry(main_frame, textvariable=self.start_number, width=10)
        self.start_number_entry.grid(row=2, column=1, sticky=tk.W, pady=(0, 10))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 20))
        
        ttk.Button(button_frame, text="Preview Files", command=self.preview_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Rename Files", command=self.rename_files).pack(side=tk.LEFT)
        
        # Status label - Move this BELOW the button frame
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=4, column=0, columnspan=4, pady=(0, 10))
        
        # Log area - Update row number to 5 since we moved status label
        ttk.Label(main_frame, text="Log:").grid(row=5, column=0, sticky=(tk.W, tk.N))
        
        # Text widget with scrollbar - Update row number to 5
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=5, column=1, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(text_frame, height=15, width=60)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Update the rowconfigure to match new layout
        main_frame.rowconfigure(5, weight=1)
        
        # Set current directory as default
        self.folder_path.set(os.getcwd())
        
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def find_design_files(self):
        """Find all files matching the pattern: ratio (number).extension"""
        folder = self.folder_path.get()
        if not os.path.exists(folder):
            return []
        
        # Pattern to match: ratio (number).extension
        # Examples: 1x1 (1).jpg, 4x5 (2).png, 16x9 (10).jpeg
        pattern = r'^([a-zA-Z0-9x]+)\s*\((\d+)\)\.(jpg|jpeg|png|gif|bmp)$'
        
        files = []
        for filename in os.listdir(folder):
            match = re.match(pattern, filename, re.IGNORECASE)
            if match:
                ratio = match.group(1)
                number = int(match.group(2))
                extension = match.group(3)
                files.append({
                    'original': filename,
                    'ratio': ratio,
                    'number': number,
                    'extension': extension,
                    'path': os.path.join(folder, filename)
                })
        
        return sorted(files, key=lambda x: (x['number'], x['ratio']))
    
    def generate_new_name(self, file_info, company_name):
        """Generate new filename: companyname_hookN_ratio.extension"""
        start = int(self.start_number.get() or "1")  # Default to 1 if empty
        hook_number = start + file_info['number'] - 1  # Adjust the number based on start
        return f"{company_name}_hook{hook_number}_{file_info['ratio']}.{file_info['extension']}"
    
    def preview_files(self):
        self.clear_log()
        
        company_name = self.company_name.get().strip()
        if not company_name:
            messagebox.showerror("Error", "Please enter a company name")
            return
        
        files = self.find_design_files()
        if not files:
            self.log("No matching files found.")
            self.log("Looking for files with pattern: ratio (number).extension")
            self.log("Examples: 1x1 (1).jpg, 4x5 (2).png, 16x9 (3).jpeg")
            return
        
        self.log(f"Found {len(files)} files to rename:")
        self.log("-" * 50)
        
        for file_info in files:
            old_name = file_info['original']
            new_name = self.generate_new_name(file_info, company_name)
            self.log(f"{old_name} → {new_name}")
        
        self.status_var.set(f"Preview complete - {len(files)} files found")
    
    def rename_files(self):
        company_name = self.company_name.get().strip()
        if not company_name:
            messagebox.showerror("Error", "Please enter a company name")
            return
        
        files = self.find_design_files()
        if not files:
            messagebox.showerror("Error", "No matching files found in the selected folder")
            return
        
        # Confirm before renaming
        result = messagebox.askyesno(
            "Confirm Rename", 
            f"This will rename {len(files)} files. Continue?"
        )
        if not result:
            return
        
        self.clear_log()
        self.log(f"Starting rename process for {len(files)} files...")
        self.log("-" * 50)
        
        success_count = 0
        error_count = 0
        
        for file_info in files:
            try:
                old_path = file_info['path']
                new_name = self.generate_new_name(file_info, company_name)
                new_path = os.path.join(self.folder_path.get(), new_name)
                
                # Check if target file already exists
                if os.path.exists(new_path):
                    self.log(f"ERROR: Target file already exists - {new_name}")
                    error_count += 1
                    continue
                
                # Rename the file
                os.rename(old_path, new_path)
                self.log(f"✓ {file_info['original']} → {new_name}")
                success_count += 1
                
            except Exception as e:
                self.log(f"ERROR: Failed to rename {file_info['original']} - {str(e)}")
                error_count += 1
        
        self.log("-" * 50)
        self.log(f"Rename complete! Success: {success_count}, Errors: {error_count}")
        self.status_var.set(f"Rename complete - {success_count} successful, {error_count} errors")
        
        if success_count > 0:
            messagebox.showinfo("Success", f"Successfully renamed {success_count} files!")

def main():
    root = tk.Tk()
    app = DesignRenamer(root)
    root.mainloop()

if __name__ == "__main__":
    main()