package migrations

import (
    "gorm.io/gorm"
 //   "/home/ubuntu/lifeisacanvas24.github.io/zola-admin/models" // Update with your module path
)

// Migrate function to run migrations
func Migrate(db *gorm.DB) error {
    // Migrate the schema
    return db.AutoMigrate(&models.User{}, &models.Token{})
}
