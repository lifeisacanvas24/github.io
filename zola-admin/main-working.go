package main

import (
    "log"
    "time"

    "github.com/gofiber/fiber/v2"
    "github.com/gofiber/jwt/v3"
    "github.com/golang-jwt/jwt/v4"
)

const jwtSecret = "L1f315AcanV45" // Use a secure key

type User struct {
    Username string `json:"username"`
    Password string `json:"password"`
}

// In-memory user store (for demo purposes; use a database in production)
var users = map[string]string{
    "admin": "password123", // In a real app, store hashed passwords
}

func main() {
    app := fiber.New()

    // Public route (login)
    app.Post("/login", login)

    // Private routes (authenticated)
    app.Use(jwtware.New(jwtware.Config{
        SigningKey: []byte(jwtSecret),
    }))

    app.Get("/profile", profile)

    log.Fatal(app.Listen(":3000"))
}

func login(c *fiber.Ctx) error {
    var user User

    if err := c.BodyParser(&user); err != nil {
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
            "error": "Cannot parse JSON",
        })
    }

    // Check credentials
    if password, ok := users[user.Username]; !ok || password != user.Password {
        return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
            "error": "Invalid credentials",
        })
    }

    // Create JWT
    token := jwt.New(jwt.SigningMethodHS256)
    claims := token.Claims.(jwt.MapClaims)
    claims["username"] = user.Username
    claims["exp"] = time.Now().Add(time.Hour * 72).Unix()

    t, err := token.SignedString([]byte(jwtSecret))
    if err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
            "error": "Could not login",
        })
    }

    return c.JSON(fiber.Map{
        "token": t,
    })
}

func profile(c *fiber.Ctx) error {
    user := c.Locals("user").(*jwt.Token)
    claims := user.Claims.(jwt.MapClaims)
    username := claims["username"].(string)

    return c.JSON(fiber.Map{
        "message": "Welcome " + username,
    })
}
