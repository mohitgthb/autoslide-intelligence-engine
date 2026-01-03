const express = require("express");
const router = express.Router();
const { register, login} = require("../controllers/auth.controller");
const authMiddleware = require("../middleware/auth.middleware");

router.post("/register", register);
router.post("/login", authMiddleware, login);

module.exports = router;