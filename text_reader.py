#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TextReader - A Simple and Elegant Text Reader Application
Similar to NeatReader, designed for comfortable reading experience.

Features:
- Support for TXT and other text-based formats
- Customizable fonts (family, size, style)
- Customizable background and text colors
- Reading progress tracking
- Bookmarks
- Fullscreen mode
- Auto-scroll feature
- High-DPI/4K display support
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, font as tkfont
import json
import os
import sys
import ctypes
import re
from pathlib import Path


def enable_high_dpi_awareness():
    """
    Enable High-DPI awareness for Windows to fix blurry display on 4K screens.
    This must be called BEFORE creating any Tkinter windows.
    """
    if sys.platform == 'win32':
        try:
            # For Windows 10 version 1607+ (Anniversary Update)
            # PROCESS_PER_MONITOR_DPI_AWARE = 2
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except AttributeError:
            try:
                # For older Windows versions
                ctypes.windll.user32.SetProcessDPIAware()
            except AttributeError:
                pass
        except OSError:
            # Already set or not supported
            pass


class TextReader:
    """Main TextReader application class."""
    
    # Default settings
    DEFAULT_SETTINGS = {
        'font_family': 'SimSun',
        'font_size': 16,
        'font_weight': 'normal',
        'text_color': '#333333',
        'bg_color': '#F5F5DC',
        'line_spacing': 10,
        'window_width': 900,
        'window_height': 700,
        'last_file': '',
        'last_position': 0,
        'auto_scroll_speed': 50,
        'bookmarks': {},
        'recent_files': []
    }
    
    # Predefined color themes
    THEMES = {
        '护眼绿': {'bg': '#CCE8CF', 'text': '#333333'},
        '羊皮纸': {'bg': '#F5F5DC', 'text': '#333333'},
        '夜间模式': {'bg': '#1E1E1E', 'text': '#E0E0E0'},
        '暖白色': {'bg': '#FFF8E7', 'text': '#333333'},
        '淡蓝色': {'bg': '#E6F3FF', 'text': '#333333'},
        '纯白色': {'bg': '#FFFFFF', 'text': '#000000'},
        '深棕色': {'bg': '#3E2723', 'text': '#D7CCC8'},
        '海洋蓝': {'bg': '#0D47A1', 'text': '#E3F2FD'},
    }
    
    # Maximum length for chapter title (to filter out false positives)
    MAX_CHAPTER_TITLE_LENGTH = 50
    
    def __init__(self, root):
        """Initialize the TextReader application."""
        self.root = root
        self.root.title("TextReader - 文本阅读器")
        
        # Settings file path
        self.settings_file = Path.home() / '.textreader_settings.json'
        
        # Load settings
        self.settings = self.load_settings()
        
        # Current file info
        self.current_file = None
        self.current_content = ""
        
        # Auto-scroll state
        self.auto_scroll_active = False
        self.auto_scroll_speed = self.settings.get('auto_scroll_speed', 50)  # milliseconds between scroll
        
        # Search state
        self.search_matches = []
        self.current_match_index = -1
        self.search_frame_visible = False
        
        # Table of contents (chapters)
        self.chapters = []
        self.toc_visible = False
        
        # Setup UI
        self.setup_ui()
        self.setup_menu()
        self.setup_bindings()
        
        # Apply settings
        self.apply_settings()
        
        # Load last file if exists
        if self.settings.get('last_file') and os.path.exists(self.settings['last_file']):
            self.load_file(self.settings['last_file'])
            # Restore last reading position
            if self.settings.get('last_position', 0) > 0:
                self.root.after(100, lambda: self.text_widget.yview_moveto(self.settings['last_position']))
    
    def load_settings(self):
        """Load settings from file or use defaults."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # Merge with defaults for any missing keys
                    for key, value in self.DEFAULT_SETTINGS.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
        except Exception as e:
            print(f"Error loading settings: {e}")
        return self.DEFAULT_SETTINGS.copy()
    
    def save_settings(self):
        """Save current settings to file."""
        try:
            # Save current text position
            if self.current_file:
                self.settings['last_file'] = self.current_file
                self.settings['last_position'] = self.text_widget.yview()[0]
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def setup_ui(self):
        """Setup the main UI components."""
        # Configure root window
        self.root.geometry(f"{self.settings['window_width']}x{self.settings['window_height']}")
        self.root.minsize(600, 400)
        
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        self.setup_toolbar()
        
        # Search bar (hidden by default)
        self.setup_search_bar()
        
        # Content area with TOC and text
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Table of Contents sidebar (hidden by default)
        self.setup_toc_panel()
        
        # Text area with scrollbar
        self.text_frame = ttk.Frame(self.content_frame)
        self.text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget
        self.text_widget = tk.Text(
            self.text_frame,
            wrap=tk.WORD,
            yscrollcommand=self.scrollbar.set,
            state=tk.DISABLED,
            cursor="arrow",
            relief=tk.FLAT,
            padx=40,
            pady=20
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure search highlight tag
        self.text_widget.tag_configure('search_highlight', background='#FFFF00', foreground='#000000')
        self.text_widget.tag_configure('current_match', background='#FF6B00', foreground='#FFFFFF')
        
        self.scrollbar.config(command=self.text_widget.yview)
        
        # Status bar
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(self.status_frame, text="欢迎使用 TextReader！请打开一个文件开始阅读。")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.progress_label = ttk.Label(self.status_frame, text="")
        self.progress_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def setup_search_bar(self):
        """Setup the search bar UI."""
        self.search_frame = ttk.Frame(self.main_frame)
        # Not packed initially - shown when user presses Ctrl+F
        
        ttk.Label(self.search_frame, text="🔍 查找:").pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=2)
        self.search_entry.bind('<Return>', lambda e: self.find_next())
        self.search_entry.bind('<Escape>', lambda e: self.hide_search())
        self.search_var.trace('w', lambda *args: self.on_search_change())
        
        ttk.Button(self.search_frame, text="上一个", command=self.find_previous).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.search_frame, text="下一个", command=self.find_next).pack(side=tk.LEFT, padx=2)
        
        self.search_count_label = ttk.Label(self.search_frame, text="")
        self.search_count_label.pack(side=tk.LEFT, padx=10)
        
        # Case sensitive checkbox
        self.case_sensitive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.search_frame, text="区分大小写", variable=self.case_sensitive_var, 
                       command=self.on_search_change).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.search_frame, text="✕", width=3, command=self.hide_search).pack(side=tk.RIGHT, padx=5)
    
    def setup_toc_panel(self):
        """Setup the Table of Contents sidebar."""
        self.toc_frame = ttk.Frame(self.content_frame, width=250)
        # Not packed initially - shown when user clicks TOC button
        
        # TOC header
        toc_header = ttk.Frame(self.toc_frame)
        toc_header.pack(fill=tk.X, pady=5)
        
        ttk.Label(toc_header, text="📚 目录", font=('', 11, 'bold')).pack(side=tk.LEFT, padx=10)
        ttk.Button(toc_header, text="✕", width=3, command=self.toggle_toc).pack(side=tk.RIGHT, padx=5)
        
        # Refresh button
        ttk.Button(toc_header, text="🔄", width=3, command=self.refresh_toc).pack(side=tk.RIGHT, padx=2)
        
        ttk.Separator(self.toc_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5)
        
        # TOC listbox with scrollbar
        toc_list_frame = ttk.Frame(self.toc_frame)
        toc_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        toc_scrollbar = ttk.Scrollbar(toc_list_frame)
        toc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.toc_listbox = tk.Listbox(
            toc_list_frame,
            yscrollcommand=toc_scrollbar.set,
            font=('', 10),
            selectmode=tk.SINGLE,
            activestyle='none'
        )
        self.toc_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.toc_listbox.bind('<Double-1>', self.on_toc_select)
        self.toc_listbox.bind('<Return>', self.on_toc_select)
        
        toc_scrollbar.config(command=self.toc_listbox.yview)
    
    def setup_toolbar(self):
        """Setup the toolbar with quick actions."""
        self.toolbar = ttk.Frame(self.main_frame)
        self.toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Open button
        ttk.Button(self.toolbar, text="📂 打开", command=self.open_file).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Font size controls
        ttk.Label(self.toolbar, text="字号:").pack(side=tk.LEFT, padx=2)
        
        self.font_size_var = tk.StringVar(value=str(self.settings['font_size']))
        self.font_size_spinbox = ttk.Spinbox(
            self.toolbar,
            from_=8,
            to=72,
            width=5,
            textvariable=self.font_size_var,
            command=self.on_font_size_change
        )
        self.font_size_spinbox.pack(side=tk.LEFT, padx=2)
        self.font_size_spinbox.bind('<Return>', lambda e: self.on_font_size_change())
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Font family dropdown
        ttk.Label(self.toolbar, text="字体:").pack(side=tk.LEFT, padx=2)
        
        self.available_fonts = sorted(set(tkfont.families()))
        self.font_family_var = tk.StringVar(value=self.settings['font_family'])
        self.font_combobox = ttk.Combobox(
            self.toolbar,
            textvariable=self.font_family_var,
            values=self.available_fonts,
            width=15,
            state='readonly'
        )
        self.font_combobox.pack(side=tk.LEFT, padx=2)
        self.font_combobox.bind('<<ComboboxSelected>>', lambda e: self.on_font_change())
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Theme dropdown
        ttk.Label(self.toolbar, text="主题:").pack(side=tk.LEFT, padx=2)
        
        self.theme_var = tk.StringVar(value='羊皮纸')
        self.theme_combobox = ttk.Combobox(
            self.toolbar,
            textvariable=self.theme_var,
            values=list(self.THEMES.keys()),
            width=10,
            state='readonly'
        )
        self.theme_combobox.pack(side=tk.LEFT, padx=2)
        self.theme_combobox.bind('<<ComboboxSelected>>', lambda e: self.apply_theme())
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Custom color buttons
        ttk.Button(self.toolbar, text="🎨 背景", command=self.choose_bg_color).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="🖌️ 文字", command=self.choose_text_color).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Search button
        ttk.Button(self.toolbar, text="🔍 查找", command=self.show_search).pack(side=tk.LEFT, padx=2)
        
        # TOC button
        ttk.Button(self.toolbar, text="📚 目录", command=self.toggle_toc).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Auto-scroll toggle
        self.auto_scroll_btn = ttk.Button(self.toolbar, text="▶ 自动滚动", command=self.toggle_auto_scroll)
        self.auto_scroll_btn.pack(side=tk.LEFT, padx=2)
        
        # Fullscreen button
        ttk.Button(self.toolbar, text="⛶ 全屏", command=self.toggle_fullscreen).pack(side=tk.RIGHT, padx=2)
    
    def setup_menu(self):
        """Setup the menu bar."""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="打开...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        
        # Recent files submenu
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="最近文件", menu=self.recent_menu)
        self.update_recent_menu()
        
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_close, accelerator="Alt+F4")
        
        # View menu
        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_command(label="增大字号", command=self.increase_font_size, accelerator="Ctrl++")
        view_menu.add_command(label="减小字号", command=self.decrease_font_size, accelerator="Ctrl+-")
        view_menu.add_separator()
        view_menu.add_command(label="全屏模式", command=self.toggle_fullscreen, accelerator="F11")
        view_menu.add_command(label="隐藏工具栏", command=self.toggle_toolbar, accelerator="Ctrl+T")
        view_menu.add_separator()
        view_menu.add_command(label="显示/隐藏目录", command=self.toggle_toc, accelerator="Ctrl+L")
        
        # Edit menu (for search)
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="查找...", command=self.show_search, accelerator="Ctrl+F")
        edit_menu.add_command(label="查找下一个", command=self.find_next, accelerator="F3")
        edit_menu.add_command(label="查找上一个", command=self.find_previous, accelerator="Shift+F3")
        
        # Navigate menu
        nav_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="导航", menu=nav_menu)
        nav_menu.add_command(label="跳转到开头", command=self.goto_start, accelerator="Home")
        nav_menu.add_command(label="跳转到结尾", command=self.goto_end, accelerator="End")
        nav_menu.add_separator()
        nav_menu.add_command(label="跳转到位置...", command=self.goto_position, accelerator="Ctrl+G")
        nav_menu.add_separator()
        nav_menu.add_command(label="目录...", command=self.toggle_toc, accelerator="Ctrl+L")
        nav_menu.add_separator()
        nav_menu.add_command(label="添加书签", command=self.add_bookmark, accelerator="Ctrl+B")
        nav_menu.add_command(label="管理书签...", command=self.manage_bookmarks)
        
        # Settings menu
        settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="设置", menu=settings_menu)
        settings_menu.add_command(label="字体设置...", command=self.open_font_settings)
        settings_menu.add_command(label="颜色设置...", command=self.open_color_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="行间距设置...", command=self.open_line_spacing_settings)
        settings_menu.add_command(label="自动滚动速度...", command=self.open_scroll_speed_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="恢复默认设置", command=self.reset_settings)
        
        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="快捷键列表", command=self.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="关于", command=self.show_about)
    
    def setup_bindings(self):
        """Setup keyboard shortcuts and event bindings."""
        # File operations
        self.root.bind('<Control-o>', lambda e: self.open_file())
        
        # Font size
        self.root.bind('<Control-plus>', lambda e: self.increase_font_size())
        self.root.bind('<Control-minus>', lambda e: self.decrease_font_size())
        self.root.bind('<Control-equal>', lambda e: self.increase_font_size())
        
        # Search
        self.root.bind('<Control-f>', lambda e: self.show_search())
        self.root.bind('<F3>', lambda e: self.find_next())
        self.root.bind('<Shift-F3>', lambda e: self.find_previous())
        self.root.bind('<Control-l>', lambda e: self.toggle_toc())
        
        # Navigation
        self.root.bind('<Home>', lambda e: self.goto_start())
        self.root.bind('<End>', lambda e: self.goto_end())
        self.root.bind('<Control-g>', lambda e: self.goto_position())
        self.root.bind('<Control-b>', lambda e: self.add_bookmark())
        
        # View
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self.on_escape())
        self.root.bind('<Control-t>', lambda e: self.toggle_toolbar())
        
        # Scrolling
        self.root.bind('<space>', lambda e: self.page_down())
        self.root.bind('<Prior>', lambda e: self.page_up())
        self.root.bind('<Next>', lambda e: self.page_down())
        self.root.bind('<Up>', lambda e: self.scroll_up())
        self.root.bind('<Down>', lambda e: self.scroll_down())
        
        # Window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Track scroll for progress
        self.text_widget.bind('<MouseWheel>', lambda e: self.root.after(100, self.update_progress))
        self.scrollbar.bind('<ButtonRelease-1>', lambda e: self.root.after(100, self.update_progress))
    
    def apply_settings(self):
        """Apply current settings to the UI."""
        # Configure font
        font_config = (
            self.settings['font_family'],
            self.settings['font_size'],
            self.settings['font_weight']
        )
        
        self.text_widget.configure(
            font=font_config,
            bg=self.settings['bg_color'],
            fg=self.settings['text_color'],
            spacing3=self.settings['line_spacing'],
            insertbackground=self.settings['text_color']
        )
        
        # Update toolbar values
        self.font_size_var.set(str(self.settings['font_size']))
        self.font_family_var.set(self.settings['font_family'])
    
    def open_file(self):
        """Open a file dialog to select a text file."""
        filetypes = [
            ('文本文件', '*.txt'),
            ('所有文件', '*.*'),
            ('Markdown文件', '*.md'),
            ('HTML文件', '*.html *.htm'),
            ('日志文件', '*.log'),
        ]
        
        filepath = filedialog.askopenfilename(
            title="选择要打开的文件",
            filetypes=filetypes
        )
        
        if filepath:
            self.load_file(filepath)
    
    def load_file(self, filepath):
        """Load and display a text file."""
        try:
            # Try different encodings
            content = None
            encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'latin-1']
            
            for encoding in encodings:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                raise ValueError("无法识别文件编码")
            
            self.current_file = filepath
            self.current_content = content
            
            # Update text widget
            self.text_widget.configure(state=tk.NORMAL)
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, content)
            self.text_widget.configure(state=tk.DISABLED)
            
            # Update title
            filename = os.path.basename(filepath)
            self.root.title(f"TextReader - {filename}")
            
            # Update status
            line_count = content.count('\n') + 1
            char_count = len(content)
            self.status_label.config(text=f"已打开: {filename} | {line_count} 行 | {char_count} 字符")
            
            # Restore position if available
            if filepath in self.settings.get('bookmarks', {}):
                pos = self.settings['bookmarks'][filepath].get('position', 0)
                self.text_widget.yview_moveto(pos)
            
            # Add to recent files
            self.add_to_recent(filepath)
            
            # Update progress
            self.update_progress()
            
            # Auto-generate table of contents
            self.generate_toc()
            
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件:\n{str(e)}")
    
    # ==================== Search Functions ====================
    
    def show_search(self):
        """Show the search bar."""
        if not self.search_frame_visible:
            self.search_frame.pack(fill=tk.X, padx=5, pady=2, after=self.toolbar)
            self.search_frame_visible = True
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)
    
    def hide_search(self):
        """Hide the search bar."""
        if self.search_frame_visible:
            self.search_frame.pack_forget()
            self.search_frame_visible = False
            self.clear_search_highlights()
            self.search_var.set('')
            self.search_matches = []
            self.current_match_index = -1
    
    def on_escape(self):
        """Handle Escape key press."""
        if self.search_frame_visible:
            self.hide_search()
        else:
            self.exit_fullscreen()
    
    def on_search_change(self):
        """Called when search text changes."""
        self.perform_search()
    
    def perform_search(self):
        """Perform the search and highlight all matches."""
        self.clear_search_highlights()
        self.search_matches = []
        self.current_match_index = -1
        
        search_text = self.search_var.get()
        if not search_text:
            self.search_count_label.config(text="")
            return
        
        # Get text content
        content = self.text_widget.get("1.0", tk.END)
        
        # Search options
        if self.case_sensitive_var.get():
            flags = 0
        else:
            flags = re.IGNORECASE
        
        # Find all matches
        try:
            pattern = re.compile(re.escape(search_text), flags)
            for match in pattern.finditer(content):
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                self.search_matches.append((start_idx, end_idx))
                self.text_widget.tag_add('search_highlight', start_idx, end_idx)
        except re.error:
            pass
        
        # Update count label
        count = len(self.search_matches)
        if count == 0:
            self.search_count_label.config(text="未找到")
        else:
            self.search_count_label.config(text=f"找到 {count} 个匹配")
            # Auto-jump to first match
            if count > 0:
                self.current_match_index = 0
                self.highlight_current_match()
    
    def clear_search_highlights(self):
        """Clear all search highlights."""
        self.text_widget.tag_remove('search_highlight', '1.0', tk.END)
        self.text_widget.tag_remove('current_match', '1.0', tk.END)
    
    def highlight_current_match(self):
        """Highlight the current match and scroll to it."""
        if not self.search_matches or self.current_match_index < 0:
            return
        
        # Remove previous current match highlight
        self.text_widget.tag_remove('current_match', '1.0', tk.END)
        
        # Highlight current match
        start_idx, end_idx = self.search_matches[self.current_match_index]
        self.text_widget.tag_add('current_match', start_idx, end_idx)
        
        # Scroll to show the match
        self.text_widget.see(start_idx)
        
        # Update count label
        count = len(self.search_matches)
        self.search_count_label.config(text=f"{self.current_match_index + 1} / {count}")
    
    def find_next(self):
        """Find the next match."""
        if not self.search_matches:
            self.perform_search()
            return
        
        if self.search_matches:
            self.current_match_index = (self.current_match_index + 1) % len(self.search_matches)
            self.highlight_current_match()
    
    def find_previous(self):
        """Find the previous match."""
        if not self.search_matches:
            self.perform_search()
            return
        
        if self.search_matches:
            self.current_match_index = (self.current_match_index - 1) % len(self.search_matches)
            self.highlight_current_match()
    
    # ==================== Table of Contents Functions ====================
    
    def toggle_toc(self):
        """Toggle the Table of Contents sidebar."""
        if self.toc_visible:
            self.toc_frame.pack_forget()
            self.toc_visible = False
        else:
            self.toc_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5), before=self.text_frame)
            self.toc_visible = True
            # Refresh TOC when showing
            if not self.chapters:
                self.generate_toc()
    
    def refresh_toc(self):
        """Refresh the table of contents."""
        self.generate_toc()
    
    def generate_toc(self):
        """Auto-generate table of contents from the text."""
        self.chapters = []
        self.toc_listbox.delete(0, tk.END)
        
        if not self.current_content:
            self.toc_listbox.insert(tk.END, "(无内容)")
            return
        
        # Chapter patterns for Chinese novels
        patterns = [
            # 第X章, 第X节, 第X回, 第X卷
            r'^[\s　]*(第[一二三四五六七八九十百千万零0-9]+[章节回卷部篇集].*?)$',
            # Chapter X, CHAPTER X
            r'^[\s　]*((?:Chapter|CHAPTER|chapter)\s*\d+.*?)$',
            # 数字章节 如 "1. 标题", "1、标题", "1．标题"
            r'^[\s　]*(\d+[\.、．]\s*.+?)$',
            # 【章节标题】
            r'^[\s　]*(【.+?】)$',
            # 序章、序、前言、楔子、尾声、番外
            r'^[\s　]*((?:序章|序|序言|前言|引子|楔子|尾声|番外|后记|附录).*)$',
            # 卷X
            r'^[\s　]*(卷[一二三四五六七八九十百千万零0-9]+.*)$',
        ]
        
        lines = self.current_content.split('\n')
        line_number = 1
        
        for line in lines:
            line_stripped = line.strip()
            if line_stripped:
                # Check if line matches any chapter pattern
                for pattern in patterns:
                    match = re.match(pattern, line, re.MULTILINE)
                    if match:
                        chapter_title = match.group(1).strip()
                        # Skip if title is too long (probably not a chapter)
                        if len(chapter_title) <= self.MAX_CHAPTER_TITLE_LENGTH:
                            self.chapters.append({
                                'title': chapter_title,
                                'line': line_number,
                                'index': f"{line_number}.0"
                            })
                        break
            line_number += 1
        
        # Populate listbox
        if self.chapters:
            for i, chapter in enumerate(self.chapters):
                display_text = f"{chapter['title']}"
                self.toc_listbox.insert(tk.END, display_text)
        else:
            self.toc_listbox.insert(tk.END, "(未检测到章节)")
            self.toc_listbox.insert(tk.END, "")
            self.toc_listbox.insert(tk.END, "支持的格式:")
            self.toc_listbox.insert(tk.END, "・第X章/节/回/卷")
            self.toc_listbox.insert(tk.END, "・Chapter X")
            self.toc_listbox.insert(tk.END, "・1. 标题")
            self.toc_listbox.insert(tk.END, "・【标题】")
    
    def on_toc_select(self, event=None):
        """Handle TOC item selection."""
        selection = self.toc_listbox.curselection()
        if selection and self.chapters:
            index = selection[0]
            if index < len(self.chapters):
                chapter = self.chapters[index]
                # Jump to chapter
                self.text_widget.see(chapter['index'])
                self.text_widget.yview(chapter['index'])
                self.update_progress()
    
    def add_to_recent(self, filepath):
        """Add file to recent files list."""
        recent = self.settings.get('recent_files', [])
        
        # Remove if already exists
        if filepath in recent:
            recent.remove(filepath)
        
        # Add to front
        recent.insert(0, filepath)
        
        # Keep only last 10
        self.settings['recent_files'] = recent[:10]
        
        # Update menu
        self.update_recent_menu()
    
    def update_recent_menu(self):
        """Update the recent files menu."""
        self.recent_menu.delete(0, tk.END)
        
        recent = self.settings.get('recent_files', [])
        
        if not recent:
            self.recent_menu.add_command(label="(无最近文件)", state=tk.DISABLED)
        else:
            for filepath in recent:
                if os.path.exists(filepath):
                    filename = os.path.basename(filepath)
                    self.recent_menu.add_command(
                        label=filename,
                        command=lambda f=filepath: self.load_file(f)
                    )
    
    def update_progress(self):
        """Update reading progress display."""
        if self.current_file:
            position = self.text_widget.yview()
            progress = int(position[0] * 100)
            self.progress_label.config(text=f"阅读进度: {progress}%")
    
    def on_font_size_change(self):
        """Handle font size change from spinbox."""
        try:
            size = int(self.font_size_var.get())
            if 8 <= size <= 72:
                self.settings['font_size'] = size
                self.apply_settings()
        except ValueError:
            pass
    
    def on_font_change(self):
        """Handle font family change."""
        self.settings['font_family'] = self.font_family_var.get()
        self.apply_settings()
    
    def increase_font_size(self):
        """Increase font size by 2."""
        new_size = min(72, self.settings['font_size'] + 2)
        self.settings['font_size'] = new_size
        self.font_size_var.set(str(new_size))
        self.apply_settings()
    
    def decrease_font_size(self):
        """Decrease font size by 2."""
        new_size = max(8, self.settings['font_size'] - 2)
        self.settings['font_size'] = new_size
        self.font_size_var.set(str(new_size))
        self.apply_settings()
    
    def choose_bg_color(self):
        """Open color picker for background."""
        color = colorchooser.askcolor(
            color=self.settings['bg_color'],
            title="选择背景颜色"
        )
        if color[1]:
            self.settings['bg_color'] = color[1]
            self.apply_settings()
    
    def choose_text_color(self):
        """Open color picker for text."""
        color = colorchooser.askcolor(
            color=self.settings['text_color'],
            title="选择文字颜色"
        )
        if color[1]:
            self.settings['text_color'] = color[1]
            self.apply_settings()
    
    def apply_theme(self):
        """Apply selected theme."""
        theme_name = self.theme_var.get()
        if theme_name in self.THEMES:
            theme = self.THEMES[theme_name]
            self.settings['bg_color'] = theme['bg']
            self.settings['text_color'] = theme['text']
            self.apply_settings()
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        
        if not is_fullscreen:
            # Hide toolbar in fullscreen
            self.toolbar.pack_forget()
            self.status_frame.pack_forget()
        else:
            # Show toolbar when exiting fullscreen
            self.toolbar.pack(fill=tk.X, padx=5, pady=5, before=self.text_frame)
            self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    def exit_fullscreen(self):
        """Exit fullscreen mode."""
        if self.root.attributes('-fullscreen'):
            self.toggle_fullscreen()
    
    def toggle_toolbar(self):
        """Toggle toolbar visibility."""
        if self.toolbar.winfo_viewable():
            self.toolbar.pack_forget()
        else:
            self.toolbar.pack(fill=tk.X, padx=5, pady=5, before=self.text_frame)
    
    def toggle_auto_scroll(self):
        """Toggle auto-scroll feature."""
        self.auto_scroll_active = not self.auto_scroll_active
        
        if self.auto_scroll_active:
            self.auto_scroll_btn.config(text="⏸ 停止滚动")
            self.do_auto_scroll()
        else:
            self.auto_scroll_btn.config(text="▶ 自动滚动")
    
    def do_auto_scroll(self):
        """Perform auto-scroll."""
        if self.auto_scroll_active:
            self.text_widget.yview_scroll(1, 'units')
            self.update_progress()
            self.root.after(self.auto_scroll_speed, self.do_auto_scroll)
    
    def scroll_up(self):
        """Scroll up by one line."""
        self.text_widget.yview_scroll(-1, 'units')
        self.update_progress()
    
    def scroll_down(self):
        """Scroll down by one line."""
        self.text_widget.yview_scroll(1, 'units')
        self.update_progress()
    
    def page_up(self):
        """Scroll up by one page."""
        self.text_widget.yview_scroll(-1, 'pages')
        self.update_progress()
    
    def page_down(self):
        """Scroll down by one page."""
        self.text_widget.yview_scroll(1, 'pages')
        self.update_progress()
    
    def goto_start(self):
        """Go to the beginning of the document."""
        self.text_widget.yview_moveto(0)
        self.update_progress()
    
    def goto_end(self):
        """Go to the end of the document."""
        self.text_widget.yview_moveto(1)
        self.update_progress()
    
    def goto_position(self):
        """Open dialog to jump to a specific position."""
        dialog = tk.Toplevel(self.root)
        dialog.title("跳转到位置")
        dialog.geometry("300x100")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="输入百分比位置 (0-100):").pack(pady=10)
        
        entry = ttk.Entry(dialog)
        entry.pack(pady=5)
        entry.focus()
        
        def do_goto():
            try:
                pos = int(entry.get()) / 100
                pos = max(0, min(1, pos))
                self.text_widget.yview_moveto(pos)
                self.update_progress()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
        
        ttk.Button(dialog, text="跳转", command=do_goto).pack(pady=5)
        entry.bind('<Return>', lambda e: do_goto())
    
    def add_bookmark(self):
        """Add a bookmark at current position."""
        if not self.current_file:
            messagebox.showinfo("提示", "请先打开一个文件")
            return
        
        position = self.text_widget.yview()[0]
        
        if 'bookmarks' not in self.settings:
            self.settings['bookmarks'] = {}
        
        self.settings['bookmarks'][self.current_file] = {
            'position': position,
            'name': f"书签 - {int(position * 100)}%"
        }
        
        self.status_label.config(text=f"书签已添加 ({int(position * 100)}%)")
    
    def manage_bookmarks(self):
        """Open bookmark manager dialog."""
        if not self.settings.get('bookmarks'):
            messagebox.showinfo("提示", "暂无书签")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("书签管理")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        
        # Listbox for bookmarks
        listbox = tk.Listbox(dialog, selectmode=tk.SINGLE)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        bookmark_files = []
        for filepath, bookmark in self.settings['bookmarks'].items():
            filename = os.path.basename(filepath)
            pos = int(bookmark['position'] * 100)
            listbox.insert(tk.END, f"{filename} - {pos}%")
            bookmark_files.append(filepath)
        
        def goto_bookmark():
            selection = listbox.curselection()
            if selection:
                filepath = bookmark_files[selection[0]]
                if os.path.exists(filepath):
                    self.load_file(filepath)
                    pos = self.settings['bookmarks'][filepath]['position']
                    self.text_widget.yview_moveto(pos)
                    self.update_progress()
                dialog.destroy()
        
        def delete_bookmark():
            selection = listbox.curselection()
            if selection:
                filepath = bookmark_files[selection[0]]
                del self.settings['bookmarks'][filepath]
                listbox.delete(selection[0])
                bookmark_files.pop(selection[0])
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="跳转", command=goto_bookmark).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=delete_bookmark).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="关闭", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def open_font_settings(self):
        """Open font settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("字体设置")
        dialog.geometry("350x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Font family
        ttk.Label(dialog, text="字体:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        font_var = tk.StringVar(value=self.settings['font_family'])
        font_combo = ttk.Combobox(dialog, textvariable=font_var, values=self.available_fonts, width=20)
        font_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # Font size
        ttk.Label(dialog, text="字号:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        size_var = tk.StringVar(value=str(self.settings['font_size']))
        size_spin = ttk.Spinbox(dialog, from_=8, to=72, width=10, textvariable=size_var)
        size_spin.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        # Font weight
        ttk.Label(dialog, text="粗细:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        weight_var = tk.StringVar(value=self.settings['font_weight'])
        weight_combo = ttk.Combobox(dialog, textvariable=weight_var, values=['normal', 'bold'], width=10)
        weight_combo.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        # Preview
        preview_frame = ttk.LabelFrame(dialog, text="预览")
        preview_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        
        preview_label = ttk.Label(preview_frame, text="示例文字 Sample Text 123")
        preview_label.pack(padx=10, pady=10)
        
        def update_preview(*args):
            try:
                preview_label.configure(font=(font_var.get(), int(size_var.get()), weight_var.get()))
            except Exception:
                pass
        
        font_var.trace('w', update_preview)
        size_var.trace('w', update_preview)
        weight_var.trace('w', update_preview)
        update_preview()
        
        def apply_changes():
            try:
                self.settings['font_family'] = font_var.get()
                self.settings['font_size'] = int(size_var.get())
                self.settings['font_weight'] = weight_var.get()
                self.font_size_var.set(str(self.settings['font_size']))
                self.font_family_var.set(self.settings['font_family'])
                self.apply_settings()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的字号")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="确定", command=apply_changes).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def open_color_settings(self):
        """Open color settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("颜色设置")
        dialog.geometry("350x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Background color
        ttk.Label(dialog, text="背景颜色:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        bg_var = tk.StringVar(value=self.settings['bg_color'])
        bg_entry = ttk.Entry(dialog, textvariable=bg_var, width=15)
        bg_entry.grid(row=0, column=1, padx=5, pady=10)
        
        def pick_bg():
            color = colorchooser.askcolor(color=bg_var.get())[1]
            if color:
                bg_var.set(color)
        
        ttk.Button(dialog, text="选择...", command=pick_bg).grid(row=0, column=2, padx=5, pady=10)
        
        # Text color
        ttk.Label(dialog, text="文字颜色:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        text_var = tk.StringVar(value=self.settings['text_color'])
        text_entry = ttk.Entry(dialog, textvariable=text_var, width=15)
        text_entry.grid(row=1, column=1, padx=5, pady=10)
        
        def pick_text():
            color = colorchooser.askcolor(color=text_var.get())[1]
            if color:
                text_var.set(color)
        
        ttk.Button(dialog, text="选择...", command=pick_text).grid(row=1, column=2, padx=5, pady=10)
        
        # Preview
        preview_frame = ttk.LabelFrame(dialog, text="预览")
        preview_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='ew')
        
        preview_label = tk.Label(preview_frame, text="示例文字预览", padx=20, pady=10)
        preview_label.pack(fill=tk.X)
        
        def update_preview(*args):
            try:
                preview_label.configure(bg=bg_var.get(), fg=text_var.get())
            except Exception:
                pass
        
        bg_var.trace('w', update_preview)
        text_var.trace('w', update_preview)
        update_preview()
        
        def apply_changes():
            self.settings['bg_color'] = bg_var.get()
            self.settings['text_color'] = text_var.get()
            self.apply_settings()
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="确定", command=apply_changes).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def open_line_spacing_settings(self):
        """Open line spacing settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("行间距设置")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="行间距 (像素):").pack(pady=10)
        
        spacing_var = tk.IntVar(value=self.settings['line_spacing'])
        scale = ttk.Scale(dialog, from_=0, to=30, orient=tk.HORIZONTAL, variable=spacing_var, length=200)
        scale.pack(pady=5)
        
        value_label = ttk.Label(dialog, text=f"{self.settings['line_spacing']} px")
        value_label.pack(pady=5)
        
        def update_label(*args):
            value_label.config(text=f"{spacing_var.get()} px")
        
        spacing_var.trace('w', update_label)
        
        def apply_changes():
            self.settings['line_spacing'] = spacing_var.get()
            self.apply_settings()
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="确定", command=apply_changes).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def open_scroll_speed_settings(self):
        """Open auto-scroll speed settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("自动滚动速度设置")
        dialog.geometry("350x180")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="滚动速度 (毫秒/行，越小越快):").pack(pady=10)
        
        speed_var = tk.IntVar(value=self.auto_scroll_speed)
        scale = ttk.Scale(dialog, from_=10, to=200, orient=tk.HORIZONTAL, variable=speed_var, length=250)
        scale.pack(pady=5)
        
        value_label = ttk.Label(dialog, text=f"{self.auto_scroll_speed} ms")
        value_label.pack(pady=5)
        
        # Speed description
        desc_label = ttk.Label(dialog, text="提示：10ms=极快，50ms=正常，200ms=慢速")
        desc_label.pack(pady=5)
        
        def update_label(*args):
            value_label.config(text=f"{speed_var.get()} ms")
        
        speed_var.trace('w', update_label)
        
        def apply_changes():
            self.auto_scroll_speed = speed_var.get()
            self.settings['auto_scroll_speed'] = self.auto_scroll_speed
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="确定", command=apply_changes).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def reset_settings(self):
        """Reset all settings to default."""
        if messagebox.askyesno("确认", "确定要恢复默认设置吗？"):
            self.settings = self.DEFAULT_SETTINGS.copy()
            self.apply_settings()
            self.theme_var.set('羊皮纸')
    
    def show_shortcuts(self):
        """Show keyboard shortcuts."""
        shortcuts = """
快捷键列表:

文件操作:
  Ctrl+O          打开文件

查找:
  Ctrl+F          打开查找栏
  F3              查找下一个
  Shift+F3        查找上一个

视图:
  Ctrl+ +         增大字号
  Ctrl+ -         减小字号
  F11             全屏模式
  Ctrl+T          隐藏/显示工具栏
  Ctrl+L          显示/隐藏目录

导航:
  Home            跳转到开头
  End             跳转到结尾
  Ctrl+G          跳转到位置
  Ctrl+B          添加书签
  Space           下一页
  Page Up         上一页
  Page Down       下一页
  ↑↓              上下滚动

其他:
  Escape          关闭查找/退出全屏
        """
        messagebox.showinfo("快捷键列表", shortcuts)
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
TextReader 文本阅读器

版本: 1.2.0

一个简洁优雅的文本阅读器，
专为舒适阅读体验而设计。

功能特点:
• 支持 TXT 等多种文本格式
• 自定义字体、字号
• 多种护眼主题
• 自定义背景和文字颜色
• 阅读进度跟踪
• 书签功能
• 自动滚动
• 全屏阅读模式
• 4K/高DPI屏幕支持
• 快速查找功能
• 自动目录导航

© 2024 TextReader
        """
        messagebox.showinfo("关于 TextReader", about_text)
    
    def on_close(self):
        """Handle window close event."""
        # Save settings
        self.save_settings()
        
        # Close window
        self.root.destroy()


def main():
    """Main entry point."""
    # Enable High-DPI awareness BEFORE creating Tk window
    # This fixes blurry display on 4K/High-DPI screens
    enable_high_dpi_awareness()
    
    root = tk.Tk()
    
    # Additional DPI scaling for Tkinter on Windows
    # Note: Only apply additional scaling on Windows where we've set DPI awareness
    # Linux/Mac typically handle DPI scaling at the system level
    try:
        if sys.platform == 'win32':
            # Get DPI from Windows
            dpi = ctypes.windll.user32.GetDpiForSystem()
            # Standard DPI is 96, calculate scale factor
            scale_factor = dpi / 96.0
            if scale_factor > 1.0:
                # Scale all Tkinter elements proportionally
                root.tk.call('tk', 'scaling', scale_factor)
    except Exception:
        pass  # Continue without scaling if it fails
    
    # Set icon if available (optional)
    try:
        # Try to set a window icon
        pass
    except Exception:
        pass
    
    app = TextReader(root)
    root.mainloop()


if __name__ == "__main__":
    main()
