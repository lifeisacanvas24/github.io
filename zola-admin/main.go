package main

import (
    "github.com/gofiber/fiber/v2"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
//  "/home/ubuntu/lifeisacanvas24.github.io/zola-admin/migrations" // Update with your module path
)

func main() {
    // Initialize Fiber
    app := fiber.New()

    // Initialize the SQLite database
    db, err := gorm.Open(sqlite.Open("db.sqlite"), &gorm.Config{})
    if err != nil {
        panic("failed to connect to database")
    }

    // Run migrations
    if err := migrations.Migrate(db); err != nil {
        panic("failed to run migrations")
    }

    // Your routes go here
    app.Get("/", func(c *fiber.Ctx) error {
        return c.SendString("Hello, World!")
    })

    // Start the server
    app.Listen(":3000")
}
