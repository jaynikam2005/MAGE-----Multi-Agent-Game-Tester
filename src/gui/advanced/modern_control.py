"""
Modern UI Controls with Advanced Animations
Futuristic gaming industry focused widgets
"""

from typing import Optional, List
import math

from PyQt6.QtWidgets import (
    QPushButton, QSlider, QProgressBar, QLabel, QFrame, QWidget,
    QGraphicsDropShadowEffect, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect,
    pyqtSignal, QParallelAnimationGroup, QSequentialAnimationGroup,
    QVariantAnimation, QPointF
)
from PyQt6.QtGui import (
    QPainter, QColor, QBrush, QPen, QLinearGradient, QRadialGradient,
    QFont, QPainterPath, QPolygonF, QFontMetrics
)
import numpy as np


class ModernSlider(QSlider):
    """Modern slider with glow effects and smooth animations"""
    
    def __init__(self, orientation=Qt.Orientation.Horizontal):
        super().__init__(orientation)
        self.init_modern_style()
        
    def init_modern_style(self):
        """Initialize modern styling"""
        
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                border: none;
                height: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(40,40,40,255), stop:1 rgba(60,60,60,255));
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0,150,255,255), stop:1 rgba(0,100,200,255));
                border: 2px solid rgba(0,200,255,180);
                width: 20px;
                height: 20px;
                margin: -7px 0;
                border-radius: 12px;
            }
            
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0,180,255,255), stop:1 rgba(0,130,230,255));
                border: 2px solid rgba(0,230,255,255);
                box-shadow: 0 0 15px rgba(0,150,255,150);
            }
            
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0,150,255,200), stop:1 rgba(0,200,255,200));
                border-radius: 3px;
            }
        """)


class ModernButton(QPushButton):
    """Modern button with hover animations and glow effects"""
    
    def __init__(self, text: str = "", primary: bool = False):
        super().__init__(text)
        self.primary = primary
        self.is_glowing = False
        self.init_modern_style()
        self.setup_animations()
        
    def init_modern_style(self):
        """Initialize modern button styling"""
        
        if self.primary:
            style = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(0,120,215,255), stop:1 rgba(0,100,180,255));
                    border: 2px solid rgba(0,150,255,180);
                    border-radius: 8px;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 12px 24px;
                    min-height: 20px;
                }
                
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(0,140,235,255), stop:1 rgba(0,120,200,255));
                    border: 2px solid rgba(0,200,255,255);
                }
                
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(0,100,195,255), stop:1 rgba(0,80,160,255));
                }
                
                QPushButton:disabled {
                    background: rgba(100,100,100,100);
                    border: 2px solid rgba(150,150,150,100);
                    color: rgba(200,200,200,150);
                }
            """
        else:
            style = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(70,70,70,255), stop:1 rgba(50,50,50,255));
                    border: 2px solid rgba(120,120,120,180);
                    border-radius: 8px;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 12px 24px;
                    min-height: 20px;
                }
                
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(90,90,90,255), stop:1 rgba(70,70,70,255));
                    border: 2px solid rgba(150,150,150,255);
                }
                
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(50,50,50,255), stop:1 rgba(30,30,30,255));
                }
            """
        
        self.setStyleSheet(style)
        
        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
    
    def setup_animations(self):
        """Setup button animations"""
        
        # Hover animation
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def enterEvent(self, event):
        """Handle mouse enter event"""
        super().enterEvent(event)
        self.animate_hover_in()
        
    def leaveEvent(self, event):
        """Handle mouse leave event"""
        super().leaveEvent(event)
        self.animate_hover_out()
    
    def animate_hover_in(self):
        """Animate button on hover in"""
        current_rect = self.geometry()
        expanded_rect = current_rect.adjusted(-2, -2, 2, 2)
        
        self.hover_animation.setStartValue(current_rect)
        self.hover_animation.setEndValue(expanded_rect)
        self.hover_animation.start()
    
    def animate_hover_out(self):
        """Animate button on hover out"""
        current_rect = self.geometry()
        normal_rect = current_rect.adjusted(2, 2, -2, -2)
        
        self.hover_animation.setStartValue(current_rect)
        self.hover_animation.setEndValue(normal_rect)
        self.hover_animation.start()


class GlowingButton(ModernButton):
    """Button with animated glow effect"""
    
    def __init__(self, text: str = ""):
        super().__init__(text, primary=True)
        self.glow_intensity = 0
        self.setup_glow_animation()
        
    def setup_glow_animation(self):
        """Setup glow animation"""
        
        self.glow_animation = QVariantAnimation()
        self.glow_animation.setStartValue(0.0)
        self.glow_animation.setEndValue(1.0)
        self.glow_animation.setDuration(2000)
        self.glow_animation.setLoopCount(-1)
        self.glow_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.glow_animation.valueChanged.connect(self.update_glow)
        
    def update_glow(self, value):
        """Update glow intensity"""
        self.glow_intensity = value
        self.update()
    
    def start_glow(self):
        """Start glow animation"""
        self.glow_animation.start()
    
    def stop_glow(self):
        """Stop glow animation"""
        self.glow_animation.stop()
        self.glow_intensity = 0
        self.update()
    
    def paintEvent(self, event):
        """Custom paint event with glow effect"""
        super().paintEvent(event)
        
        if self.glow_intensity > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Create glow effect
            glow_color = QColor(0, 150, 255, int(50 * self.glow_intensity))
            painter.setBrush(QBrush(glow_color))
            painter.setPen(Qt.PenStyle.NoPen)
            
            # Draw glow around button
            glow_rect = self.rect().adjusted(-5, -5, 5, 5)
            painter.drawRoundedRect(glow_rect, 12, 12)


class ParticleButton(ModernButton):
    """Button with particle effects on click"""
    
    def __init__(self, text: str = ""):
        super().__init__(text, primary=True)
        self.particles = []
        self.particle_timer = QTimer()
        self.particle_timer.timeout.connect(self.update_particles)
        
    def mousePressEvent(self, event):
        """Handle mouse press with particle effect"""
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.create_particles(event.position())
    
    def create_particles(self, position: QPointF):
        """Create particle explosion at position"""
        
        for _ in range(20):
            particle = {
                'x': position.x(),
                'y': position.y(),
                'vx': np.random.uniform(-5, 5),
                'vy': np.random.uniform(-8, -2),
                'life': 1.0,
                'decay': np.random.uniform(0.02, 0.05),
                'size': np.random.uniform(2, 6),
                'color': QColor(
                    np.random.randint(100, 255),
                    np.random.randint(150, 255), 
                    255,
                    255
                )
            }
            self.particles.append(particle)
        
        self.particle_timer.start(16)  # ~60 FPS
    
    def update_particles(self):
        """Update particle physics"""
        
        for particle in self.particles[:]:
            # Update position
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Apply gravity
            particle['vy'] += 0.3
            
            # Update life
            particle['life'] -= particle['decay']
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        if not self.particles:
            self.particle_timer.stop()
        
        self.update()
    
    def paintEvent(self, event):
        """Custom paint event with particles"""
        super().paintEvent(event)
        
        if self.particles:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            for particle in self.particles:
                # Set particle color with alpha based on life
                color = QColor(particle['color'])
                color.setAlphaF(particle['life'])
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.PenStyle.NoPen)
                
                # Draw particle
                size = particle['size'] * particle['life']
                painter.drawEllipse(
                    QPointF(particle['x'], particle['y']),
                    size, size
                )


class ModernProgressBar(QProgressBar):
    """Modern progress bar with glow and animation effects"""
    
    def __init__(self):
        super().__init__()
        self.glow_position = 0
        self.is_animating = False
        self.init_modern_style()
        self.setup_glow_animation()
        
    def init_modern_style(self):
        """Initialize modern progress bar styling"""
        
        self.setStyleSheet("""
            QProgressBar {
                border: 2px solid rgba(100,100,100,150);
                border-radius: 8px;
                text-align: center;
                background-color: rgba(30,30,30,200);
                color: white;
                font-weight: bold;
                height: 25px;
            }
            
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0,150,255,255), stop:0.5 rgba(0,200,255,255), stop:1 rgba(0,150,255,255));
                border-radius: 6px;
                margin: 2px;
            }
        """)
        
        self.setTextVisible(True)
    
    def setup_glow_animation(self):
        """Setup glow animation for active progress"""
        
        self.glow_animation = QVariantAnimation()
        self.glow_animation.setStartValue(0.0)
        self.glow_animation.setEndValue(1.0)
        self.glow_animation.setDuration(1500)
        self.glow_animation.setLoopCount(-1)
        self.glow_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.glow_animation.valueChanged.connect(self.update_glow_position)
    
    def update_glow_position(self, value):
        """Update glow position"""
        self.glow_position = value
        if self.is_animating:
            self.update()
    
    def start_animation(self):
        """Start progress animation"""
        self.is_animating = True
        self.glow_animation.start()
    
    def stop_animation(self):
        """Stop progress animation"""
        self.is_animating = False
        self.glow_animation.stop()
    
    def setValue(self, value):
        """Override setValue to control animation"""
        super().setValue(value)
        
        if value > 0 and value < self.maximum() and not self.is_animating:
            self.start_animation()
        elif (value == 0 or value == self.maximum()) and self.is_animating:
            self.stop_animation()
    
    def paintEvent(self, event):
        """Custom paint event with glow effect"""
        super().paintEvent(event)
        
        if self.is_animating and self.value() > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Calculate progress area
            progress_ratio = self.value() / self.maximum() if self.maximum() > 0 else 0
            progress_width = (self.width() - 8) * progress_ratio  # Account for margins
            
            if progress_width > 0:
                # Create moving glow effect
                glow_pos = progress_width * self.glow_position
                
                gradient = QLinearGradient(glow_pos - 30, 0, glow_pos + 30, 0)
                gradient.setColorAt(0, QColor(255, 255, 255, 0))
                gradient.setColorAt(0.5, QColor(255, 255, 255, 120))
                gradient.setColorAt(1, QColor(255, 255, 255, 0))
                
                painter.setBrush(QBrush(gradient))
                painter.setPen(Qt.PenStyle.NoPen)
                
                glow_rect = QRect(4, 4, int(glow_pos + 20), self.height() - 8)
                painter.drawRoundedRect(glow_rect, 6, 6)


class ModernCard(QFrame):
    """Modern card container with shadow and hover effects"""
    
    def __init__(self, title: str = ""):
        super().__init__()
        self.title = title
        self.is_hovered = False
        self.init_card_style()
        self.setup_card_layout()
        
    def init_card_style(self):
        """Initialize card styling"""
        
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet("""
            ModernCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60,60,60,200), stop:1 rgba(40,40,40,200));
                border: 1px solid rgba(100,150,255,100);
                border-radius: 12px;
                padding: 16px;
                margin: 8px;
            }
            
            ModernCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(70,70,70,220), stop:1 rgba(50,50,50,220));
                border: 1px solid rgba(100,150,255,180);
            }
        """)
        
        # Add drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
    
    def setup_card_layout(self):
        """Setup card layout with title"""
        
        layout = QVBoxLayout(self)
        
        if self.title:
            title_label = QLabel(self.title)
            title_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #2196F3;
                margin-bottom: 10px;
                padding-bottom: 8px;
                border-bottom: 2px solid rgba(33,150,243,100);
            """)
            layout.addWidget(title_label)
    
    def enterEvent(self, event):
        """Handle mouse enter"""
        super().enterEvent(event)
        self.is_hovered = True
        
    def leaveEvent(self, event):
        """Handle mouse leave"""
        super().leaveEvent(event)
        self.is_hovered = False


