package migrations

import (
    "gorm.io/gorm"
    "github.com/lifeisacanvas24/lifeisacanvas24.github.io/zola-admin/models" // Update this path based on your project structure
)

// Migrate function to run migrations
func Migrate(db *gorm.DB) error {
    if err := db.AutoMigrate(&models.User{}); err != nil {
        return err
    }
    return nil
}
