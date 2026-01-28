# Imports
from PyQt5.QtCore import Qt, QDate, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QDateEdit, QLineEdit, QFrame, QScrollArea)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np
from sys import exit


# Main Class
class FitTrack(QWidget):
    def __init__(self):
        super().__init__()
        self.dark_mode_enabled = False
        self.settings()
        self.initUI()
        self.button_click()
        self.update_stats()

    # Settings
    def settings(self):
        self.setWindowTitle("FitTrack - Modern Fitness Tracker")
        self.resize(1400, 900)
        self.setMinimumSize(900, 600)

    # Init UI
    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Content area with scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Grid layout for cards
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(20)

        # Left column - Input form
        left_col = QVBoxLayout()
        left_col.setSpacing(20)
        
        input_card = self.create_input_card()
        actions_card = self.create_actions_card()
        
        left_col.addWidget(input_card)
        left_col.addWidget(actions_card)
        left_col.addStretch()

        # Right column - Chart and table
        right_col = QVBoxLayout()
        right_col.setSpacing(20)
        
        chart_card = self.create_chart_card()
        table_card = self.create_table_card()
        
        right_col.addWidget(chart_card)
        right_col.addWidget(table_card)

        # Add columns to grid (40% left, 60% right)
        grid_layout.addLayout(left_col, 40)
        grid_layout.addLayout(right_col, 60)

        content_layout.addLayout(grid_layout)
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)
        self.apply_styles()
        self.load_table()

    def create_header(self):
        """Create modern header with logo and stats"""
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(100)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 20, 30, 20)

        # Logo section
        logo_layout = QHBoxLayout()

        logo_text = QLabel("FitTrack")
        logo_text.setFont(QFont("Quicksand", 22, QFont.Bold))
        logo_text.setObjectName("logoText")
        

        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()

        # Stats section
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(40)

        self.stat_workouts = self.create_stat_widget("0", "WORKOUTS")
        self.stat_calories = self.create_stat_widget("0", "CALORIES")
        self.stat_distance = self.create_stat_widget("0", "YARDS")

        stats_layout.addWidget(self.stat_workouts)
        stats_layout.addWidget(self.stat_calories)
        stats_layout.addWidget(self.stat_distance)

        header_layout.addLayout(logo_layout)
        header_layout.addStretch()
        header_layout.addLayout(stats_layout)

        return header

    def create_stat_widget(self, value, label):
        """Create a stat display widget"""
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_label.setFont(QFont("Space Mono", 20, QFont.Bold))
        value_label.setObjectName("statValue")
        value_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(label)
        text_label.setFont(QFont("Quicksand", 9, QFont.Normal))
        text_label.setObjectName("statLabel")
        text_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(value_label)
        layout.addWidget(text_label)

        return container

    def create_input_card(self):
        """Create input form card"""
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(20)

        # Title
        title = QLabel("📝 Log Workout")
        title.setFont(QFont("Quicksand", 16, QFont.DemiBold))
        title.setObjectName("cardTitle")
        card_layout.addWidget(title)

        # Date input
        date_layout = QVBoxLayout()
        date_label = QLabel("DATE")
        date_label.setFont(QFont("Quicksand", 10, QFont.Medium))
        date_label.setObjectName("formLabel")
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.date_box.setCalendarPopup(True)
        self.date_box.setObjectName("formInput")
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_box)
        card_layout.addLayout(date_layout)

        # Calories input
        cal_layout = QVBoxLayout()
        cal_label = QLabel("CALORIES BURNED")
        cal_label.setFont(QFont("Quicksand", 10, QFont.Medium))
        cal_label.setObjectName("formLabel")
        self.kal_box = QLineEdit()
        self.kal_box.setPlaceholderText("300")
        self.kal_box.setObjectName("formInput")
        cal_layout.addWidget(cal_label)
        cal_layout.addWidget(self.kal_box)
        card_layout.addLayout(cal_layout)

        # Distance input
        dist_layout = QVBoxLayout()
        dist_label = QLabel("DISTANCE (YARDS)")
        dist_label.setFont(QFont("Quicksand", 10, QFont.Medium))
        dist_label.setObjectName("formLabel")
        self.distance_box = QLineEdit()
        self.distance_box.setPlaceholderText("1000")
        self.distance_box.setObjectName("formInput")
        dist_layout.addWidget(dist_label)
        dist_layout.addWidget(self.distance_box)
        card_layout.addLayout(dist_layout)

        # Description input
        desc_layout = QVBoxLayout()
        desc_label = QLabel("DESCRIPTION")
        desc_label.setFont(QFont("Quicksand", 10, QFont.Medium))
        desc_label.setObjectName("formLabel")
        self.description = QLineEdit()
        self.description.setPlaceholderText("Morning lap swim")
        self.description.setObjectName("formInput")
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.description)
        card_layout.addLayout(desc_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.add_btn = QPushButton("ADD WORKOUT")
        self.add_btn.setObjectName("btnPrimary")
        self.add_btn.setCursor(Qt.PointingHandCursor)
        
        self.clear_btn = QPushButton("CLEAR")
        self.clear_btn.setObjectName("btnSecondary")
        self.clear_btn.setCursor(Qt.PointingHandCursor)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.clear_btn)
        
        card_layout.addLayout(btn_layout)
        card_layout.addStretch()

        return card

    def create_actions_card(self):
        """Create actions card"""
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(20)

        # Title
        title = QLabel("⚡ Quick Actions")
        title.setFont(QFont("Quicksand", 16, QFont.DemiBold))
        title.setObjectName("cardTitle")
        card_layout.addWidget(title)

        # Info text
        info = QLabel("Select a workout from the table below to delete it.")
        info.setWordWrap(True)
        info.setObjectName("infoText")
        card_layout.addWidget(info)

        # Delete button
        self.delete_btn = QPushButton("DELETE SELECTED")
        self.delete_btn.setObjectName("btnDanger")
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.delete_btn)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setObjectName("separator")
        card_layout.addWidget(separator)

        # Generate chart button
        self.submit_btn = QPushButton("📊 GENERATE CHART")
        self.submit_btn.setObjectName("btnPrimary")
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.submit_btn)

        # Dark mode toggle
        self.dark_mode = QPushButton("🌙 TOGGLE DARK MODE")
        self.dark_mode.setObjectName("btnSecondary")
        self.dark_mode.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.dark_mode)

        card_layout.addStretch()

        return card

    def create_chart_card(self):
        """Create chart visualization card"""
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumHeight(450)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(15)

        # Title
        title = QLabel("📈 Performance Analysis")
        title.setFont(QFont("Quicksand", 16, QFont.DemiBold))
        title.setObjectName("cardTitle")
        card_layout.addWidget(title)

        # Chart
        self.figure = plt.figure(figsize=(8, 5))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(350)
        card_layout.addWidget(self.canvas)

        return card

    def create_table_card(self):
        """Create workout history table card"""
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumHeight(400)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(15)

        # Title
        title = QLabel("🗂️ Workout History")
        title.setFont(QFont("Quicksand", 16, QFont.DemiBold))
        title.setObjectName("cardTitle")
        card_layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Calories", "Distance (yds)", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setObjectName("table")
        
        card_layout.addWidget(self.table)

        return card

    # Events
    def button_click(self):
        self.add_btn.clicked.connect(self.add_workout)
        self.delete_btn.clicked.connect(self.delete_workout)
        self.submit_btn.clicked.connect(self.calculate_calories)
        self.dark_mode.clicked.connect(self.toggle_dark)
        self.clear_btn.clicked.connect(self.reset)

    # Load Tables
    def load_table(self):
        self.table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM fitness ORDER BY date DESC")
        row = 0
        while query.next():
            fit_id = query.value(0)
            date = query.value(1)
            calories = query.value(2)
            distance = query.value(3)
            description = query.value(4)

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(fit_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            
            # Handle calories - convert to number and format
            try:
                cal_value = float(calories) if calories else 0
                self.table.setItem(row, 2, QTableWidgetItem(str(int(cal_value))))
            except (ValueError, TypeError):
                self.table.setItem(row, 2, QTableWidgetItem("0"))
            
            # Handle distance - convert to number and format
            try:
                dist_value = float(distance) if distance else 0
                self.table.setItem(row, 3, QTableWidgetItem(str(int(dist_value))))
            except (ValueError, TypeError):
                self.table.setItem(row, 3, QTableWidgetItem("0"))
            
            self.table.setItem(row, 4, QTableWidgetItem(description if description else ""))
            
            # Center align numeric columns
            for col in [0, 2, 3]:
                self.table.item(row, col).setTextAlignment(Qt.AlignCenter)
            
            row += 1

    # Add workout
    def add_workout(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        calories = self.kal_box.text()
        distance = self.distance_box.text()
        description = self.description.text()

        if not calories or not distance:
            QMessageBox.warning(self, "Missing Data", "Please enter both calories and distance.")
            return

        query = QSqlQuery("""
                        INSERT INTO fitness (date, calories, distance, description)
                          VALUES(?,?,?,?)
                        """)
        query.addBindValue(date)
        query.addBindValue(calories)
        query.addBindValue(distance)
        query.addBindValue(description)
        query.exec_()

        # Success feedback
        original_text = self.add_btn.text()
        self.add_btn.setText("✓ ADDED!")
        self.add_btn.setEnabled(False)
        QTimer.singleShot(1500, lambda: (
            self.add_btn.setText(original_text),
            self.add_btn.setEnabled(True)
        ))

        self.reset()
        self.load_table()
        self.update_stats()

    # Delete workout
    def delete_workout(self):
        selected_row = self.table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a row to delete.")
            return

        fit_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(
            self, 
            "Confirm Delete", 
            "Are you sure you want to delete this workout?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.No:
            return
        
        query = QSqlQuery()
        query.prepare("DELETE FROM fitness WHERE id = ?")
        query.addBindValue(fit_id)
        query.exec_()

        self.load_table()
        self.update_stats()

    # Calculate and visualize
    def calculate_calories(self):
        distances = []
        calories = []

        query = QSqlQuery("SELECT distance, calories FROM fitness ORDER BY distance ASC")
        while query.next():
            distance = query.value(0)
            calorie = query.value(1)
            if distance and calorie:
                try:
                    # Remove commas and convert to float
                    distance_clean = str(distance).replace(',', '')
                    calorie_clean = str(calorie).replace(',', '')
                    distances.append(float(distance_clean))
                    calories.append(float(calorie_clean))
                except (ValueError, TypeError):
                    # Skip invalid entries
                    continue

        if not distances or not calories:
            QMessageBox.warning(self, "No Data", "Please add some workouts first!")
            return

        try:
            # Clear previous plot
            self.figure.clear()

            # Create scatter plot with gradient coloring
            min_calorie = min(calories)
            max_calorie = max(calories)
            
            if max_calorie > min_calorie:
                normalized_calories = [(cal - min_calorie) / (max_calorie - min_calorie) for cal in calories]
            else:
                normalized_calories = [0.5] * len(calories)

            # Set style based on theme
            if self.dark_mode_enabled:
                plt.style.use('dark_background')
                bg_color = '#2d3748'
                text_color = '#e2e8f0'
            else:
                plt.style.use('default')
                bg_color = '#ffffff'
                text_color = '#2d3748'

            ax = self.figure.add_subplot(111)
            scatter = ax.scatter(
                distances, 
                calories, 
                c=normalized_calories, 
                cmap='viridis', 
                s=100,
                alpha=0.7,
                edgecolors='white',
                linewidth=1.5
            )
            
            ax.set_title("Distance vs. Calories Burned", 
                        fontsize=14, 
                        fontweight='bold',
                        color=text_color,
                        pad=20)
            ax.set_xlabel("Distance (yards)", fontsize=11, color=text_color)
            ax.set_ylabel("Calories Burned", fontsize=11, color=text_color)
            
            # Add colorbar
            cbar = self.figure.colorbar(scatter, ax=ax)
            cbar.set_label("Normalized Calories", color=text_color)
            
            # Style the plot
            ax.grid(True, alpha=0.2)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            self.figure.patch.set_facecolor(bg_color)
            ax.set_facecolor(bg_color)
            ax.tick_params(colors=text_color)
            
            self.figure.tight_layout()
            self.canvas.draw()

        except Exception as e:
            print(f"ERROR: {e}")
            QMessageBox.warning(self, "Error", "Could not generate chart. Please try again.")

    def update_stats(self):
        """Update the statistics in the header"""
        try:
            query = QSqlQuery("SELECT COUNT(*), SUM(calories), SUM(distance) FROM fitness")
            if query.next():
                workouts = query.value(0) or 0
                total_calories = query.value(1) or 0
                total_distance = query.value(2) or 0

                # Update stat displays with proper formatting
                self.stat_workouts.findChild(QLabel, "statValue").setText(str(workouts))
                self.stat_calories.findChild(QLabel, "statValue").setText(f"{int(float(total_calories)):,}")
                self.stat_distance.findChild(QLabel, "statValue").setText(f"{int(float(total_distance)):,}")
        except (ValueError, TypeError) as e:
            print(f"Error updating stats: {e}")
            # Set default values if there's an error
            self.stat_workouts.findChild(QLabel, "statValue").setText("0")
            self.stat_calories.findChild(QLabel, "statValue").setText("0")
            self.stat_distance.findChild(QLabel, "statValue").setText("0")

    def apply_styles(self):
        """Apply modern stylesheet"""
        if self.dark_mode_enabled:
            stylesheet = """
                QWidget {
                    background-color: #1a202c;
                    color: #e2e8f0;
                    font-family: 'Quicksand', 'Segoe UI', Arial, sans-serif;
                }
                
                QScrollArea {
                    border: none;
                }
                
                #header {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #00a67d, stop:1 #008c69);
                    border: none;
                    background: transparent;
                }
                
                #logoText, #statLabel {
                    color: white;
                    background: transparent;
                }

                #statValue {
                    color: white;
                    background: transparent;
                }
                
                #card {
                    background-color: #2d3748;
                    border-radius: 12px;
                    border: 1px solid #4a5568;
                }
                
                #cardTitle {
                    color: #e2e8f0;
                    background: transparent;
                }
                
                #formLabel {
                    color: #a0aec0;
                    letter-spacing: 0.5px;
                    background: transparent;
                }
                
                #formInput, QDateEdit {
                    background-color: #1a202c;
                    color: #e2e8f0;
                    border: 2px solid #4a5568;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 14px;
                }
                
                #formInput:focus, QDateEdit:focus {
                    border-color: #00c896;
                    background: transparent;
                }
                
                QDateEdit::drop-down {
                    border: none;
                    width: 30px;
                }
                
                #btnPrimary {
                    background-color: #00c896;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 20px;
                    font-weight: 600;
                    font-size: 13px;
                    letter-spacing: 0.5px;
                }
                
                #btnPrimary:hover {
                    background-color: #00a67d;
                }
                
                #btnSecondary {
                    background-color: #4a5568;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 20px;
                    font-weight: 600;
                    font-size: 13px;
                    letter-spacing: 0.5px;
                }
                
                #btnSecondary:hover {
                    background-color: #5a6678;
                }
                
                #btnDanger {
                    background-color: #ff6b6b;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 20px;
                    font-weight: 600;
                    font-size: 13px;
                    letter-spacing: 0.5px;
                }
                
                #btnDanger:hover {
                    background-color: #ee5a52;
                }
                
                #table {
                    background-color: #2d3748;
                    border: none;
                    gridline-color: #4a5568;
                    selection-background-color: #00c896;
                }
                
                QTableWidget::item {
                    padding: 8px;
                    color: #e2e8f0;
                }
                
                QHeaderView::section {
                    background: transparent;
                    color: #a0aec0;
                    padding: 12px;
                    border: none;
                    border-bottom: 2px solid #4a5568;
                    font-weight: 600;
                    font-size: 11px;
                    letter-spacing: 0.5px;
                }
                
                #infoText {
                    color: #a0aec0;
                    font-size: 13px;
                    background: transparent;
                }
                
                #separator {
                    color: #4a5568;
                }
                
                QMessageBox {
                    background-color: #2d3748;
                }
            """
        else:
            stylesheet = """
                QWidget {
                    background-color: #f8fafb;
                    color: #1a2332;
                    font-family: 'Quicksand', 'Segoe UI', Arial, sans-serif;
                }
                
                QScrollArea {
                    border: none;
                }
                
                #header {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #00c896, stop:1 #00a67d);
                    border: none;
                }
                
                #logoText, #statValue, #statLabel {
                    color: white;
                }
                
                #card {
                    background-color: white;
                    border-radius: 12px;
                    border: 1px solid #e1e8ed;
                }
                
                #cardTitle {
                    color: #1a2332;
                }
                
                #formLabel {
                    color: #5a6c7d;
                    letter-spacing: 0.5px;
                }
                
                #formInput, QDateEdit {
                    background-color: #f0f4f8;
                    color: #1a2332;
                    border: 2px solid #e1e8ed;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 14px;
                }
                
                #formInput:focus, QDateEdit:focus {
                    border-color: #00c896;
                    background-color: white;
                }
                
                QDateEdit::drop-down {
                    border: none;
                    width: 30px;
                }
                
                #btnPrimary {
                    background-color: #00c896;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 20px;
                    font-weight: 600;
                    font-size: 13px;
                    letter-spacing: 0.5px;
                }
                
                #btnPrimary:hover {
                    background-color: #00a67d;
                }
                
                #btnSecondary {
                    background-color: #f0f4f8;
                    color: #1a2332;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 20px;
                    font-weight: 600;
                    font-size: 13px;
                    letter-spacing: 0.5px;
                }
                
                #btnSecondary:hover {
                    background-color: #e1e8ed;
                }
                
                #btnDanger {
                    background-color: #ff6b6b;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 20px;
                    font-weight: 600;
                    font-size: 13px;
                    letter-spacing: 0.5px;
                }
                
                #btnDanger:hover {
                    background-color: #ee5a52;
                }
                
                #table {
                    background-color: white;
                    border: none;
                    gridline-color: #e1e8ed;
                    selection-background-color: #e6f9f4;
                    selection-color: #1a2332;
                }
                
                QTableWidget::item {
                    padding: 8px;
                }
                
                QHeaderView::section {
                    background-color: #f0f4f8;
                    color: #5a6c7d;
                    padding: 12px;
                    border: none;
                    border-bottom: 2px solid #e1e8ed;
                    font-weight: 600;
                    font-size: 11px;
                    letter-spacing: 0.5px;
                }
                
                #infoText {
                    color: #5a6c7d;
                    font-size: 13px;
                }
                
                #separator {
                    color: #e1e8ed;
                }
            """

        self.setStyleSheet(stylesheet)

    def toggle_dark(self):
        """Toggle between light and dark mode"""
        self.dark_mode_enabled = not self.dark_mode_enabled
        self.apply_styles()
        
        # Update chart if it exists
        if self.figure.get_axes():
            self.calculate_calories()

    def reset(self):
        """Clear all input fields"""
        self.date_box.setDate(QDate.currentDate())
        self.kal_box.clear()
        self.distance_box.clear()
        self.description.clear()
        self.figure.clear()
        self.canvas.draw()


# Initialize Database
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("fitness.db")

if not db.open():
    QMessageBox.critical(None, "ERROR", "Cannot open the database")
    exit(2)

query = QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS fitness (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                calories REAL,
                distance REAL,
                description TEXT
            )
            """)

if __name__ == "__main__":
    app = QApplication([])
    
    # Set application-wide font
    app.setFont(QFont("Quicksand", 10))
    
    main = FitTrack()
    main.show()
    app.exec_()
