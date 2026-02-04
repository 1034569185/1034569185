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
import time
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
        'paragraph_spacing': 10,
        'window_width': 900,
        'window_height': 700,
        'last_file': '',
        'last_position': 0,
        'auto_scroll_speed': 50,
        'ui_scale': 1.0,
        'reading_stats': {},
        'bookmarks': {},
        'recent_files': []
    }
    
    # Predefined color themes (inspired by koodo-reader)
    THEMES = {
        '羊皮纸': {'bg': '#E9D8BC', 'text': '#594429'},  # Classic sepia
        '护眼绿': {'bg': '#C5E7CF', 'text': '#36503E'},  # Eye-care green
        '纯白色': {'bg': '#FFFFFF', 'text': '#000000'},  # Pure white
        '深夜模式': {'bg': '#2C2F31', 'text': '#FFFFFF'},  # Dark mode
        '暖白色': {'bg': '#FFF8E7', 'text': '#333333'},  # Warm white
        '淡蓝色': {'bg': '#E6F3FF', 'text': '#333333'},  # Light blue
        '薄荷绿': {'bg': '#E8F5E9', 'text': '#1B5E20'},  # Mint green
        '薰衣草': {'bg': '#F3E5F5', 'text': '#4A148C'},  # Lavender
        '桃粉色': {'bg': '#FCE4EC', 'text': '#880E4F'},  # Peach pink
        '深棕色': {'bg': '#3E2723', 'text': '#D7CCC8'},  # Deep brown
        '海洋蓝': {'bg': '#0D47A1', 'text': '#E3F2FD'},  # Ocean blue
        '墨绿色': {'bg': '#1B5E20', 'text': '#C8E6C9'},  # Dark green
    }
    
    # Maximum length for chapter title (to filter out false positives)
    MAX_CHAPTER_TITLE_LENGTH = 50
    
    # Maximum display length for chapter title in TOC (with ellipsis)
    MAX_TOC_TITLE_DISPLAY_LENGTH = 35
    
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
        self.word_count = 0
        self.char_count = 0
        
        # Reading time tracking
        self.reading_start_time = None
        self.total_reading_time = 0  # in seconds
        
        # Auto-scroll state
        self.auto_scroll_active = False
        self.auto_scroll_speed = self.settings.get('auto_scroll_speed', 50)  # milliseconds between scroll
        
        # Search state
        self.search_matches = []
        self.current_match_index = -1
        self.search_frame_visible = False
        self.search_job = None  # For debounced search
        
        # Table of contents (chapters)
        self.chapters = []
        self.toc_visible = False
        
        # UI Scale factor
        self.ui_scale = self.settings.get('ui_scale', 1.0)
        
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
        
        # Setup ttk style with scaled fonts
        self.setup_styles()
        
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        self.setup_toolbar()
        
        # Content area with TOC and text (must be created BEFORE search bar and TOC panel)
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Search bar (hidden by default) - needs content_frame for results panel
        self.setup_search_bar()
        
        # Table of Contents sidebar (hidden by default) - needs content_frame
        self.setup_toc_panel()
        
        # Text area with scrollbar
        self.text_frame = ttk.Frame(self.content_frame)
        self.text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget with optimized settings for smooth scrolling
        self.text_widget = tk.Text(
            self.text_frame,
            wrap=tk.WORD,
            yscrollcommand=self.scrollbar.set,
            state=tk.DISABLED,
            cursor="arrow",
            relief=tk.FLAT,
            padx=40,
            pady=20,
            takefocus=0,  # Don't take keyboard focus
            highlightthickness=0,  # Remove highlight border
            borderwidth=0,  # Remove border
            undo=False,  # Disable undo for better performance
            autoseparators=False,  # Disable auto separators
            maxundo=0  # No undo history
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
    
    def setup_styles(self):
        """Setup ttk styles with UI scaling."""
        self.style = ttk.Style()
        
        # Calculate scaled font size (base size is 10)
        base_font_size = int(10 * self.ui_scale)
        button_font_size = int(10 * self.ui_scale)
        
        # Configure default font for all ttk widgets
        default_font = ('Microsoft YaHei UI', base_font_size)
        button_font = ('Microsoft YaHei UI', button_font_size)
        
        # Configure ttk styles
        self.style.configure('.', font=default_font)
        self.style.configure('TLabel', font=default_font, padding=2)
        self.style.configure('TButton', font=button_font, padding=4)
        self.style.configure('TCheckbutton', font=default_font)
        self.style.configure('TRadiobutton', font=default_font)
        self.style.configure('TEntry', font=default_font, padding=2)
        self.style.configure('TCombobox', font=default_font)
        self.style.configure('TSpinbox', font=default_font)
        
        # Configure menu font
        self.menu_font = ('Microsoft YaHei UI', base_font_size)
    
    def setup_search_bar(self):
        """Setup the search bar UI with results panel."""
        # Search bar (top)
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
        
        # Toggle results panel button
        ttk.Button(self.search_frame, text="📋 结果", command=self.toggle_search_results).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.search_frame, text="✕", width=3, command=self.hide_search).pack(side=tk.RIGHT, padx=5)
        
        # Search results panel (side panel like Koodo Reader)
        self.setup_search_results_panel()
    
    def setup_search_results_panel(self):
        """Setup the search results panel with excerpts (like Koodo Reader)."""
        panel_width = int(350 * self.ui_scale)
        self.search_results_frame = ttk.Frame(self.content_frame, width=panel_width)
        self.search_results_visible = False
        # Not packed initially
        
        # Header
        header = ttk.Frame(self.search_results_frame)
        header.pack(fill=tk.X, pady=5)
        
        title_font_size = int(12 * self.ui_scale)
        ttk.Label(header, text="🔍 搜索结果", font=('Microsoft YaHei UI', title_font_size, 'bold')).pack(side=tk.LEFT, padx=10)
        ttk.Button(header, text="✕", width=3, command=self.toggle_search_results).pack(side=tk.RIGHT, padx=5)
        
        ttk.Separator(self.search_results_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5)
        
        # Results info and pagination
        self.search_results_info_frame = ttk.Frame(self.search_results_frame)
        self.search_results_info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.search_results_info_label = ttk.Label(self.search_results_info_frame, text="")
        self.search_results_info_label.pack(side=tk.LEFT)
        
        # Pagination controls
        self.search_page_frame = ttk.Frame(self.search_results_info_frame)
        self.search_page_frame.pack(side=tk.RIGHT)
        
        ttk.Button(self.search_page_frame, text="◀", width=3, command=self.prev_search_page).pack(side=tk.LEFT, padx=2)
        self.search_page_label = ttk.Label(self.search_page_frame, text="1/1")
        self.search_page_label.pack(side=tk.LEFT, padx=5)
        ttk.Button(self.search_page_frame, text="▶", width=3, command=self.next_search_page).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.search_results_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5)
        
        # Results list with scrollbar
        results_list_frame = ttk.Frame(self.search_results_frame)
        results_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        results_scrollbar = ttk.Scrollbar(results_list_frame)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Use Text widget for rich display of excerpts
        result_font_size = int(10 * self.ui_scale)
        self.search_results_text = tk.Text(
            results_list_frame,
            wrap=tk.WORD,
            yscrollcommand=results_scrollbar.set,
            font=('Microsoft YaHei UI', result_font_size),
            cursor='arrow',
            state=tk.DISABLED,
            padx=10,
            pady=5
        )
        self.search_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.config(command=self.search_results_text.yview)
        
        # Configure tags for search results
        self.search_results_text.tag_configure('excerpt', foreground='#666666')
        self.search_results_text.tag_configure('keyword', foreground='#E53935', font=('Microsoft YaHei UI', result_font_size, 'bold'))
        self.search_results_text.tag_configure('location', foreground='#1976D2', font=('Microsoft YaHei UI', result_font_size - 1))
        self.search_results_text.tag_configure('separator', foreground='#CCCCCC')
        self.search_results_text.tag_configure('clickable', foreground='#333333')
        
        # Bind click events for result items
        self.search_results_text.bind('<Button-1>', self.on_search_result_click)
        self.search_results_text.bind('<Enter>', lambda e: self.search_results_text.config(cursor='hand2'))
        self.search_results_text.bind('<Leave>', lambda e: self.search_results_text.config(cursor='arrow'))
        
        # Pagination state
        self.search_results_page = 0
        self.search_results_per_page = 20
        self.search_results_data = []  # List of {start_idx, end_idx, excerpt, line}
    
    def setup_toc_panel(self):
        """Setup the Table of Contents sidebar."""
        toc_width = int(250 * self.ui_scale)
        self.toc_frame = ttk.Frame(self.content_frame, width=toc_width)
        # Not packed initially - shown when user clicks TOC button
        
        # TOC header
        toc_header = ttk.Frame(self.toc_frame)
        toc_header.pack(fill=tk.X, pady=5)
        
        toc_title_font_size = int(12 * self.ui_scale)
        ttk.Label(toc_header, text="📚 目录", font=('Microsoft YaHei UI', toc_title_font_size, 'bold')).pack(side=tk.LEFT, padx=10)
        ttk.Button(toc_header, text="✕", width=3, command=self.toggle_toc).pack(side=tk.RIGHT, padx=5)
        
        # Refresh button
        ttk.Button(toc_header, text="🔄", width=3, command=self.refresh_toc).pack(side=tk.RIGHT, padx=2)
        
        # Chapter count info
        self.toc_count_label = ttk.Label(self.toc_frame, text="", font=('Microsoft YaHei UI', int(9 * self.ui_scale)))
        self.toc_count_label.pack(fill=tk.X, padx=10)
        
        ttk.Separator(self.toc_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5)
        
        # TOC search box
        toc_search_frame = ttk.Frame(self.toc_frame)
        toc_search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.toc_search_var = tk.StringVar()
        toc_search_entry = ttk.Entry(toc_search_frame, textvariable=self.toc_search_var, width=20)
        toc_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        toc_search_entry.insert(0, "")
        self.toc_search_var.trace('w', lambda *args: self.filter_toc())
        
        ttk.Label(toc_search_frame, text="🔍").pack(side=tk.LEFT)
        
        ttk.Separator(self.toc_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5)
        
        # TOC listbox with scrollbar - use Text widget for better styling
        toc_list_frame = ttk.Frame(self.toc_frame)
        toc_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        toc_scrollbar = ttk.Scrollbar(toc_list_frame)
        toc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        toc_font_size = int(11 * self.ui_scale)
        self.toc_text = tk.Text(
            toc_list_frame,
            wrap=tk.WORD,
            yscrollcommand=toc_scrollbar.set,
            font=('Microsoft YaHei UI', toc_font_size),
            cursor='arrow',
            state=tk.DISABLED,
            padx=5,
            pady=5
        )
        self.toc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        toc_scrollbar.config(command=self.toc_text.yview)
        
        # Configure TOC text tags
        self.toc_text.tag_configure('chapter', foreground='#333333')
        self.toc_text.tag_configure('chapter_hover', foreground='#1976D2', underline=True)
        self.toc_text.tag_configure('chapter_num', foreground='#888888', font=('Microsoft YaHei UI', toc_font_size - 1))
        self.toc_text.tag_configure('separator', foreground='#CCCCCC')
        
        # Store filtered chapters for display
        self.filtered_chapters = []
    
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
        # Menu font
        menu_font_size = int(10 * self.ui_scale)
        menu_font = ('Microsoft YaHei UI', menu_font_size)
        
        self.menubar = tk.Menu(self.root, font=menu_font)
        self.root.config(menu=self.menubar)
        
        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0, font=menu_font)
        self.menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="打开...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        
        # Recent files submenu
        self.recent_menu = tk.Menu(file_menu, tearoff=0, font=menu_font)
        file_menu.add_cascade(label="最近文件", menu=self.recent_menu)
        self.update_recent_menu()
        
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_close, accelerator="Alt+F4")
        
        # View menu
        view_menu = tk.Menu(self.menubar, tearoff=0, font=menu_font)
        self.menubar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_command(label="增大字号", command=self.increase_font_size, accelerator="Ctrl++")
        view_menu.add_command(label="减小字号", command=self.decrease_font_size, accelerator="Ctrl+-")
        view_menu.add_separator()
        view_menu.add_command(label="全屏模式", command=self.toggle_fullscreen, accelerator="F11")
        view_menu.add_command(label="隐藏工具栏", command=self.toggle_toolbar, accelerator="Ctrl+T")
        view_menu.add_separator()
        view_menu.add_command(label="显示/隐藏目录", command=self.toggle_toc, accelerator="Ctrl+L")
        
        # Edit menu (for search)
        edit_menu = tk.Menu(self.menubar, tearoff=0, font=menu_font)
        self.menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="查找...", command=self.show_search, accelerator="Ctrl+F")
        edit_menu.add_command(label="查找下一个", command=self.find_next, accelerator="F3")
        edit_menu.add_command(label="查找上一个", command=self.find_previous, accelerator="Shift+F3")
        
        # Navigate menu
        nav_menu = tk.Menu(self.menubar, tearoff=0, font=menu_font)
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
        settings_menu = tk.Menu(self.menubar, tearoff=0, font=menu_font)
        self.menubar.add_cascade(label="设置", menu=settings_menu)
        settings_menu.add_command(label="字体设置...", command=self.open_font_settings)
        settings_menu.add_command(label="颜色设置...", command=self.open_color_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="行间距设置...", command=self.open_line_spacing_settings)
        settings_menu.add_command(label="段落间距设置...", command=self.open_para_spacing_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="自动滚动速度...", command=self.open_scroll_speed_settings)
        settings_menu.add_command(label="界面缩放...", command=self.open_ui_scale_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="阅读统计", command=self.show_reading_stats)
        settings_menu.add_separator()
        settings_menu.add_command(label="恢复默认设置", command=self.reset_settings)
        
        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0, font=menu_font)
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
        
        # Scrolling - return 'break' to prevent default behavior
        self.root.bind('<space>', self.on_space_key)
        self.root.bind('<Prior>', self.on_page_up)
        self.root.bind('<Next>', self.on_page_down)
        self.root.bind('<Up>', self.on_arrow_up)
        self.root.bind('<Down>', self.on_arrow_down)
        
        # Bind mouse wheel for smooth scrolling
        self.text_widget.bind('<MouseWheel>', self.on_mouse_wheel)
        self.text_widget.bind('<Button-4>', self.on_mouse_wheel_linux)  # Linux scroll up
        self.text_widget.bind('<Button-5>', self.on_mouse_wheel_linux)  # Linux scroll down
        
        # Window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Track scroll for progress when scrollbar is dragged
        # 50ms delay allows scroll animation to complete before reading position
        self.scrollbar.bind('<ButtonRelease-1>', lambda e: self.root.after(50, self.update_progress))
    
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
            spacing1=self.settings.get('paragraph_spacing', 10),  # paragraph spacing (before)
            spacing3=self.settings.get('line_spacing', 10),  # line spacing (after)
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
            
            # Calculate statistics
            self.char_count = len(content)
            # Count Chinese characters
            chinese_chars = len([c for c in content if '\u4e00' <= c <= '\u9fff'])
            # Count English words using regex
            english_words = len(re.findall(r'\b[a-zA-Z]+\b', content))
            self.word_count = chinese_chars + english_words
            
            # Estimate reading time (average 300 Chinese chars/min or 200 English words/min)
            reading_time_min = max(1, self.word_count / 300)  # Minimum 1 minute
            
            # Update text widget
            self.text_widget.configure(state=tk.NORMAL)
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, content)
            self.text_widget.configure(state=tk.DISABLED)
            
            # Update title
            filename = os.path.basename(filepath)
            self.root.title(f"TextReader - {filename}")
            
            # Update status with reading time estimate
            line_count = content.count('\n') + 1
            if reading_time_min < 60:
                time_str = f"约 {int(reading_time_min)} 分钟"
            else:
                hours = int(reading_time_min // 60)
                mins = int(reading_time_min % 60)
                time_str = f"约 {hours} 小时 {mins} 分钟"
            
            self.status_label.config(text=f"已打开: {filename} | {line_count:,} 行 | {self.char_count:,} 字 | 阅读时间: {time_str}")
            
            # Start reading time tracking
            self.reading_start_time = time.time()
            
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
        """Hide the search bar and results panel."""
        if self.search_frame_visible:
            self.search_frame.pack_forget()
            self.search_frame_visible = False
            self.clear_search_highlights()
            self.search_var.set('')
            self.search_matches = []
            self.current_match_index = -1
        
        # Also hide results panel
        if self.search_results_visible:
            self.search_results_frame.pack_forget()
            self.search_results_visible = False
    
    def toggle_search_results(self):
        """Toggle the search results panel."""
        if self.search_results_visible:
            self.search_results_frame.pack_forget()
            self.search_results_visible = False
        else:
            self.search_results_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0), before=self.text_frame)
            self.search_results_visible = True
            # Refresh results display
            self.display_search_results_page()
    
    def on_escape(self):
        """Handle Escape key press."""
        if self.search_frame_visible:
            self.hide_search()
        else:
            self.exit_fullscreen()
    
    def on_search_change(self):
        """Called when search text changes. Uses debounce to avoid freeze."""
        # Cancel previous scheduled search
        if self.search_job:
            self.root.after_cancel(self.search_job)
        
        # Schedule new search after 300ms delay (debounce)
        # This prevents freezing when typing Chinese with IME
        self.search_job = self.root.after(300, self.start_progressive_search)
    
    def start_progressive_search(self):
        """Start a progressive/incremental search."""
        self.search_job = None  # Clear the job reference
        self.clear_search_highlights()
        self.search_matches = []
        self.search_results_data = []  # Clear excerpt data
        self.search_results_page = 0
        self.current_match_index = -1
        
        search_text = self.search_var.get()
        if not search_text:
            self.search_count_label.config(text="")
            self.update_search_results_panel()
            return
        
        # Get text content
        content = self.text_widget.get("1.0", tk.END)
        
        # Prepare search
        if self.case_sensitive_var.get():
            search_content = content
            search_pattern = search_text
        else:
            search_content = content.lower()
            search_pattern = search_text.lower()
        
        # Store search state for progressive processing
        self.search_state = {
            'content': search_content,
            'original_content': self.current_content,  # For excerpts
            'pattern': search_pattern,
            'original_pattern': search_text,  # Original search text
            'pattern_len': len(search_text),
            'start': 0,
            'batch_size': 50,  # Process 50 matches per batch
            'max_matches': 2000,
            'excerpt_context': 30  # Characters before/after match for excerpt
        }
        
        self.search_count_label.config(text="搜索中... 已找到 0 个")
        
        # Start progressive search
        self.continue_progressive_search()
    
    def jump_to_first_match_if_needed(self):
        """Jump to first match if not already done."""
        if len(self.search_matches) > 0 and self.current_match_index == -1:
            self.current_match_index = 0
            self.highlight_current_match()
    
    def continue_progressive_search(self):
        """Continue progressive search in batches to avoid UI freeze."""
        if not hasattr(self, 'search_state') or self.search_state is None:
            return
        
        state = self.search_state
        content = state['content']
        original_content = state['original_content']
        pattern = state['pattern']
        original_pattern = state['original_pattern']
        pattern_len = state['pattern_len']
        start = state['start']
        batch_size = state['batch_size']
        max_matches = state['max_matches']
        excerpt_context = state['excerpt_context']
        
        # Process one batch
        batch_count = 0
        while batch_count < batch_size:
            pos = content.find(pattern, start)
            if pos == -1:
                # Search complete
                self.finish_progressive_search()
                return
            
            start_idx = f"1.0+{pos}c"
            end_idx = f"1.0+{pos + pattern_len}c"
            self.search_matches.append((start_idx, end_idx))
            self.text_widget.tag_add('search_highlight', start_idx, end_idx)
            
            # Generate excerpt for this match
            excerpt_start = max(0, pos - excerpt_context)
            excerpt_end = min(len(original_content), pos + pattern_len + excerpt_context)
            
            # Get excerpt text and find actual keyword position in it
            excerpt = original_content[excerpt_start:excerpt_end]
            keyword_start_in_excerpt = pos - excerpt_start
            keyword_end_in_excerpt = keyword_start_in_excerpt + pattern_len
            
            # Get line number
            line_num = original_content[:pos].count('\n') + 1
            
            # Store result data
            self.search_results_data.append({
                'start_idx': start_idx,
                'end_idx': end_idx,
                'excerpt': excerpt,
                'keyword_start': keyword_start_in_excerpt,
                'keyword_end': keyword_end_in_excerpt,
                'line': line_num,
                'pos': pos
            })
            
            start = pos + 1
            batch_count += 1
            
            # Check max matches limit
            if len(self.search_matches) >= max_matches:
                self.finish_progressive_search(truncated=True)
                return
        
        # Update state for next batch
        state['start'] = start
        
        # Update progress
        count = len(self.search_matches)
        self.search_count_label.config(text=f"搜索中... 已找到 {count} 个")
        
        # Jump to first match if this is the first batch with results
        self.jump_to_first_match_if_needed()
        
        # Schedule next batch (yield to UI thread)
        self.search_job = self.root.after(1, self.continue_progressive_search)
    
    def finish_progressive_search(self, truncated=False):
        """Finish the progressive search."""
        self.search_state = None
        self.search_job = None
        
        count = len(self.search_matches)
        if count == 0:
            self.search_count_label.config(text="未找到")
        elif truncated:
            self.search_count_label.config(text=f"找到 {count}+ 个匹配")
        else:
            self.search_count_label.config(text=f"找到 {count} 个匹配")
        
        # Jump to first match if not already
        self.jump_to_first_match_if_needed()
        
        # Update search results panel
        self.update_search_results_panel()
    
    def update_search_results_panel(self):
        """Update the search results panel with current results."""
        if not hasattr(self, 'search_results_text'):
            return
        
        self.display_search_results_page()
    
    def display_search_results_page(self):
        """Display the current page of search results with excerpts."""
        if not hasattr(self, 'search_results_text'):
            return
        
        self.search_results_text.config(state=tk.NORMAL)
        self.search_results_text.delete('1.0', tk.END)
        
        total = len(self.search_results_data)
        if total == 0:
            self.search_results_text.insert(tk.END, "\n  无搜索结果\n\n  请在搜索框输入关键词")
            self.search_results_info_label.config(text="")
            self.search_page_label.config(text="0/0")
            self.search_results_text.config(state=tk.DISABLED)
            return
        
        # Calculate pagination
        per_page = self.search_results_per_page
        total_pages = (total + per_page - 1) // per_page
        current_page = self.search_results_page
        
        # Ensure current page is valid
        if current_page >= total_pages:
            current_page = total_pages - 1
            self.search_results_page = current_page
        if current_page < 0:
            current_page = 0
            self.search_results_page = 0
        
        start_idx = current_page * per_page
        end_idx = min(start_idx + per_page, total)
        
        # Update info labels
        self.search_results_info_label.config(text=f"共 {total} 个结果")
        self.search_page_label.config(text=f"{current_page + 1}/{total_pages}")
        
        # Display results for current page
        for i, result in enumerate(self.search_results_data[start_idx:end_idx]):
            result_num = start_idx + i + 1
            line = result['line']
            excerpt = result['excerpt']
            keyword_start = result['keyword_start']
            keyword_end = result['keyword_end']
            
            # Clean up excerpt (replace newlines with spaces)
            excerpt = excerpt.replace('\n', ' ').replace('\r', '')
            
            # Add prefix/suffix ellipsis if truncated
            # Prefix: if match position is beyond context window from start
            prefix = "..." if result['pos'] > 30 else ""
            # Suffix: if there's more content after the excerpt
            excerpt_end_pos = result['pos'] + result['keyword_end'] - result['keyword_start'] + 30
            suffix = "..." if excerpt_end_pos < len(self.current_content) else ""
            
            # Insert result number and location
            self.search_results_text.insert(tk.END, f"\n #{result_num}  ", 'clickable')
            self.search_results_text.insert(tk.END, f"第 {line} 行\n", 'location')
            
            # Insert excerpt with highlighted keyword
            # Add tag for making it clickable
            tag_name = f"result_{start_idx + i}"
            self.search_results_text.tag_configure(tag_name, foreground='#333333')
            self.search_results_text.tag_bind(tag_name, '<Button-1>', 
                lambda e, idx=start_idx + i: self.jump_to_search_result(idx))
            self.search_results_text.tag_bind(tag_name, '<Enter>', 
                lambda e: self.search_results_text.config(cursor='hand2'))
            self.search_results_text.tag_bind(tag_name, '<Leave>', 
                lambda e: self.search_results_text.config(cursor='arrow'))
            
            # Insert excerpt text with keyword highlighted
            self.search_results_text.insert(tk.END, f"  {prefix}", tag_name)
            
            # Text before keyword
            if keyword_start > 0:
                self.search_results_text.insert(tk.END, excerpt[:keyword_start], ('excerpt', tag_name))
            
            # Keyword (highlighted)
            self.search_results_text.insert(tk.END, excerpt[keyword_start:keyword_end], ('keyword', tag_name))
            
            # Text after keyword
            if keyword_end < len(excerpt):
                self.search_results_text.insert(tk.END, excerpt[keyword_end:], ('excerpt', tag_name))
            
            self.search_results_text.insert(tk.END, f"{suffix}\n", tag_name)
            
            # Separator
            if i < end_idx - start_idx - 1:
                self.search_results_text.insert(tk.END, "  ─────────────────────────\n", 'separator')
        
        self.search_results_text.config(state=tk.DISABLED)
    
    def prev_search_page(self):
        """Go to previous page of search results."""
        if self.search_results_page > 0:
            self.search_results_page -= 1
            self.display_search_results_page()
    
    def next_search_page(self):
        """Go to next page of search results."""
        total = len(self.search_results_data)
        total_pages = (total + self.search_results_per_page - 1) // self.search_results_per_page
        if self.search_results_page < total_pages - 1:
            self.search_results_page += 1
            self.display_search_results_page()
    
    def on_search_result_click(self, event):
        """Handle click on search result (fallback)."""
        # This is a fallback - individual results have their own click handlers
        pass
    
    def jump_to_search_result(self, index):
        """Jump to a specific search result."""
        if 0 <= index < len(self.search_results_data):
            self.current_match_index = index
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
        
        if not self.current_content:
            self.display_toc()
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
        
        # Display TOC
        self.display_toc()
    
    def filter_toc(self):
        """Filter TOC based on search text."""
        self.display_toc()
    
    def display_toc(self):
        """Display the table of contents in the Text widget."""
        if not hasattr(self, 'toc_text'):
            return
        
        self.toc_text.config(state=tk.NORMAL)
        self.toc_text.delete('1.0', tk.END)
        
        if not self.current_content:
            self.toc_text.insert(tk.END, "\n  (无内容)")
            self.toc_count_label.config(text="")
            self.toc_text.config(state=tk.DISABLED)
            return
        
        # Get filter text
        filter_text = self.toc_search_var.get().lower() if hasattr(self, 'toc_search_var') else ""
        
        # Filter chapters
        if filter_text:
            self.filtered_chapters = [c for c in self.chapters if filter_text in c['title'].lower()]
        else:
            self.filtered_chapters = self.chapters.copy()
        
        # Update count label
        total = len(self.chapters)
        filtered = len(self.filtered_chapters)
        if filter_text:
            self.toc_count_label.config(text=f"显示 {filtered}/{total} 章节")
        else:
            self.toc_count_label.config(text=f"共 {total} 章节")
        
        if not self.filtered_chapters:
            if self.chapters:
                self.toc_text.insert(tk.END, "\n  无匹配章节")
            else:
                self.toc_text.insert(tk.END, "\n  (未检测到章节)\n\n")
                self.toc_text.insert(tk.END, "  支持的格式:\n")
                self.toc_text.insert(tk.END, "  ・第X章/节/回/卷\n")
                self.toc_text.insert(tk.END, "  ・Chapter X\n")
                self.toc_text.insert(tk.END, "  ・1. 标题\n")
                self.toc_text.insert(tk.END, "  ・【标题】\n")
            self.toc_text.config(state=tk.DISABLED)
            return
        
        # Display chapters with clickable tags
        for i, chapter in enumerate(self.filtered_chapters):
            # Create unique tag for this chapter
            tag_name = f"chapter_{i}"
            self.toc_text.tag_configure(tag_name, foreground='#333333')
            
            # Find original index in chapters list
            original_idx = self.chapters.index(chapter)
            
            # Bind click event
            self.toc_text.tag_bind(tag_name, '<Button-1>', 
                lambda e, idx=original_idx: self.jump_to_chapter(idx))
            self.toc_text.tag_bind(tag_name, '<Enter>', 
                lambda e, t=tag_name: self.toc_text.tag_configure(t, foreground='#1976D2', underline=True))
            self.toc_text.tag_bind(tag_name, '<Leave>', 
                lambda e, t=tag_name: self.toc_text.tag_configure(t, foreground='#333333', underline=False))
            
            # Insert chapter number
            chapter_num = i + 1
            self.toc_text.insert(tk.END, f"\n {chapter_num:3d}. ", 'chapter_num')
            
            # Insert chapter title (clickable), truncate if too long
            title = chapter['title']
            max_len = self.MAX_TOC_TITLE_DISPLAY_LENGTH
            if len(title) > max_len:
                title = title[:max_len - 3] + "..."
            self.toc_text.insert(tk.END, f"{title}", tag_name)
            
            # Insert line number
            self.toc_text.insert(tk.END, f"  (行 {chapter['line']})", 'chapter_num')
        
        self.toc_text.insert(tk.END, "\n")
        self.toc_text.config(state=tk.DISABLED)
    
    def jump_to_chapter(self, index):
        """Jump to a specific chapter."""
        if 0 <= index < len(self.chapters):
            chapter = self.chapters[index]
            self.text_widget.see(chapter['index'])
            self.text_widget.yview(chapter['index'])
            self.update_progress()
    
    def on_toc_select(self, event=None):
        """Handle TOC item selection (legacy - for listbox compatibility)."""
        pass
    
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
    
    # ==================== Keyboard Event Handlers ====================
    
    def _is_in_text_entry(self, event):
        """Check if event occurred in a text entry widget."""
        return event.widget == self.search_entry
    
    def on_space_key(self, event):
        """Handle space key - page down."""
        if self._is_in_text_entry(event):
            return  # Let entry handle it
        self.page_down()
        return 'break'  # Prevent default
    
    def on_page_up(self, event):
        """Handle Page Up key."""
        self.page_up()
        return 'break'  # Prevent default
    
    def on_page_down(self, event):
        """Handle Page Down key."""
        self.page_down()
        return 'break'  # Prevent default
    
    def on_arrow_up(self, event):
        """Handle Up arrow key."""
        if self._is_in_text_entry(event):
            return  # Let entry handle it
        self.scroll_up()
        return 'break'  # Prevent default
    
    def on_arrow_down(self, event):
        """Handle Down arrow key."""
        if self._is_in_text_entry(event):
            return  # Let entry handle it
        self.scroll_down()
        return 'break'  # Prevent default
    
    def on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling with improved smoothness."""
        # Windows/Mac: event.delta is typically ±120
        # Scroll 3 lines per wheel tick for smooth but responsive scrolling
        if event.delta > 0:
            self.text_widget.yview_scroll(-3, 'units')
        else:
            self.text_widget.yview_scroll(3, 'units')
        
        self.update_progress()
        return 'break'  # Prevent default
    
    def on_mouse_wheel_linux(self, event):
        """Handle mouse wheel scrolling on Linux (Button-4/5)."""
        # Scroll 3 lines per wheel tick for smooth but responsive scrolling
        if event.num == 4:
            self.text_widget.yview_scroll(-3, 'units')
        elif event.num == 5:
            self.text_widget.yview_scroll(3, 'units')
        
        self.update_progress()
        return 'break'  # Prevent default
    
    # ==================== Scroll Functions ====================
    
    def scroll_up(self):
        """Scroll up by 2 lines for smoother experience."""
        self.text_widget.yview_scroll(-2, 'units')
        self.update_progress()
    
    def scroll_down(self):
        """Scroll down by 2 lines for smoother experience."""
        self.text_widget.yview_scroll(2, 'units')
        self.update_progress()
    
    def page_up(self):
        """Scroll up by approximately one page (80% of visible area for context)."""
        visible_fraction = self.text_widget.yview()
        page_size = visible_fraction[1] - visible_fraction[0]
        
        # Move by 80% of page to keep some context for reading continuity
        new_pos = max(0, visible_fraction[0] - page_size * 0.8)
        self.text_widget.yview_moveto(new_pos)
        self.update_progress()
    
    def page_down(self):
        """Scroll down by approximately one page (80% of visible area for context)."""
        visible_fraction = self.text_widget.yview()
        page_size = visible_fraction[1] - visible_fraction[0]
        
        # Move by 80% of page to keep some context
        # yview_moveto clamps to [0, 1], so we can simply calculate the new position
        new_pos = min(1.0, visible_fraction[0] + page_size * 0.8)
        self.text_widget.yview_moveto(new_pos)
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
        dialog.geometry("350x150")
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
        dialog.geometry("450x350")
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
        dialog.geometry("400x320")
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
        dialog.geometry("420x280")
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
        dialog.geometry("380x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="行间距 (像素):").pack(pady=15)
        
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
    
    def open_para_spacing_settings(self):
        """Open paragraph spacing settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("段落间距设置")
        dialog.geometry("380x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="段落间距 (像素):").pack(pady=15)
        
        spacing_var = tk.IntVar(value=self.settings.get('paragraph_spacing', 10))
        scale = ttk.Scale(dialog, from_=0, to=50, orient=tk.HORIZONTAL, variable=spacing_var, length=200)
        scale.pack(pady=5)
        
        value_label = ttk.Label(dialog, text=f"{self.settings.get('paragraph_spacing', 10)} px")
        value_label.pack(pady=5)
        
        def update_label(*args):
            value_label.config(text=f"{spacing_var.get()} px")
        
        spacing_var.trace('w', update_label)
        
        def apply_changes():
            self.settings['paragraph_spacing'] = spacing_var.get()
            self.apply_settings()
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="确定", command=apply_changes).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def show_reading_stats(self):
        """Show reading statistics dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("阅读统计")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Current session stats
        ttk.Label(dialog, text="📊 阅读统计", font=('', 14, 'bold')).pack(pady=15)
        
        stats_frame = ttk.LabelFrame(dialog, text="当前文件")
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        if self.current_file:
            filename = os.path.basename(self.current_file)
            ttk.Label(stats_frame, text=f"文件: {filename}").pack(anchor='w', padx=10, pady=5)
            ttk.Label(stats_frame, text=f"字符数: {self.char_count:,}").pack(anchor='w', padx=10, pady=2)
            ttk.Label(stats_frame, text=f"预计字数: {self.word_count:,}").pack(anchor='w', padx=10, pady=2)
            
            # Reading progress
            progress = self.text_widget.yview()
            read_percent = int(progress[0] * 100)
            ttk.Label(stats_frame, text=f"阅读进度: {read_percent}%").pack(anchor='w', padx=10, pady=2)
            
            # Session reading time
            if self.reading_start_time:
                session_time = int(time.time() - self.reading_start_time)
                mins = session_time // 60
                secs = session_time % 60
                ttk.Label(stats_frame, text=f"本次阅读时间: {mins} 分 {secs} 秒").pack(anchor='w', padx=10, pady=2)
            
            # Estimated remaining time (only show if progress > 5% to avoid huge estimates)
            if read_percent >= 5 and self.reading_start_time:
                session_time = time.time() - self.reading_start_time
                if session_time > 60:  # Only show if reading for more than 1 minute
                    remaining_percent = 100 - read_percent
                    estimated_remaining = (session_time / read_percent) * remaining_percent
                    rem_mins = int(estimated_remaining // 60)
                    ttk.Label(stats_frame, text=f"预计剩余时间: 约 {rem_mins} 分钟").pack(anchor='w', padx=10, pady=2)
        else:
            ttk.Label(stats_frame, text="(未打开文件)").pack(padx=10, pady=10)
        
        # Tip
        tip_frame = ttk.LabelFrame(dialog, text="阅读建议")
        tip_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tips = [
            "💡 每阅读 45 分钟，休息 10-15 分钟",
            "💡 调整字号和行间距可提高阅读舒适度",
            "💡 护眼绿和羊皮纸主题适合长时间阅读",
            "💡 使用书签功能标记重要位置"
        ]
        for tip in tips:
            ttk.Label(tip_frame, text=tip).pack(anchor='w', padx=10, pady=2)
        
        ttk.Button(dialog, text="关闭", command=dialog.destroy).pack(pady=15)
    
    def open_scroll_speed_settings(self):
        """Open auto-scroll speed settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("自动滚动速度设置")
        dialog.geometry("420x240")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="滚动速度 (毫秒/行，越小越快):").pack(pady=15)
        
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
    
    def open_ui_scale_settings(self):
        """Open UI scale settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("界面缩放设置")
        dialog.geometry("480x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="界面缩放比例:").pack(pady=15)
        
        # Use DoubleVar for float values
        scale_var = tk.DoubleVar(value=self.ui_scale)
        scale_slider = ttk.Scale(dialog, from_=0.8, to=2.0, orient=tk.HORIZONTAL, variable=scale_var, length=300)
        scale_slider.pack(pady=5)
        
        value_label = ttk.Label(dialog, text=f"{self.ui_scale:.1f}x ({int(self.ui_scale * 100)}%)")
        value_label.pack(pady=5)
        
        # Preset buttons
        preset_frame = ttk.Frame(dialog)
        preset_frame.pack(pady=10)
        
        ttk.Label(preset_frame, text="快速选择: ").pack(side=tk.LEFT, padx=5)
        for preset in [1.0, 1.25, 1.5, 1.75, 2.0]:
            ttk.Button(
                preset_frame, 
                text=f"{int(preset * 100)}%", 
                command=lambda p=preset: scale_var.set(p),
                width=6
            ).pack(side=tk.LEFT, padx=2)
        
        # Description
        desc_label = ttk.Label(dialog, text="提示: 缩放后需要重启应用才能完全生效")
        desc_label.pack(pady=5)
        
        def update_label(*args):
            val = scale_var.get()
            value_label.config(text=f"{val:.1f}x ({int(val * 100)}%)")
        
        scale_var.trace('w', update_label)
        
        def apply_changes():
            new_scale = round(scale_var.get(), 2)
            self.settings['ui_scale'] = new_scale
            self.ui_scale = new_scale
            self.save_settings()
            messagebox.showinfo("提示", "界面缩放设置已保存。\n请重启应用以应用新的缩放比例。")
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

版本: 1.6.0

一个简洁优雅的文本阅读器，
专为舒适阅读体验而设计。
参考 Koodo Reader 优化。

功能特点:
• 支持 TXT 等多种文本格式
• 自定义字体、字号、间距
• 12种精选护眼主题
• 自定义背景和文字颜色
• 阅读进度和时间统计
• 书签功能
• 自动滚动
• 全屏阅读模式
• 4K/高DPI屏幕支持
• 搜索结果带片段预览
• 搜索结果分页显示
• 目录搜索过滤
• 界面缩放（80%-200%）
• 平滑翻页和滚动

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
    
    try:
        app = TextReader(root)
        root.mainloop()
    except Exception as e:
        import traceback
        error_msg = f"程序启动时发生错误:\n\n{str(e)}\n\n{traceback.format_exc()}"
        try:
            messagebox.showerror("错误", error_msg)
        except:
            print(error_msg)
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(traceback.format_exc())
        input("按 Enter 键退出...")
