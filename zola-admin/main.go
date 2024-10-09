package main

import (
    "github.com/gofiber/fiber/v2"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
    "github.com/lifeisacanvas24/lifeisacanvas24.github.io/zola-admin/models"    // Update with your actual module path
    "github.com/lifeisacanvas24/lifeisacanvas24.github.io/zola-admin/migrations" // Update with your actual module path
)

func main() {
    app := fiber.New()

    // Initialize database
    db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
    if err != nil {
        panic("failed to connect database")
    }

    // Run migrations
    err = migrations.Migrate(db)
    if err != nil {
        panic("failed to migrate database")
    }

    // Other routes and app logic...

    app.Listen(":3000")
}
