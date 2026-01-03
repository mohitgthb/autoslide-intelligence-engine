// step 3: Controller after model and db connection

const User = require("../models/User");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");

//Register User
exports.register = async (req, res) => {
    const {name, email, password} = req.body;

    try {
        let user = await User.findOne({email});
        if(user){
            return res.status(400).json({ msg: "User already exists"});
        }
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        user = await User.create({
            name,
            email,
            password: hashedPassword
        });
        
        const token = jwt.sign(
            {id: user._id},
            process.env.JWT_SECRET,
            {expiresIn: "1d"}
        );

        res.json({ token });

    } catch (err) {
        console.error(err.message);
        res.status(500).json({ msg: "Server error"});
    }
}; 

// Login 
exports.login = async (req, res) => {
    const {email, password} = req.body;

    try {
        const user = await User.findOne({email});
        if(!user){
            return res.status(400).json({msg: "Invalid Credentials"});
        }
        const isMatch = await bcrypt.compare(password, user.password);
        if(!isMatch){
            return res.status(400).json({msg: "Invalid Credentials"});
        }

        const token = jwt.sign(
            {id: user._id},
            process.env.JWT_SECRET,
            {expiresIn: "1d"}
        );

        res.json({ token });
    } catch (err) {
        res.status(500).json({ msg: "Server error" });
    }
};