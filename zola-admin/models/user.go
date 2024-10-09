package models

import (
    "gorm.io/gorm"
    "time" // Add this import for the time package

)

// User model
type User struct {
    ID       uint   `gorm:"primaryKey"`
    Username string `gorm:"unique;not null"`
    Password string `gorm:"not null"`
    CreatedAt time.Time
}

// Token model
type Token struct {
    ID        uint      `gorm:"primaryKey"`
    UserID    uint      `gorm:"not null"`
    Token     string    `gorm:"not null"`
    CreatedAt time.Time
}