class AnimatedLabel(QLabel):
    """Label with text animation effects"""
    
    def __init__(self, text: str = ""):
        super().__init__(text)
        self.original_text = text
        self.animation_type = "none"
        self.animation_timer = QTimer()
        self.animation_frame = 0
        self.animation_timer.timeout.connect(self.update_animation)
        
    def start_typing_animation(self, speed: int = 100):
        """Start typing animation"""
        self.animation_type = "typing"
        self.animation_frame = 0
        self.setText("")
        self.animation_timer.start(speed)
    
    def start_pulse_animation(self, speed: int = 1000):
        """Start pulse animation"""
        self.animation_type = "pulse"
        self.animation_frame = 0
        self.animation_timer.start(speed // 10)
    
    def stop_animation(self):
        """Stop current animation"""
        self.animation_timer.stop()
        self.animation_type = "none"
        self.setText(self.original_text)
    
    def update_animation(self):
        """Update animation frame"""
        
        if self.animation_type == "typing":
            if self.animation_frame < len(self.original_text):
                self.setText(self.original_text[:self.animation_frame + 1])
                self.animation_frame += 1
            else:
                self.stop_animation()
                
        elif self.animation_type == "pulse":
            intensity = abs(math.sin(self.animation_frame * 0.1))
            color_intensity = int(155 + 100 * intensity)
            
            self.setStyleSheet(f"""
                color: rgb({color_intensity}, {color_intensity}, {color_intensity});
                font-weight: bold;
            """)
            
            self.animation_frame += 1
    
    def set_text_animated(self, text: str):
        """Set text with typing animation"""
        self.original_text = text
        self.start_typing_animation()


class ProgressRing(QWidget):
    """Circular progress ring with glow effects"""
    
    def __init__(self, size: int = 100):
        super().__init__()
        self.size = size
        self.progress = 0
        self.max_progress = 100
        self.ring_width = 8
        self.init_ring_style()
        
    def init_ring_style(self):
        """Initialize ring styling"""
        
        self.setFixedSize(self.size, self.size)
        
        # Colors
        self.background_color = QColor(40, 40, 40, 150)
        self.progress_color = QColor(0, 150, 255, 255)
        self.glow_color = QColor(0, 200, 255, 100)
    
    def set_progress(self, value: int):
        """Set progress value"""
        self.progress = max(0, min(value, self.max_progress))
        self.update()
    
    def paintEvent(self, event):
        """Custom paint event for progress ring"""
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Center and radius
        center = self.rect().center()
        radius = (self.size - self.ring_width) // 2
        
        # Background ring
        painter.setPen(QPen(self.background_color, self.ring_width))
        painter.drawEllipse(center, radius, radius)
        
        # Progress ring
        if self.progress > 0:
            # Calculate angle
            angle = (self.progress / self.max_progress) * 360
            
            # Create gradient for progress
            gradient = QRadialGradient(center, radius)
            gradient.setColorAt(0, self.progress_color)
            gradient.setColorAt(1, self.glow_color)
            
            painter.setPen(QPen(QBrush(gradient), self.ring_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            
            # Draw progress arc
            start_angle = -90 * 16  # Start at top
            span_angle = angle * 16
            
            painter.drawArc(
                center.x() - radius, center.y() - radius,
                radius * 2, radius * 2,
                start_angle, span_angle
            )
        
        # Progress text
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        progress_text = f"{self.progress}%"
        text_rect = painter.fontMetrics().boundingRect(progress_text)
        text_pos = QPointF(
            center.x() - text_rect.width() / 2,
            center.y() + text_rect.height() / 4
        )
        
        painter.drawText(text_pos, progress_text)


class NeonButton(ModernButton):
    """Button with neon glow effect"""
    
    def __init__(self, text: str = "", neon_color: QColor = None):
        super().__init__(text)
        self.neon_color = neon_color or QColor(0, 255, 150)
        self.glow_intensity = 0.5
        self.init_neon_style()
        
    def init_neon_style(self):
        """Initialize neon button styling"""
        
        color = self.neon_color
        
        self.setStyleSheet(f"""
            QPushButton {{
                background: rgba(20, 20, 20, 200);
                border: 2px solid rgb({color.red()}, {color.green()}, {color.blue()});
                border-radius: 8px;
                color: rgb({color.red()}, {color.green()}, {color.blue()});
                font-weight: bold;
                font-size: 14px;
                padding: 12px 24px;
                text-transform: uppercase;
            }}
            
            QPushButton:hover {{
                background: rgba({color.red()}, {color.green()}, {color.blue()}, 30);
                border: 2px solid rgb({min(255, color.red() + 50)}, {min(255, color.green() + 50)}, {min(255, color.blue() + 50)});
                color: rgb({min(255, color.red() + 50)}, {min(255, color.green() + 50)}, {min(255, color.blue() + 50)});
            }}
            
            QPushButton:pressed {{
                background: rgba({color.red()}, {color.green()}, {color.blue()}, 60);
            }}
        """)
        
        # Add neon glow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(color.red(), color.green(), color.blue(), 150))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)
    
    def paintEvent(self, event):
        """Custom paint event with enhanced neon glow"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Add inner glow
        color = self.neon_color
        glow_rect = self.rect().adjusted(2, 2, -2, -2)
        
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(color.red(), color.green(), color.blue(), int(20 * self.glow_intensity)))
        gradient.setColorAt(1, QColor(color.red(), color.green(), color.blue(), int(60 * self.glow_intensity)))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(glow_rect, 6, 6)
